# `our_markets`

The set of jurisdictions and commercial markets in scope for Monitor 01. Consumed by the ranker. Reviewed at least quarterly. Versioned changelog at the bottom so the ranker can reason about when a market entered or left scope.

> **Framing:** Prosus's perimeter is a tree, not a list. The parent is Dutch-listed and JSE-secondary-listed; the operating companies are local and the local regulator is who actually opens the file. So `our_markets` is the union of (a) where the holding entity sits, (b) where each operating company is regulated and sells, and (c) where regulators reach Prosus by extraterritorial operation of law.
>
> Flat lists make the ranker treat Brazil and Bulgaria as equal. They aren't. Hence the tiers below — calibrated for Monitor 01's four domains (AI, privacy/data protection, IP, legal ops). Note: **China sits in Tier A** because Tencent represents the dominant share of group NAV and is a directly regulated entity under all four Monitor 01 domains — financial and disclosure exposure is functionally equivalent to a controlled OpCo.

---

## Tier A — primary group-level regulators

Anything from these reaches Prosus or a controlled operating company directly, or affects Tencent. **Rank A material when severity ≥ 3, automatic Rank A when a Prosus company or Tencent is named.**

### European Union — dominant lens across all four domains

- **AI:** European Commission (DG CNECT, AI Office); European Artificial Intelligence Board; national market surveillance authorities under the AI Act; notified bodies for conformity assessment. EU AI Act obligations escalate through **2 August 2026** for high-risk systems.
- **Privacy & data protection:** European Data Protection Board (EDPB); European Data Protection Supervisor (EDPS); national DPAs of each member state; **lead supervisory authority for Prosus group entities is typically the Dutch DPA (Autoriteit Persoonsgegevens)** by virtue of Amsterdam headquartering and one-stop-shop cooperation.
- **IP:** EUIPO (trade marks and designs); European Patent Office (technically outside EU but governs European patents); Court of Justice of the EU; General Court; national IP courts.
- **Legal ops:** Council of Bars and Law Societies of Europe (CCBE) for cross-border professional rules; data protection rules touching e-discovery and LegalTech vendors; DSA/AI Act intersection with legal-function tooling.

### Netherlands — home jurisdiction

- AP (Autoriteit Persoonsgegevens) — privacy — **one of the more assertive DPAs and the likely lead authority for cross-border GDPR cases against the Prosus group**.
- Octrooicentrum Nederland (patents); Benelux Office for Intellectual Property (Benelux marks and designs).
- Rechtbank Den Haag (IP litigation); Hoge Raad (ultimate civil appeals).
- Dutch Bar Association (NOvA) — legal-ops professional-conduct rules for in-house counsel.

### United Kingdom — high-intensity, separate post-Brexit

- **AI:** no omnibus Act; operationalised through sectoral regulators — **ICO** (data), **CMA** (competition + digital markets), **Ofcom** (online safety), **FCA** (financial services); **AI Safety Institute** issues influential evaluations.
- **Privacy:** ICO; UK GDPR + Data Protection Act 2018 + **Data (Use and Access) Act 2025** reforms.
- **IP:** UKIPO; **High Court (Chancery Division)**, particularly **Patents Court** and **IPEC**; Court of Appeal; Supreme Court — UK is an active forum for AI copyright litigation, **including Getty v Stability AI**.
- **Legal ops:** SRA; Bar Standards Board — AI-in-legal-practice rules.

### China — primary jurisdiction for Tencent-related exposure

> Tencent ≈ 23% stake accounting for **over 90% of net asset value**. Tencent is a major frontier AI developer (Hunyuan, gaming AI, WeChat AI integration) regulated under the full stack.

- **AI:** CAC (lead AI/algorithm regulator); Interim Measures for Generative AI Services; Algorithm Recommendation regulations; MIIT (app and platform standards); MoST (foundational AI policy).
- **Privacy & data protection:** CAC (lead) with MIIT, MPS, SAMR concurrent jurisdiction; PIPL; DSL; CSL (revised, **effective 1 January 2026**); Cross-Border Data Transfer Measures (**effective 1 January 2026**). PIPL obligates large internet platforms to establish independent external oversight bodies — Tencent has done so.
- **IP:** CNIPA; Beijing/Shanghai/Guangzhou IP Courts; **Supreme People's Court IP Tribunal**. China is the most active jurisdiction globally for AI patent filings, including by Tencent.
- **Legal ops:** ACLA — less relevant for Prosus's own in-house function but relevant for Tencent's legal-function tooling decisions.

> **Scope note for the ranker:** China-jurisdiction items reach Rank A when they affect Tencent's compliance posture, valuation, operations, AI strategy, or governance disclosures — not when they merely affect Chinese tech generally. A CAC enforcement action naming Tencent is Rank A; CAC generative AI guidance is Rank A if Tencent is a designated large model provider under it; a Chinese privacy ruling against a smaller platform is Rank B precedent unless it sets a doctrine that will reach Tencent. See **Rule 6 (Tencent-attribution rule)** in `ranking-criteria.md`.

