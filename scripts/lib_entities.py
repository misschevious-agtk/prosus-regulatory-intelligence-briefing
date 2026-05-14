#!/usr/bin/env python3
"""
lib_entities.py — entity extraction for the ranker.

Two passes:
1. CASE NUMBERS — regex against EU / UK / US citation formats. Anything that
   looks like a docket / case / decision number gets tagged.
2. NAMED ENTITIES — gazetteer + portfolio matching. The gazetteer (regulators,
   courts, Big Tech, AI labs) lives in scripts/gazetteer.yml. Prosus portfolio
   companies are parsed at runtime from portfolios.md so the gazetteer stays
   Prosus-agnostic.

Used by rank_candidates.py. Standalone — no fastembed / torch deps.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
GAZETTEER_FILE = ROOT / "scripts" / "gazetteer.yml"
PORTFOLIOS_FILE = ROOT / "portfolios.md"

# ----------------------------------------------------------------------
# Case-number patterns
# ----------------------------------------------------------------------
# Each pattern: a compiled regex + a label describing what it catches. The
# label gets stored as the citation's "scheme" so downstream tooling can
# group by court / regulator.

CASE_PATTERNS: list[tuple[str, re.Pattern]] = [
    # EU General Court — "T-604/22"
    ("EU General Court", re.compile(r"\bT[-‑]\d{1,4}/\d{2}\b")),
    # Court of Justice — "C-376/22"
    ("EU Court of Justice", re.compile(r"\bC[-‑]\d{1,4}/\d{2}\b")),
    # DG COMP antitrust — "Case AT.40437"
    ("EU antitrust (AT)", re.compile(r"\b(?:Case\s+)?AT\.\d{4,6}\b")),
    # EU merger control (current) — "M.10999"
    ("EU merger (M.)", re.compile(r"\bM\.\d{3,5}\b")),
    # EU state aid — "SA.65541"
    ("EU state aid (SA.)", re.compile(r"\bSA\.\d{4,6}\b")),
    # UK Court of Appeal — "[2024] EWCA Civ 1234"
    ("UK Court of Appeal", re.compile(r"\[\d{4}\]\s+EWCA\s+(?:Civ|Crim)\s+\d+")),
    # UK High Court — "[2024] EWHC 1234 (Ch)"
    ("UK High Court", re.compile(r"\[\d{4}\]\s+EWHC\s+\d+\s*\(\w+\)")),
    # UK Supreme Court — "[2024] UKSC 12"
    ("UK Supreme Court", re.compile(r"\[\d{4}\]\s+UKSC\s+\d+")),
    # CMA case reference — "ME/6961/24"
    ("UK CMA merger", re.compile(r"\bME/\d{4}/\d{2}\b")),
    # US Federal — "No. 23-1234" (loosely matched; pair with a regulator hit
    # to reduce false positives)
    ("US case no.", re.compile(r"\bNo\.\s+\d{2}[-‑]\d{4,5}\b")),
    # Generic FCC / FTC docket — "MD Docket No. 12-345"
    ("US docket", re.compile(r"\bDocket\s+No\.\s+\d{2}[-‑]\d{1,5}\b",
                              re.IGNORECASE)),
]


@dataclass(frozen=True)
class CaseCitation:
    scheme: str
    citation: str

    def to_dict(self) -> dict:
        return {"scheme": self.scheme, "citation": self.citation}


@dataclass(frozen=True)
class EntityMatch:
    name: str
    type: str
    jurisdiction: str
    matched_alias: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.type,
            "jurisdiction": self.jurisdiction,
            "matched_alias": self.matched_alias,
        }


def extract_case_numbers(text: str) -> list[CaseCitation]:
    """Return de-duplicated case citations found in text."""
    if not text:
        return []
    seen: set[tuple[str, str]] = set()
    hits: list[CaseCitation] = []
    for scheme, pattern in CASE_PATTERNS:
        for match in pattern.findall(text):
            # findall can return strings or tuples depending on groups; we
            # use no capture groups, so it's always strings.
            citation = match if isinstance(match, str) else " ".join(match)
            # Normalise non-breaking hyphen back to ASCII for stable storage.
            citation_norm = citation.replace("‑", "-")
            key = (scheme, citation_norm)
            if key in seen:
                continue
            seen.add(key)
            hits.append(CaseCitation(scheme=scheme, citation=citation_norm))
    return hits


# ----------------------------------------------------------------------
# Gazetteer + portfolio loading
# ----------------------------------------------------------------------

# Words ≤ this length are matched with word boundaries on both sides so
# acronyms like "EC" / "FTC" don't trigger inside other words.
_ACRONYM_MAX_LEN = 8


def _alias_pattern(alias: str) -> re.Pattern:
    escaped = re.escape(alias.strip())
    if len(alias) <= _ACRONYM_MAX_LEN and " " not in alias:
        return re.compile(rf"\b{escaped}\b")
    # For multi-word aliases or longer tokens, allow case-insensitive
    # substring with no boundary requirement (more forgiving).
    return re.compile(escaped, re.IGNORECASE)


def load_gazetteer(path: Path | None = None) -> list[dict]:
    p = path or GAZETTEER_FILE
    if not p.exists():
        return []
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or []
    if not isinstance(data, list):
        return []
    return data


def _portfolio_strip_parenthetical(raw: str) -> str:
    """'PayU (India + retained)' -> 'PayU'.

    Also splits 'Despegar / Decolar' into the first form; the second is
    added as an alias separately.
    """
    raw = re.sub(r"\s*\([^)]*\)\s*", " ", raw).strip()
    return raw.strip(" .,")


def parse_portfolio_companies(path: Path | None = None) -> list[dict]:
    """Parse portfolios.md and return gazetteer-shaped entries for each
    portfolio company. Looks for the markdown table headed by
    '| Portfolio company        | Region            | …'"""
    p = path or PORTFOLIOS_FILE
    if not p.exists():
        return []
    text = p.read_text(encoding="utf-8")

    entries: list[dict] = []
    seen_names: set[str] = set()
    in_table = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            in_table = False
            continue
        if line.lower().startswith("| portfolio company"):
            in_table = True
            continue
        if not in_table:
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        # Table separator row
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue

        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        raw_name = cells[0]
        # Bold-strip
        raw_name = re.sub(r"\*+", "", raw_name).strip()
        if not raw_name:
            continue

        # Names like "Despegar / Decolar" or "EMPG / dubizzle" expose two
        # surface forms — split and treat both as aliases.
        forms = [_portfolio_strip_parenthetical(f) for f in re.split(r"\s+/\s+", raw_name)]
        forms = [f for f in forms if f]
        if not forms:
            continue
        canonical = forms[0]
        if canonical in seen_names:
            continue
        seen_names.add(canonical)

        jurisdiction = cells[1] if len(cells) > 1 else ""
        # Build aliases — canonical + secondary forms + a few sensible variants
        aliases = list(dict.fromkeys(forms + _portfolio_aliases(canonical)))

        entries.append({
            "name": canonical,
            "type": "portfolio",
            "jurisdiction": jurisdiction,
            "aliases": aliases,
        })

    return entries


def _portfolio_aliases(name: str) -> list[str]:
    """Add a few common variants — drop suffixes like 'Group', drop case
    variants. Avoids matching very short generic words."""
    variants: list[str] = []
    base = name
    for suffix in [" Group", " Holdings", " AG", " SE", " plc", " PLC",
                   " Inc", " Inc.", " Ltd", " B.V.", " BV"]:
        if base.endswith(suffix):
            stripped = base[: -len(suffix)].strip()
            if len(stripped) >= 4:
                variants.append(stripped)
    return variants


def build_entity_index(extra_entries: Iterable[dict] | None = None) -> list[dict]:
    """Gazetteer + portfolio entries, with pre-compiled alias patterns
    attached on each entry under '_patterns'. Cached one-shot per process."""
    base = load_gazetteer()
    if extra_entries:
        base = base + list(extra_entries)
    out: list[dict] = []
    for entry in base:
        aliases = entry.get("aliases") or []
        if not aliases:
            aliases = [entry.get("name", "")]
        patterns = [(a, _alias_pattern(a)) for a in aliases if a]
        out.append({**entry, "_patterns": patterns})
    return out


def extract_entities(text: str, index: list[dict]) -> list[EntityMatch]:
    """Return de-duplicated entity matches against the supplied index."""
    if not text or not index:
        return []
    seen: set[str] = set()
    out: list[EntityMatch] = []
    for entry in index:
        for alias, pattern in entry.get("_patterns", []):
            if pattern.search(text):
                key = entry["name"]
                if key in seen:
                    break
                seen.add(key)
                out.append(EntityMatch(
                    name=entry["name"],
                    type=entry.get("type", ""),
                    jurisdiction=entry.get("jurisdiction", ""),
                    matched_alias=alias,
                ))
                break
    return out


# Convenience for callers that don't want to assemble the index themselves.
_DEFAULT_INDEX: list[dict] | None = None


def default_index() -> list[dict]:
    global _DEFAULT_INDEX
    if _DEFAULT_INDEX is None:
        portfolio = parse_portfolio_companies()
        _DEFAULT_INDEX = build_entity_index(portfolio)
    return _DEFAULT_INDEX
