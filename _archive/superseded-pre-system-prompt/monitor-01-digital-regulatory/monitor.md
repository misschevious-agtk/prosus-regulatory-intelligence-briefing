# Digital & Regulatory Monitor

## 1. Identity

- **Monitor name:** Digital & Regulatory Monitor
- **Monitor ID:** `monitor-01-digital-regulatory`
- **Owner:** Group Legal & Public Policy — primary contact: Klimentina Maleevska
- **Status:** Active
- **Last updated:** 12 May 2026
- **Template version in use:** 1.0

---

## 2. Persona

- **Profession & seniority:** Group Legal & Public Policy lead. In-house, Prosus Group, Amsterdam. Reports into the Chief Legal Officer; briefs the CEO and Board as needed on cross-cutting regulatory exposure.
- **Profile:** Owns the Group's situational awareness on digital regulation across every market Prosus operates in. Coordinates between the EU Comp, AI Counsel, Privacy, India hub, LatAm hub, and Tencent IR liaison sub-teams. Decisions this briefing feeds into: which items to escalate to CLO/CEO; which to delegate to a sub-team; which to fold into the next Board pack; which to monitor passively. Gets blamed if something material lands in the press before it lands in their inbox.
- **Reading context:** Morning, 07:30–08:30 CEST, before standing meetings. Often mobile commute followed by a desktop revisit. Will dip back into the briefing 1–2 times across the day if a flash event lands.
- **Decision authority:** Can act on items directly (delegate, draft, escalate). Owns the routing logic to sub-teams.

---

## 3. Purpose & Needs

- **Purpose:** Surface every regulatory or legal development across digital sectors that could affect Prosus, its portfolio companies, or its operating markets within a 12-month horizon — fast enough to act before the news cycle moves.

- **Needs:**
  - Daily situational awareness across AI policy, privacy, competition, IP, AI launches, legal ops, and trending macro-legal topics, on a single page.
  - Deadline radar: anything Prosus or a portfolio company must file, respond to, or attend in the next 30 days.
  - Portfolio mapping: which items touch which portfolio company, with who-owns-what visible.
  - "Why it matters for Prosus" framing on every item — not generic legal summaries.
  - The ability to escalate or delegate an item in two clicks (Share, Open source) without leaving the briefing.
  - Memory of past items so today's brief can reference last week's pattern.

- **Out of scope:**
  - Pure tax policy (handled by M07 Tax Policy Monitor when live).
  - M&A antitrust filings for specific Prosus transactions (handled by M06 M&A Antitrust Monitor when live; until then, surfaced here only when external precedent value is material).
  - ESG / CSRD-only items unless they intersect digital regulation.
  - Internal company news.
  - Tech-sector business news without a regulatory or legal angle.

---

## 4. Sources Scanned

