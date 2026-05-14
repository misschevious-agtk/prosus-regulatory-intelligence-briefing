# Operating Preferences

Block 3 of INITIALISATION (per `SYSTEM-PROMPT.md`). How Monitor 01 runs, when it produces what, who reviews escalations, and how the function learns from missed items.

> **The personas have different natural rhythms.** Forcing them all to the same beat either over-samples Legal Ops or under-samples Privacy — both failure modes. This file captures the differentiated cadences.

---

## 1. Cadence — per persona

### AI News — **daily, with intra-day push for named-Prosus or named-Tencent triggers**

Frontier-model releases, vendor ToS changes, EU AI Office publications, and enforcement actions move on a daily news cycle.

- **Run window:** Morning (CET).
- **Findings filed:** By mid-afternoon (CET), ready for the daily index.
- **Intra-day push exception:** Any trigger that names a Prosus operating company, Tencent, or a vendor in `our_stack` with a same-day operational implication routes immediately as a push brief.

### Privacy & Data Protection — **daily, with same-day breach-incident push route**

The 72-hour breach clock is the structural reason this domain can't go weekly.

- **Run window:** Morning (CET).
- **Findings filed:** Daily.
- **Breach-incident bypass:** Breach findings bypass the daily index and route directly to the **on-call OpCo DPO and Group GC** via a dedicated channel (`INCIDENT-YYYY-MM-DD-[slug].md` — see section 2). DPA decisions, EDPB opinions, CJEU rulings flow on the normal daily cadence.

> **Breach route is the only domain with a bypass.** Protocol: **escalate first, document second.**

### Intellectual Property — **daily for marketplace and brand-protection; twice-weekly otherwise**

Counterfeit and deepfake-brand-harm enforcement signals move fast (especially when a Prosus brand is being impersonated at scale); training-data copyright rulings and patent activity can wait two days.

- **Daily scan;** **twice-weekly findings batch (Tuesday and Friday).**
- **Daily-route exceptions:** Vendor IP indemnity changes and open-source licence drift (Qwen especially) go on the daily route since they affect `our_stack` directly.

### Legal Ops — **weekly batch, with mid-week push for vendor-breach or vendor-deprecation**

Vendor announcements, bar-association opinions, court standing orders, and CLOC/ACC benchmark releases sit comfortably in a weekly cycle.

- **Weekly scan; weekly findings batch.**
- **Mid-week push exceptions:**
  - A tool in active production use suffers a breach.
  - A vendor announces a deprecation affecting an in-flight matter.
  - A court issues a sanctions ruling against a panel firm for AI use.

### Cross-domain — monthly digest and quarterly review

- **Monthly digest cadence:** First business day of each month. All four personas contribute. This is the rhythm at which patterns become visible that daily/weekly findings can't surface alone.
- **Quarterly review cadence:** Last business week of each quarter. Profile refresh, sources baseline review, `our_stack` and `our_markets` re-confirmation, rank-rule audit, evaluation of which off-baseline sources have recurred enough to warrant baseline promotion.

---

## 2. Output format — five document types + one incident channel

The system prompt already specifies (a) individual finding MDs in `/findings/` and (b) weekly `INDEX-YYYY-WW.md`. Three more layers on top, plus one incident channel.

### Type 1 — Individual finding (existing)
- **File:** `/findings/YYYY-MM-DD-[domain]-[slug].md`
- **Schema:** Full schema per `output-schema.md`. Verbatim anchor quote mandatory.
- **Audience:** The cross-domain coordination point + downstream readers.

### Type 2 — Weekly index (existing)
- **File:** `/findings/INDEX-YYYY-WW.md` (ISO week)
- **Format:** Structured listing of all findings by rank (A → B → C → D) with one-line summaries.
- **Audience:** Group GC team, AI and ethics working group.

### Type 3 — Daily push briefs (new) — AI News, Privacy, IP only
- **File:** `/findings/BRIEF-YYYY-MM-DD-[domain].md`
- **Format:** Pure prose, no schema. **3–5 sentences** summarising the day's Rank A/B findings with links to the underlying finding files.
- **Audience:** The persona's substantive partner (Group AI Counsel, Group Privacy Counsel, Tara Harris).
- **Design constraint:** **Readable in 60 seconds.**

### Type 4 — Monthly digest (new)
- **File:** `/findings/DIGEST-YYYY-MM.md`
- **Format:** Prose, structured into four sections:
  1. **What changed in the regulatory landscape this month** — by domain, 1–2 paragraphs each.
  2. **What changed in `our_stack` and our exposures** — vendor moves, OpCo developments, Tencent items, named-Prosus triggers.
  3. **What patterns are emerging across domains** — the cross-cutting analysis daily/weekly cadence can't produce.
  4. **What's coming next month** — known deadlines, anticipated rulings, scheduled regulator publications.
- **Length target:** 4–6 pages.
- **Coordinator:** The **Legal Ops persona** consolidates (already plays the cross-functional orchestration role). The other three personas draft their sections.
- **Audience:** Group GC and OpCo GCs.

### Type 5 — Quarterly board-facing summary (new)
- **File:** `/findings/BOARD-SUMMARY-YYYY-QQ.md`
- **Format:** Prose only, no findings-level detail. **~2 pages.**
- **Focus:**
  - Material risk shifts.
  - Material new obligations.
  - Material new exposures.
  - One paragraph on the function's own performance against its KPIs (findings filed, escalations, false-positive rate measured by Rank A items downgraded after human review, time-to-finding from primary-source publication).
- **Owner:** Group GC owns the document; the four personas feed in.
- **Audience:** Group ExCo and the board risk committee.