### Brazil — most operationally exposed Latam jurisdiction

- **AI:** PL 2338/2023 progressing toward enactment; ANPD coordinating with sector regulators.
- **Privacy:** ANPD — LGPD in active enforcement; **increasingly aggressive on dark patterns, ADM, and AI-related data uses**. iFood, OLX Brasil, Despegar/Decolar all process Brazilian personal data at scale.
- **IP:** INPI; federal courts for copyright and patent litigation.
- **Legal ops:** OAB — professional-conduct rules; increasingly debated topic of AI in legal practice.

### India — large operating footprint, fast-moving regulatory environment

- **AI:** MeitY advisories; Digital India Act in development; sectoral regulators (RBI fintech AI, SEBI markets).
- **Privacy:** DPDP Act (Digital Personal Data Protection Act 2023) **now in operational phase**; Data Protection Board of India being stood up.
- **IP:** Indian Patent Office (CGPDTM); **Delhi High Court and Bombay High Court** for IP litigation — Delhi HC is the active forum for AI copyright cases.
- **Legal ops:** Bar Council of India.

### United States — venture portfolio, Stack Overflow, precedent value

- **AI:** no federal AI law; FTC (deception, unfair practices, algorithmic discrimination); state laws — **California TFAIA (effective 1 January 2026)**, **Colorado AI Act (effective 30 June 2026)**, **Texas RAIGA**, **Illinois HB 3773**; recent federal Executive Order signalling preemption attempts.
- **Privacy:** FTC; state AGs; CPPA under CCPA/CPRA; the patchwork (VCDPA, CPA, CTDPA, UCPA and successors); sector regulators (HHS, CFPB).
- **IP:** USPTO; **US Copyright Office** (active on AI-training guidance and registration policy); federal district courts — **N.D. Cal., D. Del., S.D.N.Y.** for AI training-data and output litigation; **Federal Circuit** (patent appeals); **Ninth and Second Circuits** (copyright).
- **Legal ops:** ABA model rules; state bar associations — **AI-in-legal-practice ethics opinions are issued state-by-state**.

### South Africa — group-level disclosure jurisdiction via Naspers

- **Privacy:** Information Regulator under POPIA.
- **IP:** CIPC.
- **Legal ops:** Legal Practice Council.

---

## Tier B — significant national regulators with active Prosus operating companies

**Rank A when severity ≥ 4 OR a Prosus operating company is named; otherwise Rank B.**

- **Germany** — BfDI (federal DPA) and 16 Länder DPAs (notably LfDI Baden-Württemberg, BlnBDI Berlin, HmbBfDI Hamburg — historically the most assertive on tech); DPMA for IP; JET via Lieferando is a leading operator; German DPAs are influential on platform-data practices.
- **Poland** — UODO (privacy); Patent Office of Poland; OLX Poland is market-leading classifieds; JET operates as Pyszne.pl.
- **Romania** — ANSPDCP (privacy); OSIM (IP); eMAG is the leading e-tailer; Storia leads classifieds.
- **Italy** — Garante per la protezione dei dati personali (**one of the most aggressive DPAs in Europe — the ChatGPT precedent originated here**); UIBM (IP); JET via Just Eat Italy.
- **Spain** — AEPD (**highly assertive on consent and dark patterns**); OEPM (IP); JET via Just Eat Spain.
- **Ireland** — DPC — **critical because Ireland is the EU lead supervisory authority for many US tech platforms whose terms Prosus companies rely on**; JET operates in Ireland; DPC is the de facto gatekeeper for many large GDPR investigations.
- **France** — CNIL (**extremely active on AI training data, biometrics, ADM**); INPI (IP); Paris courts are an active forum for AI-IP litigation; JET exited France but OLX Group now owns **La Centrale**, so France is squarely on the map for OLX/auto-classifieds.
- **Belgium, Austria, Switzerland, Portugal, Bulgaria, Luxembourg, Slovakia, Israel** — JET operating jurisdictions; respective DPAs and IP offices; **Austria's DPA and noyb-driven complaints make Austria punch above its size on privacy**.
- **Mexico, Argentina, Colombia, Chile, Peru, Ecuador, Uruguay** — Despegar and OLX Latam footprint; **INAI (Mexico), AAIP (Argentina), SIC (Colombia)** main privacy authorities; respective IP offices.
- **Turkey** — KVKK (privacy); Turkish Patent and Trademark Office; iyzico and PayU Turkey.
- **UAE / Saudi Arabia / Egypt / Pakistan** — EMPG/dubizzle stake; **UAE Data Office, SDAIA in KSA, Egyptian DPA in formation**.
- **Canada** — OPC under PIPEDA and forthcoming CPPA; CIPO (IP); provincial regulators — **Québec's CAI notably assertive under Law 25**; JET via SkipTheDishes.

---

## Tier C — observer jurisdictions

**Rank B at most unless severity ≥ 4 AND a specific Prosus exposure is named.**

