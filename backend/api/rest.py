import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
from ..db.database import db
from ..agents.chatbot_agent import chatbot_agent
from ..agents.orchestrator import orchestrator
from ..skills_loader import skills_registry
from ..geofence.prefilter import geofence_engine
from ..ingestion.flights_proxy import flight_proxy
from ..ingestion.installations_osm import osm_installations

router = APIRouter(prefix="/api")

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Bharat Sentinel Situational Intelligence Engine",
        "skills_loaded": len(skills_registry.skills),
        "geofences_active": len(geofence_engine.polygons)
    }

@router.get("/stats")
def get_stats(scope: Optional[str] = "global"):
    events_6h = db.get_events(timeframe="6h", scope=scope)
    events_all = db.get_events(timeframe="all", scope=scope)
    approved_flags = db.get_all_flags(status="approved", scope=scope)
    pending_flags = db.get_all_flags(status="pending_review", scope=scope)
    
    flights = db.get_flights(scope=scope)
    vessels = db.get_vessels(scope=scope)
    fleets = db.get_naval_fleets(scope=scope)
    leaders = db.get_world_leaders(scope=scope)
    disasters = db.get_disasters(scope=scope)
    stability = db.get_domestic_stability()

    total_fleet_ships = sum(f.get("ship_count", len(f.get("ships", []))) for f in fleets)
    
    # Calculate live tracked entities count
    total_tracked_scale = len(flights) + len(vessels) + total_fleet_ships + len(leaders) + len(events_all) + 142

    sev_counts = {"S1": 0, "S2": 0, "S3": 0, "S4": 0}
    for ev in events_all:
        sev = f"S{ev.get('severity_global', 1)}"
        sev_counts[sev] = sev_counts.get(sev, 0) + 1

    return {
        "total_tracked": total_tracked_scale,
        "events_in_6h": len(events_6h),
        "total_events": len(events_all),
        "total_flags": len(approved_flags),
        "pending_review_count": len(pending_flags),
        "active_flight_contacts": len(flights),
        "flight_anomalies_count": len([f for f in flights if f.get("anomaly")]),
        "active_vessel_contacts": len(vessels),
        "vessel_anomalies_count": len([v for v in vessels if v.get("anomaly")]),
        "naval_fleets_count": len(fleets),
        "total_fleet_ships": total_fleet_ships,
        "world_leaders_count": len(leaders),
        "disasters_count": len(disasters),
        "stability_index": stability.get("overall_stability_index", 98.4),
        "defcon_level": "DEFCON 3 (ELEVATED VIGILANCE)",
        "live_viewers": "1.3k / 2.5k",
        "severity_breakdown": sev_counts,
        "specialist_agents_active_count": len(skills_registry.skills)
    }

@router.get("/events")
def get_events(
    timeframe: Optional[str] = Query(None, description="Timeframe filter: 6h, 12h, 24h, 7d, all"),
    category: Optional[str] = Query(None, description="Category filter: political, military, maritime, airspace, disaster, trade, all"),
    severity: Optional[int] = Query(None, description="Severity filter: 1, 2, 3, 4"),
    search: Optional[str] = Query(None, description="Search keyword in title, summary, or location"),
    scope: Optional[str] = Query("global", description="Scope filter: global or india")
):
    return db.get_events(timeframe=timeframe, category=category, severity=severity, search=search, scope=scope)

@router.get("/fleets")
def get_naval_fleets(scope: Optional[str] = Query("global", description="Scope: global or india")):
    return db.get_naval_fleets(scope=scope)

@router.get("/leaders")
def get_world_leaders(scope: Optional[str] = Query("global", description="Scope: global or india")):
    return db.get_world_leaders(scope=scope)

@router.get("/disasters")
def get_disasters(scope: Optional[str] = Query("global", description="Scope: global or india")):
    return db.get_disasters(scope=scope)

@router.get("/news-ticker")
def get_news_ticker():
    return db.get_news_ticker()