### Incident channel — standing on-call route (new)
- **File:** `/findings/INCIDENT-YYYY-MM-DD-[slug].md`
- **Format:** Short incident-style note — what happened, who's affected, what we know, what we don't, **what the clock is**.
- **Bypasses the normal schema.** One per incident.
- **Structural owner:** **Privacy persona** (the 72-hour breach clock is the load-bearing case). Other personas may file incidents that route differently — e.g. a critical vendor breach affecting Toqan or the LCM stack goes via the AI persona to the same incident channel.
- **Audience:** On-call OpCo DPO + Group GC; cross-copies the relevant substantive persona partner.

### Mapping audience × cadence

| Output type            | Cadence              | Audience                                            |
|------------------------|----------------------|-----------------------------------------------------|
| Individual finding     | Per-event            | Cross-domain coordination + downstream readers      |
| Daily push brief       | Daily                | Persona's substantive partner                       |
| Weekly index           | Weekly               | Group GC team, AI and ethics working group          |
| Monthly digest         | Monthly              | Group GC + OpCo GCs                                  |
| Quarterly board summary| Quarterly            | Group ExCo + board risk committee                    |
| Incident               | Same-day             | On-call DPO/GC + persona partner                    |

> Skip the brief and the substantive lawyers have to read every finding to keep up; skip the digest and the pattern-level intelligence is invisible; skip the board summary and the function can't demonstrate value upward.

---

## 3. Escalation review — who and on what timeline

Two-tier escalation review, separating the rank-rule trigger from the human-judgment review.

### Rank A — within 48 hours, by named individuals (acknowledgment + triage)

> A single 48-hour clock for all Rank A items isn't realistic if it's "review and decide"; **it is realistic if it's "review, acknowledge, schedule the decision."** The 48-hour clock is for **acknowledgment and triage**, with the actual decision routing into one of:
> - **Same-week** — most Rank A items within the persona's substantive partner's authority.
> - **Next-cycle** — Rank A items requiring cross-domain or cross-functional coordination, batched into the weekly review.
> - **Next-monthly** — Rank A items that surface a pattern rather than a discrete action (drives `needs.md` or rank-rule revisions).

Named owners per domain (substantive review pair):

| Domain      | Substantive review pair                                                                                        | Lateral copy                                              |
|-------------|---------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| AI News     | Group AI Counsel persona **+** Group AI team lead (Euro Beinat's organisation)                                | Group Privacy Counsel and Tara Harris when relevant       |
| Privacy     | Group Privacy Counsel persona **+** relevant OpCo DPO                                                          | Group AI Counsel and Tara Harris when relevant            |
| IP          | Tara Harris (or named successor) **+** Group GC                                                                | AI and Privacy when relevant                              |
| Legal Ops   | Head of Legal Ops **+** Group GC **+** Procurement lead (vendor-related) or relevant OpCo GC (ethics/court-rule items) | —                                                  |

### Escalate-class items — within 24 hours, by Group GC

When a persona marks a finding `recommended_action_class: escalate` rather than `act`, the rank rules didn't fit the item and human judgment is needed. The **Group GC is the single owner of the escalate channel**; can delegate to a deputy but **not to the persona itself** (that would defeat the purpose). This is the relief valve for novel categories the rank table doesn't anticipate.

### Weekly review — by the Digital & Regulatory team collectively

All **Rank B findings** reviewed once a week in a **30-minute standing slot**. Rank B is where patterns surface that warrant a posture shift; bringing the four personas' substantive partners together once a week is where the cross-domain reading happens.

### Monthly review — by Group GC and OpCo GCs

- **Artefact:** the monthly digest (Type 4 above).
- **Format:** 60-minute standing meeting with the four substantive partners plus OpCo GCs joining via roster (not all at once).
- **Output:** any rank-rule revisions, `our_markets` updates, `our_stack` updates, profile refresh items.

### Quarterly review — by Group ExCo and the board risk committee

- **Artefact:** the board summary (Type 5 above).
- **Cadence:** whatever the board already has.
- **Focus:** the function itself is reviewed — KPIs, false-positive rates, missed-item retrospectives.

---

## 4. Missed-item retrospectives

> **The most important continuous-improvement mechanism the system has, and the one easiest to skip when busy. Bake it in.**

When a regulatory or vendor event surfaces **outside the Monitor 01 stream** — a Group GC hears about it from external counsel, a peer company, the press, or an internal stakeholder — the team runs a short post-mortem with these questions:

1. **Was the item in scope?** Should the personas have caught this?
2. **Did the sources baseline cover the surface area?** Or did the item live in a source none of the four personas tracks?
3. **Did the persona file but not escalate?** Was it caught and triaged-down inappropriately?
4. **Did the rank rules misfire?** Did the schema's enumerated fields not capture what made this material?

Findings from these retrospectives feed the **quarterly profile refresh** and may produce rank-rule revisions (additions to Rules 1–21).

---

## 5. Calibration mode (first 14 days)

Per `cold-start-protocol.md`:

- **Prosus Relevance Filter** runs **one level looser** than the steady-state setting (each persona's profile.md states the persona's target strictness).
- **Daily cap +50%**, hard ceiling 15 items.
- **Two-sentence summaries** instead of one.
- **Daily owner check-in for first 3 days**, every-other-day thereafter.
- **Locked filters and Rule 6 (Tencent attribution), Rule 12 (breach clock), Rule 14 (DPF fragility) remain inviolate** even during calibration.
- **Day 14 calibration review** with the four substantive partners.

---

## Change log

| Date       | Change                                                                                                       | Author |
|------------|--------------------------------------------------------------------------------------------------------------|--------|
| 2026-05-12 | Initial Block 3 operating preferences — differentiated cadences, six output types, two-tier escalation review, missed-item retrospective protocol. | Operator |
