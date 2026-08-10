"""Validate exact A1 lexical selection, Oxford treatment, and ownership."""

import json

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_lexical_item_catalog import ITEMS
from scripts.a1_lexical_ownership_contract import (
    FUNCTIONS, INPUTS, ITEM_TYPES, OUTPUT, OXFORD, OXFORD_DISPOSITIONS, REGISTERS,
    ROOT, SCHEMA, WORKLIST,
)
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
        errors.append("lexical ownership input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    worklist = _load(WORKLIST)
    candidate_ids = {row["candidate_id"] for row in worklist["candidates"]}
    evidence_ids = {
        ref for row in worklist["candidates"]
        for ref in row["evidence"]["level_fit"]["matched_all_level_record_ids"]
    }
    function_ids = {row["function_code"] for row in _load(FUNCTIONS)["strands"]}
    oxford_ids = {
        row["record_id"] for row in _load(OXFORD)["records"]
        if row["interpretation"]["cefr_codes"] == ["a1"]
    }
    item_ids = [row["lexical_item_id"] for row in data["course_items"]]
    expected_item_ids = [row["lexical_item_id"] for row in ITEMS]
    if item_ids != expected_item_ids or len(item_ids) != len(set(item_ids)):
        errors.append("lexical item catalog or order changed")
    known_items = set(item_ids)
    for row in data["course_items"]:
        if row["item_type"] not in ITEM_TYPES or row["register"] not in REGISTERS:
            errors.append(f"{row['lexical_item_id']}: uncontrolled type or register")
        locations = {row["introduction_location"], *row["recycle_locations"]}
        unknown_locations = {
            value for value in locations
            if value.startswith("lesson_candidate.") and value not in candidate_ids
        }
        if unknown_locations:
            errors.append(f"{row['lexical_item_id']}: unknown locations {sorted(unknown_locations)}")
        if set(row["communicative_owner_ids"]) - function_ids:
            errors.append(f"{row['lexical_item_id']}: unknown communicative owner")
        if row["introduction_location"] in row["recycle_locations"]:
            errors.append(f"{row['lexical_item_id']}: introduction reused as recycle")
        if not set(row["source_refs"]).issubset(oxford_ids | evidence_ids):
            errors.append(f"{row['lexical_item_id']}: unknown source reference")
    disposition_ids = [row["source_record_id"] for row in data["oxford_a1_dispositions"]]
    if set(disposition_ids) != oxford_ids or len(disposition_ids) != len(set(disposition_ids)):
        errors.append("Oxford A1 disposition inventory changed")
    for row in data["oxford_a1_dispositions"]:
        if row["disposition"] not in OXFORD_DISPOSITIONS:
            errors.append(f"{row['source_record_id']}: uncontrolled disposition")
        if set(row["course_item_ids"]) - known_items:
            errors.append(f"{row['source_record_id']}: unknown selected item")
        selected = row["disposition"] == "selected_course_item"
        if selected != bool(row["course_item_ids"]):
            errors.append(f"{row['source_record_id']}: selection ownership mismatch")
    expected_vocab = {
        row["candidate_id"] for row in worklist["candidates"]
        if row["current_language_targets"]["vocabulary"]
    }
    expected_phrases = {
        row["candidate_id"] for row in worklist["candidates"]
        if row["current_language_targets"]["phrases"]
    }
    candidate_rows = {row["candidate_id"]: row for row in data["candidate_ownership"]}
    if set(candidate_rows) != expected_vocab | expected_phrases:
        errors.append("legacy lexical candidate inventory changed")
    for candidate_id, row in candidate_rows.items():
        if not row["lexical_item_ids"] or set(row["lexical_item_ids"]) - known_items:
            errors.append(f"{candidate_id}: missing or unknown lexical ownership")
    required_fields = set(_load(INPUTS[1])["selection_contract"]["required_item_fields"])
    if any(not required_fields.issubset(row) for row in data["course_items"]):
        errors.append("a selected item is missing a global lexical-contract field")
    integrity = (
        "uncovered_vocabulary_candidate_ids", "uncovered_phrase_candidate_ids",
        "unknown_candidate_location_ids", "unknown_communicative_owner_ids",
        "items_without_source_refs", "items_without_recycle_locations", "items_without_oxford_refs",
    )
    if any(data["audit"][field] for field in integrity):
        errors.append("lexical ownership audit retains an integrity error")
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
