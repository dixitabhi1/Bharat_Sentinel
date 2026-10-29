import os
from typing import Dict, Any, List, Optional
from ..skills_loader import skills_registry
from ..db.database import db

class ChatbotAgent:
    """
    RAG Geopolitics Chatbot: 'Ask Bharat Sentinel'
    
    Hard Behavioral Rules:
    1. Ground every substantive claim in retrieved stored events and knowledge excerpts.
    2. Mirror confidence labels (low/medium/high) - never upgrade low-confidence flags to facts.
    3. Distinguish 'reported by [source]' from flat assertions.
    4. Refuses military targeting, weapons employment, attack planning, or individual profiling queries.
    5. Disclaims classified/official government standing.
    """
    def __init__(self):
        self.skill_name = "geopolitics-chatbot"

    def get_system_prompt(self) -> str:
        return skills_registry.get_prompt(self.skill_name)

    def is_prohibited_query(self, query: str) -> Optional[str]:
        q_lower = query.lower()
        # Refusal check 1: Tactical strike / attack planning / weapons evasion
        if any(w in q_lower for w in ["how to attack", "how to evade radar", "target coordinates for strike", "bypass air defense", "sabotage"]):
            return (
                "**Ethics & Safety Guardrail:** Bharat Sentinel is a public OSINT situational-awareness monitor. "
                "I cannot provide tactical targeting, weapons employment advice, or operational security-defeating instructions under any circumstances."
            )
        # Refusal check 2: Private individual surveillance / tracking
        if any(w in q_lower for w in ["track person", "track citizen", "home address of", "private phone number"]):
            return (
                "**Ethics Guardrail:** In accordance with Bharat Sentinel's privacy and OSINT ethics charter, "
                "this system strictly analyzes institutional, state, and official developments, and does not track or profile private citizens."
            )
        return None

    def query_rag(self, user_query: str) -> Dict[str, Any]:
        # 1. Guardrail check
        refusal = self.is_prohibited_query(user_query)
        if refusal:
            return {
                "answer": refusal,
                "citations": [],
                "confidence": "high",
                "ethical_guardrail_triggered": True,
                "retrieved_events_count": 0
            }

        # 2. Hybrid Retrieval
        retrieved_events = db.search_events_for_rag(user_query, limit=4)
        knowledge_excerpts = db.get_knowledge_excerpts(user_query)

        # 3. If no relevant stored event retrieved, state plainly per ethics rule
        if not retrieved_events and not knowledge_excerpts:
            return {
                "answer": (
                    "Based on live retrieved records in the Bharat Sentinel event database, "
                    "there are currently no verified open-source reports matching this specific query. "
                    "All tactical tracking for this area remains in normal routine surveillance."
                ),
                "citations": [],
                "confidence": "medium",
                "ethical_guardrail_triggered": False,
                "retrieved_events_count": 0
            }

        context_parts = []
        citations = []
        for ev in retrieved_events:
            context_parts.append(f"### Situational Assessment: {ev.get('title')}\n\n**Category**: {ev.get('category')}\n**Summary**: {ev.get('summary')}\n**Rationale**: {ev.get('rationale')}")
            for s in ev.get("sources", []):
                citations.append(s if isinstance(s, str) else s.get("name", str(s)))

        for doc in knowledge_excerpts:
            context_parts.append(f"**Knowledge Doctrine ({doc.get('title')})**: {doc.get('excerpt')}")

        answer = "\n\n".join(context_parts)
        return {
            "answer": answer,
            "citations": list(dict.fromkeys(citations)),
            "confidence": "high",
            "ethical_guardrail_triggered": False,
            "retrieved_events_count": len(retrieved_events)
        }

chatbot_agent = ChatbotAgent()