### Primary sources (Tier 1 — official register)
- **European Commission press corner** · https://ec.europa.eu/commission/presscorner/ · DG-COMP, DG-CNECT, DG-JUST press releases · RSS
- **Official Journal of the EU (OJEU)** · https://eur-lex.europa.eu/oj/direct-access.html · Implementing acts, regulations, decisions · daily digest
- **EDPB** · https://www.edpb.europa.eu/ · Opinions, guidelines, decisions · RSS
- **UK CMA** · https://www.gov.uk/government/organisations/competition-and-markets-authority · Decisions, investigations, market studies · RSS
- **RBI (Reserve Bank of India)** · https://www.rbi.org.in/ · Circulars, master directions, press releases · RSS + scrape
- **MeitY (Ministry of Electronics & IT, India)** · https://www.meity.gov.in/ · DPDP, intermediary rules · scrape
- **CCI (Competition Commission of India)** · https://www.cci.gov.in/ · Suo-motu orders, investigations · scrape
- **DPIIT** · https://dpiit.gov.in/ · FDI clarifications · scrape
- **ANPD (Brazil)** · https://www.gov.br/anpd/pt-br · LGPD enforcement · RSS
- **CADE (Brazil)** · https://www.gov.br/cade/pt-br · Antitrust decisions · scrape
- **STJ / STF (Brazil)** · https://www.stj.jus.br/ · Higher-court rulings on platform liability · digest
- **CAC (Cyberspace Administration of China)** · http://www.cac.gov.cn/ · GenAI rules, data-export rules · scrape
- **PDPC (Singapore)** · https://www.pdpc.gov.sg/ · AI governance framework, enforcement · RSS
- **KOMINFO (Indonesia)** · https://www.kominfo.go.id/ · AI ethics rules, content moderation · scrape
- **Information Regulator (South Africa)** · https://inforegulator.org.za/ · POPIA enforcement, ADM code · scrape
- **N.D. Cal. + S.D.N.Y dockets** · PACER feeds · AI fair-use litigation · API
- **Câmara dos Deputados + Senado Federal (Brazil)** · https://www.camara.leg.br/ · PL 2630 and related platform bills · digest
- **Tencent Investor Relations** · https://www.tencent.com/en-us/investors.html · Earnings, regulatory disclosures · RSS

### Secondary sources (Tier 2 — reputable wire / specialist)
- Reuters Legal · https://www.reuters.com/legal/ · global wire
- Bloomberg Law · https://www.bloomberglaw.com/ · US-anchored legal news
- Mint · https://www.livemint.com/ · India business + reg
- Folha de S.Paulo · https://www.folha.uol.com.br/ · Brazil
- Caixin · https://www.caixin.com/ · China business + reg
- Conjur · https://www.conjur.com.br/ · Brazil legal commentary
- Business Standard · https://www.business-standard.com/ · India
- Law360 · https://www.law360.com/ · US litigation digest
- Financial Times — competition / digital regulation desks · https://www.ft.com/

### Excluded sources
- Anonymous Twitter / X aggregators — never primary, never quoted.
- LinkedIn long-form posts without a verifiable source citation — never primary.
- Paid press-release wires (PR Newswire, BusinessWire, etc.) as standalone — only used to find the underlying primary source.

---

## 5. Run Cadence

- **Frequency:** Daily.
- **Run window:** 04:00–05:30 CEST.
- **Delivery time:** 07:30 CEST.
- **Delivery channel:** Web dashboard (`prosus-digital-regulatory-monitor.html`) + 07:30 CEST email digest. Flash events trigger an in-app notification when they land outside the run window.

---

## 6. Filters

### User-set filters
- **Date range / recency window:** Default "last 7 days" view, with same-day flash items always at the top.
- **Jurisdictions / geographies:** All jurisdictions where Prosus has material exposure (India, Brazil, EU, US, UK, China, ZA, NL, ID, SG, PL) — see `portfolios.md`.
- **Prosus Relevance Filter:** **Medium.** Surface direct hits and items with clear read-through to a Prosus business within 12 months. Excludes pure-precedent items unless they touch a Prosus operating market.
- **Topic emphasis:** AI & Policy and Privacy & Data weighted slightly heavier than Competition through 2026 — reflects the current regulatory cycle.
- **Length cap per briefing:** 8–10 items per day (Group-level monitor default).

### Locked filters

**System-wide locks** _(inherited from `strategy.md` — never edited here):_
- No paywalled-only content without a self-authored summary
- No items older than 30 days unless flagged "historical context"
- No items sourced from blocked sources (Section 4)
- No PII leakage from sources
- No paid-promotion content treated as primary
- No speculative legal advice in summaries
- No items that violate Prosus external communications policy
- No silent removal of Tier-1 sources

