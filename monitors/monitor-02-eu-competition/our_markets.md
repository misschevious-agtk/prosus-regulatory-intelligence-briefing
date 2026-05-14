# `our_markets`

> **[DRAFT — confirm with operator (Anne-Claire); Block 1 Question 2 redline]**

The set of jurisdictions and competition authorities in scope for Monitor 02. Consumed by the ranker. Reviewed at least quarterly. Versioned changelog at the bottom so the ranker can reason about when a market entered or left scope.

> **Framing:** Prosus's competition perimeter is shaped by two facts the Monitor 01 perimeter does not have. First, the relevant authority set is the competition-authority subset of Monitor 01's authorities — DG COMP, CJEU/General Court, national NCAs, plus US DOJ/FTC, CADE, CCI, SAMR, SACC — not the broader DPAs or AI regulators. Second, the tier hierarchy is calibrated for competition exposure specifically: where Prosus or an OpC holds plausibly dominant market position, where deal-flow filings happen, where the dawn-raid pattern matters most.
>
> Two open Block 1 questions affect the tiering and need Anne-Claire's redline before this file is locked: (a) the dominance map (which OpCos are plausibly dominant in which product/geographic markets), and (b) the Naspers/SACC attribution rule (whether Prosus and Naspers are a single undertaking for South African Competition Commission purposes — if yes, ZA is Tier A; if no, ZA drops to Tier B).

---

## Tier A — primary group-level competition authorities

Anything from these reaches Prosus or a controlled operating company directly, or affects Tencent. **Rank A material when severity ≥ 3, automatic Rank A when a Prosus company or Tencent is named per ranking-criteria.md Rules 9–19.**

### European Union — dominant lens across all four Monitor 02 domains

- **DG COMP** — Articles 101/102, EUMR, FSR, state aid.
- **DG CONNECT** — DMA enforcement.
- **European Commission** — DSA enforcement.
- **CJEU and General Court** — judicial layer.
- **European Competition Network (ECN)** — cross-NCA coordination signal.

### Netherlands — home jurisdiction

- **ACM (Autoriteit Consument & Markt)** — Anne-Claire's first regulator. Also the host for the March 2026 Competition Law & Resilience event.

### United Kingdom — high-intensity, post-Brexit, distinct

- **CMA** — including DMU/SMS regime, AI Foundation Models work, NSI Act for FDI, market investigations.
- **CAT (Competition Appeal Tribunal)** — appellate layer.

### Brazil — most operationally exposed Latam jurisdiction, active food-delivery regulator

- **CADE** — particularly active food-delivery regulator; the iFood TCC (Termo de Compromisso de Cessação) closed in 2023 is a live ongoing commitment.

### India — large operating footprint, fast-moving regulatory environment

- **CCI (Competition Commission of India)** — active digital markets regulator with ex-ante platform rules under debate; PharmEasy e-pharmacy delivery exposure live.

### South Africa — group-level disclosure jurisdiction via Naspers

> **Open question for Anne-Claire**: whether Prosus and Naspers are treated as a single undertaking for SACC purposes. If yes, ZA is Tier A and Naspers-level conduct comes inside Monitor 02 scope. If no, ZA drops to Tier B and Naspers-level conduct is out of scope.

- **South Africa Competition Commission** and **Competition Tribunal** — Property24 market-leader exposure plus Naspers structural connection.

### China — primary jurisdiction for Tencent-related competition exposure

> Tencent ≈ 23% stake; over 90% of net asset value. SAMR competition wing actions read through to Prosus per **Rule 13 (Tencent SAMR auto-upgrade)** in `ranking-criteria.md`.

- **SAMR competition wing** — anti-monopoly enforcement against Tencent's gaming, music, fintech, super-app conduct.

### United States — venture portfolio, Stack Overflow, precedent value

- **DOJ Antitrust Division** and **FTC** — Sherman §1 / §2 precedent; particularly relevant for ecosystem theories, killer acquisitions, and digital-markets enforcement that travels.

