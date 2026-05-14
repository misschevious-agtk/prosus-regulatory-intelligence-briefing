---
skill: feedback-integration
description: Process a feedback batch dropped by the website widget — re-thread the voted-on articles against keywords / source tiers / ranking rules and emit a delta report. Phase 4c of the network roadmap.
trigger: A new `fb-YYYY-MM-DD-HHMM.md` file lands in `queue/feedback/inbox/`. Can also be invoked manually.
output: `generated/reports/YYYY-MM-DD-feedback-delta.md` + retrospective re-thread of the affected articles in `findings/` and `_brain/link-map.md`.
version: 1.0
last-updated: 2026-05-14
---

# Skill — Feedback integration

The operator and named anchors vote on articles directly from the website (`website/monitor-XX/`). Each vote is a thumbs-up or thumbs-down plus an optional one-line reason. Votes accumulate in the browser's `localStorage`. When the operator clicks **Export feedback** in the topbar, the widget writes a markdown batch named `fb-YYYY-MM-DD-HHMM.md` and drops it into the user's downloads. The operator moves that file into `queue/feedback/inbox/` and the Orchestrator picks it up.

This skill defines what happens then. It is the Phase 4c "feedback writeback" loop alluded to in `CLAUDE.md`'s current weekly focus, and the practical implementation of the architectural promise that the network is feedback-shaped, not just feed-shaped.

## Trigger

- A new file matching `queue/feedback/inbox/fb-*.md` is detected (scheduled scan, or invoked manually).
- Manual invocation: operator says "process the feedback batch" or names a specific batch file.

If multiple batches are present, process them in filename order (which is chronological because of the `YYYY-MM-DD-HHMM` stamp). Emit one delta report per batch — never merge batches silently, the audit trail matters.

## Context required

1. `CLAUDE.md` — operating rules 1–10, especially **Rule 6** (one 👎 is a signal, not a verdict) and **Rule 4** (no publish without a change-log row).
2. The batch file itself — frontmatter for shape, body for the votes.
3. The current state of the affected articles. For each voted article ID, locate it in `findings/` (or `monitors/monitor-XX/items.json` / `website/monitor-XX/items.json` if not yet in findings).
4. The dimensions the system re-threads against (see `feedback_retrospective_rethreading.md` in operator memory, mirrored here for self-contained reading):
   - per-monitor `keywords.md` (four-tier)
   - per-monitor `needs.md` and `profile.md`
   - `portfolio-map.md`, `our_markets.md`, `our_stack.md`, `sectoral-overlays.md`
   - `gazetteer.yml` entity entries
   - `findings/instruments/` doctrinal anchors
   - `strategy.md` ranking rules (Rules 1–21) and source-tier assignments
   - theories of harm (M02 specific)
5. The last two delta reports in `generated/reports/` — to detect repeat signals (a third 👎 on the same source escalates posture; a first 👎 does not).

## Process

Two passes — forward (what the votes are telling us) and retrospective (re-thread the corpus).

### Pass 1 — read the batch

1. Parse the frontmatter (`votes`, `votes-up`, `votes-down`, `batch-id`).
2. For each vote, locate the article (by `article_id` within the monitor named in `monitor_id`). If the article is no longer present, record it as `orphan` in the delta — do not invent a match.
3. Cluster votes by (a) monitor, (b) theme/topic, (c) source domain, (d) jurisdiction (`country` field), (e) any gazetteer entity matched in the title. This clustering is what drives Rule 6's "pattern, not verdict" threshold.

### Pass 2 — produce candidate signals

Each cluster with **≥3 votes in the same direction** is a candidate signal. Below that threshold the votes are logged but do not move weights. Per Rule 6, the threshold for persona reconciliation is "patterns at ~15 items over four weeks"; this skill uses **3 votes per cluster per batch** as the lower bar for *flagging* a signal in the delta report, not for *acting*. Action across batches still requires the persona-reconciliation cadence.

For each candidate signal, classify:

- **Keyword drift** — the voted-on articles share a tier-3 or tier-4 keyword that consistently produces 👎. Candidate: demote keyword to a lower tier or move to `keywords.md` "stop" list.
- **Source-tier reassignment** — the voted-on articles come from the same source domain. If 👎 dominates, candidate Tier-A → Tier-B demotion (or Tier-B → "auto-review" gate). If 👍 dominates on a current Tier-C, candidate promotion.
- **Ranking-rule edge case** — the voted-on articles all fire the same Rule (1–21) but the operator disagrees with the rank. Candidate: open a `strategy.md` PR to refine the rule's trigger condition. Do **not** widen a locked filter; see Rule 1.
- **Theory-of-harm mismatch** (M02 only) — the voted-on articles all map to the same theory-of-harm tag but the anchor disagrees. Candidate: edit the theory-of-harm anchor wording.
- **Jurisdiction misrouting** — votes saying "wrong jurisdiction" cluster on a single country code. Candidate: re-check the country tagger and Rule 21/22 routing.

### Pass 3 — retrospective re-thread (per `feedback_retrospective_rethreading.md`)

