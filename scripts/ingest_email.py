#!/usr/bin/env python3
"""
ingest_email.py — Legal Intelligence Briefing email ingestion v0.1

Companion to fetch_articles.py. Where fetch_articles.py pulls items from free
RSS feeds, this script pulls items from alert emails that arrive in a
dedicated Gmail inbox (myFT, MLex, subscribed law firm newsletters, etc.) —
the legitimate way to get headline + link + teaser from sources whose articles
sit behind a paywall.

Each alert is parsed into one or more (headline, link, teaser, published)
items, routed to a monitor/domain (by sender map + keyword match against the
same Tier 1/2 keywords used by the RSS scraper), and written as a candidate
markdown file into findings/candidates/YYYY-MM-DD/monitor/domain/ — the exact
same shape fetch_articles.py uses, so everything downstream (Netlify build,
ranker, HTML monitor pages) just works.

Auth: IMAP over SSL using a Gmail App Password.
  Set env vars GMAIL_USER and GMAIL_APP_PASSWORD before running.
  Generate an App Password at https://myaccount.google.com/apppasswords
  (requires 2-Step Verification turned on).

Run manually:        python scripts/ingest_email.py
Run via Actions:     .github/workflows/scrape.yml (cron daily 07:00 UTC)

Exit codes:
  0  ran (zero or more candidates written; or no creds configured — silent)
  1  hard failure (config malformed, etc.)
"""

from __future__ import annotations

import email
import email.policy
import imaplib
import os
import re
import sys
import time
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

import yaml
from bs4 import BeautifulSoup

# ---------- Shared helpers ------------------------------------------------
#
# These four helpers are intentionally duplicated from fetch_articles.py so
# this script stays standalone (importable without feedparser, runnable in a
# leaner env). If any of these are edited in fetch_articles.py, mirror the
# change here. They are small, stable, and rarely touched.

_LANG_OR_BROAD = re.compile(
    r"\s*\[(broad|FR|DE|IT|NL|ES|PT|PT-BR|PL|RO|TR|HU|GR|MT|FI|SE|DK|NO|LV)\]",
    re.IGNORECASE,
)
_LEADING_PUNCT = re.compile(r"^[*\-\s]+")
_TRAILING_PUNCT = re.compile(r"[:\s]+$")

_MIN_KEYWORD_LEN = 3
_STOP_WORDS = {
    "ai", "eu", "us", "uk", "fr", "de", "it", "es", "nl", "pt", "br",
    "the", "and", "of", "in", "to", "for", "on", "with",
}


def extract_keywords(md_path: Path) -> set[str]:
    """Tier 1+2 keywords from a domain's keywords.md (matches fetch_articles.py)."""
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
            cleaned = _LANG_OR_BROAD.sub("", raw)
            cleaned = _LEADING_PUNCT.sub("", cleaned)
            cleaned = _TRAILING_PUNCT.sub("", cleaned)
            cleaned = cleaned.strip()
            cleaned = re.sub(r"^\*+|\*+$", "", cleaned).strip()
            if not cleaned:
                continue
            for part in re.split(r"\s+/\s+", cleaned):
                part = part.strip().strip(".")
                if len(part) < _MIN_KEYWORD_LEN:
                    continue
                if part.lower() in _STOP_WORDS:
                    continue
                keywords.add(part)
    return keywords


def slugify(text: str, maxlen: int = 70) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen] or "item"


def make_match_regex(keyword: str) -> re.Pattern:
    if len(keyword) <= 8 and " " not in keyword:
        return re.compile(r"\b" + re.escape(keyword) + r"\b", re.IGNORECASE)
    return re.compile(re.escape(keyword), re.IGNORECASE)


def match_article(text: str, keyword_regexes: dict[str, re.Pattern]) -> list[str]:
    return [kw for kw, pat in keyword_regexes.items() if pat.search(text)]

# -------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
MONITORS_DIR = ROOT / "monitors"
EMAIL_SOURCES_FILE = ROOT / "scripts" / "email_sources.yml"
OUTPUT_BASE = ROOT / "findings" / "candidates"

IMAP_HOST = "imap.gmail.com"
IMAP_PORT = 993

# Cap per-run to keep the workflow bounded even if a backlog of unread alerts
# piles up. Anything older falls into the next run, or gets manually triaged.
MAX_EMAILS_PER_RUN = 200
MAX_ITEMS_PER_EMAIL = 50
TEASER_MAX_LEN = 600

