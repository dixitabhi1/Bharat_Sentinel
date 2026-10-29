# Bharat Sentinel — Complete Project Recreation & Architecture Blueprint

> **System Designation**: Bharat Sentinel Multi-Domain Strategic OSINT & Situational Intelligence Command Platform  
> **Repository Location**: `c:\Users\ACER\Downloads\bharat-sentinel`  
> **Status**: Fully Reconstructed & Verified

---

## 1. System Overview

**Bharat Sentinel** is an open-source intelligence (OSINT) and situational awareness platform built for defense analysts, strategic researchers, and operations centers. It provides real-time multi-domain tracking of:
- **Global & Indian Airspace Telemetry**: Rotated GPU vector aircraft silhouettes with live aviation altitude heatmaps (`0` to `40,000+` ft), true heading alignment, and 60 FPS kinematic smoothing.
- **Naval Fleets & Carrier Strike Groups (CSGs)**: 18 verified worldwide strike groups (US Navy 5th/6th/7th Fleets, Russian Northern/Med/Pacific, PLA Navy Liaoning/Shandong/Fujian, NATO SNMG1/2, EU Aspides, UK, France, Italy, India, Pakistan) verified via official naval press releases and dispatches.
- **Strategic Air & Naval Military Bases**: 46 global military installations across 10 global powers with runway counts, active fighter squadrons, and homeported warship rosters.
- **Dynamic Combat Radius & Marked Radar Boundaries**: Mathematical multi-tier concentric rings (100%, 75%, 50%, 25%) indicating fighter jet combat strike radius and radar coverage envelopes.
- **Multi-Agent AI Intelligence Engine**: Specialized multi-agent system (Air Anomaly Agent, Naval Agent, Troop Buildup Agent, Diplomatic Posture Agent, India-Impact Classifier, and RAG Geopolitics Chatbot).

---

## 2. Complete Directory Structure

