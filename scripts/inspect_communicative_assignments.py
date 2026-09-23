#!/usr/bin/env python3
"""Inspect reviewed communicative assignments without dumping the full dataset."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = ROOT / "data/reviewed/communicative-tag-assignments-v1.json"
STRANDS = ROOT / "data/reviewed/communicative-function-strands-v1.json"


def summarize(value: Any, depth: int = 0) -> Any:
    if depth >= 2:
        if isinstance(value, dict):
            return {"type": "dict", "keys": sorted(value.keys())}
        if isinstance(value, list):
            return {"type": "list", "length": len(value)}
        return value
    if isinstance(value, dict):
        return {k: summarize(v, depth + 1) for k, v in value.items()}
    if isinstance(value, list):
        return [summarize(v, depth + 1) for v in value[:3]]
    return value


def main() -> None:
    data = json.loads(ASSIGNMENTS.read_text(encoding="utf-8"))
    strands = json.loads(STRANDS.read_text(encoding="utf-8"))
    print("ASSIGNMENT_TOP_KEYS", sorted(data.keys()))
    print("STRAND_TOP_KEYS", sorted(strands.keys()))

    list_fields = {k: v for k, v in data.items() if isinstance(v, list)}
    print("ASSIGNMENT_LIST_FIELDS", {k: len(v) for k, v in list_fields.items()})
    for key, values in list_fields.items():
        if not values:
            continue
        print("LIST", key, "FIRST_RECORD", json.dumps(summarize(values[0]), ensure_ascii=False, sort_keys=True))
        if isinstance(values[0], dict):
            print("LIST", key, "RECORD_KEYS", sorted(values[0].keys()))
            key_freq: Counter[str] = Counter()
            for record in values:
                if isinstance(record, dict):
                    key_freq.update(record.keys())
            print("LIST", key, "KEY_FREQ", dict(sorted(key_freq.items())))
            for candidate in (
                "level", "cefr", "cefr_level", "stage_level", "source", "source_id",
                "source_record_id", "record_id", "assignment_id", "function", "function_tag",
                "function_id", "strand_id", "skill", "mode", "disposition", "expected_control"
            ):
                vals = [record.get(candidate) for record in values if isinstance(record, dict) and candidate in record]
                if vals:
                    printable = Counter(json.dumps(v, sort_keys=True) if isinstance(v, (dict, list)) else str(v) for v in vals)
                    print("FIELD", key, candidate, "COUNT", len(vals), "TOP", printable.most_common(30))

    stage_refs: list[tuple[str, str, str]] = []
    for strand in strands.get("strands", []):
        strand_id = strand.get("strand_id")
        for stage in strand.get("stages", []):
            level = stage.get("level")
            for source_id in stage.get("source_record_ids", []):
                stage_refs.append((strand_id, level, source_id))
    print("STRAND_STAGE_REF_COUNT", len(stage_refs))
    print("STRAND_STAGE_REF_UNIQUE", len(set(stage_refs)))
    print("STRAND_STAGE_LEVEL_COUNTS", dict(Counter(level for _, level, _ in stage_refs)))
    print("STRAND_STAGE_SAMPLE", stage_refs[:20])


if __name__ == "__main__":
    main()
