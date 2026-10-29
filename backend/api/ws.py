import asyncio
import json
import time
from typing import List, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
try:
    from ..db.database import db
    from ..ingestion.flights_proxy import flight_proxy
except (ImportError, ValueError):
    from db.database import db
    from ingestion.flights_proxy import flight_proxy

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self._background_task = None

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        if self._background_task is None or self._background_task.done():
            self._background_task = asyncio.create_task(self._live_telemetry_loop())

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)

    async def broadcast(self, message: dict):
        dead_connections = set()
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
            except Exception:
                dead_connections.add(connection)
        
        for dead in dead_connections:
            self.active_connections.discard(dead)

    async def _live_telemetry_loop(self):
        """Streams live ADS-B movement and telemetry heartbeat without drops"""
        while len(self.active_connections) > 0:
            try:
                await asyncio.sleep(4)
                if not self.active_connections:
                    break
                
                # Fetch cached high-density flight pool
                flights_pool = flight_proxy.get_cached_flights()
                
                payload = {
                    "type": "TELEMETRY_TICK",
                    "timestamp": time.time(),
                    "flights": flights_pool,
                    "total_events": len(db.events),
                    "total_flags": len(db.india_flags)
                }
                await self.broadcast(payload)
            except Exception as e:
                print(f"[WS Loop Error] {e}")
                await asyncio.sleep(4)

ws_manager = ConnectionManager()

@router.websocket("/ws/live")
async def websocket_live_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send initial connection handshake
        await websocket.send_json({
            "type": "CONNECTION_ESTABLISHED",
            "message": "Connected to Bharat Sentinel Real-Time Telemetry Stream",
            "channel": "global-intel:live"
        })
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("type") == "PING":
                    await websocket.send_json({"type": "PONG", "timestamp": payload.get("timestamp")})
            except Exception:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception:
        ws_manager.disconnect(websocket)
