# Bharat Sentinel — Global & Regional Situational Awareness OSINT Platform

> **Live Global & Regional Situation Room & Multi-Agent Situational-Awareness Engine**  
> Centered on India and the Indian Ocean Region (IOR), grounded in verified multi-source open data.

---

## 1. System Overview

**Bharat Sentinel** aggregates open-source intelligence (OSINT) across air, naval, border, diplomatic, and infrastructure vectors. Every incoming signal passes through a deterministic geofencing pre-filter and is analyzed by specialist agents powered directly by **Specialist Agent Skills** (`.agents/skills/*`), before being scored by an **India-Impact Classifier** and surfaced onto an interactive, futuristic command deck.

### Core Modules
1. **Interactive Geospatial Operations Matrix**: Photorealistic satellite hybrid and tactical map rendering strategic geofences (LAC corridor, LoC buffer, India EEZ, Arabian Sea, Bay of Bengal, Strait of Hormuz, Strait of Malacca), real-time ADS-B aircraft vectors, USNI/Naval Fleet strike groups, and AIS maritime traffic with anomaly indicators.
2. **Global & Regional Threat Feed**: Real-time ticker and left drawer categorizing events (Political, Military, Maritime, Airspace, Disaster, Trade) with explainable rationales and confidence ratings.
3. **World Leader & Naval Fleet Trackers**: Pinned leader headshot avatars with statement sentiment analysis and floating fleet cluster dossiers.
4. **Ask Bharat Sentinel (RAG Geopolitics AI)**: Sourced RAG chatbot grounded strictly in live database events and strategic geography definitions.
5. **Domestic Stability & Resilience Dashboard**: Positive-framing state wellness index monitoring Cloudflare internet connectivity, NDMA public disaster bulletins, port cargo flow, and national power grid frequency.
6. **Specialist Multi-Agent Neural HUD**: Inspector displaying all loaded specialist agent skills, runtime reasoning status, and dynamic system prompts (`SKILL.md`).
7. **Human Analyst Review Gatekeeper**: Gatekeeper console enforcing review policy for Tier 4 (Major) and uncorroborated Tier 3 signals before public dissemination.

---

## 2. Multi-Agent Architecture

```
[ Ingestions: ADS-B (OpenSky) | AIS (AISStream) | GDELT/RSS | USGS | FIRMS | Cloudflare ]
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │ Deterministic Geofencing  │  (Shapely Polygon Pre-Filter)
                    └─────────────┬─────────────┘
                                  │
                                  ▼
        ┌────────────────────────────────────────────────────────┐
        │                 SPECIALIST AGENT LAYER                 │
        │                                                        │
        │  • Flight Anomaly Agent       (.agents/skills/flight...)│
        │  • Naval / Maritime Agent     (.agents/skills/naval...) │
        │  • Troop / Buildup Agent      (.agents/skills/troop...) │
        │  • Leader Statement Agent     (.agents/skills/leader...)│
        │  • Severity Scoring Helper    (.agents/skills/event...) │
        └─────────────────────────┬──────────────────────────────┘
                                  │
                                  ▼
        ┌────────────────────────────────────────────────────────┐
        │            INDIA-IMPACT CLASSIFIER AGENT               │
        │                                                        │
        │  • impact_severity: 1 (Routine) to 4 (Major)           │
        │  • confidence: low | medium | high                     │
        │  • explainable natural language rationale               │
        │  • human review gate for Tier 4 / uncorroborated Tier 3│
        └─────────────────────────┬──────────────────────────────┘
                                  │
                  ┌───────────────┴───────────────┐
                  ▼                               ▼
      ┌───────────────────────┐       ┌────────────────────────┐
      │   Database Store &    │       │ RAG Chatbot Assistant  │
      │   WebSocket Stream    │◄─────►│ "Ask Bharat Sentinel"  │
      └───────────────────────┘       └────────────────────────┘
```

---

## 3. Quick Start & Execution

### Prerequisites
- **Python 3.10+** (with `fastapi`, `uvicorn`, `shapely`, `pyyaml`, `httpx`, `websockets`, `python-dotenv`)
- **Node.js 18+** & **npm**

### Option A: One-Click Startup (PowerShell)
```powershell
.\start_all.ps1
```

### Option B: Manual Startup

**Terminal 1 — Backend API:**
```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 — Frontend App:**
```bash
cd frontend
npm run dev
```

Open your browser at **`http://localhost:5173`**.

---

## 4. Key Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health and loaded skills count |
| `GET` | `/api/stats` | Aggregated threat stats & tracked count |
| `GET` | `/api/events` | Multi-source event feed with timeframe filter |
| `GET` | `/api/fleets` | USNI / Naval Fleet strike groups and warships |
| `GET` | `/api/leaders` | World leaders, coordinates, and statements |
| `GET` | `/api/disasters` | USGS earthquakes & environmental alerts |
| `GET` | `/api/news-ticker` | Real-time breaking headlines for marquee |
| `GET` | `/api/flights` | Live ADS-B aircraft vectors & anomaly flags |
| `GET` | `/api/vessels` | AIS vessel traffic & dark-gap monitoring |
| `GET` | `/api/geofence` | GeoJSON polygons for tactical map |
| `GET` | `/api/domestic-stability` | State resilience & infrastructure indicators |
| `POST` | `/api/chat` | RAG Geopolitical analyst query |
| `GET` | `/api/skills` | Active specialist agent skills and prompts |
| `GET` | `/api/review-queue` | Analyst verification queue |
| `POST` | `/api/simulate-event` | Inject custom telemetry payload |
| `WS` | `/ws/live` | Real-time WebSocket telemetry feed |
