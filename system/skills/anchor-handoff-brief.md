---
skill: anchor-handoff-brief
description: Generate a one-page brief that prepares a named anchor to review their monitor's recent output.
trigger: A queue file named ANCHOR-BRIEF-<anchor>-W<NN>.md OR a scheduled run on the eve of an anchor review meeting OR an explicit operator request "run anchor-handoff-brief for <anchor>".
output: generated/handoffs/YYYY-WNN-<anchor>-anchor-handoff.md
version: 1.0
last-updated: 2026-05-14
---

# Skill — Anchor handoff brief

The anchor handoff brief is what a named anchor (e.g. Anne-Claire Hoyng for M02) sees **before** opening their monitor for the week's review. It tells them in one page what changed since last cycle, where their last redline landed, and what one decision is worth their time this week. The goal is to convert their review from a 45-minute scroll into a 10-minute calibration.

## Trigger

One of three:

- A file named `queue/ANCHOR-BRIEF-<anchor-slug>-W<NN>.md` is dropped by the operator.
- The scheduled run fires on the eve of the anchor review (operating-preferences.md sets the cadence — typically Friday afternoon for a Monday review).
- The operator types or messages "run anchor-handoff-brief for `<anchor>` week `<NN>`".

## Context required

Before drafting, read in this order:

1. `CLAUDE.md` — current weekly focus, operating rules.
2. The anchor's monitor `SYSTEM-PROMPT.md` — who they are, what they need, what they have explicitly said they don't want.
3. The last four cycles of the monitor's `findings/` — to identify what is genuinely new vs continuing.
4. The monitor's `findings/feedback/` log — every 👍 / 👎 the anchor has cast in the relevant window.
5. The most recent **redline** for the anchor's monitor (look under `generated/handoffs/` and the monitor's Change History). What did the anchor object to? What did the operator change in response? Did the change land?
6. `metrics/state-of-the-monitors-YYYY-WNN.md` for the current week, if it exists.
7. `scripts/regulatory_calendar.yml` — the next 14-day window for this monitor's domains.

If any of these inputs is missing, the brief flags the gap explicitly. Do not paper over absence with prose.

## Process

1. **Identify continuity vs change.** For each of the monitor's domains, list the items that continue a thread the anchor is already tracking vs the items that open a new thread. Two columns.
2. **Trace the last redline.** State what the anchor pushed back on last time, what changed in the spec, and one concrete example from this week's findings of how the change shows up. If the change has not yet manifested, say so plainly.
3. **Single decision worth their time.** Not three decisions. One. Phrased as a question with two or three options the operator already understands.
4. **One thing to say before the meeting ends.** A specific commitment, ask, or escalation the operator wants the anchor to lock in. If there is nothing, write "Nothing this week" — do not invent.
5. **Coming up.** Three lines max from `regulatory_calendar.yml` — known windows in the next fourteen days for this monitor's domain.
6. **The one question worth sitting with.** A genuine open question, not a rhetorical one. Phrased to be answerable in one sentence.

## Output format

Save to `generated/handoffs/YYYY-WNN-<anchor-slug>-anchor-handoff.md` with this exact shape:

```markdown
---
anchor: <Anne-Claire Hoyng | …>
monitor: monitor-02-eu-competition
week: 2026-WNN
generated-by: anchor-handoff-brief skill v1.0
generated-at: <ISO-8601>
status: draft-for-operator-review
---

# Pre-review brief — <anchor> — <Monitor name> — Week <NN>

## What changed since last cycle
<two-column or two-paragraph: continuing threads vs new threads. Be specific. Cite the finding ID.>

## Where your last redline landed
<one paragraph: what they pushed back on, what changed, one concrete example. If the change has not yet manifested, say so.>

## The one decision worth your time this week
<question + 2–3 options. Operator's lean noted, but not pre-decided.>

## One thing to lock in before the meeting ends
<specific commitment / ask / escalation, or "Nothing this week".>

## Coming up — next 14 days
- <date — event — why it matters in one line>
- <date — event — why it matters in one line>
- <date — event — why it matters in one line>

## One question worth sitting with
<open question, answerable in a sentence.>
```

## Quality bar

A handoff brief earns its place when:

- The anchor can read it in **under five minutes** and walk into the review prepared.
- Every claim is **traceable** to a finding ID, a Change History row, a feedback entry, or a calendar date. No "in general", no "broadly speaking".
- The one decision is **a real decision**, not a recap. If you cannot find one, the brief says so — and the operator knows the cycle was quiet.
- The brief is **drafted to the anchor's reading style** as documented in their monitor's `profile.md` files. For Anne-Claire: doctrinal precision over rhetorical flourish; opinions in advice, not in tone.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill — contract drafted in parallel with the first concrete handoff (Anne-Claire / M02 / W20). | K. Maleevska |
