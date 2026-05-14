---
skill: operator-morning-brief
description: Five-minute morning brief for the operator — overnight signal across monitors, what's stale, what's awaiting redline, what to do first today.
trigger: Mon–Fri 06:00 CET scheduled run.
output: generated/briefings/YYYY-MM-DD-morning.md
version: 1.0
last-updated: 2026-05-14
---

# Skill — Operator morning brief

The operator opens this before they open Slack, email, or the website hub. It is the equivalent of the daily content brief in the article — but for the operator of a legal-intelligence network, not for a content creator. The bar is five minutes to a working understanding of where the network stands.

## Trigger

Mon–Fri 06:00 CET. Skips weekends and Prosus holidays. Can be invoked manually at any time.

## Context required

1. `CLAUDE.md` — current weekly focus and operating rules.
2. Last 24 hours of new findings across every active monitor (use `findings/candidates-YYYY-WW.md` if the weekly file exists, else loose findings files).
3. The last 24 hours of escalations (`findings/escalations/YYYY-MM-DD/` across monitors).
4. Any new files dropped in `queue/` overnight.
5. Items in `findings/` older than seven days that are still flagged as "pending" or "awaiting anchor" — the staleness list.
6. The next 7 days from `scripts/regulatory_calendar.yml`.

## Process

1. **Rule 21 / 22 overlap check.** Did the same item land in M01 and M02 overnight? List the overlaps with the routing decision. If the routing surprises you, flag it.
2. **Escalations overnight.** Any item that hit `escalate.py`. One line each, ranked: 24-hour-OpCo trigger > breach incident > dawn-raid pattern > other.
3. **What's stale.** Items pending operator action for more than seven days. Anchor handoffs not yet redlined. Source promotion requests not yet decided.
4. **The queue.** What is sitting in `queue/` waiting to be processed today.
5. **First thing.** The single most leveraged action the operator should take this morning, drawn from the above. Not a list.

## Output format

Save to `generated/briefings/YYYY-MM-DD-morning.md`:

```markdown
---
date: YYYY-MM-DD
generated-by: operator-morning-brief skill v1.0
generated-at: <ISO-8601>
network-state: <calibration | steady-state | post-incident>
status: ready-to-read
---

# Operator morning brief — YYYY-MM-DD

## Overnight signal across monitors
<5-line max. New finding count per monitor + the one most consequential item.>

## Rule 21 / 22 overlap
<list of items caught by both M01 and M02 overnight, with routing. Or "None.">

## Escalations
<list with rank A / triggered rule / one-line reason. Or "None.">

## Stale and awaiting action
<items > 7 days old still pending. Anchor handoffs not redlined.>

## In the queue
<what is sitting in queue/ waiting today.>

## First thing
<one action. One sentence. Verb first.>

## Coming up — next 7 days
<3 lines max from regulatory_calendar.yml.>
```

## Quality bar

- **Under five minutes to read.** If the operator has to scroll, the brief is too long.
- **First thing is one action.** Not three. If you cannot pick, the synthesis is too shallow.
- **"None" is a valid section content.** Empty escalations are good news; the brief reports them honestly.
- The morning brief does not duplicate the weekly synthesis. The synthesis is for thinking; the morning brief is for doing.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. | K. Maleevska |
