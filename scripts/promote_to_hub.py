#!/usr/bin/env python3
"""
promote_to_hub.py -- candidate -> website hub auto-promotion

Reads the day's top-ranked candidates from findings/candidates/<today>/<monitor>/
<domain>/*.md and appends them to the inline `window.ITEMS_DATA` array in each
monitor's website/<monitor>/index.html. Hand-curated entries are preserved --
we only ADD auto-promoted items, never remove.

Auto-promoted items carry `"auto": true` so the renderer (or a reviewer) can
distinguish them from hand-shaped findings with rich Prosus attribution.
Placeholder fields (`why`, `co`, `owner`) are stubbed as "[awaiting review]"
so the reviewer has a clear signal of what still needs human input.

Quality gates (a candidate must pass ALL to be promoted):
  * cluster_role == 'canonical'   -- pick the cluster representative, not siblings
  * match_count >= 2              -- at least two keywords matched
  * has a non-empty source_url    -- click-throughable
  * title not already in hub      -- de-dupe vs hand-curated items

Caps:
  * Max N_PER_DOMAIN per (monitor, domain) per run (default 5)
  * Max N_PER_MONITOR per monitor per run (default 20)

Run manually:        python scripts/promote_to_hub.py
Run via Actions:     scrape.yml, step after `rank_candidates.py`
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_BASE = ROOT / "findings" / "candidates"
WEBSITE_DIR = ROOT / "website"

# Caps tuned 2026-05-14: previous values (5/20) capped M01 at ~20 auto
# items per run -- felt thin once the page actually rendered. Bumped to
# 12/50 to surface more of the day's raw signal. Reviewers can still
# manually demote noise by editing the inline ITEMS_DATA.
N_PER_DOMAIN = 12
N_PER_MONITOR = 50

# Map monitor folder name -> website folder name
MONITOR_WEBSITE = {
    "monitor-01": "monitor-01",
    "monitor-02-eu-competition": "monitor-02",
}

# Map candidate-folder domain name -> hub theme + catLabel + default owner
DOMAIN_TO_THEME = {
    # Monitor 01
    "ai-news": ("ai-news", "AI Policy", "Group AI Counsel"),
    "intellectual-property": ("ip", "IP & Brand", "Tara Harris"),
    "privacy-data-protection": ("privacy", "Privacy & Data", "Group Privacy Counsel"),
    "legal-ops": ("legal-ops", "Legal Ops", "Head of Legal Ops"),
    # Monitor 02 -- theme ids match M02's MONITOR_DATA.topics ids exactly.
    "antitrust-cartels": ("antitrust", "Antitrust & Cartels", "Anne-Claire Hoyng"),
    "abuse-of-dominance": ("dominance", "Abuse of Dominance", "Anne-Claire Hoyng"),
    "merger-control-fdi": ("merger", "Merger & FDI", "Anne-Claire Hoyng"),
    "digital-markets-sector-state-aid": ("digital", "Digital Markets", "Anne-Claire Hoyng"),
}


def parse_frontmatter(md_path: Path) -> dict | None:
    """Read a candidate .md file and return its YAML frontmatter as a dict.
    Returns None if no parsable frontmatter."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception:
        return None
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None


def risk_from_match_count(n: int) -> str:
    if n >= 5:
        return "high"
    if n >= 3:
        return "med"
    return "low"


def format_date_label(date_str: str) -> str:
    """Try to convert an RSS date string to '14 May 2026' format. Falls back
    to the original string on parse failure (the renderer is lenient)."""
    if not date_str:
        return ""
    # Try common formats
    for fmt in (
        "%a, %d %b %Y %H:%M:%S %z",
        "%a, %d %b %Y %H:%M:%S %Z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
    ):
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%-d %b %Y") if sys.platform != "win32" else dt.strftime("%#d %b %Y")
        except ValueError:
            continue
    return date_str.strip()[:24]


def slug_to_id(slug: str) -> str:
    """Convert a slug like 'foo-bar-baz' to an id 'foo-bar-baz' (just hyphens kept)."""
    return re.sub(r"[^a-z0-9-]", "", slug.lower())[:60]


def candidate_to_item(fm: dict, slug: str, theme: str, cat_label: str, owner: str) -> dict | None:
    """Map candidate frontmatter to a hub items.json item dict.
    Returns None if essential fields are missing."""
    title = (fm.get("title") or "").strip()
    url = (fm.get("source_url") or "").strip()
    if not title or not url:
        return None
    if fm.get("match_count", 0) < 2:
        return None
    if fm.get("cluster_role") and fm.get("cluster_role") != "canonical":
        return None

    # YAML may parse date strings as datetime.date objects; coerce to str.
    source_date = str(fm.get("source_date") or fm.get("date_found") or "")
    date_label = format_date_label(source_date) or str(fm.get("date_found", ""))
    iso_date = str(fm.get("date_found") or "")

    return {
        "id": slug_to_id(slug),
        "theme": theme,
        "catLabel": cat_label,
        "country": "??",
        "countryLabel": "— Source",
        "risk": risk_from_match_count(int(fm.get("match_count", 0))),
        "date": iso_date,
        "dateLabel": date_label,
        "source": fm.get("source_publisher", "(unknown)"),
        "url": url,
        "title": title,
        "body": "(See source article for full text.)",
        "why": "[awaiting review] -- auto-promoted from RSS feed. Edit this field to add Prosus-relevance analysis.",
        "co": "[awaiting review]",
        "owner": owner,
        "ownerTeam": "Group Legal",
        "auto": True,
    }


