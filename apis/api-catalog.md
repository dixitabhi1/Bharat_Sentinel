---
name: api-catalog
description: Every external API this project needs, whether it's used, free-tier status, and which module consumes it. Read before writing any ingestion code.
---

# API Catalog

All entries carried over from the base project's API research, plus India-specific additions/notes.

## News & Events
| API | Free? | Used by |
|---|---|---|
| GDELT 2.0 (DOC API + Events DB) | Free, no key | Base ingestion; primary source for Troop/Buildup Agent and Leader-Statement Agent (filter by South Asia + relevant countries) |
| ACLED | Free (academic/nonprofit); commercial needs license | Structured conflict/protest events — good corroboration source for border-incident reporting |
| Google News RSS | Free, no key | Supplemental per-keyword feed (e.g., "LAC," "Line of Control," specific ministry names) |
| Official RSS: PIB India, MEA India, MoD India | Free, public | **Primary, highest-trust source for Leader-Statement Agent's India-side statements** |

## Aircraft (ADS-B) — Budget-Governed Dual-Redundancy Proxy
| API | Free? | Used by |
|---|---|---|
| OpenSky Network | Free, non-commercial license, OAuth2, rate-limited | Primary ADS-B source — pre-filter to India/LAC/LoC bounding boxes via server proxy |
| adsb.lol / airplanes.live | Free, community, no key required | Secondary redundant ADS-B source — automated fallback on OpenSky 429/error, military vector enrichment |

## Strategic Infrastructure & Installations (Display-Only)
| API / Source | Free? | Used by |
|---|---|---|
| OpenStreetMap (OSM) Extract | Free, ODbL open community data | Static installations layer (Airbases, Naval Bases, Commercial Ports, ALGs, Chokepoints). Strictly display-only; no live feed joins. |

## Ships (AIS)
| API | Free? | Used by |
|---|---|---|
| aisstream.io | Free, WebSocket, no SLA | Naval/Maritime Agent — subscribe with bounding boxes for Arabian Sea, Bay of Bengal, Hormuz, Malacca |

## Earthquakes / Fires / Connectivity (feed the Domestic Stability Dashboard + base map)
| API | Free? | Used by |
|---|---|---|
| USGS Earthquake feed | Free, no key | Disaster layer, South Asia filtered |
| NASA FIRMS | Free `MAP_KEY` | Wildfire layer, South Asia filtered |
| Cloudflare Radar | Free tier | Internet-outage signal for Domestic Stability Dashboard |
| IODA | Free | Corroboration for outage signals |

## Geocoding
| API | Free? | Used by |
|---|---|---|
| GeoNames | Free w/ account, rate-limited | Place-name resolution for all agents |

## LLM / Agent runtime
| API | Notes |
|---|---|
| Anthropic API (Claude) | Structured-output calls for all specialist agents + chatbot; **use function-calling/structured JSON mode for every classifier agent output**, not free-text parsing |

## Explicitly not used (documented, not silently skipped)
- **X/Twitter API** — no viable free tier; excluded from MVP per base project's API research.
- **Satellite imagery tasking** — no free/public API for on-demand tasking; Troop/Buildup Agent relies on *news reporting that references* satellite imagery (e.g., Maxar-sourced stories), not raw imagery access.
- **Any classified/government-restricted feed** — out of scope by design (see ethics doc).

## Config
See `config/.env.example` for every credential this catalog implies.
