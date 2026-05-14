#!/usr/bin/env python3
"""
test_dedup.py — golden-file harness for the cross-monitor dedup engine.

Reads scripts/tests/dedup_golden.yml and asserts that the routing engine
returns the expected (primary_monitor, primary_domain, secondary) tuple
for each case.

The routing engine itself is `route_finding` in this file — a deliberate,
small, deterministic Python translation of the routing rule set in
strategy.md ("Cross-monitor deduplication"), M01 Rule 22, and M02 Rule 21.
If the rules in the markdown change, change them here too and the test
catches drift on the next run.

Exit codes:
  0 — all cases pass
  1 — one or more failures
  2 — usage / load error

Run:    python scripts/test_dedup.py
        python scripts/test_dedup.py --verbose
        python scripts/test_dedup.py --update      # rewrite golden with current output (use carefully)
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "scripts" / "tests" / "dedup_golden.yml"

# --- the routing rules -------------------------------------------------------

# Source-type families used by the router.
M02_TYPES = {
    "commission-decision", "nca-decision", "court-judgment", "ag-opinion",
    "statement-of-objections", "settlement", "guidance", "market-investigation",
    "sector-inquiry",
}
M01_TYPES = {
    "primary-law", "court-ruling", "regulator-guidance", "enforcement-action",
    "vendor-announcement",
}

# Trigger-type to monitor affinity. The first match wins.
TRIGGER_AFFINITY = [
    # Pure competition triggers.
    ("designation",                "monitor-02-eu-competition"),
    ("final_decision",             "monitor-02-eu-competition"),
    ("interim_decision",           "monitor-02-eu-competition"),
    ("statement_of_objections",    "monitor-02-eu-competition"),
    ("dawn_raid_pattern",          "monitor-02-eu-competition"),
    ("merger_review",              "monitor-02-eu-competition"),
    ("settlement",                 "monitor-02-eu-competition"),
    ("ag_opinion",                 "monitor-02-eu-competition"),
    ("threshold_change",           "monitor-02-eu-competition"),
    ("sector_inquiry_opened",      "monitor-02-eu-competition"),
    ("sector_inquiry_concluded",   "monitor-02-eu-competition"),
    ("remedy_precedent",           "monitor-02-eu-competition"),
    ("leniency_change",            "monitor-02-eu-competition"),
    ("market_investigation",       "monitor-02-eu-competition"),
    # M01 specifics.
    ("law_enacted",                "monitor-01"),
    ("law_effective_date",         "monitor-01"),
    ("regulator_guidance",         "monitor-01"),
    ("enforcement_action",         "monitor-01"),
    ("model_release",              "monitor-01"),
    ("capability_demo",            "monitor-01"),
    ("vendor_change",              "monitor-01"),
    ("breach_incident",            "monitor-01"),
    ("license_event",              "monitor-01"),
    ("tooling_change",             "monitor-01"),
    ("workflow_benchmark",         "monitor-01"),
    # Shared / ambiguous — fall through to entity/system tests.
]

# M01 domain affinity by trigger / entity patterns. Order matters — more
# specific doctrine families come before more general ones.
M01_DOMAIN_HINTS = [
    ("ip",          ["copyright", "indemnity", "training-data", "training pipeline", "training data", "deepfake", "trademark", "patent"]),
    ("privacy",     ["LGPD", "GDPR", "ANPD", "CNIL", "ICO", "recommender", "ADM", "Article 22", "transfer mechanism", "DPF", "Schrems", "personal data"]),
    ("legal-ops",   ["panel firm", "AI-use disclosure", "court standing order", "legal-tech"]),
    ("ai-news",     ["AI Act", "GPAI", "Annex III", "LCM", "Toqan", "Qwen", "frontier model", "AI foundation models", "foundation model"]),
]

# M02 domain affinity. Order matters — antitrust / abuse / merger before the
# digital-markets bucket so that doctrine markers beat institutional shell.
M02_DOMAIN_HINTS = [
    ("antitrust-cartels",                   ["cartel", "horizontal restraint", "MFN", "parity", "price-fixing", "TCC", "supplier contract", "iFood TCC"]),
    ("abuse-of-dominance",                  ["abuse of dominance", "Article 102", "self-preferencing", "recommender-as-abuse", "ecosystem theory", "Tencent"]),
    ("merger-control-fdi",                  ["merger", "Article 22", "FDI", "FSR", "CFIUS", "phase II", "below-threshold call-in"]),
    ("digital-markets-sector-state-aid",    ["DMA", "DSA", "VLOP", "VLOSE", "SMS", "state aid", "sector regulation", "Foundation Models", "designation"]),
]

# When these tokens appear in named_entities or affected_systems_or_practices,
# the substantive doctrine override pulls the finding to M01 even when the
# trigger or source type would otherwise route to M02.
M01_DOCTRINE_OVERRIDE_TOKENS = {
    "ai foundation models", "foundation model", "lcm", "toqan", "qwen",
    "gpai", "ai training", "training pipeline", "training-data",
}


@dataclass
class Routing:
    primary_monitor: str
    primary_domain: str
    secondary: list[dict[str, str]]


def _haystack(item: dict[str, Any]) -> str:
    """Concatenate strings to substring-match against."""
    parts: list[str] = []
    for key in ("trigger_type", "primary_axis", "source_type", "jurisdiction"):
        v = item.get(key)
        if v:
            parts.append(str(v))
    for key in ("named_entities", "affected_systems_or_practices"):
        v = item.get(key) or []
        if isinstance(v, list):
            parts.extend(str(x) for x in v)
    return " ".join(parts)


# Triggers that are doctrinally "soft" — the authority might be competition
# but the substantive question can still be M01. For these, AI doctrine markers
# can override and pull the finding to M01.
DOCTRINE_OVERRIDABLE_TRIGGERS = {
    "market_investigation", "sector_inquiry_opened", "sector_inquiry_concluded",
    "court_ruling", "narrative_shift", "market_move",
}


def _has_doctrine_override(item: dict[str, Any]) -> bool:
    """True if any AI-doctrine marker is present in enumerated fields."""
    hay = _haystack(item).lower()
    return any(tok in hay for tok in M01_DOCTRINE_OVERRIDE_TOKENS)


def _primary_monitor(item: dict[str, Any]) -> str:
    """Decide primary monitor from trigger type, falling back to source type.

    The M01 doctrine override pulls AI-substantive items to M01 when the
    trigger is doctrinally soft (market investigation, sector inquiry).
    For hard M02 triggers (final_decision, designation, guidance_published,
    statement_of_objections, settlement, etc.), the override is suppressed
    and the M01 read-through becomes a secondary cross-reference instead.
    """
    trigger = str(item.get("trigger_type", ""))
    if trigger in DOCTRINE_OVERRIDABLE_TRIGGERS and _has_doctrine_override(item):
        return "monitor-01"
    for trig, monitor in TRIGGER_AFFINITY:
        if trigger == trig:
            return monitor
    source_type = str(item.get("source_type", ""))
    if source_type in M02_TYPES:
        return "monitor-02-eu-competition"
    if source_type in M01_TYPES:
        return "monitor-01"
    # Final fallback: M01 (broader scope).
    return "monitor-01"


def _domain(item: dict[str, Any], monitor: str) -> str:
    hay = _haystack(item).lower()
    hints = M01_DOMAIN_HINTS if monitor == "monitor-01" else M02_DOMAIN_HINTS
    for domain, keywords in hints:
        for kw in keywords:
            if kw.lower() in hay:
                return domain
    # Fall-back defaults.
    return "ai-news" if monitor == "monitor-01" else "digital-markets-sector-state-aid"


def _secondary(item: dict[str, Any], primary_monitor: str, primary_domain: str) -> list[dict[str, str]]:
    """Detect read-through to the other monitor's domains."""
    hay = _haystack(item).lower()
    secondaries: list[dict[str, str]] = []
    if primary_monitor == "monitor-01":
        # Look for M02 read-through markers.
        for domain, keywords in M02_DOMAIN_HINTS:
            for kw in keywords:
                if kw.lower() in hay:
                    secondaries.append({"monitor": "monitor-02-eu-competition", "domain": domain})
                    break
    else:
        # Primary M02 — look for M01 read-through.
        for domain, keywords in M01_DOMAIN_HINTS:
            for kw in keywords:
                if kw.lower() in hay:
                    if (domain, primary_domain) == (domain, domain):
                        continue
                    secondaries.append({"monitor": "monitor-01", "domain": domain})
                    break
    # Deduplicate and drop any equal to the primary cell.
    seen: set[tuple[str, str]] = set()
    out: list[dict[str, str]] = []
    for s in secondaries:
        key = (s["monitor"], s["domain"])
        if s["monitor"] == primary_monitor and s["domain"] == primary_domain:
            continue
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def route_finding(item: dict[str, Any]) -> Routing:
    monitor = _primary_monitor(item)
    domain = _domain(item, monitor)
    secondary = _secondary(item, monitor, domain)
    return Routing(monitor, domain, secondary)