---

## Tier B — significant national competition authorities with active Prosus operating companies

**Rank A when severity ≥ 4 OR a Prosus operating company is named (per Rule 17 — comparable-deal precedent in our sectors); otherwise Rank B.**

- **Germany** — **Bundeskartellamt** (GWB §19a designation regime, §39a transaction-value threshold, active digital-markets regulator). Lieferando market position. Anne-Claire's particular attention to GWB §19a watching brief.
- **France** — **Autorité de la concurrence** (active on platform regulation, La Centrale post-acquisition).
- **Italy** — **AGCM** (particularly aggressive on platform conduct, Just Eat Italy exposure, hyperscaler T&Cs work).
- **Spain** — **CNMC** (Just Eat Spain).
- **Poland** — **UOKiK** (OLX Poland market leader, Pyszne.pl).
- **Romania** — **Competition Council** (eMAG market leader, Storia).
- **Ireland** — **CCPC** (JET Ireland).
- **Austria** — **BWB** (transaction-value threshold for mergers).
- **Belgium** — **BMA**.
- **Portugal** — **AdC** (Imovirtual).
- **Switzerland** — **COMCO** (Booking parity-clause comparator jurisdiction for Anne-Claire's depth).
- **Mexico** — **COFECE** (OLX Mexico, PayU footprint).
- **Argentina** — **CNDC** (Despegar home market, OLX Argentina).
- **Turkey** — **Rekabet Kurumu** (iyzico, PayU Turkey).
- **UAE** — competition regulator at MoEC (EMPG/dubizzle).
- **Canada** — **Competition Bureau** (SkipTheDishes).

---

## Tier C — observer jurisdictions

**Rank B at most unless severity ≥ 4 AND a specific Prosus exposure is named.**

- **Singapore** — CCCS; venture exposure.
- **Hong Kong** — Competition Commission.
- **Israel** — Israel Competition Authority (JET Israel).
- **Australia, New Zealand** — ACCC, ComCom (JET Australia / NZ, exited but precedent relevant).
- **Bulgaria, Hungary, Slovakia, Czech Republic** — eMAG and other CEE OpC footprints; competition authorities lower priority than national NCAs above but tracked.
- **Egypt, Pakistan, Saudi Arabia** — EMPG/dubizzle and PayU footprint; competition regulators in formation.

---

## Tier D — precedential value only

**Rank C at most; archive unless severity ≥ 4 AND novel doctrine.**

- All other jurisdictions. Surfaced only when a ruling or decision establishes doctrine portable to Tier A or Tier B (e.g. a Japan JFTC ruling on platform conduct that any Tier A authority could plausibly cite).

---

## International and multilateral fora

Not jurisdictions but read as primary signal for policy direction:

- **OECD Competition Committee** — Anne-Claire's policy-engagement lane; working papers and roundtable outputs are primary signal for academia-leads-enforcement reading.
- **ICN (International Competition Network)** — cross-agency coordination signal.
- **UNCTAD Competition and Consumer Policies** — particularly relevant for Latam and emerging-market regulators.
- **WTO competition-related work** — low cadence but tracked.

---

## Rules for tier movement

- **Promotion to a higher tier** requires (a) a Prosus operating-company acquisition or growth into the jurisdiction at scale, or (b) a structural regulatory change in the jurisdiction making it materially more aggressive on platform / digital-markets conduct.
- **Demotion** follows disposal of operating-company presence or sustained inactivity.
- **Quarterly review** confirms tier assignments per `operating-preferences.md` quarterly review cadence.

---

## Change log

| Date       | Change | Author |
|------------|--------|--------|
| 2026-05-13 | Initial competition-tier draft. Tier A = EU, NL, UK, BR, IN, ZA (subject to Naspers attribution question), CN (Tencent), US. Tier B = 16 active OpC jurisdictions. Pending Anne-Claire's Block 1 redline. | K. Maleevska |
