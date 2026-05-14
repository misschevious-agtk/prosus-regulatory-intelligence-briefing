# Portfolio Map

Per-operating-company reality. The shared map across all four Monitor 01 personas — so AI News, Privacy, IP, and Legal Ops are reading against the same exposure base.

> **Why this file exists:** Monitor 01's regulator landscape is 5–10× larger than Monitor 02's. More DPAs, more national IP offices, more state-level AI laws, more bar associations, more standards bodies, more sub-regulator guidance documents. Without a portfolio map, each persona will independently chase items that turn out not to touch a real Prosus exposure. The map lets each persona quickly determine whether a finding actually attaches to an operating company or just exists in jurisdiction-space.

For each entity below: legal status, primary regulator(s), data-processing footprint, named AI systems, IP exposure, bar/ethics jurisdiction for in-house counsel.

---

## Controlled operating companies

### iFood
- **Status:** Wholly-owned (since 2022). Brazil-headquartered.
- **Primary regulators:** ANPD (privacy); CADE (competition — Monitor 02); ANATEL (telecom-adjacent); MAPA / ANVISA (food + pharma delivery); STF/STJ for platform liability rulings; **Brazilian labour courts on gig couriers**.
- **Data-processing footprint:** ~80M users in Brazil; pharma delivery line processes health-adjacent data.
- **Named AI systems:** **LCM** (originated here); **Ailo** (WhatsApp assistant); restaurant matching; courier dispatch; pricing recommender; food/pharma recommender.
- **IP exposure:** LCM training corpus; vendor indemnity reliance on Anthropic, OpenAI, AWS; Qwen open-source licence compliance (LCM foundation).
- **In-house bar/ethics jurisdiction:** OAB (São Paulo, federal).
- **Monitor 01 attention:** **Highest.** Touches every domain. Sectoral overlays: food, pharma, employment (gig couriers), online intermediaries, advertising.

### OLX Group
- **Status:** Wholly-owned global classifieds group. Multiple operating entities.
- **Components:** OLX Brasil, OLX Polska, OLX in MENA / India (via dubizzle/EMPG stake), **La Centrale (France, recent acquisition)**, **Property24 (South Africa)**, **Storia (Romania)**, **Imovirtual (Portugal)**, OLX Motors verticals.
- **Primary regulators:** national DPAs in each market (notably AP NL, AEPD Spain, CNIL France, ANPD Brazil, AEPD); EU Commission for DSA; **Ofcom in UK** if exceeds OSA thresholds; HUD-equivalent fair-housing regulators in Property24-relevant markets; competition authorities (Monitor 02).
- **Data-processing footprint:** broad EU + LatAm + MENA + SA; significant listings of housing, vehicles, jobs (all touched by algorithmic-discrimination rules).
- **Named AI systems:** **OLX Magic** (multi-modal conversational shopping); LCM-trained recommender; image-search; URL parser; trust & safety AI.
- **IP exposure:** trade marks across all sub-brands; UGC moderation IP; vendor indemnities.
- **In-house bar/ethics jurisdiction:** mixed — primary teams in Netherlands (NOvA), Brazil (OAB), Poland, Portugal, South Africa, plus US for stakes.
- **Monitor 01 attention:** **High.** Direct DSA addressee; fair-housing exposure via Property24; recommender exposure across all verticals.

### PayU (controlled where retained)
- **Status:** PayU Global Payments Organisation (GPO) partially divested to Rapyd March 2025; **PayU India** retained as the core remaining controlled entity (payments + NBFC consumer lending via LazyPay, PaySense).
- **Primary regulators:** RBI (India) — payment systems, payment aggregators, NBFC lending, **AI/ML governance circulars**; BDDK (Turkey for **PayU Turkey**); national regulators where PayU is retained.
- **Data-processing footprint:** Indian payments at scale; lending decisions; KYC.
- **Named AI systems:** fraud detection; underwriting models; KYC automation; chatbots; recommender for upsell/cross-sell.
- **IP exposure:** payments-tech patents; vendor indemnities; lending-model IP.
- **In-house bar/ethics jurisdiction:** Bar Council of India.
- **Monitor 01 attention:** **High.** Triggers Rule 7 (sectoral upgrade) on financial-services and consumer-credit overlays automatically.

### iyzico
- **Status:** Turkish payment institution, wholly owned.
- **Primary regulators:** **BDDK**; KVKK (privacy).
- **Data-processing footprint:** Turkish merchants and consumers.
- **Named AI systems:** fraud detection; merchant risk; KYC/AML automation.
- **IP exposure:** payments tech; vendor indemnities.
- **In-house bar/ethics jurisdiction:** Turkish bar.
- **Monitor 01 attention:** **Medium-high.** Financial-services sectoral overlay; KVKK is an active DPA.

