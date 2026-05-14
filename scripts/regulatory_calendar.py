#!/usr/bin/env python3
"""
regulatory_calendar.py — surface upcoming regulator windows for the briefing.

Reads scripts/regulatory_calendar.yml and emits a compact summary of windows
in the next N days. Used by the weekly briefing as a "Coming up" section and
by the hub freshness pulse as a "next window" pointer.

Run:
    python scripts/regulatory_calendar.py                # next 14 days
    python scripts/regulatory_calendar.py --days 30
    python scripts/regulatory_calendar.py --monitor monitor-02-eu-competition
    python scripts/regulatory_calendar.py --json         # JSON output for tooling
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
CALENDAR_FILE = ROOT / "scripts" / "regulatory_calendar.yml"

WEEKDAY_MAP = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}


def upcoming_windows(agency: dict[str, Any], today: date, horizon_days: int) -> list[date]:
    cadence = agency.get("cadence") or {}
    out: list[date] = []
    weekday = cadence.get("weekday")
    if weekday and weekday in WEEKDAY_MAP:
        target = WEEKDAY_MAP[weekday]
        for offset in range(horizon_days + 1):
            d = today + timedelta(days=offset)
            if d.weekday() == target:
                out.append(d)
    for ds in cadence.get("dates") or []:
        try:
            d = date.fromisoformat(ds)
        except (ValueError, TypeError):
            continue
        if today <= d <= today + timedelta(days=horizon_days):
            out.append(d)
    return sorted(out)


def main() -> int:
    ap = argparse.ArgumentParser(description="Upcoming regulator windows.")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--monitor", help="Filter to one monitor.")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if not CALENDAR_FILE.exists():
        print(f"ERROR: {CALENDAR_FILE} not found", file=sys.stderr)
        return 2
    data = yaml.safe_load(CALENDAR_FILE.read_text(encoding="utf-8")) or {}
    agencies = data.get("agencies") or []
    today = datetime.now(timezone.utc).date()

    rows: list[dict[str, Any]] = []
    for agency in agencies:
        if args.monitor and args.monitor not in (agency.get("affects_monitors") or []):
            continue
        dates = upcoming_windows(agency, today, args.days)
        if not dates:
            continue
        rows.append(
            {
                "id": agency.get("id"),
                "name": agency.get("name"),
                "jurisdiction": agency.get("jurisdiction"),
                "next_window": dates[0].isoformat(),
                "all_windows": [d.isoformat() for d in dates],
                "note": (agency.get("cadence") or {}).get("note", ""),
            }
        )

    rows.sort(key=lambda r: r["next_window"])

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(f"# Upcoming regulator windows (next {args.days} days)")
    print()
    if not rows:
        print("_no windows in range_")
        return 0
    for r in rows:
        print(f"- **{r['next_window']}** · {r['name']} ({r['jurisdiction']})")
        if r["note"]:
            print(f"  _{r['note']}_")
    return 0


if __name__ == "__main__":
    sys.exit(main())
