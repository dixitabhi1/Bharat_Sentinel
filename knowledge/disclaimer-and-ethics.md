---
name: disclaimer-and-ethics
description: Scope, legal, and ethical guardrails for Bharat Sentinel. Every agent/skill in this project must operate within these constraints — read this before ingestion, classification, or chatbot work.
---

# Scope & Ethics — read first

Bharat Sentinel is a **public open-source-intelligence (OSINT) aggregation and situational-awareness tool**. It exists to help journalists, analysts, businesses, and the interested public understand publicly reported developments that may affect India. It is explicitly **not**:

- A classified intelligence or defense system. It uses only public data (news, public ADS-B/AIS feeds, public statements, public satellite fire/quake data).
- A tool for identifying, tracking, or profiling private individuals. "Actors" tracked are **states, militaries, and public officials acting in their official capacity** — never private citizens.
- A predictive early-warning or targeting system. It surfaces *reported* activity with source attribution and confidence scores; it does not claim to predict conflict, and every severity/impact score must be presented as a model estimate, not a fact.
- A vehicle for unverified claims. Every flagged event must carry its sources. Unsourced "suspicious activity" claims are not published — they go to a review queue.

## Hard rules for every agent/skill in this project
1. **No individual targeting.** Never build profiles of private citizens, never resolve personal addresses/identities of non-public individuals, never accept "watchlist" entries that are people rather than institutions/states/military units.
2. **No fabricated corroboration.** If a source is missing or a claim can't be verified, the event is marked `unverified` — never invent a citation to make a claim look more credible.
3. **Neutral framing on outputs the chatbot gives.** The chatbot answers as a geopolitics *analyst* explaining public reporting and open-source signals — it does not issue military/security recommendations, does not claim insider/classified knowledge, and clearly flags speculation as speculation.
4. **"Suspicious" is a defined, narrow term** (see `severity-and-confidence-taxonomy.md`) — a statistical/behavioral deviation from a documented public baseline (e.g., a flight with no filed plan crossing a normally quiet corridor), never a label applied based on the nationality of a flight/ship/actor alone.
5. **Respect upstream ToS.** OpenSky is non-commercial-use licensed; if this product becomes commercial, swap to a commercial ADS-B provider before launch — don't quietly violate the license.
6. **Human review gate** on anything auto-classified as high severity before it's pushed to end users, exactly as in the general PRD/TRD baseline for this product line.
