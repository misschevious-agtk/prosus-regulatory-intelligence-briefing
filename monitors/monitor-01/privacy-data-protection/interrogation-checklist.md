# Privacy & Data Protection — Interrogation Checklist

Run every incoming item against these eight questions **before** deciding whether to escalate to a finding. Empty output is valid output: if the item fails the materiality threshold, discard it.

The persona reading these questions is the named Privacy Counsel for the company. Their lens is binding obligation, not abstract policy interest.

---

1. **Does this affect a lawful basis we currently rely on?**
   Consent, legitimate interest, contractual necessity, legal obligation — each is fragile in its own way. A new DPA opinion, court ruling, or guidance that re-frames how a lawful basis must be evidenced is always material if we rely on the basis in production.

2. **Does it change a data flow we operate (collection, processing, transfer, retention)?**
   Cross-border transfer mechanisms (SCCs, BCRs, adequacy decisions), retention obligations, processor chains, sensitive-category processing — any change here touches the data map.

3. **Does it trigger or alter a notification obligation (breach, DPIA, ADM)?**
   Look for changes to notification thresholds, timing windows, the definition of "high risk," ADM transparency rights, or DPIA scope. Notification obligations are operational, not theoretical.

4. **Does it shift regulator interpretation of a concept we depend on (consent quality, LI balancing, anonymisation threshold)?**
   Concepts that look settled often aren't. A DPA refining what "freely given" means, or a court tightening the anonymisation test, can invalidate work already done.

5. **Is a vendor or processor we use implicated?**
   Cross-reference `our_stack` and the processor list. A DPA fining or sanctioning a processor, a vendor losing certification, or a sub-processor changing locations — all touch our chain.

6. **Does it create a new individual right we must operationalise?**
   New rights mean new request-handling, new SLAs, new tooling. The cost is operational. Flag the right and the operational implication.

7. **Worst / best / most likely reading?**
   Bound the interpretation. For privacy, the worst reading is usually a reinterpretation of an existing concept that invalidates an existing practice; the best is a clarification that confirms our reading; most likely sits between and drives the plan.

8. **Is the source the DPA itself, a court, or a commentator? Weight accordingly.**
   - DPA decisions, guidelines, opinions → `confidence: high`.
   - National court rulings → `confidence: high`, with appellate watchfulness.
   - Article-29 / EDPB working-party material → `confidence: high` for direction, less for binding effect.
   - Trade press summarising the above → `confidence: medium`, confirm against primary.
   - Law-firm commentary → useful for framing only; never sole source.

---

## Materiality threshold

If the item affects **no decision, deadline, control, contract, public statement, deployment, or budget within 24 months**, drop it. Do not file. Operating Rule 2 from `SYSTEM-PROMPT.md`.

---

## Self-critique pass

Before filing, ask: "Would this survive a sceptical partner asking 'where exactly does it say that?'" If the answer is no, either downgrade `confidence` or drop.
