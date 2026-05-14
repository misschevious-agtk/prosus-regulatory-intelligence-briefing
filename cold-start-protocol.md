# Cold-Start Protocol

What a brand-new monitor does on day one, when it has no feedback log to learn from. Designed to compensate for the absence of memory by leaning on looser filters, more frequent owner check-ins, and clear exit criteria.

> Read with `README.md` (architecture), `strategy.md` (locked filters + dedup), and `_template/monitor-template.md` (the spec a cold-start monitor is filling out).

---

## Why we need this

A monitor that has been running for six months has accumulated:

- Hundreds of feedback signals shaping source weights.
- A stable understanding of what its persona considers signal vs noise.
- A library of "why it matters" framings tied to the persona's actual decisions.

A monitor on day one has none of that. If it applies the same filters and length cap as a mature monitor, it will either over-prune (the persona sees nothing useful) or be tonally wrong (the persona sees plenty but it doesn't tie back to their needs). The cold-start protocol is a 2-week sprint that closes both gaps fast.

---

## The two-week calibration window

A new monitor runs in **calibration mode** for 14 calendar days from first delivery. Mode is recorded in the monitor's Section 1 ("Status: experimental — calibration mode, day N of 14").

### What changes in calibration mode

| Setting                       | Normal                                    | Calibration mode                                              |
|-------------------------------|-------------------------------------------|---------------------------------------------------------------|
| Prosus Relevance Filter       | Whatever level the spec sets              | **One level looser** than the spec target (tight → medium, medium → loose, loose → no filter beyond locked locks) |
| Daily item cap                | As defined in Section 7                   | **+50%** rounded up, hard ceiling of 15 items                  |
| Length per item               | One-sentence summary                      | Two-sentence summary — extra context helps persona triage      |
| "Why it matters" requirement  | Tied to specific Section 3 need           | Tied to a Section 3 need **plus** a short rationale of why the agent thought it qualified |
| Source tiering                | Tier 1 + Tier 2 routine; Tier 3 secondary | Tier 1 + Tier 2 routine; Tier 3 surfaces with a flag — owner decides whether it's signal |
| Feedback expectations         | 👍 / 👎 as desired                          | **Persona is asked to review every item daily**, even if just thumbs |
| Owner check-in                | Weekly self-review                        | Daily 5-minute check-in for first 3 days, then every 2nd day  |
| Locked filters                | Honoured                                   | **Still honoured — never relaxed.** Calibration only widens user-set layer. |
| Cross-monitor dedup           | Normal (most-specific wins)               | New monitor **always cross-references**, never overrides. Stops it from claiming items that belong to mature monitors before it has earned the assignment. |

The point: a new monitor is allowed to over-surface, but only against the user-set layer. Locked filters and the dedup rule are inviolate.

---

## Day-by-day shape

### Day -1 — Feedback log bootstrap

Before the monitor takes its first scheduled run, seed its feedback log with
**synthetic 👍 / 👎 derived from past decisions** the persona has already
made on items that pre-date the system. Twenty to forty worked examples per
persona is the target.

The intent is not to pretend the monitor has been running for months. The
intent is to give the calibration loop something to anchor against on day 1
instead of starting from a blank slate. Synthetic feedback is clearly tagged
as such and never accumulates beyond the bootstrap.

Mechanics:

1. The operator (or persona anchor) drafts a worked-examples file at
   `monitors/<monitor>/<domain>/cold-start-examples.md`. Each example is
   one bullet:

   ```markdown
   - 👍  CMA AI Foundation Models market study (April 2025) — should have surfaced same day; doctrine markers in the title alone.
   - 👎  Random LinkedIn law-firm post recapping the GPAI Code — restating Tier 1 content, no new signal.
   - 👍  EDPB binding opinion on cross-border ADM under Art. 22 GDPR — Rule 13 (M01) territory.
   ```

2. Run `python scripts/bootstrap_feedback.py --monitor <monitor>`. The
   script reads each example, parses the leading 👍/👎, and writes one
   feedback file per example under `monitors/<monitor>/findings/feedback/`
   with the frontmatter shape `persona_reconcile.py` expects:

   ```yaml
   ---
   vote: up
   bootstrap: true
   themes: ["AI foundation models", "CMA market study"]
   annotation: "doctrine markers in the title alone"
   ---
   ```

3. The themes are extracted automatically from the example text using a
   simple keyword pass against `glossary.md` and the persona's `keywords.md`.

4. `bootstrap: true` is the tag that distinguishes seed feedback from
   real-world feedback. The persona reconciliation script ignores
   bootstrap rows by default but can be told to include them with
   `--include-bootstrap` for sanity checks.

**Why this matters**: a 14-day calibration window with no anchor pulls
the persona harder than necessary. A small seed gives the cold-start
loop a calibration target on day 1 that mostly survives reconciliation,
and the rare cases where the persona disagrees with a seed are
themselves signals worth recording.

**What this is not**: it is not a way to manufacture moat. The real
feedback log builds from real reactions to real findings. The bootstrap
is a primer, not a substitute.

### Days 1–3
- Agent runs at the looser settings above.
- Persona reviews every item, leaves thumbs + a free-text note where the signal is non-obvious.
- Owner does a 5-minute check-in at end of day. Quick adjustments are allowed: changing recency window, adding/removing a source from Section 4, tightening or loosening the Prosus Relevance Filter strictness.
- All adjustments recorded in Section 9 (Change History) with reason.

### Days 4–7
- Agent narrows based on Days 1–3 feedback. Daily cap may already be back to spec if signal-to-noise is good.
- Owner check-in drops to every 2 days.
- Agent writes its first short self-review (Section 8 — Weekly self-review) at Day 7. What worked, what didn't, what it changed.

### Days 8–14
- Agent runs at near-steady-state. Length cap returns to spec; "why it matters" tightens to one rationale.
- Persona feedback frequency naturally drops; that's fine, but persona should still thumbs at least 5 items across this stretch.
- Owner does a Day 14 calibration review (see below).

---

## Day-14 calibration review

A short, structured review between the monitor's owner and its persona. Output is one of three decisions, recorded in Section 9:

1. **Approve into steady state** — strictness restored to spec, cap restored, status changed to `active`. Most common outcome.
2. **Extend calibration by 1 week** — if either side flags meaningful uncertainty (sparse source set, persona traveled and missed days, regulatory news cycle was unusually quiet). Cap stays raised.
3. **Re-spec** — back to drafting. Either persona, sources, purpose, or filters need a real rewrite. Status stays `experimental`.

### Review checklist

The owner asks the persona, on the record:

- Did the briefing surface anything you would have wanted to know but didn't? (Recall check.)
- Was there a class of item that kept appearing and didn't earn its place? (Precision check.)
- Did "why it matters" feel tied to your actual job, or generic? (Framing check.)
- Are the source weights right? Anything missing? Anything dominant for the wrong reason?
- Is the daily cap the right size for your reading time?
- Is delivery time right? (07:30 default may not suit everyone.)

The agent writes the answers into Section 8 (Feedback Log) under a dated heading "Day-14 calibration review".

---

## What the agent must NOT do during cold-start

- **Never relax a locked filter.** Calibration widens the user-set layer only. Locked filters from `strategy.md` and from monitor-specific Section 6 are inviolate.
- **Never claim items as primary from mature monitors.** Always cross-reference. Earned authority comes after Day 14 sign-off.
- **Never silently drop sources.** If a Tier-1 source produced nothing in 7 days, that is logged, not removed.
- **Never auto-raise its own cap.** Owner sign-off only.
- **Never act on a single 👎.** The "one signal not a verdict" rule applies from day one.

---

## What success looks like at Day 14

- Persona says, unprompted, "this is useful — keep it coming."
- Daily 👍 rate ≥ 50% of items, 👎 rate ≤ 15%.
- Source weights have moved on the back of feedback — meaning the agent is learning, not just running.
- At least one cross-reference correctly handed an item to a mature monitor (proves dedup is wired right).
- Section 9 (Change History) has 3–8 documented edits — calibration without churn.

If those conditions don't hold, extend or re-spec. Don't ship a half-formed monitor into the family.

---

## Re-cold-start

A live monitor that undergoes a material spec change — new persona, replaced source list, jurisdiction expansion — re-enters calibration mode for 7 days. Half the duration, same protocol. Logged in Section 9 with reason.

---

## Change log for this file

| Date       | Change                                              | Author |
|------------|-----------------------------------------------------|--------|
| 12 May 2026 | Initial protocol — 14-day window, daily check-in, exit criteria | Group Legal & Public Policy |
| 2026-05-14 | Added Day -1 feedback bootstrap. Helper at `scripts/bootstrap_feedback.py`; worked-examples template lives at `monitors/<m>/<d>/cold-start-examples.md`. Seed rows carry `bootstrap: true` and are ignored by `persona_reconcile.py` by default. | K. Maleevska |
