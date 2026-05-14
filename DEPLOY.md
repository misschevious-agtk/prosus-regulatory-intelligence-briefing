# Deployment runbook — Legal Intelligence Briefing

**Audience:** operator (Klimentina) for v0.1 deployment; internal Prosus tech team for v1.0 onward.

**Status as of 2026-05-13:** v0.1 deploys the website hub only. Article-retrieval pipeline (the actual scraping using the keyword files) is the next build phase, after Anne-Claire's keyword redline lands.

---

## What's ready to deploy

- **Repo root:** `prosus-legal-intelligence-briefing/`
- **Website source:** `website/index.html` (single-page hub, references `./m01/` and `./m02/` which 404 until per-monitor pages are built)
- **Netlify config:** `netlify.toml` (publish directory = `website/`, security headers, redirect rules)
- **Git config:** `.gitignore` (excludes secrets, OS junk)
- **Spec content:** the rest of the repo (monitor specs, profiles, needs, keywords, ranking criteria) — sits inside the repo for source control but is **not** served by Netlify

## Phase 1 — Push to GitHub (your terminal, 5 min)

### 1.1 Open terminal in the briefing folder

```bash
cd "/path/to/Claude Free Ride Project/prosus-legal-intelligence-briefing"
```

### 1.2 Initialise the repo

```bash
git init -b main
git config user.email "klimentina.maleevska@prosus.com"
git config user.name "Klimentina Maleevska"
git add -A
git status        # sanity check: review what's being committed
git commit -m "Initial commit — Legal Intelligence Briefing v0.1

Monitor 01 (Regulatory Intelligence) — four domains: AI News, Privacy & Data
Protection, IP, Legal Ops. Initialisation complete Blocks 1-3.

Monitor 02 (Competition Law) — four reading-modes of single anchor (Anne-Claire
Hoyng): Antitrust & Cartels, Abuse of Dominance, Merger & FDI, Digital Markets,
Sector Regulation & State Aid. Initialisation complete Blocks 1-3, pending
Anne-Claire redline.

Eight keyword files at v1.1 expansion. Conventions documented in
keyword-conventions.md. Website hub at website/index.html."
```

### 1.3 Create GitHub repo and push

**Option A — gh CLI (one command, recommended):**

```bash
# Install gh if missing:
brew install gh

# Authenticate (opens browser):
gh auth login

# Create private repo and push:
gh repo create prosus-legal-intelligence-briefing --private --source=. --remote=origin --push
```

**Option B — manual (if gh CLI is unavailable):**

1. Go to https://github.com/new
2. Repository name: `prosus-legal-intelligence-briefing`
3. **Private** (critical — privileged work product even at v0.1)
4. Do NOT initialise with README, .gitignore, or licence
5. Create repository
6. Back in terminal:

```bash
git remote add origin git@github.com:[your-github-username]/prosus-legal-intelligence-briefing.git
git push -u origin main
```

### 1.4 Verify

Open the repo on github.com. You should see the full folder structure. Confirm `netlify.toml` and `website/index.html` are present.

---

## Phase 2 — Deploy on Netlify (10 min)

### 2.1 Connect

1. Go to https://app.netlify.com
2. Sign in with GitHub (uses your GitHub identity)
3. **Add new site → Import an existing project**
4. Choose **GitHub** as the provider, authorise Netlify if first time
5. Find and select `prosus-legal-intelligence-briefing`

### 2.2 Configure

- Branch to deploy: `main`
- Build settings: **leave them blank**. Netlify reads `netlify.toml` and auto-configures `publish = "website"`.
- Click **Deploy site**

### 2.3 First build

Takes ~30 seconds. You'll get a random URL like `https://lovely-bandicoot-12345.netlify.app`.

### 2.4 Rename and lock

- **Site configuration → Change site name** → set to `prosus-legal-intelligence` (or similar)
- Your live URL becomes `https://prosus-legal-intelligence.netlify.app`

### 2.5 Verify

Open the URL. The hub should render: gradient wordmark, two monitor cards (Monitor 01 + Monitor 02), "Add a monitor" gradient-bordered card, activity feed. Click a monitor card — expected to 404 (per-monitor pages not built yet).

