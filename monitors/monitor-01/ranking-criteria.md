# Ranking Criteria (SHARED — TIER-2 FIXED RANKS)

This is the **set-in-stone** rank table. It operates only on enumerated fields from `output-schema.md`. It does not read prose. If a finding cannot be ranked by these rules, the finding's `recommended_action_class` is set to `escalate` and the item is routed for human triage.

The value of this layer is **consistency, not coverage**. When in doubt between two ranks, take the lower rank.

---

## Inputs only

The ranker reads — and only reads — the following fields from each finding's frontmatter:

- `trigger_type`
- `severity_self_assessment` (referred to below as `severity`)
- `deadline_if_any`
- `jurisdiction` (compared against `our_markets`)
- `source_type`
- `affected_systems_or_practices` (compared against `our_stack` for in-stack/in-practice tests)
- `primary_axis`
- `recommended_action_class`
- `confidence`
- `date_found`

It does not read prose. If a rule would require reading the body, the schema is missing a field — add the field rather than letting tier-2 do prose interpretation.

---

## Rank A — Immediate human review (≤48 hours)

A finding lands at Rank A if **any** of the following is true:

- `trigger_type = law_effective_date` AND `deadline_if_any ≤ 180 days` AND `jurisdiction ∈ our_markets`
- `trigger_type = enforcement_action` AND `severity ≥ 4`
- `trigger_type = court_ruling` AND `source_type ∈ [primary-law, court-ruling]` AND `severity ≥ 4`
- `trigger_type = breach_incident` AND `affected_systems_or_practices` includes a system listed in `our_stack`
- `recommended_action_class = escalate` (any reason)

---

## Rank B — Weekly review

A finding lands at Rank B if **any** of the following is true (and it does not qualify for Rank A):

- `severity = 3` across any trigger type
- `trigger_type = regulator_guidance` AND `jurisdiction ∈ our_markets`
- `trigger_type = vendor_change` AND vendor is in `our_stack`
- `trigger_type = license_event` (any IP-domain finding)
- `trigger_type = tooling_change` AND tool is in `our_stack` (legal-ops domain)
- `confidence = high` AND `primary_axis ∈ [compliance, liability]`

---

## Rank C — Monthly digest

A finding lands at Rank C if **any** of the following is true (and it does not qualify for Rank A or B):

- `severity ≤ 2` AND `confidence ≥ medium`
- `trigger_type ∈ [market_move, capability_demo, narrative_shift, workflow_benchmark]`
- `primary_axis = reputational` (unless `severity ≥ 4`)

---

## Rank D — Archive only, no review surface

A finding lands at Rank D if **any** of the following is true (and it does not qualify for A, B, or C):

- `confidence = low` AND `severity ≤ 2`
- `source_type = marketing` AND no corroboration
- Items not affecting any system, practice, or obligation listed in the relevant `needs.md`

---

## Tie-breaking

When a finding hits multiple rank rules, the highest rank wins (A > B > C > D).

When two findings are at the same rank and an order is needed (e.g. for an index):

1. **Higher `severity` first.**
2. **Sooner `deadline_if_any` first** (null deadlines sort last within their rank).
3. **Newer `date_found` first.**

Tier-2 must **never** re-read the source to break a tie. If it would need to, the schema is missing a field. Add the field rather than letting tier-2 do prose interpretation.

---

## Operator-specified rules (Rules 1–8)

These rules apply **after** the base Rank A/B/C/D tables above. They upgrade, ceiling, or attribute findings based on operator-supplied context from `our_markets.md`, `our_stack.md`, `sectoral-overlays.md`, and `portfolio-map.md`. Like the base rules, they read only enumerated fields.

### Rule 1 — Tier A upgrade

When a Monitor 01 trigger touches a **Tier A jurisdiction** (per `our_markets.md`) AND a Prosus operating company is **directly named**, the rank **moves up by one tier** from the default.

> Example: An ANPD enforcement action naming iFood is automatically **Rank A**. A CNIL guidance document covering recommender systems is **Rank A** if it could touch iFood's LCM, OLX's matching, or Despegar's personalisation.

### Rule 2 — Tier C / D ceiling

Items from **Tier C** jurisdictions never reach above **Rank B**, regardless of severity, unless severity ≥ 4 AND a specific Prosus exposure is named. Items from **Tier D** jurisdictions never reach above **Rank C**, regardless of severity.

> Tier C/D items contribute **precedent only**, never auto-upgrade rank.

### Rule 3 — Extraterritorial-reach instruments treated as Tier A