# Links inside alert emails that are never the actual article.
SKIP_LINK_PATTERNS = re.compile(
    r"unsubscribe|view.in.browser|preferences|privacy.policy|"
    r"linkedin\.com|twitter\.com|x\.com/|facebook\.com|"
    r"youtube\.com|instagram\.com|mailto:|tel:|"
    r"mailchi\.mp/.*track|list-manage\.com",
    re.IGNORECASE,
)

# Tracking and redirect wrappers we strip from URLs so dedup works.
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "mc_cid", "mc_eid", "_hsenc", "_hsmi", "hsCtaTracking",
    "gclid", "fbclid", "msclkid", "yclid",
}


def _env(name: str) -> str | None:
    val = os.environ.get(name)
    return val.strip() if val else None


def normalise_url(raw: str) -> str:
    """Strip tracking params + fragment so two links to the same article match."""
    if not raw:
        return raw
    try:
        parts = urlparse(raw)
    except Exception:
        return raw
    if not parts.scheme or not parts.netloc:
        return raw
    cleaned_q = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                 if k not in TRACKING_PARAMS]
    return urlunparse((
        parts.scheme,
        parts.netloc.lower(),
        parts.path.rstrip("/") or parts.path,
        "",
        urlencode(cleaned_q),
        "",
    ))


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text[:TEASER_MAX_LEN]


def _html_to_soup(payload: str) -> BeautifulSoup:
    return BeautifulSoup(payload, "html.parser")


def _get_email_body(msg: EmailMessage) -> tuple[str, str]:
    """Return (html, text) bodies. Either may be empty string."""
    html_body = ""
    text_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = (part.get("Content-Disposition") or "").lower()
            if "attachment" in disp:
                continue
            try:
                payload = part.get_content()
            except Exception:
                continue
            if not isinstance(payload, str):
                continue
            if ctype == "text/html" and not html_body:
                html_body = payload
            elif ctype == "text/plain" and not text_body:
                text_body = payload
    else:
        ctype = msg.get_content_type()
        try:
            payload = msg.get_content()
        except Exception:
            payload = ""
        if isinstance(payload, str):
            if ctype == "text/html":
                html_body = payload
            else:
                text_body = payload
    return html_body, text_body


# ---------- Parsers ------------------------------------------------------

def parse_generic_html(html_body: str, sender: str) -> list[dict]:
    """Generic alert-email parser.

    Walk the HTML, collect every meaningful <a href=...>, pair it with the
    nearest preceding heading or surrounding paragraph as the teaser. Filters
    out unsubscribe/social/tracking links. Works on most law-firm newsletters
    and is the safe fallback for senders without a dedicated parser.
    """
    if not html_body:
        return []
    soup = _html_to_soup(html_body)

    # Drop common boilerplate containers so we don't pick up "View in browser"
    for selector in ["[class*=footer]", "[class*=unsubscribe]",
                     "[class*=social]", "[id*=footer]"]:
        for node in soup.select(selector):
            node.decompose()

    items: list[dict] = []
    seen_urls: set[str] = set()

    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        if not href or SKIP_LINK_PATTERNS.search(href):
            continue
        if not href.lower().startswith(("http://", "https://")):
            continue
        norm = normalise_url(href)
        if norm in seen_urls:
            continue

        # Headline: link text if it has any words, else nearest preceding heading.
        link_text = _clean_text(link.get_text(" "))
        headline = link_text
        if len(headline) < 8:
            heading = link.find_previous(["h1", "h2", "h3", "h4", "strong", "b"])
            if heading:
                headline = _clean_text(heading.get_text(" "))
        if not headline or len(headline) < 8:
            continue
        # Reject if the headline is purely a CTA like "Read more".
        if re.fullmatch(
            r"(read more|learn more|continue reading|view|click here|"
            r"download|register|read full article)\s*[.>»]*",
            headline, re.IGNORECASE,
        ):
            # Use the nearest heading instead.
            heading = link.find_previous(["h1", "h2", "h3", "h4"])
            headline = _clean_text(heading.get_text(" ")) if heading else ""
            if not headline:
                continue

        # Teaser: nearest enclosing paragraph or list item.
        teaser_node = link.find_parent(["p", "li", "td", "div"])
        teaser = _clean_text(teaser_node.get_text(" ")) if teaser_node else ""
        # Remove the headline from the teaser if it's just duplicated at the start.
        if teaser.lower().startswith(headline.lower()):
            teaser = _clean_text(teaser[len(headline):].lstrip(" -—:|"))

        seen_urls.add(norm)
        items.append({
            "headline": headline,
            "link": norm,
            "teaser": teaser,
            "sender": sender,
        })
        if len(items) >= MAX_ITEMS_PER_EMAIL:
            break

    return items


