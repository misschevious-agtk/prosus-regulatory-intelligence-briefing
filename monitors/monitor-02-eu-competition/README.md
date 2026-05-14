# Monitor 02 — Competition Law

## Purpose

Monitor 02 reads external competition-law developments on behalf of Prosus Group. It is split into four domains, each handled as a distinct reading-mode of a single named persona anchor. Its job is to surface what changes Prosus's exposure, obligations, position, or opportunity under competition rules — and to flag anything ambiguous, absent, or worth the worst-case reading. Empty output is valid output: items that affect no practice, deal, deadline, contract, public statement, or commercial decision within 24 months are discarded, not filed.

## Persona anchor

The named anchor for Monitor 02 is **Anne-Claire Hoyng (PhD), Global Head of Competition Policy, Prosus Group**. The four domain profiles are not four different people — they are four reading-modes of the same anchor, calibrated to each domain's specific doctrine and enforcement pattern. P1, P2, P3, and the substantive body of P5 are unitary across all four `profile.md` files; only P4 (posture), P6 (pet concerns), and P7 (escalation threshold) differ between domains.

Her actual profile drives the posture for the whole monitor: PhD in Economics (University of Amsterdam), trained as a competition economist not a lawyer, Dutch Competition Authority (ACM) case-handler background, telecoms sector via KPN and Liberty Global, eight years on platform-MFN frontline at Booking.com, Global Head Competition Policy at Prosus since November 2021, teaches Economics of Competition Law at Utrecht since 2013, publishes on pricing algorithms and the digital-competition toolbox, active on the European competition policy circuit.

## Shape difference from Monitor 01

Three structural inversions relative to the Monitor 01 operational-counsel personas. These are not stylistic preferences; they change source weighting, interrogation order, and rank-rule operation.

**Policy is the operational unit, not enforcement.** Anne-Claire's remit is shaping Prosus's positioning in the policy conversation — Commission consultations, OECD working parties, academic engagement, regulator dialogue, public submissions — at least as much as defending specific enforcement actions. A consultation opening or a CMA call for evidence in our markets is a Rank A trigger candidate even when it produces no immediate enforcement action, because failure to engage is itself the exposure. This is enforced through the parallel "policy/doctrinal signal" question added to each interrogation checklist.

**Academic and policy literature is primary signal, not secondary commentary.** Competition law is unusually tight in how academic literature, agency thinking, and case law cycle through each other. SSRN preprints, the Tilburg/CRESSE/CLEEN/Toulouse working-paper streams, World Competition, European Competition Journal, Journal of Competition Law & Economics, and ECLR are read as primary signal — not as commentary the way trade press is treated in Monitor 01. Agency speeches are directional but capped at `confidence: medium` unless a formal instrument follows. Final decisions and judgments are obviously primary but are *lagging* indicators in competition policy: by the time a decision cites a theory, the policy window for shaping it is usually closed.

**Economics-first instinct.** The interrogation checklists ask about market definition, theories of harm, counterfactuals, efficiencies, and the as-efficient-competitor test before they ask about procedure and precedent. Most in-house competition functions are run by lawyers who consult economists; this one runs the other way and the persona reflects that inversion.

## The four domains

1. **Antitrust & Cartels** (`/antitrust-cartels/`) — Article 101 TFEU / Sherman Act §1 territory: horizontal agreements, cartels, information exchange, hub-and-spoke, vertical restraints, RPM, exclusivity, MFN clauses, dawn raids, leniency.

2. **Abuse of Dominance & Unilateral Conduct** (`/abuse-of-dominance/`) — Article 102 TFEU / Sherman Act §2: dominance assessment, abusive practices (predatory pricing, margin squeeze, refusal to deal, tying, self-preferencing), excessive pricing, gatekeeper conduct.

3. **Merger Control & Foreign Investment Screening** (`/merger-control-fdi/`) — EUMR, national merger regimes, FDI/FSR review, killer acquisitions, gun-jumping, remedies, below-threshold call-ins (Article 22 referrals, Illumina/Grail-style theories).

4. **Digital Markets, Sector Regulation & State Aid** (`/digital-markets-sector-state-aid/`) — DMA, DSA, sector-specific competition rules (telecoms, energy, financial services), state aid (Article 107 TFEU), Foreign Subsidies Regulation, market investigations (UK CMA-style), and the increasingly fuzzy border between competition law and digital regulation.

## How the four domains relate

For any item touching two domains, the finding is filed **once** in the primary domain and cross-referenced in the secondary's index. Findings are never duplicated.

Common dual-domain cases and their primary assignment:

