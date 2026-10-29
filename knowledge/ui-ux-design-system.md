---
name: ui-ux-design-system
description: UI/UX design system for Bharat Sentinel — futuristic command HUD, cyber aesthetics, glowing reticles, scanlines, and tactical typography.
---

# Bharat Sentinel UI/UX Design System

## 1. Palette & Color Taxonomy
- **Primary Cyber Dark**: `#030712`, `#0B132B`, `#0D182E`
- **Accent Cyan / Radar**: `#22D3EE` (Telemetry & Sensors)
- **Accent Emerald**: `#10B981` (Confirmed Live Feeds & Peace/Disaster Readiness)
- **Accent Amber**: `#F59E0B` (Delayed Data & Tier 2 Alerts)
- **Accent Crimson**: `#EF4444` (Tier 4 Breaking Signals & Human Review Queue)
- **Accent Violet**: `#A855F7` (Simulated Injects & Domain Agents)
- **Border Subtle**: `rgba(34, 211, 238, 0.18)`

## 2. Freshness Badges
- `LIVE` 🟢 `background: rgba(16, 185, 129, 0.2); border: 1px solid #10B981; color: #34D399;`
- `DELAYED` 🟡 `background: rgba(245, 158, 11, 0.2); border: 1px solid #F59E0B; color: #FBBF24;`
- `ESTIMATED` 🔵 `background: rgba(56, 189, 248, 0.2); border: 1px solid #38BDF8; color: #7DD3FC;`
- `SIMULATED` 🟣 `background: rgba(168, 85, 247, 0.2); border: 1px solid #A855F7; color: #C084FC;`

## 3. Command HUD Overlays
- Atmospheric globe glow on 3D spherical rendering
- Scanline CSS backdrop overlay (`background-size: 100% 4px;`)
- Tactical corner brackets on command panels (`hud-corners`)
- Glowing pulsating beacon markers for high-severity signals