```text
bharat-sentinel/
├── README.md                           # Project mission & feature highlights
├── TRD.md                              # Technical Requirements Document
├── start_all.ps1                       # One-click dual-stack startup script
├── PROJECT_RECREATION_GUIDE.md         # This recreation blueprint
├── config/
│   └── .env.example                    # Environment configuration template
├── agents/                             # Agent specification markdown files
│   ├── chatbot-agent.md
│   ├── orchestrator-agent.md
│   └── specialist-agents-index.md
├── apis/                               # Open API catalog documentation
│   └── api-catalog.md
├── knowledge/                          # Ethical charter & UI/UX design tokens
│   ├── disclaimer-and-ethics.md
│   ├── installations-layer.md
│   ├── reference-project-gods-eye-view.md
│   └── ui-ux-design-system.md
├── backend/                            # FastAPI Python Backend
│   ├── main.py                         # Application entrypoint & CORS middleware
│   ├── requirements.txt                # Python dependencies
│   ├── skills_loader.py                # Dynamic agent skill prompt loader
│   ├── STRUCTURE.md                    # Backend architecture documentation
│   ├── api/
│   │   ├── rest.py                     # REST endpoints (/api/health, /api/flights/live, etc.)
│   │   └── ws.py                       # WebSocket endpoint (/ws/live) emitting 4s ticks
│   ├── db/
│   │   └── database.py                 # Core intelligence store (Bases, Fleets, Leaders, Flights)
│   ├── geofence/
│   │   ├── prefilter.py                # Deterministic spatial geofence pre-filter
│   │   └── regions.geojson             # GeoJSON boundaries (EEZ, LAC, LoC, Chokepoints)
│   ├── ingestion/
│   │   ├── flights_proxy.py            # Airplanes.live v2 clusters + mil feed + failover
│   │   ├── flights_opensky.py          # OpenSky Network fallback adapter
│   │   ├── ships_aisstream.py          # Live AIS maritime vessel stream
│   │   └── installations_osm.py        # OpenStreetMap military installations catalog
│   └── agents/
│       ├── orchestrator.py             # Event fan-out and classification pipeline
│       ├── flight_anomaly_agent.py     # ADS-B tactical loiter/incursion detector
│       ├── naval_agent.py              # Maritime chokepoint & EEZ patrol detector
│       ├── troop_buildup_agent.py      # Border buildup & fortification analyzer
│       ├── leader_statement_agent.py   # Diplomatic posture & deterrence analyzer
│       ├── india_impact_classifier.py  # 1-4 severity & confidence scoring rubric
│       └── chatbot_agent.py            # RAG geopolitical assistant with strict safety guardrails
├── frontend/                           # React 18 + Vite Frontend
│   ├── index.html                      # HTML5 shell with Google Cyber Fonts
│   ├── package.json                    # NPM dependencies (React, Vite, MapLibre GL, Lucide)
│   ├── vite.config.js                  # Vite configuration & dev server proxy
│   └── src/
│       ├── main.jsx                    # React DOM root hydration
│       ├── App.jsx                     # Top-level state coordinator & tab switcher
│       ├── index.css                   # Cyber tactical design system & scanlines
│       └── components/
│           ├── TacticalMap.jsx         # MapLibre GL GPU radar, SDF planes, drawers, rings
│           ├── Header.jsx              # Command HUD, scope toggles, search, tickers
│           ├── ThreatFeed.jsx          # Live intelligence feed & severity indicators
│           ├── ChatbotConsole.jsx      # 'Ask Bharat Sentinel' RAG chatbot console
│           ├── AgentNeuralHUD.jsx      # Neural agent pipeline visualizer
│           ├── DomesticStability.jsx   # Theater status matrix & internal security index
│           ├── ReviewQueueModal.jsx    # Human-in-the-loop analyst review queue modal
│           ├── EventSimulatorModal.jsx # Multi-agent event injector & scenario simulator
│           └── SplashScreen.jsx        # Cyber boot sequence splash screen
└── scratch/
    ├── restore_bharat_sentinel.py      # Automated project rebuilder
    └── verify_all.py                   # Automated end-to-end verification test suite
```

---

## 3. Step-by-Step Installation & Setup

### Prerequisites
1. **Python 3.10+**: Ensure `python` and `pip` are accessible in your PATH.
2. **Node.js 18+ & npm**: Ensure `node` and `npm` are installed.

---

### Step 3.1 — Backend Setup

1. Open PowerShell or Terminal and navigate to the project root:
   ```powershell
   cd c:\Users\ACER\Downloads\bharat-sentinel
   ```
2. Install Python dependencies:
   ```powershell
   pip install fastapi uvicorn websockets httpx pydantic shapely
   ```
3. Test backend loading:
   ```powershell
   python -c "from backend.main import app; print('Backend loaded successfully:', app.title)"
   ```
4. Start the FastAPI server on port 8000:
   ```powershell
   python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   - API Health: `http://localhost:8000/api/health`
   - Interactive Swagger Docs: `http://localhost:8000/docs`

---

### Step 3.2 — Frontend Setup

1. Navigate to the `frontend/` directory:
   ```powershell
   cd c:\Users\ACER\Downloads\bharat-sentinel\frontend
   ```
2. Install Node dependencies:
   ```powershell
   npm install
   ```
3. Run the Vite development server:
   ```powershell
   npm run dev -- --host
   ```
4. Open the live tactical dashboard in your web browser:
   **`http://localhost:5173/`**

---

### Step 3.3 — One-Click Dual Launch (`start_all.ps1`)

From the project root, simply execute:
```powershell
.\start_all.ps1
```
This opens two independent PowerShell windows (Backend on `:8000` and Frontend on `:5173`) and automatically opens your browser.

---

## 4. Automated System Verification

To run full end-to-end automated tests verifying all endpoints, databases, and flight feeds:
```powershell
python scratch/verify_all.py
```
