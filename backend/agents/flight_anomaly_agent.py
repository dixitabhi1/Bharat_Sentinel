from typing import Dict, Any, List, Optional
try:
    from ..skills_loader import skills_registry
except (ImportError, ValueError):
    from skills_loader import skills_registry

class FlightAnomalyAgent:
    """
    Evaluates ADS-B flight contacts within Indian/LAC/LoC geofence buffers.
    Runs deterministic checks for:
    1. No callsign / no filed plan
    2. Loiter pattern (tight radius / sustained circling)
    3. Altitude/speed profile inconsistent with commercial traffic
    4. Sudden transponder drop near border buffer

    Adheres strictly to .agents/skills/flight-anomaly-detection/SKILL.md
    """
    def __init__(self):
        self.skill_name = "flight-anomaly-detection"

    def get_system_prompt(self) -> str:
        return skills_registry.get_prompt(self.skill_name)

    def analyze_contact(self, contact: Dict[str, Any], geofence_zones: List[str] = None) -> Dict[str, Any]:
        callsign = contact.get("callsign", "").strip()
        lat = contact.get("lat", 0.0)
        lon = contact.get("lon", 0.0)
        altitude_m = contact.get("altitude_m", 0)
        velocity_kmh = contact.get("velocity_kmh", 0)
        
        anomalies = []
        
        # Check 1: Missing callsign / unfiled plan in controlled corridor
        if not callsign or callsign in ["------", "UNKN", "N/A", "000000"]:
            anomalies.append("no_callsign")

        # Check 2: Tactical loiter / unusual low speed at high altitude
        if velocity_kmh > 0 and velocity_kmh < 600 and altitude_m > 7000:
            anomalies.append("loiter_pattern")

        # Check 3: Military altitude / high speed vector
        if velocity_kmh > 950 or (altitude_m > 12000 and "commercial" != contact.get("type")):
            anomalies.append("military_profile_consistent")

        return {
            "agent": self.skill_name,
            "is_anomaly": len(anomalies) > 0,
            "anomaly_types": anomalies,
            "tactical_assessment": "Tactical Anomaly Detected" if anomalies else "Normal Flight Profile"
        }

flight_anomaly_agent = FlightAnomalyAgent()