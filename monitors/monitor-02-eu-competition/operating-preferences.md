# Operating Preferences — Monitor 02

> **[DRAFT — confirm with operator]**
>
> This document captures Block 3 operating preferences for Monitor 02: cadence per domain, output format and document types, escalation review, missed-item retrospectives, and confidentiality framing. Domain-specific rank-rule additions (Rules 9–21) sit in `ranking-criteria.md`, not here. Three flags for Anne-Claire's sign-off at the end.

## 1. Cadence — per domain

The four Monitor 02 domains have meaningfully different natural rhythms. Competition enforcement moves slower in headline cadence than AI news or privacy (Monitor 01's territory), but the deal-clock pressure in merger control and the same-day dawn-raid pattern in antitrust-and-cartels create more concentrated push moments than the Monitor 01 personas need.

### Antitrust & Cartels — twice-weekly batch, with same-day push for dawn-raid patterns and statement-of-objections-grade events

Routine enforcement (decisions, judgments, vertical-restraint cases, MFN doctrine) moves on a slower cycle than AI or privacy; a twice-weekly batch (Tuesday and Friday) captures it without losing signal. The exceptions: dawn-raid pattern detection in any sector with Prosus exposure, and any statement of objections naming a Prosus OpC, Tencent, or a forum we participate in. These bypass the batch and route same-day to the on-call escalation chain. Anne-Claire's persona explicitly treats dawn-raid pattern detection as same-day-push (P7), mirroring the Privacy persona's breach-incident route.

### Abuse of Dominance — twice-weekly batch, with intra-day push for named-Prosus or Tencent enforcement

Same base cadence and exception structure as antitrust-and-cartels. The CJEU and General Court rulings on Article 102 doctrine that travel are the most consequential single category for this domain; a Grand Chamber ruling deserves intra-day attention even when not naming a Prosus entity, because the doctrinal portability is the point.

### Merger Control & FDI — daily, with intra-day push for deal-clock-sensitive events

The only Monitor 02 domain that runs daily. Two reasons. First, the live Delivery Hero divestment monitoring is operational compliance work that benefits from daily attention. Second, merger-control developments globally (any clearance, prohibition, phase II opening, commitment, or Article 22 referral in food delivery, classifieds, payments, OTA, e-tail, e-pharmacy across Tier A jurisdictions) are deal-relevant intelligence in a way the other three domains' developments aren't. The daily cadence isn't about volume; it's about ensuring no deal-clock-sensitive event is missed.

Intra-day push for: Article 22 referral requests, CMA call-in decisions, BKartA §39a notifications, FSR notifications, FDI/NSI Act reviews naming Prosus or a signalled transaction, and any Delivery Hero divestment commitment modification or alleged breach.

### Digital Markets, Sector Regulation & State Aid — weekly batch, with mid-week push for DMA enforcement and gatekeeper-effects events

Slowest base cadence of the four because the regulatory cycle (DMA enforcement decisions, FSR cases, market investigations, sector regulation transposition) is genuinely slower. Mid-week push for: DMA designation decisions, DMA non-compliance decisions affecting gatekeepers Prosus depends on (Google, Apple, Meta, Amazon, Microsoft, ByteDance, Booking Holdings particularly), DSA VLOP/VLOSE designation decisions affecting Prosus OpCos, FSR prohibitions, and any sectoral-regulator enforcement action with material competition-conduct implication for a Prosus OpC.

### Cross-domain — monthly digest and quarterly / annual review

**Monthly digest** — first business day of each month. All four domains feed a higher-level digest in the same pattern as Monitor 01. Anne-Claire's policy-engagement role makes the digest especially important here because the patterns visible across daily/weekly findings (DG COMP enforcement intensity drifting, agency speech themes converging, academic consensus forming) are exactly what she needs to read for the Brussels working-lunch and Concurrences-circuit conversations she shapes.

**Quarterly review** — last business week of each quarter. Profile refresh, sources baseline review, `our_markets` and dominance-map re-confirmation, rank-rule audit, persona-overlap calibration, and the same off-baseline-source promotion exercise as Monitor 01. The dominance map review is particularly important for this monitor — market shares shift, market definitions sharpen, and the question of which Prosus OpCs are "plausibly dominant" should be re-asked formally each quarter rather than re-asked implicitly per finding.

**Annual review** — once a year, calibrated with the Prosus competition compliance review cycle. Standing annual review checking that the four `needs.md` files still reflect the actual portfolio (post-disposal, post-acquisition), that the dominance map is current, that the trade-associations-and-fora list is accurate, and that the persona's posture-by-axis settings still match how Anne-Claire actually reads. Tied to whatever annual competition-compliance cycle Prosus already runs so it doesn't create an additional process.

## 2. Output format — five document types + one incident channel + one policy-paper note

Same five-layer structure as Monitor 01, parameterised differently for the four domains' rhythms.

### Type 1 — Individual finding (existing in `/output-schema.md`)

Per the existing schema. One MD per finding in `/findings/`, named `YYYY-MM-DD-[domain]-[slug].md`.

### Type 2 — Weekly index (existing in system prompt)

`INDEX-YYYY-WW.md` aggregating all four domains' findings by rank with one-line summaries. Audience: Anne-Claire + Group GC + the Digital & Regulatory team for cross-monitor coordination with Monitor 01 personas.

### Type 3 — Push briefs (new)

Per-domain briefs at each domain's cadence. Short MD, pure prose, no schema, 3–5 sentences summarising the period's Rank A/B findings with links to underlying finding files.

- **Daily** for Merger Control & FDI: `BRIEF-YYYY-MM-DD-merger-control-fdi.md`, top of `/findings/`. Audience: Anne-Claire + Group GC + Corporate Development.
- **Twice-weekly** for Antitrust & Cartels and Abuse of Dominance: `BRIEF-YYYY-MM-DD-antitrust-cartels.md` and `BRIEF-YYYY-MM-DD-abuse-of-dominance.md` published Tuesday and Friday.
- **Weekly** for Digital Markets, Sector Regulation & State Aid: `BRIEF-YYYY-WW-digital-markets-sector-state-aid.md`, published Friday afternoon.

### Type 4 — Monthly digest (new)

`DIGEST-YYYY-MM.md`. One document per month, all four Monitor 02 domains, written in prose with structure:

- (i) what changed in the competition-law landscape this month — by domain, with policy and academic threads explicit;
- (ii) what changed in Prosus's deal and remedy posture — Delivery Hero monitoring, iFood TCC monitoring, any signalled transactions, any FSR/FDI exposures, any market-investigation engagement;
- (iii) what patterns are emerging across domains and across the EU/UK/Brazil/India regulatory landscape;
- (iv) what Anne-Claire is hearing in the policy circuit that the formal record hasn't yet caught up to — the section that distinguishes this monitor's digest from a pure-enforcement summary;
- (v) what's coming next month — known deadlines, anticipated rulings, scheduled regulator publications, scheduled academic conferences and Concurrences events.

Length target: 4–6 pages. Anne-Claire owns the prose voice; the monitor produces the structured draft she edits. Audience: Group GC, OpCo GCs, ExCo as recipient (not as reviewer).

### Type 5 — Quarterly board-facing summary (new)

`BOARD-SUMMARY-YYYY-QQ.md`. Two pages, prose, no findings-level detail. Audience: Board risk committee. Focus: material competition exposures shifts, ongoing remedy compliance (Delivery Hero, iFood TCC), any active investigations or regulator dialogues, the function's KPIs. Group GC owns the document; Anne-Claire drafts the competition section.

### Incident channel — standing on-call route

`INCIDENT-YYYY-MM-DD-[slug].md`. Same structure as Monitor 01 for dawn-raid notifications, statement-of-objections-grade events, FSR or FDI prohibition orders, or any Delivery Hero divestment commitment alleged-breach signal. Bypasses normal schema; short prose note (what happened, who's affected, what we know, what we don't, what the clock is). Anne-Claire is the structural owner of the incident route for Monitor 02; cross-references into Monitor 01 incident channels where the trigger has cross-monitor implications (the CMA AI Foundation Models work being the canonical example of a competition-framed trigger that lands in Monitor 01 as well).

### Policy-paper finding (unique to Monitor 02)

Academic working papers, Concurrences articles, and OECD/Bruegel/CERRE policy work are sometimes themselves the unit of analysis rather than reactions to news events. A finding may be filed on a single high-signal working paper if it proposes a coherent new theory of harm that any major agency could plausibly adopt within 12 months. These findings use the standard schema but the `source_type` is set to `academic`, `source_publisher` to the institution, and the confidence calibration is explicitly signal-only unless an agency has cited the paper. The receiving Claude treats these as a normal output category, not as an exception.

### Mapping audience × cadence

| Document | Audience | Cadence |
|---|---|---|
| Individual findings | Anne-Claire + Group GC + named recipients | Continuous |
| Push briefs (per domain) | Anne-Claire + Group GC + (merger-control: Corporate Development) | Per domain rhythm |
| Weekly index | Anne-Claire + Group GC + Digital & Regulatory team | Weekly |
| Monthly digest | Group GC + OpCo GCs + ExCo (recipient) | Monthly |
| Board-facing summary | Board risk committee | Quarterly |
| Incident notes | Anne-Claire + Group GC + named recipients (same-day) | As triggered |
| Policy-paper findings | Anne-Claire + (selectively) Group GC | As triggered |

## 3. Escalation review — who and on what timeline

Same two-tier structure as Monitor 01 (acknowledge-and-triage within 48 hours, decide on appropriate cycle), but the named owners differ because the substantive partner here is a single person (Anne-Claire) rather than four, and Corporate Development becomes a regular reviewer for merger-control items.

### Rank A — within 48 hours, acknowledge and triage, by named individuals

- **Antitrust & Cartels Rank A** → Anne-Claire + Group GC + retained external counsel for the affected jurisdiction. For dawn-raid pattern detections and statement-of-objections-grade events, add the relevant OpCo GC. For information-exchange / trade-association concerns, add the OpCo participating in the forum.
- **Abuse of Dominance Rank A** → Anne-Claire + Group GC + retained external counsel. For ecosystem-theory or recommender-system-as-abuse findings, add Group AI Counsel and Tara for cross-domain coordination (the LCM, OLX Magic, and Ailo questions cross from Monitor 02 into Monitor 01 AI and IP). For exploitative-T&Cs findings, add Group Privacy Counsel.
- **Merger Control & FDI Rank A** → Anne-Claire + Group GC + Corporate Development + retained external counsel for the affected jurisdiction. Corporate Development is a standing recipient on this domain in a way it isn't on the other three; deal-flow context is necessary for ranking decisions.
- **Digital Markets, Sector Regulation & State Aid Rank A** → Anne-Claire + Group GC + relevant OpCo GC + (for DMA/DSA-gatekeeper-effects findings) Group AI Counsel and Group Privacy Counsel. For sectoral-regulator findings, add the relevant sectoral compliance owner at the affected OpCo.

The 48-hour clock is for acknowledgment and triage, not for decision — same posture as Monitor 01. Decisions route into same-week (most Rank A items within Anne-Claire's authority), next-cycle (cross-domain or cross-functional coordination), or next-monthly (pattern-level items driving rank-rule or `needs.md` revisions).

### Escalate-class items — within 24 hours, by Group GC

The `escalate` action class is Anne-Claire's relief valve for novel category items the rank rules don't anticipate. Group GC owns the channel; can delegate to a deputy but not to Anne-Claire herself (defeats the purpose). Same posture as Monitor 01.

### Weekly review — Anne-Claire + Group GC + invited OpCo GCs

All Rank B findings reviewed in a standing weekly slot. The composition is leaner than Monitor 01's weekly review (which assembled the four Monitor 01 substantive partners) because Monitor 02 has one substantive partner. OpCo GCs rotate through on a roster — iFood, OLX Group, JET, PayU, Despegar, eMAG, Swiggy, Stack Overflow as the primary set — so that no OpCo's competition exposure is reviewed without its GC present.

### Monthly review — Group GC, Anne-Claire, OpCo GCs, plus invited cross-monitor participants

Monthly digest is the artefact; the review is a standing 60-minute meeting. Tara, Group AI Counsel, and Group Privacy Counsel join when the digest contains cross-monitor items (which it usually will, because Monitor 02 digital-markets domain bleeds into Monitor 01 AI and Privacy domains routinely).

### Quarterly review — Group ExCo + Board risk committee

Quarterly summary is the artefact; the review cadence follows whatever the board risk committee already runs. KPIs and function-level retrospectives are presented at this layer.

### A note on external-counsel coordination

Unique to this monitor: external counsel are partners in the escalation chain, not just consulted experts. When Anne-Claire escalates a Rank A item involving an active matter, retained counsel is in the loop on the same 48-hour clock — they need to know what the monitor is surfacing so their advice tracks the same primary sources. For findings on live matters, the monitor's output may need to flow into privileged communications; see Section 5 (Confidentiality framing).

## 4. Missed-item retrospectives

Same discipline as Monitor 01. When a competition development surfaces outside the Monitor 02 stream — Anne-Claire hears about it from a Skadden or Cleary partner before the monitor catches it — a short post-mortem covers:

- was the item in scope;
- did the sources baseline cover the surface area;
- did the persona file but not escalate;
- did the rank rules misfire.

Findings feed the quarterly profile refresh.

## 5. Confidentiality framing

Competition work has confidentiality requirements that the Monitor 01 domains don't have in the same way. Four distinct layers; each shapes how the receiving Claude drafts findings, not just how findings are distributed. **Drafting with privilege in mind affects voice, attribution, and what gets included; getting that wrong creates discoverable record.**

### Layer 1 — Legal professional privilege

Findings that touch active investigations, live merger reviews, ongoing remedy monitoring (Delivery Hero, iFood TCC), or matters where Prosus has retained external counsel for advice are privileged work product. The monitor's outputs on these matters must be drafted as if they will be reviewed under privilege — meaning attribution to external counsel where counsel is the source, careful framing of internal legal analysis, and explicit privilege markings on finding MDs where applicable.

**Receiving Claude instruction**: when a finding touches a live matter with retained counsel, the finding MD includes a header line `Privileged and confidential — prepared for legal advice` and the substantive content is drafted with privilege in mind. Anne-Claire confirms which live matters require this treatment as part of Block 1 redline.

### Layer 2 — Leniency programme sensitivity

If at any point Prosus is considering or has filed a leniency application (none publicly known but Block 1 Question 8 is where this is confirmed), every related finding is strictly compartmentalised. The leniency-track finding stream sits outside the normal `/findings/` flow and is accessible only to Anne-Claire and Group GC; cross-references in indexes are redacted or omitted.

**Receiving Claude instruction**: if any leniency-adjacent finding is produced, route via incident channel to Anne-Claire only, flag the finding as `LENIENCY-SENSITIVE`, and wait for human routing decision before any wider distribution.

### Layer 3 — Information-exchange discipline

Anne-Claire's antitrust-and-cartels reading-mode is hyperaware of information-exchange risk. The monitor's outputs are an internal information channel; they could in principle be discoverable in the course of an information-exchange investigation if Prosus participates in a forum where competitor information was inappropriately shared.

**The discipline**: monitor outputs do not contain competitor commercial information that wouldn't already be in the public record. **Receiving Claude instruction**: do not include confidential competitor information from external counsel briefings, internal commercial intelligence, or OpCo-level strategic information in finding MDs; if such information is genuinely necessary to the finding, mark the finding privileged and route to Anne-Claire and Group GC only, not into the standard distribution.

### Layer 4 — Cross-monitor confidentiality coordination

Monitor 01 findings may reference competition matters and vice versa under Rule 21 (cross-monitor rank rule). Where a cross-referenced finding touches privileged or leniency-sensitive material, the cross-reference is redacted in the secondary monitor — the index entry reads "see Monitor 02 finding [date]" with the title omitted and access controlled.

**Receiving Claude instruction**: default-redact cross-references involving live competition matters rather than default-include.

### Distribution scope

- Standard finding MDs flow to Anne-Claire, Group GC, and the named recipients in the escalation chain.
- Monthly digest flows to Group GC + OpCo GCs + ExCo (as recipient).
- Quarterly summary flows to Board risk committee.
- Privileged findings flow only to Anne-Claire and Group GC.
- Leniency-sensitive findings flow only to Anne-Claire.
- Findings touching trade-association participation flow to Anne-Claire and the relevant OpCo legal team for protocol review before any wider distribution.

### A note on retention and audit trail

Competition matters can produce regulator information requests years after the underlying event. The monitor's findings, indexes, briefs, and digests are part of Prosus's internal documentary record and should be retained on the same schedule as other legal-function intelligence outputs — but with the same privilege protections that govern other competition-function documents.

**Receiving Claude instruction**: do not draft any finding in a way that would create unnecessary discoverable record beyond what the substantive analysis requires. Use Anne-Claire's confidence-flagging discipline (the persona's instinct, well-rehearsed from Booking and KPN) as the editorial threshold.

## Flags for Anne-Claire's sign-off

Three items materially shape how the monitor runs and warrant explicit confirmation before going live.

1. **Cadence asymmetry across the four domains** (daily for merger, twice-weekly for antitrust and abuse, weekly for digital markets) is a deliberate operational tuning, not a hierarchy of importance. If Anne-Claire prefers a uniform twice-weekly cadence across all four with merger getting its own intra-day push channel for deal-clock events, that's defensible — it's a matter of operational preference rather than substance. The default reflects the live-deal-flow context (Prosus is actively acquisitive and disposing through 2027) and the Delivery Hero monitoring obligation.

2. **Confidentiality framing is materially heavier than Monitor 01's.** Worth explicit Anne-Claire sign-off because the four layers (privilege, leniency, information-exchange, cross-monitor coordination) shape how the receiving Claude *drafts* findings, not just how findings are distributed. Drafting with privilege in mind affects voice, attribution, and what gets included; getting that wrong creates discoverable record.

3. **Rule 21 (Monitor 01 / Monitor 02 cross-reference)** is the first rule that explicitly spans both monitors. Worth confirming that Monitor 01's `ranking-criteria.md` is updated symmetrically — adding the same rule from the Monitor 01 side — so the cross-reference behaviour is symmetric. The CMA AI Foundation Models work is the immediate test case; that's primary Monitor 01 with secondary Monitor 02, and both monitors need to file it consistently.
