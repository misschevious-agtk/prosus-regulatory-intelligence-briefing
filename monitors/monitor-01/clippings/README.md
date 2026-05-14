---
title: M01 Clippings — intake folder
purpose: How to feed the M01 brain with HTML from the Obsidian Web Clipper
status: active
last-updated: 2026-05-14
---

# M01 Clippings

The intake folder for everything you save via the Obsidian Web Clipper (or drop manually). Two paths in, one destination.

## Folder layout

```
clippings/
├── inbox/                    ← you drop here (Web Clipper, manual save)
├── processed/                ← Sourcing & Connecting writes here
│   ├── 2026/
│   │   ├── W19/
│   │   │   ├── _raw/         ← original HTML, audit only
│   │   │   ├── <source>__<title>.md
│   │   │   └── …
│   │   └── W20/…
│   ├── _this-week.md         ← hand-off list to Static Workflow
│   └── _unknown-entities-YYYY-WW.md
└── README.md (this file)
```

## Path A — Obsidian Web Clipper (preferred for volume)

In the Web Clipper settings:

1. **Save location:** point it at `monitors/monitor-01/clippings/inbox/` inside your Prosus vault.
2. **Filename template:** `{{date:YYYY-MM-DD}}_{{slug}}` (the agent normalises this anyway, but a clean filename helps).
3. **Format:** HTML (not Markdown). The Sourcing & Connecting agent parses HTML → Markdown deliberately, with frontmatter and tagging; if you ship pre-converted Markdown the agent has to second-guess it.
4. **Tags:** none required at clip time. The agent tags. (You're welcome to add a tag — it'll be preserved — but don't feel obliged.)

That's it. Save pages as you read them. The cell sweeps the inbox on its next run.

## Path B — Drop into chat

If you don't want to save into the folder (one-off, on mobile, etc.):

- Upload the HTML to Claude in chat.
- I'll route it through the same parse-tag-file flow and tell you what landed where.

Same destination, same conventions.

## What the Sourcing & Connecting agent does on sweep

For each file in `inbox/`:

1. Parse title / byline / publication / date / body / URL.
2. Detect source tier (Tier-A regulator/major outlet, Tier-B trade press, Tier-C industry blogs).
3. Tag entities from the gazetteer.
4. Tag reading-mode: `#reading-mode/ai-news`, `/privacy-data-protection`, `/intellectual-property`, `/legal-ops` (multi-tag allowed).
5. Tag jurisdiction.
6. Resolve instrument references → `[[wikilinks]]`. New instruments get flagged to the Regulations agent.
7. Write the cleaned Markdown to `processed/<year>/<week>/<source>__<title>.md`.
8. Move the original HTML to `processed/<year>/<week>/_raw/`.
9. Append the entry to `processed/_this-week.md`.

You can verify a clipping was processed by looking for the matching file in `processed/<year>/<week>/`.

## Naming convention (after processing)

`<source-slug>__<title-slug>.md`

- `source-slug` is the publication or feed name (`ec-europa-eu`, `reuters`, `iapp`, `mlex`, `politico-eu`).
- `title-slug` is a 60-char-max kebab-case version of the headline.
- Double underscore separates them.

Examples:
- `ec-europa-eu__ai-act-art-50-guidance-published.md`
- `iapp__dpdp-section-16-cross-border-rules-finalised.md`

## When something goes wrong

- **The Web Clipper saved Markdown instead of HTML:** The agent still ingests but flags `#format/clipper-md` so the Orchestrator can spot pattern drift.
- **A clipping has no detectable source:** Tagged `#source/unknown` and surfaced in the weekly unknown-entities file.
- **An instrument is mentioned that doesn't yet have a note:** Flagged to the Regulations agent for creation.
- **An entity is mentioned that's not in the gazetteer:** Tagged `#entity/candidate` and surfaced in `_unknown-entities-YYYY-WW.md`. Three sightings in 30 days → promotion.

## Do not

- Don't pre-tag clippings with `#reading-mode/...` — the agent decides, and conflicting tags create cleanup work.
- Don't edit files in `processed/`. Those are agent output. If something needs fixing, raise it to the Orchestrator and the next reflection cycle will adjust.
- Don't manually delete from `_raw/`. That's the audit trail.

## See also
- [[../agents/02-sourcing-connecting|Sourcing & Connecting agent]]
- [[../agents/01-regulations|Regulations agent]]
- [[../../../keyword-conventions|keyword-conventions.md]]
- [[../../../strategy|strategy.md]] — source tiers
