from typing import List, Dict, Any

class OSMInstallationsExtract:
    """
    Static, display-only OpenStreetMap infrastructure layer.
    Extracts public community-mapped airstrips, military airfields, naval berths,
    deep-water commercial ports, and strategic maritime chokepoints.
    
    HARD CONSTRAINT (Rule 7 / Ethics Charter):
    This layer is strictly display-only. Location data ONLY — never join this layer
    against any live flight/vessel feed for distance, range, or risk computation.
    """
    def __init__(self):
        self.disclaimer = "Community-mapped from OpenStreetMap; may be incomplete or outdated. Display-only."
        self._installations: List[Dict[str, Any]] = [
            # --- Indian Air Force Stations & Bases ---
            {
                "id": "osm-air-ambala",
                "name": "Ambala Air Force Station",
                "type": "airbase",
                "subtype": "Military Airfield",
                "country": "India",
                "lat": 30.3683,
                "lon": 76.8172,
                "elevation_m": 272,
                "tags": {"aeroway": "aerodrome", "military": "airfield", "operator": "Indian Air Force"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            },
            {
                "id": "osm-air-bhatinda",
                "name": "Bhatinda Air Force Station (Bhisi)",
                "type": "airbase",
                "subtype": "Military Airfield",
                "country": "India",
                "lat": 30.2700,
                "lon": 74.7570,
                "elevation_m": 204,
                "tags": {"aeroway": "aerodrome", "military": "airfield", "operator": "Indian Air Force"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            },
            {
                "id": "osm-air-hasimara",
                "name": "Hasimara Air Force Station",
                "type": "airbase",
                "subtype": "Military Airfield",
                "country": "India",
                "lat": 26.7022,
                "lon": 89.3697,
                "elevation_m": 104,
                "tags": {"aeroway": "aerodrome", "military": "airfield", "operator": "Indian Air Force"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            },
            {
                "id": "osm-air-tezpur",
                "name": "Tezpur Air Force Station",
                "type": "airbase",
                "subtype": "Military Airfield",
                "country": "India",
                "lat": 26.7094,
                "lon": 92.7844,
                "elevation_m": 73,
                "tags": {"aeroway": "aerodrome", "military": "airfield", "operator": "Indian Air Force"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            },
            {
                "id": "osm-air-chabua",
                "name": "Chabua Air Force Station",
                "type": "airbase",
                "subtype": "Military Airfield",
                "country": "India",
                "lat": 27.4650,
                "lon": 95.1200,
                "elevation_m": 109,
                "tags": {"aeroway": "aerodrome", "military": "airfield", "operator": "Indian Air Force"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            },
            # --- Indian Navy Bases ---
            {
                "id": "osm-navy-karwar",
                "name": "INS Kadamba (Karwar)",
                "type": "naval_base",
                "subtype": "Naval Base",
                "country": "India",
                "lat": 14.7570,
                "lon": 74.1530,
                "elevation_m": 0,
                "tags": {"military": "naval_base", "operator": "Indian Navy"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            },
            {
                "id": "osm-navy-vizag",
                "name": "Visakhapatnam Naval Dockyard",
                "type": "naval_base",
                "subtype": "Naval Base",
                "country": "India",
                "lat": 17.6970,
                "lon": 83.2840,
                "elevation_m": 0,
                "tags": {"military": "naval_base", "operator": "Indian Navy"},
                "source": "OpenStreetMap Extract",
                "freshness": "delayed",
                "provenance": "OpenStreetMap Community Contributors",
                "disclaimer": self.disclaimer
            }
        ]

    def get_installations(self) -> List[Dict[str, Any]]:
        return self._installations

osm_installations = OSMInstallationsExtract()