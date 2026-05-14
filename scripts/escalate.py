#!/usr/bin/env python3
"""
escalate.py — out-of-band escalation channel for top-rank findings.

Walks today's findings and identifies items matching the escalation policy
(see strategy.md > Escalation channel). For each match, writes a stub to
findings/escalations/YYYY-MM-DD/ and — if a delivery channel is configured —
posts to it.

Escalation criteria (any of):
  1. Rank A + named Prosus OpCo or Tencent + finding age < 24h.
  2. recommended_action_class = escalate (the persona's flag).
  3. trigger_type = breach_incident with affected_systems_or_practices
     intersecting our_stack (Rule 12 M01 — 72h notification clock).
  4. trigger_type = dawn_raid_pattern (Rule 9 M02).

Delivery channels (configured via env vars; none required to run):
  - ESCALATE_EMAIL_TO       (comma-separated; uses GMAIL_USER + APP_PASSWORD)
  - ESCALATE_SLACK_WEBHOOK  (incoming-webhook URL)
  - ESCALATE_TEAMS_WEBHOOK  (incoming-webhook URL)

Channel posting is best-effort; the audit log records what was sent.
If no channel is configured the script still writes the stub, so the
operator can pick the file up on next review.

Run manually:
    python scripts/escalate.py
    python scripts/escalate.py --dry-run
    python scripts/escalate.py --since 2026-05-14

Hook into CI by adding a step to .github/workflows/scrape.yml after
rank_candidates.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import smtplib
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MONITORS_DIR = ROOT / "monitors"
ESCALATIONS_DIR = ROOT / "findings" / "escalations"
PORTFOLIOS_FILE = ROOT / "portfolios.md"
OUR_STACK_FILES = list(ROOT.glob("monitors/*/our_stack.md"))

NAMED_OPCS_FALLBACK = {
    "iFood", "OLX", "PayU", "iyzico", "Despegar", "Decolar", "eMAG",
    "Just Eat Takeaway", "JET", "Stack Overflow", "GoodHabitz",
    "Swiggy", "Remitly", "Delivery Hero", "EMPG", "dubizzle",
    "Tencent",
}


def parse_frontmatter(md_path: Path) -> dict[str, Any] | None:
    text = md_path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def date_prefix(path: Path) -> date | None:
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", path.stem)
    if not m:
        return None
    try:
        return date(int(m[1]), int(m[2]), int(m[3]))
    except ValueError:
        return None


def named_opcs() -> set[str]:
    """Read portfolios.md to pick up the live OpCo list; fall back to defaults."""
    if not PORTFOLIOS_FILE.exists():
        return NAMED_OPCS_FALLBACK
    out: set[str] = set()
    text = PORTFOLIOS_FILE.read_text(encoding="utf-8")
    for m in re.finditer(r"\*\*([A-Za-z0-9 /+()&.\-]+?)\*\*\s*\|", text):
        name = m.group(1).strip()
        if 2 < len(name) < 50:
            out.add(name)
    return out or NAMED_OPCS_FALLBACK


def named_stack_items() -> set[str]:
    """Read our_stack.md from each monitor to assemble the stack vocabulary."""
    out: set[str] = set()
    for f in OUR_STACK_FILES:
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r"^[-*]\s+\*\*([^*]+?)\*\*", text, flags=re.MULTILINE):
            out.add(m.group(1).strip())
    return out


def should_escalate(fm: dict[str, Any], today: date, opcs: set[str], stack: set[str]) -> str | None:
    """Return the rule that triggered escalation, or None."""
    if fm.get("recommended_action_class") == "escalate":
        return "persona_flag"

    trigger = fm.get("trigger_type")
    if trigger == "dawn_raid_pattern":
        return "dawn_raid_rule_9_M02"

    if trigger == "breach_incident":
        affected = " ".join(str(x) for x in (fm.get("affected_systems_or_practices") or []))
        if any(s.lower() in affected.lower() for s in stack):
            return "breach_clock_rule_12_M01"

    rank = fm.get("rank")
    found = fm.get("_date") or fm.get("date_found")
    if isinstance(found, str):
        try:
            found = date.fromisoformat(found)
        except ValueError:
            found = None
    age_days = (today - found).days if isinstance(found, date) else None

    if rank == "A" and age_days is not None and age_days < 1:
        hay = " ".join(
            str(x) for x in [
                fm.get("source_publisher", ""),
                fm.get("one_sentence_summary", ""),
                *list(fm.get("affected_systems_or_practices") or []),
                *list(fm.get("affected_practices_or_deals") or []),
            ]
        )
        for opc in opcs:
            if opc.lower() in hay.lower():
                return f"rank_a_named_opc:{opc}"

    return None


def write_stub(escalation_dir: Path, fm: dict[str, Any], reason: str, source_path: Path) -> Path:
    escalation_dir.mkdir(parents=True, exist_ok=True)
    slug = source_path.stem
    stub = escalation_dir / f"{slug}.escalation.md"
    body = "\n".join(
        [
            "---",
            f"escalated_at: {datetime.now(timezone.utc).isoformat()}",
            f"reason: {reason}",
            f"source_finding: {source_path.relative_to(ROOT)}",
            f"rank: {fm.get('rank', 'unknown')}",
            f"trigger_type: {fm.get('trigger_type', 'unknown')}",
            "---",
            "",
            f"# Escalation — {fm.get('one_sentence_summary', '(no summary)')}",
            "",
            f"**Reason:** {reason}",
            "",
            f"**Source finding:** `{source_path.relative_to(ROOT)}`",
            "",
            f"**Publisher:** {fm.get('source_publisher', '(unknown)')}",
            "",
            f"**Jurisdiction:** {fm.get('jurisdiction', '(unknown)')}",
            "",
            f"**Action class:** {fm.get('recommended_action_class', '(unset)')}",
            "",
            f"**Severity:** {fm.get('severity_self_assessment', '?')} — {fm.get('severity_justification', '')}",
            "",
            f"**URL:** {fm.get('source_url', '(no link)')}",
            "",
        ]
    )
    stub.write_text(body, encoding="utf-8")
    return stub


def post_slack(webhook: str, summary: str) -> bool:
    try:
        req = urllib.request.Request(
            webhook,
            data=json.dumps({"text": summary}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10).read()
        return True
    except Exception as exc:
        print(f"WARN: slack post failed: {exc}", file=sys.stderr)
        return False


def post_teams(webhook: str, summary: str) -> bool:
    try:
        req = urllib.request.Request(
            webhook,
            data=json.dumps({"text": summary}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10).read()
        return True
    except Exception as exc:
        print(f"WARN: teams post failed: {exc}", file=sys.stderr)
        return False


def post_email(to: list[str], subject: str, body: str) -> bool:
    user = os.environ.get("GMAIL_USER")
    pw = os.environ.get("GMAIL_APP_PASSWORD")
    if not user or not pw:
        print("WARN: GMAIL_USER / GMAIL_APP_PASSWORD not set; skipping email", file=sys.stderr)
        return False
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = user
        msg["To"] = ", ".join(to)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
            s.login(user, pw)
            s.sendmail(user, to, msg.as_string())
        return True
    except Exception as exc:
        print(f"WARN: email send failed: {exc}", file=sys.stderr)
        return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Escalate top-rank findings out-of-band.")
    ap.add_argument("--since", help="Date (YYYY-MM-DD). Defaults to today UTC.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    since = date.fromisoformat(args.since) if args.since else today

    opcs = named_opcs()
    stack = named_stack_items()

    escalated = 0
    today_dir = ESCALATIONS_DIR / today.isoformat()

    for monitor_dir in sorted(MONITORS_DIR.iterdir()):
        if not monitor_dir.is_dir():
            continue
        findings = monitor_dir / "findings"
        if not findings.exists():
            continue
        for md_path in findings.rglob("*.md"):
            if any(s in md_path.parts for s in ("candidates", "feedback", "escalations", "_confidential")):
                continue
            d = date_prefix(md_path)
            if d is None or d < since:
                continue
            fm = parse_frontmatter(md_path) or {}
            fm["_date"] = d
            reason = should_escalate(fm, today, opcs, stack)
            if not reason:
                continue
            escalated += 1
            if args.dry_run:
                print(f"WOULD ESCALATE  {md_path.relative_to(ROOT)}  reason={reason}")
                continue
            stub = write_stub(today_dir, fm, reason, md_path)
            summary = f"[ESCALATION] {fm.get('one_sentence_summary','(no summary)')}\nreason: {reason}\nfile: {md_path.relative_to(ROOT)}"
            slack = os.environ.get("ESCALATE_SLACK_WEBHOOK")
            teams = os.environ.get("ESCALATE_TEAMS_WEBHOOK")
            email_to = [x.strip() for x in (os.environ.get("ESCALATE_EMAIL_TO") or "").split(",") if x.strip()]
            if slack:
                post_slack(slack, summary)
            if teams:
                post_teams(teams, summary)
            if email_to:
                post_email(email_to, f"[ESCALATION] {monitor_dir.name}", summary)
            print(f"ESCALATED  {stub.relative_to(ROOT)}  reason={reason}")

    print(f"\n{escalated} escalations.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
