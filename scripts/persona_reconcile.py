#!/usr/bin/env python3
"""
persona_reconcile.py — quarterly persona/needs reconciliation.

For each persona, reads needs.md (the stated needs, one bullet item per
recognised need) and walks the feedback log for the most recent quarter.
Emits a three-column reconciliation file:

  monitors/<monitor>/<domain>/_reconciliation/YYYY-QN.md

The three columns:
  Stated need | Feedback signal | Status (contradiction | decay | implicit need | aligned)

This is a diff aide, not a decision. The persona's anchor + operator look at
the output and pick one of {update spec, recalibrate feedback, leave it} per
row. The reconciliation file is then checked in as the record.

Run:
    python scripts/persona_reconcile.py
    python scripts/persona_reconcile.py --monitor monitor-01 --domain privacy
    python scripts/persona_reconcile.py --quarter 2026-Q2

Convention for needs.md item extraction: lines beginning with "- " or "* "
under any header containing "Needs" (case-insensitive). The first bullet
sentence is taken as the canonical need text; sub-bullets are ignored.

Convention for feedback files (frontmatter):
    vote:    up | down
    annotation: "free text"
    finding_path: "findings/2026-05-12-privacy-cnil-recommender.md"
    themes: ["ANPD enforcement", "ADM doctrine creep"]      # optional
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
MONITORS_DIR = ROOT / "monitors"


def quarter_bounds(quarter: str) -> tuple[date, date]:
    m = re.fullmatch(r"(\d{4})-Q([1-4])", quarter)
    if not m:
        raise ValueError(f"--quarter must be YYYY-QN, got {quarter}")
    year, q = int(m[1]), int(m[2])
    start_month = (q - 1) * 3 + 1
    start = date(year, start_month, 1)
    end = date(year + (1 if q == 4 else 0), 1 if q == 4 else start_month + 3, 1) - \
          (date(year, start_month, 1) - date(year, start_month, 1))
    # Compute end as last day of quarter:
    from calendar import monthrange
    end_month = start_month + 2
    end = date(year, end_month, monthrange(year, end_month)[1])
    return start, end


def current_quarter(today: date) -> str:
    q = (today.month - 1) // 3 + 1
    return f"{today.year}-Q{q}"


def extract_needs(needs_md: Path) -> list[str]:
    """Return a list of stated need bullets from needs.md.

    needs.md uses nested headers (e.g. "## Categories" > "### Frontier model
    releases" > bullets), so the only useful state filter is "skip
    blockquotes, code blocks, and change-log tables". Any top-level
    bullet that survives those filters is treated as a stated need.
    """
    if not needs_md.exists():
        return []
    out: list[str] = []
    in_code = False
    in_changelog = False
    for raw in needs_md.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith(">"):
            continue
        if re.match(r"^#{1,6}\s.*change.?log", line, re.IGNORECASE):
            in_changelog = True
            continue
        if re.match(r"^#{1,6}\s", line):
            # Re-entry into normal sections after a changelog header
            in_changelog = False
            continue
        if in_changelog:
            continue
        m = re.match(r"^[-*]\s+(.+?)(?:\s+—\s+.+)?$", line.strip())
        if not m:
            continue
        # Strip leading bold like "**Some thing**" so themes match cleanly.
        need = re.sub(r"^\*\*(.+?)\*\*", r"\1", m.group(1)).strip()
        # Drop sub-bullets (start with a space before `-`) by checking indent.
        if raw.startswith(" ") or raw.startswith("\t"):
            continue
        if 5 < len(need) < 300:
            out.append(need)
    return out


def collect_feedback(monitor_dir: Path, domain: str, start: date, end: date) -> list[dict[str, Any]]:
    """Feedback for a single domain in the given quarter."""
    out: list[dict[str, Any]] = []
    fdir = monitor_dir / "findings" / "feedback"
    if not fdir.exists():
        return out
    for md in fdir.rglob("*.md"):
        text = md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            continue
        path_field = str(fm.get("finding_path", ""))
        if domain and domain not in path_field and domain not in md.name:
            continue
        try:
            d = date.fromisoformat(str(fm.get("date") or md.stem[:10]))
        except ValueError:
            continue
        if not (start <= d <= end):
            continue
        out.append(fm)
    return out


def reconcile(needs: list[str], feedback: list[dict[str, Any]]) -> list[dict[str, Any]]:
    theme_votes: dict[str, Counter] = defaultdict(Counter)
    for fb in feedback:
        vote = str(fb.get("vote", "")).lower()
        themes = fb.get("themes") or []
        for theme in themes:
            theme_votes[str(theme).strip()][vote] += 1

    rows: list[dict[str, Any]] = []
    seen_themes: set[str] = set()

    # First, walk stated needs and see how they fared.
    for need in needs:
        need_lc = need.lower()
        match_theme = None
        for theme in theme_votes:
            if theme.lower() in need_lc or need_lc.startswith(theme.lower()):
                match_theme = theme
                break
        if match_theme:
            counts = theme_votes[match_theme]
            seen_themes.add(match_theme)
            status = _status(counts["up"], counts["down"])
            rows.append({"need": need, "theme": match_theme, "up": counts["up"], "down": counts["down"], "status": status})
        else:
            rows.append({"need": need, "theme": "", "up": 0, "down": 0, "status": "decay"})

    # Then, surface themes with feedback but no stated need.
    for theme, counts in theme_votes.items():
        if theme in seen_themes:
            continue
        rows.append({"need": "(not in needs.md)", "theme": theme, "up": counts["up"], "down": counts["down"], "status": "implicit_need"})

    return rows


def _status(up: int, down: int) -> str:
    if up == 0 and down == 0:
        return "decay"
    if down >= 5 and down >= 2 * up:
        return "contradiction"
    if up > down:
        return "aligned"
    return "review"


def render(monitor: str, domain: str, quarter: str, rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# Persona reconciliation — {monitor} / {domain} — {quarter}",
        "",
        f"_Generated {datetime.now(timezone.utc).isoformat()}_",
        "",
        "| Stated need | Theme | 👍 | 👎 | Status |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['need'][:80]} | {r['theme'][:40]} | {r['up']} | {r['down']} | **{r['status']}** |"
        )
    lines += [
        "",
        "## Statuses",
        "",
        "- **aligned** — the feedback supports the stated need; no action.",
        "- **contradiction** — the need is stated but the feedback persistently says no; either update the spec or recalibrate the feedback.",
        "- **decay** — the need is stated but no feedback either way; either re-explain or drop.",
        "- **implicit_need** — feedback is positive on a theme not in needs.md; consider writing it into the spec.",
        "- **review** — borderline (e.g. equal up/down). Take a look.",
        "",
        "## Decisions (fill in)",
        "",
        "_For each row above, record one of: update spec / recalibrate feedback / leave._",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Quarterly persona reconciliation.")
    ap.add_argument("--monitor", help="Restrict to one monitor.")
    ap.add_argument("--domain", help="Restrict to one domain (within --monitor).")
    ap.add_argument("--quarter", help="YYYY-QN. Defaults to current quarter.")
    args = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    quarter = args.quarter or current_quarter(today)
    start, end = quarter_bounds(quarter)

    monitors = [MONITORS_DIR / args.monitor] if args.monitor else sorted(MONITORS_DIR.iterdir())
    for monitor_dir in [m for m in monitors if m.is_dir()]:
        for child in sorted(monitor_dir.iterdir()):
            if not child.is_dir():
                continue
            if args.domain and child.name != args.domain:
                continue
            needs_md = child / "needs.md"
            if not needs_md.exists():
                continue
            needs = extract_needs(needs_md)
            feedback = collect_feedback(monitor_dir, child.name, start, end)
            rows = reconcile(needs, feedback)
            out_dir = child / "_reconciliation"
            out_dir.mkdir(parents=True, exist_ok=True)
            out_path = out_dir / f"{quarter}.md"
            out_path.write_text(render(monitor_dir.name, child.name, quarter, rows), encoding="utf-8")
            print(f"Wrote {out_path.relative_to(ROOT)}  ({len(rows)} rows)")

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
