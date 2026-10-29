import os
import uvicorn
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .api.rest import router as rest_router
from .api.ws import router as ws_router
from .skills_loader import skills_registry
from .geofence.prefilter import geofence_engine

app = FastAPI(
    title="Bharat Sentinel API",
    description="Live Global & Regional Intelligence & Multi-Agent Situational-Awareness Platform",
    version="1.0.0"
)

# Enable CORS for frontend development
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
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