- **Singapore** — PDPC; IPOS; influential AI Verify framework; venture exposure.
- **Hong Kong** — PCPD.
- **Japan** — PPC; JPO; AI Strategy Council.
- **South Korea** — PIPC; KIPO; active on platform regulation.
- **Australia / New Zealand** — OAIC; IP Australia; Privacy Act reforms in train.
- **Czech Republic, Greece, Norway, Finland, Denmark** — JET-adjacent (past or upcoming entries); respective DPAs and IP offices.

---

## Tier D — precedent-only jurisdictions

**Rank C at most.** Read for theory spillover, not direct legal exposure. Reserved for jurisdictions producing meaningful AI/privacy/IP precedent that does not reach Prosus or Tencent directly — e.g. specific US state-level rulings without doctrinal reach, niche national IP courts in markets where Prosus has no footprint. **China is not in this tier for Monitor 01 (see Tier A).**

---

## Commissions and Courts — named institutions to monitor

Country-tiering doesn't surface the institutions that actually produce signal. Monitor 01 personas should track named institutions, not just countries.

### Cross-border bodies and commissions
- European Commission (DG CNECT, DG JUST, AI Office)
- European Data Protection Board (EDPB) — guidelines and binding decisions
- European Data Protection Supervisor (EDPS) — opinions
- Council of Europe — Framework Convention on AI
- OECD AI Policy Observatory
- WIPO — AI and IP standard-setting
- UNESCO AI ethics
- G7 Hiroshima Process; GPAI

### EU courts
- Court of Justice of the European Union (CJEU) — Grand Chamber and Chambers
- General Court of the EU
- Advocates General opinions (signal value)

### National courts where AI / privacy / IP precedent is being set
- **Germany:** Bundesverfassungsgericht; Bundesgerichtshof
- **France:** Conseil d'État; Cour de cassation
- **UK:** Supreme Court; Court of Appeal; High Court (Chancery)
- **US:** Supreme Court; Federal Circuit; Ninth and Second Circuits; district courts of N.D. Cal., D. Del., S.D.N.Y.
- **Brazil:** STF; STJ
- **India:** Delhi High Court; Bombay High Court; Supreme Court of India
- **Netherlands:** Hoge Raad
- **China:** Beijing, Shanghai, Guangzhou IP Courts; Supreme People's Court IP Tribunal

### Specific commissions / inquiries — standing alerts
- US Copyright Office's ongoing AI inquiry and registration guidance
- USPTO AI inventorship guidance and proceedings
- UK CMA's AI Foundation Models work (competition itself is Monitor 02, but the CMA's AI work overlaps into platform and data policy that Monitor 01 should track)
- ICO AI guidance and audit reports
- CNIL's AI Action Plan and recommendations
- ANPD Brazil's regulatory sandboxes and AI consultations
- Indian MeitY consultations on AI and the Digital India Act
- EDPB AI-related opinions (Art. 64(2) on generative AI and ADM)
- EU AI Office Codes of Practice
- CAC's generative AI service registrations and algorithm filings (Tencent-relevant)
- Bar association ethics opinions on AI in legal practice (multi-jurisdictional)

---

## Commercial markets — where Prosus companies process data, generate/use IP, deploy AI

For Monitor 01 the commercial market matters because **extraterritorial reach is the norm, not the exception**. GDPR reaches anywhere a user sits; the EU AI Act reaches anywhere a system is placed on the EU market or its output is used in the EU; copyright is jurisdictional but training data and infringement claims travel.

- **EEA (all 30 countries)** — extraterritorial GDPR and AI Act reach.
- **United Kingdom** — UK GDPR and forthcoming AI rules.
- **Brazil and Latin America** — LGPD across Brazil; sectoral data laws in Argentina (Ley 25.326 and forthcoming reform), Colombia, Chile, Mexico.
- **India and South Asia** — DPDP Act in operational phase.
- **MENA** — UAE PDPL, KSA PDPL, Egyptian PDP, Pakistan PDP draft.
- **Sub-Saharan Africa** — POPIA in South Africa, Nigeria NDPA, Kenya DPA.
- **US and Canada** — patchwork.
- **Turkey** — KVKK.
- **Israel** — Privacy Protection Authority.
- **Australia / New Zealand** — OAIC; NZ Privacy Act.
- **Singapore, Hong Kong, Japan, South Korea, Taiwan** — venture exposure and Stack Overflow user base.
- **Greater China (WeChat and Tencent platforms)** — for group-level disclosures and AI/IP intelligence flowing through to Prosus's most valuable asset.

---

## Living document

Prosus has explicitly signalled **>$2bn in asset disposals in 2026 and continued sales in 2027**, plus ongoing acquisitive activity. Treat `our_markets` as a living MD updated at least quarterly with a versioned changelog so the ranker can reason about when a market entered or left scope.

---

## Change log

| Date       | Change                                                                                                   | Author   |
|------------|----------------------------------------------------------------------------------------------------------|----------|
| 2026-05-12 | Initial tier framework — Tier A (8 jurisdictions inc. China), Tier B (broad), Tier C (observer), Tier D (precedent-only). Named institutions enumerated. Commercial markets enumerated. | Operator |