### Despegar/Decolar
- **Status:** Controlled Latam OTA (Argentina-headquartered, listed).
- **Primary regulators:** PROCON Brazil; DNDC Argentina; PROFECO Mexico; SIC Colombia; CNIL (some EU consumer touchpoints); aviation regulators (ANAC Brazil etc.).
- **Data-processing footprint:** Latin America-wide; travel + payment data.
- **Named AI systems:** personalised pricing; dynamic packaging; LCM-trained recommender; chat/search.
- **IP exposure:** booking-engine IP; vendor indemnities.
- **In-house bar/ethics jurisdiction:** Argentine bar primary; Brazilian OAB for Decolar.
- **Monitor 01 attention:** **Medium.** Personalised-pricing and dark-patterns are the hot edges.

### eMAG
- **Status:** Controlled CEE e-tailer (Romania-headquartered; also BG, HU).
- **Primary regulators:** ANSPDCP Romania; UODO Poland (where present); CPC Bulgaria.
- **Data-processing footprint:** RO + BG + HU.
- **Named AI systems:** marketplace recommender; LCM-trained search/ranking.
- **IP exposure:** marketplace trade marks; vendor indemnities.
- **In-house bar/ethics jurisdiction:** Romanian bar.
- **Monitor 01 attention:** **Medium.** DSA addressee; NIS2 important-entity candidate.

### Just Eat Takeaway (JET)
- **Status:** Controlled following 2024 transaction; operating subsidiaries across Europe, Canada (SkipTheDishes), Israel, Australia/NZ etc.
- **Primary regulators:** local DPAs in each market; Ofcom UK; OAIC AU; **Ireland DPC** as one-stop-shop touchpoint; labour courts (gig riders).
- **Data-processing footprint:** broad EU + Canada + Israel + AU/NZ + UK.
- **Named AI systems:** matching; dispatch; pricing; LCM-trained recommender; rider-ranking algorithms (EU Platform Work Directive scope).
- **IP exposure:** trade marks across sub-brands (Lieferando, Pyszne, etc.); vendor indemnities.
- **In-house bar/ethics jurisdiction:** mixed — Netherlands primary; UK SRA; Canada provincial; AU Law Society.
- **Monitor 01 attention:** **High.** Platform Work Directive sectoral overlay is Rule 7 trigger; recommender exposure broad.

### Stack Overflow
- **Status:** Wholly-owned (since 2021). US-headquartered with EU presence.
- **Primary regulators:** US FTC, state AGs, CPPA California; ICO UK; AP NL; **US Copyright Office and federal courts** on AI training data (the load-bearing IP forum).
- **Data-processing footprint:** global Q&A users; enterprise customers.
- **Named AI systems:** AI search; Q&A assistance; enterprise AI deployments; **content licensing API to model providers** (Anthropic, Google, OpenAI deals).
- **IP exposure:** **central to AI training-data litigation**. Q&A corpus is uniquely valuable inbound IP; licensing deals are outbound IP. **Watch Bartz v Anthropic precedent** explicitly.
- **In-house bar/ethics jurisdiction:** US state bars (primarily New York, California); UK SRA for European counsel.
- **Monitor 01 attention:** **Highest for IP domain.** Also material for AI News (frontier vendor relationships) and Privacy.

### GoodHabitz
- **Status:** Controlled corporate-training (acquired 2023). NL-headquartered.
- **Primary regulators:** AP NL; member-state DPAs.
- **Data-processing footprint:** enterprise customers across Europe.
- **Named AI systems:** AI-powered learning recommendations.
- **IP exposure:** course IP; vendor indemnities.
- **In-house bar/ethics jurisdiction:** NOvA Netherlands.
- **Monitor 01 attention:** **Medium.** Minors exposure (some courses reach under-18); enterprise B2B AI deployment.

---

## Major stakes (not controlled, but functionally `our_stack` for ranking)

### Tencent (~23% stake)
- **Status:** Equity stake; >90% of group NAV.
- **Primary regulators:** **CAC, MIIT, MPS, SAMR** (China); **State Council Information Office**; SFC Hong Kong; HKEX disclosure rules.
- **Data-processing footprint:** WeChat, gaming, cloud — at the platform scale that triggers PIPL's external-oversight obligations.
- **Named AI systems:** **Hunyuan** foundation model; gaming AI; WeChat AI integration; Tencent Cloud AI.
- **IP exposure:** Tencent is among the **world's most active AI patent filers**.
- **In-house bar/ethics jurisdiction:** ACLA China.
- **Monitor 01 attention:** **Highest after iFood.** Treated as if a Prosus operating company per Rule 6 (Tencent-attribution).

