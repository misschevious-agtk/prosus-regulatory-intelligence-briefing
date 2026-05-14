---
title: CLAUDE.md — the network constitution
description: The first file Claude reads in any session. Tells Claude who runs this, how this thinks, what it must never do, and what matters this week.
version: 1.0
status: active
author: K. Maleevska
last-updated: 2026-05-14
---

# CLAUDE.md — Read this first

> If you are an agent (Claude or otherwise) running anywhere in this repo, read this file **before** doing anything else. Then read the file or files it points you to for the specific task. Do not skip ahead.

This is the constitution of the Prosus Legal Intelligence Briefing network. It tells you who the operator is, what the network is, the order you should read context in, the rules you must follow when acting autonomously, and the focus of the current week. The companion files (`README.md`, `strategy.md`, `HOW-THIS-THINKS.md`, `agents-architecture.md`) go deeper. This file is the always-on context layer that sits on top of them.

---

## Who runs this

**Klimentina Maleevska** — Group Legal & Public Policy at Prosus N.V. — is the **operator**. She designs and maintains the monitor specs, the locked filters, the feedback architecture, and the network as a whole. She is not the typical consumer of any single monitor; named anchors are. Today the only named anchor is **Anne-Claire Hoyng** (Global Head of Competition Policy), consumer of Monitor 02. Other monitors will acquire named anchors as the network grows.

When in doubt: optimise for the operator's leverage, not for individual monitor output. The architecture is the moat. The monitors are tenants.

---

## What this network is — in one paragraph

A federated network of legal-intelligence monitors for Prosus's Group Legal & Public Policy function. Each monitor is a long-running Claude agent with a persona (or several), a defined source set, a Prosus Relevance Filter at a chosen strictness, eight system-wide locked filters, twenty-plus ranking rules including one cross-monitor dedup rule, a feedback memory that compounds over weeks, and a fixed-shape output. Two monitors are live as of 14 May 2026: **M01** (multi-persona — AI / Privacy / IP / Legal Ops) in calibration mode Day 0 of 14, and **M02** (Competition Law — four doctrinal reading-modes, single named anchor Anne-Claire Hoyng) initialised but pending Anne-Claire's redline. The structure is replicable: any team — Tax, Treasury, ESG, M&A — can clone the folder and run their own monitor network.

If this paragraph reads as outdated when you find yourself here, fix it. This file is the source of truth for "what is the network, right now".

---

## Read in this order

| Step | File | What it gives you |
|------|------|-------------------|
| 1 | `CLAUDE.md` (this file) | Constitution, current focus, operating rules |
| 2 | `strategy.md` | Locked filters 1–8, Prosus Relevance Filter, cross-monitor dedup rule, source tiers, escalation, confidentiality pre-filter |
| 3 | `README.md` | Folder layout, monitor index, how to create a new monitor |
| 4 | `HOW-THIS-THINKS.md` | Architecture rationale — why each design choice exists |
| 5 | `agents-architecture.md` | The 5 + 1 agent pattern that runs inside each monitor |
| 6 | the specific monitor's `SYSTEM-PROMPT.md` | The per-monitor constitution Claude reads when operating that monitor |
| 7 | the specific `system/skills/<skill>.md` | The exact prompt and contract for whatever skill is being invoked |

You almost never need all seven. For a queued research task you read this file, `strategy.md`, and the relevant skill file. For weekly synthesis you add the monitor's SYSTEM-PROMPT and its `findings/` folder. For redline integration you add the anchor's redline notes and the affected Blocks 1–3.

---

## Where things live

The repo is laid out for both humans and agents. The numbered folders are operational (you write into them); the un-numbered folders are infrastructural (you read from them or they organise themselves).

- `monitors/` — per-monitor specs, personas, and findings. Each monitor is autonomous within shared rules.
- `system/skills/` — the codified skills Claude invokes (anchor handoff, weekly synthesis, redline integration, performance review, deep research). One file per skill. Read the skill file before performing the skill.
- `queue/` — operator's inbox to the network. Drop a file here describing what you need (`RESEARCH-<topic>.md`, `ANCHOR-BRIEF-<anchor>-W<NN>.md`, `REDLINE-<monitor>-block<N>.md`); the system picks it up and processes it.
- `generated/` — every autonomous output lands here, never elsewhere. Subfolders: `briefings/`, `research/`, `handoffs/`, `syntheses/`, `reports/`. Files in `generated/` are not edited in place — they are reviewed, then either promoted into the monitor's `findings/` or archived.
- `daily/` — operator log, one file per working day. Inline conventions (DECISION:, REDLINE:, ANCHOR_FEEDBACK:, ESCALATED:, SOURCE_ADDED:, FEEDBACK:) are parsed by the daily-roll-up skill.
- `cadences/` — operator-facing cadence docs (what the human does on what schedule). Pairs with `system/skills/` (what Claude does when invoked).
- `metrics/` — health and state-of-the-monitors snapshots.
- `scripts/` — the deterministic pipeline (fetch, rank, escalate, regulatory calendar, confidentiality filter, persona reconcile).
- `website/` — the surfacing layer (Netlify hub).
- `findings/`, `exports/` — per-monitor; this is where the monitor's own outputs land.
- `_template/`, `_archive/` — read-only.

