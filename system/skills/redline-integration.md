---
skill: redline-integration
description: Integrate an anchor's redline on a monitor's Block 1/2/3 spec into the spec itself, with full Change History.
trigger: A queue file named REDLINE-<monitor>-block<N>.md OR explicit operator request.
output: Diff applied to the Block file + Change History row + summary in generated/handoffs/YYYY-MM-DD-<monitor>-redline-summary.md
version: 1.0
last-updated: 2026-05-14
---

# Skill — Redline integration

When a named anchor returns a redline on a Block 1/2/3 spec (the persona profile, the needs, the interrogation checklist, the keywords, the locked filters at the user-set layer), the redline must be integrated into the spec **carefully**. The risks: changing a profile statement breaks the interrogation checklist that depended on it; loosening a user-set filter affects every downstream finding; widening keywords changes the source-scan candidate set tomorrow. This skill takes the anchor's redline and produces the minimal, auditable, reversible change.

## Trigger

- A file at `queue/REDLINE-<monitor>-block<N>.md` containing the anchor's redline (markdown comments, tracked-changes export, or operator's transcription of a conversation).
- Explicit operator request: "integrate Anne-Claire's redline on M02 Block 2 needs".

## Context required

1. `CLAUDE.md` — operating rules (especially Rule 1: locked filters never widened without a `strategy.md` row).
2. The original Block file (`monitors/<monitor>/<domain>/needs.md`, etc.).
3. The redline source — exactly as provided. Do not interpret beyond the literal text.
4. The downstream files that depend on the Block being edited:
   - `needs.md` → `interrogation-checklist.md`, `keywords.md`, `output-schema.md`
   - `interrogation-checklist.md` → `output-schema.md`
   - `keywords.md` → `scripts/sources.yml` (where applicable)
   - `profile.md` → all four of the above
5. The monitor's existing Change History (Section 9).

## Process

1. **Parse the redline.** Produce a numbered list of discrete changes. Each numbered change is one before / one after. If the anchor's redline is prose, normalise it.
2. **Classify each change.**
   - **Editorial** — phrasing only, no behaviour change.
   - **Scope** — adds or removes a domain, a jurisdiction, a doctrine, a portfolio company.
   - **Filter** — changes a locked filter or user-set filter. If locked, **stop** and surface to operator; locked filter changes require `strategy.md` action.
   - **Source** — adds, demotes, removes a source. If removal of a Tier-1 source, **stop** and surface; requires owner sign-off per `strategy.md`.
3. **Trace downstream effects.** For each non-editorial change, list which downstream file(s) need a paired edit. Do not apply the paired edits silently — produce a draft.
4. **Apply the changes.** Write the changes to the Block file. Add a Change History row to the monitor with the date, the redline source (anchor + cycle), and a one-line summary.
5. **Write the summary.** A separate file in `generated/handoffs/` that tells the operator (and the anchor on next cycle): "you asked for X; here is what changed; here is what was downstream-affected; here is what was flagged for your sign-off because it touched a locked filter or Tier-1 source".

## Output format

The Block file: edited in place. The Change History: one row appended. The summary file:

```markdown
---
monitor: <monitor-id>
block: <1 | 2 | 3>
redline-from: <anchor name>
cycle: <week or date>
integrated-by: redline-integration skill v1.0
integrated-at: <ISO-8601>
status: applied | pending-operator-signoff
---

# Redline integration summary — <monitor> — Block <N>

## What the anchor asked for
<numbered list of discrete changes>

## What I changed
<numbered list mapped 1:1 to above, with file paths>

## Downstream edits drafted (not yet applied)
<file paths + one-line description>

## Flagged for your sign-off
<any locked-filter or Tier-1-source changes — these wait for you>

## Change History row
<the exact row added>
```

## Quality bar

- **Never silently widen a locked filter.** Even if the anchor explicitly asks. The skill surfaces and stops.
- **Never silently remove a Tier-1 source.** Same rule.
- **Editorial changes are applied without review.** Anything else is flagged.
- The Change History row is **specific**. "Updated needs" is not acceptable. "Replaced 'AI training data scraping' with 'AI training data scraping where the model is later commercialised in a Prosus operating market'" is.
- Every change is **reversible** because the original is in git history. The skill does not need to keep its own backup; the repo is the backup.

## Skill change-log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-14 | Initial skill. | K. Maleevska |
