# How this thinks

A plain explainer of the architecture for an engineer joining the project.
Reads top-to-bottom in 10–15 minutes. By the end you should be able to open
any file in the repo and know why it exists and what to do with it.

This is the companion to `README.md` (which describes the folder layout)
and `strategy.md` (which states the rules). This file explains the *why*
of the design choices — the load-bearing ones that, if you tweak them
without understanding the rationale, will break things in subtle ways.

If you have to choose one file to keep with you on Phase 5 handoff, keep
this one.

---

## What we are building

A federated network of legal-intelligence monitors for Prosus's Group Legal
and Public Policy function. Each monitor is a long-running agent that:

1. **Scans** a defined set of sources (regulators, courts, specialist
   wires, law-firm bulletins) on a defined cadence.
2. **Filters** what it finds against a Prosus relevance test and a set of
   locked filters (which never bend, regardless of feedback).
3. **Interrogates** each candidate as a domain-specific persona (e.g.
   "in-house IP counsel responsible for AI training data") using a
   checklist of questions that persona always asks.
4. **Produces a finding** — a markdown file with structured frontmatter
   plus a fixed-shape body — only when a candidate clears interrogation.
5. **Ranks** the finding A / B / C / D mechanically from enumerated fields,
   never from prose.
6. **Records feedback** from the human reader and updates its behaviour
   over weeks, not minutes.

We have two monitors live today (M01 — Regulatory horizontal; M02 —
Competition Law) and an architecture that supports many more. The website
is a thin surface that renders findings; the structure is the product.

---

## The four load-bearing design choices

### 1. The structure is the product.

A future Tax team, Treasury, ESG, M&A — anyone — can clone this folder,
swap personas and sources, and run their own monitor network. We trade
some flexibility (every monitor must keep the same 9-section shape) for
a lot of replicability. This trade-off is intentional and worth defending.

The implication for engineering: do not bake monitor-specific logic into
the scanner, ranker, or rendering layer. Anything monitor-specific lives
in `monitors/<monitor>/` — every file there. The scripts/ folder is
deliberately monitor-agnostic; it discovers monitors by walking the
`monitors/` directory.

### 2. The ranker is set in stone.

`monitors/<monitor>/ranking-criteria.md` is not negotiable at run time.
It reads only enumerated fields from finding frontmatter — never prose.
If a rule wants to read prose, the schema is missing a field. You add
the field and backfill, then update the rule. This is the discipline
that prevents quiet drift.

The implication: the rank engine is intentionally narrow. Don't be
tempted to add "if the AG opinion is strongly worded, upgrade by one
tier" because that's prose. Either add a field (`ag_opinion_strength`)
to the schema or live with the lower rank.

### 3. Feedback compounds; spec changes don't.

Feedback (👍 / 👎 / annotations) accumulates daily. The persona uses it
to recalibrate within the bounds the spec allows — never to override
locked filters or rank rules. Spec changes happen quarterly during
persona reconciliation (`cadences/persona-reconciliation.md`), not
continuously.

The implication: never let an agent edit its own spec mid-run. Spec
edits go through the change-log discipline (every monitor's
`ranking-criteria.md` and `keywords.md` has one). Feedback writes flow
freely; spec writes need owner sign-off.

### 4. Locked filters are upstream, the confidentiality pre-filter
is upstream of that.

The order, from outside in:

1. **Confidentiality pre-filter** (`scripts/lib_confidentiality.py`) —
   matches against an internal watchlist of matter codes, leniency
   phrases, and sender domains. Quarantines anything that matches.
   Runs before a candidate file is even written.
2. **Section 4 / Source list** — the monitor's allowed source set, with
   Tier 1 / 2 / 3 weighting.
3. **Section 6 / Locked filters** — system-wide filters from
   `strategy.md`, plus the monitor's own. They cannot be overridden.
4. **Prosus Relevance Filter** — the tight / medium / loose strictness
   per monitor.
5. **Persona interrogation** — domain-specific reasoning, the part the
   LLM does.
6. **Ranker** — mechanical, on enumerated fields only.

