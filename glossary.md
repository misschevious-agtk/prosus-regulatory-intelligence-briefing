# Glossary

A single source of truth for the domain language used across this briefing system. Definitions are deliberately short and operator-focused — what the term *does* for the briefing, not the textbook entry. New monitors and external counsel should read this before reading the per-monitor specs.

Entries are alphabetical within sections. When a term is contested or jurisdiction-specific, the entry says so.

---

## Architecture and process terms

**Anchor (named anchor)** — A specific senior counsel a monitor is built to serve, e.g. Anne-Claire Hoyng for Monitor 02. A multi-persona monitor with a single named anchor reads the world through that person's four (or however many) doctrinal lenses rather than four independent personas.

**Block 1 / Block 2 / Block 3** — The three operator-completed initialisation sections inside every monitor's `SYSTEM-PROMPT.md`. Block 1 is markets and stack, Block 2 is persona profiles and needs, Block 3 is operational cadences and domain-specific rank rules. A monitor is not live until all three are signed off.

**Candidate** — Output of the source-scan stage. A markdown file with frontmatter and a raw teaser, written to `findings/candidates/YYYY-MM-DD/monitor/domain/`. Not yet a finding — the persona has not interrogated it.

**Cold start** — The first 14 days of a new monitor's life. Behaviour is more conservative, feedback is captured more aggressively, and the operator reviews every Rank A item. See `cold-start-protocol.md`.

**Cross-reference (cross-monitor)** — When a single source item is caught by two monitors, the primary monitor surfaces the full card and the other monitor includes a one-line link. See `strategy.md` for the dedup rule and Rule 21 (M02) / Rule 22 (M01) for the cross-monitor ranking carve-out.

**Domain** — A sub-area of a multi-persona monitor. M01 has four (AI News, Privacy, IP, Legal Ops); M02 has four (Antitrust & Cartels, Abuse of Dominance, Merger Control & FDI, Digital Markets, Sector Regulation & State Aid). Each domain has its own `profile.md`, `needs.md`, `interrogation-checklist.md`, `keywords.md`.

**Feedback Log** — Per-monitor record of 👍/👎 reactions, free-text annotations, and persona drift notes. The moat: a monitor that has been running for six months is materially better than one starting from scratch. Lives in each domain's `findings/` folder.

**Finding** — A persona-interrogated item produced in the shape defined by `output-schema.md`. Always has a verbatim anchor quote. One MD file per finding.

**Locked filter** — A system-wide filter (Section 6 of every monitor) that cannot be overridden by feedback, persona, or agent. Listed in `strategy.md`. Eight currently active.

**Operating company / OpCo / OC** — A Prosus investee or operating subsidiary (iFood, OLX, PayU, etc.). The `our_markets.md` and `portfolio-map.md` files name them per monitor.

**Persona** — The reading mode the agent assumes. Defined by `profile.md` (who they are), `needs.md` (what they need to be told), `interrogation-checklist.md` (how they interrogate every candidate). One persona per domain.

**Prosus Relevance Filter** — The single most important filter. An item is Prosus-relevant if it names a Prosus entity, names a portfolio company, falls in a Prosus operating market, implicates a Prosus investment thesis, or sets a horizontal precedent likely to apply to a Prosus business within 12 months. Each monitor sets its strictness — tight, medium, or loose. Defined in `README.md`.

**Ranker / Tier-2** — The mechanical rank application step. Reads only enumerated fields from finding frontmatter, never prose. Applies Rules 1–21 (or 1–22 in M01) and produces A/B/C/D. Source of consistency, not coverage.

**Source tier (1 / 2 / 3)** — Tier 1 is official register (regulators, courts, parliaments); Tier 2 is reputable wire / specialist (Reuters Legal, Bloomberg Law, FT, Law360, MLex, Mint, Folha); Tier 3 is commentary / law-firm bulletins. Defined in `strategy.md`. Promotion between tiers requires owner sign-off.

**Tier A / B / C / D jurisdiction** — Operator-defined attention tiers in `our_markets.md`. Tier A is "directly named or operating", Tier D is "precedent only". Distinct from source tiers above.

**Trigger type** — The enumerated field in finding frontmatter that drives most rank rules. Pick it carefully; the ranker reads nothing else with the same weight.

---

## Competition law — instruments and procedures

**Article 22 EUMR referral** — Mechanism allowing Member States or the Commission to call in transactions below thresholds. Used for "killer acquisitions" in digital markets. Tracked under Rule 16.

**Article 101 / 102 TFEU** — EU prohibitions on anti-competitive agreements (101) and abuse of dominance (102). The substantive backbone of EU competition law.

**Below-threshold call-in** — Any mechanism by which an authority asserts jurisdiction over a deal that does not meet statutory notification thresholds. Includes Article 22 EUMR, CMA discretionary call-in, BKartA §39a, AGCM call-in, CADE adverse AC. Treated as deal-relevant intelligence under Rule 16 (M02).

