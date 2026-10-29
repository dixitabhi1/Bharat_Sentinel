"""
Naval Intelligence Specialist Agent.
Monitors maritime telemetry, carrier strike groups, and EEZ incursions.
"""
from typing import Dict, Any, List, Optional
try:
    from ..db.database import db
except (ImportError, ValueError):
    from db.database import db

class NavalIntelligenceAgent:
    def __init__(self):
        self.name = "Naval Intelligence Agent"
        self.status = "active"

    def analyze_vessel(self, event_data: Dict[str, Any], matching_zones: List[str] = None) -> Dict[str, Any]:
        """Analyzes a maritime event or contact for tactical anomalies."""
        loc = event_data.get("location", {})
        lat = loc.get("lat", 0.0)
        lon = loc.get("lon", 0.0)
        
        is_eez = (5.0 <= lat <= 22.0 and 65.0 <= lon <= 95.0)
        is_chokepoint = bool(matching_zones and any("Chokepoint" in z or "Strait" in z for z in matching_zones))
        
        return {
            "agent": self.name,
            "in_eez": is_eez,
            "in_strategic_chokepoint": is_chokepoint,
            "tactical_alert": is_chokepoint or is_eez
        }

    async def analyze_vessel_telemetry(self, vessel: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes a maritime vessel contact for tactical anomalies."""
        lat = vessel.get("lat", 0.0)
        lon = vessel.get("lon", 0.0)
        speed = vessel.get("speed_knots", 0.0)
        
        is_eez = (5.0 <= lat <= 22.0 and 65.0 <= lon <= 95.0)
        is_chokepoint = (5.0 <= lat <= 8.0 and 78.0 <= lon <= 82.0) or (11.0 <= lat <= 14.0 and 92.0 <= lon <= 94.0)
        
        anomaly = False
        reasons = []
        if is_chokepoint and speed < 3.0:
            anomaly = True
            reasons.append("Loitering near strategic maritime chokepoint")
        if vessel.get("vessel_type") == "survey" and is_eez:
            anomaly = True
            reasons.append("Foreign survey/research ship inside Exclusive Economic Zone")
            
        return {
            "vessel_id": vessel.get("mmsi") or vessel.get("name"),
            "is_anomaly": anomaly,
            "reasons": reasons,
            "tactical_assessment": "Verified" if not anomaly else "Heightened Surveillance Required"
        }

naval_agent = NavalIntelligenceAgent()
