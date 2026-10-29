        │  Realtime push (WS) →      │        │  Chatbot Agent (RAG)      │
        │  India dashboard            │◄──────►│  retrieves from events +  │
        └────────────────────────────┘        │  india_flags + knowledge/ │
                                               └─────────────────────────┘
```

## 2. Agentic Design

Each agent is implemented as an **Antigravity Skill** under `.agents/skills/<name>/SKILL.md` — this lets the orchestrator (a long-running backend service, not the IDE agent) reuse the exact same instructions/knowledge that a human developer working in Antigravity would see, keeping "how the system behaves" and "how the code was built" in sync. At runtime, each skill's SKILL.md is loaded as the system prompt for a corresponding LLM worker (they don't have to literally run inside Antigravity — the skill file format is just markdown+YAML, easily loaded by any backend).

### 2.1 Orchestrator Agent (`agents/orchestrator-agent.md`)
- Subscribes to the base `events` table's publish stream (Redis pub/sub, per base TRD).
- For every new/updated event, determines which of the specialist agents are relevant (a flight-type raw report → Flight Anomaly Agent; a ship AIS burst → Naval Agent; a news article → also runs India-Impact Classifier directly since news doesn't need a domain-specific pre-agent).
- Fans out to the relevant specialist agent(s) in parallel, collects their structured outputs, and passes the union to the India-Impact Classifier Agent for the final scoring pass.
- Writes the result to `india_flags` and re-publishes on a `india-flags` Redis channel for the dashboard's WebSocket layer.
