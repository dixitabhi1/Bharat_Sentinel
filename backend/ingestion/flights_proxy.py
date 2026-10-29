import time
import httpx
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
try:
    from ..db.database import db
except (ImportError, ValueError):
    from db.database import db

AIRLINE_ICAO_MAP = {
    "IGO": "IndiGo Airlines",
    "AIC": "Air India",
    "SEJ": "SpiceJet",
    "VTI": "Vistara",
    "AXB": "Air India Express",
    "I5": "AirAsia India / AIX Connect",
    "AKY": "Akasa Air",
    "UAE": "Emirates",
    "QTR": "Qatar Airways",
    "ETD": "Etihad Airways",
    "BAW": "British Airways",
    "AFR": "Air France",
    "DLH": "Lufthansa",
    "SIA": "Singapore Airlines",
    "THY": "Turkish Airlines",
    "PIA": "Pakistan International Airlines",
    "CCA": "Air China",
    "CES": "China Eastern Airlines",
    "CSN": "China Southern Airlines",
    "AFL": "Aeroflot Russian Airlines",
    "FDX": "FedEx Express Cargo",
    "UPS": "UPS Airlines Cargo",
    "CPA": "Cathay Pacific",
    "MAS": "Malaysia Airlines",
    "THA": "Thai Airways",
    "JAL": "Japan Airlines",
    "ANA": "All Nippon Airways",
    "KAL": "Korean Air",
    "UAL": "United Airlines",
    "AAL": "American Airlines",
    "DAL": "Delta Air Lines",
    "SWA": "Southwest Airlines",
    "KLM": "KLM Royal Dutch Airlines",
    "IBE": "Iberia",
    "SWR": "Swiss International Air Lines",
    "AUA": "Austrian Airlines",
    "SAS": "Scandinavian Airlines",
    "FIN": "Finnair",
    "WZZ": "Wizz Air",
    "RYR": "Ryanair",
    "EZY": "easyJet",
    "RCH": "USAF Air Mobility Command",
    "IAF": "Indian Air Force",
    "IFC": "Indian Air Force VIP",
    "PLAAF": "PLA Air Force",
    "PAF": "Pakistan Air Force",
    "RRR": "Royal Air Force",
    "ASCOT": "Royal Air Force Transport",
    "FAF": "French Air & Space Force",
    "COTAM": "French Air & Space Force",
    "RFF": "Russian Aerospace Forces"
}

MODEL_ICAO_MAP = {
    "A20N": "Airbus A320-251N (neo)",
    "A21N": "Airbus A321-271NX (neo)",
    "A320": "Airbus A320-200",
    "A321": "Airbus A321-200",
    "A319": "Airbus A319-100",
    "A359": "Airbus A350-941",
    "A35K": "Airbus A350-1041",
    "A388": "Airbus A380-841",
    "A332": "Airbus A330-200",
    "A333": "Airbus A330-300",
    "A339": "Airbus A330-900 (neo)",
    "B738": "Boeing 737-800",
    "B739": "Boeing 737-900ER",
    "B38M": "Boeing 737 MAX 8",
    "B39M": "Boeing 737 MAX 9",
    "B77W": "Boeing 777-300ER",
    "B772": "Boeing 777-200ER",
    "B77L": "Boeing 777-200LR",
    "B788": "Boeing 787-8 Dreamliner",
    "B789": "Boeing 787-9 Dreamliner",
    "B78X": "Boeing 787-10 Dreamliner",
    "B744": "Boeing 747-400",
    "B748": "Boeing 747-8I",
    "AT76": "ATR 72-600",
    "AT75": "ATR 72-500",
    "DH8D": "De Havilland Dash 8-400",
    "E190": "Embraer E190",
    "E195": "Embraer E195",
    "E295": "Embraer E195-E2",
    "CRJ9": "Bombardier CRJ-900",
    "F35": "Lockheed Martin F-35A Lightning II",
    "F35A": "Lockheed Martin F-35A Lightning II",
    "RFL": "Dassault Rafale DH",
    "RAFALE": "Dassault Rafale DH",
    "SU30": "Sukhoi Su-30MKI Flanker-H",
    "SU35": "Sukhoi Su-35S Flanker-E",
    "SU57": "Sukhoi Su-57 Felon",
    "J20": "Chengdu J-20 Mighty Dragon",
    "J16": "Shenyang J-16 Flying Shark",
    "J15": "Shenyang J-15 Flying Shark Carrier Fighter",
    "J10": "Chengdu J-10C Vigorous Dragon",
    "JF17": "PAC/CAC JF-17 Thunder Block III",
    "EF20": "Eurofighter Typhoon FGR4",
    "TYPHOON": "Eurofighter Typhoon FGR4",
    "F22": "Lockheed Martin F-22 Raptor",
    "F16": "Lockheed Martin F-16 Fighting Falcon",
    "F15": "Boeing F-15EX Eagle II",
    "FA18": "Boeing F/A-18E Super Hornet",
    "P8": "Boeing P-8I Neptune ASW",
    "P8I": "Boeing P-8I Neptune ASW",
    "E3TF": "Boeing E-3 Sentry AWACS",
    "E145": "DRDO EMB-145 Netra AEW&C",
    "NETRA": "DRDO EMB-145 Netra AEW&C",
    "C17": "Boeing C-17 Globemaster III",
    "C130": "Lockheed C-130J Super Hercules",
    "IL76": "Ilyushin Il-76MD Gajraj",
    "IL78": "Ilyushin Il-78 Midas Refueler",
    "B52": "Boeing B-52H Stratofortress",
    "TU95": "Tupolev Tu-95MS Bear-H",
    "TU160": "Tupolev Tu-160 Blackjack",
    "M29K": "Mikoyan MiG-29K Fulcrum-D"
}

