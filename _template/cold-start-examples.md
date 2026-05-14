# Cold-start examples — template

Copy this file to `monitors/<monitor>/<domain>/cold-start-examples.md` and
fill it in with **real items the persona has already seen and reacted to**.
Twenty to forty bullets is the target.

Format per bullet:

```markdown
- 👍 [short identifier of the item] — [one-sentence reason]
- 👎 [short identifier of the item] — [one-sentence reason]
```

The leading emoji is parsed by `scripts/bootstrap_feedback.py`. Text after
the emoji becomes the annotation; themes are extracted automatically from
the text by substring matching against `glossary.md` and the persona's
`keywords.md`.

> **Important.** These are bootstrap examples, not real findings. They
> seed the feedback log with `bootstrap: true` and exist to give the
> calibration loop a calibration target on day 1. The persona will
> over-write them with real feedback within weeks.

## Worked examples

- 👍 CMA AI Foundation Models market study (April 2025) — should have surfaced same day; doctrine markers in the title alone.
- 👍 EDPB binding opinion on Article 22 GDPR scope, Dec 2024 — directly on Rule 13 line.
- 👍 N.D. Cal. ruling on AI training-data copyright (June 2024) — Rule 15 territory.
- 👍 Anthropic ToS narrowing indemnity Oct 2024 — vendor change with material commercial impact.
- 👍 ANPD enforcement against iFood recommender — named OC + LGPD ADM doctrine.
- 👎 Random LinkedIn law-firm recap of GPAI Code — restating Tier 1 content; no new signal.
- 👎 Generic AI capability demo (open-source model release without stack relevance) — noise.
- 👎 Op-ed on AI Act from non-specialist outlet — commentary tier, not primary.
- 👎 Tier-3 vendor marketing on AI ethics — promotion, no enforcement nexus.
- 👍 SAMR guidance touching Tencent compliance posture — Rule 6/13 line.
- 👍 Schrems-style DPF fragility update from EDPB — portfolio-wide transfer-mechanism exposure.

[…fill in more as the persona reacts to historical items…]

---

## Change log

| Date | Change | Author |
|---|---|---|
| _add a row when the operator updates the seed set._ | | |
