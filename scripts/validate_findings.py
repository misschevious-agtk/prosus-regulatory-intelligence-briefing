#!/usr/bin/env python3
"""
validate_findings.py — schema validator for finding files.

Walks `findings/` (and `findings/candidates/` if `--candidates` is set) for
every monitor, parses the YAML frontmatter from each markdown file, and
validates it against `schemas/finding.schema.json`.

Exit codes:
  0  — all valid (or no files found)
  1  — one or more files failed schema validation
  2  — unexpected error (couldn't load schema, malformed YAML, etc.)

Run manually:
    python scripts/validate_findings.py
    python scripts/validate_findings.py --candidates
    python scripts/validate_findings.py --monitor monitor-01 --strict

Hook into CI in `.github/workflows/scrape.yml` after rank_candidates.py.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from jsonschema import Draft202012Validator as _Validator  # type: ignore
except ImportError:  # pragma: no cover — older jsonschema in the local sandbox
    try:
        from jsonschema import Draft7Validator as _Validator  # type: ignore

        print(
            "WARN: jsonschema <4.18 — falling back to Draft 7 validator. "
            "Install jsonschema>=4.18 in CI per scripts/requirements.txt.",
            file=sys.stderr,
        )
    except ImportError:
        print("ERROR: pip install jsonschema (>=4.18) --break-system-packages", file=sys.stderr)
        sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
SCHEMA_FILE = ROOT / "scripts" / "schemas" / "finding.schema.json"
MONITORS_DIR = ROOT / "monitors"


def parse_frontmatter(md_path: Path) -> dict[str, Any] | None:
    """Return the YAML frontmatter as a dict, or None if no frontmatter found."""
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        raise ValueError(f"YAML parse error in {md_path}: {exc}") from exc


def collect_finding_files(monitor_dir: Path, include_candidates: bool) -> list[Path]:
    """All finding-shaped MDs under a monitor, optionally including candidates."""
    files: list[Path] = []
    findings_dir = monitor_dir / "findings"
    if findings_dir.exists():
        for p in findings_dir.rglob("*.md"):
            # Skip docs / READMEs / indexes — only date-prefixed file names.
            if not p.stem[:4].isdigit():
                continue
            if "candidates" in p.parts and not include_candidates:
                continue
            files.append(p)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate finding frontmatter against the JSON Schema.")
    ap.add_argument("--monitor", help="Restrict to one monitor (e.g. monitor-01).")
    ap.add_argument("--candidates", action="store_true", help="Include findings/candidates/ files.")
    ap.add_argument("--strict", action="store_true", help="Exit 1 even on missing-optional warnings.")
    args = ap.parse_args()

    try:
        schema = json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: schema not found at {SCHEMA_FILE}", file=sys.stderr)
        return 2

    validator = _Validator(schema)

    if not MONITORS_DIR.exists():
        print(f"ERROR: monitors/ not found at {MONITORS_DIR}", file=sys.stderr)
        return 2

    monitor_dirs = [MONITORS_DIR / args.monitor] if args.monitor else sorted(MONITORS_DIR.iterdir())
    monitor_dirs = [d for d in monitor_dirs if d.is_dir()]

    total = 0
    failed = 0
    for monitor_dir in monitor_dirs:
        monitor_id = monitor_dir.name
        for md_path in collect_finding_files(monitor_dir, args.candidates):
            total += 1
            try:
                fm = parse_frontmatter(md_path)
            except ValueError as exc:
                failed += 1
                print(f"FAIL  {md_path.relative_to(ROOT)}: {exc}")
                continue
            if fm is None:
                if args.strict:
                    failed += 1
                    print(f"FAIL  {md_path.relative_to(ROOT)}: no frontmatter")
                continue
            # Inject monitor id if absent. Frontmatter today doesn't carry it.
            fm.setdefault("monitor", monitor_id)
            errors = sorted(validator.iter_errors(fm), key=lambda e: e.path)
            if errors:
                failed += 1
                print(f"FAIL  {md_path.relative_to(ROOT)}")
                for err in errors:
                    loc = ".".join(str(p) for p in err.absolute_path) or "<root>"
                    print(f"      [{loc}] {err.message}")

    print(f"\n{total} files checked, {failed} failed.")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
