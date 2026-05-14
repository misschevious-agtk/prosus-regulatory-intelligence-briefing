# Keyword Conventions — Legal Intelligence Briefing

**Version:** v1.0 — 2026-05-13.

**Scope:** Conventions for the `keywords.md` files that sit in each domain folder of each monitor. Applies to all monitors current and future. New monitors clone this convention; deviations require a Change Log entry in the deviating monitor's `keywords.md` file and a note here.

> **Why this file exists.** The eight `keywords.md` files across Monitor 01 and Monitor 02 follow the same structural pattern by design — same four tiers, same multilingual handling, same `[broad]` markers, same change-log discipline. This file documents that pattern so future monitor builders inherit it cleanly rather than reverse-engineering from existing files.

---

## 1. File location — Pattern A

One `keywords.md` per **domain folder**, not per monitor:

```
monitors/monitor-XX/<domain>/keywords.md
```

Examples:

- `monitors/monitor-01/ai-news/keywords.md`
- `monitors/monitor-01/privacy-data-protection/keywords.md`
- `monitors/monitor-02-eu-competition/antitrust-cartels/keywords.md`
- `monitors/monitor-02-eu-competition/abuse-of-dominance/keywords.md`

**Reasoning:** the retrieval pipeline runs separately per domain (each persona has different sources, different cadences per `operating-preferences.md`), and the keyword sets are calibrated to that persona. A top-level `scraper-keywords.md` with sections inside was tried briefly and rejected because it created merge-conflict pressure when two personas' keyword updates collided.

## 2. Four-tier structure

Every `keywords.md` follows the same four tiers in the same order. Tier headings are mandatory; sub-section headings inside a tier are optional and used freely for navigation.

### Tier 1 — Named entities

Authorities, courts, individuals, vendors, operating companies, comparator entities, named cases. The unifying property: **mention alone signals relevance**. Tier 1 terms are typically high-precision and low-noise.

Sub-section examples that work:

- "Competition authorities and courts"
- "EU AI institutions"
- "Anthropic stack" / "OpenAI stack" / "AWS stack" — per-vendor blocks for stack-relevance domains
- "Named individuals"
- "Landmark cases and ongoing matters (auto-relevance)"
- "Trade associations and fora" (with explicit placeholder when operator-supplied)

### Tier 2 — Doctrinal and substantive terms

The specific legal-technical phrases that mark a finding as in-scope. Tier 2 carries the bulk of multilingual coverage — doctrinal terms need their equivalents in each language the persona reads.

Sub-section examples:

- "Article 101 / Sherman §1 core"
- "MFN / parity-clause doctrine"
- "Cross-border transfers (multilingual)"
- "AI training and training data"

### Tier 3 — Trigger-type terms

Words that flag a development is **action-bearing rather than commentary** — "judgment", "decision", "fine", "sanction", "consultation opened", "dawn raid". Tier 3 narrows Tier 1 and Tier 2 from "this is in scope" to "something happened".

Sub-section examples:

- "Procedural"
- "Court rulings"
- "Vendor releases (`our_stack` triggers)"
- "Speeches and policy signals"

### Tier 4 — Exclusion terms

Phrases that flag items as out of scope **even when matching Tier 1–3**. Tier 4 does not auto-discard; it informs the persona's drop rule per the interrogation checklist. Useful to silence predictable false positives.

Tier 4 is a single section (no sub-sections needed) and typically short — a paragraph of comma-separated phrases.

## 3. Inline markers

Used inside any tier without preamble or legend (the convention is documented here once and assumed across all files).

### `[broad]` — noisy term flag

Marks terms with high false-positive rate that need combination with another keyword to be useful. Example: `pricing algorithm [broad] · dynamic pricing [broad]` — these match too many sales-and-marketing articles to fire on their own.

Operating rule: the retrieval pipeline should require `[broad]` terms to co-occur with at least one Tier 2 or Tier 3 term in the same document.

### Language markers — `[FR]`, `[DE]`, `[IT]`, `[NL]`, `[ES]`, `[PT]`, `[PT-BR]`, `[PL]`, `[RO]`, `[TR]`, `[HU]`

Marks non-English entries. Multilingual variants are **grouped with their English term**, not split into separate sections, because retrieval typically OR-combines variants of the same concept.

Example: `consent · consentement [FR] · Einwilligung [DE] · consenso [IT] · consentimiento [ES] · consentimento [PT] · toestemming [NL]`

When a term has no clean English form (e.g. CJK characters, agency acronyms), it appears with just the language marker and translation in parentheses: `Garante per la protezione dei dati personali · GPDP [IT]`.

## 4. Multilingual policy — Choice 2 (calibrated per persona)

Each persona's multilingual baseline is calibrated to **how that persona actually reads**, not to a uniform standard. Multilingual coverage is asymmetric across the eight files by design.

### Per-domain baselines

| Domain (Monitor) | Languages baseline | Reasoning |
|---|---|---|
| AI News (M01) | EN (primary) + FR, DE, NL targeted | Most regulators publish English; FR/DE/NL for AISI/AI Office and DPA-AI angle |
| Privacy & Data Protection (M01) | EN + NL + FR + DE + IT + ES + PT + Mandarin | DPA decisions publish primarily in national language; most multilingual of the eight |
| Intellectual Property (M01) | EN + FR, DE, IT, PT, Mandarin | Copyright/patent/trademark traditions vary; CNIPA Mandarin matters |
| Legal Ops (M01) | EN (dominant) + NL, FR for bar associations only | Function vocabulary is canonically English |
| Antitrust & Cartels (M02) | EN + NL + FR + DE + IT (Anne-Claire baseline); PT, ES, Mandarin shortlisted | Anne-Claire reads original-language CJEU and NCA decisions |
| Abuse of Dominance (M02) | Same as Antitrust | Persona is unitary across the four M02 reading-modes |
| Merger Control & FDI (M02) | Same as Antitrust | Plus US procedural English for HSR-tracking |
| Digital Markets, Sector Regulation & State Aid (M02) | Same as Antitrust | Brussels-policy lens; some Mandarin for CAC × competition |

