"""Validate A1 function/dimension ownership, overlap coverage, and Unit 1 findings."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_ability_coverage_contract import (
    FUNCTIONS, INPUTS, OUTPUT, ROOT, SCHEMA, SUPPORT_FUNCTION_OWNERS, UNIT1, WORKLIST,
)
from scripts.a1_overlap_group_catalog import GROUPS, expand_id
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    if [row["path"] for row in data["inputs"]] != [item.relative_to(ROOT).as_posix() for item in INPUTS]:
        errors.append("ability-audit input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    candidates = _load(WORKLIST)["candidates"]
    candidate_ids = {row["candidate_id"] for row in candidates}
    required_functions = {
        row["function_code"] for row in _load(FUNCTIONS)["strands"]
        if row["lifecycle"]["consolidation_level"] == "a1"
    }
    functions = {row["function_code"]: row for row in data["function_coverage"]}
    if set(functions) != required_functions:
        errors.append("A1 function inventory changed")
    for code, row in functions.items():
        expected_candidates = [item["candidate_id"] for item in candidates if code in item["function_codes"]]
        if row["candidate_owner_ids"] != expected_candidates:
            errors.append(f"{code}: candidate ownership changed")
        if row["support_owner_ids"] != list(SUPPORT_FUNCTION_OWNERS.get(code, ())):
            errors.append(f"{code}: support ownership changed")
        if not row["candidate_owner_ids"] and not row["support_owner_ids"]:
            errors.append(f"{code}: A1 function is orphaned")
    expected_groups = {group_id: [expand_id(item) for item in short_ids] for group_id, short_ids, _ in GROUPS}
    actual_groups = {row["group_id"]: row["candidate_ids"] for row in data["overlap_groups"]}
    if actual_groups != expected_groups:
        errors.append("reviewed overlap groups changed")
    if any(item not in candidate_ids for values in actual_groups.values() for item in values):
        errors.append("overlap group references an unknown candidate")
    unit_ids = [row["candidate_id"] for row in _load(UNIT1)["lessons"]]
    if data["unit1_audit"]["candidate_ids"] != unit_ids:
        errors.append("Unit 1 candidate inventory or order changed")
    integrity = ("uncovered_function_codes", "uncovered_exit_dimensions", "unknown_overlap_candidate_ids")
    if any(data["audit"][field] for field in integrity):
        errors.append("ability audit retains a coverage or overlap integrity error")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL {OUTPUT}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
