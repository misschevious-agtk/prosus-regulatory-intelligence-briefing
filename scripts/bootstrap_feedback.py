#!/usr/bin/env python3
"""
bootstrap_feedback.py — seed a monitor's feedback log from worked examples.

Reads monitors/<monitor>/<domain>/cold-start-examples.md (one bullet per
example, leading 👍 or 👎) and writes one feedback file per example under
monitors/<monitor>/findings/feedback/. Each file is tagged `bootstrap: true`
so the persona-reconciliation script can ignore it by default.

Themes are extracted by substring-matching against glossary.md headers
and the persona's keywords.md Tier 1/2 entries. The simple approach is
deliberate; we want the bootstrap to be reproducible from the markdown
without an LLM in the loop.

Run:
    python scripts/bootstrap_feedback.py --monitor monitor-01
    python scripts/bootstrap_feedback.py --monitor monitor-01 --domain privacy
    python scripts/bootstrap_feedback.py --dry-run                       # all monitors, preview

Idempotency: filenames are slug-derived from the example text. Re-running
overwrites the same files.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml

ROOT = Path(__file__).resolve().parent.parent
MONITORS_DIR = ROOT / "monitors"
GLOSSARY = ROOT / "glossary.md"

UP_MARKERS = ("👍", ":+1:", "[up]", "[+]")
DOWN_MARKERS = ("👎", ":-1:", "[down]", "[-]")


def parse_examples(md_path: Path) -> list[tuple[str, str]]:
    """Returns a list of (vote, text) tuples extracted from bullet items."""
    if not md_path.exists():
        return []
    out: list[tuple[str, str]] = []
    for raw in md_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        m = re.match(r"^[-*]\s+(.+)$", line)
        if not m:
            continue
        body = m.group(1).strip()
        vote = None
        for marker in UP_MARKERS:
            if body.startswith(marker):
                vote = "up"
                body = body[len(marker):].lstrip(" .,-:—")
                break
        if vote is None:
            for marker in DOWN_MARKERS:
                if body.startswith(marker):
                    vote = "down"
                    body = body[len(marker):].lstrip(" .,-:—")
                    break
        if vote is None:
            continue
        if not body:
            continue
        out.append((vote, body))
    return out


def theme_vocabulary(monitor_dir: Path, domain: str) -> list[str]:
    """Lift theme strings from glossary.md headers + per-domain keywords.md tiers 1-2."""
    vocab: list[str] = []
    if GLOSSARY.exists():
        for line in GLOSSARY.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\*\*(.+?)\*\*\s*—", line)
            if m:
                vocab.append(m.group(1).strip())
    kw_path = monitor_dir / domain / "keywords.md"
    if kw_path.exists():
        in_tier = False
        for line in kw_path.read_text(encoding="utf-8").splitlines():
            if re.match(r"^## Tier [12]\b", line):
                in_tier = True
                continue
            if line.startswith("## "):
                in_tier = False
                continue
            if not in_tier:
                continue
            if " · " not in line:
                continue
            for chunk in line.split(" · "):
                token = re.sub(r"\[(broad|FR|DE|IT|NL|ES|PT|PT-BR|PL|RO|TR|HU|GR|MT|FI|SE|DK|NO|LV)\]", "", chunk).strip(" *-:")
                if 3 < len(token) < 80:
                    vocab.append(token)
    # De-dup while preserving order.
    seen: set[str] = set()
    out: list[str] = []
    for v in vocab:
        key = v.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(v)
    return out


def extract_themes(text: str, vocab: Iterable[str]) -> list[str]:
    hay = text.lower()
    matches: list[str] = []
    for term in vocab:
        if 3 < len(term) and term.lower() in hay:
            matches.append(term)
        if len(matches) >= 6:
            break
    return matches


def slugify(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower())
    s = s.strip("-")[:48] or "example"
    short = hashlib.sha1(text.encode("utf-8")).hexdigest()[:6]
    return f"{s}-{short}"


def write_feedback(feedback_dir: Path, vote: str, text: str, themes: list[str], today_iso: str) -> Path:
    feedback_dir.mkdir(parents=True, exist_ok=True)
    name = f"{today_iso}-bootstrap-{slugify(text)}.md"
    body = (
        "---\n"
        + yaml.safe_dump(
            {
                "vote": vote,
                "bootstrap": True,
                "themes": themes,
                "annotation": text,
                "date": today_iso,
            },
            sort_keys=False,
            allow_unicode=True,
        )
        + "---\n"
        f"\n# Bootstrap example\n\n{text}\n"
    )
    out = feedback_dir / name
    out.write_text(body, encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Bootstrap a monitor's feedback log from worked examples.")
    ap.add_argument("--monitor", help="One monitor (defaults to all).")
    ap.add_argument("--domain", help="One domain within --monitor.")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    monitors = [MONITORS_DIR / args.monitor] if args.monitor else sorted(MONITORS_DIR.iterdir())
    monitors = [m for m in monitors if m.is_dir()]
    if not monitors:
        print("No monitors to process.", file=sys.stderr)
        return 0

    today_iso = datetime.now(timezone.utc).date().isoformat()
    total = 0

    for monitor_dir in monitors:
        domains = [d for d in sorted(monitor_dir.iterdir()) if d.is_dir() and not d.name.startswith("_")]
        if args.domain:
            domains = [d for d in domains if d.name == args.domain]
        for dom in domains:
            examples_md = dom / "cold-start-examples.md"
            pairs = parse_examples(examples_md)
            if not pairs:
                continue
            vocab = theme_vocabulary(monitor_dir, dom.name)
            feedback_dir = monitor_dir / "findings" / "feedback"
            for vote, text in pairs:
                themes = extract_themes(text, vocab)
                if args.dry_run:
                    print(f"DRY  {monitor_dir.name}/{dom.name}  {vote}  {text[:80]}  themes={themes}")
                else:
                    write_feedback(feedback_dir, vote, text, themes, today_iso)
                    total += 1
            if not args.dry_run:
                print(f"Seeded {len(pairs)} examples for {monitor_dir.name}/{dom.name}")

    print(f"\nTotal bootstrap rows written: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
