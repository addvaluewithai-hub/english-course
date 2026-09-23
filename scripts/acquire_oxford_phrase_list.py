#!/usr/bin/env python3
"""Acquire the official Oxford Phrase List PDF and record deterministic metadata."""
from __future__ import annotations

import hashlib
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.oxfordlearnersdictionaries.com/external/pdf/wordlists/oxford-phrase-list/Oxford%20Phrase%20List.pdf"
RAW = ROOT / "sources/raw/vocabulary/oxford-phrase-list.pdf"
META = ROOT / "data/derived/oxford-phrase-list-source.json"


def main() -> None:
    request = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 curriculum-source-audit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()
    if not content.startswith(b"%PDF-"):
        raise SystemExit("Oxford Phrase List acquisition did not return a PDF")
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_bytes(content)
    digest = hashlib.sha256(content).hexdigest().upper()
    metadata = {
        "schema_version": 1,
        "source_id": "oup.oxford_phrase_list",
        "official_url": URL,
        "raw_file": str(RAW.relative_to(ROOT)).replace("\\", "/"),
        "sha256": digest,
        "bytes": len(content),
        "published_scope": "750 common phrases; A1-C1",
        "status": "official_snapshot_acquired_pending_structured_extraction",
    }
    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
