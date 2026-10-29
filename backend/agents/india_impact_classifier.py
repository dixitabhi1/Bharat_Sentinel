from typing import Dict, Any, List, Optional
from ..skills_loader import skills_registry

class IndiaImpactClassifier:
    """
    Final synthesis and scoring stage for Bharat Sentinel.
    Takes base event + specialist agent outputs, applies the taxonomy from
    knowledge/severity-and-confidence-taxonomy.md, and produces the india_flags record.
    
    Rubric Rules:
    - Sets category from: naval_ior | airspace | border_lac_loc | diplomatic | economic_trade | cyber_infra | domestic_stability
    - Assigns impact_severity (1-4)
    - Assigns confidence (low | medium | high) based on independent corroboration
    - Generates explainable rationale citing specific signals and sources
    - Sets route_to_human_review = True if severity == 4 OR (severity == 3 and confidence != 'high')
    """
    def __init__(self):
        self.skill_name = "india-impact-classifier"

    def get_system_prompt(self) -> str:
        return skills_registry.get_prompt(self.skill_name)

    def classify_and_score(
        self,
        event: Dict[str, Any],
        specialist_outputs: Dict[str, Any],
        geofence_zones: List[str] = None
    ) -> Dict[str, Any]:
        geofence_zones = geofence_zones or []
        title = event.get("title", "")
        summary = event.get("summary", "")
        sources = event.get("sources", [])
        source_type = event.get("source_type", "news")
        
        # 1. Determine Category
        category = "diplomatic"
        if "flight_anomaly_agent" in specialist_outputs or any(z in ["lac_buffer", "loc_buffer"] for z in geofence_zones) and source_type == "flight_raw":
            category = "airspace"
        elif "naval_agent" in specialist_outputs or any(z in ["arabian_sea", "bay_of_bengal", "strait_of_hormuz", "strait_of_malacca"] for z in geofence_zones):
            category = "naval_ior"
        elif "troop_buildup_agent" in specialist_outputs or any(z in ["lac_buffer", "loc_buffer"] for z in geofence_zones):
            category = "border_lac_loc"
        elif any(w in title.lower() for w in ["trade", "tariff", "crude", "energy", "rupee", "chokepoint", "shipping"]):
            category = "economic_trade"
        elif any(w in title.lower() for w in ["cyber", "radar", "outage", "cable", "telecom"]):
            category = "cyber_infra"

        # 2. Determine Severity (1 to 4)
        severity = 2
        text = f"{title} {summary}".lower()
        if any(w in text for w in ["strike", "clash", "casualty", "confrontation", "missile launch", "intercept"]):
            severity = 4
        elif any(w in text for w in ["scramble", "incursion", "standoff", "violation", "alert", "drills near border"]):
            severity = 3
        elif any(w in text for w in ["meeting", "bilateral", "statement", "delegation"]):
            severity = 1

        # 3. Determine Confidence
        confidence = "medium"
        if len(sources) >= 2 or any("pib" in s.lower() or "mod" in s.lower() or "navy" in s.lower() for s in sources):
            confidence = "high"
        elif len(sources) == 0:
            confidence = "low"

        route_to_human_review = (severity == 4) or (severity == 3 and confidence != "high")

        rationale = f"Classified under {category} at Severity {severity} based on detected tactical cues in {len(sources)} independent sources."

        return {
            "category": category,
            "impact_severity": severity,
            "confidence": confidence,
            "rationale": rationale,
            "route_to_human_review": route_to_human_review,
            "is_india_relevant": True
        }

india_impact_classifier = IndiaImpactClassifier()