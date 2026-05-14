---
title: Agents Architecture — the brain inside each monitor
version: 0.1 (M01 + M02 scaffold)
status: active
author: K. Maleevska
last-updated: 2026-05-14
---

# Agents Architecture

This is the cognitive layer inside each monitor. The repo already defines *what* a monitor watches (sources, filters, personas). This doc defines *how a monitor thinks* — the set of agents that read, regulate, source, connect, reason, and adjudicate, and how they grow the brain over time.

The brain is the workspace folder. The workspace folder is the Obsidian vault. Every agent's output is a Markdown file with `[[wikilinks]]`, which means the graph thickens every time the system runs. That is the design intent: a brain that keeps connecting.

---

## The 5 + 1 pattern

Each monitor runs the same six-agent cell. Five workers, one adjudicator.

| # | Agent | One-line job | Reads from | Writes to |
|---|---|---|---|---|
| 0 | **Orchestrator** | Keeps the brain learning and connecting. Owns the graph. | Everything the monitor has ever produced | `monitors/monitor-XX/agents/_brain/` (concept notes, link maps, weekly reflections) |
| 1 | **Regulations** | Tracks the actual legal instruments — bills, acts, guidelines, draft texts, cases. | Official sources + clipped HTML tagged `#instrument` | `monitors/monitor-XX/findings/instruments/` |
| 2 | **Sourcing & Connecting** | Finds new sources, ingests clipped HTML, tags entities, threads pieces into existing concepts. | RSS, email, `clippings/inbox/` | `monitors/monitor-XX/clippings/processed/`, entity stubs |
| 3 | **Static Workflow** | The connector. Runs the fixed pipeline: fetch → rank → cluster → schema-check → emit. Deterministic, auditable. | Sourcing output + ranker + gazetteer | `monitors/monitor-XX/findings/candidates-YYYY-WW.md` |
| 4 | **Legal Reasoning** | Reads candidates and instruments and produces the *so what* — Prosus exposure, doctrinal framing, second-order risk. | Candidates + instruments + portfolio map | `monitors/monitor-XX/findings/reasoning-YYYY-WW.md` |
| 5 | **Adjudicator** | The final call. Decides what makes the brief, what gets demoted, what gets escalated. One per monitor. | All four upstream outputs + operating-preferences + ranking-criteria | `monitors/monitor-XX/findings/brief-YYYY-WW.md` |

The Orchestrator is numbered 0 because it doesn't sit in the weekly pipeline — it sits above it. It runs continuously, reads everything, and rewrites the connective tissue.

---

## Why these five, and not three or ten

The shape of the cell maps to the four things a legal-intelligence operator actually does, plus the meta-layer that makes the system grow:

- **Watch the law itself** → Regulations
- **Watch the world talk about the law** → Sourcing & Connecting
- **Standardise what you found** → Static Workflow
- **Decide what it means for us** → Legal Reasoning
- **Decide what's worth saying** → Adjudicator
- **Decide what the system should learn from this round** → Orchestrator

If an agent doesn't map to one of those six jobs, it doesn't belong in the cell. New agents go through the Orchestrator first; if the Orchestrator can't justify the addition in one line, the cell stays at six.

---

## How the brain grows

Every run produces three classes of artefact:

1. **Findings** (weekly, dated) — candidates, reasoning, the brief. Lives under `findings/`.
2. **Instruments** (evergreen, versioned) — one note per legal instrument (e.g. `[[AI Act]]`, `[[DMA]]`, `[[DPDP]]`). Lives under `findings/instruments/`. Updated, never duplicated.
3. **Brain notes** (Orchestrator output) — concept notes, link maps, weekly reflections, cross-monitor bridges. Lives under `agents/_brain/`.

The Orchestrator's job is to make sure (1) and (2) keep linking to each other and to (3). Concretely, after every weekly run the Orchestrator:

- Scans new findings for entities and concepts that don't yet have a brain note → creates stubs.
- Updates the link map (`agents/_brain/link-map.md`) — a single document listing every concept and what it connects to.
- Writes a weekly reflection (`agents/_brain/reflections/YYYY-WW.md`) — what surprised the cell, what dedup hit Rule 21, what the Adjudicator overrode and why.
- Flags cross-monitor edges to the sibling monitor's Orchestrator (M01 ↔ M02), which is how Rule 21 dedup actually fires in practice.

