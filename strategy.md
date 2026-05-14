# Strategy

What we are building, why, and the rules every monitor inherits.

---

## What this system is

A federated network of legal-intelligence monitors. Each monitor is a Claude agent with its own persona, sources, filters, and feedback memory. The monitors are independent but share one architecture, one set of locked filters, and one Prosus Relevance Filter (see `README.md`).

The reason for federation rather than one mega-monitor: a single agent that tries to serve a Group Legal lead, a Tax counsel, an EU Comp counsel and an India GC will compromise on all four. Domain-specific personas reading from domain-specific source sets produce better signal, faster.

## Why now

Three drivers:

1. **Regulatory volume is up and rising.** AI Act, DMA/DSA, DPDP, LGPD enforcement, CCI suo-motu activity, US state-level AI rules, NAV-disclosure asks from Tencent. The legal team can no longer read everything that matters in a working day.
2. **Portfolio surface is wide.** Prosus operates across food delivery, classifieds, fintech, edtech, payments, GenAI infrastructure, in 15+ jurisdictions. No single counsel covers the whole map.
3. **Feedback-shaped agents work.** A monitor that learns over weeks beats a static digest. The Feedback Log is the moat.

---

## System-wide locked filters

> These are inherited by every monitor's Section 6 ("Locked filters"). They cannot be overridden by feedback, by the persona, or by the agent itself. They can only be changed by a documented edit to this file with sign-off from Group Legal.

1. **No paywalled-only content without a self-authored summary.** If only a paywall snippet is available, the agent writes its own summary from what is public or skips the item.
2. **No items older than 30 days** unless explicitly flagged as "historical context" and tied to a current item.
3. **No items sourced from blocked sources** (defined per monitor in Section 4).
4. **No personal data leakage.** PII surfaced by a source must be redacted before the agent quotes it. Names of public officials acting in public capacity are exempt.
5. **No paid-promotion content treated as primary.** Sponsored content, press releases without source citation, and content marketing pieces are secondary at best.
6. **No speculative legal advice in summaries.** The agent reports what the source says. "Why it matters" is allowed because it ties to the persona's stated needs; legal conclusions are not.
7. **No items that violate Prosus's external communications policy** (defamation risk, sanctions-sensitive geographies treated incautiously, market-moving info on unconfirmed sources).
8. **No removal of source `X` without sign-off** where `X` is on the official-register tier (regulators, courts, parliaments). A regulator that goes silent is information; we don't stop watching.

---

## The Prosus Relevance Filter is shared

Every monitor's Section 6 includes the Prosus Relevance Filter at a chosen strictness level (tight / medium / loose). The definition lives in `README.md` and is never re-defined per monitor — only the strictness setting varies.

If a monitor finds itself wanting to redefine what "Prosus-adjacent" means, that is a signal to open a `strategy.md` PR, not to fork the definition.

---

## Cross-monitor deduplication

When the same item is caught by two or more monitors — for example, an EU Court of Justice ruling on platform liability that lands in both the **EU Competition Law Monitor** and the **AI Governance Monitor** — exactly one monitor surfaces it as the primary item. The others link to it.

### Primary monitor — the rule

The **most-specific monitor wins**, in this priority order:

1. **Jurisdiction-specific over thematic.** A French Conseil d'État ruling goes to a France monitor before a global AI monitor.
2. **Single-domain over horizontal.** A DMA designation goes to EU Competition before AI Governance, even though AI Governance has read-through.
3. **Older monitor over newer.** If two monitors are equally specific and equally domain-fit, the monitor with the lower ID (older) wins. Stable assignment beats clever re-routing.
4. **Tie-breaker:** the monitor whose persona is closer to the item's centre of gravity. Owners decide.

### Mechanics

- Each item carries a content hash on the way out of the source-scan stage.
- The scheduler maintains a `briefed_items` index keyed by hash + date.
- When monitor B finds an item already briefed by monitor A today, monitor B includes a one-line **cross-reference** in its briefing instead of the full card: _"Also covered in today's [Monitor A] — see card #N."_
- Cross-references count toward briefing length but use a third of the cap (one cross-ref ≈ ⅓ item).
- Feedback (👍/👎) on a cross-reference flows back to **the primary monitor**, not the linking one.

### When to override

If the persona of the linking monitor would genuinely benefit from full coverage — different framing, different "why it matters", different action — the linking monitor can promote the cross-reference to a full item, but must:

- Add `dedup-override` tag with reason in the card metadata.
- Append to its own Change History (Section 9).
- Owner must approve at next weekly review.

Overrides are rare. If a monitor overrides more than ~10% of cross-refs, something is wrong with the assignment logic or the persona definition — open a `strategy.md` PR.

---

## Source-tier model

Every source goes into one of three tiers. This is system-wide and used by every monitor's Section 4.

| Tier | Examples                                                                 | Treatment                                                                 |
|------|--------------------------------------------------------------------------|---------------------------------------------------------------------------|
| 1 — Official register | EC press corner, OJEU, court dockets, regulator press releases, parliamentary records | Always trusted as primary. Quote directly. Cite by ID where one exists.  |
| 2 — Reputable wire / specialist | Reuters Legal, Bloomberg Law, FT, Law360, Mint, Folha, Caixin, Conjur | Primary if no Tier-1 source exists yet. Otherwise framing or confirmation. |
| 3 — Commentary / law-firm bulletins | Skadden alerts, Linklaters bulletins, individual analyst blogs | Secondary only. Used for "why it matters" framing; never the sole source. |

