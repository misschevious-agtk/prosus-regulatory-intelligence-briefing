---
title: queue/feedback — the loop between the website and the brain
description: Where website-exported vote batches land for the Orchestrator to process via the feedback-integration skill.
version: 1.0
status: active
last-updated: 2026-05-14
---

# queue/feedback

This is the inbox half of the feedback loop. The website (`website/monitor-XX/`) has a thumbs widget on every article card. Each vote is stored in the browser's `localStorage`. When the operator clicks **Export feedback** in the topbar, the widget produces an `fb-YYYY-MM-DD-HHMM.md` file and drops it into the user's downloads.

The operator moves that file here, into `queue/feedback/inbox/`. The Orchestrator picks it up and invokes the `feedback-integration` skill (see `system/skills/feedback-integration.md`). The skill writes a delta report to `generated/reports/`, re-threads the affected articles against the network's dimensions (keywords, source tiers, gazetteer entries, theories of harm), and archives the batch here to `_processed/YYYY-MM-DD/`.

## Folder shape

```
queue/feedback/
├── README.md           ← you are here
├── inbox/              ← drop fb-YYYY-MM-DD-HHMM.md files here
└── _processed/         ← archived batches, organised by date
    └── 2026-MM-DD/     ← one folder per processing day
```

Per `CLAUDE.md` Rule 3, processed batches are **archived, not deleted**. The audit trail for what feedback was acted on lives here permanently.

## What the website produces

A batch file has this shape (see `queue/_templates/FEEDBACK.md` for the canonical template):

```markdown
---
batch-id: fb-2026-05-14-1530
generated-at: 2026-05-14T15:30:00Z
generated-by: website-feedback-widget v0.3
votes: 7
votes-up: 4
votes-down: 3
status: ready-for-feedback-integration
---

# Feedback batch — 2026-05-14 · 7 new votes

## Summary by monitor
- M01 · 4 votes (3 up · 1 down)
- M02 · 3 votes (2 up · 1 down)

## Votes
### M01 · ai-news · CCI suo-motu AI probe
- **Vote:** 👎 not for me
- **Article ID:** `cci-suo-motu-ai-2026-05`
- **Monitor:** M01 (`monitor-01`)
- **Topic / Category:** ai-news (AI Policy)
- **Country:** IN
- **URL:** …
- **Voted at:** 2026-05-14T15:22:03Z
> wrong jurisdiction for this topic — should be in M02
…
```

## What happens next

1. The Orchestrator detects the new batch (scheduled scan or manual invocation).
2. It loads `system/skills/feedback-integration.md` and follows the five-pass process: parse → cluster → produce candidate signals → retrospective re-thread → write delta report.
3. The delta report lands in `generated/reports/YYYY-MM-DD-feedback-delta.md`, with explicit `☐ accept ☐ defer ☐ reject` checkboxes on each candidate signal. The operator decides; nothing auto-merges.
4. The batch file moves to `_processed/YYYY-MM-DD/<batch>.md`.

## Rules that bind this loop

- **Rule 6 — one 👎 is not a verdict.** The skill flags clusters of ≥3 votes per batch; cross-batch action goes through persona reconciliation.
- **Rule 1 — locked filters are not for widening via feedback.** If a candidate signal would widen a locked filter, the skill blocks the change and tells the operator to open a `strategy.md` PR instead.
- **Rule 7 — confidentiality pre-filter still binds.** Votes on items in `findings/_confidential/` are not exposed in public delta reports.
- **Retrospective re-thread is additive only** (per `feedback_retrospective_rethreading.md`). The brain re-reads prior articles when new dimensions appear; it never edits prior findings or briefs.

## How to wipe local browser state

If the operator wants to start fresh in the browser — for example, after exporting and processing a batch and confirming the delta — the **Feedback** dropdown in the website topbar has a **Clear local feedback** button. That wipes the `localStorage` for this browser only. Already-exported batches in this folder are not affected.
