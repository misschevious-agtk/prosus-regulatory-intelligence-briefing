#!/usr/bin/env python3
"""
test_scrape.py — offline tests for scrape_articles.py

Exercises the extraction path against scripts/tests/scrape_fixture.html so
selector-config behaviour doesn't silently regress. Does not perform any
network I/O.

Run:    python scripts/test_scrape.py
Exit:   0 = pass, 1 = fail
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from scrape_articles import extract_items  # noqa: E402
from lib_candidates import (  # noqa: E402
    build_keyword_regexes,
    make_match_regex,
    match_article,
    slugify,
    write_candidate,
)

FIXTURE = SCRIPTS / "tests" / "scrape_fixture.html"


def _site_cfg() -> dict:
    return {
        "name": "Fixture authority",
        "list_url": "https://example.org/press",
        "list_selector": "li.press-item",
        "item": {
            "title_selector": "h3 a",
            "url_selector": "h3 a",
            "date_selector": "time",
            "date_attr": "datetime",
            "summary_selector": "p.summary",
        },
        "base_url": "https://example.org",
    }


def test_extract_items_returns_three() -> None:
    html = FIXTURE.read_text(encoding="utf-8")
    items = extract_items(html, _site_cfg())
    assert len(items) == 3, f"expected 3 items, got {len(items)}"


def test_extract_items_resolves_relative_url() -> None:
    items = extract_items(FIXTURE.read_text(encoding="utf-8"), _site_cfg())
    first = items[0]
    assert first["link"].startswith("https://example.org/press/2026/"), (
        f"relative URL not resolved: {first['link']}"
    )


def test_extract_items_preserves_absolute_url() -> None:
    items = extract_items(FIXTURE.read_text(encoding="utf-8"), _site_cfg())
    second = items[1]
    assert second["link"] == "https://example.org/press/2026/merger-clearance", (
        f"absolute URL altered: {second['link']}"
    )


def test_extract_items_reads_date_attr() -> None:
    items = extract_items(FIXTURE.read_text(encoding="utf-8"), _site_cfg())
    assert items[0]["published"] == "2026-05-12"


def test_extract_items_captures_summary() -> None:
    items = extract_items(FIXTURE.read_text(encoding="utf-8"), _site_cfg())
    assert "Digital Markets Act" in items[0]["summary"]


def test_keyword_match_against_extracted_items() -> None:
    items = extract_items(FIXTURE.read_text(encoding="utf-8"), _site_cfg())
    regexes = build_keyword_regexes({"DMA", "self-preferencing", "divestiture"})
    item_with_match = items[0]
    text = " ".join([item_with_match["title"], item_with_match["summary"]])
    matched = match_article(text, regexes)
    assert "DMA" in matched
    assert "self-preferencing" in matched

    # The procurement item should match nothing.
    procurement = items[2]
    procurement_text = " ".join([procurement["title"], procurement["summary"]])
    assert match_article(procurement_text, regexes) == []


def test_write_candidate_emits_source_method_scrape() -> None:
    """write_candidate should embed source_method: scrape in the frontmatter
    when called from the scrape path, so the ranker can tell them apart."""
    with tempfile.TemporaryDirectory() as tmp:
        out_dir = Path(tmp) / "out"
        out_dir.mkdir()
        wrote = write_candidate(
            out_dir=out_dir,
            monitor="monitor-02-eu-competition",
            domain="digital-markets-sector-state-aid",
            source_name="Fixture authority",
            title="DMA non-compliance decision against Gatekeeper X",
            link="https://example.org/press/2026/dma",
            summary="The Commission adopted a non-compliance decision under the DMA.",
            published="2026-05-12",
            matched=["DMA", "non-compliance"],
            today="2026-05-14",
            root=Path(tmp),
            source_method="scrape",
        )
        assert wrote is True
        files = list(out_dir.glob("*.md"))
        assert len(files) == 1
        body = files[0].read_text(encoding="utf-8")
        assert "source_method: scrape" in body
        assert "monitor: monitor-02-eu-competition" in body
        assert "DMA non-compliance" in body


def test_slugify_handles_punctuation() -> None:
    assert slugify("DMA: non-compliance decision (May 2026)") == "dma-non-compliance-decision-may-2026"


def test_make_match_regex_acronym_word_boundary() -> None:
    pat = make_match_regex("DMA")
    assert pat.search("subject to DMA obligations")
    assert not pat.search("the DMAA standard")  # word boundary respected


def main() -> int:
    tests = [
        test_extract_items_returns_three,
        test_extract_items_resolves_relative_url,
        test_extract_items_preserves_absolute_url,
        test_extract_items_reads_date_attr,
        test_extract_items_captures_summary,
        test_keyword_match_against_extracted_items,
        test_write_candidate_emits_source_method_scrape,
        test_slugify_handles_punctuation,
        test_make_match_regex_acronym_word_boundary,
    ]
    failed = 0
    for test in tests:
        try:
            test()
            print(f"  OK   {test.__name__}")
        except AssertionError as exc:
            print(f"  FAIL {test.__name__}: {exc}", file=sys.stderr)
            failed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ERR  {test.__name__}: {exc!r}", file=sys.stderr)
            failed += 1
    print(f"\n{len(tests) - failed}/{len(tests)} passed", file=sys.stderr)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