- Merger with abuse-of-dominance theories of harm → primary = `merger-control-fdi`, secondary = `abuse-of-dominance`.
- DMA enforcement action with merger-control overtones (e.g. consolidation among gatekeeper-adjacent platforms) → primary = `digital-markets-sector-state-aid`, secondary = `merger-control-fdi`.
- Trade-association information-exchange finding that triggers an Article 101 case alongside DMA/DSA implications → primary = `antitrust-cartels`, secondary = `digital-markets-sector-state-aid`.
- Sector inquiry concluding with both behavioural remedies (Article 102-flavoured) and market-investigation order (sector-regulation-flavoured) → primary = `digital-markets-sector-state-aid`, secondary = `abuse-of-dominance`.

When in doubt on primary assignment, file in the domain whose reading-mode has the deepest standing question on the item. When still in doubt, mark `recommended_action_class: escalate` and let human triage decide.

## File structure

Mirrors Monitor 01's structure for cross-monitor architectural consistency.

```
/monitors/monitor-02-eu-competition/
  SYSTEM-PROMPT.md                       # CANONICAL operating spec, locked
  README.md                              # This file — monitor overview, status
  output-schema.md                       # SHARED structured-finding schema
  ranking-criteria.md                    # SHARED tier-2 fixed rank rules + Rules 9–21
  operating-preferences.md               # Cadence, output, escalation, confidentiality
  our_markets.md                         # Competition jurisdictions Tier A/B/C/D
  our_stack.md                           # Mirrored from M01; competition-lens annotations
  sectoral-overlays.md                   # Competition-relevant sector subset
  portfolio-map.md                       # Per-OC competition exposure + dominance map
  /antitrust-cartels/
    profile.md                           # [DRAFT — pending Anne-Claire redline]
    needs.md                             # [DRAFT — pending Anne-Claire redline]
    interrogation-checklist.md
    keywords.md                          # Pattern A — four-tier retrieval keywords
  /abuse-of-dominance/
    profile.md                           # [DRAFT — pending Anne-Claire redline]
    needs.md                             # [DRAFT — pending Anne-Claire redline]
    interrogation-checklist.md
    keywords.md                          # Pattern A — four-tier retrieval keywords
  /merger-control-fdi/
    profile.md                           # [DRAFT — pending Anne-Claire redline]
    needs.md                             # [DRAFT — pending Anne-Claire redline]
    interrogation-checklist.md
    keywords.md                          # Pattern A — four-tier retrieval keywords
  /digital-markets-sector-state-aid/
    profile.md                           # [DRAFT — pending Anne-Claire redline]
    needs.md                             # [DRAFT — pending Anne-Claire redline]
    interrogation-checklist.md
    keywords.md                          # Pattern A — four-tier retrieval keywords
  /findings/
    README.md                            # Naming conventions, folder convention at scale
    YYYY-MM-DD-[domain]-[slug].md        # One file per material finding
    INDEX-YYYY-WW.md                     # Weekly index by rank
    BRIEF-YYYY-MM-DD-[domain].md         # Per-domain push briefs
    DIGEST-YYYY-MM.md                    # Monthly digest
    BOARD-SUMMARY-YYYY-QQ.md             # Quarterly board summary
    INCIDENT-YYYY-MM-DD-[slug].md        # As triggered
```

The legacy single-persona spec (`monitor.md`, 9-section, pre-system-prompt) has been archived to `_archive/superseded-pre-system-prompt/monitor-02-eu-competition/monitor.md` with a date-stamped header noting supersession.

## Initialisation status

**Blocks 1, 2, and 3 are now all drafted. All three are pending Anne-Claire's redline. No findings will be filed until all three blocks are signed off.**

### Block 1 — Company context (drafted, pending redline)

Drafted by the operator against Anne-Claire's actual profile and Prosus's public posture. Seven flagged items await her redline:

1. The market-position dominance map (which OpCos read as plausibly dominant for Article 102 purposes).
2. The deal posture and ongoing remedies — specifically the Delivery Hero divestment commitment from the August 2025 JET clearance and any residual iFood TCC obligations.
3. The trade-associations-and-fora list with internal participation protocols.
4. The investigation history inventory.
5. The academic-as-leading-indicator policy decision — whether a Tirole-or-similar working paper proposing a new theory of harm is Rank A material before any agency picks it up, or Rank B until cited.
6. The Tencent attribution rule — whether SAMR Article 102-equivalent action against Tencent reads as direct Prosus exposure, valuation context, or out-of-scope.
7. The Naspers/SACC dimension — whether Prosus and Naspers are treated as a single undertaking for South African Competition Commission purposes (Tier A) or not (drops SA to Tier B).

### Block 2 — Per-domain persona and needs (drafted, pending redline)

Drafted by the operator against Block 1, Anne-Claire's verifiable public profile, and the agreed persona structure (one named anchor, four reading-modes). The four `profile.md` files each carry their own copy of the shared P1, P2, P3, P5 sections with an explicit header note that those sections are unitary across all four — if maintenance pain becomes real, refactor to a shared file is available.

**Design notes for Anne-Claire's redline pass:**