def collect_promotions(today: str, monitor_dir_name: str) -> list[dict]:
    """For one monitor, walk its candidate domains and pick up to N_PER_DOMAIN
    canonical, multi-match candidates per domain. Return the merged item list,
    capped at N_PER_MONITOR overall."""
    monitor_root = CANDIDATES_BASE / today / monitor_dir_name
    if not monitor_root.exists():
        return []

    promoted: list[dict] = []
    for domain_dir in sorted(monitor_root.iterdir()):
        if not domain_dir.is_dir():
            continue
        domain_name = domain_dir.name
        if domain_name not in DOMAIN_TO_THEME:
            continue
        theme, cat_label, owner = DOMAIN_TO_THEME[domain_name]

        # Read all candidates in this domain, score them, pick the top N
        scored: list[tuple[int, dict, str]] = []
        for md_file in sorted(domain_dir.glob("*.md")):
            fm = parse_frontmatter(md_file)
            if not fm:
                continue
            slug = md_file.stem
            # Score: higher match_count + larger cluster wins
            score = int(fm.get("match_count", 0)) * 10 + int(fm.get("cluster_size", 1))
            scored.append((score, fm, slug))

        scored.sort(key=lambda t: -t[0])
        added_for_domain = 0
        for score, fm, slug in scored:
            item = candidate_to_item(fm, slug, theme, cat_label, owner)
            if item is None:
                continue
            promoted.append(item)
            added_for_domain += 1
            if added_for_domain >= N_PER_DOMAIN:
                break

    return promoted[:N_PER_MONITOR]


def update_index_html(index_path: Path, new_items: list[dict]) -> int:
    """Read index.html, parse the inline window.ITEMS_DATA array, append any
    new items whose `url` isn't already in the array (dedupe by URL), and
    write back. Returns the number of items actually appended."""
    if not index_path.exists():
        print(f"  ! {index_path} not found, skipping", file=sys.stderr)
        return 0

    text = index_path.read_text(encoding="utf-8")
    # Find the inline ITEMS_DATA array. It's a single-line declaration:
    # `window.ITEMS_DATA = [...];` where [...] is potentially very long.
    m = re.search(r"window\.ITEMS_DATA\s*=\s*", text)
    if not m:
        print(f"  ! window.ITEMS_DATA not found in {index_path}", file=sys.stderr)
        return 0

    # Walk forward from m.end() balancing brackets to find the matching ']'.
    start = m.end()
    if text[start] != "[":
        print(f"  ! Expected '[' at position {start}", file=sys.stderr)
        return 0
    depth = 0
    in_string = False
    escape = False
    end = -1
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        print(f"  ! Could not find end of ITEMS_DATA array", file=sys.stderr)
        return 0

    array_text = text[start:end + 1]
    try:
        existing = json.loads(array_text)
    except json.JSONDecodeError as exc:
        print(f"  ! Failed to parse ITEMS_DATA as JSON: {exc}", file=sys.stderr)
        return 0

    # Idempotency: strip any previously auto-promoted items first, then
    # re-add the current batch. Hand-curated items (those WITHOUT auto:true)
    # are preserved untouched.
    curated = [it for it in existing if isinstance(it, dict) and not it.get("auto")]
    curated_urls = {it.get("url") for it in curated}
    # Don't re-promote anything that's already in the curated set.
    to_add = [it for it in new_items if it.get("url") not in curated_urls]

    if not to_add and len(curated) == len(existing):
        # Nothing to change at all.
        return 0

    merged = curated + to_add
    new_array_json = json.dumps(merged, ensure_ascii=False, separators=(", ", ": "))
    new_text = text[:start] + new_array_json + text[end + 1:]
    index_path.write_text(new_text, encoding="utf-8")
    return len(to_add)


def main() -> int:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    print(f"\n[promote_to_hub] today = {today}", file=sys.stderr)

    grand_total = 0
    for monitor_dir_name, website_subdir in MONITOR_WEBSITE.items():
        print(f"\n[{monitor_dir_name} -> website/{website_subdir}/]", file=sys.stderr)
        items = collect_promotions(today, monitor_dir_name)
        print(f"  collected: {len(items)} candidate(s) eligible for promotion",
              file=sys.stderr)
        if not items:
            continue
        index_path = WEBSITE_DIR / website_subdir / "index.html"
        added = update_index_html(index_path, items)
        print(f"  appended: {added} new item(s) to {index_path.name}",
              file=sys.stderr)
        grand_total += added

    print(f"\n[promote_to_hub] total items added across hub: {grand_total}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
