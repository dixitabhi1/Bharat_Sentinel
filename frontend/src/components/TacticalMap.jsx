import React, { useEffect, useRef, useState } from "react";
import * as maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { 
  Layers, 
  Plane, 
  Ship, 
  AlertOctagon, 
  Compass, 
  Maximize2, 
  Flame, 
  Activity, 
  Info,
  ShieldAlert,
  Anchor,
  X,
  ExternalLink,
  Bot,
  MapPin,
  Eye,
  Globe,
  Map as MapIcon,
  Crosshair,
  Radio,
  Clock,
  ShieldCheck,
  Building2,
  Zap,
  Target,
  CircleDot,
  RadioTower,
  Navigation,
  ArrowRight,
  FileText,
  CheckCircle2,
  Award,
  Camera,
  Shield,
  Search,
  SlidersHorizontal,
  Pause,
  Play,
  RotateCcw,
  ChevronDown,
  ChevronUp
} from "lucide-react";

// Helper to draw an SDF top-down airplane vector icon for GPU MapLibre symbol layer
function createAirplaneSDFImage() {
  const size = 64;
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext("2d");

  ctx.fillStyle = "#FFFFFF";
  ctx.beginPath();
  
  // Tactical Swept-Wing Airliner / Fighter Silhouette facing 0° (North / Top)
  ctx.moveTo(32, 4);
  ctx.bezierCurveTo(34, 8, 35, 16, 35, 22);
  ctx.lineTo(58, 34);
  ctx.lineTo(58, 38);
  ctx.lineTo(35, 34);
  ctx.lineTo(34, 48);
  ctx.lineTo(46, 56);
  ctx.lineTo(46, 59);
  ctx.lineTo(32, 57);
  ctx.lineTo(18, 59);
  ctx.lineTo(18, 56);
  ctx.lineTo(30, 48);
  ctx.lineTo(29, 34);
  ctx.lineTo(6, 38);
  ctx.lineTo(6, 34);
  ctx.bezierCurveTo(29, 16, 30, 8, 32, 4);
  
  ctx.closePath();
  ctx.fill();

  return ctx.getImageData(0, 0, size, size);
}

// Mathematical helper to generate multi-ring GeoJSON circles for combat radius and radar range
function createGeoJSONCircle(centerLat, centerLon, radiusKm, points = 72) {
  const coords = [];
  const kmPerLat = 111.32;
  const kmPerLon = 111.32 * Math.cos(centerLat * Math.PI / 180);
  for (let i = 0; i <= points; i++) {
    const angle = (i / points) * 2 * Math.PI;
    const dLat = (radiusKm * Math.cos(angle)) / kmPerLat;
    const dLon = (radiusKm * Math.sin(angle)) / kmPerLon;
    coords.push([centerLon + dLon, centerLat + dLat]);
  }
  return {
    type: "Feature",
    properties: { radius_km: radiusKm },
    geometry: {
      type: "Polygon",
      coordinates: [coords]
    }
  };
}

// Generate concentric multi-tier marked boundary rings (100%, 75%, 50%, 25%)
function createMultiRingBoundaries(centerLat, centerLon, maxRadiusKm) {
  const rings = [1.0, 0.75, 0.5, 0.25];
  const features = [];
  rings.forEach((pct) => {
    const rKm = Math.round(maxRadiusKm * pct);
    features.push(createGeoJSONCircle(centerLat, centerLon, rKm));
  });
  return {
    type: "FeatureCollection",
    features: features
  };
}

// Ultra-reliable fallback vector silhouette data URIs
const FALLBACK_AIRCRAFT_SVG = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60" fill="%2338BDF8"><path d="M50 5 L55 25 L85 35 L85 40 L55 35 L53 50 L60 55 L60 58 L50 56 L40 58 L40 55 L47 50 L45 35 L15 40 L15 35 L45 25 Z"/></svg>`;
const FALLBACK_FIGHTER_SVG = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 60" fill="%23F59E0B"><path d="M50 2 L54 18 L88 38 L88 42 L54 36 L52 52 L62 56 L62 59 L50 57 L38 59 L38 56 L48 52 L46 36 L12 42 L12 38 L46 18 Z"/></svg>`;

// Curated high-res WebP CDN photos for major airframe families
const AIRCRAFT_FAMILY_PHOTOS = {
  "A20N": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=600&q=80",
  "A320": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=600&q=80",
  "A321": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=600&q=80",
  "A350": "https://images.unsplash.com/photo-1570710891163-6d3b5c47248b?auto=format&fit=crop&w=600&q=80",
  "A380": "https://images.unsplash.com/photo-1520437358207-323b43b50729?auto=format&fit=crop&w=600&q=80",
  "B738": "https://images.unsplash.com/photo-1569154941061-e231b4725ef1?auto=format&fit=crop&w=600&q=80",
  "B777": "https://images.unsplash.com/photo-1517479149777-5f3b1511d5ad?auto=format&fit=crop&w=600&q=80",
  "B788": "https://images.unsplash.com/photo-1519074069444-1ba4fff16def?auto=format&fit=crop&w=600&q=80",
  "RAFALE": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Dassault_Rafale_C_at_Aero_India_2011.jpg/640px-Dassault_Rafale_C_at_Aero_India_2011.jpg",
  "SU30": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Su-30MKI_of_the_Indian_Air_Force_taking_off_at_Aero_India_2015.jpg/640px-Su-30MKI_of_the_Indian_Air_Force_taking_off_at_Aero_India_2015.jpg",
  "F35": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/F-35A_flight_%28cropped%29.jpg/640px-F-35A_flight_%28cropped%29.jpg",
  "J20": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Chengdu_J-20_at_Airshow_China_2018.jpg/640px-Chengdu_J-20_at_Airshow_China_2018.jpg",
  "P8": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Boeing_P-8I_Neptune_of_the_Indian_Navy.jpg/640px-Boeing_P-8I_Neptune_of_the_Indian_Navy.jpg",
  "TYPHOON": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Eurofighter_Typhoon_FGR4%2C_Royal_Air_Force_at_RIAT_2022.jpg/640px-Eurofighter_Typhoon_FGR4%2C_Royal_Air_Force_at_RIAT_2022.jpg"
};

const COUNTRIES_LIST = [
  { id: "all", label: "ALL", flag: "🌐" },
  { id: "IN", label: "IN", flag: "🇮🇳" },
  { id: "US", label: "US", flag: "🇺🇸" },
  { id: "CN", label: "CN", flag: "🇨🇳" },
  { id: "RU", label: "RU", flag: "🇷🇺" },
  { id: "PK", label: "PK", flag: "🇵🇰" },
  { id: "UK", label: "UK", flag: "🇬🇧" },
  { id: "FR", label: "FR", flag: "🇫🇷" },
  { id: "NATO", label: "NATO", flag: "🛡️" },
  { id: "JP", label: "JP", flag: "🇯🇵" },
  { id: "IR", label: "IR", flag: "🇮🇷" }
];

