---
name: installations-layer
description: Specification for the static, display-only installations layer (airbases, naval facilities, ports, airstrips, chokepoints). Strictly decoupled from live tracking feeds.
---

# Installations Layer (Static, Display-Only)

## 1. Purpose & Scope
The Installations Layer renders community-mapped strategic infrastructure locations across India, South Asia, and the Indian Ocean Region (IOR) sourced from OpenStreetMap (OSM) public extracts.

It provides geographic context for situational awareness — showing where major airbases, naval stations, commercial deep-water ports, Advanced Landing Grounds (ALGs), and maritime chokepoints are situated.

## 2. Mandatory Ethics & Legal Guardrails
1. **Display-Only Context**: This layer is strictly for background situational rendering.
2. **ZERO Join / Distance Computation**: Never compute distance, proximity, weapons range, threat radius, or engagement envelopes between any live contact (aircraft, vessel, fleet) and an installation.
3. **Community Attribution**: Every marker and layer header must clearly display:
   *"Community-mapped, may be incomplete or outdated. Display-only."*
4. **No Classified Facilities**: Sourced entirely from public OpenStreetMap nodes and tags (`aeroway=aerodrome`, `military=airfield`, `harbour=yes`, `seamark:type=harbour`).

## 3. Supported Infrastructure Categories
- **Airbase / Air Force Station**: Military and dual-use airbases (e.g. Ambala AFS, Bhatinda AFS, Hasimara AFS, Pune AFS, Leh AFS).
- **Naval Base / Station**: Coastal naval commands and berths (e.g. INS Kadamba Karwar, INS Hansa Goa, INS Rajali, INS Dega).
- **Commercial Deep-water Port**: Major maritime trade hubs (e.g. JNPT Mumbai, Chennai Port, Cochin Port, Colombo, Singapore, Gwadar, Chabahar).
- **Advanced Landing Ground (ALG) / Community Airstrip**: High-altitude forward airstrips (e.g. Daulat Beg Oldie, Nyoma, Fukche, Walong).
- **Strategic Maritime Chokepoint**: Global maritime straits and transit corridors (e.g. Strait of Malacca, Strait of Hormuz, Bab-el-Mandeb, Ten Degree Channel).
