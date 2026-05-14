---
title: M01 Agent Cell — index
monitor: M01 (Digital Regulatory)
status: active
last-updated: 2026-05-14
---

# M01 Agent Cell

The six agents that run inside Monitor 01. See [[../../agents-architecture|the architecture doc]] for the pattern; this index is the M01-specific instance.

| # | Agent | File |
|---|---|---|
| 0 | Orchestrator | [[00-orchestrator]] |
| 1 | Regulations | [[01-regulations]] |
| 2 | Sourcing & Connecting | [[02-sourcing-connecting]] |
| 3 | Static Workflow | [[03-static-workflow]] |
| 4 | Legal Reasoning | [[04-legal-reasoning]] |
| 5 | Adjudicator | [[05-adjudicator]] |

## Reading-modes this cell serves
- [[../ai-news/README|AI News]]
- [[../privacy-data-protection/README|Privacy & Data Protection]]
- [[../intellectual-property/README|Intellectual Property]]
- [[../legal-ops/README|Legal Ops]]

## Brain
- `_brain/link-map.md` — every concept and its edges
- `_brain/reflections/YYYY-WW.md` — weekly reflections
- `_brain/adjudicator-log.md` — every override the Adjudicator made
- `_brain/cross-monitor-bridges.md` — M01 ↔ M02 edges (Rule 21)

## Weekly run order
1. Sourcing & Connecting sweeps `clippings/inbox/` + RSS + email
2. Regulations updates `findings/instruments/`
3. Static Workflow produces candidates
4. Legal Reasoning produces the *so what*
5. Adjudicator produces the brief + decision log
6. Orchestrator runs the reflection + link-map update

The Orchestrator may also run between weekly cycles when intake is heavy.
