#!/usr/bin/env python3
"""
fetch_articles.py — Legal Intelligence Briefing RSS scraper v0.2

Reads per-domain keywords from each monitor's keywords.md files, fetches the
RSS feeds configured in sources.yml, matches each article against Tier 1 and
Tier 2 keywords, and writes candidate findings to findings/candidates/.

Each candidate is a markdown file with YAML frontmatter capturing source,
matched keywords, and routing (monitor/domain). These are NOT formal findings
yet — they're the scraper output the persona reviews against the
interrogation-checklist before promoting to a finding under output-schema.md.

Run manually:        python scripts/fetch_articles.py
Run via Actions:     .github/workflows/scrape.yml (cron daily 07:00 UTC)

Change-log:
  2026-05-14 — v0.2: shared candidate-writing helpers extracted to
               lib_candidates.py. Behaviour unchanged for the RSS path.
               candidate frontmatter now includes `source_method: rss`.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import yaml

from lib_candidates import (
    build_keyword_regexes,
    extract_keywords,
    match_article,
    write_candidate,
)

ROOT = Path(__file__).resolve().parent.parent
MONITORS_DIR = ROOT / "monitors"
SOURCES_FILE = ROOT / "scripts" / "sources.yml"
OUTPUT_BASE = ROOT / "findings" / "candidates"

MAX_ENTRIES_PER_FEED = 30


def fetch_domain(
    monitor: str,
    domain: str,
    feeds: list[dict],
    keywords: set[str],
    today: str,
) -> int:
    """Fetch all feeds for a domain, write candidate findings, return count."""
    if not keywords or not feeds:
        return 0

    keyword_regexes = build_keyword_regexes(keywords)
    out_dir = OUTPUT_BASE / today / monitor / domain
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for feed_cfg in feeds:
        url = feed_cfg.get("url", "")
        name = feed_cfg.get("name", url)
        if not url:
            continue
        print(f"    fetching: {name}", file=sys.stderr)
        try:
            parsed = feedparser.parse(url)
        except Exception as exc:
            print(f"    ! error: {exc}", file=sys.stderr)
            continue
        if parsed.bozo and not parsed.entries:
            print(f"    ! feed parse error: {parsed.get('bozo_exception')}",
                  file=sys.stderr)
            continue

        feed_matches = 0
        for entry in parsed.entries[:MAX_ENTRIES_PER_FEED]:
            title = entry.get("title", "") or ""
            summary = entry.get("summary", "") or entry.get("description", "") or ""
            text = " ".join([title, summary])
            matched = match_article(text, keyword_regexes)
            if not matched:
                continue
            written = write_candidate(
                out_dir=out_dir,
                monitor=monitor,
                domain=domain,
                source_name=name,
                title=title,
                link=entry.get("link", "") or "",
                summary=summary,
                published=entry.get("published", "") or entry.get("updated", "") or "",
                matched=matched,
                today=today,
                root=ROOT,
                source_method="rss",
            )
            if written:
                feed_matches += 1
                total += 1
        print(f"      candidates: {feed_matches}", file=sys.stderr)
        time.sleep(0.5)  # be polite to source servers
    return total


def main() -> int:
    if not SOURCES_FILE.exists():
        print(f"ERROR: {SOURCES_FILE} not found", file=sys.stderr)
        return 1

    sources = yaml.safe_load(SOURCES_FILE.read_text(encoding="utf-8")) or {}
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    grand_total = 0

    for monitor_dir in sorted(MONITORS_DIR.iterdir()):
        if not monitor_dir.is_dir():
            continue
        monitor = monitor_dir.name
        print(f"\n[{monitor}]", file=sys.stderr)
        for domain_dir in sorted(monitor_dir.iterdir()):
            if not domain_dir.is_dir() or domain_dir.name == "findings":
                continue
            domain = domain_dir.name
            kw_file = domain_dir / "keywords.md"
            if not kw_file.exists():
                continue

            keywords = extract_keywords(kw_file)
            feed_key = f"{monitor}/{domain}"
            feeds = sources.get(feed_key, [])
            print(f"  {domain}: {len(keywords)} keywords, {len(feeds)} feeds",
                  file=sys.stderr)
            if not feeds:
                continue
            n = fetch_domain(monitor, domain, feeds, keywords, today)
            grand_total += n

    print(f"\nTotal candidates written: {grand_total}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
