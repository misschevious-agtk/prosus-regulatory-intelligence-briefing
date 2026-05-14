---
title: M02 Clippings — intake folder
purpose: How to feed the M02 (Competition) brain with HTML from the Obsidian Web Clipper
status: active
last-updated: 2026-05-14
---

# M02 Clippings

Same shape as M01's intake, tuned for competition-law content. Two paths in, one destination.

## Folder layout

```
clippings/
├── inbox/                    ← you drop here (Web Clipper, manual save)
├── processed/
│   ├── 2026/
│   │   ├── W19/
│   │   │   ├── _raw/
│   │   │   ├── <source>__<title>.md
│   │   │   └── …
│   │   └── W20/…
│   ├── _this-week.md
│   └── _unknown-entities-YYYY-WW.md
└── README.md (this file)
```

## Path A — Obsidian Web Clipper (preferred)

Web Clipper settings:

1. **Save location:** `monitors/monitor-02-eu-competition/clippings/inbox/`
2. **Filename template:** `{{date:YYYY-MM-DD}}_{{slug}}`
3. **Format:** HTML.
4. **Tags:** none required.

Particularly useful Web Clipper triggers for M02:
- EU Commission DG COMP press releases and case pages
- CMA case pages
- CCI orders
- CADE decisions
- SAMR announcements
- MLex, GCR, PaRR, Concurrences (trade press)
- CJEU/General Court judgment pages
- National court antitrust judgments

## Path B — Drop into chat

Same as M01: upload HTML, I route it through the parse-tag-file flow, tell you where it landed.

## What the Sourcing & Connecting agent does on sweep

For each file in `inbox/`:

1. Parse the basics.
2. Detect tier (Tier-A regulator/court page > Tier-B specialist trade press > Tier-C general business press).
3. Tag entities — firms, regulators, case numbers, judges/rapporteurs, named officials.
4. Tag doctrinal area: `#reading-mode/antitrust-cartels`, `/abuse-of-dominance`, `/merger-fdi`, `/digital-markets-sector-state-aid`.
5. Tag jurisdiction.
6. Tag theory of harm if explicit.
7. Tag procedural stage (`#stage/phase-1`, `/phase-2`, `/decision`, `/appeal`, `/commitment`).
8. Tag role (`#role/defendant`, `/applicant`, `/complainant`, `/third-party`) only if the source explicitly states it.
9. Resolve instrument and decision references.
10. File to `processed/<year>/<week>/`.

## Naming convention (after processing)

`<source-slug>__<title-slug>.md`

Examples:
- `ec-europa-eu__commission-opens-phase-ii-into-acme-bookings.md`
- `mlex__cci-suo-motu-fintech-rails-investigation.md`
- `cma__remedies-decision-supermarket-merger-2026.md`

## Particularities of M02 intake

- **Case numbers are first-class.** When a source includes one (e.g. `COMP/M.10987`, `2024-FTC-04567`, `CMA/M/2025/123`), the agent extracts and tags it. This is how clusters survive across the lifetime of a matter.
- **Regulator press releases vs trade press coverage of the same matter.** Both ingest. The cluster stitches them. The ranker prefers the regulator page as the cluster representative.
- **Appeals.** Tag `#stage/appeal`. The cluster for an appeal is *new*, not merged with the underlying decision — though they're linked.
- **Multi-jurisdictional parallel matters.** Each jurisdiction is its own cluster, linked via the shared firm tag.

## Do not

- Don't pre-tag with `#stage/...` or `#toh/...` — the agent decides.
- Don't edit files in `processed/`.
- Don't manually delete from `_raw/`.

## See also
- [[../agents/02-sourcing-connecting|Sourcing & Connecting agent]]
- [[../agents/01-regulations|Regulations agent]]
- [[../../../keyword-conventions|keyword-conventions.md]]
- [[../../../strategy|strategy.md]] — source tiers