When you create something new, put it where it belongs. If you cannot decide between two folders, you are probably about to create something that shouldn't exist yet.

---

## Operating rules for autonomous actions

These rules bind every agent in the network. They are not suggestions.

1. **Never widen a locked filter without a `strategy.md` change-log row.** The eight locked filters in `strategy.md` are the floor. Feedback can only move the user-set layer above them. If you find yourself wanting to override, write the change first.
2. **Never redefine "Prosus-adjacent" per monitor.** The definition lives in `README.md`. Only the strictness setting (tight / medium / loose) varies per monitor. If you want to change the definition itself, open a `strategy.md` PR.
3. **Never delete a file.** Move to `_archive/` with a one-line reason. The system values traceability over tidiness.
4. **Never publish without a change-log row.** Every spec edit, every redline integration, every source promotion / demotion gets a row in the relevant Change History (Section 9 of each monitor; the bottom of `strategy.md` for system-wide changes; the bottom of this file for constitutional changes).
5. **Never communicate on behalf of the operator.** Drafts of anchor-facing communications go to `generated/handoffs/` for operator review. Do not send, post, or hand off without explicit go-ahead.
6. **Never act on a single thumbs-down.** One 👎 is a signal, not a verdict. Persona reconciliation acts on patterns at ~15 items over four weeks (see `cadences/persona-reconciliation.md`).
7. **Never breach the confidentiality pre-filter.** Items matched by `scripts/lib_confidentiality.py` are quarantined to `findings/_confidential/` and never re-surface. You do not see them. You do not infer them.
8. **When in doubt, deposit in `generated/` and flag for operator review.** Better to surface something the operator discards than to drop something they would have wanted.
9. **Tight beats loose by default.** Widening attention is easy; winning it back after a noisy week is hard.
10. **The structure is the product.** When proposing a change that touches more than one monitor, ask whether the change belongs in `strategy.md` or in this file, not in the individual monitor's spec.

---

## What I want from you, agent

- **Surface connections across monitors I have not seen.** M01 and M02 will catch the same item via different lenses. The interesting cases are where the lenses disagree — same fact, different "why it matters", different recommended action. Flag those for me, do not silently dedup them.
- **Challenge the assumption before agreeing with it.** If I queue research on a premise that contradicts something I logged three weeks ago, tell me. Do not produce the briefing as though the contradiction does not exist.
- **Answer from the vault, not generically.** When I ask "what should we be watching this week", the answer must come from `findings/`, `metrics/`, the regulatory calendar, and the last week's `daily/` notes — not from your training data.
- **Flag stale focus.** If the "Current weekly focus" below is more than seven days old, refuse to use it; produce a draft update for me to approve.

---

## Current weekly focus

> Update every Monday morning. Five minutes. A stale focus produces stale answers.

**Week of 2026-W20 (Mon 11 May → Sun 17 May 2026)**

- **M01:** Day 0 of calibration. Goal of the week is to get to Day 5 without overriding a locked filter and without a single null briefing. Watch the four personas (AI / Privacy / IP / Legal Ops) for early thumbs-down clustering — that is the signal for an out-of-cycle persona reconciliation, not a quarterly one.
- **M02:** Anne-Claire's redline is the gating dependency. The pre-anchor handoff brief (`generated/handoffs/2026-W20-hoyng-anchor-handoff.md` — see below) is the artefact she should see first. Aim is redline returned by Fri 15 May.
- **Network:** Phase 4a (per-monitor website pages) and Phase 4b (article retrieval going live) are both pending. Neither blocks this week's calibration; both block the next named-anchor onboarding. **Phase 4c (feedback writeback) shipped 14 May** — website thumbs widget + `feedback-integration` skill + `queue/feedback/` inbox. Watch the first batch through the loop end-to-end before treating the phase as closed.
- **One question worth sitting with this week:** the M01 / M02 overlap on platform-liability rulings (CJEU, CMA, CCI). Rule 21 / Rule 22 dedup handles routing, but the *reasoning* file for each monitor produces a different "so what". Should the operator see both, or should the adjudicator pick one for the brief? This is a Phase 4c question (feedback writeback) but the design choice can be made this week.

---

## Constitutional change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial CLAUDE.md — promoted from implicit (read-everything-and-guess) to explicit constitution. Added reading order, operating rules 1–10, current weekly focus. | K. Maleevska |
| 2026-05-14 | **Phase 4c (feedback writeback) wired.** Website monitor pages now render a per-article thumbs widget (`website/shared/monitor.js` v0.3, `website/shared/monitor.css` v0.3). Votes accumulate in `localStorage`; the topbar "Feedback" panel exports them as `fb-YYYY-MM-DD-HHMM.md` batches. Batches land in `queue/feedback/inbox/`; the Orchestrator processes them via the new `system/skills/feedback-integration.md` and emits a delta report to `generated/reports/`. Re-threads prior articles against keywords / source tiers / gazetteer (additive only, per `feedback_retrospective_rethreading.md`). Respects Rule 6 (≥3-vote cluster threshold for flagging, persona-reconciliation cadence for acting) and Rule 1 (cannot widen locked filters). monitor-01/02 pages converted from inlined CSS/JS to external `../shared/` references; pre-patch copies kept as `index.html.bak.2026-05-14`. | K. Maleevska |