**Monitor-specific locks:**
- **Always surface deadline items inside the 30-day window**, even if the persona's user-set window is narrower. Deadlines are sacrosanct.
- **Always surface items where a Prosus entity or portfolio company is directly named**, even if the topic emphasis is muted.
- **Never drop the EU AI Act, DPDP Act, LGPD, DMA, or DSA from primary scope** while those regimes are active. These are the four spine regimes for Prosus's digital footprint.
- **Tencent NAV-disclosure items always surface.** Disclosure cycles are non-discretionary.
- **Court orders involving Prosus or any portfolio company always surface.**

---

## 7. Output Format

### Briefing-level wrapper
- **Top of briefing:** Date · Monitor name · Item count · Run timestamp · "Today's takeaway" (3-sentence synthesis)
- **Item ordering:** Most need-relevant first. Tie-breaker: high-risk before medium before low; deadline-proximate before non-deadline.
- **Length cap:** 8–10 items.
- **Tone:** Tight, factual, no hedging language. One-sentence summary per item; "why it matters" can be two short sentences if the read-through is non-obvious. No "may", "could", "potentially" unless the source itself is hedged.
- **Footer:** Pipeline stats — sources swept, items considered, items selected, items filtered out, topic areas active.

### Per-item structure
Each card:

- **Headline** — source title or a tight rewrite (≤120 chars).
- **One-sentence summary** — what happened.
- **Why it matters for Prosus** — explicit tie to one of the Section 3 needs. Names the portfolio company or operating market.
- **Source** — primary citation (Tier 1) plus a secondary if used for framing.
- **Date** — publication date.
- **Jurisdiction** — country/region tag.
- **Risk band** — low / medium / high. High = active legal-team attention this week; medium = monitor and prep; low = situational awareness.
- **Portfolio exposure** — affected Prosus entity (Tencent NAV, iFood, Swiggy, Stack Overflow, OLX, PayU, Meesho, Brainly, Codecademy, or "Group").
- **Owner** — internal Prosus owner if action is required.
- **Status** — new / triaged / in progress / awaiting response / closed.
- **Next action** — one sentence, only if action_required = true.
- **Deadline** — date, only if applicable.
- **Estimated impact** — one short phrase (e.g. "€2–5M legal & engineering cost", "NAV disclosure cycle", "Precedent — saved to playbook").

### Card actions (must be present on every item)
1. **Copy** — copy summary + source to clipboard.
2. **Summarise** — expand into a longer brief, on demand.
3. **Share** — push to Slack / Teams / email.
4. **Open source** — open the underlying source URL in a new tab.

### Pinning (Watchlist)
- Star icon on every card. Pinning adds the item to the persona's Watchlist tab, persisted in-session. (Cross-session persistence handled at the website layer, not here.)

---

## 8. Feedback & Learning Log

### Feedback mechanism
- 👍 / 👎 per item directly in the dashboard.
- Free-text comment field per item.
- Weekly "anything we missed?" prompt every Friday.

### Agent rules
- One 👎 is a signal, not a verdict. Log it; act on patterns of three or more comparable signals inside 14 days.
- Locked filters in Section 6 are never modified by feedback.
- Source removal requires owner sign-off and a Section 9 row. De-prioritisation does not.
- Positive signal acts faster: two 👍 on a previously-low-weight source triggers a weight bump within 7 days.

### Running log

| Date       | Signal                                                                 | Agent's interpretation & action                                                                                            |
|------------|------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| 2026-05-12 | Initial seeding — no prior signal                                       | Calibration mode begins per `cold-start-protocol.md`. Daily cap raised to 12, Prosus Relevance Filter loosened to "Loose" for first 14 days. |

### Weekly self-review

- **2026-05-12:** Day 0. Calibration mode active. Will write first self-review on 2026-05-15 (Day 3).

---

## 9. Change History

| Date       | Change                                                                                  | Author       | Sign-off |
|------------|-----------------------------------------------------------------------------------------|--------------|----------|
| 2026-05-12 | Initial creation. Spec drafted from existing Digital & Regulatory dashboard prototype. | K. Maleevska | CLO      |
