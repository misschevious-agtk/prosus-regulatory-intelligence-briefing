#!/usr/bin/env python3
"""
weekly_retrospective.py -- weekly summary of the scrape system's behaviour.

Reads the last seven days of archive snapshots + curated tier files and
emits one markdown brief at metrics/retrospective-YYYY-WNN.md.

Complements `compute_metrics.py`:
  * compute_metrics.py reads `findings/` (formal findings, post-promotion)
    -- mostly empty until reviewers manually promote candidates.
  * weekly_retrospective.py reads `archive/` (raw scrape signal) -- this
    is where the real volume lives right now.

Run manually:        python scripts/weekly_retrospective.py
Run via Actions:     .github/workflows/weekly-retrospective.yml (cron
                     Sunday 18:00 UTC).
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
RUNS_BASE = ROOT / "archive" / "runs"
CURATED_BASE = ROOT / "archive" / "curated"
METRICS_DIR = ROOT / "metrics"

WINDOW_DAYS = 7  # the retrospective window


def parse_frontmatter(md_path: Path) -> dict:
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return {}
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def iter_run_jsons(since: datetime) -> list[dict]:
    """Return every run snapshot JSON written on or after `since`."""
    out: list[dict] = []
    if not RUNS_BASE.exists():
        return out
    for date_dir in sorted(RUNS_BASE.iterdir()):
        if not date_dir.is_dir():
            continue
        try:
            d = datetime.strptime(date_dir.name, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        except ValueError:
            continue
        if d < since:
            continue
        for jf in sorted(date_dir.glob("run-*.json")):
            try:
                out.append(json.loads(jf.read_text(encoding="utf-8")))
            except json.JSONDecodeError:
                continue
    return out


def iter_curated_in_window(since: datetime) -> list[tuple[str, dict]]:
    """Return (tier, frontmatter) tuples for curated items first-seen in window."""
    out: list[tuple[str, dict]] = []
    if not CURATED_BASE.exists():
        return out
    for tier_dir in CURATED_BASE.iterdir():
        if not tier_dir.is_dir():
            continue
        tier = tier_dir.name
        for md in tier_dir.glob("*.md"):
            fm = parse_frontmatter(md)
            if not fm:
                continue
            first_seen = fm.get("first_seen", "")
            # YAML may parse the ISO timestamp as a datetime object or
            # leave it as a string -- handle both.
            fs: datetime | None = None
            if isinstance(first_seen, datetime):
                fs = first_seen if first_seen.tzinfo else first_seen.replace(tzinfo=timezone.utc)
            elif isinstance(first_seen, str) and first_seen:
                try:
                    fs = datetime.strptime(first_seen, "%Y-%m-%dT%H:%M:%SZ").replace(
                        tzinfo=timezone.utc
                    )
                except ValueError:
                    continue
            if fs is None:
                continue
            if fs >= since:
                out.append((tier, fm))
    return out


def render_retrospective(
    week_label: str, window_start: str, window_end: str,
    runs: list[dict], curated: list[tuple[str, dict]]
) -> str:
    # Aggregate from per-run snapshots
    total_runs = len(runs)
    total_candidates = sum(int(r.get("total_candidates", 0)) for r in runs)
    per_source: Counter = Counter()
    per_domain: Counter = Counter()
    entities: Counter = Counter()
    for r in runs:
        for src, n in (r.get("per_source") or {}).items():
            per_source[src] += int(n)
        for key, n in (r.get("per_domain") or {}).items():
            per_domain[key] += int(n)
        for e in (r.get("top_entities") or []):
            if isinstance(e, dict) and e.get("name"):
                entities[e["name"]] += int(e.get("count", 0))

    # Aggregate from curated tier files (items NEW this week)
    by_tier = Counter()
    monitors_seen = Counter()
    new_per_source: Counter = Counter()
    a_tier_items: list[dict] = []
    for tier, fm in curated:
        by_tier[tier] += 1
        monitors_seen[fm.get("monitor", "?")] += 1
        new_per_source[fm.get("source_publisher", "?")] += 1
        if tier == "A":
            a_tier_items.append(fm)

    # Identify productive vs silent feeds across the week
    productive = [(s, n) for s, n in per_source.most_common(10)]

    lines = [
        "---",
        f"window: {week_label}",
        f"window_start: {window_start}",
        f"window_end: {window_end}",
        f"runs_observed: {total_runs}",
        f"total_candidates_window: {total_candidates}",
        f"curated_new_window: {sum(by_tier.values())}",
        f"tier_a_new: {by_tier['A']}",
        f"tier_b_new: {by_tier['B']}",
        f"tier_c_new: {by_tier['C']}",
        "---",
        "",
        f"# Weekly retrospective -- {week_label}",
        "",
        f"Window: **{window_start}** -> **{window_end}**. "
        f"Runs observed: **{total_runs}**. "
        f"Total raw candidates produced: **{total_candidates}**. "
        f"New curated items added this week: "
        f"**{sum(by_tier.values())}** "
        f"(A: {by_tier['A']}, B: {by_tier['B']}, C: {by_tier['C']}).",
        "",
        "## What got into the curated library (Tier A) this week",
        "",
    ]
    if not a_tier_items:
        lines.append("_No Tier A items this week. Either signal was thin or the "
                     "match_count >= 5 threshold needs revisiting._")
    else:
        for fm in a_tier_items[:25]:
            t = (fm.get("title") or "").strip()
            url = fm.get("source_url") or ""
            src = fm.get("source_publisher") or "?"
            mon = fm.get("monitor") or "?"
            lines.append(f"- **{t}** -- _{src}_ -- `{mon}` -- [source]({url})")
    lines.append("")

    lines.append("## Most productive feeds (total candidates this week)")
    lines.append("")
    if not productive:
        lines.append("_No data._")
    else:
        for src, n in productive:
            lines.append(f"- **{src}** -- {n} candidate(s)")
    lines.append("")

    lines.append("## Per-monitor / domain volume")
    lines.append("")
    if not per_domain:
        lines.append("_No data._")
    else:
        for key, n in sorted(per_domain.items()):
            lines.append(f"- `{key}` -- {n}")
    lines.append("")

    lines.append("## Top entities surfaced")
    lines.append("")
    if not entities:
        lines.append("_No entities tagged (rank_candidates.py may not have run)._")
    else:
        for name, n in entities.most_common(15):
            lines.append(f"- **{name}** -- {n} mention(s)")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "_Auto-generated by `scripts/weekly_retrospective.py`. "
        "Reads `archive/runs/<date>/run-*.json` and `archive/curated/<tier>/*.md` "
        "for the past 7 days. The frontmatter above is the agent-parseable "
        "contract for the orchestrator's brain._"
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=WINDOW_DAYS)
    iso_year, iso_week, _ = now.isocalendar()
    week_label = f"{iso_year}-W{iso_week:02d}"
    window_start = since.strftime("%Y-%m-%d")
    window_end = now.strftime("%Y-%m-%d")

    runs = iter_run_jsons(since)
    curated = iter_curated_in_window(since)

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = METRICS_DIR / f"retrospective-{week_label}.md"
    out_path.write_text(
        render_retrospective(week_label, window_start, window_end, runs, curated),
        encoding="utf-8",
    )
    print(
        f"[weekly_retrospective] {week_label}: "
        f"{len(runs)} run snapshot(s), {len(curated)} curated item(s) "
        f"-> {out_path.relative_to(ROOT)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