**Cartel / cartelisation** — Horizontal coordination (price-fixing, market-sharing, bid-rigging, output restriction). Investigated by Article 101 in the EU, equivalent national instruments elsewhere.

**Commitment decision (Article 9)** — EU Commission decision under Article 9 of Regulation 1/2003 that makes commitments offered by the undertaking binding. Closes the case without an infringement finding.

**Conseil d'État** — France's supreme administrative court. Reviews administrative decisions including those of the French competition authority and digital regulators (Arcom, CNIL on certain regulatory acts).

**Dawn raid** — Unannounced inspection by a competition authority (Article 20 of Regulation 1/2003 in the EU, equivalent NCA powers nationally). Indicator of the authority's working theory and the case's seriousness.

**DG COMP** — Directorate-General for Competition at the European Commission.

**EUMR (EU Merger Regulation)** — Regulation (EC) No 139/2004. Establishes the EU merger control regime, including notification thresholds and substantive review.

**FDI screening** — Foreign Direct Investment screening regimes (Regulation (EU) 2019/452 at EU level, national regimes implementing it, plus CFIUS in the US, NSI Act in the UK, etc.). Increasingly intersects with merger control.

**FSR (Foreign Subsidies Regulation)** — Regulation (EU) 2022/2560. Allows the EU Commission to investigate distortive foreign subsidies in M&A, public procurement, and ex officio. New regime; every decision is precedent. Rule 19 (M02) treats prohibition or precedent-setting commitments as auto-rank.

**General Court / CJEU** — The General Court is the EU's first-instance court for direct actions against EU institutions including competition decisions. The Court of Justice of the EU (CJEU) hears appeals on points of law and is the highest EU court. Grand Chamber rulings carry the most weight.

**Leniency / leniency-track** — Programme allowing cartel participants to receive immunity (Type 1A) or reduced fines (Type 1B/2) in exchange for cooperation. Highly confidential — leniency-track content must be excluded from this briefing system by the confidentiality pre-filter.

**MFN (Most-Favoured-Nation) / parity clause** — Contract clause requiring one party to offer terms at least as favourable as those offered to others. Wide MFN (across all channels) and narrow MFN (own direct channel only) are treated differently by enforcers. Doctrinally fragmented across Tier A jurisdictions. Rule 10 (M02) auto-ranks any binding doctrinal shift.

**NCA (National Competition Authority)** — Generic term for a Member State or third-country competition agency. Examples: BKartA (Germany), CMA (UK), AdC (Portugal), AGCM (Italy), ACM (Netherlands), CADE (Brazil), CCI (India), COFECE (Mexico), SACC (South Africa), SAMR (China).

**Phase I / Phase II merger review** — Phase I is the initial 25 working day review (EU); Phase II is the deeper 90 working day investigation triggered by competition concerns. Equivalent two-stage structures exist in most jurisdictions.

**SAMR** — State Administration for Market Regulation, China's competition authority. Most relevant to Prosus through its oversight of Tencent.

**SO (Statement of Objections)** — The Commission's formal preliminary charge document. Indicates the working theory of harm, not the final position.

**State aid** — Articles 107–109 TFEU regime governing aid granted by Member States. Relevant to Prosus where digital-services or platform rules implicate state-aid analysis.

**Suo motu** — "On its own initiative" (Latin). Used most often in the Indian context: a CCI suo motu investigation is one opened without a complaint.

**TCC (Termo de Compromisso de Cessação)** — Brazilian "cease-and-desist commitment", the Brazilian analogue of an EU commitment decision. The iFood TCC is monitored under Rule 11 (M02).

---

## Digital markets, sector regulation, AI Act

**Annex III (EU AI Act)** — The annex listing high-risk AI system use cases (employment, credit scoring, education access, etc.). Any expansion is Rank A under Rule 11 (M01).

**AI Act (EU)** — Regulation (EU) 2024/1689. Risk-tiered horizontal AI regulation. The GPAI obligations and high-risk obligations have different effective dates between 2025 and 2027.

**CMA SMS (Strategic Market Status) designation** — UK designation under the Digital Markets, Competition and Consumers Act 2024 (DMCC). Brings the firm under conduct requirements. UK analogue of DMA gatekeeper status.

**DMA (Digital Markets Act)** — Regulation (EU) 2022/1925. Imposes ex ante obligations on designated gatekeepers. Designation is auto-rank under Rule 18 (M02).

**DSA (Digital Services Act)** — Regulation (EU) 2022/2065. Layered obligations on intermediaries, with VLOPs and VLOSEs facing the heaviest set. VLOP/VLOSE designation is auto-rank under Rule 18 (M02).

**Gatekeeper** — A platform designated under the DMA. Designation triggers ex ante obligations. Prosus OpCos are mostly business users of gatekeepers, which still creates downstream-effect exposure.

**GPAI (General-Purpose AI) model** — An AI Act category. GPAI providers have specific transparency, copyright, and (for models with systemic risk) safety obligations. Compute threshold 10^25 FLOPs for systemic risk presumption.

