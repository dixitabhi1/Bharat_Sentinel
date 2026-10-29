# Backend Directory Structure

This document outlines the Python backend architecture for **Bharat Sentinel**.

```
backend/
├── main.py                 # FastAPI application entrypoint, CORS, static routes
├── skills_loader.py        # Dynamic loader/parser for specialist SKILL.md system prompts
├── api/
│   ├── rest.py             # REST endpoints (/api/stats, /api/events, /api/fleets, etc.)
│   └── ws.py               # WebSocket broadcaster for real-time telemetry stream
├── db/
│   └── database.py         # Intelligence store (events, flags, fleets, leaders, flights)
├── geofence/
│   ├── polygons.py         # Shapely coordinates for LAC, LoC, EEZ, Hormuz, Malacca
│   └── prefilter.py        # Spatial intersection engine
├── agents/
│   ├── orchestrator.py     # Multi-agent coordinator
│   ├── specialist_agents.py# Domain-specific specialist agents
│   └── chatbot_agent.py    # RAG Geopolitical analyst
└── ingestion/              # Ingestion connectors (OpenSky, AISStream, GDELT, USGS)
```

`skills_loader.py` is the bridge: it reads the same `SKILL.md` files and uses their body content as the system prompt for the corresponding backend agent class, so the spec and the running system never drift apart.
