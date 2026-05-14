# Ranking Criteria — Monitor 02 (Tier-2 Fixed Rank Rules)

This is the **set-in-stone** rank table for Monitor 02. It operates only on enumerated fields from the structured finding frontmatter defined in `/output-schema.md`. **It does not read prose.** If a finding cannot be ranked by these rules, mark `recommended_action_class: escalate` for human triage rather than inventing an interpretation.

## Operating principles

1. **Mechanical application.** Apply these rules without softening or hardening based on tone, narrative, or recency bias.
2. **No prose re-reading at rank time.** Tier-2 must never re-read the source to break a tie. If it would need to, the schema is missing a field — add the field rather than letting tier-2 do prose interpretation.
3. **Lower-rank default on ties or doubt.** When two ranks could plausibly apply, take the lower one. Tier-2's value is consistency, not coverage.
4. **`our_markets` and `our_practices` are defined in the operator answers to Block 1** (currently in redline). Until Block 1 is signed off, the rank rules below cannot be operated.
5. **Domain-specific overrides take precedence over the baseline rank tables.** Rules 9–21 below override the Rank A/B/C/D baseline when triggered — they always promote, never demote.

---

## Baseline rank tables (Rules 1–8 implicit via the table structure)

### Rank A — Immediate human review (≤48 hours)

Any of the following:

- `trigger_type ∈ [final_decision, court_ruling]` AND `severity ≥ 4` AND `jurisdiction ∈ our_markets`
- `trigger_type = dawn_raid_pattern` AND sector or practice matches ours
- `trigger_type = statement_of_objections` AND target operates in our market or sector
- `trigger_type = designation` (DMA, FSR, FDI sector designation, German GWB §19a, UK SMS, or analogous) AND we or a key counterparty are within scope
- `trigger_type = threshold_change` AND `jurisdiction ∈ our_markets` (could affect deal filings)
- `recommended_action_class = escalate` (any reason)

### Rank B — Weekly review

Any of the following (and not already Rank A):

- `severity = 3` across any trigger type
- `trigger_type = guidance_published` AND `jurisdiction ∈ our_markets`
- `trigger_type ∈ [settlement, interim_decision]` AND adjacent sector
- `trigger_type = remedy_precedent` AND practice or deal type matches ours
- `trigger_type = sector_inquiry_opened` AND our sector or adjacent
- `confidence = high` AND `primary_axis ∈ [enforcement-risk, transaction-risk, compliance]`

### Rank C — Monthly digest

Any of the following (and not already Rank A or B):

- `severity ≤ 2` AND `confidence ≥ medium`
- `trigger_type ∈ [market_move, narrative_shift, ag_opinion]`
- `primary_axis ∈ [strategic-opportunity, reputational]` (unless `severity ≥ 4`)
- `trigger_type = sector_inquiry_concluded` in non-adjacent sectors (precedent value only)

### Rank D — Archive only, no review surface

Any of the following:

- `confidence = low` AND `severity ≤ 2`
- `source_type ∈ [marketing, vendor-announcement]` AND no corroboration
- Items not affecting any practice, deal, or obligation listed in the relevant `needs.md`

### Tie-breaking

Resolved in order:

1. `severity` (higher = higher rank)
2. `deadline_if_any` (sooner = higher)
3. `date_found` (newer = higher)

If two findings remain tied after all three, escalate both — do not pick one arbitrarily.

---

## Domain-specific overrides (Block 3 additions, Rules 9–21)

Eleven domain-specific rules plus one cross-monitor rule. Each overrides the baseline tables when triggered, **always promoting, never demoting**. Rules apply in addition to baseline Rule A/B/C/D logic; a finding matching both Rule 17 and a baseline Rank B condition is filed at Rank A.

### Antitrust & Cartels — Rules 9 through 11

**Rule 9 — Dawn-raid pattern auto-rank.** Any dawn raid in a sector where Prosus has operating-company exposure is **Rank A regardless of severity** and routes via the same-day incident channel. Sectoral matches: food delivery, online classifieds, OTA, online retail/marketplace, payments, e-pharmacy, digital advertising. Coordinated cross-NCA dawn raids in any sector are Rank A because the coordination signal alone justifies attention.