---

## Phase 3 — Lock access (before sharing the URL — 15 min)

Out of the box the Netlify URL is **publicly reachable**. Add auth before sharing with Anne-Claire or external counsel.

### Option A — Netlify Identity (simpler, free tier)

1. **Site configuration → Identity → Enable**
2. **Identity settings:**
   - Registration → **Invite only**
   - External providers → disable (or enable Google if Prosus uses Google Workspace)
   - Email templates → customise the invite email
3. **Invite users one by one:** yourself first, then Anne-Claire when ready. External counsel as they come online.
4. Add a login wrapper to `website/index.html`. I can write this snippet when you're ready — it goes at the bottom of `<body>` as a `<script>` block. Pattern: redirect to login if no token, show the page only after authentication.

### Option B — Netlify Identity with SAML SSO (Prosus-grade, paid)

If Prosus has a SAML SSO provider (Okta, Azure AD, Google Workspace SSO):

1. **Site configuration → Identity → Settings → External providers → SAML SSO**
2. Configure with the IdP metadata your IT team provides
3. Anyone with a `@prosus.com` email logs in via SSO
4. External counsel uses email/password or magic link

Net effect: clean SSO for Prosus staff, controlled email-list for external counsel.

---

## Phase 4 — What's next after Phase 3

### Per-monitor pages (Phase 4a)

The hub links to `./m01/` and `./m02/` which 404 right now. Build the per-monitor dashboards next. Each dashboard shows the four domains, recent findings, the weekly index, the monthly digest, the feedback form per item. I can mock these up when you're ready.

### Email-alert ingestion (Phase 4b.2 — paywalled sources, the legitimate way)

For sources whose articles sit behind paywalls (MLex, FT, premium law firm
content) the route is **not** to scrape the site. The route is to ingest the
publisher's own alert emails. They contain exactly what we need — headline,
deep link, and 1-2 sentence teaser — and using them is what the
subscription's alert feature is for.

`scripts/ingest_email.py` reads a dedicated Gmail inbox via IMAP, parses every
alert from a configured sender (`scripts/email_sources.yml`), runs each item
through the same Tier 1/2 keyword files the RSS scraper uses, and writes
candidate markdown files into `findings/candidates/YYYY-MM-DD/monitor/domain/`
— the same shape `fetch_articles.py` produces, so the Netlify rebuild and the
per-monitor HTML pages render RSS and email candidates identically.

**Step 0 — feasibility check on Prosus Workspace (do this first):**

The Prosus Google Workspace tenant almost certainly disables IMAP and app
passwords by default — both bypass SSO/MFA, so they're the standard things
enterprise IT turns off. Check before doing any other setup:

1. Open `https://myaccount.google.com/apppasswords` while signed into your
   Prosus account. If the page loads and lets you create an app password,
   you're clear. If it says *"The setting you are looking for is not
   available for your account"*, app passwords are blocked.
2. In Prosus Gmail, open *Settings → See all settings → Forwarding and
   POP/IMAP*. If the IMAP section is greyed out or says *"disabled by your
   administrator"*, IMAP is blocked too.

**If either is blocked**, the cleanest workaround is the two-mailbox pattern:

- Create a personal Gmail address dedicated to this (e.g.
  `<initial>.legalbriefing@gmail.com`). App passwords work fine on consumer
  Gmail.
- In Prosus Gmail, set up a filter that auto-forwards alert emails (from
  `*@mlex.com`, `*@ft.com`, plus your law firm sender list) to that personal
  address. *Settings → Forwarding and POP/IMAP → Add a forwarding address*,
  then *Filters → Create a filter → Forward to:*. External forwarding is
  often allowed even when IMAP is not.
- The GitHub workflow reads the personal Gmail, not your Prosus inbox. This
  also tightens the security story: the credential in GitHub never touches
  any Prosus system.

**If both are allowed** on your Prosus account, you can use it directly. The
rest of the setup below is the same either way.

---

**One-time setup (label-scoped — 20 min):**

1. **Pick the inbox** (per Step 0): either your Prosus Workspace account if
   IMAP + app passwords are enabled, or a dedicated personal Gmail receiving
   forwarded alerts. Below refers to that account as "the inbox".
