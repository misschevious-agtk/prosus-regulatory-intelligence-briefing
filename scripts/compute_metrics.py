#!/usr/bin/env python3
"""
compute_metrics.py — weekly metrics report + website state.json.

Walks every monitor's findings, reads the YAML frontmatter, joins with the
feedback log (any markdown file under findings/feedback/), and emits two
artefacts:

  metrics/state-of-the-monitors-YYYY-WNN.md   — human-readable weekly digest
  website/state.json                          — trimmed projection for the hub

If --coverage is also passed, emits the monthly coverage audit:

  metrics/coverage-health-YYYY-MM.md

Designed to be cheap and re-runnable. Output is deterministic for a given
state of `findings/`, so re-running mid-week overwrites the same week's report.

Run manually:
    python scripts/compute_metrics.py
    python scripts/compute_metrics.py --coverage
    python scripts/compute_metrics.py --week 2026-W19

Hook into CI by adding a step to .github/workflows/scrape.yml after the
ranker — keeps the hub's freshness pulse current on every scrape.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
MONITORS_DIR = ROOT / "monitors"
METRICS_DIR = ROOT / "metrics"
WEBSITE_STATE = ROOT / "website" / "state.json"
COVERAGE_FILE_TEMPLATE = "coverage-health-{year}-{month:02d}.md"
WEEKLY_FILE_TEMPLATE = "state-of-the-monitors-{year}-W{week:02d}.md"

COLD_CELL_DAYS = 30

# --- frontmatter parsing -----------------------------------------------------

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


# --- finding + feedback collection ------------------------------------------

def collect_findings(monitor_dir: Path) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    findings = monitor_dir / "findings"
    if not findings.exists():
        return out
    for md_path in findings.rglob("*.md"):
        if "candidates" in md_path.parts:
            continue
        if "feedback" in md_path.parts:
            continue
        if "_confidential" in md_path.parts:
            continue
        if not md_path.stem[:4].isdigit():
            continue
        fm = parse_frontmatter(md_path) or {}
        fm["_path"] = str(md_path.relative_to(ROOT))
        fm["_date"] = date_prefix(md_path)
        fm["_monitor"] = monitor_dir.name
        out.append(fm)
    return out


def collect_feedback(monitor_dir: Path) -> list[dict[str, Any]]:
    """Feedback files live at findings/feedback/YYYY-MM-DD-*.md."""
    out: list[dict[str, Any]] = []
    fdir = monitor_dir / "findings" / "feedback"
    if not fdir.exists():
        return out
    for md_path in fdir.rglob("*.md"):
        fm = parse_frontmatter(md_path) or {}
        fm["_path"] = str(md_path.relative_to(ROOT))
        fm["_date"] = date_prefix(md_path)
        fm["_monitor"] = monitor_dir.name
        out.append(fm)
    return out


# --- aggregations -----------------------------------------------------------

def iso_week_range(when: date) -> tuple[date, date, int, int]:
    """ISO year-week tuple (start, end_inclusive, year, week)."""
    year, week, _ = when.isocalendar()
    start = date.fromisocalendar(year, week, 1)
    end = start + timedelta(days=6)
    return start, end, year, week


def items_in_range(items: list[dict[str, Any]], start: date, end: date) -> list[dict[str, Any]]:
    return [it for it in items if it.get("_date") and start <= it["_date"] <= end]


def rank_distribution(items: Iterable[dict[str, Any]]) -> dict[str, int]:
    out = {"A": 0, "B": 0, "C": 0, "D": 0, "unranked": 0}
    for it in items:
        rank = it.get("rank")
        if rank in out:
            out[rank] += 1
        elif rank in ("a", "b", "c", "d"):
            out[rank.upper()] += 1
        else:
            out["unranked"] += 1
    return out


def by_domain(items: Iterable[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for it in items:
        counts[str(it.get("domain", "unknown"))] += 1
    return dict(counts)


def by_source_tier(items: Iterable[dict[str, Any]]) -> dict[str, int]:
    """Tier inferred from source_type. Aligned with strategy.md source-tier model."""
    TIER_1 = {
        "primary-law", "court-ruling", "regulator-guidance", "enforcement-action",
        "commission-decision", "nca-decision", "court-judgment", "ag-opinion",
        "statement-of-objections", "settlement", "guidance",
    }
    TIER_2 = {"trade-press", "market-investigation", "sector-inquiry", "speech"}
    TIER_3 = {"academic", "marketing", "vendor-announcement", "other"}
    counts = {"tier_1": 0, "tier_2": 0, "tier_3": 0, "uncategorised": 0}
    for it in items:
        t = it.get("source_type")
        if t in TIER_1:
            counts["tier_1"] += 1
        elif t in TIER_2:
            counts["tier_2"] += 1
        elif t in TIER_3:
            counts["tier_3"] += 1
        else:
            counts["uncategorised"] += 1
    return counts


def feedback_summary(feedback: Iterable[dict[str, Any]]) -> dict[str, int]:
    summary = {"up": 0, "down": 0, "annotations": 0, "silent_reviews": 0}
    for fb in feedback:
        vote = str(fb.get("vote", "")).lower()
        if vote in ("up", "👍", "thumbs_up"):
            summary["up"] += 1
        elif vote in ("down", "👎", "thumbs_down"):
            summary["down"] += 1
        if fb.get("annotation"):
            summary["annotations"] += 1
        if fb.get("reviewed") and not vote:
            summary["silent_reviews"] += 1
    return summary


def dedup_hits(items: Iterable[dict[str, Any]]) -> int:
    return sum(1 for it in items if it.get("cluster_role") == "sibling" or it.get("cross_reference_to"))


def cold_cells(items: list[dict[str, Any]], today: date) -> list[str]:
    """(domain × jurisdiction) intersections with no finding in COLD_CELL_DAYS."""
    last_seen: dict[tuple[str, str], date] = {}
    domains: set[str] = set()
    jurisdictions: set[str] = set()
    for it in items:
        if not it.get("_date"):
            continue
        dom = str(it.get("domain", "unknown"))
        jur = str(it.get("jurisdiction", "unknown")).split("|", 1)[0].strip()
        if not dom or not jur:
            continue
        domains.add(dom)
        jurisdictions.add(jur)
        key = (dom, jur)
        prev = last_seen.get(key)
        if prev is None or it["_date"] > prev:
            last_seen[key] = it["_date"]
    cold = []
    threshold = today - timedelta(days=COLD_CELL_DAYS)
    # Only flag cells we expected to see at all (observed in last 12 months).
    for (dom, jur), seen in last_seen.items():
        if seen < threshold:
            cold.append(f"{dom} × {jur}  (last: {seen.isoformat()})")
    return sorted(cold)


# --- reports ----------------------------------------------------------------

def render_weekly_md(generated_at: datetime, week_year: int, week_num: int,
                     per_monitor: dict[str, dict[str, Any]]) -> str:
    lines = [
        f"# State of the Monitors — {week_year} W{week_num:02d}",
        "",
        f"_Generated {generated_at.isoformat()}_",
        "",
        "## Summary",
        "",
        "| Monitor | Items this week | A / B / C / D | 👍 / 👎 | Dedup hits | Cold cells |",
        "|---|---|---|---|---|---|",
    ]
    for monitor, m in per_monitor.items():
        ranks = m["ranks"]
        rank_str = f"{ranks['A']} / {ranks['B']} / {ranks['C']} / {ranks['D']}"
        fb = m["feedback"]
        fb_str = f"{fb['up']} / {fb['down']}"
        lines.append(
            f"| {monitor} | {m['count']} | {rank_str} | {fb_str} | {m['dedup_hits']} | {len(m['cold_cells'])} |"
        )

    for monitor, m in per_monitor.items():
        lines += [
            "",
            f"## {monitor}",
            "",
            f"- Items this week: **{m['count']}**",
            f"- Rank distribution: A {m['ranks']['A']} · B {m['ranks']['B']} · C {m['ranks']['C']} · D {m['ranks']['D']} · unranked {m['ranks']['unranked']}",
            f"- By domain: {format_dict(m['by_domain'])}",
            f"- By source tier: T1 {m['by_tier']['tier_1']} · T2 {m['by_tier']['tier_2']} · T3 {m['by_tier']['tier_3']} · uncategorised {m['by_tier']['uncategorised']}",
            f"- Feedback: 👍 {m['feedback']['up']} · 👎 {m['feedback']['down']} · annotations {m['feedback']['annotations']} · silent reviews {m['feedback']['silent_reviews']}",
            f"- Dedup hits (siblings + cross-refs): {m['dedup_hits']}",
            f"- Quarantined this week: {m['quarantined']}",
            f"- Cold cells (no finding in {COLD_CELL_DAYS}+ days):",
        ]
        if m["cold_cells"]:
            for cc in m["cold_cells"]:
                lines.append(f"  - {cc}")
        else:
            lines.append("  - none")

    lines += [
        "",
        "## Reading the report",
        "",
        "- Cold cells are not a verdict. _No news is news_ for some weeks; investigate when a Tier A cell goes cold.",
        "- A locked-filter trip count near zero is normal early in cold start. A monitor running for >60 days with zero trips suggests the filter is dead weight; investigate.",
        "- Single 👎 is a signal, not a verdict. Patterns across a week are the unit of analysis.",
        "",
    ]
    return "\n".join(lines)


def format_dict(d: dict[str, int]) -> str:
    if not d:
        return "—"
    return ", ".join(f"{k} {v}" for k, v in sorted(d.items()))


def quarantined_in_range(start: date, end: date) -> int:
    """Count audit-log rows in [start, end]."""
    audit = ROOT / "findings" / "_confidential" / "_audit-log.jsonl"
    if not audit.exists():
        return 0
    n = 0
    for line in audit.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
            when = datetime.fromisoformat(row["ts"]).date()
        except Exception:
            continue
        if start <= when <= end:
            n += 1
    return n


# --- main -------------------------------------------------------------------

def parse_week_arg(arg: str) -> tuple[int, int]:
    m = re.fullmatch(r"(\d{4})-W(\d{2})", arg)
    if not m:
        raise argparse.ArgumentTypeError(f"--week must be YYYY-WNN, got {arg}")
    return int(m[1]), int(m[2])


def main() -> int:
    ap = argparse.ArgumentParser(description="Emit the weekly metrics report and website state.json.")
    ap.add_argument("--week", help="ISO week (YYYY-WNN). Defaults to current week.")
    ap.add_argument("--coverage", action="store_true", help="Also emit the monthly coverage audit.")
    args = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    if args.week:
        year, week = parse_week_arg(args.week)
        start = date.fromisocalendar(year, week, 1)
        end = start + timedelta(days=6)
    else:
        start, end, year, week = iso_week_range(today)

    if not MONITORS_DIR.exists():
        print(f"ERROR: monitors/ not found at {MONITORS_DIR}", file=sys.stderr)
        return 2

    per_monitor: dict[str, dict[str, Any]] = {}
    state_monitors: dict[str, Any] = {}

    for monitor_dir in sorted(MONITORS_DIR.iterdir()):
        if not monitor_dir.is_dir():
            continue
        findings = collect_findings(monitor_dir)
        week_items = items_in_range(findings, start, end)
        feedback = collect_feedback(monitor_dir)
        week_feedback = items_in_range(feedback, start, end)

        per_monitor[monitor_dir.name] = {
            "count": len(week_items),
            "ranks": rank_distribution(week_items),
            "by_domain": by_domain(week_items),
            "by_tier": by_source_tier(week_items),
            "feedback": feedback_summary(week_feedback),
            "dedup_hits": dedup_hits(week_items),
            "cold_cells": cold_cells(findings, today),
            "quarantined": quarantined_in_range(start, end),
        }

        last_dates = [it["_date"] for it in findings if it.get("_date")]
        last_finding = max(last_dates).isoformat() if last_dates else None
        items_today = sum(1 for it in findings if it.get("_date") == today)
        state_monitors[monitor_dir.name] = {
            "last_finding_at": last_finding,
            "items_today": items_today,
            "items_this_week": len(week_items),
            "cold_cells": per_monitor[monitor_dir.name]["cold_cells"][:5],
        }

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    weekly_path = METRICS_DIR / WEEKLY_FILE_TEMPLATE.format(year=year, week=week)
    weekly_path.write_text(
        render_weekly_md(datetime.now(timezone.utc), year, week, per_monitor),
        encoding="utf-8",
    )

    WEBSITE_STATE.parent.mkdir(parents=True, exist_ok=True)
    WEBSITE_STATE.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "iso_week": f"{year}-W{week:02d}",
                "monitors": state_monitors,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"Wrote {weekly_path.relative_to(ROOT)}")
    print(f"Wrote {WEBSITE_STATE.relative_to(ROOT)}")

    if args.coverage:
        coverage_path = METRICS_DIR / COVERAGE_FILE_TEMPLATE.format(year=today.year, month=today.month)
        coverage_path.write_text(render_coverage_md(today, per_monitor), encoding="utf-8")
        print(f"Wrote {coverage_path.relative_to(ROOT)}")

    return 0


def render_coverage_md(today: date, per_monitor: dict[str, dict[str, Any]]) -> str:
    lines = [
        f"# Coverage Health — {today.year}-{today.month:02d}",
        "",
        f"_Generated {today.isoformat()}_",
        "",
        "What this report answers: which (persona × jurisdiction) intersections of the",
        f"coverage matrix produced findings recently, and which have gone dark for {COLD_CELL_DAYS}+ days.",
        "",
        "**Cold ≠ broken.** Some regulators go silent for stretches and that is itself",
        "information. Use this to ask: did we miss something, or did nothing happen?",
        "",
    ]
    for monitor, m in per_monitor.items():
        lines += [
            f"## {monitor}",
            "",
            f"- Cold cells: **{len(m['cold_cells'])}**",
        ]
        if m["cold_cells"]:
            for cc in m["cold_cells"]:
                lines.append(f"  - {cc}")
        else:
            lines.append("  - none")
        lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
