# Portfolios — Coverage

Which monitors cover what, who they serve.

> Read with `README.md` (architecture) and `strategy.md` (cross-monitor rules).
> **Current scope:** Monitor 01 (multi-persona, four domains) and Monitor 02 (multi-persona, four reading-modes of a single named anchor). Both monitors are now on the multi-persona architecture. The authoritative coverage maps for each monitor live inside that monitor:
>
> - `monitors/monitor-01/portfolio-map.md`, `our_markets.md`, `sectoral-overlays.md`, `our_stack.md`
> - `monitors/monitor-02-eu-competition/portfolio-map.md`, `our_markets.md`, `sectoral-overlays.md`, `our_stack.md`
>
> Both monitors share the same underlying Prosus reality but read it through different lenses. The portfolio-map files are deliberately maintained separately because the attention matrix and dominance map differ per monitor. Where the underlying vendor list or jurisdictional tier overlaps (e.g. `our_stack.md` between M01 and M02), Monitor 01 is the single source of truth and Monitor 02 mirrors with competition-lens annotations.
>
> This page is the briefing-level index of those maps, not a duplicate. When a new monitor is added, its coverage rolls up here.

---

## Coverage matrix — domain × jurisdiction

Rows are Monitor 01 and Monitor 02 domains. Columns are Tier A jurisdictions across both monitors. Cells mark which monitor/domain owns the intersection.

| Domain / Monitor                                          | EU       | NL       | UK       | CN (Tencent) | BR  | IN  | US  | ZA  |
|-----------------------------------------------------------|----------|----------|----------|--------------|-----|-----|-----|-----|
| **M01** AI News                                           | ✅       | ✅       | ✅       | ✅           | ✅  | ✅  | ✅  | ✅  |
| **M01** Privacy & Data Protection                         | ✅       | ✅       | ✅       | ✅           | ✅  | ✅  | ✅  | ✅  |
| **M01** Intellectual Property                             | ✅       | ✅       | ✅       | ✅           | ✅  | ✅  | ✅  | ✅  |
| **M01** Legal Ops                                         | ✅       | ✅       | ✅       | —            | ✅  | ✅  | ✅  | ✅  |
| **M02** Antitrust & Cartels                               | ✅       | ✅       | ✅       | ✅ (SAMR via Tencent) | ✅ (CADE) | ✅ (CCI) | ✅ (DOJ/FTC) | ✅ (subject to Naspers/SACC question) |
| **M02** Abuse of Dominance & Unilateral Conduct           | ✅       | ✅       | ✅       | ✅ (SAMR)    | ✅  | ✅  | ✅  | ✅ (subject to Naspers/SACC question) |
| **M02** Merger Control & Foreign Investment Screening     | ✅       | ✅       | ✅       | ✅ (SAMR)    | ✅  | ✅  | ✅  | ✅ |
| **M02** Digital Markets, Sector Regulation & State Aid    | ✅ (DMA/DSA/FSR primary) | ✅ | ✅ (CMA DMU/SMS) | ✅ (CAC × competition) | ✅ | ✅ | ✅ | ✅ |

Tier B / C / D jurisdictions are read by both monitors with the rank ceilings defined in their respective `our_markets.md` and `ranking-criteria.md`. Monitor 02's coverage extends globally, not EU-only, despite the historic directory name.

**Cross-monitor dedup:** Per `strategy.md` Cross-monitor deduplication and per Rule 21 in both monitors' `ranking-criteria.md`, an item is filed in the **primary monitor** (whichever monitor's substantive doctrine most directly answers the question "what action does this require") with a cross-reference note in the secondary monitor's weekly index. Canonical examples:

- CMA AI Foundation Models work → primary M01 AI News; secondary M02 Digital Markets.
- EU AI Act competition-policy provisions → primary M01 AI News; secondary M02 Digital Markets and potentially Abuse of Dominance.
- CADE food-delivery enforcement combining horizontal-restraint and personal-data theories → primary M02 Antitrust & Cartels; secondary M01 Privacy.

Cross-monitor routing now runs both ways: M02 Rule 21 ↔ M01 Rule 22 (added 2026-05-14). The dedup engine is exercised against `scripts/tests/dedup_golden.yml` on every change.

---

## Coverage matrix — portfolio companies

Full per-OC detail lives in `monitors/monitor-01/portfolio-map.md`. Summary here:

| Portfolio company        | Region            | Primary thesis           | Monitor 01 attention (highest of 4 domains) |
|--------------------------|-------------------|--------------------------|----------------------------------------------|
| **iFood**                | BR                | Food delivery            | **Highest** — touches every domain           |
| **OLX Group**            | EU / LatAm / MENA | Classifieds              | High                                          |
| **PayU (India + retained)** | IN / global    | Payments + lending       | High                                          |
| **iyzico**               | TR                | Payments                 | Medium-high                                   |
| **Despegar / Decolar**   | LatAm             | OTA / travel             | Medium                                        |
| **eMAG**                 | RO / BG / HU      | E-tail                   | Medium                                        |
| **Just Eat Takeaway**    | EU / UK / Canada / IL / AU / NZ | Food delivery | High                              |
| **Stack Overflow**       | US / global       | Developer Q&A            | High (IP centre of gravity)                   |
| **GoodHabitz**           | NL / EU           | Corporate training       | Medium                                        |
| **Tencent (NAV stake)**  | CN                | Stake — dominant NAV     | **Highest after iFood** — Rule 6              |
| **Swiggy (stake)**       | IN                | Food + quick-commerce    | High                                          |
| **Remitly (stake)**      | US                | Remittances              | Medium                                        |
| **Delivery Hero (stake)**| DE                | Food delivery            | Medium                                        |
| **EMPG / dubizzle**      | MENA              | Classifieds / property   | Medium                                        |
| **Edtech stakes**        | Multiple          | EdTech                   | Medium (minors overlay)                       |
| **Ventures AI book (30+)** | Global          | AI-native startups       | Medium (intelligence, not consumption)        |

---

## Rules for portfolio coverage

- **A new portfolio acquisition triggers a coverage review** within 30 days. The review answers: which existing personas (within Monitor 01 or any future monitor) expand, which need a new persona, or whether a new monitor is justified.
- **A divestment triggers a removal review** within 30 days. Sources tied only to the divested entity should be re-tiered or removed. Prosus has signalled **$2bn+ in disposals in 2026 and continued sales in 2027** — coverage maps are living MDs and reviewed quarterly.
- **No part-time coverage.** If a domain owns a cell, the persona is responsible for keeping it scanned.

---

## Change log

| Date       | Change                                                                                                  | Author |
|------------|---------------------------------------------------------------------------------------------------------|--------|
| 2026-05-12 | Initial coverage matrix; first wave plan (M01–M08 single-persona)                                       | Group Legal & Public Policy |
| 2026-05-12 | Architecture pivot to multi-persona Monitor 01. Old M01–M08 plan archived. Coverage maps now live inside the monitor and roll up here. | Group Legal & Public Policy |
| 2026-05-13 | Rebuilt post Monitor 02 Block 1–3 initialisation. Monitor 02 moved to multi-persona reading-mode architecture (Anne-Claire Hoyng as named anchor; four doctrinal domains). Coverage matrix expanded to show M02's four domains across Tier A jurisdictions globally (not EU-only). Cross-monitor coordination via Rule 21 in both monitors' `ranking-criteria.md`. | K. Maleevska |