def parse_mlex(html_body: str, text_body: str, subject: str, sender: str) -> list[dict]:
    """MLex alerts — typically subject = article title; body has lede + deep link.

    Strategy:
    1. Try parse_generic_html first; if it finds items, return those.
    2. Else fall back to subject-as-headline + first http link in the body.
    """
    items = parse_generic_html(html_body, sender)
    if items:
        return items
    # Fallback for plain-text alerts
    link_match = re.search(r"https?://\S+", text_body or "")
    if not link_match:
        return []
    link = normalise_url(link_match.group(0).rstrip(".,);"))
    if SKIP_LINK_PATTERNS.search(link):
        return []
    return [{
        "headline": _clean_text(subject) or "MLex alert",
        "link": link,
        "teaser": _clean_text(text_body)[:TEASER_MAX_LEN],
        "sender": sender,
    }]


def parse_ft_myft(html_body: str, sender: str) -> list[dict]:
    """FT myFT digest emails. Items are usually anchor-wrapped headlines
    inside a structured table; the generic parser handles this well, but we
    also bias toward longer link text (FT standfirsts often sit next to the
    headline link)."""
    return parse_generic_html(html_body, sender)


def parser_for(parser_hint: str):
    return {
        "mlex": "mlex",
        "ft-myft": "ft",
        "generic": "generic",
    }.get((parser_hint or "generic").lower(), "generic")


# ---------- Routing ------------------------------------------------------

def load_keyword_index() -> dict[str, dict[str, set[str]]]:
    """Return {monitor: {domain: {keyword, ...}}} by walking the same
    keywords.md files the RSS scraper uses."""
    index: dict[str, dict[str, set[str]]] = {}
    if not MONITORS_DIR.is_dir():
        return index
    for monitor_dir in sorted(MONITORS_DIR.iterdir()):
        if not monitor_dir.is_dir():
            continue
        per_domain: dict[str, set[str]] = {}
        for domain_dir in sorted(monitor_dir.iterdir()):
            if not domain_dir.is_dir() or domain_dir.name == "findings":
                continue
            kw_file = domain_dir / "keywords.md"
            if not kw_file.exists():
                continue
            kws = extract_keywords(kw_file)
            if kws:
                per_domain[domain_dir.name] = kws
        if per_domain:
            index[monitor_dir.name] = per_domain
    return index


def route_item(
    item: dict,
    sender_default: tuple[str, str] | None,
    kw_index: dict[str, dict[str, set[str]]],
) -> tuple[str, str, list[str]] | None:
    """Decide monitor + domain + matched keywords for an item.

    1. Run keyword match across every domain. The (monitor, domain) with the
       most matches wins. Ties broken by sender default if it's one of the
       tied candidates, else alphabetical for stability.
    2. If zero matches anywhere and a sender default exists, use that with
       an empty matched-keywords list (still useful — the persona can review).
    3. Else return None (item is dropped).
    """
    text = f"{item['headline']} {item.get('teaser', '')}"
    best: list[tuple[str, str, list[str]]] = []
    best_count = 0
    for monitor, domains in kw_index.items():
        for domain, keywords in domains.items():
            regexes = {kw: make_match_regex(kw) for kw in keywords}
            matched = match_article(text, regexes)
            if not matched:
                continue
            if len(matched) > best_count:
                best = [(monitor, domain, matched)]
                best_count = len(matched)
            elif len(matched) == best_count:
                best.append((monitor, domain, matched))

    if best:
        if sender_default and len(best) > 1:
            for monitor, domain, matched in best:
                if (monitor, domain) == sender_default:
                    return monitor, domain, matched
        return best[0]

    if sender_default:
        return sender_default[0], sender_default[1], []

    return None


def match_sender(from_header: str, configured: list[dict]) -> dict | None:
    """Return the matching email_sources.yml entry for a From: header, or None."""
    if not from_header:
        return None
    lower = from_header.lower()
    for entry in configured:
        for pattern in entry.get("match", []):
            if pattern.lower() in lower:
                return entry
    return None


# ---------- Output -------------------------------------------------------

