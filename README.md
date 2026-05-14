# Prosus Legal Intelligence Briefing

A modular architecture for a network of legal-intelligence monitors, each run by its own Claude agent with memory and feedback-driven learning. The end state is a website surfacing the output of every monitor, all governed by a single shared spec.

> **The structure is the product as much as the content is.** Any team — Tax, Treasury, Comms, ESG, M&A — can clone this folder, swap the persona / sources / purpose, leave the template intact, and run their own monitor network.

---

## How it works (operationally)

Each monitor is one folder under `monitors/`. The folder contains a `SYSTEM-PROMPT.md` (or `monitor.md` for legacy single-persona monitors) that **is the spec** the Claude agent reads on every run. The spec tells the agent who it serves, where to look, what to surface, what to ignore, how to present output, and how to learn over time.

A monitor may have **one persona** (the legacy single-persona archetype) or **multiple domain personas** sharing a schema and ranker (the current Monitor 01 archetype). The architecture supports both.

A run loop looks like this:

1. **Agent reads `SYSTEM-PROMPT.md`** for the monitor.
2. **Agent reads its per-domain context** (persona, needs, interrogation checklist) for the domain in question.
3. **Agent scans the sources** within the recency window, applying user-set and locked filters.
4. **Agent produces findings** in the format defined by `output-schema.md`.
5. **Ranker assigns A/B/C/D** mechanically from `ranking-criteria.md` enumerated fields.
6. **Agent appends to the Feedback Log** as 👍 / 👎 come in. Behaviour compounds.
7. **Agent records spec edits** in Change History — separate from feedback.

---

## Folder structure

```
prosus-legal-intelligence-briefing/
├── README.md                       ← this file
├── strategy.md                     ← overarching strategy + cross-monitor rules
├── portfolios.md                   ← which monitors cover what; coverage matrix
├── cold-start-protocol.md          ← how a brand-new monitor behaves on day one
├── keyword-conventions.md          ← four-tier keyword pattern shared by all monitors
├── glossary.md                     ← shared domain language (DMA, FSR, ADM, MFN, TCC, NAV…)
├── HOW-THIS-THINKS.md              ← architecture explainer for engineering handoff (Phase 5)
│
├── _template/                      ← reference for the legacy single-persona archetype
│   └── monitor-template.md
│
├── _archive/                       ← superseded specs (read-only)
│   ├── README.md
│   └── superseded-pre-system-prompt/
│       └── monitor-01-digital-regulatory/   ← pre-system-prompt draft of M01, superseded
│
└── monitors/
    ├── monitor-01/                 ← Monitor 01 — multi-persona (AI / Privacy / IP / Legal Ops)
    │   ├── SYSTEM-PROMPT.md
    │   ├── README.md
    │   ├── output-schema.md         ← shared across all four domains
    │   ├── ranking-criteria.md      ← shared, Rules 1–21 baked in
    │   ├── operating-preferences.md ← shared, Block 3 cadences + 6 doc types + escalation review
    │   ├── our_markets.md           ← shared context
    │   ├── our_stack.md             ← shared context
    │   ├── sectoral-overlays.md     ← shared context
    │   ├── portfolio-map.md         ← shared context
    │   ├── responsible-ai-policy.pdf
    │   ├── responsible-ai-policy-summary.md
    │   ├── ai-news/{profile, needs, interrogation-checklist, keywords}.md
    │   ├── privacy-data-protection/{profile, needs, interrogation-checklist, keywords}.md
    │   ├── intellectual-property/{profile, needs, interrogation-checklist, keywords}.md
    │   ├── legal-ops/{profile, needs, interrogation-checklist, keywords}.md
    │   └── findings/                ← findings, briefs, indexes, digests, board summaries, incidents
    │
    └── monitor-02-eu-competition/  ← Monitor 02 — multi-persona (Antitrust / Abuse of Dominance / Merger & FDI / Digital Markets)
        ├── SYSTEM-PROMPT.md
        ├── README.md
        ├── output-schema.md         ← shared across all four domains
        ├── ranking-criteria.md      ← shared, Rules 1–21 (8 baseline + 11 domain-specific + 1 cross-monitor)
        ├── operating-preferences.md ← shared, Block 3 cadences + 7 doc types + escalation review + confidentiality framing
        ├── our_markets.md           ← shared context — competition jurisdictions
        ├── our_stack.md             ← shared context, mirror of M01 with competition-lens annotations
        ├── sectoral-overlays.md     ← shared context — competition-relevant sector subset
        ├── portfolio-map.md         ← shared context — per-OC competition exposure + dominance map
        ├── antitrust-cartels/{profile, needs, interrogation-checklist, keywords}.md
        ├── abuse-of-dominance/{profile, needs, interrogation-checklist, keywords}.md
        ├── merger-control-fdi/{profile, needs, interrogation-checklist, keywords}.md
        ├── digital-markets-sector-state-aid/{profile, needs, interrogation-checklist, keywords}.md
        └── findings/                ← findings, briefs, indexes, digests, board summaries, incidents
```

