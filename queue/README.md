---
title: queue — the operator's inbox to the network
description: Drop a request file here; the network processes it and deposits the output in generated/.
version: 1.0
status: active
last-updated: 2026-05-14
---

# Queue

`queue/` is the network's intake. It is the only place outside the monitor folders where the operator initiates work for an agent to pick up. Without the queue, every research ask, every anchor brief, every redline integration has to be initiated as an ad-hoc conversation — which means it cannot run unattended and cannot be audited later.

The rule is simple: **if a task has a known shape, it has a queue template**. If it does not, the task either belongs inside a monitor's spec or it should not be asked of the network at all.

## How the queue works

1. Operator drops a file into `queue/` named per the convention below.
2. The relevant skill in `system/skills/` picks the file up — either by a scheduled scan or because the operator invoked the skill.
3. The skill processes the file and writes its output to `generated/<subfolder>/`.
4. The processed queue file is **archived** to `queue/_processed/YYYY-MM-DD/<original-name>` rather than deleted, so the queue history stays auditable.

## Filename conventions

The first token of the filename tells the network which skill claims it.

| Filename pattern | Skill | Output location |
|---|---|---|
| `RESEARCH-<topic-slug>.md` | `deep-research` | `generated/research/YYYY-MM-DD-<topic-slug>.md` |
| `ANCHOR-BRIEF-<anchor-slug>-W<NN>.md` | `anchor-handoff-brief` | `generated/handoffs/YYYY-WNN-<anchor-slug>-anchor-handoff.md` |
| `REDLINE-<monitor>-block<N>.md` | `redline-integration` | Spec edits + Change History + `generated/handoffs/YYYY-MM-DD-<monitor>-redline-summary.md` |
| `SYNTHESIS-W<NN>.md` | `weekly-synthesis` | `generated/syntheses/YYYY-WNN-network-synthesis.md` |
| `PERFORMANCE-<monitor>-<period>.md` | `monitor-performance-review` | `generated/reports/YYYY-MM-<monitor>-performance.md` |

Unrecognised filenames are left untouched and listed in the next morning brief under "unprocessed queue items".

## What goes into a queue file

Each template starts with a frontmatter block plus a body. Frontmatter fields are skill-specific (see each skill's `system/skills/<skill>.md`). Body is a markdown free-form section the operator uses to frame the request.

Use `queue/_templates/<skill>.md` as a starting point — the templates are loaded with the right frontmatter for each skill and have prompt notes on what to include.

## Rules for the queue

- **One ask per file.** If a queue file contains two unrelated asks, the skill will surface the conflict rather than guess.
- **Deadline in frontmatter or in the body.** If neither is present, the skill assumes 48 hours.
- **Never put confidential matter codes in queue filenames.** The filenames are committed to git; the body is what gets confidentiality-filtered.
- **Queue is not a chat log.** If the operator's framing changes between dropping the file and the skill running, the operator updates the file or drops a new one — not an addendum.

## Folder structure

```
queue/
├── README.md
├── _templates/
│   ├── RESEARCH.md
│   ├── ANCHOR-BRIEF.md
│   ├── REDLINE.md
│   ├── SYNTHESIS.md
│   └── PERFORMANCE.md
└── _processed/
    └── YYYY-MM-DD/
        └── <archived queue files>
```

## Change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial queue. Five templates introduced. | K. Maleevska |