2. **Turn on 2-Step Verification** for the inbox at
   `https://myaccount.google.com/security`. App passwords require 2SV.
3. **Generate an App Password.** `https://myaccount.google.com/apppasswords`
   → App: *Mail*, Device: *Custom — Legal Briefing Bot*. Copy the 16-char
   code. You won't see it again.
4. **Create two Gmail labels** in the inbox:
   - `Briefing/Ingest` — the *input* label. The script reads only messages
     with this label. Everything else in the mailbox is invisible to the
     workflow.
   - `Briefing/Processed` — the *output* label. The script applies this to
     each email it successfully ingests so you can audit what's been touched.
5. **Create a Gmail filter** that auto-applies `Briefing/Ingest` to incoming
   alerts. *Settings → Filters → Create a new filter*. Suggested condition:
   `from:(mlex.com OR ft.com OR <law-firm-domains>)` — refine as you add
   senders. *Actions:* "Skip the inbox" (optional) and "Apply label:
   Briefing/Ingest".
6. **Add two GitHub repo secrets**
   (`Settings → Secrets and variables → Actions → New repository secret`):
   - `GMAIL_USER` = the inbox address
   - `GMAIL_APP_PASSWORD` = the 16-char app password (no spaces)
7. **Subscribe the alerts** (point them at the inbox you picked):
   - **myFT** — log into FT, set up keyword/topic alerts.
   - **MLex** — in MLex Insight, configure email alerts on your topics and
     jurisdictions.
   - **Law firm newsletters** — subscribe from each firm's *Insights* page.
     For each firm, add a `senders:` block to `scripts/email_sources.yml`
     with the firm's domain and (where the newsletter is single-topic) a
     `default` monitor/domain. Also add the firm's domain to the Gmail
     filter so its mail gets labelled `Briefing/Ingest`.
8. **Push the workflow.** First scheduled run after secrets are added will
   pick up any labelled alerts.

**Safety properties of this design (worth knowing for any audit):**

- No paywalled site is ever scraped. Every item ingested came from an email
  the publisher chose to send to a subscribed address.
- The credential stored in GitHub is for a single-purpose mailbox, not your
  MLex login or your FT account. If the secret ever leaks, the worst case is
  someone reads your already-public alert emails — no subscription credentials
  are exposed and no other Prosus systems are reachable.
- Items the script can't confidently route are left unread (not silently
  deleted) so they surface in normal Gmail triage.
- Re-running the workflow is idempotent: candidate filenames are slug-based
  and the writer skips any file that already exists.

---

### Ranker upgrade (Phase 4b.3 — clustering + entity tagging)

`scripts/rank_candidates.py` runs after the two ingest scripts (RSS + email)
and enriches every candidate within a 7-day window in three ways:

- **Entity tagging.** `scripts/lib_entities.py` runs each candidate's title +
  teaser against a curated gazetteer (`scripts/gazetteer.yml` — competition
  regulators, DPAs, IP offices, financial regulators, Big Tech, AI labs)
  plus Prosus portfolio companies parsed at runtime from `portfolios.md`.
  Recognised entities are written into the candidate's frontmatter as
  `entities: [{name, type, jurisdiction, matched_alias}, …]`.

- **Case-citation extraction.** Regex pass that catches EU General Court
  (`T-604/22`), CJEU (`C-376/22`), DG COMP antitrust (`Case AT.40437`), EU
  merger (`M.10999`), state aid (`SA.65541`), UK Court of Appeal, UK High
  Court, UK Supreme Court, CMA merger refs (`ME/6961/24`), and US dockets.
  Stored as `case_numbers: [{scheme, citation}, …]`.

