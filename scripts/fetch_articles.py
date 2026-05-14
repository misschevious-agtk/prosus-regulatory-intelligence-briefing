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
  2026-05-14 — v0.3: feed fetch now goes through `requests` with a
               browser-flavoured User-Agent and a permissive Accept header
               before handing bytes to feedparser. UTF-8/16 BOMs are
               stripped pre-parse. Together these fix the
               "<unknown>:2:0: syntax error" class of bogus parse failures
               (ICO, CEPS, Reuters Legal) and the "text/html is not an
               XML media type" class (TechPolicy.Press, possibly others
               where the publisher serves HTML to non-browser UAs).
"""

from __future__ import annotations

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import feedparser
import requests
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
REQUEST_TIMEOUT_SECONDS = 20

# Browser-flavoured UA. Many publishers (e.g. via Cloudflare bot-mitigation
# or careless Accept-based content negotiation) serve HTML to clients whose
# UA starts with "Python-" or "feedparser/", which is what feedparser sends
# by default. Leading with a Mozilla token avoids that filter; the project
# URL and contact email keep us identifiable to anyone reading server logs.
FEED_USER_AGENT = (
    "Mozilla/5.0 (compatible; ProsusLegalBriefing/0.3; "
    "+https://github.com/misschevious-agtk/prosus-regulatory-intelligence-briefing; "
    "klimentina.maleevska@prosus.com)"
)
FEED_ACCEPT_HEADER = (
    "application/rss+xml, application/atom+xml, application/xml;q=0.9, "
    "text/xml;q=0.8, */*;q=0.5"
)


def fetch_feed_bytes(url: str) -> bytes | None:
    """GET a feed URL with a browser UA, strip a leading BOM, return bytes.

    Returns None on network failure or HTTP >= 400. The caller passes the
    bytes to feedparser.parse(), which handles XML parsing identically to
    its URL-fetching mode but without the default UA quirks.
    """
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": FEED_USER_AGENT, "Accept": FEED_ACCEPT_HEADER},
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )
    except requests.RequestException as exc:
        print(f"    ! request error: {exc}", file=sys.stderr)
        return None
    if resp.status_code >= 400:
        print(f"    ! HTTP {resp.status_code}", file=sys.stderr)
        return None
    body = resp.content
    # Strip a leading UTF-8 BOM (most common cause of
    # `<unknown>:2:0: syntax error` from feedparser — the BOM byte is read
    # as content before the XML declaration on what should be line 1).
    if body.startswith(b"\xef\xbb\xbf"):
        body = body[3:]
    # UTF-16 BOMs (rare in RSS but cheap to handle defensively)
    elif body.startswith(b"\xff\xfe") or body.startswith(b"\xfe\xff"):
        body = body[2:]
    return body


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
        # Two-stage fetch: requests for transport (UA + BOM strip), then
        # feedparser for XML parsing. Keeps feedparser's resilient entry
        # extraction without inheriting its default UA.
        body = fetch_feed_bytes(url)
        if body is None:
            continue
        try:
            parsed = feedparser.parse(body)
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