This ordering is load-bearing. If you re-order or skip a step, you can
get privileged content into git, or noisy items into the briefing, or
unranked items into Rank A. Don't.

---

## The data model

### Finding

A finding is a markdown file with YAML frontmatter and a six-section body.
Defined per monitor in `monitors/<monitor>/output-schema.md`. The
machine-validated form is `scripts/schemas/finding.schema.json`; run
`scripts/validate_findings.py` to enforce it.

Key frontmatter fields:

| Field | Purpose |
|---|---|
| `date_found` | When the agent surfaced it. Drives the file name and the weekly bucket. |
| `domain` | Which persona owns it. Required for routing and reconciliation. |
| `source_type`, `source_url`, `source_publisher` | Provenance. Drives source-tier classification (in `compute_metrics.py`). |
| `trigger_type` | The single most important rank input. Pick precisely. |
| `severity_self_assessment` | 1–5. Set by the persona; read by the ranker. |
| `recommended_action_class` | `monitor` / `review` / `act` / `escalate`. Drives both rank and the escalation channel. |
| `confidence` | `low` / `medium` / `high`. Affects rank and downstream filtering. |
| `affected_systems_or_practices` | Multi-valued list. Joins to `our_stack.md` for in-stack tests. |
| `cluster_id`, `cluster_role` | Set by the ranker after `rank_candidates.py` runs. Lets the website group siblings. |

### Candidate

The output of `fetch_articles.py` (RSS) and `ingest_email.py` (email).
Same shape as a finding but produced before persona interrogation.
Lives under `findings/candidates/YYYY-MM-DD/monitor/domain/`. The
persona reads the candidate, applies the interrogation checklist, and
either drops it or promotes it to a finding in `findings/`.

### Feedback

A markdown file under `findings/feedback/YYYY-MM-DD-<id>.md` recording
one of:

- `vote: up | down`
- `annotation: "free text"`
- `themes: [...]` (operator-tagged) — used by `persona_reconcile.py`

Feedback never modifies findings; it accumulates and shifts persona
behaviour over time.

### Escalation

A stub under `findings/escalations/YYYY-MM-DD/<slug>.escalation.md`,
created by `scripts/escalate.py` whenever an out-of-band trigger fires.
Stubs include the reason and source-finding path; never the body.

### Confidentiality quarantine

An opaque stub under `findings/_confidential/YYYY-MM-DD/<sha>.stub.md`
plus an append-only JSONL audit log at
`findings/_confidential/_audit-log.jsonl`. Body is dropped on entry.

---

## The pipeline

```
                +----------------------------+
                |   email + RSS sources      |
                +-------------+--------------+
                              |
              fetch_articles.py / ingest_email.py
                              |
                +-------------v--------------+
                |   confidentiality filter   |   <-- lib_confidentiality.py
                |   (quarantine on match)    |
                +-------------+--------------+
                              |
                              v
                  findings/candidates/YYYY-MM-DD/...
                              |
                              v
                       rank_candidates.py
                  (entity tagging + clustering)
                              |
                              v
                        validate_findings.py
                              |
                              v
                          escalate.py
                              |
                              v
                       compute_metrics.py
                  (weekly report + state.json)
                              |
                              v
                  +-----------------------+
                  |  Netlify auto-deploys |
                  +-----------------------+
```

Each script is independently runnable and idempotent. Re-running over the
same inputs produces the same outputs.

---

## The folder map