# --- harness ----------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description="Golden test harness for the dedup engine.")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not GOLDEN.exists():
        print(f"ERROR: golden file missing at {GOLDEN}", file=sys.stderr)
        return 2

    golden = yaml.safe_load(GOLDEN.read_text(encoding="utf-8")) or {}
    cases = golden.get("cases") or []
    if not cases:
        print("No cases in golden file.")
        return 0

    failed = 0
    for case in cases:
        cid = case.get("id", "<no-id>")
        item = case.get("item") or {}
        expected = case.get("expected") or {}
        got = route_finding(item)

        ok = (
            got.primary_monitor == expected.get("primary_monitor")
            and got.primary_domain == expected.get("primary_domain")
            and _normalise_secondary(got.secondary) == _normalise_secondary(expected.get("secondary") or [])
        )
        if ok:
            if args.verbose:
                print(f"PASS  {cid}")
        else:
            failed += 1
            print(f"FAIL  {cid}")
            print(f"      expected: {expected.get('primary_monitor')} / {expected.get('primary_domain')} + {expected.get('secondary')}")
            print(f"      got     : {got.primary_monitor} / {got.primary_domain} + {got.secondary}")

    total = len(cases)
    print(f"\n{total} cases, {failed} failed.")
    return 0 if failed == 0 else 1


def _normalise_secondary(items: list[dict[str, str]] | None) -> list[tuple[str, str]]:
    return sorted((s["monitor"], s["domain"]) for s in (items or []))


if __name__ == "__main__":
    sys.exit(main())