When the affecting instrument is **extraterritorial in legal effect** (GDPR, EU AI Act, DSA, EU Data Act, UK GDPR, and US state privacy laws to the extent Prosus companies have US users), the item is treated as **Tier A for the whole group** regardless of operating-company footprint.

> Rationale: a Prosus entity sitting outside the EU still has direct exposure when a user is in the EU. The ranker must not downgrade an EU AI Act item because the affected operating company is iFood Brazil — the LCM is processing data about EU users via Despegar/JET cross-sell.

### Rule 4 — Court rulings weighted by appellate level

Court rulings are weighted by the appellate level of the issuing court.

- **CJEU Grand Chamber, US Supreme Court, UK Supreme Court, national supreme/constitutional courts** — `severity_self_assessment` floor of 4; **Rank A** even when other rule conditions are not met, if `domain` is in scope.
- **General Court of the EU, US Federal Circuit / Circuit Courts of Appeals, UK Court of Appeal, national appellate courts** — `severity_self_assessment` floor of 3; **Rank B** baseline.
- **First-instance / district / trial-level rulings** — **Rank B** unless named-Prosus or directly precedent-setting for a practice we use.

> Stops the ranker over-weighting district court noise.

### Rule 5 — Bar / ethics rulings weighted by in-house jurisdiction relevance

Bar association and ethics rulings on **AI-in-legal-practice** are **Rank C by default**, **upgraded to Rank B only when** they affect a jurisdiction where Prosus's in-house legal function operates (Netherlands, UK, US states where in-house counsel sit — see `portfolio-map.md`).

> Stops every ABA Formal Opinion on ChatGPT generating a Rank A finding.

### Rule 6 — Tencent-attribution rule

China-jurisdiction items are:

- **Rank A** when they (a) name Tencent, (b) affect a regulatory framework that materially binds Tencent, or (c) signal a doctrine that would reasonably bind Tencent within 12 months.
- **Rank B** for Chinese sector-wide guidance that doesn't yet reach Tencent.
- **Rank C** for general China-tech-precedent value with no Tencent nexus.

> Tencent is treated as if it were a Prosus operating company for ranking purposes in this domain, even though it isn't controlled, because the financial and disclosure exposure is functionally equivalent. The analogue of the operating-company upgrade rule (Rule 1) for the Tencent stake.

### Rule 7 — Sectoral-overlay upgrade

When a Monitor 01 trigger touches one of the sectoral overlays in `sectoral-overlays.md` AND the affected Prosus operating company is in that sector, **the rank moves up by one tier** from the default.

> Example: A generic CNIL guidance document on AI hits **Rank B** normally, but if it specifically addresses **AI-in-payments**, it becomes **Rank A** for PayU/iyzico.
>
> Prevents the ranker treating "AI in credit scoring" the same as "AI in retail."

### Rule 8 — Multi-sector items

When a single trigger lands on two or more sectoral overlays at once (very common for AI rules — e.g. EU AI Act high-risk classifications hit financial services, employment, and health simultaneously), **the rank is set by the highest-affected sector**, and the finding records all affected sectors in the `secondary_axes` field of the schema.

> Multi-domain analogue of the cross-domain filing rule in `SYSTEM-PROMPT.md` Operating Rule 5.

### In-stack rank notes (from `our_stack.md`)

Three operational notes apply alongside Rules 1–8:

- **Multi-vendor architecture lowers urgency for single-vendor events.** Single-vendor disruptions are recoverable when redundancy exists; capability-class disruptions are not.
- **Qwen / Chinese-origin model events are upgraded.** Any event affecting Qwen, US export controls on Chinese AI, or Alibaba's open-source licensing posture is **automatically Rank A** because LCM has a direct dependency. (Now also formalised as **Rule 10**.)
- **Toqan and LCM are regulated artefacts, not just consumption.** Regulatory developments addressing model **developer** obligations shift the materiality threshold downward for AI persona.

---

## Domain-specific rules (Rules 9–21)

These rules surface things the shared Rules 1–8 under-rank or over-rank, per domain. They are operator-specified (Block 3 INITIALISATION) and read enumerated fields only.

### AI News domain — Rules 9–11

#### Rule 9 — Frontier-model release auto-rank
A frontier-model release by a vendor in `our_stack` (Anthropic, OpenAI, AWS, Alibaba/Qwen) is **automatically Rank B** unless paired with one of:
- (a) Deprecation of a model in production use,
- (b) Material capability shift affecting a deployed Prosus system,
- (c) Vendor ToS or pricing change.

