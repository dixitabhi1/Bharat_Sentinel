---
name: reference-project-gods-eye-view
description: Architectural patterns for OSINT live maps, including the budget-governed proxy pattern, live data provenance labeling, and 3D globe projection.
---

# Reference Architecture — God's Eye View Pattern

## 1. Budget-Governed Ingestion Proxy
- Upstream free-tier and community APIs (OpenSky, adsb.lol, USGS, GDELT, AISStream) have strict or variable rate limits.
- The **Budget-Governed Proxy** acts as a single gateway running on the backend:
  - In-memory TTL caching (10–15s) shields upstream providers from multiple client polls.
  - Multi-provider redundancy: Primary queries are backed by secondary community providers (e.g. OpenSky + adsb.lol).
  - Merging and deduplication happens server-side by unique identifier (e.g. `ICAO24` or `MMSI`).
  - Frontend clients never contact upstream providers directly.

## 2. Data Freshness & Provenance Labeling
Every telemetry point presented on the situational map carries:
- **State**: `live` (confirmed real-time telemetry), `delayed` (cached/stale feed), `estimated` (extrapolated vector), or `simulated` (scenario inject).
- **Timestamp**: Exact ISO 8601 UTC timestamp of observation.
- **Provider Provenance**: Clear attribution string (e.g. "OpenSky Network (ADS-B)", "adsb.lol Community", "aisstream.io (AIS)").

## 3. Projection & Rendering
- **3D Globe Projection** (`projection: 'globe'` in WebGL via MapLibre GL JS) provides distortion-free polar and hemispheric situational awareness.
- Flat Mercator toggle (`projection: 'mercator'`) allows conventional tactical grid navigation.