```
prosus-legal-intelligence-briefing/
├── README.md                  ← what this is and how to clone
├── strategy.md                ← rules, locked filters, dedup, confidentiality, escalation
├── portfolios.md              ← coverage matrix
├── glossary.md                ← domain language
├── cold-start-protocol.md     ← how a fresh monitor behaves
├── keyword-conventions.md     ← four-tier keyword pattern
├── HOW-THIS-THINKS.md         ← this file
├── DEPLOY.md                  ← deployment runbook
│
├── cadences/                  ← non-content operational doctrines
│   └── persona-reconciliation.md
│
├── _template/                 ← read-only legacy single-persona archetype
├── _archive/                  ← superseded specs
│
├── monitors/
│   ├── monitor-01/
│   │   ├── SYSTEM-PROMPT.md
│   │   ├── output-schema.md
│   │   ├── ranking-criteria.md
│   │   ├── operating-preferences.md
│   │   ├── our_markets.md / our_stack.md / sectoral-overlays.md / portfolio-map.md
│   │   ├── <domain>/{profile,needs,interrogation-checklist,keywords}.md
│   │   └── findings/
│   │       ├── candidates/         (scraper output)
│   │       ├── feedback/           (votes + annotations)
│   │       ├── escalations/        (out-of-band stubs)
│   │       ├── _confidential/      (quarantine — gitignored)
│   │       └── (findings themselves at top level)
│   └── monitor-02-eu-competition/  ← same shape
│
├── scripts/
│   ├── fetch_articles.py
│   ├── ingest_email.py
│   ├── lib_confidentiality.py
│   ├── confidential_watchlist.example.yml
│   ├── rank_candidates.py
│   ├── lib_entities.py / gazetteer.yml
│   ├── validate_findings.py / schemas/finding.schema.json
│   ├── escalate.py
│   ├── regulatory_calendar.py / regulatory_calendar.yml
│   ├── compute_metrics.py
│   ├── persona_reconcile.py
│   ├── test_dedup.py / tests/dedup_golden.yml
│   └── sources.yml / email_sources.yml / requirements.txt
│
├── metrics/                   ← weekly state-of-the-monitors + monthly coverage
├── exports/                   ← anything cut for external sharing
└── website/
    ├── index.html             ← hub
    └── state.json             ← regenerated by compute_metrics.py
```

---

## What you should not touch without thinking hard

- `monitors/<monitor>/ranking-criteria.md` — read the change-log
  discipline in that file first. Rule numbers are stable identifiers
  referenced from elsewhere.
- `strategy.md` — every monitor inherits from this. Edits cascade.
- `output-schema.md` — backfill or break. There is no third option.
- The 9-section monitor shape. Reordering a section breaks the cloning
  story.
- `confidential_watchlist.yml` — gitignored on purpose; never copy the
  real file into the repo or into a CI variable.

---

## What you can change freely

- Per-domain `keywords.md` files — Tier 1 / 2 are the scraper input;
  Tier 3 / 4 are persona-only.
- Source lists in each monitor's Section 4 (subject to the locked-filter
  rule that official-register sources can't be removed without sign-off).
- Cadences and cap volumes in `operating-preferences.md`.
- Anything in `scripts/` that is monitor-agnostic, as long as you keep
  the contract clean (read frontmatter, write frontmatter, treat
  monitors as discoverable).
- Anything in `website/` that doesn't change the data model.

---

## The first day on the job

If you've just inherited this, do these in order:

1. Clone the repo locally. Read `README.md`, this file, then `strategy.md`.
2. Run `pip install -r scripts/requirements.txt --break-system-packages`.
3. Run `python scripts/test_dedup.py` — confirms the engine works.
4. Run `python scripts/compute_metrics.py` — emits an empty state.json
   if there are no findings yet, which is the expected state during
   cold-start.
5. Run `python scripts/regulatory_calendar.py` — sanity check.
6. Open `website/index.html` locally — the freshness strip should
   render either real numbers (if state.json is populated) or the
   placeholder copy.
7. Skim one full monitor end-to-end: `monitors/monitor-01/SYSTEM-PROMPT.md`
   → `output-schema.md` → `ranking-criteria.md` → `ai-news/profile.md`
   → `ai-news/needs.md` → `ai-news/interrogation-checklist.md` →
   `ai-news/keywords.md`. That's the persona stack for one domain.
8. Read the change-logs at the bottom of each spec file. They tell you
   *why* a rule exists.
9. Read `DEPLOY.md` end-to-end. That's the production posture.
10. Only then make a change.

---

## Change log

| Date       | Change                                                 | Author |
|------------|--------------------------------------------------------|--------|
| 2026-05-14 | Initial engineering handoff explainer for Phase 5.     | K. Maleevska (drafted with Claude) |
