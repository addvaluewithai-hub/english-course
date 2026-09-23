#!/usr/bin/env python3
"""Inspect the reviewed EGP/GSE Grammar family crosswalk compactly."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STRANDS = ROOT / "data/reviewed/grammar-family-strands-v1.json"
GSE = ROOT / "data/derived/gse-grammar-all.json"


def walk_keys(node: Any, prefix: str = "") -> Counter[str]:
    found: Counter[str] = Counter()
    if isinstance(node, dict):
        for key, value in node.items():
            path = f"{prefix}.{key}" if prefix else key
            if any(token in key.lower() for token in ("gse", "cross", "record", "source", "feature")):
                found[path] += 1
            found.update(walk_keys(value, path))
    elif isinstance(node, list):
        for value in node:
            found.update(walk_keys(value, prefix + "[]"))
    return found


def main() -> None:
    strands = json.loads(STRANDS.read_text(encoding="utf-8"))
    families = strands["families"]
    gse = json.loads(GSE.read_text(encoding="utf-8"))
    gse_records = gse["records"]
    print("TOP_KEYS", sorted(strands.keys()))
    print("FAMILY_COUNT", len(families))
    print("FAMILY_KEYS", sorted(families[0].keys()))
    print("FIRST_FAMILY", json.dumps(families[0], ensure_ascii=False)[:8000])
    print("INTERESTING_PATHS")
    for path, count in walk_keys(families).most_common(100):
        print(count, path)
    print("GSE_TOP_KEYS", sorted(gse.keys()))
    print("GSE_RECORD_COUNT", len(gse_records))
    print("GSE_RECORD_KEYS", sorted(gse_records[0].keys()))
    print("GSE_FIRST", json.dumps(gse_records[0], ensure_ascii=False, sort_keys=True))
    for candidate in ("Level", "level", "CEFR", "cefr", "record_id", "id"):
        vals = [r.get(candidate) for r in gse_records if candidate in r]
        if vals:
            print("GSE_FIELD", candidate, Counter(map(str, vals)).most_common(30))


if __name__ == "__main__":
    main()
