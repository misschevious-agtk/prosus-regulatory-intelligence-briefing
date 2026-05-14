# Findings — Monitor 02

This folder holds all Monitor 02 outputs. Empty until Block 1, Block 2, and Block 3 sign-off lands from Anne-Claire and the monitor goes live.

## Naming conventions

### Individual findings
```
YYYY-MM-DD-[domain]-[slug].md
```
Where `[domain]` is one of: `antitrust-cartels`, `abuse-of-dominance`, `merger-control-fdi`, `digital-markets-sector-state-aid`. The `[slug]` is short kebab-case (e.g. `dg-comp-mfn-guidance-update`, `cade-ifood-tcc-extension`, `bkarta-19a-designation-pattern`).

### Weekly index
```
INDEX-YYYY-WW.md
```
ISO week number. Aggregates all findings of the week by rank, with one-line summaries and links.

### Push briefs (per domain at each domain's cadence)
```
BRIEF-YYYY-MM-DD-merger-control-fdi.md          # daily
BRIEF-YYYY-MM-DD-antitrust-cartels.md           # Tuesday and Friday
BRIEF-YYYY-MM-DD-abuse-of-dominance.md          # Tuesday and Friday
BRIEF-YYYY-WW-digital-markets-sector-state-aid.md  # weekly Friday afternoon
```

### Monthly digest
```
DIGEST-YYYY-MM.md
```
First business day of the month. Five-section prose per `operating-preferences.md` Type 4.

### Quarterly board summary
```
BOARD-SUMMARY-YYYY-QQ.md
```
Where `QQ` is `Q1`, `Q2`, `Q3`, `Q4`. Two pages, board-facing, drafted by Anne-Claire, owned by Group GC.

### Incident notes (as triggered)
```
INCIDENT-YYYY-MM-DD-[slug].md
```
For dawn-raid notifications, statement-of-objections-grade events, FSR or FDI prohibition orders, or any Delivery Hero divestment commitment alleged-breach signal. Bypasses normal schema.

### Policy-paper findings (unique to Monitor 02)
Same `YYYY-MM-DD-[domain]-[slug].md` pattern as individual findings, with the standard schema. Distinguished by `source_type: academic` in frontmatter and `source_publisher` set to the institution (SSRN, TILEC, Toulouse, CRESSE, CLEEN, Stigler Center, ECLR, JCLE, etc.).

---

## Folder convention at scale

When findings volume exceeds ~200 files in this directory, sub-folder by year:

```
/findings/
  /2026/
    YYYY-MM-DD-...
    INDEX-YYYY-WW.md
    ...
  /2027/
    ...
```

Briefs and digests sub-folder by year-quarter only if volume justifies. Default is flat within `/findings/`.

## Privileged and leniency-sensitive findings

Per `operating-preferences.md` Section 5 (Confidentiality framing):

- **Privileged findings** carry a header line `Privileged and confidential — prepared for legal advice` and are flagged in frontmatter (`source_type` may still be standard but the file itself has restricted distribution).
- **Leniency-sensitive findings** are flagged `LENIENCY-SENSITIVE` in frontmatter and route via incident channel to Anne-Claire only. Cross-references in indexes are redacted or omitted.

Both categories sit in this `/findings/` directory alongside standard findings but with access controlled at the distribution layer rather than at the filesystem layer.

## Cross-monitor cross-references

Per `ranking-criteria.md` Rule 21, cross-references to Monitor 01 findings appear in this monitor's weekly index entries. Where the cross-referenced item is privileged or leniency-sensitive, the cross-reference is redacted (title omitted, access controlled) per Layer 4 of the confidentiality framing.

## Retention

Findings, indexes, briefs, and digests are retained on the same schedule as Prosus's broader legal-function intelligence outputs. Competition matters can produce regulator information requests years after the underlying event; the audit trail in this folder is part of the documentary record.