This is the connecting part of the brief. It's not magic — it's a discipline of always writing the next link before closing the loop.

---

## Clipper intake — two paths, one destination

Klimentina uses the Obsidian Web Clipper to capture HTML pages. There are two ways into the brain, both supported:

**Path A — Inbox folder (preferred for volume):**
- Configure the Web Clipper to save HTML into `monitors/monitor-XX/clippings/inbox/`.
- File naming: `YYYY-MM-DD_<short-slug>.html`.
- The Sourcing & Connecting agent (or its scheduled task) sweeps `inbox/` on each run, parses, tags, files into `clippings/processed/<year>/<week>/`, and links new entities into the brain.

**Path B — Chat upload (one-offs):**
- Drop the HTML into the conversation.
- Claude routes it through the same parse-tag-file step and tells you where it landed.

Both paths converge on `clippings/processed/`. Nothing else ever writes there directly.

See per-monitor `clippings/README.md` for the exact filename convention and Web Clipper settings.

---

## Persona file + runnable subagent — the dual form

Every agent exists twice:

- **Persona file** — a Markdown note inside the monitor (`monitors/monitor-XX/agents/<n>-<name>.md`). This is the source of truth. It has frontmatter, a mission, inputs, process, outputs, failure modes, and `[[wikilinks]]` into the rest of the brain. It shows up in the Obsidian graph. It clones cleanly when another team forks the repo.
- **Runnable subagent** — a thin wrapper under `.claude/agents/<monitor>-<name>.md`. This is what Claude actually invokes via the Task tool. The wrapper has YAML frontmatter (`name`, `description`, `tools`) and a one-paragraph body that says: *read the persona file at `<path>` and operate accordingly*. The wrapper exists so Claude can route work; the persona file is where the substance lives.

Update the persona, not the wrapper. The wrapper should rarely change.

---

## Adjudicator — one per monitor

Each monitor has exactly one Adjudicator. Not one per persona, not one per reading-mode. The Adjudicator is monitor-scoped because cross-persona conflict resolution is its job: when M01's AI persona and Privacy persona disagree about whether a story is for AI Counsel or Privacy Counsel, the Adjudicator decides.

The Adjudicator reads:
- All four upstream agent outputs for the week
- `operating-preferences.md`
- `ranking-criteria.md` (the 21 rules)
- The last four weeks of its own decisions, to stay coherent

The Adjudicator emits a single weekly brief plus a *decision log* line for every override (`agents/_brain/adjudicator-log.md`). The decision log is what the Orchestrator reads to spot drift.

---

## How this scales

The cell is the unit. To scale:

- **Add a monitor (e.g. Tax, Treasury, ESG, M&A)** → copy a `monitor-XX/` folder, edit personas, edit the six agents, ship. The architecture doesn't change.
- **Add a team inside a monitor** → add a reading-mode/persona file. The six agents already accommodate it because they're monitor-scoped, not persona-scoped.
- **Cross-monitor coordination** → only the Orchestrators talk to each other. Workers stay in their cell. Rule 21 dedup is an Orchestrator-to-Orchestrator handshake, mediated by `_brain/cross-monitor-bridges.md`.

When this hits five+ monitors, the pattern that breaks first is the weekly reflection cadence. At that point we promote the Orchestrators to a federation-level *Council* that meets (i.e. produces a coordinated brain note) once per cycle. That's a future concern. Documented here so we don't forget.

---

## What this is *not*

- Not a substitute for the human anchor (Klimentina for M01, Anne-Claire Hoyng for M02). The Adjudicator's brief is a *recommendation*; the anchor signs off.
- Not a replacement for `strategy.md`, `ranking-criteria.md`, `operating-preferences.md`, or `output-schema.md`. Those are the rules; the agents *execute* the rules.
- Not autonomous. Every run is invoked, every output is reviewed. The brain grows because Klimentina runs it, not because it runs itself. (Yet.)

---

## See also

- [[README]] — repo overview
- [[strategy]] — locked filters, source tiers, dedup
- [[HOW-THIS-THINKS]] — the operator's mental model
- [[portfolios]] — coverage matrix
- [[monitors/monitor-01/agents/AGENTS|M01 agent cell]]
- [[monitors/monitor-02-eu-competition/agents/AGENTS|M02 agent cell]]
