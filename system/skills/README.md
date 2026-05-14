---
title: system/skills — codified skills the network performs
description: One file per skill. Read the skill file before performing the skill. Output goes to generated/.
version: 1.0
status: active
last-updated: 2026-05-14
---

# Skills library

Each file in this folder is a **codified skill** — a Claude prompt with explicit contract: trigger, context required, process, output format, output location, and quality bar. Codified skills are how the network turns recurring operator work into something an agent can run unattended.

A skill file is not a cadence. The pair is:

- `cadences/<skill>.md` — what the human is expected to do on what schedule, who is involved, what success looks like operationally.
- `system/skills/<skill>.md` — the exact prompt and contract Claude reads when invoked to perform the skill.

When in doubt: cadences are read by people, skills are read by agents.

| Skill | When | Reads | Writes |
|------|------|-------|--------|
| `anchor-handoff-brief.md` | Before an anchor reviews their monitor's output | Anchor's monitor SYSTEM-PROMPT, last 4 cycles of findings + reasoning, last redline if any, current week's calendar | `generated/handoffs/YYYY-WNN-<anchor>-anchor-handoff.md` |
| `weekly-synthesis.md` | Friday end-of-week | All monitors' last 7 days of findings, daily/ notes, metrics/ snapshots | `generated/syntheses/YYYY-WNN-network-synthesis.md` |
| `operator-morning-brief.md` | Monday → Friday, before work | Last 24h of findings across monitors, escalations, queue/, calendar | `generated/briefings/YYYY-MM-DD-morning.md` |
| `redline-integration.md` | When an anchor returns a redline on a Block 1–3 spec | Original Block file, anchor's redline notes, affected downstream personas / sources | Diff applied to Block file + Change History row + summary in `generated/handoffs/` |
| `monitor-performance-review.md` | End of each calibration cycle (Day 14) and quarterly thereafter | Monitor's `findings/feedback/` log, brief volume vs cap, escalation count, null-briefing count | `generated/reports/YYYY-MM-monitor-XX-performance.md` |
| `deep-research.md` | Triggered by a `queue/RESEARCH-*.md` file | The queue file, existing notes on the topic in `findings/` and `metrics/`, the relevant monitor's SYSTEM-PROMPT | `generated/research/YYYY-MM-DD-<topic>.md` |
| `daily-rollup.md` | End of each working day or first thing the next morning | The day's `daily/YYYY-MM-DD.md` operator log | Conventions parsed → routed to Change History, feedback log, queue, or persona reconciliation flag |

Each skill file follows the same five-section shape: **Trigger**, **Context required**, **Process**, **Output format**, **Quality bar**. If you are adding a new skill, mirror that shape exactly so an agent invoking the skill knows what to read and what success looks like without re-reading this README first.

## Quality bar for the skills themselves

A skill earns its place when:

1. It runs **without operator hand-holding** — the contract is complete enough that an agent reading only the skill file can perform it.
2. It writes to **`generated/`** rather than directly into a monitor's `findings/`. Promotion to `findings/` is always a human gate.
3. Its output **respects the same locked filters** the rest of the network uses (`strategy.md` section "System-wide locked filters").
4. Its Change History (at the bottom of the skill file) is current.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skills library — seven skills introduced as part of the Obsidian-pattern integration. Anchor-handoff-brief, weekly-synthesis, operator-morning-brief, redline-integration, monitor-performance-review, deep-research, daily-rollup. | K. Maleevska |
