#!/usr/bin/env python3
"""
archive_run.py -- per-scrape-run snapshot for the orchestrator brain.

Writes a structured markdown + JSON pair under archive/runs/YYYY-MM-DD/
each time the workflow runs. The orchestrator (and any other agent) can
backfill-sweep these snapshots to reason about prior runs without having
to walk the full candidates tree.

Output structure:

    archive/runs/
        2026-05-14/
            run-2026-05-14T07-00-00Z.md   <- human + agent readable
            run-2026-05-14T07-00-00Z.json <- machine-readable detail
        2026-05-15/
            ...

The .md has YAML frontmatter (date, totals, per-domain counts, top
entities, top clusters, broken-feed flags) so an agent can parse it with
the same lib_candidates helpers used elsewhere. The body is short prose
that summarises the run for a human skim.

Run manually:    python scripts/archive_run.py
Run via Actions: scrape.yml, step after `rank_candidates.py`.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_BASE = ROOT / "findings" / "candidates"
CLUSTERS_BASE = ROOT / "findings" / "clusters"
ARCHIVE_BASE = ROOT / "archive" / "runs"

# How many examples to include in each summary bucket.
TOP_ENTITIES_N = 10
TOP_CLUSTERS_N = 5
TOP_TITLES_PER_MONITOR = 5


def parse_frontmatter(md_path: Path) -> dict:
    """Extract YAML frontmatter from a candidate markdown file. Returns
    empty dict if no frontmatter or parse error."""
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


def collect_today(today: str) -> dict:
    """Walk findings/candidates/<today>/ and assemble a per-domain map of
    candidate counts, entities, clusters, source publishers, and example
    titles. Also reads the day's cluster file if present."""

    day_root = CANDIDATES_BASE / today
    summary = {
        "date": today,
        "total_candidates": 0,
        "per_domain": {},          # "monitor-01/ai-news": int
        "per_source": {},          # "OpenAI blog": int
        "entities": Counter(),     # entity name -> count
        "clusters": [],            # list of {id, size, canonical_title}
        "top_titles": {},          # "monitor-01": [titles...]
        "broken_feed_sources": [], # populated below from candidates with `source_method` rss but match_count zero across run -- left as a placeholder for now
    }

    if not day_root.exists():
        return summary

    candidates_by_monitor: dict[str, list[dict]] = {}

    for monitor_dir in sorted(day_root.iterdir()):
        if not monitor_dir.is_dir():
            continue
        monitor = monitor_dir.name
        candidates_by_monitor.setdefault(monitor, [])

        for domain_dir in sorted(monitor_dir.iterdir()):
            if not domain_dir.is_dir():
                continue
            domain = domain_dir.name
            key = f"{monitor}/{domain}"
            n = 0
            for md_path in domain_dir.glob("*.md"):
                fm = parse_frontmatter(md_path)
                if not fm:
                    continue
                n += 1
                summary["total_candidates"] += 1
                src = fm.get("source_publisher", "(unknown)")
                summary["per_source"][src] = summary["per_source"].get(src, 0) + 1
                for ent in (fm.get("entities") or []):
                    if isinstance(ent, dict) and ent.get("name"):
                        summary["entities"][ent["name"]] += 1
                candidates_by_monitor[monitor].append(fm)
            summary["per_domain"][key] = n

    # Top titles per monitor (by match_count, then cluster_size)
    for monitor, fms in candidates_by_monitor.items():
        fms.sort(
            key=lambda fm: (
                -int(fm.get("match_count", 0)),
                -int(fm.get("cluster_size", 1)),
            )
        )
        summary["top_titles"][monitor] = [
            {
                "title": (fm.get("title") or "").strip()[:140],
                "source": fm.get("source_publisher", ""),
                "match_count": int(fm.get("match_count", 0)),
                "cluster_role": fm.get("cluster_role", ""),
            }
            for fm in fms[:TOP_TITLES_PER_MONITOR]
        ]

    # Read the day's cluster file if present and add top clusters by size
    cluster_path = CLUSTERS_BASE / f"{today}.json"
    if cluster_path.exists():
        try:
            cl = json.loads(cluster_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cl = None
        if isinstance(cl, dict) and "clusters" in cl:
            clusters_list = cl["clusters"]
        elif isinstance(cl, list):
            clusters_list = cl
        else:
            clusters_list = []
        clusters_list = sorted(
            clusters_list,
            key=lambda c: -int(c.get("size", 0) if isinstance(c, dict) else 0),
        )[:TOP_CLUSTERS_N]
        summary["clusters"] = [
            {
                "id": c.get("id", ""),
                "size": int(c.get("size", 0)),
                "canonical_title": (
                    c.get("canonical_title")
                    or c.get("canonical_slug", "")
                ),
            }
            for c in clusters_list
            if isinstance(c, dict)
        ]

    summary["top_entities"] = [
        {"name": name, "count": count}
        for name, count in summary["entities"].most_common(TOP_ENTITIES_N)
    ]
    # Drop the raw Counter -- not directly JSON-serialisable
    del summary["entities"]
    return summary


def render_markdown(summary: dict, run_ts: str) -> str:
    """Produce the agent-readable markdown for the run snapshot."""
    fm_lines = [
        "---",
        f"run_ts: {run_ts}",
        f"date: {summary['date']}",
        f"total_candidates: {summary['total_candidates']}",
        "per_domain:",
    ]
    for k, v in sorted(summary["per_domain"].items()):
        fm_lines.append(f"  {k}: {v}")
    fm_lines.append("per_source:")
    for src, n in sorted(summary["per_source"].items(), key=lambda x: -x[1]):
        safe_src = src.replace('"', "'")
        fm_lines.append(f'  "{safe_src}": {n}')
    fm_lines.append("top_entities:")
    for e in summary.get("top_entities", []):
        safe_name = e["name"].replace('"', "'")
        fm_lines.append(f'  - name: "{safe_name}"')
        fm_lines.append(f"    count: {e['count']}")
    fm_lines.append("top_clusters:")
    for c in summary.get("clusters", []):
        safe_title = (c.get("canonical_title") or "").replace('"', "'")
        fm_lines.append(f'  - id: "{c.get("id", "")}"')
        fm_lines.append(f"    size: {c.get('size', 0)}")
        fm_lines.append(f'    canonical: "{safe_title}"')
    fm_lines.append("---")
    fm_lines.append("")

    body = [
        f"# Scrape run snapshot -- {summary['date']}",
        "",
        f"Captured at `{run_ts}`. Total candidates written: **{summary['total_candidates']}**.",
        "",
        "## Per-domain counts",
        "",
    ]
    for k, v in sorted(summary["per_domain"].items()):
        body.append(f"- `{k}` -- {v}")
    body.append("")

    if summary.get("top_entities"):
        body.append("## Top entities mentioned")
        body.append("")
        for e in summary["top_entities"]:
            body.append(f"- **{e['name']}** ({e['count']} mention(s))")
        body.append("")

    if summary.get("clusters"):
        body.append("## Largest clusters")
        body.append("")
        for c in summary["clusters"]:
            body.append(f"- `{c['id']}` -- size {c['size']} -- canonical: {c.get('canonical_title', '(unknown)')}")
        body.append("")

    body.append("## Top titles per monitor")
    body.append("")
    for monitor, items in sorted(summary.get("top_titles", {}).items()):
        body.append(f"### {monitor}")
        body.append("")
        if not items:
            body.append("_(no candidates this run)_")
            body.append("")
            continue
        for it in items:
            body.append(
                f"- **{it['title']}** -- _{it['source']}_ "
                f"(match_count={it['match_count']}, role={it['cluster_role'] or 'n/a'})"
            )
        body.append("")

    body.append("---")
    body.append("")
    body.append(
        "_Auto-generated by `scripts/archive_run.py`. The frontmatter above is the_\n"
        "_agent-parseable contract; the body is a human skim of the same data._"
    )
    return "\n".join(fm_lines) + "\n".join(body) + "\n"


def main() -> int:
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    run_ts = now.strftime("%Y-%m-%dT%H-%M-%SZ")

    summary = collect_today(today)
    if summary["total_candidates"] == 0:
        print(
            f"[archive_run] No candidates found under {CANDIDATES_BASE / today}; "
            "skipping snapshot.",
            file=sys.stderr,
        )
        return 0

    out_dir = ARCHIVE_BASE / today
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / f"run-{run_ts}.md"
    json_path = out_dir / f"run-{run_ts}.json"

    md_path.write_text(render_markdown(summary, run_ts), encoding="utf-8")
    json_path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(
        f"[archive_run] {summary['total_candidates']} candidates "
        f"snapshotted -> {md_path.relative_to(ROOT)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