In any of (a)/(b)/(c), the rank upgrades to **Rank A**.

Releases by **non-stack vendors** (Mistral, DeepSeek, Llama) are **Rank C** unless they cross the GPAI compute threshold or are publicly cited as candidates for stack inclusion.

#### Rule 10 — Qwen / Chinese-origin auto-upgrade
Any item affecting Qwen specifically, **US export controls on Chinese AI**, or Alibaba's open-source licensing posture is **Rank A regardless of severity score**, because the LCM has a direct architectural dependency. The named-dependency analogue of the Tencent-attribution rule (Rule 6).

#### Rule 11 — GPAI Code of Practice and Annex III triggers
Any change to:
- The **GPAI Code of Practice** (new measures, new signatories, threshold updates),
- Any **expansion of EU AI Act Annex III**,
- Any **implementing regulation affecting GPAI provider obligations**,

is **Rank A regardless of severity**, because the LCM is plausibly in scope and the obligations carry hard deadlines.

### Privacy & Data Protection domain — Rules 12–14

#### Rule 12 — Breach-clock override
Any breach incident plausibly engaging the **72-hour notification clock at any OpCo** is **Rank A automatically** and routes via the **same-day incident channel** (`INCIDENT-YYYY-MM-DD-[slug].md`), bypassing the normal daily cadence. Severity score is computed retroactively for the audit trail but does not gate the routing.

> **Structural owner:** Privacy persona.

#### Rule 13 — Article 22 / LGPD Article 20 doctrine creep
Any regulator decision, court ruling, EDPB opinion, or DPA guidance that broadens the characterisation of **"decisions based solely on automated processing"** — particularly to include:
- Recommender systems
- Dynamic pricing
- Gig-platform dispatch
- AI-assisted credit decisioning

is **Rank A regardless of severity**. The LCM, OLX Magic, PayU credit, and gig-platform dispatch all sit on this line.

#### Rule 14 — DPF / cross-border transfer fragility
Any Schrems-style challenge to the **EU-US Data Privacy Framework** that advances to a stage creating real fragility (CJEU referral, adequacy review, Commerce Department decertification, EDPB binding opinion) is **Rank A regardless of severity**, because cross-border transfer mechanism failure is a portfolio-wide operational problem.

### Intellectual Property domain — Rules 15–17

#### Rule 15 — Training-data copyright doctrine auto-upgrade
Any court ruling on AI training-data copyright in **N.D. Cal., S.D.N.Y., D. Del., Federal Circuit, UK High Court, CJEU, Tokyo District Court, Delhi HC, or Bombay HC** is **Rank A regardless of severity at trial level**, and stays Rank A at appellate level.

> Rationale: the LCM's training pipeline is the single largest IP exposure in the group and the doctrine is unsettled enough that every ruling matters.

#### Rule 16 — Vendor IP indemnity narrowing
Any **narrowing of training-data indemnity, output-IP indemnity, or carve-out scope** by Anthropic, OpenAI, AWS, or any vendor in `our_stack` is **Rank A regardless of severity**, because the indemnity terms are operational protections the business has been relying on.

#### Rule 17 — Deepfake brand harm at scale
Any deepfake or AI-impersonation campaign targeting a **Prosus brand, OpCo, or named executive at material scale** is **Rank A regardless of severity** and routes via the IP persona to the relevant OpCo's brand-protection team within **48 hours**.

**Material scale defined as:**
- More than one platform, OR
- More than one jurisdiction, OR
- Evidence of organised activity rather than isolated incident.

### Legal Ops domain — Rules 18–20

#### Rule 18 — Production-vendor breach or deprecation auto-rank
Any breach incident, security advisory, or deprecation announcement affecting a **vendor in active production use** in our legal-tech stack is **Rank A regardless of severity**, and routes via the **mid-week push channel**.

> Rationale: legal-tech vendor failures affect in-flight matters and privilege exposure, both time-sensitive.

#### Rule 19 — Court standing order on AI use
Any **US federal court, UK court, or other court-of-Prosus-active-litigation** issuing:
- A standing order requiring AI-use disclosure,
- A prohibition on AI-generated filings,
- Sanctions on AI-related conduct,

is **Rank A regardless of severity**, because it changes how panel firms must operate on our matters.

#### Rule 20 — Pilot-kill threshold
Any **AI-in-legal-tools pilot that crosses its pre-defined success-or-kill threshold** (in either direction) is **Rank A**.

