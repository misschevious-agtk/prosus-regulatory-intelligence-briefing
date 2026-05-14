# Persona reconciliation — cadence

Each persona lives in two places: the **spec** (`needs.md`,
`interrogation-checklist.md`, `keywords.md`) and the **feedback log** (the
running 👍 / 👎 / annotation record under `findings/feedback/`). The two will
drift. The needs file said the persona cared about X; the feedback log shows
the persona has been thumbs-downing X for two months and thumbs-upping Y.
Once a quarter, the spec is reconciled against the log.

> Drift is normal. Drift left undocumented is how monitors become useless.

---

## When

Quarterly. Aim for the first week of January, April, July, October. Out-of-cycle
reconciliation is fine when a 👎 streak crosses ~15 items on a single theme
within four weeks — the helper flags this and surfaces it on the weekly
metrics report.

## Who

The persona's named anchor (where there is one) and the operator. For M01
the operator drives all four domains; for M02 Anne-Claire drives all four
doctrinal lenses.

## What the helper does

`scripts/persona_reconcile.py` reads:

- `monitors/<monitor>/<domain>/needs.md` — the stated needs (extracted as
  bullet items).
- `monitors/<monitor>/findings/feedback/` — the accumulated feedback corpus.

…and produces a diff in three columns:

| Stated in needs.md | Feedback signal | Status |
|---|---|---|
| _"surface ANPD enforcement actions monthly"_ | 14 👎 on ANPD items in last quarter, 0 👍 | **Contradiction** — surface less, or surface only Tier A |
| _"capability demos OK"_ | 0 👎, 0 👍 — silence | **Decay** — needs to be re-explained or dropped |
| (not in needs.md) | 8 👍 on EU AI Act trilogue items in last quarter | **Implicit need** — write it into needs.md |

Output: `monitors/<monitor>/<domain>/_reconciliation/YYYY-QN.md`. Diff is
markdown so it diffs cleanly when the next quarter's pass updates it.

## The decision

For each row, the persona/operator decides one of:

1. **Update the spec.** Persona drift was right; rewrite needs.md or the
   keywords. Record the change in the per-monitor change log.
2. **Recalibrate the feedback.** Persona was reading the world the wrong
   way; the spec stays, but the operator adds explicit thumbs-up examples
   to the cold-start bootstrap so future feedback re-anchors.
3. **Leave it.** Some drift is genuine seasonal variation. Note the call
   in the reconciliation file so next quarter doesn't re-litigate.

## What this is not

- Not a continuous adjustment loop. The whole point is that needs.md is
  stable enough to act on a quarterly cycle, not weekly.
- Not a feedback gate. Individual 👎 still flows to the persona and the
  rank ceiling continues to use feedback. Reconciliation is a separate,
  slower, deliberate step.
- Not a way to silently re-tune the rank rules. Rules 1–22 are spec; if a
  reconciliation suggests a rule change, open a change request against
  `ranking-criteria.md` rather than mutating feedback to compensate.

---

## Change log

| Date       | Change                                              | Author |
|------------|-----------------------------------------------------|--------|
| 2026-05-14 | Initial cadence — quarterly reconciliation, helper. | K. Maleevska (drafted with Claude) |
