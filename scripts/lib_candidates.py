#!/usr/bin/env python3
"""
lib_candidates.py — shared candidate-writing helpers

Used by both fetch_articles.py (RSS) and scrape_articles.py (HTML). Owns the
candidate output schema, keyword extraction, regex compilation, and the
confidentiality pre-filter integration. Centralising these here prevents
schema drift between the two fetchers.

Schema change-log:
  2026-05-14 — Initial extraction from fetch_articles.py. Added
               `source_method` field to candidate frontmatter so the ranker
               can tell RSS-sourced from scrape-sourced candidates.
"""

from __future__ import annotations

import re
from pathlib import Path

# Confidentiality pre-filter — keeps privileged or leniency-track content out
# of findings/candidates/ entirely. The library is local to this scripts/ dir.
try:
    from lib_confidentiality import is_confidential, load_watchlist, quarantine  # type: ignore
except ImportError:  # pragma: no cover
    is_confidential = None  # type: ignore
    load_watchlist = lambda _p: {}  # type: ignore
    quarantine = None  # type: ignore

# ---------------------------------------------------------------------------
# Constants — shared parsing thresholds. Identical to fetch_articles.py v0.1
# so behaviour is unchanged for the RSS path.
# ---------------------------------------------------------------------------

LANG_OR_BROAD = re.compile(
    r"\s*\[(broad|FR|DE|IT|NL|ES|PT|PT-BR|PL|RO|TR|HU|GR|MT|FI|SE|DK|NO|LV)\]",
    re.IGNORECASE,
)
LEADING_PUNCT = re.compile(r"^[*\-\s]+")
TRAILING_PUNCT = re.compile(r"[:\s]+$")

MIN_KEYWORD_LEN = 3
MAX_KEYWORDS_PER_CANDIDATE = 15

# Keywords matching this stop-list never trigger on their own (too generic).
STOP_WORDS = {
    "ai", "eu", "us", "uk", "fr", "de", "it", "es", "nl", "pt", "br",
    "the", "and", "of", "in", "to", "for", "on", "with",
}


# ---------------------------------------------------------------------------
# Keyword extraction
# ---------------------------------------------------------------------------

def extract_keywords(md_path: Path) -> set[str]:
    """Extract Tier 1 and Tier 2 keywords from a domain's keywords.md file."""
    if not md_path.exists():
        return set()

    text = md_path.read_text(encoding="utf-8")
    keywords: set[str] = set()
    in_tier = False

    tier_pattern = re.compile(r"^## Tier ([12])\b")
    stop_pattern = re.compile(r"^## (Tier [34]|Change|Cross-monitor)")

    for line in text.splitlines():
        if tier_pattern.match(line):
            in_tier = True
            continue
        if stop_pattern.match(line):
            in_tier = False
            continue
        if not in_tier:
            continue
        if line.startswith("#") or line.startswith(">"):
            continue
        if " · " not in line:
            continue

        for raw in line.split(" · "):
            cleaned = LANG_OR_BROAD.sub("", raw)
            cleaned = LEADING_PUNCT.sub("", cleaned)
            cleaned = TRAILING_PUNCT.sub("", cleaned)
            cleaned = cleaned.strip()
            cleaned = re.sub(r"^\*+|\*+$", "", cleaned).strip()
            if not cleaned:
                continue
            for part in re.split(r"\s+/\s+", cleaned):
                part = part.strip().strip(".")
                if len(part) < MIN_KEYWORD_LEN:
                    continue
                if part.lower() in STOP_WORDS:
                    continue
                keywords.add(part)

    return keywords


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------

def slugify(text: str, maxlen: int = 70) -> str:
    """Filesystem-safe slug. Collapse non-alphanumerics to hyphens."""
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen] or "item"


def make_match_regex(keyword: str) -> re.Pattern:
    """Compile a case-insensitive regex that requires word boundaries for short
    acronyms but allows substring match for multi-word phrases."""
    if len(keyword) <= 8 and " " not in keyword:
        return re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)
    return re.compile(re.escape(keyword), re.IGNORECASE)


def match_article(text: str, keyword_regexes: dict[str, re.Pattern]) -> list[str]:
    """Return the list of keywords that match the article text."""
    matched = []
    for keyword, pattern in keyword_regexes.items():
        if pattern.search(text):
            matched.append(keyword)
    return matched


def build_keyword_regexes(keywords: set[str]) -> dict[str, re.Pattern]:
    """Compile a keyword set into a dict of name -> regex."""
    return {kw: make_match_regex(kw) for kw in keywords}


# ---------------------------------------------------------------------------
# Candidate writer — the schema authority. Both fetchers go through this.
# ---------------------------------------------------------------------------

def write_candidate(
    *,
    out_dir: Path,
    monitor: str,
    domain: str,
    source_name: str,
    title: str,
    link: str,
    summary: str,
    published: str,
    matched: list[str],
    today: str,
    root: Path,
    source_method: str = "rss",
) -> bool:
    """Write a candidate finding markdown file. Returns True if newly written.

    Keyword-only arguments so callers can be explicit. `source_method` is
    'rss' for fetch_articles.py and 'scrape' for scrape_articles.py — the
    ranker uses it for source-confidence weighting in Rule 21 dedup.
    """
    title = (title or "").strip()
    if not title:
        return False

    summary = (summary or "").strip()
    link = (link or "").strip()
    published = (published or "").strip()

    slug = slugify(title)
    out_file = out_dir / f"{slug}.md"
    if out_file.exists():
        return False

    # Strip HTML tags from summary for readability
    summary_text = re.sub(r"<[^>]+>", " ", summary)
    summary_text = re.sub(r"\s+", " ", summary_text).strip()[:1200]

    # Confidentiality pre-filter — runs before the candidate is written.
    # See strategy.md > Confidentiality pre-filter.
    if is_confidential is not None:
        watchlist = load_watchlist(root / "scripts")
        hit, category = is_confidential(
            f"{title}\n{summary_text}",
            url=link,
            sender=source_name,
            watchlist=watchlist,
        )
        if hit and quarantine is not None:
            quarantine(
                candidate_text=f"{title}\n{summary_text}",
                reason=category or "unspecified",
                source_url=link,
                source_publisher=source_name,
                sender=source_name,
                root=root,
                watchlist=watchlist,
            )
            return False

    matched_display = matched[:MAX_KEYWORDS_PER_CANDIDATE]
    matched_yaml = ", ".join(f'"{k}"' for k in matched_display)
    safe_title = title.replace('"', "'").replace("\n", " ").strip()
    safe_source = source_name.replace('"', "'")

    body = f"""---
date_found: {today}
monitor: {monitor}
domain: {domain}
source_url: "{link}"
source_publisher: "{safe_source}"
source_date: "{published}"
source_method: {source_method}
title: "{safe_title}"
matched_keywords: [{matched_yaml}]
match_count: {len(matched)}
status: candidate
---

# {title}

**Source:** [{source_name}]({link})
**Published:** {published or "unknown"}
**Matched keywords ({len(matched)}):** {", ".join(matched_display)}

## Summary excerpt

{summary_text or "_No summary available from source feed._"}

---

*Auto-generated candidate from `scripts/{('fetch_articles.py' if source_method == 'rss' else 'scrape_articles.py')}`. Review against the
persona's `interrogation-checklist.md` before promoting to a formal finding
under `output-schema.md`.*
"""
    out_file.write_text(body, encoding="utf-8")
    return True