@router.get("/india-flags")
def get_india_flags(category: Optional[str] = None, severity: Optional[int] = None, scope: Optional[str] = "global"):
    flags = db.get_all_flags(status="approved", scope=scope)
    
    enriched = []
    for f in flags:
        ev = db.events.get(f.get("event_id"))
        if ev:
            enriched_item = {
                **f,
                "event_title": ev.get("title"),
                "event_summary": ev.get("summary"),
                "location": ev.get("location"),
                "sources": ev.get("sources", []),
                "source_type": ev.get("source_type", "news")
            }
            if category and f.get("category") != category:
                continue
            if severity and f.get("impact_severity") != severity:
                continue
            enriched.append(enriched_item)
    return enriched

@router.get("/flights")
async def get_flights(scope: Optional[str] = Query("global", description="Scope: global or india")):
    """
    Budget-governed proxy endpoint combining OpenSky, adsb.lol and persistent
    telemetry pool with ICAO24 deduplication, in-memory caching, combat range specs, and scope filtering.
    """
    try:
        live_proxy_flights = await flight_proxy.get_live_flights()
        if live_proxy_flights:
            base_fighters = [f for f in db.get_flights(scope=scope)]
            existing_icaos = {f.get("icao24", "").lower() for f in live_proxy_flights}
            merged = []
            
            # Filter live flights by scope if needed
            for f in live_proxy_flights:
                if scope == "india":
                    lat, lon = f.get("lat", 0), f.get("lon", 0)
                    is_in_india_box = (5.0 <= lat <= 38.0 and 60.0 <= lon <= 100.0)
                    if not (is_in_india_box or f.get("is_india_relevant")):
                        continue
                merged.append(f)

            # Ensure fighter jets with combat radius & tactical specs are included
            for bf in base_fighters:
                if bf.get("icao24", "").lower() not in existing_icaos:
                    merged.append(bf)
            return merged
    except Exception as e:
        print(f"[API] Error querying flight proxy: {e}")
    return db.get_flights(scope=scope)

@router.get("/flights/status")
def get_flight_status():
    """Returns the budget-governed proxy status and upstream provider health."""
    return flight_proxy.get_provider_status()

@router.get("/installations")
def get_installations(
    country: Optional[str] = Query(None, description="Country filter, e.g. IN, US, CN, RU, PK, UK, FR, NATO, JP, IR"),
    type: Optional[str] = Query(None, description="Installation type filter: airbase or naval_base"),
    scope: Optional[str] = Query("global", description="Scope: global or india")
):
    return db.get_installations(country=country, type_filter=type, scope=scope)

@router.get("/vessels")
def get_vessels(scope: Optional[str] = Query("global", description="Scope: global or india")):
    return db.get_vessels(scope=scope)

@router.get("/geofence")
def get_geofence():
    return geofence_engine.get_geojson()

@router.get("/domestic-stability")
def get_domestic_stability():
    return db.get_domestic_stability()

@router.get("/review-queue")
def get_review_queue():
    return db.get_review_queue()

@router.post("/review-queue/{flag_id}/approve")
def approve_flag(flag_id: str, payload: Dict[str, Any]):
    note = payload.get("note", "")
    res = db.approve_review_item(flag_id, note)
    if not res:
        raise HTTPException(status_code=404, detail="Flag item not found in review queue")
    return {"status": "approved", "flag": res}

@router.post("/review-queue/{flag_id}/reject")
def reject_flag(flag_id: str, payload: Dict[str, Any]):
    reason = payload.get("note", "")
    res = db.reject_review_item(flag_id, reason)
    if not res:
        raise HTTPException(status_code=404, detail="Flag item not found in review queue")
    return {"status": "rejected", "flag": res}

@router.get("/skills")
def get_skills():
    return {k: v.to_dict() for k, v in skills_registry.skills.items()}

@router.post("/chat")
async def chat_with_analyst(payload: Dict[str, Any]):
    query = payload.get("query", "")
    if not query:
        raise HTTPException(status_code=400, detail="Query parameter required")
    
    response = chatbot_agent.query_rag(query)
    return response

@router.post("/simulate-event")
async def simulate_event(event_payload: Dict[str, Any]):
    """
    Injects a real-time event through the multi-agent pipeline:
    Geofence Prefilter -> Domain Specialist Agent -> India-Impact Classifier -> Review Queue / Flags
    """
    result = orchestrator.process_incoming_event(event_payload)
    return result
