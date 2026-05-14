---
name: M02 Static Workflow
description: The connector. Deterministic pipeline that turns processed intake into ranked, clustered, schema-conformant candidates for the Competition cell.
type: agent
monitor: M02
function: static-workflow
runs: weekly
status: active
---

# M02 Static Workflow

## Mission
Take everything [[02-sourcing-connecting|Sourcing & Connecting]] gathered and produce a ranked, clustered, schema-conformant candidate list for [[04-legal-reasoning|Legal Reasoning]] and the [[05-adjudicator|Adjudicator]]. Same shape as M01's Static Workflow; the differences live in the rules — competition law clusters differently (by firm + case number, not just by topic), and Tier-A sources are heavier here (regulator decisions are primary).

## Inputs
- `clippings/processed/_this-week.md`
- All files in `clippings/processed/<year>/<week>/`
- `findings/instruments/_changed-this-week.md`
- [[../ranking-criteria|ranking-criteria.md]] — the 21 rules
- [[../output-schema|output-schema.md]]
- `scripts/rank_candidates.py`, `scripts/lib_entities.py`, `scripts/gazetteer.yml`
- M01's `_brain/cross-monitor-bridges.md`

## Process
1. **Load.** Read every processed file from the week.
2. **Score.** Apply rules 1–20 in order, with M02-specific weightings:
   - Tier-A weight is higher than in M01 (regulator press releases > journalism on the same story).
   - Stage matters: `#stage/decision` and `#stage/phase-2` weight higher than `#stage/phase-1` and `#stage/commitment` proposals.
   - Theory-of-harm novelty weights positively (new theories matter for precedent).
   - Portfolio-exposure weight is binary AND high — if a Prosus portfolio company is named, score floors at a high value.
3. **Cluster.** Group articles by `(firm OR case-number) + doctrinal area`. A cluster represents *one matter*. The representative is the highest-tier source; ties broken by earliest date.
4. **Rule 21.** Check M01's `_brain/cross-monitor-bridges.md`. The DMA is the chronic overlap; AI Act/competition crossovers are rising. Flag `#rule-21/peer-claim`, downweight, don't drop.
5. **Schema-conform.** Match [[../output-schema|output-schema.md]]. Incomplete candidates go to `findings/_incomplete-YYYY-WW.md`.
6. **Emit.** Write `findings/candidates-YYYY-WW.md` — candidates in rank order, with frontmatter (score, rule trace, cluster members, doctrinal area, firms, instruments/decisions, jurisdiction, Prosus exposure pointer) and body (headline + source + date + lede).

## Cluster rules specific to M02
- A merger filing and its eventual decision are *the same cluster* across the lifetime of the matter. Static Workflow stitches them via case number.
- Appeals are *new clusters* — they cite the original but represent fresh procedural action.
- Commitments / consent decrees are *new clusters* — distinct procedural event.
- Parallel investigations in multiple jurisdictions are *distinct clusters* but linked via the same firm tag (let the Adjudicator decide whether to surface as one global story).

## Outputs
- `findings/candidates-YYYY-WW.md`
- `findings/_incomplete-YYYY-WW.md`

## Failure modes (do not)
- Don't merge parallel-jurisdiction investigations into one cluster. They are legally distinct.
- Don't deflate a candidate because the source is Tier-B if the underlying *fact* (the decision, the filing) is regulator-confirmed elsewhere. Tier governs the source; the fact is the fact.
- Don't drop appellate matters because they're "old news". An appeal is fresh procedural action.
- Don't summarize the article. Headline + source + date + lede only.

## Promotion criteria
- A candidate that combines Tier-A source + Phase II / decision stage + named Prosus portfolio exposure is a default-to-brief item.
- A new theory-of-harm cluster is promoted regardless of portfolio exposure (precedent matters for the whole practice).

## See also
- [[00-orchestrator]] · [[01-regulations]] · [[02-sourcing-connecting]] · [[04-legal-reasoning]] · [[05-adjudicator]]
- [[../ranking-criteria|ranking-criteria.md]] · [[../output-schema|output-schema.md]]
- `scripts/rank_candidates.py`, `scripts/lib_entities.py`
