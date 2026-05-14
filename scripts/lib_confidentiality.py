#!/usr/bin/env python3
"""
lib_confidentiality.py — pre-filter against privileged or leniency-track content.

Two entry points:

  is_confidential(text, url, sender, watchlist) -> (bool, str | None)
      Cheap predicate. Returns (True, reason) on first match, else (False, None).

  quarantine(candidate_path, reason, watchlist, root) -> Path
      Writes an opaque stub to findings/_confidential/YYYY-MM-DD/ and appends a
      JSONL audit row. The original candidate body is dropped — the stub
      records path, sha256, sender, source domain, and the matching pattern
      *category* (not the matching phrase itself, so the audit log isn't a
      privileged keyword index).

Used by:
  - fetch_articles.py before writing a candidate
  - ingest_email.py before writing an email-derived candidate

Reads:
  - scripts/confidential_watchlist.yml          (gitignored, real)
  - scripts/confidential_watchlist.example.yml  (fallback, ships with repo)

Design properties worth knowing for any audit:
  - The watchlist itself can contain matter codes that are confidential, so it
    must be gitignored. The example file is safe to ship.
  - Matching is substring + case-insensitive. Regex was considered and rejected:
    a one-character typo in a regex can silently disable the filter; substring
    matching fails closed.
  - The audit log records pattern *category* (matter_code / keyword_phrase /
    sender_email), never the matching string itself.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

DEFAULT_WATCHLIST_NAMES = (
    "confidential_watchlist.yml",
    "confidential_watchlist.example.yml",
)


def load_watchlist(scripts_dir: Path) -> dict[str, Any]:
    """Load the real watchlist if present, fall back to the example."""
    for name in DEFAULT_WATCHLIST_NAMES:
        path = scripts_dir / name
        if path.exists():
            return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {}


def _lower_list(items: Any) -> list[str]:
    if not items:
        return []
    return [str(x).strip().lower() for x in items if str(x).strip()]


def is_confidential(
    text: str,
    url: str = "",
    sender: str = "",
    watchlist: dict[str, Any] | None = None,
) -> tuple[bool, str | None]:
    """Cheap predicate. Returns (hit, category) on first match."""
    if not watchlist:
        return False, None

    haystack = "\n".join([text or "", url or ""]).lower()
    sender_lc = (sender or "").lower()

    for code in _lower_list(watchlist.get("matter_codes")):
        if code and code in haystack:
            return True, "matter_code"

    for phrase in _lower_list(watchlist.get("keyword_phrases")):
        if phrase and phrase in haystack:
            return True, "keyword_phrase"

    for email in _lower_list(watchlist.get("sender_emails")):
        if email and email == sender_lc:
            return True, "sender_email"
        # Domain-only match: example.com matches alerts@example.com.
        if email and "@" not in email and sender_lc.endswith("@" + email):
            return True, "sender_email"

    return False, None


def quarantine(
    candidate_text: str,
    reason: str,
    source_url: str,
    source_publisher: str,
    sender: str,
    root: Path,
    watchlist: dict[str, Any],
) -> Path:
    """Write a redacted stub and append an audit-log row. Returns stub path."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    on_match = watchlist.get("on_match") or {}
    quarantine_dir_rel = on_match.get("quarantine_dir", "findings/_confidential")
    audit_log_rel = on_match.get("audit_log", f"{quarantine_dir_rel}/_audit-log.jsonl")

    qdir = root / quarantine_dir_rel / today
    qdir.mkdir(parents=True, exist_ok=True)

    sha = hashlib.sha256((candidate_text or "").encode("utf-8")).hexdigest()[:16]
    stub_path = qdir / f"{sha}.stub.md"
    stub_path.write_text(
        "\n".join(
            [
                "---",
                f"quarantined_at: {datetime.now(timezone.utc).isoformat()}",
                f"reason_category: {reason}",
                f"source_publisher: {source_publisher or '(unknown)'}",
                f"sha256_prefix: {sha}",
                "---",
                "",
                "Body redacted: matched confidential watchlist. "
                "See _audit-log.jsonl for category. Body itself is not stored.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    audit_path = root / audit_log_rel
    audit_path.parent.mkdir(parents=True, exist_ok=True)
    with audit_path.open("a", encoding="utf-8") as fh:
        fh.write(
            json.dumps(
                {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "category": reason,
                    "source_publisher": source_publisher,
                    "source_url_host": _host(source_url),
                    "sender": sender,
                    "sha256_prefix": sha,
                }
            )
            + "\n"
        )

    return stub_path


def _host(url: str) -> str:
    if not url:
        return ""
    try:
        from urllib.parse import urlparse

        return urlparse(url).hostname or ""
    except Exception:
        return ""
