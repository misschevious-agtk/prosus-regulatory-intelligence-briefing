---
skill: deep-research
description: Operator-queued deep dive on a specific topic that the regular monitor cadence cannot do justice to.
trigger: A queue file named RESEARCH-<topic-slug>.md OR explicit operator request.
output: generated/research/YYYY-MM-DD-<topic-slug>.md
version: 1.0
last-updated: 2026-05-14
---

# Skill — Deep research

The regular monitor cadence is breadth-first: every working day, across every domain, a small number of high-signal items. The deep research skill is depth-first: one topic, treated with the time and synthesis the briefing format does not allow. Used for things like the CMA mobile-ecosystems case before a Hoyng meeting, the Tencent NAV-disclosure regulatory exposure ahead of a board ask, or the DPDP enforcement trajectory before a Swiggy India review.

## Trigger

- A file at `queue/RESEARCH-<topic-slug>.md` containing the operator's framing of what they want to know.
- Explicit operator request, e.g. "deep-research the DMA gatekeeper review window for portfolio companies".

The queue file should include: the question, the consumer (operator, named anchor, or specific Prosus stakeholder), the deadline, and the depth (one-pager vs. multi-page).

## Context required

1. `CLAUDE.md` — current weekly focus.
2. The queue file's framing — read it literally; do not interpret beyond it without flagging.
3. The relevant monitor's `SYSTEM-PROMPT.md`, `our_markets.md`, `portfolio-map.md`, `sectoral-overlays.md`.
4. Existing findings in `findings/` that touch this topic — research must build on what the vault already knows, not duplicate it.
5. `metrics/` for any prior synthesis touching this topic.
6. `strategy.md` source-tier model and locked filters — they apply to research as much as to briefings.

## Process

Five passes.

1. **The core question.** State it in one sentence. If the operator's framing was loose, sharpen and confirm.
2. **What the vault already knows.** Summarise existing findings and prior synthesis on this topic, with finding IDs. Identify the gap between what is known and what is asked.
3. **The non-obvious angle.** What does most coverage of this topic miss? This is what makes research worth doing rather than reading a Bloomberg piece.
4. **Three concrete examples or data points** with citations. Tier-1 sources preferred; Tier-2 acceptable; Tier-3 only for framing.
5. **What it means for Prosus.** Per-OpCo exposure where applicable. Per-jurisdiction action triggers. Honest about uncertainty.

## Output format

Save to `generated/research/YYYY-MM-DD-<topic-slug>.md`:

```markdown
---
topic: <topic-slug>
question: <one sentence>
consumer: <operator | anchor name | stakeholder>
queued-at: <ISO-8601 from queue file>
delivered-at: <ISO-8601>
depth: <one-pager | full>
generated-by: deep-research skill v1.0
status: draft-for-operator-review
---

# Deep research — <topic> — <date>

## Core question
<one sentence.>

## What the vault already knows
<prior findings + synthesis IDs, with one-line each.>

## The non-obvious angle
<what most coverage misses.>

## Supporting evidence
1. <source citation + relevance.>
2. <source citation + relevance.>
3. <source citation + relevance.>

## What this means for Prosus
<per-OpCo / per-jurisdiction. Honest about uncertainty.>

## Recommended next step
<one — a finding to promote, a redline to draft, a brief to prepare, or "no action — surfaced for awareness".>
```

## Quality bar

- The core question must be **answerable in one sentence**. If it cannot be, the research is too broad and needs to be split.
- "The vault already knows X" entries are **mandatory**. Research that duplicates a finding from three weeks ago is research that failed.
- The non-obvious angle must be **genuinely non-obvious**. If a Bloomberg Law subscriber would have flagged it from the headline, dig deeper.
- "Per-OpCo exposure" applies the **Prosus Relevance Filter** at the monitor's chosen strictness. Do not loosen for the sake of a longer "what this means" section.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. | K. Maleevska |
