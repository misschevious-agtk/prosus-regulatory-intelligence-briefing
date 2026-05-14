# Findings

Append-only library of material findings produced by Monitor 01, plus the higher-level digests, briefs, indexes, and incidents that surface them. Empty until the agent starts sifting (and an empty run is a valid run — see Operating Rule 2 in `SYSTEM-PROMPT.md`).

---

## Document types and file-naming conventions

Six document types live in this folder. Each has its own naming convention and its own audience (full audience map in `operating-preferences.md`).

### 1. Individual finding (the core unit)
```
YYYY-MM-DD-[domain]-[slug].md
```
- `YYYY-MM-DD` — `date_found` from the finding's frontmatter (not `source_date`).
- `[domain]` — one of `ai-news` · `privacy` · `ip` · `legal-ops`.
- `[slug]` — short, lowercase, hyphenated, no more than 6 words.
- **Schema:** full `output-schema.md`. No claim without a verbatim anchor quote.

**Examples:**
```
2026-05-13-ai-news-edpb-training-data-opinion.md
2026-05-13-privacy-cnil-fines-vendor-x.md
2026-05-14-ip-bartz-anthropic-fairness-hearing.md
2026-05-15-legal-ops-cloc-2026-benchmark.md
```

### 2. Daily push brief
```
BRIEF-YYYY-MM-DD-[domain].md
```
- One per domain per day (AI News, Privacy, IP only — Legal Ops doesn't run daily).
- Pure prose, 3–5 sentences summarising the day's Rank A/B findings with links to the underlying finding files.
- **Audience:** the persona's substantive partner. **Readable in 60 seconds.**
- See `operating-preferences.md` Type 3.

### 3. Weekly index
```
INDEX-YYYY-WW.md
```
- Where `WW` is the ISO week number.
- Structured listing of all findings from that week by rank (A → B → C → D) with one-line summaries.
- **Audience:** Group GC team, AI and ethics working group.

### 4. Monthly digest
```
DIGEST-YYYY-MM.md
```
- First business day of each month. Single document; all four domains combined.
- Prose structured into four sections: regulatory landscape changes by domain · `our_stack` and exposures · cross-domain patterns · what's coming next month.
- Length target: 4–6 pages.
- **Coordinator:** Legal Ops persona consolidates; other three drafts their sections.
- **Audience:** Group GC + OpCo GCs.

### 5. Quarterly board summary
```
BOARD-SUMMARY-YYYY-QQ.md
```
- Where `QQ` is `Q1`/`Q2`/`Q3`/`Q4`.
- Prose only, ~2 pages, no findings-level detail.
- Focus: material risk shifts · material new obligations · material new exposures · function performance vs KPIs.
- **Owner:** Group GC.
- **Audience:** Group ExCo + board risk committee.

### 6. Incident note (same-day push, bypasses normal schema)
```
INCIDENT-YYYY-MM-DD-[slug].md
```
- One per incident.
- Short incident-style note — what happened, who's affected, what we know, what we don't, what the clock is.
- **Structural owner:** Privacy persona (the 72-hour breach clock is the load-bearing case). Other personas may file incidents that route through this channel (e.g. critical vendor breach affecting Toqan or the LCM stack).
- **Audience:** On-call OpCo DPO + Group GC; cross-copies the relevant persona partner.
- **Protocol:** **escalate first, document second.**

---

## What goes here and what doesn't

- ✅ Every material finding produced by any of the four domain personas.
- ✅ Cross-references from a secondary domain (file once in the primary domain; the secondary domain's index references it).
- ✅ Daily briefs, weekly indexes, monthly digests, quarterly board summaries, and incident notes — per the conventions above.
- ❌ Drafts. Drafts live in the agent's working memory until they pass self-critique. Only filed findings land here.
- ❌ Items below the materiality threshold. Empty output is valid output.

---

## Discipline

- **Append-only.** If a finding needs correction, file a new finding that references the original via `secondary_axes` and note the correction in Open questions. Do not edit history.
- **One source per finding.** Corroborating sources go in the body, not as separate findings.
- **No invented URLs, citations, dates, or quotes.** Ever.
- **Incidents bypass the schema; everything else honours it.**