> Unusual because it's an **internal trigger** rather than an external one, but it belongs in the rank rules because it forces the function to confront the kill-or-promote decision on schedule rather than letting pilots drift indefinitely.

### Cross-domain — Rule 21

#### Rule 21 — Multi-domain item escalation override
When a single trigger lands on **three or more domains simultaneously** (e.g. a CJEU ruling on AI-training that touches AI, Privacy, IP, and indirectly Legal Ops via panel-firm advice):
- The **rank is set by the highest-affected domain**.
- The finding is **filed once in the primary domain** with cross-references in the secondary domains' weekly indexes.
- **The Group GC is the default decision owner on multi-domain items**, because the coordination cost otherwise falls on whichever persona filed first.

This is the domain-level analogue of Rule 8 (multi-sector).

### Cross-monitor — Rule 22

#### Rule 22 — Monitor 01 / Monitor 02 cross-reference rule
Symmetric with Monitor 02's Rule 21. When a Monitor 01 trigger lands on a Monitor 02 domain (or vice versa), the finding is filed in the **primary monitor** — the monitor whose substantive doctrine most directly answers the question "what action does this require" — with a cross-reference note in the secondary monitor's weekly index.

Canonical examples:

- CMA AI Foundation Models work → primary: Monitor 01 AI News; secondary: Monitor 02 Digital Markets.
- EU AI Act competition-policy provisions → primary: Monitor 01 AI News; secondary: Monitor 02 Digital Markets and potentially Abuse of Dominance.
- CADE food-delivery enforcement action combining horizontal-restraint and personal-data theories → primary: Monitor 02 Antitrust & Cartels; secondary: Monitor 01 Privacy.

Cross-monitor coordination is handled at Group GC level. Feedback (👍/👎) on a cross-reference flows back to the **primary** monitor, not the linking one (see `strategy.md` Cross-monitor deduplication).

Test cases for the dedup engine live in `scripts/tests/dedup_golden.yml` and are run by `scripts/test_dedup.py`.

---

## Failure modes the ranker does not absorb

The ranker is intentionally narrow. The following are handled elsewhere:

- **Ambiguity about whether a vendor is in `our_stack`** — handled at the schema layer, by requiring `affected_systems_or_practices` to use names from the `our_stack` vocabulary. If a name doesn't match, the agent flags `confidence: low` and surfaces an open question.
- **Cross-domain double-filing** — handled by Operating Rule 5 in `SYSTEM-PROMPT.md`. The ranker doesn't deduplicate; it ranks every filed finding once.
- **Stale findings** — handled by an archival sweep, not the ranker. A Rank A finding from 6 months ago is still Rank A in its frozen state; archival is a separate action class.

---

## Change discipline

This file is set in stone. To add a rank rule or change a threshold:

1. Open an explicit change request with the operator. State the rule, the field(s) it depends on, and the rank.
2. If the new rule needs a field not yet in `output-schema.md`, add the field to the schema in the same change. Backfill existing findings as needed.
3. Test the change against the last 30 days of findings — does any finding move ranks? Is that movement intentional?
4. Update this file and date the change in the change log below.

---

## Change log

| Date       | Change                                                                                                                    | Author    | Sign-off |
|------------|---------------------------------------------------------------------------------------------------------------------------|-----------|----------|
| 2026-05-12 | Initial spec — Ranks A, B, C, D                                                                                            | Operator  | Operator |
| 2026-05-12 | Rules 1–8 added (Tier A upgrade, Tier C/D ceiling, extraterritorial-reach, court appellate weighting, bar/ethics weighting, Tencent-attribution, sectoral-overlay upgrade, multi-sector resolution). Three in-stack notes added. | Operator  | Operator |
| 2026-05-12 | Domain-specific Rules 9–21 added: AI News (9 frontier-model, 10 Qwen/Chinese-origin, 11 GPAI/Annex III), Privacy (12 breach-clock, 13 ADM doctrine creep, 14 DPF fragility), IP (15 training-data copyright, 16 vendor IP indemnity, 17 deepfake brand harm), Legal Ops (18 production-vendor breach, 19 court AI standing orders, 20 pilot-kill threshold), Cross-domain (21 multi-domain escalation override). | Operator | Operator |
| 2026-05-14 | Rule 22 added — Monitor 01 / Monitor 02 cross-reference rule, symmetric with Monitor 02 Rule 21. Closes the Block 3 sign-off flag carried in M02. Dedup test harness at `scripts/test_dedup.py` + `scripts/tests/dedup_golden.yml`. | K. Maleevska | Operator |
