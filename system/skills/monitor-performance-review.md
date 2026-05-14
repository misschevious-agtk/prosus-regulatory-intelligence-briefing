---
skill: monitor-performance-review
description: End-of-calibration and quarterly performance review for a single monitor.
trigger: A monitor reaches Day 14 of calibration OR quarterly schedule (first week of Jan/Apr/Jul/Oct) OR operator request.
output: generated/reports/YYYY-MM-monitor-XX-performance.md
version: 1.0
last-updated: 2026-05-14
---

# Skill — Monitor performance review

The performance review is to a monitor what a one-on-one is to a person on your team. Once at end-of-calibration to ratify the monitor as ready for steady-state. Once a quarter thereafter to keep it honest. Either way the goal is the same: did the monitor earn its place this period, and if so, what does it need next.

## Trigger

- A monitor crosses Day 14 of its calibration cycle (operator-set; see `cold-start-protocol.md`).
- The first week of January, April, July, October.
- Explicit operator request: "run performance review on M01".

## Context required

1. `CLAUDE.md` — operating rules.
2. The monitor's `SYSTEM-PROMPT.md`.
3. The monitor's full `findings/feedback/` log for the period (calibration: 14 days; quarterly: 90 days).
4. Brief volume per day vs the monitor's daily cap (`operating-preferences.md`).
5. Null-briefing count and reasons.
6. Escalation count and reasons.
7. Source promotions / demotions in the period.
8. Persona reconciliation events (out-of-cycle and scheduled).
9. The previous performance review file if one exists.

## Process

Six passes.

1. **Volume and cap discipline.** What was the mean and max daily brief volume? How often did the monitor hit the cap? Did the cap get raised (and if so, did `strategy.md` get a row)?
2. **Feedback shape.** 👍 / 👎 ratio per domain. The number of items with no feedback at all (a quiet 👎 is still a 👎). Any concentration of 👎 by theme.
3. **Filter integrity.** Did any locked filter get widened? (If yes, the monitor failed regardless of other metrics — surface immediately.) Did the user-set Prosus Relevance Filter strictness move?
4. **Source health.** Promotions / demotions in the period. Any Tier-1 source that went silent. Any Tier-3 commentary source over-cited.
5. **Cross-monitor behaviour.** How many items did this monitor surface that overlapped another monitor's catch? How many cross-references were issued vs received? How many overrides (`dedup-override`)?
6. **What it needs next.** Three asks max. Ranked by leverage. Phrased as concrete edits to the spec, not aspirations.

## Output format

Save to `generated/reports/YYYY-MM-monitor-XX-performance.md`:

```markdown
---
monitor: <monitor-id>
period: <calibration-day14 | YYYY-Qx>
generated-by: monitor-performance-review skill v1.0
generated-at: <ISO-8601>
status: draft-for-operator-review
---

# Performance review — <monitor> — <period>

## Volume and cap discipline
<stats + one-paragraph narrative.>

## Feedback shape
<ratios per domain + any thematic clusters.>

## Filter integrity
<locked filter status. User-set Prosus Relevance Filter trajectory.>

## Source health
<promotions / demotions / silent sources / over-cited.>

## Cross-monitor behaviour
<overlap, cross-references issued / received, overrides.>

## What this monitor needs next — three asks ranked
1. <ask 1 — concrete spec edit, not aspiration>
2. <ask 2>
3. <ask 3>

## Verdict
<one-sentence: pass to steady-state | extend calibration | structural change needed>
```

## Quality bar

- **Quantitative claims tied to log entries.** No "the monitor seems to be doing well". Either it is or it isn't, and the log says which.
- **Filter widening is a fail condition.** Even one. Surface it.
- **The three asks are spec edits.** Not "the persona could be improved". Specifically what should change in `needs.md` lines X–Y.
- The verdict is **one of three states** and binding. If unsure between two, write "extend calibration".

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. | K. Maleevska |