---

## The Prosus Relevance Filter

Every Prosus monitor shares one filter: **is this Prosus-adjacent?** It's the single most important filter we have and the one that bonds the monitor family together. It is defined system-wide so it is applied consistently.

An item is Prosus-relevant if one or more of the following is true:

- A **Prosus Group entity** is named or directly affected (Prosus N.V., Naspers, MIH, etc.).
- A **portfolio company** is named or directly affected (current holdings in `portfolios.md`).
- A **Prosus operating market** is the subject of new rule-making in the monitor's domain (India, Brazil, EU, US, UK, China, South Africa, Netherlands, Indonesia, Singapore, Poland, plus regional aggregates).
- A **Prosus investment thesis** is implicated — for example, food delivery, classifieds, fintech, edtech, GenAI infrastructure, payments rails.
- The item creates a **horizontal precedent** likely to be applied to a Prosus business within 12 months.

### Strictness levels

Each monitor sets its own strictness level for this filter:

| Level    | Behaviour                                                                                                |
|----------|----------------------------------------------------------------------------------------------------------|
| **Tight**   | Only surface items where a Prosus entity, portfolio company, or operating market is **directly** named or affected. Lowest noise, highest precision. |
| **Medium**  | Surface direct hits and items with **clear read-through** to a Prosus business within 12 months. Default for most monitors. |
| **Loose**   | Surface direct hits, read-throughs, and items establishing a **horizontal precedent** that could plausibly reach Prosus. Use for monitors covering fast-moving frontier areas (AI, crypto, new digital-services regimes). |

When in doubt, **start tight**. Loosening is easy. Tightening after a persona has been spammed for two weeks is harder.

---

## Index of monitors

> Maintained by hand. Update when a new monitor is added.

**Current scope:** two monitors, both multi-persona archetype.

| ID                          | Name                          | Archetype                     | Owner                                          | Status                                                |
|-----------------------------|-------------------------------|-------------------------------|------------------------------------------------|-------------------------------------------------------|
| `monitor-01`                | Monitor 01                    | Multi-persona (4 domains)     | Group Legal & Public Policy (K. Maleevska)     | **Calibration mode (Day 0 of 14)** — Initialisation complete (Blocks 1, 2, 3) on 12 May 2026 |
| `monitor-02-eu-competition` | Competition Law Monitor       | Multi-persona (4 domains, single named anchor) | Group Legal & Public Policy — Anne-Claire Hoyng (named anchor); K. Maleevska (operator) | **Initialisation complete (Blocks 1, 2, 3) drafted 13 May 2026; pending Anne-Claire redline before go-live** |

The two monitors are deliberately complementary. M01 cross-cuts every operating market across AI / Privacy / IP / Legal Ops with four distinct in-house counsel personas. M02 covers competition law across four doctrinal domains (antitrust & cartels, abuse of dominance, merger control & FDI, digital markets & sector regulation & state aid) handled as four reading-modes of a single named anchor (Anne-Claire Hoyng, Global Head of Competition Policy). M02's scope is global, not EU-only — though the directory name retains the `-eu-competition` suffix from its original placeholder for cross-reference stability.

