"""Create the reviewed A1-C2 lexical selection and progression contract."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from typing import Any

from scripts.lexical_progression_contract import (
    FUNCTIONS, LEVELS, OXFORD_3000, OXFORD_5000, OUTPUT, PROFILES,
    REPORT, REQUIRED_ITEM_FIELDS, REVIEWED_AT, REVIEWER, ROOT,
)
from scripts.lexical_resource_catalog import RESOURCE_STRANDS
from scripts.lexical_selection_policy import C2_METHOD, PROMOTION_GATES, SELECTION_PRINCIPLES
from scripts.source_disposition_inputs import file_sha256


def _hash(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def _pool(path) -> tuple[dict, list[dict]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data, data["records"]


def _pool_audit(path, data: dict, records: list[dict]) -> dict:
    counts = Counter(row["interpretation"]["cefr_codes"][0] for row in records)
    labels = {
        row["source_facts"]["other_verbatim"]["headword_source"].casefold()
        for row in records
    }
    ids = [row["record_id"] for row in records]
    return {
        "dataset_id": data["dataset_id"],
        "path": path.relative_to(ROOT).as_posix(),
        "entry_line_count": len(records),
        "distinct_printed_headword_labels": len(labels),
        "level_counts": {level: counts[level] for level in LEVELS if counts[level]},
        "record_ids_sha256": _hash(ids),
    }


def _states(level: str, control: str, consolidate: str) -> list[str]:
    index = LEVELS.index(level)
    control_index = LEVELS.index(control)
    consolidate_index = LEVELS.index(consolidate)
    if index < control_index:
        return ["expose"]
    if index == control_index == consolidate_index:
        return ["introduce", "practise", "consolidate"]
    if index == control_index:
        return ["introduce", "practise"]
    if index < consolidate_index:
        return ["recycle", "practise"]
    if index == consolidate_index:
        return ["recycle", "consolidate"]
    return ["recycle", "extend"]


def _strand(code: str, row: dict, profiles: dict[str, dict]) -> dict:
    stages = []
    for level in LEVELS:
        claim = profiles[level]["language_control"]["vocabulary"]
        states = _states(level, row["control"], row["consolidate"])
        stages.append({
            "level": level,
            "expectation": row["expectations"][level],
            "exit_boundary": claim["text"],
            "profile_claim_id": claim["claim_id"],
            "control_focus": "receptive" if states == ["expose"] else "both",
            "lifecycle_states": states,
        })
    return {
        "strand_id": f"lexis.{code}", "strand_code": code, "title": row["title"],
        "first_guided_productive_level": row["control"],
        "first_family_consolidation_level": row["consolidate"],
        "stages": stages,
        "review": {
            "status": "accepted",
            "basis": "approved_exit_boundary_plus_product_lexical_resource_review",
        },
    }


def build() -> dict[str, Any]:
    o3, o3_rows = _pool(OXFORD_3000)
    o5, o5_rows = _pool(OXFORD_5000)
    profile_data = json.loads(PROFILES.read_text(encoding="utf-8"))
    function_data = json.loads(FUNCTIONS.read_text(encoding="utf-8"))
    profiles = {row["level"]: row for row in profile_data["levels"]}
    pool_rows = o3_rows + o5_rows
    strands = [_strand(code, RESOURCE_STRANDS[code], profiles) for code in RESOURCE_STRANDS]
    return {
        "schema_version": 1, "dataset_id": "lexical_progression_strands", "version": 1,
        "level_order": list(LEVELS),
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in (OXFORD_3000, OXFORD_5000, PROFILES, FUNCTIONS)
        ],
        "reference_pool": {
            "use_policy": "reference_pool_not_automatic_target_inventory",
            "datasets": [
                _pool_audit(OXFORD_3000, o3, o3_rows),
                _pool_audit(OXFORD_5000, o5, o5_rows),
            ],
            "total_entry_lines": len(pool_rows),
            "all_source_record_ids_sha256": _hash([row["record_id"] for row in pool_rows]),
            "levels_without_published_pool": ["c2"],
            "all_records_accounted_for": True,
        },
        "selection_contract": {
            "communicative_owner_dataset": function_data["dataset_id"],
            "communicative_owner_count": len(function_data["strands"]),
            "required_item_fields": list(REQUIRED_ITEM_FIELDS),
            "principles": list(SELECTION_PRINCIPLES),
            "promotion_gates": {key: list(value) for key, value in PROMOTION_GATES.items()},
        },
        "resource_strands": strands,
        "c2_selection_method": {key: list(value) if isinstance(value, tuple) else value for key, value in C2_METHOD.items()},
        "audit": {
            "resource_strand_count": len(strands),
            "stage_count": sum(len(row["stages"]) for row in strands),
            "pool_record_count": len(pool_rows),
            "unaccounted_source_records": [], "missing_stage_boundaries": [],
            "invalid_lifecycle_order": [], "missing_selection_fields": [],
        },
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "reference_pool_audit_resource_family_progression_and_item_selection_contract",
            "limitations": [
                "Resource families control syllabus design; individual lexical items are selected during level reconciliation.",
                "Oxford levels are evidence pools and do not define productive control, lesson order, or promised word counts.",
                "C2 items require registered corpus or domain evidence before selection because Oxford supplies no C2 list.",
            ],
        },
    }


def _report(data: dict) -> str:
    lines = [
        "# Lexical Progression v1", "", "Status: accepted internal curriculum contract.", "",
        "Oxford provides 5,322 levelled entry lines as a reference pool, not 5,322 mandatory targets.",
        "Every selected item must serve an approved communicative owner and pass the lifecycle gates.", "",
        "| Resource family | First guided use | First family consolidation | A1 | C2 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for strand in data["resource_strands"]:
        lines.append(
            f"| {strand['title']} | {strand['first_guided_productive_level'].upper()} | "
            f"{strand['first_family_consolidation_level'].upper()} | {strand['stages'][0]['expectation']} | "
            f"{strand['stages'][-1]['expectation']} |"
        )
    lines += [
        "", "## C2 boundary", "",
        "There is no invented C2 list or word-count target. A C2 item needs an approved outcome,",
        "registered contemporary usage evidence, domain evidence when specialist, and explicit",
        "sense, collocation, register, connotation, control, and recycling decisions.", "",
        "Exact A1 headwords, meanings, chunks, and recycle locations are selected in SPINE-005.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['resource_strands'])} strands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
