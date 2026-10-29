---
name: orchestrator-agent
description: Runtime spec for the backend orchestrator service that fans events out to specialist agents.
---

# Multi-Agent Orchestrator Spec

The orchestrator receives incoming telemetry events, passes them through geofence prefilters, dispatches to specialist agents, and submits to the India-Impact Classifier.