**Rule 10 — MFN/parity doctrine auto-rank.** Any binding instrument, final court ruling, or settlement in a Tier A jurisdiction that materially shifts MFN or platform-parity doctrine is **Rank A regardless of severity**. Despegar supplier contracts, food-delivery price-parity arrangements, and marketplace-pricing features all sit on this doctrinal line; the doctrine is jurisdictionally fragmented in a way that makes every Tier A decision portable. (Resolves Block 3 pending question 8 — MFN/parity depth elevation, set as auto-rank rather than one-tier-upgrade.)

**Rule 11 — iFood/CADE TCC monitoring trigger.** Any CADE communication, monitoring report, modification proposal, alleged-breach signal, or competitor-complaint relating to the iFood TCC is **Rank A regardless of severity**. Live ongoing commitment; cannot be downgraded by routine. (Resolves Block 3 pending question 4 — iFood TCC residual obligation monitoring.)

### Abuse of Dominance — Rules 12 through 14

**Rule 12 — Self-preferencing and recommender-system-as-abuse auto-rank.** Any CJEU, General Court, or Tier A NCA ruling, agency formal guidance, or statement of objections that materially shifts self-preferencing doctrine, recommender-system-as-abuse doctrine, or marketplace own-brand prioritisation doctrine is **Rank A regardless of severity**. The LCM, Ailo, OLX Magic, and eMAG own-brand practices all sit on this line; the doctrine is being made in real time post-Google Shopping and Google Ad Tech.

**Rule 13 — Tencent SAMR competition exposure auto-upgrade.** Any SAMR competition wing enforcement action, court ruling, or formal guidance that names Tencent or materially affects Tencent's competition compliance posture is **Rank A regardless of severity**. Mirrors the Monitor 01 Tencent-attribution rule for the competition domain specifically. (Resolves Block 3 pending question 5 — Tencent attribution rule, set as direct Prosus-equivalent exposure for competition action.)

