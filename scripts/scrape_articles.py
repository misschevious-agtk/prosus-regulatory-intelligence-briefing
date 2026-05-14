#!/usr/bin/env python3
"""
scrape_articles.py — Legal Intelligence Briefing HTML scraper v0.1

Sibling of fetch_articles.py for sources that don't publish RSS. Reads
scrape_sources.yml (per-site selector config), fetches list pages over HTTP,
extracts items with BeautifulSoup, runs the same keyword match and
confidentiality pre-filter as the RSS path, and writes to the same
findings/candidates/ tree. Output is interchangeable with RSS-sourced
candidates — rank_candidates.py needs no changes.

Selector config schema (v0.1, minimal):
  monitor-NN/domain:
    - name: human label
      list_url: https://example.com/news
      list_selector: "div.news-item"           # CSS selector for items on list page
      item:
        title_selector: "h2 a"                  # text becomes title
        url_selector: "h2 a"                    # @href becomes link
        date_selector: "time"                   # text becomes published (optional)
        date_attr: "datetime"                   # if date is in an attribute (optional)
        summary_selector: "p.summary"           # text becomes summary (optional)
      base_url: https://example.com             # for resolving relative URLs (optional)
      rate_limit_seconds: 2                     # pause between requests (default 2)
      max_items: 30                             # cap per list page (default 30)
      user_agent: null                          # override global UA (optional)

Run manually:        python scripts/scrape_articles.py
Run via Actions:     .github/workflows/scrape.yml (after fetch_articles.py)

Change-log:
  2026-05-14 — v0.1: initial implementation. Seeded with HTML-only sources
               identified in the audit (DG COMP merger cases, DMA enforcement
               hub, EUIPO observatory, UPC, EDPB binding decisions, AISI).
               No JavaScript rendering — flag JS-required sites and skip.
"""

from __future__ import annotations

import sys
import time
import urllib.robotparser
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

from lib_candidates import (
    build_keyword_regexes,
    extract_keywords,
    match_article,
    write_candidate,
)

ROOT = Path(__file__).resolve().parent.parent
MONITORS_DIR = ROOT / "monitors"
SCRAPE_SOURCES_FILE = ROOT / "scripts" / "scrape_sources.yml"
OUTPUT_BASE = ROOT / "findings" / "candidates"

DEFAULT_USER_AGENT = (
    "Prosus Legal Intelligence Briefing "
    "(klimentina.maleevska@prosus.com; +https://github.com/prosus/legal-intelligence-briefing)"
)
DEFAULT_RATE_LIMIT_SECONDS = 2
DEFAULT_MAX_ITEMS = 30
REQUEST_TIMEOUT_SECONDS = 20

# Cache of robots.txt parsers per netloc so we don't refetch per request.
_robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def robots_allowed(url: str, user_agent: str) -> bool:
    """Return True if robots.txt at the URL's host permits the user-agent.

    Failures (unreachable robots.txt, parse errors) are logged and treated as
    permissive — most regulator sites don't serve robots.txt, and a missing
    file is conventionally read as 'no restrictions'.
    """
    parsed = urlparse(url)
    netloc = f"{parsed.scheme}://{parsed.netloc}"
    rp = _robots_cache.get(netloc)
    if rp is None:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(urljoin(netloc, "/robots.txt"))
        try:
            rp.read()
        except Exception as exc:  # noqa: BLE001
            print(f"    ! robots.txt unreachable at {netloc}: {exc}",
                  file=sys.stderr)
            # Permissive on unreachable robots — set rules to None
            rp = None  # type: ignore[assignment]
        _robots_cache[netloc] = rp  # may be None
    if rp is None:
        return True
    try:
        return rp.can_fetch(user_agent, url)
    except Exception:  # noqa: BLE001
        return True


def fetch_html(url: str, user_agent: str) -> str | None:
    """GET a URL and return decoded HTML, or None on error."""
    try:
        resp = requests.get(
            url,
            headers={"User-Agent": user_agent, "Accept": "text/html"},
            timeout=REQUEST_TIMEOUT_SECONDS,
            allow_redirects=True,
        )
    except requests.RequestException as exc:
        print(f"    ! request error: {exc}", file=sys.stderr)
        return None
    if resp.status_code >= 400:
        print(f"    ! HTTP {resp.status_code} for {url}", file=sys.stderr)
        return None
    # requests handles encoding via headers; fall back to apparent encoding
    resp.encoding = resp.encoding or resp.apparent_encoding
    return resp.text


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

def extract_text_or_attr(element, attr: str | None) -> str:
    """Return element.get_text() or element[attr] if attr is set."""
    if element is None:
        return ""
    if attr:
        return (element.get(attr) or "").strip()
    return element.get_text(separator=" ", strip=True)


