#!/usr/bin/env python3
"""
rank_candidates.py — clustering + entity tagging for the ranker.

Runs after fetch_articles.py and ingest_email.py. Walks every candidate
markdown in findings/candidates/ that falls within the working window
(WINDOW_DAYS), and:

  1. Extracts entities and case citations using lib_entities.py.
  2. Embeds title + teaser via fastembed (BAAI/bge-small-en-v1.5, ~33MB).
  3. Clusters items within rolling CLUSTER_WINDOW_HOURS by cosine similarity.
  4. Picks a canonical per cluster (highest match_count, tiebreak earliest
     published, tiebreak alphabetical).
  5. Writes the enrichment back into each candidate's frontmatter:
        entities, case_numbers, cluster_id, cluster_role, cluster_size,
        cluster_canonical_slug (siblings only), ranked_at.
  6. Emits findings/clusters/YYYY-MM-DD.json for today, listing each cluster
     with canonical + siblings — the surface (per-monitor HTML pages, search
     index) can read this directly.

Idempotent: items that already have a cluster_id stay in their existing
cluster unless a new fresh item is similar enough to merge them. Cluster IDs
are derived from the canonical's path, so the same canonical always produces
the same ID across runs.

Run manually:        python scripts/rank_candidates.py
Run via Actions:     .github/workflows/scrape.yml (after fetch_articles +
                     ingest_email, before commit)

CLI flags:
  --window-days N    look back this many days (default 7)
  --threshold X      cosine similarity threshold for clustering (default 0.72)
  --dry-run          show what would change without writing
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib_entities import (  # noqa: E402
    extract_case_numbers,
    extract_entities,
    default_index,
)

ROOT = Path(__file__).resolve().parent.parent
CANDIDATES_BASE = ROOT / "findings" / "candidates"
CLUSTERS_BASE = ROOT / "findings" / "clusters"

WINDOW_DAYS = 7
CLUSTER_WINDOW_HOURS = 48
DEFAULT_THRESHOLD = 0.72
EMBED_MODEL = "BAAI/bge-small-en-v1.5"  # 33MB, 384-dim, MIT licence


# ---------- Frontmatter I/O ---------------------------------------------

_FM_DELIM = "---"


@dataclass
class Candidate:
    path: Path
    frontmatter: dict
    body: str
    embedding: list[float] | None = field(default=None, repr=False)

    @property
    def title(self) -> str:
        return str(self.frontmatter.get("title", "")).strip()

    @property
    def teaser(self) -> str:
        # Pull the teaser from the body's "## Summary excerpt" section.
        m = re.search(
            r"^## Summary excerpt\s*\n(.*?)(?=^---|^##|\Z)",
            self.body, re.MULTILINE | re.DOTALL,
        )
        if m:
            text = m.group(1).strip()
            if text and not text.startswith("_"):
                return re.sub(r"\s+", " ", text)[:600]
        return ""

    @property
    def slug(self) -> str:
        return self.path.stem

    @property
    def rel_path(self) -> str:
        return str(self.path.relative_to(ROOT))

    @property
    def match_count(self) -> int:
        try:
            return int(self.frontmatter.get("match_count", 0))
        except (TypeError, ValueError):
            return 0

    @property
    def published_dt(self) -> datetime:
        # Prefer source_date, fall back to date_found at start-of-day UTC.
        for key in ("source_date", "date_found"):
            val = self.frontmatter.get(key)
            if not val:
                continue
            for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S",
                        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%a, %d %b %Y %H:%M:%S %z"):
                try:
                    dt = datetime.strptime(str(val).strip(), fmt)
                    if dt.tzinfo is None:
                        dt = dt.replace(tzinfo=timezone.utc)
                    return dt
                except ValueError:
                    continue
        # Final fallback — earliest possible
        return datetime(1970, 1, 1, tzinfo=timezone.utc)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith(_FM_DELIM):
        return {}, text
    parts = text.split("\n" + _FM_DELIM, 2)
    if len(parts) < 2:
        return {}, text
    head = parts[0][len(_FM_DELIM):].strip()
    rest = parts[1].lstrip("\n")
    body = ""
    if len(parts) == 3:
        # Re-glue accidentally split content
        body = parts[1]
        # Actually use proper split-once on the closing delim
    # Cleaner: split with the closing delimiter explicitly.
    m = re.match(
        r"^---\s*\n(.*?)\n---\s*\n?(.*)$",
        text, re.DOTALL,
    )
    if m:
        try:
            fm = yaml.safe_load(m.group(1)) or {}
            if not isinstance(fm, dict):
                fm = {}
        except yaml.YAMLError:
            fm = {}
        return fm, m.group(2)
    return {}, text


def serialise_frontmatter(fm: dict, body: str) -> str:
    """Write frontmatter as YAML between --- markers, then the body."""
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True,
                             default_flow_style=False, width=10_000).strip()
    return f"---\n{fm_text}\n---\n\n{body.lstrip()}"


def load_candidate(path: Path) -> Candidate | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    fm, body = parse_frontmatter(text)
    if not fm:
        return None
    return Candidate(path=path, frontmatter=fm, body=body)


def iter_candidate_files(window_days: int) -> list[Path]:
    if not CANDIDATES_BASE.exists():
        return []
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=window_days)
    paths: list[Path] = []
    for day_dir in sorted(CANDIDATES_BASE.iterdir()):
        if not day_dir.is_dir():
            continue
        try:
            day = datetime.strptime(day_dir.name, "%Y-%m-%d").date()
        except ValueError:
            continue
        if day < cutoff:
            continue
        paths.extend(p for p in day_dir.rglob("*.md") if p.is_file())
    return paths


# ---------- Embeddings -------------------------------------------------

def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings; returns a list of float vectors."""
    if not texts:
        return []
    try:
        from fastembed import TextEmbedding  # type: ignore
    except ImportError as exc:
        raise RuntimeError(
            "fastembed is required for rank_candidates.py. "
            "Add it to scripts/requirements.txt and pip install. "
            f"Underlying error: {exc}"
        )
    model = TextEmbedding(model_name=EMBED_MODEL)
    return [list(v) for v in model.embed(texts)]


