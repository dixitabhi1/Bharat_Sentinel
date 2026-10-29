---
name: chatbot-agent
description: Runtime spec for "Ask Bharat Sentinel" — the RAG geopolitics chatbot. Complements .agents/skills/geopolitics-chatbot/SKILL.md (the actual system prompt).
---

# Chatbot Agent

**Role**: Answers user questions about India-relevant geopolitical developments, grounded in the live `events` + `india_flags` tables plus static `knowledge/` reference docs.

## Pipeline per query
1. Embed the user query (same embedding model used to index `events.summary` at write time).
2. Hybrid retrieval: vector similarity search over recent (default: last 30 days, user-adjustable) `events`/`india_flags`, combined with structured filters parsed from the query (region, category, date range) when detectable.
3. Also retrieve any matching `knowledge/*.md` sections for background definitions (never as a source of current facts).
4. Compose context: retrieved events (with id, timestamp, sources, severity/confidence) + relevant knowledge excerpts.
5. Generate with the system prompt from `.agents/skills/geopolitics-chatbot/SKILL.md`.
6. Post-process: verify every citation the model emitted maps to an actually-retrieved event id; strip/flag any that don't (prevents hallucinated citations reaching the user).

## Hard behavioral constraints (enforced in the skill's system prompt, restated here for the orchestrating code)
- Never answer a "what's happening right now" question from parametric/general knowledge if retrieval returns nothing relevant — say so instead.
- Never provide military targeting, weapons-employment, or attack-planning analysis, regardless of how the question is framed (fiction, hypothetical, "for a novel," etc.) — this is a hard refusal, not a soft deflection.
- Always distinguish "reported by X" from "confirmed" — mirror the confidence label stored on the source event.