def write_candidate(
    monitor: str,
    domain: str,
    item: dict,
    matched: list[str],
    sender_label: str,
    today: str,
) -> bool:
    out_dir = OUTPUT_BASE / today / monitor / domain
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(item["headline"])
    out_file = out_dir / f"{slug}.md"
    if out_file.exists():
        return False

    # Confidentiality pre-filter — see strategy.md > Confidentiality pre-filter.
    try:
        from lib_confidentiality import is_confidential, load_watchlist, quarantine  # type: ignore

        watchlist = load_watchlist(SCRIPTS_DIR)
        body_text = f"{item['headline']}\n{item.get('teaser','')}"
        hit, category = is_confidential(
            body_text,
            url=item.get("link", ""),
            sender=sender_label,
            watchlist=watchlist,
        )
        if hit:
            quarantine(
                candidate_text=body_text,
                reason=category or "unspecified",
                source_url=item.get("link", ""),
                source_publisher=sender_label,
                sender=sender_label,
                root=ROOT,
                watchlist=watchlist,
            )
            return False
    except ImportError:
        pass

    safe_title = item["headline"].replace('"', "'").replace("\n", " ").strip()
    safe_source = (sender_label or "email alert").replace('"', "'")
    matched_yaml = ", ".join(f'"{k}"' for k in matched[:15])

    body = f"""---
date_found: {today}
monitor: {monitor}
domain: {domain}
source_url: "{item['link']}"
source_publisher: "{safe_source}"
source_date: "{item.get('published', '')}"
title: "{safe_title}"
matched_keywords: [{matched_yaml}]
match_count: {len(matched)}
status: candidate
ingest_source: email
---

# {item['headline']}

**Source:** [{safe_source}]({item['link']})
**Published:** {item.get('published') or "unknown"}
**Matched keywords ({len(matched)}):** {", ".join(matched[:15]) or "_routed by sender default — no keyword match_"}

## Summary excerpt

{item.get('teaser') or "_No teaser in the alert email._"}

---

*Auto-generated candidate from `scripts/ingest_email.py` (email ingestion).
Review against the persona's `interrogation-checklist.md` before promoting
to a formal finding under `output-schema.md`.*
"""
    out_file.write_text(body, encoding="utf-8")
    return True


# ---------- IMAP loop ----------------------------------------------------

def _decode_header(raw: str | None) -> str:
    if not raw:
        return ""
    from email.header import decode_header, make_header
    try:
        return str(make_header(decode_header(raw)))
    except Exception:
        return raw


def _quote_mailbox(name: str) -> str:
    """Quote a Gmail label/folder name for IMAP SELECT. Gmail exposes labels
    as folders, and labels with '/' or spaces (e.g. 'Briefing/Ingest') need
    to be quoted in the SELECT command. INBOX is conventionally unquoted."""
    if not name:
        return "INBOX"
    if name == "INBOX":
        return name
    if name.startswith('"') and name.endswith('"'):
        return name
    return '"' + name.replace('"', r'\"') + '"'


def _open_inbox(user: str, password: str, mailbox: str):
    conn = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    conn.login(user, password)
    typ, data = conn.select(_quote_mailbox(mailbox))
    if typ != "OK":
        # Surface Gmail's reason (label missing, IMAP disabled by admin, etc.)
        detail = (data[0].decode() if data and isinstance(data[0], bytes)
                  else (str(data[0]) if data else ""))
        raise RuntimeError(
            f"Could not select mailbox {mailbox!r}: {detail}. "
            f"If you're on Prosus Workspace, check that IMAP is enabled in "
            f"Gmail Settings → Forwarding and POP/IMAP, and that the label "
            f"exists exactly as configured."
        )
    return conn


def fetch_message_ids(conn) -> list[bytes]:
    """All UNSEEN messages. We rely on Gmail's read/unread state as our
    'processed' marker — once we successfully write candidates for an email
    we mark it \\Seen and apply a Cowork/Processed label."""
    typ, data = conn.search(None, "UNSEEN")
    if typ != "OK" or not data or not data[0]:
        return []
    ids = data[0].split()
    return ids[-MAX_EMAILS_PER_RUN:]


def fetch_message(conn, msg_id: bytes) -> EmailMessage | None:
    typ, data = conn.fetch(msg_id, "(RFC822)")
    if typ != "OK" or not data:
        return None
    for part in data:
        if isinstance(part, tuple) and len(part) >= 2:
            raw = part[1]
            if isinstance(raw, (bytes, bytearray)):
                return email.message_from_bytes(raw, policy=email.policy.default)
    return None