def extract_items(html: str, source_cfg: dict) -> list[dict]:
    """Apply selector config to HTML and return a list of {title, link,
    summary, published} dicts. URLs are resolved against base_url if set."""
    soup = BeautifulSoup(html, "lxml")
    list_selector = source_cfg.get("list_selector", "")
    if not list_selector:
        return []

    item_cfg = source_cfg.get("item", {}) or {}
    title_sel = item_cfg.get("title_selector", "")
    url_sel = item_cfg.get("url_selector", "")
    url_attr = item_cfg.get("url_attr", "href")
    date_sel = item_cfg.get("date_selector", "")
    date_attr = item_cfg.get("date_attr", "")
    summary_sel = item_cfg.get("summary_selector", "")

    base_url = source_cfg.get("base_url", "") or source_cfg.get("list_url", "")

    nodes = soup.select(list_selector)
    max_items = int(source_cfg.get("max_items", DEFAULT_MAX_ITEMS))
    items: list[dict] = []

    for node in nodes[:max_items]:
        title_el = node.select_one(title_sel) if title_sel else node
        url_el = node.select_one(url_sel) if url_sel else None
        date_el = node.select_one(date_sel) if date_sel else None
        summary_el = node.select_one(summary_sel) if summary_sel else None

        title = (title_el.get_text(separator=" ", strip=True)
                 if title_el is not None else "")
        link = ""
        if url_el is not None:
            link = (url_el.get(url_attr) or "").strip()
        elif title_el is not None and title_el.name == "a":
            link = (title_el.get(url_attr) or "").strip()
        if link and base_url:
            link = urljoin(base_url, link)

        published = extract_text_or_attr(date_el, date_attr)
        summary = (summary_el.get_text(separator=" ", strip=True)
                   if summary_el is not None else "")

        if not title:
            continue
        items.append({
            "title": title,
            "link": link,
            "summary": summary,
            "published": published,
        })
    return items


# ---------------------------------------------------------------------------
# Per-domain driver
# ---------------------------------------------------------------------------

def scrape_domain(
    monitor: str,
    domain: str,
    sites: list[dict],
    keywords: set[str],
    today: str,
) -> int:
    """Scrape all configured sites for a domain, write candidates, return count."""
    if not keywords or not sites:
        return 0

    keyword_regexes = build_keyword_regexes(keywords)
    out_dir = OUTPUT_BASE / today / monitor / domain
    out_dir.mkdir(parents=True, exist_ok=True)

    total = 0
    for site_cfg in sites:
        name = site_cfg.get("name", "")
        list_url = site_cfg.get("list_url", "")
        if not name or not list_url:
            print("    ! skipping site with missing name or list_url",
                  file=sys.stderr)
            continue

        if site_cfg.get("disabled"):
            print(f"    skipping (disabled): {name}", file=sys.stderr)
            continue

        user_agent = site_cfg.get("user_agent") or DEFAULT_USER_AGENT
        rate_limit = float(site_cfg.get("rate_limit_seconds",
                                        DEFAULT_RATE_LIMIT_SECONDS))

        print(f"    scraping: {name}", file=sys.stderr)

        if not robots_allowed(list_url, user_agent):
            print(f"    ! robots.txt disallows {list_url} — skipping",
                  file=sys.stderr)
            continue

        html = fetch_html(list_url, user_agent)
        time.sleep(rate_limit)
        if html is None:
            continue

        try:
            items = extract_items(html, site_cfg)
        except Exception as exc:  # noqa: BLE001
            print(f"    ! extraction error for {name}: {exc}",
                  file=sys.stderr)
            continue

        site_matches = 0
        for item in items:
            text = " ".join([item["title"], item["summary"]])
            matched = match_article(text, keyword_regexes)
            if not matched:
                continue
            written = write_candidate(
                out_dir=out_dir,
                monitor=monitor,
                domain=domain,
                source_name=name,
                title=item["title"],
                link=item["link"],
                summary=item["summary"],
                published=item["published"],
                matched=matched,
                today=today,
                root=ROOT,
                source_method="scrape",
            )
            if written:
                site_matches += 1
                total += 1
        print(f"      items: {len(items)}  candidates: {site_matches}",
              file=sys.stderr)
    return total


def main() -> int:
    if not SCRAPE_SOURCES_FILE.exists():
        print(f"ERROR: {SCRAPE_SOURCES_FILE} not found — nothing to scrape",
              file=sys.stderr)
        return 0  # not an error; project may have no HTML sources yet

    sources = yaml.safe_load(SCRAPE_SOURCES_FILE.read_text(encoding="utf-8")) or {}
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
            sites_key = f"{monitor}/{domain}"
            sites = sources.get(sites_key, [])
            print(f"  {domain}: {len(keywords)} keywords, {len(sites)} sites",
                  file=sys.stderr)
            if not sites:
                continue
            n = scrape_domain(monitor, domain, sites, keywords, today)
            grand_total += n

    print(f"\nTotal scraped candidates written: {grand_total}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