**Rule 14 — Ecosystem theory auto-upgrade.** Any agency development that advances ecosystem-theory-of-harm doctrine in a way that could apply to a multi-product portfolio like Prosus is **Rank A regardless of severity**. Includes academic working papers from the trusted-primary set when an agency speech, working paper, or guidance has cited or could plausibly cite within 12 months. (Partial resolution of Block 3 pending question 2 — academic-as-leading-indicator. Default posture: Rank B until cited *except* for ecosystem theory where Rank A applies pre-citation given Prosus's specific exposure.)

### Merger Control & FDI — Rules 15 through 17

**Rule 15 — Delivery Hero divestment monitoring trigger.** Any DG COMP communication, trustee report, divestment timeline development, modification proposal, or alleged-breach signal relating to the Just Eat / Delivery Hero divestment commitment is **Rank A regardless of severity**. Live ongoing remedy compliance; cannot be downgraded by routine. (Resolves Block 3 pending question 3 — Delivery Hero divestment commitment monitoring.)

**Rule 16 — Below-threshold call-in auto-rank.** Any Article 22 EUMR referral request, CMA discretionary call-in, BKartA §39a notification, AGCM call-in, or CADE adverse-AC notification that could plausibly affect a Prosus transaction (live, recently closed, or signalled) is **Rank A regardless of severity**. Threshold protection is gone in digital-markets concentration contexts; this rule treats below-threshold call-in as deal-relevant intelligence. (Resolves Block 3 pending question 7 — below-threshold call-in elevation.)

**Rule 17 — Comparable-deal precedent in Prosus sectors.** Any merger clearance, prohibition, phase II opening, or commitment decision in food delivery, online classifieds, OTA, payments, e-tail, or e-pharmacy in a Tier A jurisdiction is **Rank A regardless of severity**. Every comparable-deal outcome becomes precedent for the next Prosus transaction or signal of agency posture toward our sectors.

### Digital Markets, Sector Regulation & State Aid — Rules 18 through 19

**Rule 18 — DMA / DSA designation auto-rank.** Any DMA gatekeeper designation, DSA VLOP/VLOSE designation, or threshold revision that brings a Prosus OpC closer to scope is **Rank A regardless of severity**. Includes designation of gatekeepers Prosus OpCs depend on as business users (Google, Apple, Meta, Amazon, Microsoft, ByteDance, Booking Holdings) because the downstream effects on Prosus business-user posture are material.

**Rule 19 — FSR prohibition or precedent-setting commitment.** Any FSR prohibition decision or commitment decision establishing precedent for what counts as a "foreign subsidy" is **Rank A regardless of severity**. The regulation is in its first enforcement cycle and every decision establishes interpretive precedent that affects Prosus's Tencent-related disclosures and any future deal involving non-EU financial flows.

### Cross-domain — Rule 20

**Rule 20 — Multi-domain Monitor 02 escalation override.** When a single trigger lands on three or more Monitor 02 domains simultaneously (e.g. a DG COMP action combining merger remedies with DMA obligations and Article 102 reasoning, or a CMA market study producing both Article 102 implications and FSR-adjacent findings), the rank is set by the **highest-affected domain** and the finding is filed once in the primary domain with cross-references in the secondary domains' weekly indexes. Group GC is the default decision owner because cross-domain coordination cost otherwise falls on the persona arbitrarily.

### Cross-monitor — Rule 21

**Rule 21 — Monitor 01 / Monitor 02 cross-reference rule.** When a Monitor 02 trigger lands on a Monitor 01 domain (or vice versa), the finding is filed in the **primary monitor** (whichever monitor the trigger most directly engages) with a cross-reference note in the secondary monitor's weekly index. Canonical examples:

- CMA AI Foundation Models work → primary: Monitor 01 AI News; secondary: Monitor 02 Digital Markets.
- EU AI Act competition-policy provisions → primary: Monitor 01 AI News; secondary: Monitor 02 Digital Markets and potentially Abuse of Dominance.
- CADE food-delivery enforcement action combining horizontal-restraint and personal-data theories → primary: Monitor 02 Antitrust & Cartels; secondary: Monitor 01 Privacy.

Default reasoning: file with the monitor whose substantive doctrine most directly answers the question "what action does this require." Cross-monitor coordination is handled at Group GC level.

**Note**: symmetric update on the Monitor 01 side is now in place as **Rule 22** in `monitors/monitor-01/ranking-criteria.md` (added 2026-05-14). Behaviour is mirrored. Test cases for the cross-monitor routing live in `scripts/tests/dedup_golden.yml`.

---

## Pending operator additions (status post-Block 3 draft)

Block 3 has resolved or partially resolved most rank-rule questions previously open. Current status:

### Resolved by Block 3 rules

- ~~iFood TCC residual obligation monitoring~~ → resolved by **Rule 11**.
- ~~Delivery Hero divestment commitment monitoring~~ → resolved by **Rule 15**.
- ~~Tencent attribution rule (for competition action)~~ → resolved by **Rule 13** (direct Prosus-equivalent exposure for SAMR competition wing actions).
- ~~Below-threshold call-in elevation~~ → resolved by **Rule 16**.
- ~~MFN/parity-clause depth elevation~~ → resolved by **Rule 10** (set as auto-rank rather than one-tier-upgrade).

### Partially resolved

- **Academic-as-leading-indicator** — default posture is Rank B until first agency citation, *except* for ecosystem-theory working papers where **Rule 14** sets Rank A pre-citation given Prosus's specific exposure. Awaiting Anne-Claire's confirmation that this split posture is correct, or whether all theories-of-harm academic preprints from the trusted-primary set should auto-rank.

### Still open (require Block 1 redline or Anne-Claire's policy call)

- **Consultation-opened-as-Rank-A**. Should an open Commission consultation, OECD competition committee working paper, CMA call for evidence, or ACM market study opening that falls within `our_markets` be Rank A regardless of enforcement-risk severity, on the theory that failure to engage is itself the exposure? Default proposal: yes, Rank A. Not yet captured as a Rule 9–21 addition. Awaiting Anne-Claire's confirmation; if confirmed, becomes Rule 22.
- **Naspers / South African Competition Commission attribution**. Whether Prosus and Naspers are treated as a single undertaking for SACC purposes. Affects whether South Africa is Tier A or Tier B in `our_markets`. Block 1 redline question; rank-rule implications cascade once answered.

### Domain-specific Block 3 additions — populated

- Antitrust & cartels: Rules 9, 10, 11
- Abuse of dominance: Rules 12, 13, 14
- Merger control & FDI: Rules 15, 16, 17
- Digital markets, sector regulation & state aid: Rules 18, 19
- Cross-domain: Rule 20
- Cross-monitor: Rule 21