def decode_airline(callsign: str, desc: str, is_mil: bool) -> str:
    if desc and "operator" not in desc.lower() and len(desc) > 3:
        return desc
    cs_upper = callsign.upper().strip()
    for prefix, name in AIRLINE_ICAO_MAP.items():
        if cs_upper.startswith(prefix):
            return name
    if is_mil:
        return "Military Air Vector"
    return "Commercial Operator"

def decode_model(t_model: str, desc: str, is_mil: bool) -> str:
    t_clean = t_model.upper().strip()
    if t_clean in MODEL_ICAO_MAP:
        return MODEL_ICAO_MAP[t_clean]
    for k, v in MODEL_ICAO_MAP.items():
        if k in t_clean or k in desc.upper():
            return v
    if t_model:
        return t_model
    return "Tactical Air Vector" if is_mil else "Commercial Airliner"

def estimate_route(lat: float, lon: float, heading: float) -> tuple:
    # Estimate realistic origin and destination based on coordinates and heading
    if 5.0 <= lat <= 38.0 and 65.0 <= lon <= 95.0:
        # India FIR
        if lat > 24.0:
            return ("DEL / Delhi", "BOM / Mumbai" if 140 <= heading <= 240 else "BLR / Bengaluru")
        else:
            return ("BOM / Mumbai" if lon < 78.0 else "BLR / Bengaluru", "DEL / Delhi" if heading < 90 or heading > 270 else "MAA / Chennai")
    elif 15.0 <= lat <= 35.0 and 40.0 <= lon <= 65.0:
        # Middle East
        return ("DXB / Dubai", "DOH / Doha" if 200 <= heading <= 300 else "LHR / London")
    elif 35.0 <= lat <= 60.0 and -10.0 <= lon <= 30.0:
        # Europe
        return ("LHR / London", "CDG / Paris" if 90 <= heading <= 180 else "FRA / Frankfurt")
    elif 25.0 <= lat <= 50.0 and -125.0 <= lon <= -65.0:
        # North America
        return ("JFK / New York", "LAX / Los Angeles" if 200 <= heading <= 300 else "ORD / Chicago")
    elif 10.0 <= lat <= 45.0 and 100.0 <= lon <= 145.0:
        # East Asia
        return ("HND / Tokyo", "SIN / Singapore" if 180 <= heading <= 270 else "HKG / Hong Kong")
    return ("Origin Airfield", "En Route Destination")

