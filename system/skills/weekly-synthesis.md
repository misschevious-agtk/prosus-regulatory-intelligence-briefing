---
skill: weekly-synthesis
description: Synthesise the week across all monitors into emerging thesis, contradictions, knowledge gaps, and one action.
trigger: Friday end-of-week scheduled run OR queue file SYNTHESIS-W<NN>.md OR operator request "run weekly synthesis for week <NN>".
output: generated/syntheses/YYYY-WNN-network-synthesis.md
version: 1.0
last-updated: 2026-05-14
---

# Skill — Weekly synthesis

The weekly synthesis is the operator's compounding artefact. The daily brief surfaces connections in 24-hour windows; the synthesis is where six months of synthesis files become a record of how Prosus's regulatory exposure thinking has evolved. Skipping this skill is the single fastest way to turn the network into a daily-digest pipeline instead of a thinking partner.

## Trigger

- Friday 17:00 CET scheduled run.
- Queue file `queue/SYNTHESIS-W<NN>.md` (optionally with a "focus" hint from the operator).
- Explicit operator request.

## Context required

1. `CLAUDE.md` — current weekly focus.
2. The last seven days of `findings/` across **every active monitor**.
3. The last seven days of `daily/` operator notes.
4. The most recent `generated/syntheses/` file. The synthesis reads its own history to identify drift in the operator's own thinking.
5. The relevant `metrics/state-of-the-monitors-YYYY-WNN.md` snapshot if it exists.

## Process

Four passes. In this order, no shortcuts.

1. **Emerging thesis.** What is the operator building toward, across monitors, without having stated it explicitly? Look for repeated highlighting, repeated 👍s on similar framings, repeated escalations on similar trigger types. Name the thesis in one sentence. If you cannot, say "No thesis emerged this week" — empty weeks are real and worth recording.
2. **Contradictions.** What did the operator surface this week that contradicts something they surfaced earlier? The contradiction may be inside one monitor (a new ruling reverses an older one) or across monitors (M01 IP persona's framing of training-data scrapes disagrees with M02 abuse-of-dominance framing of the same item). Show both sides from the vault. Do not adjudicate.
3. **Knowledge gaps.** Given what the operator is reading and not reading, what perspective is missing? Be specific: which jurisdiction, which doctrine, which OpCo's exposure. If the gap is a known one already on the roadmap, say so.
4. **One action.** Given everything above, what is the single highest-leverage thing the operator could do or think about next week? One. Phrased as either a verb-first action or a question to sit with.

## Output format

Save to `generated/syntheses/YYYY-WNN-network-synthesis.md`:

```markdown
---
week: 2026-WNN
generated-by: weekly-synthesis skill v1.0
generated-at: <ISO-8601>
monitors-covered: [monitor-01, monitor-02-eu-competition]
status: draft-for-operator-review
---

# Weekly network synthesis — Week <NN>

## Emerging thesis
<one sentence, or "No thesis emerged this week — quiet across <list>.">

## Contradictions
<one to three, each with both sides traced to specific findings IDs.>

## Knowledge gaps
<what perspective is missing. Specific jurisdiction / doctrine / OpCo. Flag whether already on the roadmap.>

## One action for next week
<verb-first action or question to sit with. One.>

## What the synthesis itself learned this week
<one or two lines on what shifted since last week's synthesis, if anything. Used by next week's run to detect drift.>
```

## Quality bar

- The synthesis is **not a digest**. If it reads like a summary of what was already in the daily briefings, it failed. The point is the thinking.
- Every claim is traceable. If you assert a contradiction, link the two findings.
- "No thesis emerged this week" is a valid output. Hollow theses are worse than honest absences.
- The synthesis **does not predict the future**. It records what the vault is showing about the operator's own thinking.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. | K. Maleevska |
