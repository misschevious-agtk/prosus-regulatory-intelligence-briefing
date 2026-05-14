---
batch-id: fb-YYYY-MM-DD-HHMM
generated-at: <ISO-8601 UTC>
generated-by: website-feedback-widget v0.3
votes: <total in this batch>
votes-up: <count>
votes-down: <count>
status: ready-for-feedback-integration
---

<!--
  This template documents the shape the website's "Export feedback" button
  produces. The operator does not edit this file directly — the website widget
  writes it. The template lives here so the feedback-integration skill has a
  canonical reference and so any future agent that synthesises feedback by
  hand can match the shape.

  Drop the generated file into queue/feedback/inbox/ for processing.
-->

# Feedback batch — YYYY-MM-DD · <N> new votes

## Summary by monitor

- M01 · <n> votes (<up> up · <down> down)
- M02 · <n> votes (<up> up · <down> down)
- …one line per monitor that has votes in this batch…

## Votes

### <MXX> · <theme-id> · <article title>

- **Vote:** 👍 helpful  *or*  👎 not for me
- **Article ID:** `<article-id-slug>`
- **Monitor:** <MXX> (`<monitor-folder-id>`)
- **Topic / Category:** <theme-id> (<catLabel>)
- **Country:** <country-code>
- **URL:** <source url>
- **Voted at:** <ISO-8601 UTC>

> <optional one-line reason from the operator — blockquoted so it parses cleanly>

<!-- repeat one section per vote -->

## What the Orchestrator should do with this

1. Re-thread these articles against the dimensions in `system/skills/feedback-integration.md` — keywords, source tiers, ranking rules, theory-of-harm tags.
2. Watch for clusters (≥3 votes on the same theme / source / jurisdiction) before changing weights — per CLAUDE.md Rule 6, one 👎 is a signal, not a verdict.
3. Output a delta report to `generated/reports/YYYY-MM-DD-feedback-delta.md`. Never edit prior findings or briefs.
4. Archive this batch to `queue/feedback/_processed/YYYY-MM-DD/` once the delta report is written.
