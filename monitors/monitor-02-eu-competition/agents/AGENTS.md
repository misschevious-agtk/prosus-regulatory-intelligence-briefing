---
title: M02 Agent Cell — index
monitor: M02 (Competition, global)
anchor: Anne-Claire Hoyng
status: active
last-updated: 2026-05-14
---

# M02 Agent Cell

The six agents that run inside Monitor 02. See [[../../agents-architecture|the architecture doc]] for the pattern; this index is the M02-specific instance.

M02 is a *single-anchor* monitor (Anne-Claire Hoyng). The agents serve four doctrinal reading-modes, not four personas. Scope is global, not EU-only — the folder name is a legacy artefact.

| # | Agent | File |
|---|---|---|
| 0 | Orchestrator | [[00-orchestrator]] |
| 1 | Regulations | [[01-regulations]] |
| 2 | Sourcing & Connecting | [[02-sourcing-connecting]] |
| 3 | Static Workflow | [[03-static-workflow]] |
| 4 | Legal Reasoning | [[04-legal-reasoning]] |
| 5 | Adjudicator | [[05-adjudicator]] |

## Reading-modes this cell serves (doctrinal, not persona)
- [[../antitrust-cartels/README|Antitrust & Cartels]]
- [[../abuse-of-dominance/README|Abuse of Dominance]]
- [[../merger-control-fdi/README|Merger Control & FDI]]
- [[../digital-markets-sector-state-aid/README|Digital Markets, Sector Reg & State Aid]]

## Brain
- `_brain/link-map.md` — every concept and its edges
- `_brain/reflections/YYYY-WW.md` — weekly reflections
- `_brain/adjudicator-log.md` — every override the Adjudicator made
- `_brain/cross-monitor-bridges.md` — M02 ↔ M01 edges (Rule 21)

## Weekly run order
1. Sourcing & Connecting sweeps `clippings/inbox/` + RSS + email
2. Regulations updates `findings/instruments/`
3. Static Workflow produces candidates
4. Legal Reasoning produces the *so what* (calibrated to Anne-Claire's voice)
5. Adjudicator produces the brief + decision log
6. Orchestrator runs the reflection + link-map update

## Anchor note
Anne-Claire Hoyng is the sole human anchor. The Adjudicator's brief is a recommendation to her; she signs off (or redlines) before anything goes out. Calibration to her voice and priorities is an explicit agent responsibility (see [[04-legal-reasoning]]).