- The four `P4` postures are deliberately distinct: `antitrust-cartels` is most conservative on operational discipline (information exchange, MFN, dawn raids); `abuse-of-dominance` is most academically-led (the doctrinal contestation framing); `merger-control-fdi` is most transactional and remedy-aware (the Delivery Hero remedy is the live operational reality); `digital-markets-sector-state-aid` is most policy-engaged (matching where Anne-Claire's public work most visibly sits). If any of those characterisations are off, the corrections will mostly land in P4 rather than elsewhere.
- The four `P6` lists deliberately reference each other where the same concern bleeds across domains — MFN concerns sit primarily in `antitrust-cartels` but the Booking.com depth shows up in `abuse-of-dominance` reasoning too; Tencent attribution sits across all four. That's intentional, not duplication; the receiving Claude will read all four files and a concern that recurs across domains gets weighted heavier.
- The four `N3` named-entities lists each have a different competitor/comparator set. Worth checking those because the comparator-platform list is what determines which third-party enforcement gets flagged as Prosus-relevant. The Booking Holdings designation under DMA is the most consequential addition for the `digital-markets-sector-state-aid` file, both substantively and because Anne-Claire knows the company.
- The standing questions in `N4` are deliberately different per domain even where they're closely related, because each interrogation checklist drives different reading habits.

**Where Anne-Claire's redline is expected to be heaviest:**

(a) The trade-associations populated list in `antitrust-cartels/needs.md` N3 — shape drafted; her actual list needed.
(b) The dominance map in `abuse-of-dominance/profile.md` P4 and `needs.md` N3 — she has the most defensible internal view of where the line falls.
(c) iFood/CADE TCC or Delivery Hero divestment specifics in `antitrust-cartels` and `merger-control-fdi` P6 — she has the monitoring detail.
(d) The resilience/sovereignty policy posture in `digital-markets-sector-state-aid` P4 — that's the most policy-positioned axis and Anne-Claire's view should drive it.

### Block 3 — Operating preferences and rank-rule additions (drafted, pending redline)

Captured in `operating-preferences.md` (cadence, output format, escalation review, confidentiality framing) and `ranking-criteria.md` (Rules 9–21, eleven domain-specific overrides plus one cross-monitor rule). Of the eight rank-rule questions previously open: five are now resolved by Rules 10, 11, 13, 15, 16; one (academic-as-leading-indicator) is partially resolved via Rule 14 with a split posture awaiting Anne-Claire's confirmation; two remain open (consultation-opened-as-Rank-A would become Rule 22 if confirmed; Naspers/SACC attribution is a Block 1 question).

**Design notes for Anne-Claire's Block 3 redline pass:**

- **Cadence asymmetry across the four domains** (daily for merger, twice-weekly for antitrust and abuse, weekly for digital markets) is a deliberate operational tuning, not a hierarchy of importance. The alternative — uniform twice-weekly across all four with merger getting its own intra-day push channel for deal-clock events — is defensible as an operational preference. The default reflects live-deal-flow context and Delivery Hero monitoring obligations.
- **Confidentiality framing is materially heavier than Monitor 01's.** The four layers (privilege, leniency, information-exchange, cross-monitor coordination) shape how the receiving Claude *drafts* findings, not just how they're distributed. Drafting with privilege in mind affects voice, attribution, and what gets included; getting it wrong creates discoverable record. Worth explicit Anne-Claire sign-off.
- **Rule 21 (Monitor 01 / Monitor 02 cross-reference)** is the first rule that explicitly spans both monitors. Worth confirming that Monitor 01's `ranking-criteria.md` is updated symmetrically — adding the same rule from the Monitor 01 side — so the cross-reference behaviour is symmetric. The CMA AI Foundation Models work is the immediate test case.

**No findings will be filed** until Block 1 redline lands, Block 2 redline lands, and Block 3 sign-off (operating preferences + rank rules + confidentiality framing) is received from Anne-Claire.

## Operational rules (summary)

The full operating rules sit in the system prompt that defines this monitor. Working summary:

- Read every incoming item against the relevant domain's `interrogation-checklist.md`.
- If it fails the materiality threshold, discard. Do not file.
- If material, produce a finding file using `/output-schema.md`. No claim without a verbatim anchor quote (≤25 words).
- Apply `/ranking-criteria.md` mechanically. Tier-2 ranking operates only on enumerated schema fields; never re-read the source to break a tie.
- Cross-reference dual-domain items rather than duplicating.
- Weekly: produce `/findings/INDEX-YYYY-WW.md` by rank.
- Self-critique on every finding: "would this survive a sceptical partner asking 'where exactly does it say that?'" If not, downgrade confidence or drop.
- When in doubt between two ranks, take the lower one. Tier-2's value is consistency, not coverage.
- Never invent URLs, citations, dates, case numbers, or quotes.
