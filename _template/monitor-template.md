# Monitor Template

> **READ-ONLY REFERENCE.** This file is the canonical structure for a monitor MD.
> Do not edit it for a specific monitor. To create a new monitor, copy this file
> to `monitors/monitor-XX-<slug>/monitor.md` and fill it in.
>
> If the template itself needs to evolve, edit it deliberately, bump the version
> below, and record the change in `README.md` under "Template history".
>
> **Template version:** 1.0 — 12 May 2026

---

## 1. Identity

- **Monitor name:** _(short, descriptive — e.g. "EU Competition Law Monitor")_
- **Monitor ID:** _(stable slug, never renamed — e.g. `monitor-03-eu-competition`)_
- **Owner:** _(team or person responsible for this spec)_
- **Status:** _(active / paused / experimental)_
- **Last updated:** _(YYYY-MM-DD)_
- **Template version in use:** 1.0

---

## 2. Persona

- **Profession & seniority:** _(e.g. "Senior Competition Counsel, in-house, Prosus Group Legal")_
- **Profile:** _(what they care about; what their day looks like; what decisions this briefing feeds into; what they get blamed for if they miss something)_
- **Reading context:** _(when and how they consume the briefing — morning coffee, between meetings, mobile commute, etc.)_
- **Decision authority:** _(can they act on items themselves, do they triage to others, or are they informing leadership?)_

---

## 3. Purpose & Needs

- **Purpose** _(one sentence):_ _What this monitor exists to do._
- **Needs** _(bullet list of concrete jobs-to-be-done):_
  - _Need 1_
  - _Need 2_
  - _Need 3_
- **Out of scope** _(what this monitor explicitly does NOT cover — prevents scope creep by the agent):_
  - _Excluded topic 1_
  - _Excluded topic 2_

---

## 4. Sources Scanned

### Primary sources
> Checked every run. Official registers, regulators, courts, parliaments.
> Each entry: name · URL · what it provides · scan method (RSS / scrape / API / digest).

- _Source 1 · URL · contents · method_
- _Source 2 · URL · contents · method_

### Secondary sources
> Checked every run but weighted lower. Commentary, news, law-firm publications.

- _Source 1 · URL · contents · method_

### Excluded sources
> Blocked. Agent must never surface items from these.

- _Source 1 · reason for exclusion_

---

## 5. Run Cadence

- **Frequency:** Daily _(default — change only with owner sign-off)_
- **Run window:** _(when the scan happens — e.g. 04:00–05:00 CEST)_
- **Delivery time:** _(when the briefing lands for the persona — e.g. 07:30 local)_
- **Delivery channel:** _(email / Slack / dashboard widget / .ics push)_

---

## 6. Filters

### User-set filters
> The persona can adjust these. The agent updates them when feedback warrants
> (see Section 8) but always logs the change in Section 9.

- **Date range / recency window:** _(e.g. last 24h, last 7 days)_
- **Jurisdictions / geographies:** _(list of countries, regions, or "global")_
- **Prosus Relevance Filter:** _(tight / medium / loose — see README for definitions)_
- **Topic emphasis:** _(if any sub-topic should be boosted or muted)_
- **Length cap per briefing:** _(integer — see Section 7)_

### Locked filters
> **Set in stone. The agent must never override these, even with positive feedback.**
> Locked filters come in two layers:
>
> 1. **System-wide locks** (inherited from `strategy.md`) — always apply, listed here for transparency.
> 2. **Monitor-specific locks** — set by the monitor owner; can only be changed via Change History (Section 9) and owner sign-off.

**System-wide locks** _(do not edit — inherited):_
- No paywalled-only content without a self-authored summary
- No items older than 30 days unless flagged as "historical context"
- No items sourced from blocked sources (Section 4)
- No personal-data leakage from sources (PII must be redacted before surfacing)
- No paid-promotion content treated as primary source

**Monitor-specific locks:**
- _Locked filter 1_
- _Locked filter 2_

---

## 7. Output Format

### Briefing-level wrapper
- **Top of briefing:** Date · Monitor name · Item count · Run timestamp · Persona name
- **Item ordering:** Most need-relevant first _(not most recent first)_
- **Length cap:** _(integer, e.g. 8 items per day — forces prioritisation, not dumping)_
- **Tone:** _(e.g. "tight, factual, no hedging language; 1 sentence per item summary")_
- **Footer:** Pipeline stats (sources swept, items considered, items selected, items filtered out)

### Per-item structure
Each item is rendered as a clickable card with these fields:

- **Headline** — article/document title or a tight rewrite
- **One-sentence summary** — what happened
- **Why it matters (need-related)** — explicit tie to the persona's needs from Section 3, not a generic "this is important"
- **Source** — primary citation; secondary if used for framing
- **Date** — publication date of the source item
- **Jurisdiction** — country/region tag
- **Risk band** — low / medium / high (defined per monitor)
- **Portfolio exposure** — affected Prosus entity if any

### Card actions (must be present on every item)
1. **Copy** — copy summary + source to clipboard
2. **Summarise** — expand into a longer brief, on demand
3. **Share** — push to Slack / Teams / email
4. **Open source** — open the underlying source URL in a new tab

---

## 8. Feedback & Learning Log

> Append-only. Agent writes here whenever it changes its behaviour in response
> to user signal.

### Feedback mechanism
- 👍 / 👎 per item on the briefing
- Free-text comments accepted via reply

### Agent rules
- **One 👎 is a signal, not a verdict.** Log it, watch for the pattern, act only on repetition (≥3 within 14 days on a comparable item).
- **Locked filters (Section 6) are never modified by feedback.** Full stop.
- **Source removal is a high bar.** A source can be de-prioritised after 3 unrelated 👎; full removal requires owner sign-off recorded in Section 9.
- **Positive signal is acted on faster.** 2 👍 on a previously-low-weight source triggers a weight increase.

### Running log

| Date       | Signal                                | Agent's interpretation & action                                  |
|------------|---------------------------------------|------------------------------------------------------------------|
| YYYY-MM-DD | _e.g. 👍 on item about [topic] from [source]_ | _e.g. Increase weight on [source] for [topic-type]._     |
| YYYY-MM-DD | _e.g. 👎 on item about [topic]_       | _De-prioritise [pattern]; do not remove source entirely._        |

### Weekly self-review
> The agent appends a short note every Friday: patterns observed, changes made, things being watched.

- **YYYY-MM-DD:** _Self-review entry._

---

## 9. Change History

> Append-only. Tracks meaningful edits to **this spec** — separate from feedback log.

| Date       | Change                                    | Author       | Sign-off  |
|------------|-------------------------------------------|--------------|-----------|
| YYYY-MM-DD | Initial creation                          | _Owner_      | _Owner_   |
| YYYY-MM-DD | _e.g. Added source X; removed source Y_   | _Author_     | _Owner_   |
| YYYY-MM-DD | _e.g. Tightened locked filter; ratio …_   | _Author_     | _Owner_   |