- **Clustering.** `BAAI/bge-small-en-v1.5` (via `fastembed`, ~33MB, CI-friendly)
  embeds each candidate's title + teaser. Items within a rolling 48-hour
  window with cosine similarity ≥ 0.72 are union-found into clusters. Each
  cluster gets one canonical (highest `match_count`, tiebreak earliest
  published, tiebreak alphabetical) and zero or more siblings. New frontmatter
  fields: `cluster_id` (stable, derived from canonical's path), `cluster_role`
  (`canonical` | `sibling`), `cluster_size`, `cluster_canonical_slug`
  (siblings only).

Output: each candidate file is rewritten with the new fields appended to its
frontmatter (body untouched). A daily index lands at
`findings/clusters/YYYY-MM-DD.json` with the full cluster graph for that day
— the per-monitor HTML pages and any future search index can consume that
JSON directly.

**Idempotency.** Cluster IDs are an MD5 prefix of the canonical's path, so a
canonical that survives across days gets the same `cluster_id` every run.
The script is safe to re-run.

**Tuning.** The two knobs worth touching after a week of data are `--threshold`
(0.72 default — raise to 0.78 if too many false merges; lower to 0.65 if
near-duplicates are escaping the cluster) and `--window-days` (7 default — the
look-back range). Run with `--dry-run` to preview without writing.

**What the surface gets for free.** The per-monitor HTML pages can now show:
"6 sources covered this story — view siblings" instead of six separate rows;
filter by entity (e.g. "show only items tagged Apple Inc."); filter by case
number; and aggregate "this case was mentioned in 14 findings over 90 days"
threads. None of that requires a new pipeline — just reading the enriched
frontmatter that's already on disk.

---

### Article-retrieval pipeline (Phase 4b — the "testing articles" goal)

To actually start seeing articles flow into the monitors:

1. **GitHub Action cron job** — runs on the cadences in `operating-preferences.md` (daily for merger-control, twice-weekly for antitrust/abuse, weekly for digital-markets, daily for M01 AI / Privacy / IP, weekly for Legal Ops).
2. **Per-domain fetch script** — reads the relevant `keywords.md`, hits configured sources (RSS feeds first; paid APIs like MLex/GCR/PaRR once Prosus has subscriptions and the API keys are in GitHub Secrets), produces candidate findings.
3. **Claude inference step** — each candidate is passed through the persona's interrogation checklist; the output is a finding MD file written to `findings/` per the `output-schema.md`.
4. **Site rebuild** — Netlify auto-deploys on commit, so new findings appear on the website within a minute.

A minimal v0.1 pipeline can ship within 1-2 days using only free RSS feeds (DG COMP press releases, EU Commission press corner, CJEU RSS, CADE press releases, etc.) — enough to start "testing results of articles" without paid subscriptions. Paid sources land in Phase 4b iteration 2 once licensing is confirmed.

### Feedback writeback (Phase 4c)

Cloudflare Worker or Netlify Function that catches form POSTs from the website and commits them back to the repo as `findings/feedback/YYYY-MM-DD-[monitor]-[item-id].md` via the GitHub API. Authenticated submitter's identity comes from Netlify Identity headers.

### Validation, metrics, escalation (Phase 4d — operational scaffolding)

These ship alongside the article pipeline and run in the same GitHub Action
after `rank_candidates.py`. None require external secrets except
`escalate.py` (optional Slack/Teams webhooks or Gmail credentials).

- **`scripts/validate_findings.py`** — JSON Schema validator against
  `scripts/schemas/finding.schema.json`. Fail the workflow if a candidate
  is malformed.
- **`scripts/test_dedup.py`** — golden-file harness for the cross-monitor
  dedup engine against `scripts/tests/dedup_golden.yml`. Fail on
  regression. Add a new case any time a real-world filing surprised the
  routing.
- **`scripts/compute_metrics.py`** — weekly `state-of-the-monitors-YYYY-WNN.md`
  in `metrics/` plus `website/state.json` for the hub freshness pulse.
  Idempotent; safe to run on every commit.
- **`scripts/escalate.py`** — out-of-band channel for top-rank findings.
  Delivery via email (`GMAIL_USER` + `GMAIL_APP_PASSWORD` reused from
  Phase 4b.2), Slack (`ESCALATE_SLACK_WEBHOOK`), or Teams
  (`ESCALATE_TEAMS_WEBHOOK`). None required; if no channel is set the
  script still writes a stub to `findings/escalations/YYYY-MM-DD/`.
- **`scripts/regulatory_calendar.py`** — surfaces the next-14-day window
  list from `scripts/regulatory_calendar.yml`. Used by the weekly briefing's
  "Coming up" section.
- **`scripts/persona_reconcile.py`** — quarterly diff of `needs.md`
  against feedback themes. Output to
  `monitors/<monitor>/<domain>/_reconciliation/YYYY-QN.md`. Run by the
  operator, not by CI.
- **`scripts/bootstrap_feedback.py`** — seeds a new monitor's feedback log
  from `monitors/<m>/<d>/cold-start-examples.md` (template at
  `_template/cold-start-examples.md`). Day -1 of cold start.
- **`scripts/lib_confidentiality.py`** — pre-filter against the
  `confidential_watchlist.yml` (gitignored). Quarantines privileged or
  leniency-track content before any candidate is written.

CI step ordering (in `.github/workflows/scrape.yml`):

```
fetch_articles.py  →  ingest_email.py  →  rank_candidates.py
                                           ↓
                                  validate_findings.py
                                           ↓
                                       escalate.py
                                           ↓
                                   compute_metrics.py
                                           ↓
                                   (Netlify rebuild)
```

`test_dedup.py` runs on every PR rather than on every scrape.

---

### Internal tech-team handoff (Phase 5)

Once you're past v0.1 and ready to move ownership: fork the repo to the Prosus GitHub org, switch the Netlify site to deploy from there, archive the personal-account repo, and hand the runbook (this file) to the internal tech team. The four-tier keyword conventions, the rank-rule layer, and the persona-and-needs files are all in place for them to operate against.

---

## One pre-push sanity check

Before pushing, eyeball the staging area for anything you don't want on GitHub:

```bash
git status                              # files staged for commit
git diff --cached --stat | head -30     # what's in each file
```

If anything contains real privileged content (live-matter findings, retained-counsel correspondence, leniency-track notes) — pull it before committing. As of v0.1 / v1.1 the repo contains only draft architecture and synthetic placeholders, no real findings, so this should be clean.

---

## Change log

| Date       | Change | Author |
|------------|--------|--------|
| 2026-05-13 | Initial deployment runbook. Phase 1 (GitHub) + Phase 2 (Netlify) + Phase 3 (auth lock). Phases 4a–4c and 5 are forward-pointers for the next build cycles. | Claude (drafted with Klimentina) |
| 2026-05-13 | Added Phase 4b.2 — email-alert ingestion path for paywalled sources (myFT, MLex, law firm newsletters). New script `scripts/ingest_email.py`, config `scripts/email_sources.yml`, two extra requirements (`beautifulsoup4`, `python-dateutil`), and a continue-on-error step in `.github/workflows/scrape.yml` reading `GMAIL_USER` / `GMAIL_APP_PASSWORD` secrets. | Claude (drafted with Klimentina) |
| 2026-05-13 | Added Phase 4b.3 — ranker upgrade with entity tagging + clustering. New scripts `rank_candidates.py`, `lib_entities.py`, gazetteer `gazetteer.yml`. Adds `fastembed` + `numpy` to requirements. New frontmatter fields on every candidate (`entities`, `case_numbers`, `cluster_id`, `cluster_role`, `cluster_size`, `cluster_canonical_slug`, `ranked_at`); daily cluster index emitted to `findings/clusters/YYYY-MM-DD.json`. Idempotent, runs after the two ingest scripts. | Claude (drafted with Klimentina) |
| 2026-05-14 | Added Phase 4d — operational scaffolding. New scripts: `validate_findings.py` (+ `schemas/finding.schema.json`), `test_dedup.py` (+ golden file), `compute_metrics.py`, `escalate.py`, `regulatory_calendar.py` (+ YAML), `persona_reconcile.py`, `bootstrap_feedback.py`, `lib_confidentiality.py` (+ example watchlist). New requirements row: `jsonschema>=4.18.0`. Confidentiality pre-filter wired upstream of candidate writes. Hub freshness pulse added to `website/index.html` reading `website/state.json`. New docs: `glossary.md`, `cadences/persona-reconciliation.md`, `HOW-THIS-THINKS.md`. Cold-start protocol extended with Day -1 feedback bootstrap. M01 Rule 22 added (symmetric with M02 Rule 21). | K. Maleevska (drafted with Claude) |