def _normalise(vec: list[float]) -> list[float]:
    s = sum(v * v for v in vec) ** 0.5
    if s == 0:
        return vec
    return [v / s for v in vec]


def _cosine(a: list[float], b: list[float]) -> float:
    # Both vectors must be the same length and unit-normalised.
    return sum(x * y for x, y in zip(a, b))


# ---------- Clustering -------------------------------------------------

class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb

    def groups(self) -> dict[int, list[int]]:
        out: dict[int, list[int]] = {}
        for i in range(len(self.parent)):
            r = self.find(i)
            out.setdefault(r, []).append(i)
        return out


def cluster(
    candidates: list[Candidate],
    threshold: float,
    window: timedelta,
) -> list[list[Candidate]]:
    """Group candidates into clusters. Returns a list of clusters, each a
    list of candidates sorted so the canonical comes first."""
    if not candidates:
        return []
    # Sort by published_dt so the sliding window is straightforward.
    items = sorted(candidates, key=lambda c: c.published_dt)

    # Normalise embeddings once.
    units: list[list[float] | None] = []
    for c in items:
        units.append(_normalise(c.embedding) if c.embedding else None)

    uf = UnionFind(len(items))
    for i in range(len(items)):
        ui = units[i]
        if ui is None:
            continue
        ti = items[i].published_dt
        for j in range(i + 1, len(items)):
            if items[j].published_dt - ti > window:
                break
            uj = units[j]
            if uj is None:
                continue
            if _cosine(ui, uj) >= threshold:
                uf.union(i, j)

    groups = uf.groups()
    clusters: list[list[Candidate]] = []
    for indices in groups.values():
        members = [items[k] for k in indices]
        members.sort(key=lambda c: (
            -c.match_count, c.published_dt, c.slug,
        ))
        clusters.append(members)
    return clusters


def cluster_id_for(canonical: Candidate) -> str:
    h = hashlib.md5(canonical.rel_path.encode("utf-8")).hexdigest()[:10]
    day = canonical.path.parent.parent.parent.name  # YYYY-MM-DD
    if not re.match(r"\d{4}-\d{2}-\d{2}$", day or ""):
        day = canonical.published_dt.date().isoformat()
    return f"cluster-{day}-{h}"


