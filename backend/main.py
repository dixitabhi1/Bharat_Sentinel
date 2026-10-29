import os
import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure both backend directory and parent directory are on sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
if str(backend_dir.parent) not in sys.path:
    sys.path.insert(0, str(backend_dir.parent))

try:
    from .api.rest import router as rest_router
    from .api.ws import router as ws_router
    from .skills_loader import skills_registry
    from .geofence.prefilter import geofence_engine
except (ImportError, ValueError):
    from api.rest import router as rest_router
    from api.ws import router as ws_router
    from skills_loader import skills_registry
    from geofence.prefilter import geofence_engine

app = FastAPI(
    title="Bharat Sentinel API",
    description="Live Global & Regional Intelligence & Multi-Agent Situational-Awareness Platform",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Enable CORS for frontend development and Vercel services deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router)
app.include_router(ws_router)

@app.on_event("startup")
async def startup_event():
    print("================================================================")
    print("   BHARAT SENTINEL — GLOBAL & REGIONAL INTELLIGENCE MATRIX      ")
    print("================================================================")
    print(f"[Core] Specialist Skills Loaded: {len(skills_registry.skills)}")
    for s_name in skills_registry.skills:
        print(f"  - Specialist Agent Skill: {s_name}")
    print(f"[Core] Geofence Zones Loaded: {len(geofence_engine.zones)}")
    print("[Core] Ready to receive telemetry & RAG queries on :8000")
    print("================================================================")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
