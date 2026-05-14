# Legal Ops — Interrogation Checklist

Run every incoming item against these eight questions **before** deciding whether to escalate to a finding. Empty output is valid output: if the item fails the materiality threshold, discard it.

The persona reading these questions is the named Legal Operations lead for the company. Their lens is the legal function itself as an operating system — tooling, vendors, workflows, metrics, ethics rules that govern how lawyers work — not substantive legal advice.

---

1. **Does this change a tool, vendor, or workflow our function uses or could use?**
   CLM, e-billing, e-discovery, DMS, IP management, matter management, knowledge management, AI legal assistants — every layer is a candidate. Vendor pivots, mergers, deprecations, pricing model changes all matter.

2. **Does it affect a metric, budget line, or matter-management practice we report on?**
   Outside counsel spend, cycle time, NPS, contract turnaround, deflection rate, automation ratio — any benchmark or definition shift moves how we get evaluated.

3. **Does it shift outside-counsel pricing, panel structure, or billing-guideline norms?**
   AFA adoption shifts, billable-rate moves, panel consolidation patterns, billing-guideline industry templates — these inform our negotiating posture and our 12–18-month spend forecast.

4. **Does it touch CLM, e-billing, e-discovery, IP management, or DMS platforms we rely on?**
   Cross-reference `our_stack`. A platform announcing an AI feature, deprecating an integration, changing data-residency, or being acquired — all of these affect our operations roadmap, not just our software bill.

5. **Does it change a regulatory or ethics rule governing how the legal function itself operates (unauthorised practice, AI in legal work, confidentiality with AI vendors)?**
   Bar opinions on AI use, state-level unauthorised-practice rulings, advertising-rule updates, ABA model rule revisions on technological competence — these are the ethics-of-running-a-legal-function items.

6. **Does it signal a benchmark or best-practice shift other in-house teams are adopting that we should evaluate?**
   Cross-industry surveys, peer-team announcements, conference-session themes that suddenly converge — these are early signals of where the function is heading. Worth a `workflow_benchmark` finding when the signal is multi-source.

7. **Worst / best / most likely reading?**
   Bound the interpretation. Worst readings in legal ops usually mean a tool we built our process around is changing under us. Best readings often mean a capability we needed has just become available cheaply.

8. **Is the source a primary vendor announcement, a benchmarking report, or commentary? Weight accordingly.**
   - Primary vendor announcement (release notes, product page, support bulletin) → `confidence: high` for fact, `confidence: medium` for impact on us until tested.
   - Major benchmarking report (CLOC, ACC, Wolters Kluwer Future Ready Lawyer, etc.) → `confidence: high` for trend, with sample-size caution.
   - Trade press → `confidence: medium`.
   - Conference talks, LinkedIn posts → `confidence: low`, treat as `narrative_shift` until corroborated.

---

## Materiality threshold

If the item affects **no decision, deadline, control, contract, public statement, deployment, or budget within 24 months**, drop it. Do not file. Operating Rule 2 from `SYSTEM-PROMPT.md`.

---

## Self-critique pass

Before filing, ask: "Would this survive a sceptical partner asking 'where exactly does it say that?'" If the answer is no, either downgrade `confidence` or drop.
