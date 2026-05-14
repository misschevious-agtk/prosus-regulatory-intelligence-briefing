# Responsible AI Policy — Summary

> The full policy lives at `responsible-ai-policy.pdf` in this folder. Approved **21 November 2025**. This summary exists so the four Monitor 01 personas can anchor "posture" sections against group commitments without re-reading the PDF on every run.

---

## What the policy says (load-bearing extracts)

### Scope
Applies to **Prosus N.V. and all subsidiaries** ("Prosus group companies"). M&A activity is **explicitly in scope** — the policy is one of the standards Prosus uses when evaluating acquisitions, investments, and partnerships.

### Accountability
- **Operating-company CEOs hold ultimate responsibility** for responsible AI within their businesses.
- Each business must **designate appropriate AI-governance stakeholders**.
- The Group provides **oversight and guidance**.

### Five guiding principles
1. **Force for good** — AI applications should benefit customers, the company, stakeholders, and society at large.
2. **Technical excellence and robustness** — scientific and technical standards on par with global best practice.
3. **Fairness and inclusivity** — avoid creating unfair biases, avoid reinforcing or exacerbating existing biases.
4. **Accountability and transparency** — designers have an ongoing duty to document, monitor, and control performance; outputs context-sensitive, transparent, explainable.
5. **Privacy and security** — training and deployment data proportionate, conformant with data-protection laws; security threats minimised through technical and organisational measures.

### Four pillars of the operating framework
- **Govern** — each company specifies and publishes its own governance principles; jurisdictions with specific AI laws (including the **EU AI Act, named explicitly**) require compliance.
- **Design** — privacy, security, transparency, bias controls, and robustness built in.
- **Monitor** — auditing for accountability, bias, and risks; proactive cross-disciplinary cooperation.
- **Train** — every employee expected to become well-acquainted with company AI tools and actively use them.

### Group support and monitoring
- **Group AI team + AI and ethics working group** — primary implementation engine. Supports businesses on responsible-AI implementation, legal compliance, regulatory engagements, AI risk assessments, M&A AI implications.
- **Executive training** on responsible and ethical AI.
- **Risk committee of the Prosus board** reviews this policy and its implementation **annually**.
- External contact: **`privacy@prosus.com`**.

---

## What this means for the four Monitor 01 personas

### Anchor for "posture" sections
Each persona's `profile.md` "posture" section should be **consistent with these five principles**, not in tension with them. The personas read on behalf of the company, but they read **inside the frame the policy sets** — so:

- The AI News persona's posture on **frontier capability deployment** must respect "technical excellence and robustness" — meaning a hot capability demo without robust performance evidence is **not material** in the way a robust capability would be.
- The Privacy persona's posture on **lawful basis** is shaped by the policy's "proportionate" language on training and deployment data — proportionality is the binding test, not minimum-compliance.
- The IP persona's posture on **inbound rights** is shaped by the policy's commitment to deploy AI built on properly-licensed inputs.
- The Legal Ops persona's posture on **AI in the legal function itself** is shaped by the same "train" pillar that applies to every employee — including in-house counsel using AI tools is expected, not exceptional.

### Anchor for "what 'material' means to them"
The policy implies the **escalation chain**: persona → Group AI team / AI and ethics working group → operating-company CEO → board risk committee. Each persona's materiality threshold should anchor at "what would reasonably move up this chain" rather than at the lower threshold of "what is interesting."

### Anchor for source weighting
- **Group AI team outputs** (training, workshops, internal guidance) are primary sources for the Legal Ops persona and inform the AI News persona's "what is Prosus doing" baseline. Treat as Tier-1 internal.
- **AI and ethics working group decisions** are Tier-1 internal — they are functionally regulatory for the operating companies and should be tracked as such.
- **`privacy@prosus.com` external queries that result in policy action** become Tier-1 internal once the action lands.

---

## What the policy does NOT say (worth knowing)

> Per the discipline in `output-schema.md` body section "What the source does not say."

- **No named acceptable-use list.** The policy does not enumerate prohibited use cases beyond the principles. Each operating company defines its own.
- **No prohibition on specific vendor classes or geographies.** Nothing in the policy prevents use of Chinese-origin models (Qwen, etc.) or US-origin frontier models. Vendor selection is operational, not policy.
- **No specific audit cadence** beyond the annual board risk-committee review. Bias auditing, model-risk audits, and conformity-assessment cadence are left to operating-company implementation.
- **No detail on the "AI and ethics working group" composition or charter.** External-facing only; internal charter is referenced but not summarised.
- **No specific reference to high-risk vs. GPAI distinctions** under the EU AI Act. The policy notes EU AI Act compliance is required but does not pre-commit to a classification posture.

---

## How Monitor 01 findings travel

Per the policy's accountability structure:

```
Source event
  →  Persona reads against domain interrogation-checklist
  →  Persona files finding (output-schema.md)
  →  Ranker assigns Rank A/B/C/D (ranking-criteria.md)
  →  Rank A escalations → Group AI team + AI and ethics working group
  →  Material escalations → operating-company CEO + Group Legal & Public Policy
  →  Annual: board risk committee policy review
```

The **persona is the first step in this chain**. The "Why it matters to us" body field on every finding should be readable by the next link in the chain (Group AI team, working group, CEO) without further explanation — the chain is the audience, the persona is the author.

---

## Change log

| Date       | Change                                                                          | Author |
|------------|---------------------------------------------------------------------------------|--------|
| 2026-05-12 | Initial summary of approved 21 November 2025 policy. PDF stored alongside.      | Agent  |