export default function TacticalMap({ 
  flags = [], 
  events = [],
  flights = [], 
  vessels = [], 
  fleets = [],
  leaders = [],
  disasters = [],
  installations = [],
  geofence = null, 
  selectedItem = null,
  scope = "global",
  setScope = () => {},
  onSelectItem = () => {},
  onAskChatbot = () => {}
}) {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const markersRef = useRef([]);

  // Local animated flight telemetry pool with smooth interpolation (LERP)
  const activeFlightsRef = useRef([]);
  const animFrameIdRef = useRef(null);

  // Flight Radar Drawer State (Open / Closed)
  const [isFlightDrawerOpen, setIsFlightDrawerOpen] = useState(false);
  // Flight Category Filter: 'all' | 'commercial' | 'mil'
  const [flightTypeFilter, setFlightTypeFilter] = useState("all");
  // Flight Search Filter Query
  const [flightSearchQuery, setFlightSearchQuery] = useState("");
  // Flight Motion Freeze / Pause state
  const [isMotionPaused, setIsMotionPaused] = useState(false);

  // Globe vs Flat Projection Toggle
  const [isGlobe, setIsGlobe] = useState(false);
  const [basemapStyle, setBasemapStyle] = useState("topo");
  const [showOverlaysMenu, setShowOverlaysMenu] = useState(false);
  const [mouseCoords, setMouseCoords] = useState({ lat: 20.5, lon: 78.9, zoom: 4.8 });

  // Country Strategic Base Filter
  const [selectedCountry, setSelectedCountry] = useState("all");

  // Range and Radar Ring Overlay Toggles
  const [showCombatRadius, setShowCombatRadius] = useState(true);
  const [showRadarRange, setShowRadarRange] = useState(true);

  // Live Aircraft Photo state (Planespotters.net)
  const [livePhotoUrl, setLivePhotoUrl] = useState(null);
  const [photoPhotographer, setPhotoPhotographer] = useState(null);
  const [isPhotoLoading, setIsPhotoLoading] = useState(false);

  // Layer visibility toggles
  const [layerVisibility, setLayerVisibility] = useState({
    geofence: true,
    events: true,
    flights: true,
    vessels: true,
    fleets: true,
    leaders: true,
    installations: true,
    disasters: true,
    combatRanges: true
  });

  // Active detail modal states
  const [activeModalItem, setActiveModalItem] = useState(null);
  const [hoveredItem, setHoveredItem] = useState(null);

  // Basemap tile definitions
  const basemapSources = {
    satellite: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    dark: "https://basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}@2x.png",
    topo: "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
  };

  const getFreshnessBadge = (freshness = "live", lastUpdated, provenance) => {
    return (
      <span
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: "4px",
          padding: "2px 6px",
          background: "rgba(16, 185, 129, 0.2)",
          border: "1px solid #10B981",
          borderRadius: "3px",
          color: "#34D399",
          fontSize: "0.65rem",
          fontWeight: 700,
          fontFamily: "var(--font-mono)",
          letterSpacing: "0.5px"
        }}
        title={`Provenance: ${provenance || 'Open Telemetry'} | Last Updated: ${lastUpdated || 'Recent'}`}
      >
        <span style={{ width: "5px", height: "5px", borderRadius: "50%", background: "#34D399" }} />
        STABILIZED
      </span>
    );
  };

  // Helper to build MapLibre style JSON with Rotated SDF Airplane Icons
  const getMapStyle = (bStyle) => ({
    version: 8,
    sources: {
      "base-raster": {
        type: "raster",
        tiles: [basemapSources[bStyle]],
        tileSize: 256,
        attribution: "Bharat Sentinel ADS-B Situational Awareness"
      },
      "combat-radius-source": {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      },
      "radar-range-source": {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      },
      "flights-source": {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      },
      "vessels-source": {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      },
      "events-source": {
        type: "geojson",
        data: { type: "FeatureCollection", features: [] }
      }
    },
    layers: [
      {
        id: "base-raster-layer",
        type: "raster",
        source: "base-raster",
        minzoom: 0,
        maxzoom: 20
      },
      {
        id: "combat-radius-fill",
        type: "fill",
        source: "combat-radius-source",
        paint: {
          "fill-color": "#EF4444",
          "fill-opacity": 0.12
        }
      },
      {
        id: "combat-radius-line",
        type: "line",
        source: "combat-radius-source",
        paint: {
          "line-color": "#EF4444",
          "line-width": 3.0,
          "line-dasharray": [4, 2],
          "line-opacity": 0.95
        }
      },
      {
        id: "radar-range-fill",
        type: "fill",
        source: "radar-range-source",
        paint: {
          "fill-color": "#22D3EE",
          "fill-opacity": 0.08
        }
      },
      {
        id: "radar-range-line",
        type: "line",
        source: "radar-range-source",
        paint: {
          "line-color": "#22D3EE",
          "line-width": 2.2,
          "line-dasharray": [3, 3],
          "line-opacity": 0.9
        }
      },
      // GPU-ACCELERATED ROTATED AIRPLANE SILHOUETTES WITH STANDARD ALTITUDE COLOR GRADIENT
      {
        id: "flights-symbol-layer",
        type: "symbol",
        source: "flights-source",
        layout: {
          "icon-image": "airplane-icon-sdf",
          "icon-size": [
            "interpolate", ["linear"], ["zoom"],
            2, 0.44,
            5, 0.68,
            8, 0.95,
            12, 1.3
          ],
          "icon-rotate": ["get", "heading"],
          "icon-rotation-alignment": "map",
          "icon-allow-overlap": true,
          "icon-ignore-placement": true
        },
        paint: {
          "icon-color": [
            "case",
            ["==", ["get", "is_fighter"], true], "#F59E0B",
            ["<", ["get", "altitude_ft"], 2000], "#F97316", // 0 - 2,000 ft (Orange)
            ["<", ["get", "altitude_ft"], 6000], "#EAB308", // 2,000 - 6,000 ft (Yellow)
            ["<", ["get", "altitude_ft"], 12000], "#22C55E", // 6,000 - 12,000 ft (Green)
            ["<", ["get", "altitude_ft"], 22000], "#06B6D4", // 12,000 - 22,000 ft (Teal/Cyan)
            ["<", ["get", "altitude_ft"], 32000], "#3B82F6", // 22,000 - 32,000 ft (Blue)
            "#D946EF" // 32,000 - 45,000+ ft (Magenta/Purple)
          ],
          "icon-opacity": 0.96,
          "icon-halo-color": "#030712",
          "icon-halo-width": 1.2
        }
      },
      // GPU-accelerated maritime vessels layer
      {
        id: "vessels-circle-glow",
        type: "circle",
        source: "vessels-source",
        paint: {
          "circle-radius": [
            "interpolate", ["linear"], ["zoom"],
            2, 3.0,
            6, 4.5,
            10, 7.0
          ],
          "circle-color": [
            "case",
            ["==", ["get", "anomaly"], true], "#EF4444",
            "#10B981"
          ],
          "circle-opacity": 0.9,
          "circle-stroke-width": 1.0,
          "circle-stroke-color": "#030712"
        }
      },
      // GPU-accelerated sourced intelligence events layer
      {
        id: "events-circle-glow",
        type: "circle",
        source: "events-source",
        paint: {
          "circle-radius": [
            "interpolate", ["linear"], ["zoom"],
            2, 5.0,
            6, 7.5,
            10, 11.0
          ],
          "circle-color": [
            "match", ["get", "severity"],
            4, "#EF4444",
            3, "#F97316",
            2, "#FBBF24",
            "#38BDF8"
          ],
          "circle-opacity": 0.95,
          "circle-stroke-width": 2.0,
          "circle-stroke-color": "#FFFFFF"
        }
      }
    ]
  });

  // Fetch Live Real Aircraft Photo from Planespotters.net
  const fetchLiveAircraftPhoto = async (item) => {
    if (!item) return;
    setIsPhotoLoading(true);
    setLivePhotoUrl(null);
    setPhotoPhotographer(null);

    const reg = item.registration;
    const hex = item.icao24;

    try {
      let photoData = null;
      if (reg && reg.length > 2) {
        const regRes = await fetch(`https://api.planespotters.net/pub/photos/reg/${encodeURIComponent(reg)}`);
        if (regRes.ok) {
          const json = await regRes.json();
          if (json.photos && json.photos.length > 0) {
            photoData = json.photos[0];
          }
        }
      }

      if (!photoData && hex && hex.length >= 4) {
        const hexRes = await fetch(`https://api.planespotters.net/pub/photos/hex/${encodeURIComponent(hex)}`);
        if (hexRes.ok) {
          const json = await hexRes.json();
          if (json.photos && json.photos.length > 0) {
            photoData = json.photos[0];
          }
        }
      }

      if (photoData) {
        setLivePhotoUrl(photoData.thumbnail_large?.src || photoData.thumbnail?.src);
        setPhotoPhotographer(photoData.photographer || "Planespotters.net");
      } else {
        const modelKey = (item.model_code || item.model || "").toUpperCase();
        for (const [k, url] of Object.entries(AIRCRAFT_FAMILY_PHOTOS)) {
          if (modelKey.includes(k)) {
            setLivePhotoUrl(url);
            setPhotoPhotographer("OSINT Airframe Archive");
            break;
          }
        }
      }
    } catch (e) {
      console.warn("Planespotters fetch error:", e);
    } finally {
      setIsPhotoLoading(false);
    }
  };

  const registerAirplaneIcon = (map) => {
    if (!map) return;
    try {
      if (!map.hasImage("airplane-icon-sdf")) {
        const imgData = createAirplaneSDFImage();
        map.addImage("airplane-icon-sdf", imgData, { sdf: true });
      }
    } catch (e) {}
  };

  // 1. Initialize MapLibre GL Map
  useEffect(() => {
    if (!mapContainerRef.current) return;

    const initialCenter = [78.9, 21.0];
    const initialZoom = 4.8;

    const map = new maplibregl.Map({
      container: mapContainerRef.current,
      style: getMapStyle(basemapStyle),
      center: initialCenter,
      zoom: initialZoom,
      pitch: isGlobe ? 20 : 0,
      bearing: 0,
      maxPitch: 85,
      antialias: true
    });

    map.on("load", () => {
      registerAirplaneIcon(map);
      updateGPUSources();
      renderSpecialDOMMarkers();
    });

    map.on("styledata", () => {
      registerAirplaneIcon(map);
    });

    map.on("mousemove", (e) => {
      setMouseCoords({
        lat: parseFloat(e.lngLat.lat.toFixed(4)),
        lon: parseFloat(e.lngLat.lng.toFixed(4)),
        zoom: parseFloat(map.getZoom().toFixed(1))
      });
    });

    // Airplane Symbol Layer click handlers
    map.on("click", "flights-symbol-layer", (e) => {
      if (!e.features || !e.features[0]) return;
      const feat = e.features[0];
      const target = { ...feat.properties, lat: feat.geometry.coordinates[1], lon: feat.geometry.coordinates[0] };
      setActiveModalItem(target);
      onSelectItem(target);
      updateRangeRings(target);
      fetchLiveAircraftPhoto(target);
    });

    map.on("mouseenter", "flights-symbol-layer", (e) => {
      map.getCanvas().style.cursor = "pointer";
      if (!e.features || !e.features[0]) return;
      const p = e.features[0].properties;
      const coords = e.features[0].geometry.coordinates;
      setHoveredItem({
        title: p.callsign || p.model,
        subtitle: `${p.airline || p.model} • ${p.altitude_ft ? p.altitude_ft.toLocaleString() + ' ft' : (p.altitude_m || 0) + 'm'} • ${p.velocity_kmh || 0} km/h • ${Math.round(p.heading || 0)}°`,
        freshness: p.freshness || "live",
        provenance: p.provenance || "ADS-B Real-Time Stream",
        last_updated: p.last_updated,
        lat: coords[1],
        lon: coords[0],
        type: p.is_fighter ? "TACTICAL COMBAT AIR VECTOR" : "COMMERCIAL AIRLINER"
      });
    });

    map.on("mouseleave", "flights-symbol-layer", () => {
      map.getCanvas().style.cursor = "";
      setHoveredItem(null);
    });

    map.on("click", "events-circle-glow", (e) => {
      if (!e.features || !e.features[0]) return;
      const feat = e.features[0];
      const target = { ...feat.properties, entityType: "event", lat: feat.geometry.coordinates[1], lon: feat.geometry.coordinates[0] };
      setActiveModalItem(target);
      onSelectItem(target);
    });

    map.on("click", "vessels-circle-glow", (e) => {
      if (!e.features || !e.features[0]) return;
      const feat = e.features[0];
      const target = { ...feat.properties, entityType: "vessel", lat: feat.geometry.coordinates[1], lon: feat.geometry.coordinates[0] };
      setActiveModalItem(target);
      onSelectItem(target);
    });

    mapRef.current = map;

    return () => {
      if (animFrameIdRef.current) clearTimeout(animFrameIdRef.current);
      map.remove();
      mapRef.current = null;
    };
  }, []);

  // 2. Switch Basemap Style
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    map.setStyle(getMapStyle(basemapStyle));

    setTimeout(() => {
      try {
        registerAirplaneIcon(map);
        map.setProjection({ type: isGlobe ? "globe" : "mercator" });
        updateGPUSources();
        renderSpecialDOMMarkers();
        updateRangeRings(activeModalItem);
      } catch (err) {}
    }, 120);
  }, [basemapStyle]);

  // 3. Toggle Globe / Flat Projection
  const handleToggleProjection = () => {
    const nextGlobe = !isGlobe;
    setIsGlobe(nextGlobe);
    const map = mapRef.current;
    if (!map) return;

    try {
      map.setProjection({ type: nextGlobe ? "globe" : "mercator" });
    } catch (e) {}
  };

  // 4. Update Range Rings on Map for Selected Target
  const updateRangeRings = (item) => {
    const map = mapRef.current;
    if (!map) return;

    const combatSource = map.getSource("combat-radius-source");
    const radarSource = map.getSource("radar-range-source");

    if (!combatSource || !radarSource) return;

    if (!item) {
      combatSource.setData({ type: "FeatureCollection", features: [] });
      radarSource.setData({ type: "FeatureCollection", features: [] });
      return;
    }

    const lat = item.lat || (item.location ? item.location.lat : null);
    const lon = item.lon || (item.location ? item.location.lon : null);

    if (lat === null || lon === null) return;

    let combatRadiusKm = item.combat_radius_km;
    if (!combatRadiusKm && item.air_wing_strike_radius_nm) {
      combatRadiusKm = item.air_wing_strike_radius_nm * 1.852;
    }

    let radarRangeKm = item.radar_range_km || item.radar_coverage_km;

    if (combatRadiusKm && showCombatRadius && layerVisibility.combatRanges) {
      const multiRingCollection = createMultiRingBoundaries(lat, lon, combatRadiusKm);
      combatSource.setData(multiRingCollection);
    } else {
      combatSource.setData({ type: "FeatureCollection", features: [] });
    }

    if (radarRangeKm && showRadarRange && layerVisibility.combatRanges) {
      const radarFeat = createGeoJSONCircle(lat, lon, radarRangeKm);
      radarSource.setData({ type: "FeatureCollection", features: [radarFeat] });
    } else {
      radarSource.setData({ type: "FeatureCollection", features: [] });
    }
  };

  // 5. STABILIZED TELEMETRY MERGER: Exponential Linear Smoothing (LERP) on New Arrivals
  useEffect(() => {
    if (!flights || flights.length === 0) return;
    
    const existingMap = new Map();
    activeFlightsRef.current.forEach((f) => existingMap.set(f.icao24, f));

    const updated = flights.map((f) => {
      const isFighter = f.type === "fighter_jet" || f.type === "military_patrol" || !!f.combat_radius_km;
      const altFt = f.altitude_ft || (f.altitude_m ? Math.round(f.altitude_m * 3.28084) : 35000);
      const targetLat = Number(f.lat);
      const targetLon = Number(f.lon);
      const targetHeading = Number(f.heading || 0);
      const speed = Number(f.velocity_kmh || 800);

      const existing = existingMap.get(f.icao24);
      let smoothLat = targetLat;
      let smoothLon = targetLon;
      let smoothHeading = targetHeading;

      if (existing) {
        // Compute distance delta in km
        const dLat = (targetLat - existing.lat) * 111.0;
        const dLon = (targetLon - existing.lon) * (111.0 * Math.cos((existing.lat * Math.PI) / 180));
        const distKm = Math.sqrt(dLat * dLat + dLon * dLon);

        // If distance is reasonable (< 30km), apply exponential smoothing (no teleportation jump)
        if (distKm < 30.0 && distKm > 0.001) {
          smoothLat = existing.lat + (targetLat - existing.lat) * 0.35;
          smoothLon = existing.lon + (targetLon - existing.lon) * 0.35;
        }

        // Smooth heading angular difference
        let diff = (targetHeading - existing.heading + 180) % 360 - 180;
        smoothHeading = existing.heading + diff * 0.3;
      }

      return {
        ...f,
        lat: smoothLat,
        lon: smoothLon,
        heading: smoothHeading,
        targetLat: targetLat,
        targetLon: targetLon,
        targetHeading: targetHeading,
        velocity_kmh: speed,
        altitude_ft: altFt,
        altitude_m: f.altitude_m || Math.round(altFt * 0.3048),
        is_fighter: isFighter
      };
    });

    activeFlightsRef.current = updated;
    renderFlightsOnMap();
  }, [flights, scope, layerVisibility.flights]);

  // STABLE KINEMATIC INTEGRATION LOOP: Glides smoothly at 1 second intervals without jumping
  useEffect(() => {
    let lastTime = performance.now();

    const kinematicTick = () => {
      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000.0, 1.5);
      lastTime = now;

      if (activeFlightsRef.current.length > 0 && layerVisibility.flights && !isMotionPaused) {
        activeFlightsRef.current.forEach((f) => {
          const rad = (f.heading * Math.PI) / 180;
          const speedKmh = f.velocity_kmh || 800;
          const stepKm = (speedKmh / 3600.0) * dt;
          const dLat = stepKm / 111.0;
          const dLon = stepKm / (111.0 * Math.cos((f.lat * Math.PI) / 180) || 1);
          
          f.lat += Math.cos(rad) * dLat;
          f.lon += Math.sin(rad) * dLon;

          // Gentle attraction toward latest ground truth target coords if available
          if (f.targetLat && f.targetLon) {
            f.lat += (f.targetLat - f.lat) * 0.05;
            f.lon += (f.targetLon - f.lon) * 0.05;
          }
        });

        renderFlightsOnMap();
      }

      animFrameIdRef.current = setTimeout(kinematicTick, 1000);
    };

    animFrameIdRef.current = setTimeout(kinematicTick, 1000);

    return () => {
      if (animFrameIdRef.current) clearTimeout(animFrameIdRef.current);
    };
  }, [layerVisibility.flights, isMotionPaused, flightTypeFilter]);

  // Fast GPU source updater for flights with Commercial / Mil filtering
  const renderFlightsOnMap = () => {
    const map = mapRef.current;
    if (!map) return;

    const flightsSource = map.getSource("flights-source");
    if (!flightsSource) return;

    if (!layerVisibility.flights) {
      flightsSource.setData({ type: "FeatureCollection", features: [] });
      return;
    }

    const isIndiaOnly = scope === "india";
    const feats = [];

    activeFlightsRef.current.forEach((f) => {
      if (isIndiaOnly && !f.is_india_relevant) {
        const inIndia = (5.0 <= f.lat && f.lat <= 38.0 && 60.0 <= f.lon && f.lon <= 100.0);
        if (!inIndia) return;
      }

      // Filter by Commercial vs Mil vs All
      if (flightTypeFilter === "mil" && !f.is_fighter) return;
      if (flightTypeFilter === "commercial" && f.is_fighter) return;

      feats.push({
        type: "Feature",
        properties: {
          ...f,
          is_fighter: !!f.is_fighter,
          altitude_ft: f.altitude_ft || 35000,
          heading: f.heading || 0,
          entityType: f.is_fighter ? "fighter_jet" : "flight"
        },
        geometry: {
          type: "Point",
          coordinates: [f.lon, f.lat]
        }
      });
    });

    flightsSource.setData({ type: "FeatureCollection", features: feats });
  };

  // 6. Update Other GPU GeoJSON Sources (Vessels and Events)
  const updateGPUSources = () => {
    const map = mapRef.current;
    if (!map) return;

    const isIndiaOnly = scope === "india";

    renderFlightsOnMap();

    // Vessels GPU Source
    const vesselsSource = map.getSource("vessels-source");
    if (vesselsSource) {
      if (layerVisibility.vessels) {
        const feats = [];
        vessels.forEach((v) => {
          if (isIndiaOnly && !v.is_india_relevant) return;
          feats.push({
            type: "Feature",
            properties: {
              ...v,
              anomaly: !!v.anomaly,
              entityType: "vessel"
            },
            geometry: {
              type: "Point",
              coordinates: [v.lon, v.lat]
            }
          });
        });
        vesselsSource.setData({ type: "FeatureCollection", features: feats });
      } else {
        vesselsSource.setData({ type: "FeatureCollection", features: [] });
      }
    }

    // Events GPU Source
    const eventsSource = map.getSource("events-source");
    if (eventsSource) {
      if (layerVisibility.events) {
        const feats = [];
        events.forEach((ev) => {
          if (isIndiaOnly && !ev.is_india_relevant) return;
          const loc = ev.location;
          if (!loc || loc.lat === undefined || loc.lon === undefined) return;
          feats.push({
            type: "Feature",
            properties: {
              ...ev,
              severity: ev.severity_global || ev.severity || 1,
              entityType: "event"
            },
            geometry: {
              type: "Point",
              coordinates: [loc.lon, loc.lat]
            }
          });
        });
        eventsSource.setData({ type: "FeatureCollection", features: feats });
      } else {
        eventsSource.setData({ type: "FeatureCollection", features: [] });
      }
    }
  };

  // 7. Render Special High-Value DOM Markers (Sleek Tactical Pins with ZERO Overlapping Text)
  const renderSpecialDOMMarkers = () => {
    const map = mapRef.current;
    if (!map) return;

    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    const isIndiaOnly = scope === "india";

    // Strategic Installations (Compact Military Pins)
    if (layerVisibility.installations) {
      installations.forEach((inst) => {
        if (isIndiaOnly && !inst.is_india_relevant) return;
        if (selectedCountry !== "all" && inst.country_code !== selectedCountry && inst.country !== selectedCountry) return;

        const isNaval = inst.type === "naval_base";
        const badgeColor = isNaval ? "#10B981" : "#38BDF8";
        const badgeGlow = isNaval ? "rgba(16, 185, 129, 0.7)" : "rgba(56, 189, 248, 0.7)";
        const iconSvg = isNaval 
          ? `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="5" r="3"/><line x1="12" y1="22" x2="12" y2="8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/></svg>`
          : `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>`;

        const el = document.createElement("div");
        el.className = "marker-tactical-pin";
        el.style.cursor = "pointer";
        el.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: #030712; border: 2px solid ${badgeColor}; box-shadow: 0 0 10px ${badgeGlow}; transition: transform 0.2s ease;">
            ${iconSvg}
          </div>
        `;

        el.addEventListener("click", (e) => {
          e.stopPropagation();
          const target = { ...inst, entityType: "installation" };
          setActiveModalItem(target);
          onSelectItem(target);
          updateRangeRings(null);
        });

        el.addEventListener("mouseenter", () => {
          setHoveredItem({
            title: inst.name,
            subtitle: `${inst.subtype} • ${inst.country} (${inst.country_code})`,
            freshness: inst.freshness || "live",
            provenance: inst.provenance || "Strategic Base Directory",
            last_updated: inst.last_updated,
            lat: inst.lat,
            lon: inst.lon,
            type: isNaval ? "STRATEGIC NAVAL BASE" : "STRATEGIC AIR FORCE BASE"
          });
        });

        el.addEventListener("mouseleave", () => setHoveredItem(null));

        const marker = new maplibregl.Marker({ element: el })
          .setLngLat([inst.lon, inst.lat])
          .addTo(map);
        markersRef.current.push(marker);
      });
    }

    // Naval Fleets & Carrier Strike Groups
    if (layerVisibility.fleets) {
      fleets.forEach((fl) => {
        if (isIndiaOnly && !fl.is_india_relevant) return;
        if (selectedCountry !== "all" && fl.country_code !== selectedCountry && fl.country !== selectedCountry) return;

        const el = document.createElement("div");
        el.className = "marker-fleet-cluster";
        el.style.cursor = "pointer";
        el.innerHTML = `
          <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; cursor: pointer;">
            <div style="background: rgba(251, 191, 36, 0.95); border: 2px solid #F59E0B; box-shadow: 0 0 16px rgba(251, 191, 36, 0.8); color: #030712; font-family: var(--font-display); font-weight: 900; font-size: 0.72rem; padding: 4px 10px; border-radius: 20px; white-space: nowrap; letter-spacing: 0.5px;">
              ${fl.ship_count || fl.ships?.length || 8} SHIPS
            </div>
            <div style="font-size: 0.62rem; color: #FDE047; font-family: var(--font-heading); font-weight: 700; margin-top: 2px; text-shadow: 0 2px 4px rgba(0,0,0,0.9); background: rgba(3,7,18,0.7); padding: 1px 6px; border-radius: 4px;">
              ${fl.name.split(" ")[0]} CSG
            </div>
          </div>
        `;

        el.addEventListener("click", (e) => {
          e.stopPropagation();
          const target = { ...fl, entityType: "fleet" };
          setActiveModalItem(target);
          onSelectItem(target);
          updateRangeRings(target);
        });

        el.addEventListener("mouseenter", () => {
          setHoveredItem({
            title: fl.name,
            subtitle: `${fl.ship_count || fl.ships?.length} Warships • Strike Radius: ${fl.air_wing_strike_radius_nm || 450} NM (${fl.combat_radius_km || 830} km)`,
            freshness: fl.freshness || "live",
            provenance: fl.verified_official_source || fl.source,
            last_updated: fl.last_reported,
            lat: fl.lat,
            lon: fl.lon,
            type: "VERIFIED NAVAL CARRIER STRIKE GROUP"
          });
        });

        el.addEventListener("mouseleave", () => setHoveredItem(null));

        const marker = new maplibregl.Marker({ element: el })
          .setLngLat([fl.lon, fl.lat])
          .addTo(map);
        markersRef.current.push(marker);
      });
    }

    // World Leaders & Posture Avatars
    if (layerVisibility.leaders) {
      leaders.forEach((l) => {
        if (isIndiaOnly && !l.is_india_relevant) return;
        if (selectedCountry !== "all" && l.country_code !== selectedCountry && l.country !== selectedCountry) return;

        const el = document.createElement("div");
        el.className = "marker-leader";
        el.style.cursor = "pointer";
        el.innerHTML = `
          <div style="position: relative; width: 34px; height: 34px; border-radius: 50%; border: 2px solid #F59E0B; box-shadow: 0 0 12px rgba(245, 158, 11, 0.7); overflow: hidden; background: #030712;">
            <img src="${l.avatar_url}" alt="${l.name}" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        `;

        el.addEventListener("click", (e) => {
          e.stopPropagation();
          const target = { ...l, entityType: "leader" };
          setActiveModalItem(target);
          onSelectItem(target);
          updateRangeRings(null);
        });

        el.addEventListener("mouseenter", () => {
          setHoveredItem({
            title: l.name,
            subtitle: `${l.title} • ${l.country}`,
            freshness: l.freshness,
            provenance: l.provenance,
            last_updated: l.statement_date,
            lat: l.lat,
            lon: l.lon,
            type: "STATE LEADER POSTURE PIN"
          });
        });

        el.addEventListener("mouseleave", () => setHoveredItem(null));

        const marker = new maplibregl.Marker({ element: el })
          .setLngLat([l.lon, l.lat])
          .addTo(map);
        markersRef.current.push(marker);
      });
    }
  };

  // Synchronize sources and DOM markers whenever state updates
  useEffect(() => {
    updateGPUSources();
    renderSpecialDOMMarkers();
  }, [vessels, events, leaders, installations, disasters, fleets, layerVisibility, scope, selectedCountry, flightTypeFilter]);

  // Center map on selectedItem if provided externally
  useEffect(() => {
    if (!selectedItem || !mapRef.current) return;
    const lat = selectedItem.lat || selectedItem.location?.lat;
    const lon = selectedItem.lon || selectedItem.location?.lon;
    if (lat && lon) {
      mapRef.current.flyTo({
        center: [lon, lat],
        zoom: 6.5,
        duration: 1200
      });
      setActiveModalItem(selectedItem);
      updateRangeRings(selectedItem);
      if (selectedItem.registration || selectedItem.icao24) {
        fetchLiveAircraftPhoto(selectedItem);
      }
    }
  }, [selectedItem]);

  // Compute flight statistics for the radar drawer
  const totalFlightsCount = activeFlightsRef.current.length;
  const milFlightsCount = activeFlightsRef.current.filter(f => f.is_fighter).length;
  const commFlightsCount = totalFlightsCount - milFlightsCount;

  // Filtered flights for the drawer list
  const filteredDrawerFlights = activeFlightsRef.current.filter((f) => {
    if (flightTypeFilter === "mil" && !f.is_fighter) return false;
    if (flightTypeFilter === "commercial" && f.is_fighter) return false;
    if (flightSearchQuery.trim()) {
      const q = flightSearchQuery.toLowerCase();
      const matchCallsign = (f.callsign || '').toLowerCase().includes(q);
      const matchAirline = (f.airline || '').toLowerCase().includes(q);
      const matchModel = (f.model || '').toLowerCase().includes(q);
      const matchIcao = (f.icao24 || '').toLowerCase().includes(q);
      if (!matchCallsign && !matchAirline && !matchModel && !matchIcao) return false;
    }
    return true;
  });

  return (
    <div style={{ position: "relative", width: "100%", height: "100%", background: "#030712", overflow: "hidden" }}>
      {/* Map Container */}
      <div ref={mapContainerRef} style={{ width: "100%", height: "100%" }} />

      {/* Atmospheric Scanlines Overlay */}
      <div
        className="hud-scanlines"
        style={{
          position: "absolute",
          inset: 0,
          pointerEvents: "none",
          zIndex: 10,
          background: "linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.18) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.015), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.015))",
          backgroundSize: "100% 3px, 6px 100%"
        }}
      />

      {/* =============================================================
          UNIFIED RESPONSIVE TOP HUD COMMAND DECK (ZERO OVERLAPPING)
         ============================================================= */}
      <div
        style={{
          position: "absolute",
          top: "10px",
          left: "12px",
          right: "12px",
          zIndex: 25,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "8px",
          pointerEvents: "none"
        }}
      >
        {/* Left Section: Projection, Scope & Flight Radar Drawer Opener */}
        <div style={{ pointerEvents: "auto", display: "flex", alignItems: "center", gap: "6px", flexShrink: 0 }}>
          <button
            onClick={handleToggleProjection}
            className="btn-cyber btn-cyber-primary"
            style={{
              display: "flex",
              alignItems: "center",
              gap: "5px",
              padding: "6px 10px",
              fontSize: "0.72rem",
              fontWeight: 700,
              letterSpacing: "0.5px",
              background: isGlobe ? "linear-gradient(135deg, #0284c7, #0369a1)" : "rgba(13, 24, 46, 0.85)",
              border: isGlobe ? "1px solid #38bdf8" : "1px solid var(--border-subtle)",
              boxShadow: isGlobe ? "0 0 10px rgba(56, 189, 248, 0.4)" : "none"
            }}
            title="Toggle between 3D Spherical Globe and Flat Radar Map"
          >
            {isGlobe ? <Globe size={14} color="#FFFFFF" /> : <MapIcon size={14} color="#38BDF8" />}
            <span>{isGlobe ? "3D GLOBE" : "RADAR MAP"}</span>
          </button>

          <div style={{ display: "flex", background: "rgba(6, 11, 22, 0.9)", border: "1px solid var(--border-subtle)", borderRadius: "6px", padding: "2px" }}>
            <button
              onClick={() => {
                setScope("global");
                setSelectedCountry("all");
              }}
              style={{
                padding: "5px 9px",
                fontSize: "0.7rem",
                fontFamily: "var(--font-heading)",
                fontWeight: 700,
                borderRadius: "4px",
                border: "none",
                cursor: "pointer",
                background: scope === "global" && selectedCountry === "all" ? "linear-gradient(135deg, #3b82f6, #1d4ed8)" : "transparent",
                color: scope === "global" && selectedCountry === "all" ? "#FFFFFF" : "#94A3B8",
                transition: "all 0.15s ease"
              }}
            >
              🌍 GLOBAL
            </button>
            <button
              onClick={() => {
                setScope("india");
                setSelectedCountry("IN");
              }}
              style={{
                padding: "5px 9px",
                fontSize: "0.7rem",
                fontFamily: "var(--font-heading)",
                fontWeight: 700,
                borderRadius: "4px",
                border: "none",
                cursor: "pointer",
                background: scope === "india" || selectedCountry === "IN" ? "linear-gradient(135deg, #f59e0b, #d97706)" : "transparent",
                color: scope === "india" || selectedCountry === "IN" ? "#FFFFFF" : "#94A3B8",
                transition: "all 0.15s ease"
              }}
            >
              🇮🇳 INDIA
            </button>
          </div>

          {/* OPENABLE / CLOSABLE FLIGHT RADAR MONITOR BUTTON */}
          <button
            onClick={() => setIsFlightDrawerOpen(!isFlightDrawerOpen)}
            style={{
              padding: "5px 10px",
              fontSize: "0.72rem",
              fontFamily: "var(--font-heading)",
              fontWeight: 800,
              borderRadius: "6px",
              border: isFlightDrawerOpen ? "1px solid #D946EF" : "1px solid rgba(217, 70, 239, 0.4)",
              cursor: "pointer",
              background: isFlightDrawerOpen ? "linear-gradient(135deg, #a21caf, #c026d3)" : "rgba(18, 12, 28, 0.92)",
              color: "#FFFFFF",
              display: "flex",
              alignItems: "center",
              gap: "5px",
              boxShadow: isFlightDrawerOpen ? "0 0 12px rgba(217, 70, 239, 0.5)" : "none",
              transition: "all 0.15s ease"
            }}
            title="Open or Close the Flight Monitoring Radar Deck"
          >
            <Plane size={14} color="#FDE047" />
            <span>FLIGHT RADAR</span>
            <span style={{ fontSize: "0.62rem", background: "rgba(0,0,0,0.4)", padding: "1px 5px", borderRadius: "3px" }}>
              {flightTypeFilter.toUpperCase()}
            </span>
            {isFlightDrawerOpen ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
          </button>
        </div>

        {/* Center Section: Country Base Filter Toolbar */}
        <div
          style={{
            pointerEvents: "auto",
            display: "flex",
            alignItems: "center",
            gap: "3px",
            background: "rgba(10, 16, 28, 0.94)",
            backdropFilter: "blur(16px)",
            border: "1px solid rgba(56, 189, 248, 0.3)",
            borderRadius: "8px",
            padding: "2px 6px",
            overflowX: "auto",
            scrollbarWidth: "none",
            maxWidth: "calc(100% - 460px)",
            boxShadow: "0 4px 16px rgba(0, 0, 0, 0.6)"
          }}
        >
          <span style={{ fontSize: "0.65rem", fontFamily: "var(--font-heading)", fontWeight: 800, color: "var(--accent-cyan)", padding: "0 4px", display: "flex", alignItems: "center", gap: "3px", flexShrink: 0 }}>
            <Shield size={11} />
            <span>BASES:</span>
          </span>
          {COUNTRIES_LIST.map((c) => (
            <button
              key={c.id}
              onClick={() => {
                setSelectedCountry(c.id);
                if (c.id === "IN") setScope("india");
                else setScope("global");
              }}
              style={{
                padding: "3px 6px",
                fontSize: "0.66rem",
                fontFamily: "var(--font-heading)",
                fontWeight: 700,
                borderRadius: "4px",
                border: selectedCountry === c.id ? "1px solid var(--accent-cyan)" : "1px solid transparent",
                background: selectedCountry === c.id ? "rgba(56, 189, 248, 0.25)" : "transparent",
                color: selectedCountry === c.id ? "#FFFFFF" : "#94A3B8",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: "2px",
                whiteSpace: "nowrap",
                flexShrink: 0,
                transition: "all 0.12s ease"
              }}
            >
              <span>{c.flag}</span>
              <span>{c.label}</span>
            </button>
          ))}
        </div>

        {/* Right Section: Overlays Switcher */}
        <div style={{ pointerEvents: "auto", display: "flex", alignItems: "center", gap: "6px", flexShrink: 0, position: "relative" }}>
          <button
            onClick={() => setShowOverlaysMenu(!showOverlaysMenu)}
            className="btn-cyber"
            style={{
              padding: "6px 10px",
              fontSize: "0.72rem",
              display: "flex",
              alignItems: "center",
              gap: "4px",
              background: "rgba(11, 19, 43, 0.95)",
              border: "1px solid var(--accent-cyan)",
              color: "#FFFFFF"
            }}
          >
            <Layers size={13} color="var(--accent-cyan)" />
            <span style={{ fontWeight: 700 }}>OVERLAYS ^</span>
          </button>

          {showOverlaysMenu && (
            <div
              className="hud-panel hud-corners"
              style={{
                position: "absolute",
                top: "38px",
                right: 0,
                background: "rgba(8, 14, 26, 0.98)",
                backdropFilter: "blur(16px)",
                border: "1px solid var(--border-subtle)",
                borderRadius: "8px",
                padding: "0.9rem",
                width: "250px",
                display: "flex",
                flexDirection: "column",
                gap: "0.65rem",
                boxShadow: "0 8px 32px rgba(0,0,0,0.85)",
                zIndex: 35
              }}
            >
              <div style={{ fontSize: "0.7rem", fontFamily: "var(--font-heading)", color: "var(--accent-cyan)", fontWeight: 700, borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "3px" }}>
                BASEMAP SELECTION
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "4px" }}>
                <button
                  onClick={() => setBasemapStyle("topo")}
                  style={{
                    padding: "4px",
                    fontSize: "0.65rem",
                    background: basemapStyle === "topo" ? "rgba(34, 211, 238, 0.2)" : "rgba(3, 7, 18, 0.6)",
                    border: basemapStyle === "topo" ? "1px solid var(--accent-cyan)" : "1px solid var(--border-subtle)",
                    color: "#FFFFFF",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                >
                  Radar / Topo
                </button>
                <button
                  onClick={() => setBasemapStyle("satellite")}
                  style={{
                    padding: "4px",
                    fontSize: "0.65rem",
                    background: basemapStyle === "satellite" ? "rgba(34, 211, 238, 0.2)" : "rgba(3, 7, 18, 0.6)",
                    border: basemapStyle === "satellite" ? "1px solid var(--accent-cyan)" : "1px solid var(--border-subtle)",
                    color: "#FFFFFF",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                >
                  Satellite
                </button>
                <button
                  onClick={() => setBasemapStyle("dark")}
                  style={{
                    padding: "4px",
                    fontSize: "0.65rem",
                    background: basemapStyle === "dark" ? "rgba(34, 211, 238, 0.2)" : "rgba(3, 7, 18, 0.6)",
                    border: basemapStyle === "dark" ? "1px solid var(--accent-cyan)" : "1px solid var(--border-subtle)",
                    color: "#FFFFFF",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                >
                  Dark
                </button>
              </div>

              <div style={{ fontSize: "0.7rem", fontFamily: "var(--font-heading)", color: "var(--accent-cyan)", fontWeight: 700, borderBottom: "1px solid rgba(255,255,255,0.08)", paddingBottom: "3px", marginTop: "2px" }}>
                TACTICAL LAYERS
              </div>

              <label style={{ display: "flex", alignItems: "center", gap: "7px", fontSize: "0.72rem", color: "#CBD5E1", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={layerVisibility.flights}
                  onChange={(e) => setLayerVisibility({ ...layerVisibility, flights: e.target.checked })}
                />
                <span style={{ color: "#D946EF", fontWeight: 700 }}>Live Aircraft Icons & Heading</span>
              </label>

              <label style={{ display: "flex", alignItems: "center", gap: "7px", fontSize: "0.72rem", color: "#CBD5E1", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={layerVisibility.installations}
                  onChange={(e) => setLayerVisibility({ ...layerVisibility, installations: e.target.checked })}
                />
                <span style={{ color: "#38BDF8", fontWeight: 700 }}>Air & Naval Bases ({selectedCountry.toUpperCase()})</span>
              </label>

              <label style={{ display: "flex", alignItems: "center", gap: "7px", fontSize: "0.72rem", color: "#CBD5E1", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={layerVisibility.combatRanges}
                  onChange={(e) => setLayerVisibility({ ...layerVisibility, combatRanges: e.target.checked })}
                />
                <span style={{ color: "#EF4444", fontWeight: 700 }}>Visible Combat Range Rings</span>
              </label>

              <label style={{ display: "flex", alignItems: "center", gap: "7px", fontSize: "0.72rem", color: "#CBD5E1", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={layerVisibility.fleets}
                  onChange={(e) => setLayerVisibility({ ...layerVisibility, fleets: e.target.checked })}
                />
                <span style={{ color: "#F59E0B" }}>Global Naval Fleets ({fleets.length})</span>
              </label>

              <label style={{ display: "flex", alignItems: "center", gap: "7px", fontSize: "0.72rem", color: "#CBD5E1", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={layerVisibility.vessels}
                  onChange={(e) => setLayerVisibility({ ...layerVisibility, vessels: e.target.checked })}
                />
                <span>Maritime Vessels (AIS)</span>
              </label>

              <label style={{ display: "flex", alignItems: "center", gap: "7px", fontSize: "0.72rem", color: "#CBD5E1", cursor: "pointer" }}>
                <input
                  type="checkbox"
                  checked={layerVisibility.events}
                  onChange={(e) => setLayerVisibility({ ...layerVisibility, events: e.target.checked })}
                />
                <span>Sourced Intelligence Events</span>
              </label>
            </div>
          )}
        </div>
      </div>

      {/* =============================================================
          OPENABLE / CLOSABLE FLIGHT RADAR MONITORING PANEL
         ============================================================= */}
      {isFlightDrawerOpen && (
        <div
          style={{
            position: "absolute",
            top: "52px",
            left: "12px",
            width: "360px",
            maxHeight: "calc(100% - 90px)",
            background: "rgba(10, 16, 28, 0.97)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(217, 70, 239, 0.4)",
            borderRadius: "10px",
            zIndex: 35,
            display: "flex",
            flexDirection: "column",
            boxShadow: "0 12px 40px rgba(0, 0, 0, 0.85)",
            overflow: "hidden"
          }}
        >
          {/* Drawer Header */}
          <div
            style={{
              padding: "8px 12px",
              background: "linear-gradient(135deg, rgba(217, 70, 239, 0.15), rgba(59, 130, 246, 0.1))",
              borderBottom: "1px solid rgba(255, 255, 255, 0.08)",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between"
            }}
          >
            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <Plane size={16} color="#D946EF" />
              <span style={{ fontFamily: "var(--font-heading)", fontWeight: 800, fontSize: "0.85rem", color: "#FFFFFF", letterSpacing: "0.5px" }}>
                FLIGHT MONITORING RADAR
              </span>
            </div>
            
            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              {/* Kinematic Motion Pause / Play Toggle */}
              <button
                onClick={() => setIsMotionPaused(!isMotionPaused)}
                style={{
                  background: isMotionPaused ? "#EF4444" : "rgba(255,255,255,0.08)",
                  border: isMotionPaused ? "1px solid #EF4444" : "1px solid rgba(255,255,255,0.15)",
                  borderRadius: "4px",
                  color: "#FFFFFF",
                  padding: "3px 6px",
                  fontSize: "0.65rem",
                  fontFamily: "var(--font-mono)",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  gap: "4px"
                }}
                title={isMotionPaused ? "Resume Live Motion Glide" : "Pause / Freeze Position for Precise Inspection"}
              >
                {isMotionPaused ? <Play size={11} /> : <Pause size={11} />}
                <span>{isMotionPaused ? "PAUSED" : "LIVE 60FPS"}</span>
              </button>

              <button
                onClick={() => setIsFlightDrawerOpen(false)}
                style={{ background: "transparent", border: "none", color: "#94A3B8", cursor: "pointer", padding: "2px" }}
              >
                <X size={16} />
              </button>
            </div>
          </div>

          {/* Filter Bar: [ALL] [COMMERCIAL] [MILITARY] */}
          <div style={{ padding: "8px 10px", background: "#0D1322", borderBottom: "1px solid rgba(255,255,255,0.06)", display: "flex", flexDirection: "column", gap: "8px" }}>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "4px" }}>
              <button
                onClick={() => setFlightTypeFilter("all")}
                style={{
                  padding: "5px 4px",
                  fontSize: "0.68rem",
                  fontFamily: "var(--font-heading)",
                  fontWeight: 700,
                  borderRadius: "4px",
                  border: flightTypeFilter === "all" ? "1px solid #D946EF" : "1px solid rgba(255,255,255,0.08)",
                  background: flightTypeFilter === "all" ? "rgba(217, 70, 239, 0.25)" : "rgba(3, 7, 18, 0.6)",
                  color: flightTypeFilter === "all" ? "#FFFFFF" : "#94A3B8",
                  cursor: "pointer",
                  textAlign: "center"
                }}
              >
                ALL ({totalFlightsCount})
              </button>

              <button
                onClick={() => setFlightTypeFilter("commercial")}
                style={{
                  padding: "5px 4px",
                  fontSize: "0.68rem",
                  fontFamily: "var(--font-heading)",
                  fontWeight: 700,
                  borderRadius: "4px",
                  border: flightTypeFilter === "commercial" ? "1px solid #38BDF8" : "1px solid rgba(255,255,255,0.08)",
                  background: flightTypeFilter === "commercial" ? "rgba(56, 189, 248, 0.25)" : "rgba(3, 7, 18, 0.6)",
                  color: flightTypeFilter === "commercial" ? "#FFFFFF" : "#94A3B8",
                  cursor: "pointer",
                  textAlign: "center"
                }}
              >
                COMM ({commFlightsCount})
              </button>

              <button
                onClick={() => setFlightTypeFilter("mil")}
                style={{
                  padding: "5px 4px",
                  fontSize: "0.68rem",
                  fontFamily: "var(--font-heading)",
                  fontWeight: 700,
                  borderRadius: "4px",
                  border: flightTypeFilter === "mil" ? "1px solid #F59E0B" : "1px solid rgba(255,255,255,0.08)",
                  background: flightTypeFilter === "mil" ? "rgba(245, 158, 11, 0.25)" : "rgba(3, 7, 18, 0.6)",
                  color: flightTypeFilter === "mil" ? "#FFFFFF" : "#94A3B8",
                  cursor: "pointer",
                  textAlign: "center"
                }}
              >
                ⚔️ MIL ({milFlightsCount})
              </button>
            </div>

            {/* Quick Search */}
            <div style={{ position: "relative", width: "100%" }}>
              <Search size={13} color="#94A3B8" style={{ position: "absolute", left: "8px", top: "50%", transform: "translateY(-50%)" }} />
              <input
                type="text"
                placeholder="Search callsign, airline, model (e.g. IAF, IGO, A20N, F35)..."
                value={flightSearchQuery}
                onChange={(e) => setFlightSearchQuery(e.target.value)}
                style={{
                  width: "100%",
                  padding: "5px 8px 5px 26px",
                  fontSize: "0.72rem",
                  fontFamily: "var(--font-body)",
                  background: "rgba(3, 7, 18, 0.8)",
                  border: "1px solid rgba(255, 255, 255, 0.1)",
                  borderRadius: "4px",
                  color: "#FFFFFF",
                  outline: "none"
                }}
              />
            </div>
          </div>

          {/* Active Flights List */}
          <div style={{ flex: 1, overflowY: "auto", padding: "6px", display: "flex", flexDirection: "column", gap: "4px", maxHeight: "380px" }}>
            {filteredDrawerFlights.slice(0, 50).map((f, idx) => {
              const altFt = f.altitude_ft || Math.round((f.altitude_m || 10000) * 3.28);
              let altBadgeColor = "#D946EF";
              if (f.is_fighter) altBadgeColor = "#F59E0B";
              else if (altFt < 2000) altBadgeColor = "#F97316";
              else if (altFt < 6000) altBadgeColor = "#EAB308";
              else if (altFt < 12000) altBadgeColor = "#22C55E";
              else if (altFt < 22000) altBadgeColor = "#06B6D4";
              else if (altFt < 32000) altBadgeColor = "#3B82F6";

              return (
                <div
                  key={idx}
                  onClick={() => {
                    if (mapRef.current) {
                      mapRef.current.flyTo({ center: [f.lon, f.lat], zoom: 7.5, duration: 1000 });
                    }
                    setActiveModalItem(f);
                    onSelectItem(f);
                    updateRangeRings(f);
                    fetchLiveAircraftPhoto(f);
                  }}
                  style={{
                    background: "rgba(17, 24, 39, 0.85)",
                    border: "1px solid rgba(255, 255, 255, 0.06)",
                    borderRadius: "5px",
                    padding: "6px 8px",
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    transition: "all 0.12s ease"
                  }}
                >
                  <div style={{ display: "flex", flexDirection: "column" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                      <span style={{ fontFamily: "var(--font-mono)", fontWeight: 800, fontSize: "0.78rem", color: "#FFFFFF" }}>
                        {f.callsign || f.icao24?.toUpperCase()}
                      </span>
                      {f.is_fighter && (
                        <span style={{ background: "#F59E0B", color: "#030712", fontSize: "0.58rem", fontWeight: 900, padding: "1px 4px", borderRadius: "2px" }}>
                          MIL
                        </span>
                      )}
                    </div>
                    <div style={{ fontSize: "0.66rem", color: "#94A3B8", marginTop: "1px" }}>
                      {f.airline || f.model}
                    </div>
                  </div>

                  <div style={{ textAlign: "right", fontFamily: "var(--font-mono)" }}>
                    <div style={{ color: altBadgeColor, fontWeight: 700, fontSize: "0.72rem" }}>
                      {altFt.toLocaleString()} ft
                    </div>
                    <div style={{ color: "#94A3B8", fontSize: "0.62rem" }}>
                      {Math.round(f.velocity_kmh || 800)} km/h • {Math.round(f.heading || 0)}°
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* =============================================================
          STANDARD AVIATION ALTITUDE GRADIENT LEGEND (AS IN AIRPLANES.LIVE)
         ============================================================= */}
      <div
        style={{
          position: "absolute",
          bottom: "32px",
          left: "14px",
          zIndex: 20,
          background: "rgba(10, 16, 28, 0.92)",
          backdropFilter: "blur(12px)",
          border: "1px solid rgba(255, 255, 255, 0.12)",
          borderRadius: "6px",
          padding: "5px 10px",
          display: "flex",
          flexDirection: "column",
          gap: "3px",
          boxShadow: "0 4px 16px rgba(0, 0, 0, 0.6)"
        }}
      >
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: "0.6rem", fontFamily: "var(--font-mono)", color: "#CBD5E1", letterSpacing: "0.5px" }}>
          <span>ALTITUDE (ft)</span>
          <span style={{ color: "#94A3B8" }}>0 → 40,000+</span>
        </div>
        
        {/* Continuous Gradient Bar */}
        <div
          style={{
            width: "280px",
            height: "9px",
            borderRadius: "3px",
            background: "linear-gradient(90deg, #F97316 0%, #EAB308 15%, #22C55E 30%, #06B6D4 55%, #3B82F6 75%, #D946EF 100%)",
            border: "1px solid rgba(0,0,0,0.5)"
          }}
        />

        {/* Legend Step Ticks */}
        <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.55rem", fontFamily: "var(--font-mono)", color: "#94A3B8" }}>
          <span>0</span>
          <span>2k</span>
          <span>6k</span>
          <span>12k</span>
          <span>22k</span>
          <span>32k</span>
          <span>40k+</span>
        </div>
      </div>

      {/* Floating Hover Tooltip */}
      {hoveredItem && (
        <div
          style={{
            position: "absolute",
            bottom: "38px",
            left: "50%",
            transform: "translateX(-50%)",
            background: "rgba(6, 11, 22, 0.95)",
            backdropFilter: "blur(12px)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "6px",
            padding: "6px 14px",
            zIndex: 30,
            pointerEvents: "none",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            boxShadow: "0 6px 20px rgba(0,0,0,0.6)"
          }}
        >
          <div style={{ display: "flex", flexDirection: "column" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
              <span style={{ fontFamily: "var(--font-heading)", fontWeight: 700, fontSize: "0.82rem", color: "#FFFFFF" }}>
                {hoveredItem.title}
              </span>
              {getFreshnessBadge(hoveredItem.freshness, hoveredItem.last_updated, hoveredItem.provenance)}
            </div>
            <div style={{ fontSize: "0.7rem", color: "#94A3B8", marginTop: "1px" }}>
              {hoveredItem.subtitle}
            </div>
          </div>

          <div style={{ borderLeft: "1px solid rgba(255,255,255,0.1)", paddingLeft: "8px", fontSize: "0.66rem", fontFamily: "var(--font-mono)", color: "var(--accent-cyan)" }}>
            <div>{hoveredItem.lat?.toFixed ? hoveredItem.lat.toFixed(2) : hoveredItem.lat}°N, {hoveredItem.lon?.toFixed ? hoveredItem.lon.toFixed(2) : hoveredItem.lon}°E</div>
            <div style={{ color: "var(--text-muted)" }}>{hoveredItem.type}</div>
          </div>
        </div>
      )}

      {/* Bottom Telemetry HUD Bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: "26px",
          background: "rgba(6, 11, 22, 0.95)",
          borderTop: "1px solid var(--border-subtle)",
          zIndex: 20,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "0 1rem",
          fontSize: "0.66rem",
          fontFamily: "var(--font-mono)",
          color: "var(--text-muted)"
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span>PROJECTION: <strong style={{ color: "var(--accent-cyan)" }}>{isGlobe ? "3D GLOBE" : "RADAR MAP"}</strong></span>
          <span>NATION: <strong style={{ color: "#F59E0B" }}>{selectedCountry.toUpperCase()}</strong></span>
          <span>FILTER: <strong style={{ color: "#D946EF" }}>{flightTypeFilter.toUpperCase()} FLIGHTS</strong></span>
          <span>COORDS: <strong style={{ color: "#E2E8F0" }}>{mouseCoords.lat}°N, {mouseCoords.lon}°E</strong></span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <span>TRACKED AIRCRAFT: <strong style={{ color: "#D946EF" }}>{filteredDrawerFlights.length} Active</strong></span>
          <span>STRATEGIC BASES: <strong style={{ color: "#38BDF8" }}>{installations.length} Active</strong></span>
          <span>CARRIER STRIKE GROUPS: <strong style={{ color: "#F59E0B" }}>{fleets.length} Verified</strong></span>
        </div>
      </div>

      {/* -------------------------------------------------------------
          DETAILED FLIGHT & FIGHTER JET TRACKING DOSSIER CARD
         ------------------------------------------------------------- */}
      {activeModalItem && (activeModalItem.entityType === "fighter_jet" || activeModalItem.entityType === "flight" || activeModalItem.icao24) && (
        <div
          style={{
            position: "absolute",
            top: "52px",
            right: "12px",
            width: "420px",
            maxHeight: "calc(100% - 90px)",
            background: "rgba(10, 16, 28, 0.98)",
            backdropFilter: "blur(20px)",
            border: "1px solid rgba(56, 189, 248, 0.3)",
            borderRadius: "10px",
            zIndex: 40,
            overflowY: "auto",
            boxShadow: "0 12px 40px rgba(0, 0, 0, 0.85)",
            fontFamily: "var(--font-body)",
            color: "#FFFFFF"
          }}
        >
          {/* Top Header Bar with Resilient Photo Engine */}
          <div
            style={{
              padding: "0.75rem 0.9rem",
              background: "#1E222B",
              borderBottom: "1px solid rgba(255, 255, 255, 0.1)",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "8px"
            }}
          >
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "6px", flexWrap: "wrap" }}>
                <span style={{ fontSize: "1.15rem", fontFamily: "var(--font-display)", fontWeight: 900, color: "#FDE047", letterSpacing: "0.8px" }}>
                  {activeModalItem.callsign || `HEX-${(activeModalItem.icao24 || '').toUpperCase()}`}
                </span>
                <span style={{ background: "#2563EB", color: "#FFFFFF", fontSize: "0.68rem", fontWeight: 700, padding: "2px 5px", borderRadius: "3px", fontFamily: "var(--font-mono)" }}>
                  {activeModalItem.model_code || (activeModalItem.model ? activeModalItem.model.split(" ")[0] : "AC")}
                </span>
                <span style={{ background: "#DC2626", color: "#FFFFFF", fontSize: "0.68rem", fontWeight: 700, padding: "2px 5px", borderRadius: "3px", fontFamily: "var(--font-mono)" }}>
                  {activeModalItem.squawk || (activeModalItem.type === "fighter_jet" ? "7700" : "1200")}
                </span>
              </div>
              <div style={{ fontSize: "0.78rem", color: "#E2E8F0", marginTop: "2px", fontWeight: 600 }}>
                {activeModalItem.airline || "Commercial Operator"}
              </div>
            </div>

            {/* Aircraft Live Photo from Planespotters.net */}
            <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end" }}>
              <div style={{ width: "95px", height: "54px", borderRadius: "4px", overflow: "hidden", border: "1px solid rgba(255,255,255,0.2)", background: "#0B132B", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <img
                  src={livePhotoUrl || (activeModalItem.type === "fighter_jet" ? FALLBACK_FIGHTER_SVG : FALLBACK_AIRCRAFT_SVG)}
                  alt={activeModalItem.model || "Aircraft Silhouette"}
                  onError={(e) => {
                    e.target.onerror = null;
                    e.target.src = activeModalItem.type === "fighter_jet" ? FALLBACK_FIGHTER_SVG : FALLBACK_AIRCRAFT_SVG;
                  }}
                  style={{ width: "100%", height: "100%", objectFit: "cover" }}
                />
              </div>
              <div style={{ fontSize: "0.55rem", color: "#94A3B8", fontFamily: "var(--font-mono)", marginTop: "2px", display: "flex", alignItems: "center", gap: "2px" }}>
                <Camera size={9} />
                <span>{photoPhotographer || "Planespotters.net"}</span>
              </div>
            </div>
          </div>

          <div style={{ padding: "0.9rem", display: "flex", flexDirection: "column", gap: "8px" }}>
            {/* Real Route Box */}
            <div style={{ background: "#111827", borderRadius: "6px", padding: "0.65rem", border: "1px solid rgba(255,255,255,0.06)" }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", textAlign: "center" }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: "0.95rem", fontWeight: 800, color: "#FFFFFF", fontFamily: "var(--font-display)" }}>
                    {activeModalItem.origin || "Origin Airfield"}
                  </div>
                  <div style={{ fontSize: "0.62rem", color: "#94A3B8" }}>
                    DEPARTURE SECTOR
                  </div>
                </div>

                <div style={{ display: "flex", alignItems: "center", justifyContent: "center", padding: "0 8px" }}>
                  <div style={{ width: "26px", height: "26px", borderRadius: "50%", background: "rgba(251, 191, 36, 0.15)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                    <Plane size={14} color="#FBBF24" />
                  </div>
                </div>

                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: "0.95rem", fontWeight: 800, color: "#FFFFFF", fontFamily: "var(--font-display)" }}>
                    {activeModalItem.dest || "En Route"}
                  </div>
                  <div style={{ fontSize: "0.62rem", color: "#94A3B8" }}>
                    ARRIVAL SECTOR
                  </div>
                </div>
              </div>

              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", borderTop: "1px solid rgba(255,255,255,0.08)", marginTop: "6px", paddingTop: "5px", fontSize: "0.68rem", color: "#CBD5E1", fontFamily: "var(--font-mono)" }}>
                <span>Flight Time: Active Track</span>
                <span>Heading: {Math.round(activeModalItem.heading || 0)}°</span>
              </div>
            </div>

            {/* Aircraft Decoded Model & Registration */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "#111827", padding: "7px 10px", borderRadius: "6px", border: "1px solid rgba(255,255,255,0.06)" }}>
              <div style={{ fontSize: "0.82rem", fontWeight: 700, color: "#F3F4F6" }}>
                {activeModalItem.model || "Airbus A320neo"}
              </div>
              <div style={{ fontSize: "0.72rem", fontFamily: "var(--font-mono)", color: "#38BDF8" }}>
                REG. {activeModalItem.registration || activeModalItem.icao24?.toUpperCase()}
              </div>
            </div>

            {/* Telemetry Stats Grid */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px" }}>
              <div style={{ background: "#111827", padding: "7px 10px", borderRadius: "6px", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: "0.62rem", color: "#94A3B8", fontFamily: "var(--font-mono)" }}>BAROMETRIC ALT.</div>
                <div style={{ fontSize: "1rem", fontWeight: 800, color: "#FFFFFF", fontFamily: "var(--font-display)" }}>
                  {activeModalItem.altitude_ft ? `${activeModalItem.altitude_ft.toLocaleString()} ft` : (activeModalItem.altitude_m ? `${Math.round(activeModalItem.altitude_m * 3.28).toLocaleString()} ft` : "35,000 ft")}
                </div>
                <div style={{ fontSize: "0.65rem", color: "var(--accent-cyan)", fontFamily: "var(--font-mono)" }}>
                  {activeModalItem.altitude_m || 10668} m
                </div>
              </div>

              <div style={{ background: "#111827", padding: "7px 10px", borderRadius: "6px", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: "0.62rem", color: "#94A3B8", fontFamily: "var(--font-mono)" }}>GROUND SPEED</div>
                <div style={{ fontSize: "1rem", fontWeight: 800, color: "#FFFFFF", fontFamily: "var(--font-display)" }}>
                  {activeModalItem.velocity_kmh ? `${Math.round(activeModalItem.velocity_kmh * 0.539957)} kts` : "450 kts"}
                </div>
                <div style={{ fontSize: "0.65rem", color: "#34D399", fontFamily: "var(--font-mono)" }}>
                  {activeModalItem.velocity_kmh || 835} km/h
                </div>
              </div>

              <div style={{ background: "#111827", padding: "7px 10px", borderRadius: "6px", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: "0.62rem", color: "#94A3B8", fontFamily: "var(--font-mono)" }}>TRACK / HEADING</div>
                <div style={{ fontSize: "0.92rem", fontWeight: 700, color: "#FFFFFF", fontFamily: "var(--font-mono)" }}>
                  {activeModalItem.heading ? `${activeModalItem.heading.toFixed(1)}°` : "160.0°"}
                </div>
                <div style={{ fontSize: "0.62rem", color: "#94A3B8" }}>Compass Vector</div>
              </div>

              <div style={{ background: "#111827", padding: "7px 10px", borderRadius: "6px", border: "1px solid rgba(255,255,255,0.06)" }}>
                <div style={{ fontSize: "0.62rem", color: "#94A3B8", fontFamily: "var(--font-mono)" }}>VERTICAL SPEED</div>
                <div style={{ fontSize: "0.92rem", fontWeight: 700, color: activeModalItem.vertical_speed_fpm >= 0 ? "#34D399" : "#F87171", fontFamily: "var(--font-mono)" }}>
                  {activeModalItem.vertical_speed_fpm ? `${activeModalItem.vertical_speed_fpm > 0 ? '+' : ''}${activeModalItem.vertical_speed_fpm} fpm` : "0 fpm (Cruise Level)"}
                </div>
                <div style={{ fontSize: "0.62rem", color: "#94A3B8" }}>
                  {activeModalItem.vertical_speed_fpm > 300 ? "Climbing" : (activeModalItem.vertical_speed_fpm < -300 ? "Descending" : "Level Flight")}
                </div>
              </div>
            </div>

            {/* Fighter Jet Combat Radius & Sensor Range Specifications */}
            {activeModalItem.combat_radius_km && (
              <div style={{ background: "rgba(239, 68, 68, 0.12)", border: "1.5px solid #EF4444", borderRadius: "6px", padding: "8px" }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "4px" }}>
                  <div style={{ display: "flex", alignItems: "center", gap: "5px", color: "#F87171", fontSize: "0.72rem", fontWeight: 800, fontFamily: "var(--font-heading)" }}>
                    <Target size={14} />
                    <span>VISIBLE RANGE ESTIMATION & ENVELOPE</span>
                  </div>
                  <span style={{ fontSize: "0.62rem", background: "#EF4444", color: "#FFFFFF", padding: "2px 5px", borderRadius: "3px", fontFamily: "var(--font-mono)", fontWeight: 700 }}>
                    MARKED BOUNDARY
                  </span>
                </div>

                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "6px", fontSize: "0.72rem", fontFamily: "var(--font-mono)" }}>
                  <div>
                    <span style={{ color: "#94A3B8" }}>Combat Radius: </span>
                    <strong style={{ color: "#FDE047" }}>{activeModalItem.combat_radius_km} km ({Math.round(activeModalItem.combat_radius_km * 0.539957)} NM)</strong>
                  </div>
                  <div>
                    <span style={{ color: "#94A3B8" }}>Radar Range: </span>
                    <strong style={{ color: "#22D3EE" }}>{activeModalItem.radar_range_km || 160} km</strong>
                  </div>
                </div>

                {/* Range Toggle Buttons */}
                <div style={{ display: "flex", gap: "5px", marginTop: "6px" }}>
                  <button
                    onClick={() => {
                      const next = !showCombatRadius;
                      setShowCombatRadius(next);
                      updateRangeRings({ ...activeModalItem });
                    }}
                    style={{
                      flex: 1,
                      padding: "5px 6px",
                      fontSize: "0.66rem",
                      fontFamily: "var(--font-heading)",
                      fontWeight: 700,
                      background: showCombatRadius ? "#EF4444" : "rgba(17, 24, 39, 0.8)",
                      border: "1px solid #EF4444",
                      color: "#FFFFFF",
                      borderRadius: "4px",
                      cursor: "pointer"
                    }}
                  >
                    {showCombatRadius ? "● Visible Combat Radius (ON)" : "○ Show Combat Boundary"}
                  </button>

                  <button
                    onClick={() => {
                      const next = !showRadarRange;
                      setShowRadarRange(next);
                      updateRangeRings({ ...activeModalItem });
                    }}
                    style={{
                      flex: 1,
                      padding: "5px 6px",
                      fontSize: "0.66rem",
                      fontFamily: "var(--font-heading)",
                      fontWeight: 700,
                      background: showRadarRange ? "#0284c7" : "rgba(17, 24, 39, 0.8)",
                      border: "1px solid #22D3EE",
                      color: "#FFFFFF",
                      borderRadius: "4px",
                      cursor: "pointer"
                    }}
                  >
                    {showRadarRange ? "● Radar Dome (ON)" : "○ Show Radar Dome"}
                  </button>
                </div>
              </div>
            )}

            {/* Freshness & Provenance Labeling */}
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "#111827", padding: "5px 8px", borderRadius: "4px", fontSize: "0.68rem", fontFamily: "var(--font-mono)" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
                <span style={{ color: "#94A3B8" }}>FEED:</span>
                {getFreshnessBadge(activeModalItem.freshness, activeModalItem.last_updated, activeModalItem.provenance)}
              </div>
              <div style={{ color: "#94A3B8" }}>
                {activeModalItem.provenance || "airplanes.live v2 Stream"}
              </div>
            </div>

            {/* AI Strategic Intelligence Deep Dive */}
            <div style={{ display: "flex", gap: "6px", marginTop: "2px" }}>
              <button
                onClick={() => onAskChatbot(activeModalItem)}
                className="btn-cyber btn-cyber-primary"
                style={{ flex: 1, padding: "7px", fontSize: "0.75rem", display: "flex", alignItems: "center", justifyContent: "center", gap: "5px" }}
              >
                <Bot size={14} />
                <span>Analyze with Sentinel AI</span>
              </button>

              <button
                onClick={() => {
                  setActiveModalItem(null);
                  updateRangeRings(null);
                }}
                className="btn-cyber"
                style={{ padding: "7px 10px", fontSize: "0.75rem" }}
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* -------------------------------------------------------------
          STRATEGIC BASE DOSSIER MODAL (AIRBASE & NAVAL BASE)
         ------------------------------------------------------------- */}
      {activeModalItem && activeModalItem.entityType === "installation" && (
        <div
          style={{
            position: "absolute",
            top: "52px",
            right: "12px",
            width: "400px",
            maxHeight: "calc(100% - 90px)",
            background: "rgba(10, 16, 28, 0.98)",
            backdropFilter: "blur(20px)",
            border: activeModalItem.type === "naval_base" ? "1.5px solid #10B981" : "1.5px solid #38BDF8",
            borderRadius: "10px",
            zIndex: 40,
            overflowY: "auto",
            boxShadow: "0 12px 40px rgba(0, 0, 0, 0.85)",
            padding: "1.1rem",
            color: "#FFFFFF"
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "6px" }}>
            <div>
              <div style={{ fontSize: "0.68rem", fontFamily: "var(--font-mono)", color: activeModalItem.type === "naval_base" ? "#34D399" : "#38BDF8", textTransform: "uppercase", display: "flex", alignItems: "center", gap: "5px" }}>
                {activeModalItem.type === "naval_base" ? <Anchor size={12} /> : <Plane size={12} />}
                <span>{activeModalItem.type === "naval_base" ? "STRATEGIC NAVAL BASE" : "STRATEGIC AIR FORCE BASE"} • {activeModalItem.country_code}</span>
              </div>
              <div style={{ fontFamily: "var(--font-heading)", fontWeight: 800, fontSize: "1.05rem", color: "#FFFFFF", marginTop: "2px" }}>
                {activeModalItem.name}
              </div>
            </div>
            <button
              onClick={() => setActiveModalItem(null)}
              style={{ background: "transparent", border: "none", color: "#94A3B8", cursor: "pointer" }}
            >
              <X size={16} />
            </button>
          </div>

          <div style={{ background: "rgba(17, 24, 39, 0.8)", border: "1px solid rgba(255,255,255,0.08)", borderRadius: "6px", padding: "8px", marginBottom: "10px", display: "flex", flexDirection: "column", gap: "6px" }}>
            <div style={{ fontSize: "0.72rem", color: "#E2E8F0" }}>
              <span style={{ color: "#94A3B8" }}>Classification: </span>
              <strong>{activeModalItem.subtype}</strong>
            </div>

            {activeModalItem.active_squadrons && (
              <div style={{ fontSize: "0.72rem", color: "#E2E8F0" }}>
                <span style={{ color: "#94A3B8" }}>Stationed Squadrons: </span>
                <strong style={{ color: "#FDE047" }}>{activeModalItem.active_squadrons}</strong>
              </div>
            )}

            {activeModalItem.homeported_ships && (
              <div style={{ fontSize: "0.72rem", color: "#E2E8F0" }}>
                <span style={{ color: "#94A3B8" }}>Homeported Fleet: </span>
                <strong style={{ color: "#34D399" }}>{activeModalItem.homeported_ships}</strong>
              </div>
            )}

            <div style={{ fontSize: "0.72rem", color: "#CBD5E1", lineHeight: 1.4, borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: "6px" }}>
              <span style={{ color: "#94A3B8", display: "block", fontSize: "0.65rem", fontFamily: "var(--font-mono)", marginBottom: "2px" }}>STRATEGIC DOCTRINE & ROLE:</span>
              {activeModalItem.strategic_role}
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: "5px", fontSize: "0.65rem", fontFamily: "var(--font-mono)", color: "#94A3B8" }}>
              <span>Coords: {activeModalItem.lat?.toFixed(2)}°N, {activeModalItem.lon?.toFixed(2)}°E</span>
              <span>{activeModalItem.provenance || "Strategic Military Directory"}</span>
            </div>
          </div>

          <button
            onClick={() => onAskChatbot(activeModalItem)}
            className="btn-cyber btn-cyber-primary"
            style={{ width: "100%", padding: "7px", fontSize: "0.75rem", display: "flex", alignItems: "center", justifyContent: "center", gap: "5px" }}
          >
            <Bot size={14} />
            <span>Analyze Base Posture with Sentinel AI</span>
          </button>
        </div>
      )}

      {/* -------------------------------------------------------------
          NAVAL FLEET & CARRIER STRIKE GROUP MODAL
         ------------------------------------------------------------- */}
      {activeModalItem && activeModalItem.entityType === "fleet" && (
        <div
          style={{
            position: "absolute",
            top: "52px",
            right: "12px",
            width: "420px",
            maxHeight: "calc(100% - 90px)",
            background: "rgba(10, 16, 28, 0.98)",
            backdropFilter: "blur(20px)",
            border: "1.5px solid #F59E0B",
            borderRadius: "10px",
            zIndex: 40,
            overflowY: "auto",
            boxShadow: "0 12px 40px rgba(0, 0, 0, 0.85)",
            padding: "1.1rem",
            color: "#FFFFFF"
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "6px" }}>
            <div>
              <div style={{ fontSize: "0.68rem", fontFamily: "var(--font-mono)", color: "#FBBF24", textTransform: "uppercase", display: "flex", alignItems: "center", gap: "5px" }}>
                <Anchor size={12} />
                <span>NAVAL STRIKE GROUP • {activeModalItem.flag}</span>
              </div>
              <div style={{ fontFamily: "var(--font-heading)", fontWeight: 800, fontSize: "1.05rem", color: "#FFFFFF", marginTop: "2px" }}>
                {activeModalItem.name}
              </div>
            </div>
            <button
              onClick={() => {
                setActiveModalItem(null);
                updateRangeRings(null);
              }}
              style={{ background: "transparent", border: "none", color: "#94A3B8", cursor: "pointer" }}
            >
              <X size={16} />
            </button>
          </div>

          {/* Official Navy Press Release & News Handle Verification Section */}
          <div style={{ background: "rgba(245, 158, 11, 0.12)", border: "1px solid #F59E0B", borderRadius: "6px", padding: "8px", marginBottom: "10px" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "4px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "5px", color: "#FDE047", fontSize: "0.72rem", fontWeight: 800, fontFamily: "var(--font-heading)" }}>
                <Award size={14} />
                <span>OFFICIAL PRESS RELEASE & NEWS DISPATCH</span>
              </div>
              <span style={{ background: "#F59E0B", color: "#030712", fontSize: "0.62rem", fontWeight: 900, padding: "2px 5px", borderRadius: "3px", fontFamily: "var(--font-mono)" }}>
                {activeModalItem.official_verification_badge || "NAVY VERIFIED"}
              </span>
            </div>

            <div style={{ fontSize: "0.68rem", color: "#94A3B8", marginBottom: "4px", fontFamily: "var(--font-mono)" }}>
              <strong>Issuing Authority: </strong>
              <span style={{ color: "#E2E8F0" }}>{activeModalItem.verified_official_source || activeModalItem.source}</span>
            </div>

            <div style={{ background: "rgba(3, 7, 18, 0.7)", borderLeft: "3px solid #F59E0B", padding: "6px 8px", borderRadius: "0 4px 4px 0", fontSize: "0.72rem", fontStyle: "italic", lineHeight: 1.4, color: "#F1F5F9", marginBottom: "6px" }}>
              "{activeModalItem.official_dispatch_quote || `Active naval group deployed in ${activeModalItem.region} carrying out scheduled maritime security missions.`}"
            </div>

            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: "0.65rem", fontFamily: "var(--font-mono)", color: "#CBD5E1" }}>
              <span>Confirmed: <strong>{activeModalItem.official_confirmation_date || "2026-08-30"}</strong></span>
              {activeModalItem.official_source_url && (
                <a
                  href={activeModalItem.official_source_url}
                  target="_blank"
                  rel="noreferrer"
                  style={{ color: "#38BDF8", textDecoration: "none", display: "inline-flex", alignItems: "center", gap: "2px" }}
                >
                  <span>Official Navy Portal</span>
                  <ExternalLink size={9} />
                </a>
              )}
            </div>
          </div>

          {/* Carrier Strike Radius & Marked Boundary Controls */}
          <div style={{ background: "rgba(239, 68, 68, 0.1)", border: "1px solid rgba(239, 68, 68, 0.35)", borderRadius: "6px", padding: "7px 10px", marginBottom: "8px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
            <div>
              <div style={{ fontSize: "0.65rem", color: "#FCA5A5", fontFamily: "var(--font-mono)" }}>VISIBLE CARRIER AIR WING STRIKE RADIUS</div>
              <div style={{ fontSize: "1.05rem", fontWeight: 900, color: "#FFFFFF", fontFamily: "var(--font-display)" }}>
                {activeModalItem.air_wing_strike_radius_nm || 550} NM ({activeModalItem.combat_radius_km || 1020} km)
              </div>
            </div>
            <button
              onClick={() => {
                const next = !showCombatRadius;
                setShowCombatRadius(next);
                updateRangeRings(activeModalItem);
              }}
              style={{
                padding: "5px 8px",
                fontSize: "0.66rem",
                background: showCombatRadius ? "#EF4444" : "rgba(3,7,18,0.8)",
                color: "#FFFFFF",
                border: "1px solid #EF4444",
                borderRadius: "4px",
                fontWeight: 700,
                cursor: "pointer"
              }}
            >
              {showCombatRadius ? "● Strike Range Boundary (ON)" : "○ Show Strike Boundary"}
            </button>
          </div>

          {/* Warship Roster Table */}
          <div style={{ marginBottom: "10px" }}>
            <div style={{ fontSize: "0.68rem", fontFamily: "var(--font-heading)", color: "#CBD5E1", fontWeight: 700, marginBottom: "4px" }}>
              CONFIRMED WARSHIP ROSTER ({activeModalItem.ships?.length || 0})
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: "3px", maxHeight: "150px", overflowY: "auto" }}>
              {activeModalItem.ships?.map((ship, idx) => (
                <div key={idx} style={{ background: "#111827", padding: "5px 8px", borderRadius: "4px", border: "1px solid rgba(255,255,255,0.06)", display: "flex", alignItems: "center", justifyContent: "space-between", fontSize: "0.72rem" }}>
                  <div>
                    <strong style={{ color: "#FFFFFF" }}>{ship.name}</strong> <span style={{ color: "#38BDF8", fontFamily: "var(--font-mono)" }}>({ship.hull})</span>
                    <div style={{ fontSize: "0.65rem", color: "#94A3B8" }}>{ship.type} • {ship.country}</div>
                  </div>
                  <div style={{ textAlign: "right", fontFamily: "var(--font-mono)", fontSize: "0.68rem", color: "#34D399" }}>
                    <div>{ship.speed}</div>
                    <div style={{ color: "#94A3B8" }}>{ship.status}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => onAskChatbot(activeModalItem)}
            className="btn-cyber btn-cyber-primary"
            style={{ width: "100%", padding: "7px", fontSize: "0.75rem", display: "flex", alignItems: "center", justifyContent: "center", gap: "5px" }}
          >
            <Bot size={14} />
            <span>Analyze Fleet Posture with AI</span>
          </button>
        </div>
      )}

      {/* -------------------------------------------------------------
          WORLD LEADER & EVENT MODALS
         ------------------------------------------------------------- */}
      {activeModalItem && activeModalItem.entityType === "leader" && (
        <div
          style={{
            position: "absolute",
            top: "52px",
            right: "12px",
            width: "350px",
            background: "rgba(8, 14, 26, 0.98)",
            backdropFilter: "blur(16px)",
            border: "1px solid rgba(245, 158, 11, 0.4)",
            borderRadius: "8px",
            zIndex: 40,
            padding: "1.1rem",
            color: "#FFFFFF",
            boxShadow: "var(--shadow-hud)"
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
            <img src={activeModalItem.avatar_url} alt={activeModalItem.name} style={{ width: "44px", height: "44px", borderRadius: "50%", border: "2px solid #F59E0B" }} />
            <div>
              <div style={{ fontFamily: "var(--font-heading)", fontWeight: 800, fontSize: "1rem" }}>{activeModalItem.name}</div>
              <div style={{ fontSize: "0.68rem", color: "#94A3B8" }}>{activeModalItem.title}</div>
            </div>
          </div>

          <div style={{ background: "rgba(3, 7, 18, 0.6)", padding: "8px", borderRadius: "6px", border: "1px solid var(--border-subtle)", fontSize: "0.78rem", lineHeight: 1.45, marginBottom: "10px" }}>
            <span style={{ color: "#FBBF24", fontSize: "0.68rem", fontFamily: "var(--font-heading)", fontWeight: 700, display: "block", marginBottom: "3px" }}>
              OFFICIAL POSTURE STATEMENT:
            </span>
            "{activeModalItem.last_statement}"
          </div>

          <button
            onClick={() => onAskChatbot(activeModalItem)}
            className="btn-cyber btn-cyber-primary"
            style={{ width: "100%", padding: "7px", fontSize: "0.75rem", display: "flex", alignItems: "center", justifyContent: "center", gap: "5px" }}
          >
            <Bot size={14} />
            <span>Analyze Statement Impact with AI</span>
          </button>
        </div>
      )}

      {/* Sourced Intelligence Event Modal */}
      {activeModalItem && activeModalItem.entityType === "event" && (
        <div
          style={{
            position: "absolute",
            top: "52px",
            right: "12px",
            width: "350px",
            background: "rgba(8, 14, 26, 0.98)",
            backdropFilter: "blur(16px)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "8px",
            zIndex: 40,
            padding: "1.1rem",
            color: "#FFFFFF",
            boxShadow: "var(--shadow-hud)"
          }}
        >
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", marginBottom: "6px" }}>
            <div>
              <div style={{ fontSize: "0.68rem", fontFamily: "var(--font-mono)", color: "var(--accent-cyan)", textTransform: "uppercase" }}>
                {activeModalItem.category} • SEVERITY S{activeModalItem.severity_global || activeModalItem.severity || 1}
              </div>
              <div style={{ fontFamily: "var(--font-heading)", fontWeight: 700, fontSize: "0.95rem", marginTop: "2px" }}>
                {activeModalItem.title}
              </div>
            </div>
            <button
              onClick={() => setActiveModalItem(null)}
              style={{ background: "transparent", border: "none", color: "var(--text-muted)", cursor: "pointer" }}
            >
              <X size={16} />
            </button>
          </div>

          <div style={{ fontSize: "0.78rem", color: "#CBD5E1", lineHeight: 1.4, marginBottom: "10px" }}>
            {activeModalItem.summary}
          </div>

          <button
            onClick={() => onAskChatbot(activeModalItem)}
            className="btn-cyber btn-cyber-primary"
            style={{ width: "100%", padding: "7px", fontSize: "0.75rem", display: "flex", alignItems: "center", justifyContent: "center", gap: "5px" }}
          >
            <Bot size={14} />
            <span>Analyze with RAG Intelligence Chatbot</span>
          </button>
        </div>
      )}
    </div>
  );
}