Promotion between tiers requires owner sign-off and a Change History row.

---

## Volume targets and length discipline

To keep the briefings useful rather than overwhelming, each monitor sets a hard daily cap (Section 7). Recommended defaults:

| Monitor type        | Daily cap |
|---------------------|-----------|
| Group-level (Digital & Regulatory, AI Governance) | 8–10 items |
| Jurisdiction-specific (India, Brazil, EU)         | 6–8 items  |
| Thin-slice (M&A antitrust, Tax)                    | 4–6 items  |

If a monitor regularly hits the cap, that is a signal — either the filter is too loose, or the world is genuinely busy that week. The agent does not auto-raise the cap. Owner approves any change.

---

## Calendar awareness

Regulators are predictable in ways the scanner can use. The Commission College
meets Wednesdays; CJEU Grand Chamber rulings cluster Thursdays; CADE Tribunal
sessions are quasi-monthly; AI Act effective dates are staged through 2027.
`scripts/regulatory_calendar.yml` records these rhythms; `regulatory_calendar.py`
emits the next-14-day window list.

Two consumers today: the weekly briefing's "Coming up this week" section, and
the hub freshness pulse's "next window" pointer. A scheduled scan that runs
on the eve of a known window is a small but real signal — surfacing nothing
is itself informative when something was expected.

The calendar is deliberately small and human-maintained. Adding a new file
(e.g. a live trilogue date) is one line in the YAML. The point is not to
model every agency, only to flag windows the operator already knows are
coming.

---

## Escalation channel

Some findings cannot wait for the next daily briefing. The escalation pathway
takes them out-of-band — to email, Slack, or Teams — within minutes of being
filed, while still leaving the full finding in its normal place on the
website. Implemented by `scripts/escalate.py`.

A finding is escalated when **any** of the following is true:

1. **Rank A + named Prosus OpCo (or Tencent) + finding age < 24 hours.** This
   is the typical "this happened today and it names us" trigger.
2. **`recommended_action_class = escalate`** — the persona's explicit flag.
   The locked-filter rules (Section 6 of every monitor) honour this without
   requiring rank A.
3. **`trigger_type = breach_incident` whose `affected_systems_or_practices`
   intersects `our_stack`.** Rule 12 (M01) — the 72-hour notification clock
   is a real deadline; the briefing cycle is not the right channel.
4. **`trigger_type = dawn_raid_pattern`.** Rule 9 (M02) — the coordination
   signal alone justifies attention.

Delivery channels are configured by environment variable; any combination of
them runs in parallel. None is required — if no channel is set, the script
still writes a stub to `findings/escalations/YYYY-MM-DD/` for the operator to
pick up on next review.

| Channel | Env var | Notes |
|---|---|---|
| Email | `ESCALATE_EMAIL_TO` (comma-separated) | Uses the same `GMAIL_USER` / `GMAIL_APP_PASSWORD` as the email ingester. |
| Slack | `ESCALATE_SLACK_WEBHOOK` | Incoming-webhook URL. |
| Teams | `ESCALATE_TEAMS_WEBHOOK` | Incoming-webhook URL. |

Escalation stubs are written to `findings/escalations/YYYY-MM-DD/` and
checked into git as a permanent record. The stub does not duplicate the
finding's body — only the metadata, reason, and a link.

**Boring on purpose.** Escalation is a small number of items per week, not a
constant stream. If `escalate.py` is firing on more than a handful of items
per week, the locked filters are too loose; revisit Section 6 of the monitor
producing the noise.

---

## Confidentiality pre-filter

Before any candidate is written to `findings/candidates/`, the scraper and email
ingester pass it through `scripts/lib_confidentiality.py`, which checks against
`scripts/confidential_watchlist.yml` (gitignored). The watchlist matches three
kinds of pattern: internal **matter codes**, **keyword phrases** indicating
privileged or leniency-track work product, and **sender emails** or domains
whose alerts must never be ingested.

Matches are quarantined to `findings/_confidential/YYYY-MM-DD/` as opaque
stubs containing only the path, a 16-character sha256 prefix, and the matching
*category* (matter_code, keyword_phrase, or sender_email — never the phrase
itself). The original body is dropped. A JSONL audit log lets the operator
verify volume without exposing the privileged content.

**Why the watchlist is gitignored**: the matter codes themselves can be
privileged. The example file (`confidential_watchlist.example.yml`) ships
generic leniency / privilege phrases as safe defaults and is committed.

**Failing closed**: matching is substring + case-insensitive rather than
regex. A typo in a regex can silently disable the filter; substring matching
fails closed and is faster to audit.

**Locked filter status**: this pre-filter sits *upstream* of Section 6 locked
filters. A confidential item never reaches a persona's interrogation stage.
This makes it more than a locked filter — it is a pre-pipeline kill-switch.
To change matching behaviour, edit `lib_confidentiality.py` with a documented
change-log row here.

---

## Operating principles

- **Tight beats loose by default.** Easier to widen than to win back attention.
- **The Feedback Log is the moat.** A monitor that has been running and learning for 6 months is materially better than one starting from scratch.
- **The structure is the product.** Other teams can clone this folder. The shape is what makes the system replicable.
- **Locked filters protect against agent drift.** They are a feature, not friction.
- **The website surfaces, the monitors decide.** No business logic lives in the rendering layer.

---

## Change log for this file

| Date       | Change                                  | Author       |
|------------|-----------------------------------------|--------------|
| 12 May 2026 | Initial strategy — system-wide locked filters, dedup rule, source tiers, volume targets | Group Legal & Public Policy |
