# Metrics

Weekly auto-generated reports on the state of the monitors. Produced by
`scripts/compute_metrics.py`. Read in three places:

1. **Operator weekly review.** `metrics/state-of-the-monitors-YYYY-WNN.md` is
   the human-readable digest. Open it Monday morning; it tells you whether the
   prior week's monitoring was working.
2. **Hub freshness pulse.** `website/state.json` is a small JSON blob the
   website's hub reads at page-load to render last-finding times, item counts,
   and cold-cell warnings.
3. **Coverage health.** `metrics/coverage-health-YYYY-MM.md` is the monthly
   audit of which (persona × jurisdiction) cells produced findings vs. which
   went dark — surfacing blind spots before they become incidents.

## Files in this folder

- `state-of-the-monitors-YYYY-WNN.md` — weekly digest, one per ISO week.
- `coverage-health-YYYY-MM.md` — monthly coverage audit.
- `_latest/` — symlinks (or copies) of the most recent report of each kind so
  the website doesn't have to compute "what's the newest".

## What the weekly report covers

Per monitor and per persona:

- **Items surfaced** (count, broken down by rank A/B/C/D).
- **Feedback** — 👍 / 👎 ratio, free-text annotations count, items reviewed but
  not voted (silence is a signal in cold-start).
- **Dedup hits** — items cross-referenced rather than filed primary, by source
  monitor pair.
- **Source-tier distribution** — what share of findings came from Tier 1
  vs. Tier 2 vs. Tier 3.
- **Locked-filter trips** — how often each locked filter (1–8) fired. A locked
  filter that never fires is dead weight; one that fires a lot is a signal.
- **Confidentiality quarantine count** — derived from the audit log, not the
  content. How many items the pre-filter caught.
- **Cold cells** — (persona × jurisdiction) intersections where no finding
  has landed in 30+ days, flagged for review.

The report is markdown so it diffs cleanly week-over-week.

## What the hub state.json covers

A trimmed projection — just what the hub renders without leaking content:

```json
{
  "generated_at": "2026-05-14T08:00:00Z",
  "monitors": {
    "monitor-01": {
      "last_finding_at": "2026-05-13T17:42:00Z",
      "items_today": 4,
      "items_this_week": 23,
      "cold_cells": ["legal-ops × ZA", "ip × CN"]
    },
    "monitor-02-eu-competition": {
      "last_finding_at": "2026-05-13T11:08:00Z",
      "items_today": 2,
      "items_this_week": 11,
      "cold_cells": []
    }
  }
}
```

Trim is deliberate: no titles, no source URLs, no severity. The hub is a
freshness pulse, not a content reader.
