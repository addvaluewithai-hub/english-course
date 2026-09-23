#!/usr/bin/env python3
"""Snapshot and parse the current official Oxford Phrase List web page."""
from __future__ import annotations

import hashlib
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.oxfordlearnersdictionaries.com/wordlists/oxford-phrase-list"
RAW = ROOT / "sources/raw/vocabulary/oxford-phrase-list-online.html"
OUT = ROOT / "data/derived/oxford-phrase-list-online.json"
LEVELS = {"a1", "a2", "b1", "b2", "c1"}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> None:
    request = urllib.request.Request(
        URL,
        headers={
            "User-Agent": "Mozilla/5.0 curriculum-source-audit/1.0",
            "Accept-Language": "en-GB,en;q=0.9",
        },
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        html = response.read()
    if b"Oxford Phrase List" not in html:
        raise SystemExit("Official phrase-list page marker missing")

    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_bytes(html)
    soup = BeautifulSoup(html, "html.parser")

    records: list[dict] = []
    tag_signatures: Counter[str] = Counter()
    for li in soup.find_all("li"):
        strings = [norm(s) for s in li.stripped_strings if norm(s)]
        level_hits = [s.casefold() for s in strings if s.casefold() in LEVELS]
        if len(level_hits) != 1:
            continue
        level = level_hits[0]
        anchors = [a for a in li.find_all("a") if norm(a.get_text(" ", strip=True))]
        if not anchors:
            continue
        phrase = norm(anchors[0].get_text(" ", strip=True))
        if not phrase or phrase.casefold() in LEVELS or phrase in {"Find out more", "Download"}:
            continue
        # Keep only compact list rows: nested/navigation list items can contain many strings.
        if len(strings) > 8:
            continue
        signature = f"li.class={','.join(li.get('class', []))}|a.class={','.join(anchors[0].get('class', []))}"
        tag_signatures[signature] += 1
        records.append({
            "record_id": f"oxford.phrase.online.{len(records) + 1:04d}",
            "level": level.upper(),
            "phrase": phrase,
            "href": anchors[0].get("href"),
        })

    # De-duplicate exact DOM repeats while preserving first-seen order.
    deduped: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for record in records:
        key = (record["level"], record["phrase"].casefold())
        if key in seen:
            continue
        seen.add(key)
        record["record_id"] = f"oxford.phrase.online.{len(deduped) + 1:04d}"
        deduped.append(record)

    counts = Counter(r["level"] for r in deduped)
    print("raw candidates:", len(records))
    print("deduped:", len(deduped))
    print("level counts:", dict(counts))
    print("tag signatures:", dict(tag_signatures.most_common(10)))
    print("first records:", [(r["level"], r["phrase"]) for r in deduped[:20]])
    print("last records:", [(r["level"], r["phrase"]) for r in deduped[-20:]])

    if not 500 <= len(deduped) <= 800:
        raise SystemExit(f"Implausible current Oxford Phrase List count: {len(deduped)}")
    if set(counts) != {x.upper() for x in LEVELS}:
        raise SystemExit(f"Level coverage incomplete: {dict(counts)}")

    digest = hashlib.sha256(html).hexdigest().upper()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({
        "schema_version": 1,
        "dataset_id": "oxford_phrase_list_online",
        "source_url": URL,
        "source_file": str(RAW.relative_to(ROOT)).replace("\\", "/"),
        "source_sha256": digest,
        "record_count": len(deduped),
        "level_counts": dict(counts),
        "status": "official_online_snapshot_extracted_pending_reconciliation",
        "records": deduped,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