The architectural pattern (multi-persona, shared spec, populated profile/needs files, Block 1–3 initialisation, twenty-two rank rules on M01 and twenty-one on M02 including one cross-monitor rule each) is now applied consistently across both monitors. Cross-monitor cross-references are governed by Rule 21 in M02 and the symmetric Rule 22 in M01 (added 2026-05-14, closing the Block 3 sign-off flag). The dedup engine is exercised against `scripts/tests/dedup_golden.yml` by `scripts/test_dedup.py`.

**Domain naming convention**: frontmatter uses short slugs (`ai-news`, `privacy`, `ip`, `legal-ops` for M01; `antitrust-cartels`, `abuse-of-dominance`, `merger-control-fdi`, `digital-markets-sector-state-aid` for M02). Folder names within `monitors/<monitor>/` are the **verbose** form for human readability (`privacy-data-protection/`, `intellectual-property/`). Scripts that join frontmatter to folders use the folder name; scripts that route findings use the frontmatter slug. The JSON Schema enforces the slug form.

**Archived (genuinely superseded — pre-system-prompt single-persona drafts):**

| ID                              | Name                          | Archetype                | Status     |
|---------------------------------|-------------------------------|--------------------------|------------|
| `monitor-01-digital-regulatory` | Digital & Regulatory Monitor  | Single-persona, 9-section | Archived — its scope is now covered by the multi-persona Monitor 01  |
| `monitor-02-eu-competition` (legacy)  | EU Competition Law Monitor    | Single-persona, 9-section | Archived — superseded by multi-persona reading-mode architecture with Anne-Claire Hoyng as named anchor, May 13 2026 |

Preserved in `_archive/superseded-pre-system-prompt/` for traceability.

---

## How to create a new monitor

Two archetypes are supported:

### Archetype A — Single-persona (legacy)
1. Pick a stable ID: `monitor-<NN>-<slug>`.
2. `cp _template/monitor-template.md monitors/monitor-<NN>-<slug>/monitor.md`
3. Fill in every section.
4. Add a row to the index above and to `portfolios.md`.
5. Run `cold-start-protocol.md` for the first 2 weeks.

### Archetype B — Multi-persona (current — see Monitor 01)
1. Pick a stable ID: `monitor-<NN>` or `monitor-<NN>-<slug>`.
2. Mirror the structure of `monitors/monitor-01/`: a `SYSTEM-PROMPT.md` operating spec, shared `output-schema.md` and `ranking-criteria.md`, shared context files (`our_markets.md`, `our_stack.md`, `sectoral-overlays.md`, `portfolio-map.md`), per-domain folders with `profile.md`, `needs.md`, `interrogation-checklist.md`, plus a `findings/` folder.
3. The operator drafts the SYSTEM-PROMPT (or reuses Monitor 01's with edits).
4. The operator answers Block 1 / Block 2 / Block 3 of the SYSTEM-PROMPT's INITIALISATION section before the agent populates profile/needs files.
5. Run `cold-start-protocol.md` for the first 2 weeks.

---

## Rules every team must follow

- The template file `_template/monitor-template.md` is **read-only**. To evolve it, version it and record the change here.
- Every monitor has the **same 9 sections in the same order**. No reordering, no renamed headers, no skipped sections.
- **Locked filters** (Section 6 of every monitor) are honoured by the agent at all times. Feedback can only move the user-set layer.
- **One 👎 is a signal, not a verdict.** Act on patterns, not single votes.
- **Source removal requires owner sign-off** and a row in the monitor's Change History (Section 9).
- **Cross-monitor deduplication** follows the rule in `strategy.md` (Section: Deduplication). If a regulator action is caught by three monitors, exactly one surfaces it as primary; the others link to it.

---

## Template history

| Version | Date       | Change                                            |
|---------|------------|---------------------------------------------------|
| 1.0     | 12 May 2026 | Initial template — 9 sections, locked-filter inheritance, card-action contract. |

---

## Where the website fits in

Each `monitor.md` is the spec. The **website** is the surface — it reads from the same data model the agents produce and renders the per-item card with the four required actions (Copy, Summarise, Share, Open source). A working prototype lives at `prosus-digital-regulatory-monitor.html` in the parent folder. It is currently wired to `monitor-01-digital-regulatory`; the same renderer will host every additional monitor.
