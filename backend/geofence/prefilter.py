import json
from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from shapely.geometry import shape, Point
    HAS_SHAPELY = True
except ImportError:
    HAS_SHAPELY = False

class GeofenceEngine:
    """
    High-performance spatial geofencing pre-filter for Bharat Sentinel.
    Determines whether flight/vessel contacts or news event locations intersect
    critical monitoring zones (India Landmass + EEZ, LAC, LoC, Arabian Sea,
    Bay of Bengal, Hormuz, Malacca, South Asia Neighborhood).
    """
    def __init__(self, geojson_path: Optional[Path] = None):
        if geojson_path is None:
            geojson_path = Path(__file__).resolve().parent / "regions.geojson"
        self.geojson_path = Path(geojson_path)
        self.zones: Dict[str, Dict[str, Any]] = {}
        self.raw_geojson: Dict[str, Any] = {}
        self.load_zones()
        self.polygons = self.zones or {
            "zone-india-eez": {}, "zone-loc": {}, "zone-lac": {},
            "zone-arabian-sea": {}, "zone-bay-of-bengal": {},
            "zone-chokepoint-malacca": {}, "zone-chokepoint-hormuz": {}, "zone-neighborhood": {}
        }

    def load_zones(self):
        if not self.geojson_path.exists():
            return
        
        try:
            with open(self.geojson_path, "r", encoding="utf-8") as f:
                self.raw_geojson = json.load(f)

            if HAS_SHAPELY:
                for feature in self.raw_geojson.get("features", []):
                    zone_id = feature.get("properties", {}).get("id")
                    geometry = feature.get("geometry")
                    if zone_id and geometry:
                        shapely_geom = shape(geometry)
                        self.zones[zone_id] = {
                            "properties": feature.get("properties", {}),
                            "geometry": shapely_geom
                        }
        except Exception:
            pass

    def get_matching_zones(self, lat: float, lon: float) -> List[str]:
        matching = []
        if HAS_SHAPELY and self.zones:
            pt = Point(lon, lat)
            for zid, zdata in self.zones.items():
                try:
                    if zdata["geometry"].contains(pt):
                        matching.append(zid)
                except Exception:
                    pass
        
        # Coordinate heuristics
        if 6.0 <= lat <= 38.0 and 65.0 <= lon <= 98.0:
            if "zone-india-eez" not in matching:
                matching.append("zone-india-eez")
        if 31.0 <= lat <= 36.0 and 73.0 <= lon <= 78.0:
            if "zone-loc" not in matching:
                matching.append("zone-loc")
        if 27.0 <= lat <= 36.0 and 77.0 <= lon <= 97.0:
            if "zone-lac" not in matching:
                matching.append("zone-lac")
        if 10.0 <= lat <= 26.0 and 55.0 <= lon <= 75.0:
            if "zone-arabian-sea" not in matching:
                matching.append("zone-arabian-sea")
        if 5.0 <= lat <= 23.0 and 80.0 <= lon <= 95.0:
            if "zone-bay-of-bengal" not in matching:
                matching.append("zone-bay-of-bengal")

        return matching

    def is_in_india_buffer(self, lat: float, lon: float) -> bool:
        return 4.0 <= lat <= 40.0 and 60.0 <= lon <= 102.0

    def is_in_ior_zones(self, lat: float, lon: float) -> bool:
        return -20.0 <= lat <= 30.0 and 40.0 <= lon <= 110.0

geofence_engine = GeofenceEngine()