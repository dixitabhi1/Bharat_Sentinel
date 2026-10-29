from typing import Dict, Any, List

class TroopBuildupAgent:
    def __init__(self):
        self.name = "Troop Buildup & Fortification Agent"

    def analyze_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        title_summary = f"{event_data.get('title', '')} {event_data.get('summary', '')}".lower()
        
        indicators = []
        is_elevated = False
        
        if any(w in title_summary for w in ["lac", "eastern ladakh", "arunachal", "doklam", "tawang"]):
            indicators.append("Northern/Eastern Border Theater")
            is_elevated = True
            
        if any(w in title_summary for w in ["armor", "t-90", "type 15", "s-400", "airbase", "hardened"]):
            indicators.append("Heavy Armor / Air Defense Deployment")
            is_elevated = True

        return {
            "agent": self.name,
            "tactical_significance": "high" if is_elevated else "routine",
            "indicators": indicators,
            "escalation_risk": "elevated" if is_elevated else "stable"
        }

troop_buildup_agent = TroopBuildupAgent()
