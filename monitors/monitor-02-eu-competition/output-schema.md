# Output Schema — Monitor 02 Findings

Every material finding produces one MD file in `/findings/` using the frontmatter and body structure below. **No claim without a verbatim anchor quote.**

## Filename convention

```
YYYY-MM-DD-[domain]-[slug].md
```

Where `[domain]` is one of: `antitrust-cartels`, `abuse-of-dominance`, `merger-control-fdi`, `digital-markets-sector-state-aid`. The `[slug]` is a short kebab-case identifier (e.g. `dg-comp-mfn-guidance-update`, `cade-ifood-tcc-extension`).

## Frontmatter

```yaml
---
date_found: YYYY-MM-DD
domain: [antitrust-cartels | abuse-of-dominance | merger-control-fdi | digital-markets-sector-state-aid]
source_url:
source_publisher:
source_date:
source_type: [commission-decision | nca-decision | court-judgment | ag-opinion |
              statement-of-objections | settlement | guidance | speech |
              market-investigation | sector-inquiry | trade-press | academic |
              vendor-announcement | marketing | other]
one_sentence_summary:
primary_axis: [enforcement-risk | transaction-risk | compliance | strategic-opportunity |
               sector-regulation | reputational]
secondary_axes: []
jurisdiction: [EU | EU-member-state-XX | UK | US | other-national | multi | global]
trigger_type: [final_decision | interim_decision | statement_of_objections |
               settlement | court_ruling | ag_opinion | guidance_published |
               threshold_change | designation | sector_inquiry_opened |
               sector_inquiry_concluded | dawn_raid_pattern | leniency_change |
               remedy_precedent | market_move | narrative_shift]
deadline_if_any: [YYYY-MM-DD or null]
affected_practices_or_deals: []
recommended_action_class: [monitor | review | act | escalate]
severity_self_assessment: [1-5]
severity_justification:
confidence: [low | medium | high]
---
```

## Body sections (in order)

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

---

## Field definitions and selection guidance

The following notes apply to the enumerated fields. Tier-2 ranking operates on these values mechanically; choose them precisely.

### `source_type`

- **commission-decision** — final or interim European Commission decision under Articles 101, 102, EUMR, FSR, or state aid.
- **nca-decision** — final or interim national competition authority decision (BKartA, CMA, AdC, AGCM, ACM, CADE, CCI, COFECE, SACC, etc.).
- **court-judgment** — General Court, CJEU, national court, or US court ruling.
- **ag-opinion** — Advocate General opinion at CJEU. Directional, not binding. Weight as primary signal but `confidence: medium` ceiling unless followed by a judgment.
- **statement-of-objections** — formal preliminary charge from a competition authority. Indicates the authority's working theory of harm, not the final position.
- **settlement** — settlement or commitment decision (Article 9 settlements, NCA equivalents, CADE TCCs, US consent decrees).
- **guidance** — published guidance, guidelines, notice, or analogous formal-but-non-binding instrument.
- **speech** — agency commissioner or senior-official speech. Treat as directional only; `confidence: medium` ceiling unless a formal instrument follows.
- **market-investigation** — formal market investigation opening, interim findings, or final report (CMA-style market investigations and analogues).
- **sector-inquiry** — sector inquiry opening, interim, or final (DG COMP Article 17 inquiries, NCA equivalents).
- **trade-press** — competition-press reporting (GCR, MLex, PaRR, Concurrences, Competition Policy International). Weight depends on the source's track record; cross-check before relying.
- **academic** — peer-reviewed journal article, SSRN preprint, or working paper from a recognised competition-policy academic source. Per the persona inversion, this is primary signal for Monitor 02, not commentary.
- **vendor-announcement** — corporate or vendor press release. Default to low weight unless it concerns a transaction, commitment, or self-reported enforcement matter.
- **marketing** — promotional content. Default to `confidence: low`.
- **other** — for sources not fitting the above. Use sparingly and explain in `severity_justification`.

### `primary_axis`

Choose one. Secondary axes go in `secondary_axes` as a list.

