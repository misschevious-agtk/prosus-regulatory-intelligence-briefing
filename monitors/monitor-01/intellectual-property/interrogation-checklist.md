# Intellectual Property — Interrogation Checklist

Run every incoming item against these eight questions **before** deciding whether to escalate to a finding. Empty output is valid output: if the item fails the materiality threshold, discard it.

The persona reading these questions is the named IP Counsel for the company. Their lens is exposure on inbound rights and protectability on outbound rights — both directions of the IP balance sheet.

---

1. **Does this change the legal status of training data we use or output we produce?**
   Fair use rulings, text-and-data-mining exception cases, output-copyright eligibility, the scope of "transformative use" — all directly affect whether what we feed in and what we ship out is legally defensible.

2. **Does it affect a license we rely on (inbound or outbound)?**
   Vendor license terms, dataset licenses, open-source compliance, customer-facing license grants. A change in any of these — by case law, contract revision, or vendor announcement — is material.

3. **Does it create a new infringement theory we could be exposed to, or could assert?**
   New theories of harm work both ways. Plaintiff-side novelty is exposure; defence-side novelty is opportunity. A new test for substantial similarity, induced infringement, or contributory liability moves both sides of the table.

4. **Does it touch a vendor's IP indemnity we depend on?**
   Vendor indemnity carve-outs, caps, and conditions are read-on-the-day-you-need-them documents. A vendor changing their indemnity policy, or a court testing one, is material — even if it doesn't affect us today.

5. **Does it set precedent that reframes a previously settled assumption?**
   "Settled" is a frame, not a guarantee. A high-court ruling, an en-banc reversal, or a circuit split forming around an IP doctrine we relied on is always material.

6. **Does it implicate trade-secret exposure through model use by employees?**
   Employees pasting proprietary information into third-party model UIs is a trade-secret risk that depends on the vendor's data-handling commitments. Vendor policy changes, data-retention disclosures, and prompt-leak research all matter here.

7. **Worst / best / most likely reading?**
   Bound the interpretation. Worst readings in IP often invalidate a quiet assumption we made years ago. Best readings sometimes open a defensive door we didn't know was unlocked.

8. **Is this a final ruling, a motion, dicta, or commentary? Weight accordingly.**
   - Final ruling from a court of last resort or settled appellate decision → `confidence: high`.
   - First-instance ruling, pending appeal → `confidence: medium`, watch for upward review.
   - Motion practice, denials of summary judgement → useful as signal, not as precedent. `confidence: medium`.
   - Dicta in an otherwise-unrelated case → `confidence: low`, file as `narrative_shift` rather than ruling.
   - Practitioner commentary → never sole source; framing only.

---

## Materiality threshold

If the item affects **no decision, deadline, control, contract, public statement, deployment, or budget within 24 months**, drop it. Do not file. Operating Rule 2 from `SYSTEM-PROMPT.md`.

---

## Self-critique pass

Before filing, ask: "Would this survive a sceptical partner asking 'where exactly does it say that?'" If the answer is no, either downgrade `confidence` or drop.