This is the part that distinguishes the brain from a feed reader.

For every article in the batch — *including* the ones below the action threshold — the Orchestrator and Static Workflow run an **additive-only** sweep:

- Re-evaluate the article against every keyword tier in its monitor's `keywords.md`. If a new keyword match appears (because keywords have been added since the article was first ranked), record it.
- Re-check gazetteer matches. New gazetteer entries since first-rank may surface new entity links.
- Re-check cross-monitor membership (Rule 21/22). The same article may now route to a second monitor it didn't reach the first time.
- Record new `[[wikilinks]]` and tags in `_brain/link-map.md`. Never edit prior findings, reasoning, or briefs — if a re-score materially changes a prior candidate's rank, log it as a delta and let the *current* Adjudicator decide whether to revisit.

### Pass 4 — write the delta report

See "Output format" below. The delta report is the single artefact a human reads from this skill. Everything else (link-map additions, gazetteer tags) is silent infrastructure.

### Pass 5 — archive the batch

Move the input file from `queue/feedback/inbox/<file>.md` to `queue/feedback/_processed/YYYY-MM-DD/<file>.md`. Per `CLAUDE.md` Rule 3, never delete — the queue history stays auditable.

## Output format

Save to `generated/reports/YYYY-MM-DD-feedback-delta.md`:

```markdown
---
date: YYYY-MM-DD
batch-id: <from input frontmatter>
generated-by: feedback-integration skill v1.0
generated-at: <ISO-8601>
votes-processed: <n>
clusters-detected: <n>
candidate-signals: <n>
status: ready-for-operator-review
---

# Feedback delta — YYYY-MM-DD · batch <batch-id>

## What the operator voted on
<2–3 sentence summary. Which monitors, rough up/down split, anything that stands out from the reasons.>

## Candidate signals
<For each cluster meeting the ≥3-vote threshold, one block:

### Signal X · <one-line headline>
- **Cluster:** <monitor / theme / source / jurisdiction>
- **Direction:** 👍 / 👎 / mixed
- **Votes in cluster:** <n>
- **Candidate change:** <one of: keyword drift / source-tier reassignment / ranking-rule edge case / theory-of-harm mismatch / jurisdiction misrouting>
- **Proposed action:** <specific edit — file + line + new value>
- **Rule 6 cross-check:** <"first occurrence; log only" OR "second occurrence; recommend persona-reconciliation cycle" OR "third+ occurrence; escalate this batch">
- **Operator decision:** ☐ accept ☐ defer ☐ reject  ← operator fills in
>

## Sub-threshold votes
<bulleted list of votes that did NOT cluster to ≥3. One line each. Helpful for spotting trends across batches.>

## Retrospective re-thread additions
<List of articles whose `_brain/link-map.md` entries gained new wikilinks / tags / cross-monitor membership during this run. Append-only. Reference the link-map by line, not by reproducing the link itself.>

## Orphan votes
<Votes whose `article_id` could not be located in `findings/`. One line each — what was voted on, when, where it might have gone.>

## What I did NOT do
<Anything this skill deliberately left alone. Example: "Did not demote source ABC despite three 👎 votes — they all came from the same batch within 24h, which fails the four-week persona-reconciliation threshold." This section is what makes the report trustworthy.>
```

## Quality bar

- **No locked-filter widening.** Per Rule 1, this skill cannot propose widening a locked filter. If a candidate signal would require it, the report must say "blocked — requires `strategy.md` PR" and stop there.
- **Additive only.** The retrospective re-thread never edits prior findings, briefs, or reasoning. Re-threading injects links and tags; rank changes are deltas, not rewrites. Per the `feedback_retrospective_rethreading.md` principle.
- **One 👎 is not a verdict.** The lower bar for *flagging* a signal is 3 votes in a cluster; the bar for *acting* on it crosses batches via persona reconciliation. Do not let a single batch swing the network's weights.
- **Operator decisions are explicit.** Every candidate signal carries `☐ accept ☐ defer ☐ reject` checkboxes. The Orchestrator does not auto-merge accepted signals; the operator runs a separate skill (`redline-integration` or a future `signal-apply`) to commit them.
- **Confidentiality pre-filter still binds.** Per Rule 7, if any voted-on article is in `findings/_confidential/`, the delta report excludes it from the public delta and writes a sealed note to `findings/_confidential/_brain/feedback-confidential.md` instead.

## Interactions with other skills

- **`monitor-performance-review`** consumes the running set of delta reports to produce the monthly per-monitor scorecard.
- **`weekly-synthesis`** references the most recent delta report in its "what's shifting in the network" section.
- **`anchor-handoff-brief`** does *not* incorporate feedback automatically — Anne-Claire's votes go through redline first.
- **Persona reconciliation cadence** (`cadences/persona-reconciliation.md`) is the cross-batch consumer of delta reports for M01.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. Delivers Phase 4c (feedback writeback) per `CLAUDE.md` current weekly focus. Wired to the website thumbs widget v0.3. | K. Maleevska |