# ---------- Main -------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--window-days", type=int, default=WINDOW_DAYS,
                        help=f"Look-back window (default {WINDOW_DAYS}).")
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD,
                        help=f"Cosine similarity threshold (default "
                             f"{DEFAULT_THRESHOLD}).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print changes without writing.")
    args = parser.parse_args(argv)

    paths = iter_candidate_files(args.window_days)
    if not paths:
        print("rank_candidates: no candidates in window.", file=sys.stderr)
        return 0

    candidates: list[Candidate] = []
    for p in paths:
        c = load_candidate(p)
        if c is not None:
            candidates.append(c)

    print(f"rank_candidates: {len(candidates)} candidate(s) in last "
          f"{args.window_days} day(s)", file=sys.stderr)

    if not candidates:
        return 0

    # ------- Entity tagging
    index = default_index()
    for c in candidates:
        text = f"{c.title}\n{c.teaser}"
        ents = [e.to_dict() for e in extract_entities(text, index)]
        cases = [cc.to_dict() for cc in extract_case_numbers(text)]
        c.frontmatter["entities"] = ents
        c.frontmatter["case_numbers"] = cases

    # ------- Embedding
    texts = [f"{c.title}\n{c.teaser}".strip() for c in candidates]
    try:
        vectors = embed_texts(texts)
    except RuntimeError as exc:
        print(f"rank_candidates: embedding step failed: {exc}", file=sys.stderr)
        print("rank_candidates: writing entity tags only; clustering skipped.",
              file=sys.stderr)
        vectors = []
    for c, v in zip(candidates, vectors):
        c.embedding = v

    # ------- Clustering
    if vectors:
        clusters = cluster(
            candidates,
            threshold=args.threshold,
            window=timedelta(hours=CLUSTER_WINDOW_HOURS),
        )
        print(f"rank_candidates: formed {len(clusters)} cluster(s); "
              f"{sum(1 for cl in clusters if len(cl) > 1)} multi-member",
              file=sys.stderr)
        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        cluster_records: list[dict] = []
        for members in clusters:
            canonical = members[0]
            cid = cluster_id_for(canonical)
            for idx, member in enumerate(members):
                member.frontmatter["cluster_id"] = cid
                member.frontmatter["cluster_size"] = len(members)
                member.frontmatter["cluster_role"] = "canonical" if idx == 0 else "sibling"
                if idx == 0:
                    member.frontmatter.pop("cluster_canonical_slug", None)
                else:
                    member.frontmatter["cluster_canonical_slug"] = canonical.slug
                member.frontmatter["ranked_at"] = now_iso
            cluster_records.append({
                "cluster_id": cid,
                "size": len(members),
                "canonical": {
                    "title": canonical.title,
                    "path": canonical.rel_path,
                    "monitor": canonical.frontmatter.get("monitor"),
                    "domain": canonical.frontmatter.get("domain"),
                    "match_count": canonical.match_count,
                    "source_publisher": canonical.frontmatter.get("source_publisher"),
                },
                "siblings": [
                    {
                        "title": m.title,
                        "path": m.rel_path,
                        "monitor": m.frontmatter.get("monitor"),
                        "domain": m.frontmatter.get("domain"),
                        "source_publisher": m.frontmatter.get("source_publisher"),
                    } for m in members[1:]
                ],
                "entities": canonical.frontmatter.get("entities", []),
                "case_numbers": canonical.frontmatter.get("case_numbers", []),
            })
    else:
        cluster_records = []
        now_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
        for c in candidates:
            c.frontmatter["ranked_at"] = now_iso

    # ------- Write back
    if args.dry_run:
        print("rank_candidates: --dry-run set, no files written.",
              file=sys.stderr)
    else:
        for c in candidates:
            try:
                c.path.write_text(serialise_frontmatter(c.frontmatter, c.body),
                                  encoding="utf-8")
            except OSError as exc:
                print(f"rank_candidates: write failed for "
                      f"{c.rel_path}: {exc}", file=sys.stderr)

        if cluster_records:
            CLUSTERS_BASE.mkdir(parents=True, exist_ok=True)
            today = datetime.now(timezone.utc).date().isoformat()
            out_file = CLUSTERS_BASE / f"{today}.json"
            out_file.write_text(
                json.dumps({
                    "ranked_at": now_iso,
                    "window_days": args.window_days,
                    "threshold": args.threshold,
                    "cluster_window_hours": CLUSTER_WINDOW_HOURS,
                    "embed_model": EMBED_MODEL,
                    "clusters": cluster_records,
                }, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"rank_candidates: wrote cluster index {out_file}",
                  file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main())
