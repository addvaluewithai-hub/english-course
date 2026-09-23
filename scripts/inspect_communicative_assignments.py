#!/usr/bin/env python3
"""Inspect reviewed communicative assignments for the A1-C2 ability inventory."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSIGNMENTS = ROOT / "data/reviewed/communicative-tag-assignments-v1.json"
STRANDS = ROOT / "data/reviewed/communicative-function-strands-v1.json"
CEFR = ROOT / "data/derived/cefr-all-descriptors.json"
GSE = ROOT / "data/derived/gse-all-objectives.json"


def summarize_record(record: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in record.items():
        if isinstance(value, dict):
            out[key] = {"type": "dict", "keys": sorted(value.keys())}
        elif isinstance(value, list):
            out[key] = {"type": "list", "length": len(value), "sample": value[:2]}
        else:
            out[key] = value
    return out


def find_record_list(data: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    candidates = [(key, value) for key, value in data.items() if isinstance(value, list) and value and isinstance(value[0], dict)]
    if not candidates:
        raise SystemExit("No record list found")
    return max(candidates, key=lambda item: len(item[1]))


def main() -> None:
    data = json.loads(ASSIGNMENTS.read_text(encoding="utf-8"))
    records = data["records"]
    strands = json.loads(STRANDS.read_text(encoding="utf-8"))["strands"]

    print("ASSIGNMENT_COUNT", len(records))
    print("DATASET_COUNTS", dict(Counter(r["source_dataset_id"] for r in records)))
    print("DISPOSITION_COUNTS", dict(Counter(r["source_disposition"] for r in records)))
    level_combo_counts = Counter(tuple(r["source_level_codes"]) for r in records)
    print("LEVEL_COMBO_COUNTS", {"+".join(k): v for k, v in sorted(level_combo_counts.items())})
    flat_levels = Counter(level for r in records for level in r["source_level_codes"])
    print("FLAT_LEVEL_COUNTS", dict(sorted(flat_levels.items())))
    multi_level = [r for r in records if len(r["source_level_codes"]) != 1]
    print("MULTI_LEVEL_RECORDS", len(multi_level), json.dumps(multi_level[:10], ensure_ascii=False))
    print("PRE_A1_RECORDS", sum("pre_a1" in r["source_level_codes"] for r in records))
    print("FUNCTION_COUNTS", dict(Counter(f for r in records for f in r["function_codes"]).most_common()))
    print("SKILL_COUNTS", dict(Counter(f for r in records for f in r["skill_codes"]).most_common()))
    print("MODE_COUNTS", dict(Counter(f for r in records for f in r["mode_codes"]).most_common()))

    function_stage_counts: Counter[tuple[str, str]] = Counter()
    for strand in strands:
        function = strand["function_code"]
        for stage in strand["lifecycle"]["stages"]:
            function_stage_counts[(function, stage["level"])] = stage["evidence_count"]
    print("FUNCTION_STAGE_NONZERO", sum(v > 0 for v in function_stage_counts.values()))
    print("FUNCTION_STAGE_ZERO", sum(v == 0 for v in function_stage_counts.values()))
    print("FUNCTION_STAGE_SAMPLES", list(function_stage_counts.items())[:30])

    for label, path in (("CEFR", CEFR), ("GSE", GSE)):
        source = json.loads(path.read_text(encoding="utf-8"))
        key, source_records = find_record_list(source)
        print(label, "TOP_KEYS", sorted(source.keys()))
        print(label, "RECORD_LIST", key, len(source_records))
        print(label, "FIRST_RECORD", json.dumps(summarize_record(source_records[0]), ensure_ascii=False, sort_keys=True))
        id_candidates = sorted({k for r in source_records[:50] for k in r.keys() if "id" in k.lower() or "record" in k.lower()})
        print(label, "ID_CANDIDATE_KEYS", id_candidates)
        text_candidates = sorted({k for r in source_records[:50] for k in r.keys() if any(t in k.lower() for t in ("text", "statement", "objective", "descriptor"))})
        print(label, "TEXT_CANDIDATE_KEYS", text_candidates)


if __name__ == "__main__":
    main()