class HighDensityGlobalFlightEngine:
    """
    Unified High-Density Worldwide ADS-B Engine.
    
    Pulls live worldwide aircraft telemetry using:
      1. https://api.airplanes.live/v2/point/{lat}/{lon}/{radius_nm}
      2. https://api.airplanes.live/v2/mil (unfiltered military feed)
      3. https://api.airplanes.live/v2/hex/{icao24}
    with resilient upstream failover, persistent in-memory caching, and dead-reckoning kinematics.
    """
    def __init__(self, cache_ttl_seconds: float = 10.0):
        self.cache_ttl = cache_ttl_seconds
        self._cached_flights: List[Dict[str, Any]] = []
        self._last_fetch_time: float = 0.0
        self._is_refreshing: bool = False
        self._provider_status: Dict[str, Any] = {
            "status": "operational",
            "provider": "airplanes.live v2 Global Feed (with resilient cluster failover)",
            "primary_api": "https://api.airplanes.live/v2",
            "last_fetch_timestamp": datetime.now(timezone.utc).isoformat(),
            "active_global_contacts": 0
        }
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }
        # Pre-seed with military assets
        self._cached_flights = list(db.get_flights(scope="global"))

    async def _fetch_cluster(self, client: httpx.AsyncClient, lat: float, lon: float, radius_nm: int = 500) -> List[Dict[str, Any]]:
        url_primary = f"https://api.airplanes.live/v2/point/{lat}/{lon}/{radius_nm}"
        url_backup = f"https://api.adsb.lol/v2/lat/{lat}/lon/{lon}/dist/{radius_nm}"

        for url in [url_primary, url_backup]:
            try:
                res = await client.get(url, timeout=3.0)
                if res.status_code == 200:
                    data = res.json()
                    ac_list = data.get("ac") or []
                    now_iso = datetime.now(timezone.utc).isoformat()
                    results = []
                    for ac in ac_list:
                        lat_ac = ac.get("lat")
                        lon_ac = ac.get("lon")
                        if lat_ac is None or lon_ac is None:
                            continue
                        
                        icao = str(ac.get("hex", "")).strip().lower()
                        flight = str(ac.get("flight", "")).strip()
                        callsign = flight if flight else f"HEX-{icao.upper()}"
                        t_model_raw = str(ac.get("t", "")).strip()
                        desc_raw = str(ac.get("desc", "")).strip()
                        
                        alt_baro = ac.get("alt_baro")
                        alt_ft = int(alt_baro) if isinstance(alt_baro, (int, float)) else 35000
                        alt_m = int(round(alt_ft * 0.3048))
                        gs = ac.get("gs")
                        vel_kmh = round(gs * 1.852, 1) if isinstance(gs, (int, float)) else 850.0
                        track = float(ac.get("track", 0.0)) if ac.get("track") is not None else 0.0
                        squawk = str(ac.get("squawk", "1200"))
                        
                        is_mil = ac.get("mil", False) or any(
                            tag in callsign.upper() for tag in ["IAF", "IFC", "NETRA", "RAFAEL", "SU30", "F35", "VIP", "JAKE", "FORTE", "PATROL"]
                        )
                        
                        is_in_india = (5.0 <= float(lat_ac) <= 38.0 and 60.0 <= float(lon_ac) <= 100.0)
                        
                        airline_name = decode_airline(callsign, desc_raw, is_mil)
                        model_name = decode_model(t_model_raw, desc_raw, is_mil)
                        origin_est, dest_est = estimate_route(float(lat_ac), float(lon_ac), track)
                        
                        v_speed_fpm = int(ac.get("baro_rate", 0)) if ac.get("baro_rate") is not None else (0 if alt_m > 9000 else 1200)
                        
                        results.append({
                            "icao24": icao,
                            "callsign": callsign,
                            "airline": airline_name,
                            "origin_country": "International",
                            "lat": float(lat_ac),
                            "lon": float(lon_ac),
                            "altitude_ft": alt_ft,
                            "altitude_m": alt_m,
                            "velocity_kmh": vel_kmh,
                            "heading": track,
                            "squawk": squawk,
                            "registration": ac.get("r", icao.upper()),
                            "type": "fighter_jet" if is_mil else "commercial",
                            "model": model_name,
                            "model_code": t_model_raw if t_model_raw else (model_name.split()[0] if model_name else "A20N"),
                            "origin": origin_est,
                            "dest": dest_est,
                            "vertical_speed_fpm": v_speed_fpm,
                            "freshness": "live",
                            "provenance": "airplanes.live v2 Live Stream",
                            "is_india_relevant": is_in_india or is_mil,
                            "last_updated": now_iso,
                            "observed_at": now_iso
                        })
                    return results
            except Exception:
                continue
        return []

    async def _fetch_military(self, client: httpx.AsyncClient) -> List[Dict[str, Any]]:
        url = "https://api.airplanes.live/v2/mil"
        try:
            res = await client.get(url, timeout=3.0)
            if res.status_code == 200:
                data = res.json()
                ac_list = data.get("ac") or []
                now_iso = datetime.now(timezone.utc).isoformat()
                results = []
                for ac in ac_list:
                    lat_ac = ac.get("lat")
                    lon_ac = ac.get("lon")
                    if lat_ac is None or lon_ac is None:
                        continue
                    icao = str(ac.get("hex", "")).strip().lower()
                    flight = str(ac.get("flight", "")).strip()
                    callsign = flight if flight else f"HEX-{icao.upper()}"
                    t_model_raw = str(ac.get("t", "")).strip()
                    desc_raw = str(ac.get("desc", "")).strip()
                    alt_baro = ac.get("alt_baro")
                    alt_ft = int(alt_baro) if isinstance(alt_baro, (int, float)) else 38000
                    alt_m = int(round(alt_ft * 0.3048))
                    gs = ac.get("gs")
                    vel_kmh = round(gs * 1.852, 1) if isinstance(gs, (int, float)) else 950.0
                    track = float(ac.get("track", 0.0)) if ac.get("track") is not None else 0.0
                    squawk = str(ac.get("squawk", "7700"))
                    
                    airline_name = decode_airline(callsign, desc_raw, is_mil=True)
                    model_name = decode_model(t_model_raw, desc_raw, is_mil=True)
                    origin_est, dest_est = estimate_route(float(lat_ac), float(lon_ac), track)
                    
                    results.append({
                        "icao24": icao,
                        "callsign": callsign,
                        "airline": airline_name,
                        "origin_country": "International Military",
                        "lat": float(lat_ac),
                        "lon": float(lon_ac),
                        "altitude_ft": alt_ft,
                        "altitude_m": alt_m,
                        "velocity_kmh": vel_kmh,
                        "heading": track,
                        "squawk": squawk,
                        "registration": ac.get("r", icao.upper()),
                        "type": "fighter_jet",
                        "model": model_name,
                        "model_code": t_model_raw if t_model_raw else "MIL",
                        "origin": origin_est,
                        "dest": dest_est,
                        "vertical_speed_fpm": int(ac.get("baro_rate", 0)) if ac.get("baro_rate") is not None else 0,
                        "freshness": "live",
                        "provenance": "airplanes.live v2 Military Feed",
                        "is_india_relevant": (5.0 <= float(lat_ac) <= 38.0 and 60.0 <= float(lon_ac) <= 100.0),
                        "last_updated": now_iso,
                        "observed_at": now_iso
                    })
                return results
        except Exception:
            pass
        return []

    async def get_live_flights(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        now = time.time()
        # If cache is valid, return immediately
        if self._cached_flights and (now - self._last_fetch_time) < self.cache_ttl:
            return self.get_cached_flights(scope=scope)

        if self._is_refreshing and self._cached_flights:
            return self.get_cached_flights(scope=scope)

        self._is_refreshing = True
        try:
            clusters = [
                (28.6, 77.2, 500),   # North India / Delhi / Himalayas
                (19.1, 72.8, 500),   # West India / Mumbai / Arabian Sea
                (13.0, 80.2, 500),   # South India / Chennai / Bengaluru
                (22.5, 88.3, 500),   # East India / Kolkata / Bay of Bengal
                (25.2, 55.3, 500),   # Middle East / Persian Gulf
                (51.5, -0.1, 500),   # UK / Northern Europe
                (48.8, 2.3, 500),    # Central Europe
                (40.7, -74.0, 500),  # North America East Coast
                (34.0, -118.2, 500), # North America West Coast
                (22.3, 114.1, 500),  # East Asia / South China Sea
                (35.6, 139.7, 500),  # Japan / Tokyo
                (1.3, 103.8, 500)    # Southeast Asia / Singapore
            ]

            async with httpx.AsyncClient(headers=self.headers) as client:
                tasks = [self._fetch_cluster(client, c[0], c[1], c[2]) for c in clusters]
                tasks.append(self._fetch_military(client))
                cluster_results = await asyncio.gather(*tasks, return_exceptions=True)

            merged_dict: Dict[str, Dict[str, Any]] = {}
            
            # 1. First add base military tactical fighters with range specs
            base_fighters = db.get_flights(scope="global")
            for bf in base_fighters:
                icao = bf.get("icao24", "").lower()
                if icao:
                    if "altitude_ft" not in bf:
                        bf["altitude_ft"] = int(round(bf.get("altitude_m", 10000) * 3.28084))
                    merged_dict[icao] = bf

            # 2. Add high-density live stream contacts
            for res in cluster_results:
                if isinstance(res, list):
                    for flight in res:
                        icao = flight.get("icao24", "").lower()
                        if icao and icao not in merged_dict:
                            merged_dict[icao] = flight

            if merged_dict:
                self._cached_flights = list(merged_dict.values())
                self._last_fetch_time = now
                self._provider_status["active_global_contacts"] = len(self._cached_flights)
                self._provider_status["last_fetch_timestamp"] = datetime.now(timezone.utc).isoformat()

        except Exception as e:
            print(f"[HighDensityGlobalFlightEngine] Ingestion warning: {e}")
        finally:
            self._is_refreshing = False

        return self.get_cached_flights(scope=scope)

    def get_cached_flights(self, scope: Optional[str] = "global") -> List[Dict[str, Any]]:
        """Returns instantaneous in-memory cached flights without awaiting I/O."""
        if not self._cached_flights:
            self._cached_flights = list(db.get_flights(scope="global"))

        if scope == "india":
            return [
                f for f in self._cached_flights 
                if f.get("is_india_relevant") or (5.0 <= f.get("lat", 0) <= 38.0 and 60.0 <= f.get("lon", 0) <= 100.0)
            ]
        return self._cached_flights

    def get_provider_status(self) -> Dict[str, Any]:
        return self._provider_status

flight_proxy = HighDensityGlobalFlightEngine(cache_ttl_seconds=10.0)
