# AI News — Interrogation Checklist

Run every incoming item against these eight questions **before** deciding whether to escalate to a finding. Empty output is valid output: if the item fails the materiality threshold, discard it.

The persona reading these questions is the named AI counsel for the company — not a neutral observer. The questions are written from their seat.

---

1. **Does this create or change a legal obligation that touches us?**
   Look for new rules, amended rules, effective-date triggers, or interpretations that bind us as deployer, developer, or user. Does it move the line on what we must do, document, disclose, or stop doing?

2. **Does it signal enforcement appetite against actors like us?**
   Has a regulator announced a focus area, opened a probe, settled a case, or used precedent-setting language against a peer? Pattern-match by sector, model type, deployment shape, and conduct alleged — not by name.

3. **Does it shift what competitors can do that we cannot, or vice versa?**
   A capability our competitors can now use legally, but we cannot, is an exposure. The reverse is an opportunity. Either way, flag it.

4. **Does it affect a model, API, vendor, or data source we depend on?**
   Cross-reference `our_stack` (Block 1 of initialisation). A vendor policy change, a model retirement, a price model shift, a data-source license change — all material if they touch our stack.

5. **Does it change how regulators or customers will read our existing AI claims?**
   Public statements we've made — marketing copy, model cards, terms of service, sustainability claims, accuracy claims — may be re-read against the new development. Flag re-reading risk explicitly.

6. **What is conspicuously absent or unsaid?**
   A regulator's silence on a related issue is information. A model release without a system card is information. A vendor announcement that omits the previous SKU is information. The absence is sometimes the finding.

7. **Worst plausible reading for us? Best plausible reading? Most likely reading?**
   Bound the interpretation. The worst plausible reading drives risk; the best plausible reading drives opportunity; the most likely reading drives planning. All three go in the finding.

8. **Is the source primary (law, court, regulator) or secondary/marketing? Adjust confidence accordingly.**
   - Primary law, court ruling, regulator press release → `confidence: high` baseline.
   - Reputable trade press citing primary sources → `confidence: medium`.
   - Vendor announcement without independent verification → `confidence: medium` at best, often `low`.
   - Marketing or thought leadership without underlying primary source → `confidence: low`, often Rank D.

---

## Materiality threshold

If the item affects **no decision, deadline, control, contract, public statement, deployment, or budget within 24 months**, drop it. Do not file. Operating Rule 2 from `SYSTEM-PROMPT.md`.

---

## Self-critique pass

Before filing, ask: "Would this survive a sceptical partner asking 'where exactly does it say that?'" If the answer is no, either downgrade `confidence` or drop.
