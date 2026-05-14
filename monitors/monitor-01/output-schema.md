# Output Schema (SHARED)

Every material **finding** produces one MD file in `/findings/` using this exact shape. **No claim without a verbatim anchor quote.** No exceptions.

This schema is **locked**. It can only be changed by edit-with-sign-off; see `SYSTEM-PROMPT.md`. The ranking layer (`ranking-criteria.md`) reads enumerated fields from this schema — never prose — so any field added here must be added to the rank rules in the same change.

> **Scope note:** This file specifies the schema for **individual findings**. Monitor 01 also produces five other document types — daily briefs, weekly indexes, monthly digests, quarterly board summaries, incident notes — defined in `operating-preferences.md` Section 2. Those types follow prose conventions, not the structured schema below. See `findings/README.md` for file-naming across all six types. **Incidents bypass this schema; everything else honours it.**

---

## File naming

```
findings/YYYY-MM-DD-[domain]-[slug].md
```

- `YYYY-MM-DD` — `date_found` from the frontmatter, not `source_date`.
- `[domain]` — one of `ai-news` · `privacy` · `ip` · `legal-ops`.
- `[slug]` — short, lowercase, hyphenated, no more than 6 words.

---

## Frontmatter

```yaml
---
date_found: YYYY-MM-DD
domain: [ai-news | privacy | ip | legal-ops]
source_url:
source_publisher:
source_date:
source_type: [primary-law | court-ruling | regulator-guidance | enforcement-action |
              vendor-announcement | trade-press | academic | marketing | other]
one_sentence_summary:
primary_axis: [compliance | liability | movement | operational | reputational]
secondary_axes: []
jurisdiction: [EU | EU-member-state | US-federal | US-state-XX | UK | global | other]
trigger_type: [law_enacted | law_effective_date | enforcement_action | court_ruling |
               regulator_guidance | model_release | capability_demo | vendor_change |
               breach_incident | license_event | market_move | narrative_shift |
               tooling_change | workflow_benchmark]
deadline_if_any: [YYYY-MM-DD or null]
affected_systems_or_practices: []
recommended_action_class: [monitor | review | act | escalate]
severity_self_assessment: [1-5]
severity_justification:
confidence: [low | medium | high]
---
```

### Field notes

- **`date_found`** — when the agent surfaced it. May differ from `source_date`.
- **`domain`** — primary owner. An item touching two domains files under its primary and cross-references in the secondary (see Operating Rule 5 in `SYSTEM-PROMPT.md`).
- **`source_url`** — direct, canonical link. No tracking parameters. Archive.org snapshot acceptable as fallback.
- **`source_publisher`** — who published it (court, regulator, vendor, outlet).
- **`source_date`** — the date on the source itself.
- **`source_type`** — chosen from the enumerated list. Affects confidence. Marketing-only sources require corroboration before reaching rank C or higher.
- **`one_sentence_summary`** — plain English, no jargon, written so a non-specialist reader grasps it.
- **`primary_axis`** — the dominant lens through which this matters.
- **`secondary_axes`** — optional, list of additional axes if the item is multi-vector.
- **`jurisdiction`** — geographic scope of the legal effect. Where multiple, list the most binding first.
- **`trigger_type`** — chosen from the enumerated list. This is the single most important field for rank application — choose carefully.
- **`deadline_if_any`** — date a compliance step, response, or filing is due. `null` if none.
- **`affected_systems_or_practices`** — list of named items from `needs.md` or `our_stack` (see Block 1, Q3) the finding touches. Used by rank rules to identify in-stack/in-practice items.
- **`recommended_action_class`** — one of `monitor`, `review`, `act`, `escalate`. The persona's recommendation; not the same as the tier-2 rank.
- **`severity_self_assessment`** — integer 1–5. Used by the rank layer.
- **`severity_justification`** — one sentence explaining the severity number. Used in audit, not in ranking.
- **`confidence`** — `low` / `medium` / `high`. If unverifiable, `low`. Marketing sources without corroboration default to `low`.

### Enumerations (do not extend without sign-off)

- `source_type`: `primary-law` · `court-ruling` · `regulator-guidance` · `enforcement-action` · `vendor-announcement` · `trade-press` · `academic` · `marketing` · `other`
- `primary_axis`: `compliance` · `liability` · `movement` · `operational` · `reputational`
- `trigger_type`: `law_enacted` · `law_effective_date` · `enforcement_action` · `court_ruling` · `regulator_guidance` · `model_release` · `capability_demo` · `vendor_change` · `breach_incident` · `license_event` · `market_move` · `narrative_shift` · `tooling_change` · `workflow_benchmark`
- `recommended_action_class`: `monitor` · `review` · `act` · `escalate`
- `confidence`: `low` · `medium` · `high`

---

## Body

The body has six fixed sections, in this exact order. No additional headings.

```markdown
## Verbatim anchor quote
> [≤25 words from the source — the passage that proves the claim]

## Why it matters to us
[2-3 sentences, plain English, tied to our needs.md for this domain]

## Worst plausible reading
[1 sentence]

## Best plausible reading
[1 sentence]

## What the source does not say
[1 sentence, or "nothing notable"]

## Open questions for human review
[bullets, only if applicable]
```

### Body rules

- The **anchor quote** is the load-bearing element. ≤25 words, quoted verbatim from the source, capturing the passage that proves the claim. No paraphrasing in this block. If you can't extract a ≤25-word verbatim that proves the claim, the finding is not yet ready — either find a quotable passage or drop the finding.
- The **"why it matters to us"** must cite by name an item from the relevant `needs.md`. Generic "this is important" framing is not acceptable.
- **Worst** and **best plausible readings** are short and unhedged. They are not predictions — they are bounds.
- **What the source does not say** captures absences worth noting. A regulator's silence on a related issue is information. If genuinely nothing notable, write "nothing notable".
- **Open questions** are only for things a human reviewer needs to resolve. If there are none, omit the section.

---

## Discipline

- **One finding = one source.** If two sources corroborate, the second one goes in the body as supporting evidence after the anchor quote, with its own short citation.
- **Empty output is valid output.** A run that produces zero findings is acceptable. Forced findings degrade the corpus.
- **Never invent URLs, citations, dates, or quotes.** If you cannot verify, drop the item or mark `confidence: low` and surface the gap in Open questions.
- **Self-critique before filing.** Would this finding survive a sceptical partner asking "where exactly does it say that?" If not, downgrade `confidence` or do not file.
