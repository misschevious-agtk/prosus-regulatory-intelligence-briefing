# Monitor 01

Operating for **Prosus N.V.** (Dutch-listed, JSE-secondary-listed global consumer technology group).

Monitor 01 covers four domains, each run by a dedicated lawyer-analyst persona reading on behalf of the company — not as a neutral summariser. The agent surfaces what changes the company's exposure, obligations, position, or opportunity, and flags what is ambiguous, absent, or worth the worst-case reading.

The canonical operating spec is **`SYSTEM-PROMPT.md`** in this folder. Everything in this directory exists to support that spec.

---

## The four domains

| Domain                       | Folder                          | Scope                                                                                                                                                  |
|------------------------------|---------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| **AI News**                  | `ai-news/`                      | Frontier developments, model releases, capability shifts, vendor/ecosystem moves, enforcement actions affecting AI deployers.                          |
| **Privacy & Data Protection** | `privacy-data-protection/`     | GDPR, state privacy laws, cross-border transfers, breach notifications, regulator guidance, DPA enforcement.                                           |
| **Intellectual Property**    | `intellectual-property/`        | Copyright in training data and outputs, patent activity around AI methods, trademark in AI-generated content, trade-secret exposure from model use.    |
| **Legal Ops**                | `legal-ops/`                    | Practice management, tooling, vendor management, e-discovery, CLM, KPI/metrics, in-house function design, operational impact of AI on the legal function. |

Each domain folder contains three files:

- **`profile.md`** — the named persona. Title, seniority, background, posture, trusted sources, pet concerns, threshold for "material". **Populated from operator answers** during initialisation, not invented by the agent.
- **`needs.md`** — the specific, tightly-phrased categories of news that should trigger a finding. **Populated from operator answers** during initialisation.
- **`interrogation-checklist.md`** — the 8-question test the agent runs against every incoming item before deciding whether to escalate. Stable across deployments, drafted by the agent per the system prompt.

---

## How the four domains relate

The domains are **siloed for analysis** (each persona has its own lens, scepticism level, and source taste) but **federated at the schema layer** (every finding writes to the same `output-schema.md` and is ranked by the same `ranking-criteria.md`). That means:

- A single item can be analysed independently by two domains if it truly straddles. But only one of them files the primary finding (per the Operating Rules in `SYSTEM-PROMPT.md`); the other cross-references.
- The findings folder is one flat directory. Domain ownership is recorded in frontmatter, not in folder location.
- Rank, severity, confidence and trigger-type vocabularies are shared. The ranking layer doesn't read prose — it reads enumerated fields, identically, regardless of which domain wrote them.

This setup keeps each persona authentic to their domain (a Privacy Counsel doesn't read an IP case the way an IP Counsel does) while keeping the operations layer mechanical.

---

## Shared canonical files

| File                              | Purpose                                                                                              | Authority |
|-----------------------------------|------------------------------------------------------------------------------------------------------|-----------|
| `SYSTEM-PROMPT.md`                | The operating spec the agent reads at start of every session. Source of truth.                       | Operator  |
| `output-schema.md`                | The exact frontmatter + body shape every finding must use. No claim without a verbatim anchor quote. | Operator (shared) |
| `ranking-criteria.md`             | The set-in-stone tier-2 rank rules + operator-specified Rules 1–8.                                   | Operator (shared) |
| `our_markets.md`                  | Tiered jurisdiction map (A/B/C/D) with named institutions + commercial markets.                      | Operator (shared) |
| `our_stack.md`                    | 9-layer AI stack — foundation models, proprietary models, Toqan, agent infra, AWS, channels, ventures. | Operator (shared) |
| `sectoral-overlays.md`            | 13 sectoral overlays + Rules 7–8 (sectoral upgrade + multi-sector resolution).                       | Operator (shared) |
| `portfolio-map.md`                | Per-OC reality: legal status, regulators, AI systems, IP exposure, bar/ethics jurisdiction. Attention matrix for the four domains. | Operator + agent synthesis |
| `responsible-ai-policy.pdf`       | Group Responsible AI Policy (approved 21 Nov 2025).                                                  | Operator  |
| `responsible-ai-policy-summary.md`| Posture anchor for the four personas. Five principles, four pillars, escalation chain.               | Agent     |
| `findings/`                       | Append-only library of material findings. One file per finding, named `YYYY-MM-DD-[domain]-[slug].md`. | Agent     |

---

## How to spin up Monitor 01

1. Read `SYSTEM-PROMPT.md` end-to-end.
2. Ask the operator Block 1, Block 2 (× 4 domains), and Block 3 of the INITIALISATION section. Wait for answers.
3. Populate the four `profile.md` and four `needs.md` files from the answers.
4. Show populated files to the operator. Wait for sign-off.
5. Begin sifting incoming material.

The four `interrogation-checklist.md` files are already in place — they're stable across deployments and don't require operator input.

---

## Where findings live

Every material finding produces one MD file in `findings/`, named:

```
YYYY-MM-DD-[domain]-[slug].md
```

Domain is one of `ai-news`, `privacy`, `ip`, `legal-ops`. The slug is short and lowercase-hyphenated.

Weekly, the agent produces an index file `findings/INDEX-YYYY-WW.md` listing all findings by rank with one-line summaries.

Findings are append-only. If a finding needs correction, append a new finding with `secondary_axes` referencing the original and a one-line note in open questions — do not edit history.

---

## Status

- **Phase:** **Calibration mode — Day 0 of 14** (per `cold-start-protocol.md`). Initialisation complete; sifting may begin under calibration-mode settings.
- **Block 1 — Company context:** ✅ complete (12 May 2026). Consolidated into `our_markets.md`, `our_stack.md`, `sectoral-overlays.md`, `portfolio-map.md`, `responsible-ai-policy-summary.md`.
- **Block 2 — Persona and needs (× 4):** ✅ populated (12 May 2026). All four `profile.md` and `needs.md` files signed-off from operator side, with named-flag items pending (P3 fill-ins, P2 title choices, Tara Harris confirmations on IP).
- **Block 3 — Operating preferences:** ✅ complete (12 May 2026). Captured in `operating-preferences.md`. Rules 9–21 added to `ranking-criteria.md`. Six document types documented in `findings/README.md`.
- **`interrogation-checklist.md` × 4:** ✅ Drafted per system prompt.
- **`output-schema.md`:** ✅ Locked.
- **`ranking-criteria.md`:** ✅ Locked with operator-specified Rules 1–21.
- **`operating-preferences.md`:** ✅ Locked.
- **`findings/`:** Empty (calibration mode begins on next run). Empty output is valid output.

**Next milestone:** Day 14 calibration review (`cold-start-protocol.md` Section "Day-14 calibration review"). Three exit options: Approve into steady state · Extend calibration by 1 week · Re-spec.