### Promotion from shortlisted to baseline

A shortlisted language gets promoted to baseline if either (a) the operator declares the persona regularly reads it, or (b) findings in that language consistently come from external counsel rather than the monitor's own retrieval — signal that the monitor's coverage has a gap. Promotion is logged in the file's change log.

## 5. Cross-monitor overlap handling

Per `monitors/monitor-XX/ranking-criteria.md` Rule 21, findings on the boundary between two monitors are filed in the **primary monitor** (whichever monitor's substantive doctrine most directly answers the question "what action does this require?") with a cross-reference note in the secondary monitor's weekly index.

The keyword files do not duplicate Rule 21 — they participate in it. Two design choices flow from this:

1. **Overlap terms appear in both files where natural.** E.g. "Meta Platforms v Bundeskartellamt" appears in both M01 Privacy (Article 22 GDPR / exploitative data combination angle) and M02 Abuse of Dominance (Article 102 exploitative-T&Cs angle). The retrieval pipeline fires both monitors; the rank-rule layer routes.

2. **Tier 4 exclusion phrasing names the other monitor.** E.g. M01 Privacy Tier 4 includes "pure AI capability without privacy implication (Monitor 01 AI News)" — the parenthetical handles the routing. M02 Antitrust Tier 4 includes "pure trade-secret issue (Monitor 01 IP)" — same pattern.

The canonical cross-monitor overlap clusters as of v1.0 / v1.1:

- **AI Act × GDPR × Article 22 ADM** — M01 AI News ↔ M01 Privacy
- **Training-data copyright × AI vendor practice** — M01 IP ↔ M01 AI News
- **DMA × Article 102** — M02 Digital Markets ↔ M02 Abuse of Dominance
- **DMA × DSA × privacy (Meta consent or pay, data combination)** — M02 Digital Markets ↔ M01 Privacy
- **Platform Work Directive × algorithmic management** — M02 Digital Markets ↔ M01 AI News
- **CMA AI Foundation Models work** — M02 Digital Markets ↔ M01 AI News

## 6. Change-log discipline

Every `keywords.md` ends with a Change Log table. Entries are append-only.

### Adding keywords

- Inline change in the file plus a Change Log row.
- No additional sign-off needed for Tier 2, Tier 3, Tier 4 additions.
- Tier 1 named-entity additions: no sign-off needed if the entity is publicly verifiable; sign-off needed for internal-only entities (panel firms, named individuals not in public record).

### Removing keywords

- Inline change in the file plus a Change Log row.
- Sign-off needed for any term in the "global / cross-domain" or canonical-precedent sub-sections.
- Sign-off needed for any case-pattern regex (M02 only).
- Tier 4 additions from the suppression discipline (three or more 👎 inside 30 days) are tracked but don't require sign-off — they're operationally-driven.

### Versioning

- v1.0 = initial draft per Block 2 / Block 3 defaults.
- v1.1 = first expansion pass (typically operator-approved breadth expansion before go-live).
- v1.x continues until Anne-Claire/Tara/Group GC redline triggers a v2.0 restructure.

## 7. Quarterly review cadence

Per `monitors/monitor-XX/operating-preferences.md`, every `keywords.md` is reviewed quarterly alongside the source baseline review. The review checks:

1. **Pattern-driven additions** — sources that produced findings without matching keywords get their matched phrases added.
2. **Pattern-driven removals** — keywords that produced repeated low-quality matches (three or more 👎 inside 30 days) get retiered to Tier 4 suppression patterns.
3. **Live-case refresh** — named cases in Tier 1 that have settled, been dismissed, or generated significant procedural progeny get updated (e.g. NYT v OpenAI as the case progresses).
4. **Multilingual extension** — shortlisted languages reviewed for promotion to baseline.
5. **Cross-monitor overlap audit** — newly-emerged overlap clusters (e.g. a new doctrinal boundary opens) get logged here in section 5.

## 8. Operating principles (single line each, for fast reference)

- **Keywords cast the net; the interrogation checklist filters the catch.**
- **False positives are cheaper than false negatives at the scraper layer.**
- **Multilingual variants OR-combine; same-concept terms cluster.**
- **`[broad]` markers require co-occurrence with a Tier 2 or Tier 3 term.**
- **Tier 4 informs the persona's drop rule; it does not auto-discard.**
- **Cross-monitor overlap is handled at the rank-rule layer (Rule 21), not by keyword exclusion.**
- **Append-only change log; v1.x versioning; quarterly review.**

---

## Change log

| Date       | Change | Author |
|------------|--------|--------|
| 2026-05-13 | Initial v1.0. Captures the four-tier structure, inline-marker conventions, multilingual policy (Choice 2 calibrated per persona), cross-monitor overlap handling, change-log discipline, quarterly review cadence. Distilled from the eight `keywords.md` files in Monitor 01 and Monitor 02 after Anne-Claire-approved v1.1 expansion pass. | Claude (Anne-Claire-approved) |
