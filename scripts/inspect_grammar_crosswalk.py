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


def compact(value: Any, depth: int = 0) -> Any:
    if depth >= 3:
        if isinstance(value, dict):
            return {"type": "dict", "keys": sorted(value.keys())}
        if isinstance(value, list):
            return {"type": "list", "length": len(value)}
        return value
    if isinstance(value, dict):
        return {k: compact(v, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return [compact(v, depth + 1) for v in value[:5]]
    return value


def main() -> None:
    data = json.loads(STRANDS.read_text(encoding="utf-8"))
    families = data["families"]
    crosswalk = data["gse_crosswalk"]
    gse_records = json.loads(GSE.read_text(encoding="utf-8"))["records"]

    print("FAMILY_COUNT", len(families))
    print("CROSSWALK_TYPE", type(crosswalk).__name__)
    print("CROSSWALK_COMPACT", json.dumps(compact(crosswalk), ensure_ascii=False, sort_keys=True)[:20000])

    records = None
    if isinstance(crosswalk, list):
        records = crosswalk
    elif isinstance(crosswalk, dict):
        for key, value in crosswalk.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                print("CROSSWALK_LIST_FIELD", key, len(value), "FIRST_KEYS", sorted(value[0].keys()))
                print("CROSSWALK_FIRST", json.dumps(value[0], ensure_ascii=False, sort_keys=True))
                if records is None or len(value) > len(records):
                    records = value
            elif not isinstance(value, (dict, list)):
                print("CROSSWALK_SCALAR", key, value)
    if records is None:
        records = []

    if records:
        all_keys = Counter(k for row in records for k in row.keys())
        print("CROSSWALK_RECORD_KEYS", dict(sorted(all_keys.items())))
        for candidate in (
            "record_id", "gse_record_id", "source_record_id", "family_id", "family_ids",
            "level", "cefr", "cefr_codes", "status", "disposition", "match_type", "rationale"
        ):
            values = [row.get(candidate) for row in records if candidate in row]
            if values:
                printable = Counter(
                    json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else str(v)
                    for v in values
                )
                print("FIELD", candidate, "COUNT", len(values), "TOP", printable.most_common(50))

    source_ids = {row["record_id"] for row in gse_records}
    crosswalk_ids: list[str] = []
    for row in records:
        for key in ("gse_record_id", "source_record_id", "record_id"):
            value = row.get(key)
            if isinstance(value, str) and value.startswith("gse.grammar."):
                crosswalk_ids.append(value)
                break
    print("GSE_SOURCE_IDS", len(source_ids))
    print("CROSSWALK_GSE_IDS", len(crosswalk_ids), "UNIQUE", len(set(crosswalk_ids)))
    print("MISSING_GSE_IDS", len(source_ids - set(crosswalk_ids)))
    print("EXTRA_GSE_IDS", len(set(crosswalk_ids) - source_ids))


if __name__ == "__main__":
    main()
