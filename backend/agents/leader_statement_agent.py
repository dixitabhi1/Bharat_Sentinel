from typing import Dict, Any

class LeaderStatementAgent:
    def __init__(self):
        self.name = "Leader & Diplomatic Posture Agent"

    def analyze_statement(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        text = f"{event_data.get('title', '')} {event_data.get('summary', '')}".lower()
        
        stance = "neutral"
        if any(w in text for w in ["condemn", "unacceptable", "sovereignty", "provocation", "retaliate"]):
            stance = "firm_deterrence"
        elif any(w in text for w in ["dialogue", "peaceful", "disengagement", "cooperation", "bilateral"]):
            stance = "de_escalatory"

        return {
            "agent": self.name,
            "diplomatic_stance": stance,
            "official_channel_confirmed": any(w in text for w in ["mea", "pib", "spokesperson", "mod"])
        }

leader_statement_agent = LeaderStatementAgent()