### Swiggy (~25% stake)
- **Status:** Listed Indian food + quick-commerce platform (IPO November 2024).
- **Primary regulators:** **RBI** (Instamart payments), CCI (Monitor 02), MeitY / DPDP regime, **Indian labour courts on gig delivery partners**, **PharmEasy partnership extends to health-data overlays via Instamart**.
- **Named AI systems:** Instamart matching; restaurant ranking; dispatch.
- **Monitor 01 attention:** **High.** Indian DPDP + gig-labour overlay.

### Remitly (~12% stake)
- **Status:** Listed US money-transmitter.
- **Primary regulators:** FinCEN; US state regulators; CFPB; UK FCA; equivalent regulators in receiving markets.
- **Monitor 01 attention:** **Medium.** Financial-services sectoral overlay.

### Delivery Hero (stake, partial; Berlin-listed)
- **Status:** Equity stake.
- **Primary regulators:** BfDI; member-state DPAs; EU Commission for DSA/AI Act.
- **Named AI systems:** matching; pricing; recommender.
- **Monitor 01 attention:** **Medium.** Tracks alongside JET for sector-level developments.

### EMPG / dubizzle (significant minority)
- **Status:** MENA classifieds + property.
- **Primary regulators:** UAE Data Office; SDAIA (KSA); Egyptian DPA; Pakistan PDP (in development).
- **Monitor 01 attention:** **Medium.** MENA regulatory environment is rapidly forming.

### Edtech stakes — Brainly, Udemy, GoStudent, Eruditus, BYJU's, Platzi, Codecademy, SoloLearn, Skillsoft
- **Status:** Minority stakes (varying sizes; BYJU's value materially impaired per group disclosures).
- **Monitor 01 attention:** **Medium.** Sectoral exposure to **minors** (Rule 7 trigger). Bargain candidates for disposals per Prosus's stated $2bn+ disposal strategy.

### Travel and other stakes — MakeMyTrip, Trip.com (legacy), etc.
- Lower-priority for Monitor 01 unless personalisation/dark-patterns/AI-pricing developments name them or the host jurisdiction.

---

## Ventures portfolio — 30+ AI-native startups

Including **Advolve.AI** (acquired by iFood 2025), **Arivihan**, and broader Prosus Ventures AI book.

- Events affecting any Ventures AI portfolio company trigger:
  - **Group-level disclosure obligations** (if material).
  - **AI-news persona attention** (intelligence, not consumption-stack exposure).
  - **IP persona attention** if the venture's IP intersects Prosus operating-company IP.

---

## Operating-company × domain attention matrix

Quick reference. `H` = high-attention for this domain; `M` = medium; `L` = low; `—` = out-of-scope.

| Entity                  | AI News | Privacy | IP | Legal Ops |
|-------------------------|:-------:|:-------:|:--:|:---------:|
| **iFood**               | H       | H       | H  | M         |
| **OLX Group**           | H       | H       | M  | M         |
| **PayU**                | H       | H       | M  | M         |
| **iyzico**              | M       | H       | L  | L         |
| **Despegar**            | M       | M       | L  | L         |
| **eMAG**                | M       | H       | L  | L         |
| **JET**                 | H       | H       | M  | M         |
| **Stack Overflow**      | H       | M       | **H** | M     |
| **GoodHabitz**          | M       | M       | L  | M         |
| **Tencent (NAV)**       | **H**   | **H**   | **H** | L     |
| **Swiggy**              | M       | H       | L  | L         |
| **Remitly**             | M       | M       | L  | L         |
| **Delivery Hero**       | M       | M       | L  | L         |
| **EMPG/dubizzle**       | M       | M       | L  | L         |
| **Edtech stakes**       | M       | M       | L  | L         |
| **Ventures AI book**    | M       | L       | M  | L         |

---

## Group function — Prosus N.V. itself

- **Regulators:** AP NL (lead); AFM (financial-markets disclosure); JSE (secondary listing in Johannesburg); EU Commission (group-level for some instruments).
- **Internal stakeholders:**
  - **Group AI team** + **AI and ethics working group** (named in the Responsible AI Policy as the implementation engine and the primary upstream reader of Monitor 01 findings).
  - **Group Legal & Public Policy** (operating owner of Monitor 01).
  - **Privacy office** — `privacy@prosus.com` is the published external channel for AI-policy queries.
  - **Risk committee of the Prosus board** — reviews the Responsible AI Policy annually; receives escalations on Rank A findings affecting group-level disclosure.
  - **CLO / CEO** — escalation chain for landmark items.
- **In-house bar/ethics jurisdiction:** NOvA (Netherlands) primary; multiple other bars for sub-team counsel.

---

## Change log

| Date       | Change                                                                                | Author   |
|------------|---------------------------------------------------------------------------------------|----------|
| 2026-05-12 | Initial portfolio map. Controlled OCs, stakes, ventures, group function. Attention matrix added. | Operator + agent synthesis |