- **enforcement-risk** — the item could lead to Prosus or an OpCo being investigated, sanctioned, or required to change conduct.
- **transaction-risk** — the item affects merger control, FDI/FSR, or a deal we are doing, considering, or could be a target of.
- **compliance** — the item affects ongoing compliance obligations (commitments, remedies, conditional clearances, undertakings).
- **strategic-opportunity** — the item creates an opportunity (complaint, leniency advantage, market position) we could use.
- **sector-regulation** — the item affects sector-specific competition rules that interact with our markets but is not primarily an enforcement signal.
- **reputational** — the item affects public competition-law positioning, ESG framing, or external perception, without immediate enforcement or transaction effect.

### `trigger_type`

The trigger types are enumerated to enable mechanical ranking. Select the most specific applicable. If multiple apply, choose the one that drives the rank rule that fires.

- **final_decision** — agency final decision on liability, sanction, or commitment.
- **interim_decision** — interim measures decision, preliminary injunction equivalent.
- **statement_of_objections** — formal preliminary charge.
- **settlement** — Article 9 settlement, commitment decision, TCC, consent decree.
- **court_ruling** — judgment from any court.
- **ag_opinion** — AG opinion at CJEU.
- **guidance_published** — formal guidance or guideline publication.
- **threshold_change** — change to jurisdictional thresholds for merger control, FDI, FSR, or analogous.
- **designation** — gatekeeper designation (DMA), §19a designation (Germany), SMS designation (UK), or analogous.
- **sector_inquiry_opened** / **sector_inquiry_concluded** — opening or conclusion of a sector inquiry or market investigation.
- **dawn_raid_pattern** — disclosed dawn raid or unannounced inspection signalling a pattern.
- **leniency_change** — change to leniency policy, terms, or rewards.
- **remedy_precedent** — a remedy decision setting precedent on behavioural/structural distinction, divestiture timelines, monitoring trustees, or analogous.
- **market_move** — competitor or counterparty market move with competition implications (e.g. a competitor entering a market we operate in).
- **narrative_shift** — sustained agency narrative shift signalled by multiple speeches, working papers, or guidance signals, where no single instrument crystallises it.

### `severity_self_assessment` (1–5)

- **1** — informational only; affects nothing.
- **2** — distant precedent or watching-brief signal; affects how we read future items in the same area.
- **3** — material effect on at least one practice, deal, or compliance obligation; would change a future decision if it lands.
- **4** — material effect on a current practice, deal, or compliance obligation; would change a current decision if it lands.
- **5** — direct effect on a current practice, deal, or compliance obligation that requires action now or imminently.

Always justify in `severity_justification` with reference to the specific practice, deal, or obligation affected, identified from the relevant `needs.md`.

### `confidence`

- **high** — primary source, verbatim quote, no interpretation gap between the source and the finding.
- **medium** — primary source with some interpretation gap, OR strong secondary source (recognised trade press) corroborated by other reporting.
- **low** — single source not yet corroborated, OR primary source with substantial interpretation gap, OR speech/working-paper signal not yet matched by formal instrument.

Per the persona inversion: agency speeches and working papers cap at `confidence: medium` unless a formal instrument follows. SSRN preprints and working papers from recognised competition-policy academics may be filed at `medium` even before peer review, but never `high` until peer-reviewed or cited by an agency.

### `recommended_action_class`

- **monitor** — no action; archive and read again if related items appear.
- **review** — schedule for review at the cadence indicated by the rank rule.
- **act** — Anne-Claire or domain counsel should take a specific action (file a comment, raise internally, brief a deal team, update a protocol).
- **escalate** — does not fit the rank rules cleanly, or sits at the boundary of a Block 3 open question. Route to human triage.

---

## Self-critique pass

Before filing any finding, ask: *"would this survive a sceptical partner asking 'where exactly does it say that?'"* If the answer is no, either downgrade `confidence` or drop the finding entirely. The verbatim anchor quote requirement is the test of this — if the most defensible reading of the quote does not support the body of the finding, the finding fails self-critique.