def mark_processed(conn, msg_id: bytes, label: str) -> None:
    """Apply the configured Gmail label and mark the message seen. Labels
    containing '/' or spaces need to be quoted; X-GM-LABELS takes a
    parenthesised list of label strings."""
    try:
        quoted = label if label.startswith('"') else f'"{label}"'
        conn.store(msg_id, "+X-GM-LABELS", f"({quoted})")
    except Exception:
        pass
    try:
        conn.store(msg_id, "+FLAGS", "\\Seen")
    except Exception:
        pass


# ---------- Main ---------------------------------------------------------

def main() -> int:
    user = _env("GMAIL_USER")
    password = _env("GMAIL_APP_PASSWORD")
    if not user or not password:
        print("ingest_email: GMAIL_USER / GMAIL_APP_PASSWORD not set — "
              "skipping email ingest.", file=sys.stderr)
        return 0

    if not EMAIL_SOURCES_FILE.exists():
        print(f"ingest_email: {EMAIL_SOURCES_FILE} missing — nothing to do.",
              file=sys.stderr)
        return 0

    cfg = yaml.safe_load(EMAIL_SOURCES_FILE.read_text(encoding="utf-8")) or {}
    mailbox = cfg.get("mailbox", "INBOX")
    processed_label = cfg.get("processed_label", "Cowork/Processed")
    senders: list[dict] = cfg.get("senders") or []

    if not senders:
        print("ingest_email: no senders configured in email_sources.yml — "
              "nothing to do.", file=sys.stderr)
        return 0

    kw_index = load_keyword_index()
    if not kw_index:
        print("ingest_email: no keyword files found under monitors/ — "
              "items will route by sender default only.", file=sys.stderr)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    try:
        conn = _open_inbox(user, password, mailbox)
    except imaplib.IMAP4.error as exc:
        print(f"ingest_email: IMAP login failed: {exc}", file=sys.stderr)
        return 0
    except Exception as exc:
        print(f"ingest_email: could not open inbox: {exc}", file=sys.stderr)
        return 0

    written = 0
    processed_emails = 0
    skipped_no_sender = 0
    skipped_no_route = 0

    try:
        msg_ids = fetch_message_ids(conn)
        print(f"ingest_email: {len(msg_ids)} unread message(s) to scan",
              file=sys.stderr)

        for msg_id in msg_ids:
            msg = fetch_message(conn, msg_id)
            if msg is None:
                continue

            from_header = _decode_header(msg.get("From"))
            subject = _decode_header(msg.get("Subject"))
            sender_entry = match_sender(from_header, senders)
            if not sender_entry:
                skipped_no_sender += 1
                # Don't mark as seen — leave it for human triage.
                continue

            parser_kind = parser_for(sender_entry.get("parser", "generic"))
            sender_label = sender_entry.get("label") or from_header
            sender_default: tuple[str, str] | None = None
            default = sender_entry.get("default")
            if isinstance(default, dict) and default.get("monitor") and default.get("domain"):
                sender_default = (default["monitor"], default["domain"])

            html_body, text_body = _get_email_body(msg)

            if parser_kind == "mlex":
                items = parse_mlex(html_body, text_body, subject, sender_label)
            elif parser_kind == "ft":
                items = parse_ft_myft(html_body, sender_label)
            else:
                items = parse_generic_html(html_body, sender_label)

            # Inherit Date: header for items that don't carry their own.
            try:
                date_iso = parsedate_to_datetime(
                    msg.get("Date") or ""
                ).astimezone(timezone.utc).isoformat()
            except Exception:
                date_iso = ""

            per_email_written = 0
            for item in items:
                item.setdefault("published", date_iso)
                routed = route_item(item, sender_default, kw_index)
                if not routed:
                    skipped_no_route += 1
                    continue
                monitor, domain, matched = routed
                if write_candidate(monitor, domain, item, matched,
                                   sender_label, today):
                    per_email_written += 1
                    written += 1

            processed_emails += 1
            if per_email_written > 0:
                # Only mark as processed if we actually wrote something. Empty
                # parses (e.g., a marketing wrapper with no real items) stay
                # unread so we can audit and improve the parser.
                mark_processed(conn, msg_id, processed_label)
            time.sleep(0.05)

    finally:
        try:
            conn.close()
        except Exception:
            pass
        try:
            conn.logout()
        except Exception:
            pass

    print(
        f"ingest_email: processed {processed_emails} email(s); "
        f"wrote {written} candidate(s); "
        f"skipped {skipped_no_sender} (no sender match), "
        f"{skipped_no_route} (no route)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
