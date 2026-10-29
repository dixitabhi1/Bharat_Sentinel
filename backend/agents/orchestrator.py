import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
try:
    from ..geofence.prefilter import geofence_engine
    from .flight_anomaly_agent import flight_anomaly_agent
    from .naval_agent import naval_agent
    from .troop_buildup_agent import troop_buildup_agent
    from .leader_statement_agent import leader_statement_agent
    from .india_impact_classifier import india_impact_classifier
    from ..db.database import db
except (ImportError, ValueError):
    from geofence.prefilter import geofence_engine
    from agents.flight_anomaly_agent import flight_anomaly_agent
    from agents.naval_agent import naval_agent
    from agents.troop_buildup_agent import troop_buildup_agent
    from agents.leader_statement_agent import leader_statement_agent
    from agents.india_impact_classifier import india_impact_classifier
    from db.database import db

class OrchestratorAgent:
    """
    Subscribes to incoming events, runs deterministic geofence pre-filters,
    dispatches relevant specialist agents in parallel, and runs the final
    India-Impact Classifier before writing to database and live stream.
    """
    def __init__(self):
        pass

    def process_incoming_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        event_id = event_data.get("id") or str(uuid.uuid4())
        event_data["id"] = event_id
        if "created_at" not in event_data:
            event_data["created_at"] = datetime.now(timezone.utc).isoformat()

        # Step 1: Geofence check
        loc = event_data.get("location", {})
        lat = loc.get("lat", 0.0)
        lon = loc.get("lon", 0.0)
        matching_zones = geofence_engine.get_matching_zones(lat, lon)
        
        specialist_outputs = {}
        source_type = event_data.get("source_type", "news")

        # Step 2: Fan out to specialists
        if source_type == "flight_raw" or "flight" in event_data.get("category", ""):
            if geofence_engine.is_in_india_buffer(lat, lon):
                specialist_outputs["flight_anomaly_agent"] = flight_anomaly_agent.analyze_contact(event_data, matching_zones)

        elif source_type == "ais_raw" or "maritime" in event_data.get("category", ""):
            if geofence_engine.is_in_ior_zones(lat, lon):
                specialist_outputs["naval_agent"] = naval_agent.analyze_vessel(event_data, matching_zones)

        elif source_type == "news":
            title_summary = f"{event_data.get('title', '')} {event_data.get('summary', '')}".lower()
            if any(w in title_summary for w in ["troop", "military", "border", "posture", "lac", "loc", "buildup", "shelter", "radar"]):
                specialist_outputs["troop_buildup_agent"] = troop_buildup_agent.analyze_event(event_data)
            
            if any(w in title_summary for w in ["mea", "pib", "ministry", "spokesperson", "statement", "briefing", "minister"]):
                specialist_outputs["leader_statement_agent"] = leader_statement_agent.analyze_statement(event_data)

        # Step 3: India-Impact Classifier final scoring
        flag_result = india_impact_classifier.classify_and_score(event_data, specialist_outputs, matching_zones)
        
        flag_id = str(uuid.uuid4())
        flag_record = {
            "id": flag_id,
            "event_id": event_id,
            **flag_result,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        # Step 4: Write to DB
        db.events[event_id] = event_data
        db.india_flags[flag_id] = flag_record
        if flag_result.get("route_to_human_review"):
            db.review_queue[flag_id] = {
                "flag": flag_record,
                "event": event_data,
                "submitted_at": datetime.now(timezone.utc).isoformat()
            }

        return {
            "event": event_data,
            "flag": flag_record,
            "specialist_outputs": specialist_outputs,
            "routed_to_review": flag_result.get("route_to_human_review", False)
        }

orchestrator = OrchestratorAgent()