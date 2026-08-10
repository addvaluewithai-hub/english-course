"""Validate exact A1 grammar source coverage and provisional ownership."""

import json

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_grammar_item_catalog import ITEMS
from scripts.a1_grammar_legacy_crosswalk import CROSSWALK
from scripts.a1_grammar_ownership_contract import (
    CONTROL_STATUSES, DISPOSITIONS, EGP, GSE_GRAMMAR, INPUTS, OUTPUT, ROOT, SCHEMA,
    SUPPORT_OWNER_IDS, WORKLIST,
)
from scripts.a1_grammar_source_assignments import EGP_ASSIGNMENTS, GSE_ASSIGNMENTS
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path=OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    expected_paths = [item.relative_to(ROOT).as_posix() for item in INPUTS]
    if [row["path"] for row in data["inputs"]] != expected_paths:
        errors.append("grammar ownership input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    egp_ids = {row["id"] for row in _load(EGP)["records"] if row["Level"] == "A1"}
    gse_ids = {
        row["record_id"] for row in _load(GSE_GRAMMAR)["records"]
        if row["interpretation"]["cefr_codes"] == ["a1"]
    }
    expected_egp = {row[0] for row in EGP_ASSIGNMENTS}
    expected_gse = {row[0] for row in GSE_ASSIGNMENTS}
    if egp_ids != expected_egp:
        errors.append("A1 EGP assignment inventory changed")
    if gse_ids != expected_gse:
        errors.append("A1 GSE Grammar assignment inventory changed")
    item_ids = [row["item_id"] for row in data["course_items"]]
    expected_items = [row["item_id"] for row in ITEMS]
    if item_ids != expected_items or len(item_ids) != len(set(item_ids)):
        errors.append("course item catalog or order changed")
    known_items = set(item_ids)
    known_candidates = {row["candidate_id"] for row in _load(WORKLIST)["candidates"]}
    for row in data["course_items"]:
        if row["control_status"] not in CONTROL_STATUSES:
            errors.append(f"{row['item_id']}: unknown control status")
        if not row["source_evidence"]["source_count"]:
            errors.append(f"{row['item_id']}: no source evidence")
        owners = set(row["introduction_owner_ids"] + row["recycle_owner_ids"])
        unknown = owners - known_candidates - SUPPORT_OWNER_IDS
        if unknown:
            errors.append(f"{row['item_id']}: unknown owners {sorted(unknown)}")
    actual_source_ids = {row["source_record_id"] for row in data["source_dispositions"]}
    if actual_source_ids != egp_ids | gse_ids:
        errors.append("source disposition coverage changed")
    for row in data["source_dispositions"]:
        if row["disposition"] not in DISPOSITIONS:
            errors.append(f"{row['source_record_id']}: unknown disposition")
        if set(row["course_item_ids"]) - known_items:
            errors.append(f"{row['source_record_id']}: unknown course item")
        is_transfer = row["disposition"].startswith("transfer_")
        if is_transfer == bool(row["course_item_ids"]):
            errors.append(f"{row['source_record_id']}: transfer/item mismatch")
    worklist = _load(WORKLIST)
    grammar_candidates = {
        row["candidate_id"]: row["current_language_targets"]["grammar"][0]
        for row in worklist["candidates"] if row["current_language_targets"]["grammar"]
    }
    actual_crosswalk = {row["candidate_id"]: row for row in data["legacy_target_crosswalk"]}
    if set(actual_crosswalk) != set(grammar_candidates) or set(actual_crosswalk) != set(CROSSWALK):
        errors.append("legacy grammar target crosswalk inventory changed")
    for candidate_id, target in grammar_candidates.items():
        row = actual_crosswalk.get(candidate_id, {})
        if row.get("legacy_target") != target or tuple(row.get("exact_item_ids", ())) != CROSSWALK.get(candidate_id):
            errors.append(f"{candidate_id}: legacy target crosswalk changed")
    integrity = (
        "orphan_source_ids", "unknown_course_item_ids", "unknown_owner_ids",
        "items_without_source_evidence", "items_without_recycle_owners", "unmapped_legacy_candidate_ids",
    )
    if any(data["audit"][field] for field in integrity):
        errors.append("grammar ownership audit retains an integrity error")
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
