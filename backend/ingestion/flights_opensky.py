import httpx
from typing import List, Dict, Any

class OpenSkyIngestion:
    """
    Ingests live ADS-B state vectors within South Asian bounding box from OpenSky Network.
    """
    def __init__(self):
        self.endpoint = "https://opensky-network.org/api/states/all"

    async def fetch_flights_in_box(self, lamin: float = 6.0, lomin: float = 68.0, lamax: float = 37.0, lomax: float = 98.0) -> List[Dict[str, Any]]:
        params = {
            "lamin": lamin,
            "lomin": lomin,
            "lamax": lamax,
            "lomax": lomax
        }
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                res = await client.get(self.endpoint, params=params)
                if res.status_code == 200:
                    data = res.json()
                    states = data.get("states", [])
                    results = []
                    for s in states[:20]:
                        results.append({
                            "icao24": s[0],
                            "callsign": s[1].strip() if s[1] else "",
                            "origin_country": s[2],
                            "lon": s[5],
                            "lat": s[6],
                            "altitude_m": s[7],
                            "velocity_kmh": round((s[9] or 0) * 3.6, 1),
                            "heading": s[10] or 0
                        })
                    return results
        except Exception as e:
            print(f"[OpenSkyIngestion] Live fetch fallback: {e}")
        return []

opensky_ingestion = OpenSkyIngestion()