**GPAI Code of Practice** — The voluntary code drawn up under Article 56 of the AI Act, designed to allow GPAI providers to demonstrate compliance with Chapter V obligations. Rule 11 (M01) treats material changes as Rank A.

**VLOP / VLOSE** — Very Large Online Platform / Very Large Online Search Engine under the DSA. Designated by user count (≥45m monthly active users in the EU). Subject to the heaviest DSA obligations.

---

## Privacy and data protection

**ADM (automated decision-making)** — Decisions taken solely by automated means. Article 22 GDPR and LGPD Article 20 establish rights against being subject to ADM. Rule 13 (M01) auto-ranks doctrinal expansions (recommender systems, dynamic pricing, gig-platform dispatch, AI credit decisioning).

**ANPD** — Brazil's data protection authority (Autoridade Nacional de Proteção de Dados).

**Article 22 GDPR / LGPD Article 20** — The right not to be subject to decisions based solely on automated processing that produce legal effects or similarly significant effects. The doctrinal centre of gravity for recommender systems and dynamic pricing.

**CNIL** — France's data protection authority.

**DPA (Data Protection Authority)** — Generic term for a national data protection regulator. Examples: ICO (UK), CNIL (France), AEPD (Spain), Garante (Italy), AP (Netherlands), ANPD (Brazil), DPDP Board (India, pending).

**DPDP (Digital Personal Data Protection Act)** — India's 2023 data protection law. Phased enforcement; rules under finalisation.

**DPF (EU–US Data Privacy Framework)** — The post-Schrems-II cross-border transfer mechanism. Fragility is auto-rank under Rule 14 (M01) because transfer-mechanism failure is a portfolio-wide operational problem.

**EDPB** — European Data Protection Board. Coordinates DPAs across the EEA; issues guidance and binding opinions.

**LGPD (Lei Geral de Proteção de Dados)** — Brazil's data protection law. Materially similar to GDPR.

**PII (Personally Identifiable Information)** — Personal data; the term is more US-coded but used loosely across the briefing.

**Schrems-style challenge** — Litigation modelled on Schrems I (2015) and Schrems II (2020), which invalidated successive EU–US transfer mechanisms (Safe Harbor, Privacy Shield). The DPF is the current target.

---

## Intellectual property

**Bombay HC / Delhi HC / N.D. Cal. / S.D.N.Y. / D. Del.** — Specific courts whose rulings on AI training-data copyright are auto-rank under Rule 15 (M01). The list is doctrinal centres of gravity, not exhaustive.

**Federal Circuit** — US Court of Appeals for the Federal Circuit; specialised appellate court for patents and certain federal-question matters.

**Indemnity (training-data / output-IP)** — Contractual protection by an AI vendor against IP claims arising from training data or model outputs. Anthropic, OpenAI, AWS terms vary materially. Narrowing is auto-rank under Rule 16 (M01).

**Tokyo District Court** — Specific court whose AI training-data rulings are auto-rank under Rule 15 (M01).

---

## Legal ops and matter management

**Deepfake at material scale** — Defined in Rule 17 (M01) as a deepfake or AI-impersonation campaign affecting Prosus brand/OpCo/named executive crossing one of: more than one platform, more than one jurisdiction, or evidence of organised activity.

**Panel firm** — An outside law firm on a Prosus relationship-managed panel. Court standing orders on AI use (Rule 19 M01) affect panel-firm operations on Prosus matters.

**Pilot-kill threshold** — A pre-agreed metric at which an AI legal-tech pilot is killed or promoted to production. Rule 20 (M01) auto-ranks crossings (in either direction) to force the function to confront the decision on schedule.

---

## Internal terms

**Anne-Claire** — Anne-Claire Hoyng, Global Head of Competition Policy, Prosus. Named anchor for Monitor 02.

**Group GC** — Group General Counsel. Default decision owner for multi-domain or cross-monitor escalations under Rules 20 (M02) and 21 (M01).

**LCM** — Prosus's internal language-and-content model. Sits in the M01 AI News, Privacy, and IP threat surfaces.

**OLX Magic / Ailo** — Specific OLX Group AI features. Sit on the self-preferencing / recommender-system-as-abuse doctrinal line tracked by Rule 12 (M02).

**NAV disclosure (Tencent)** — Net Asset Value disclosure of Prosus's Tencent stake. Drives the special attention given to Tencent under Rule 6 (M01) and Rule 13 (M02) despite Tencent not being a controlled portfolio company.

**Toqan** — Prosus's internal AI product line. Treated as a regulated artefact for Rule 7 / in-stack purposes.

---

## Change log

| Date       | Change                                                                                 | Author |
|------------|----------------------------------------------------------------------------------------|--------|
| 2026-05-14 | Initial glossary — architecture, competition, digital markets, privacy, IP, legal ops. | K. Maleevska (drafted with Claude) |
