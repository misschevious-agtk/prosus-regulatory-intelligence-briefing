---
skill: daily-rollup
description: Parse the day's operator daily-note conventions and route them — Change History rows, feedback log entries, queue items, reconciliation flags.
trigger: End-of-working-day or first thing the next morning.
output: Routed entries written to the destinations defined by each convention. Summary log in generated/briefings/YYYY-MM-DD-rollup.md.
version: 1.0
last-updated: 2026-05-14
---

# Skill — Daily rollup

The operator writes one daily note (`daily/YYYY-MM-DD.md`) using a small set of conventions Claude parses. The daily-rollup skill picks those conventions up and routes them — so that "DECISION: switched M02 abuse-of-dominance Prosus Relevance Filter from medium to tight" becomes (a) a Change History row in the right place, (b) an entry the weekly synthesis reads, and (c) a note in the persona reconciliation memory.

The conventions are deliberately small. Adding more is a cost paid in operator vigilance, not in capability.

## Conventions parsed

| Prefix | Meaning | Routed to |
|--------|---------|-----------|
| `DECISION:` | Operator made a structural decision (filter, source, cap, persona, naming). | Change History of the affected monitor (or `strategy.md` if system-wide) + `generated/briefings/YYYY-MM-DD-rollup.md` |
| `REDLINE:` | Anchor returned a redline. Operator logs the receipt — full integration runs via `redline-integration` skill. | Queue: `queue/REDLINE-<monitor>-block<N>.md` is created if not already present |
| `ANCHOR_FEEDBACK:` | Anchor said something the operator wants captured (not a redline, more general). | The anchor's monitor `findings/feedback/anchor-notes.md` (append) |
| `ESCALATED:` | Operator escalated a finding outside the brief cycle. | The monitor's `findings/escalations/YYYY-MM-DD/` log (append) |
| `SOURCE_ADDED:` | Operator added a source. | `scripts/sources.yml` flagged for review + Change History row drafted |
| `SOURCE_DEMOTED:` | Operator demoted or removed a source. | Same routing as SOURCE_ADDED; **never auto-applied** if it removes a Tier-1 source — surfaces to operator. |
| `FEEDBACK:` | Operator's own feedback (👍 / 👎 / annotation) on a finding. | The monitor's `findings/feedback/` log |
| `QUESTION:` | Operator's open question for the synthesis pass. | Added to the next weekly synthesis run's input list |

Any line that does not start with a known prefix is treated as prose for the rollup file. It is not routed.

## Trigger

- Operator runs `system/skills/daily-rollup` at end of day.
- Or the next morning's `operator-morning-brief` runs the rollup as its first action.

## Context required

1. `daily/YYYY-MM-DD.md` for the date being rolled up.
2. The most recent `_rollup` summary to identify lines that have already been processed (idempotency).

## Process

1. Read the daily note line by line.
2. For each line with a known prefix: parse, classify, route.
3. For lines without a prefix: aggregate into the rollup file as prose.
4. Mark each routed line in the daily note itself with a trailing `[rolled-up: YYYY-MM-DD-HH:MM]` marker so a second run does not double-route.
5. If a routing requires operator sign-off (Tier-1 source removal, locked filter widening), do **not** apply — drop a note in the rollup file and a stub in `queue/`.
6. Write the rollup summary to `generated/briefings/YYYY-MM-DD-rollup.md`.

## Output format

The rollup file:

```markdown
---
date: YYYY-MM-DD
generated-by: daily-rollup skill v1.0
generated-at: <ISO-8601>
status: ready-to-read
---

# Daily rollup — YYYY-MM-DD

## Decisions logged
<one bullet per DECISION: line, with target file path it was routed to.>

## Redlines received
<one bullet per REDLINE: line, with queue file created.>

## Anchor feedback captured
<one bullet per ANCHOR_FEEDBACK: line, with target file appended.>

## Escalations
<one bullet per ESCALATED: line.>

## Source moves
<adds and demotions, with sign-off status.>

## Feedback events
<count and any thematic clustering.>

## Questions captured for synthesis
<one bullet per QUESTION: line.>

## Loose notes (prose, no prefix)
<prose lines verbatim. Not routed.>
```

## Quality bar

- **Idempotent.** Running the rollup twice does not produce duplicate routing.
- **Never auto-removes a Tier-1 source.** Always flags.
- **Never auto-widens a locked filter.** Always flags.
- The rollup file is **short**. If it is long, the daily note was dense — that is a signal, not a failure of the skill.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. | K. Maleevska |
