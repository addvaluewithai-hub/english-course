"""Validate final A1 candidate decisions and exact ownership transfers."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_final_decision_catalog import DECISIONS
from scripts.a1_final_decisions_contract import INPUTS, OUTPUT, ROOT, SCHEMA, SUPPORT_OWNER_IDS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, item.absolute_path)) or '$'}: {item.message}"
        for item in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    expected_paths = [item.relative_to(ROOT).as_posix() for item in INPUTS]
    if [row["path"] for row in data["inputs"]] != expected_paths:
        errors.append("final-decision input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    worklist, dependency = _load(INPUTS[0]), _load(INPUTS[-1])
    decisions = data["decisions"]
    candidate_ids = [row["candidate_id"] for row in worklist["candidates"]]
    if [row["candidate_id"] for row in decisions] != candidate_ids:
        errors.append("decision inventory or order changed")
    if [row["candidate_id"] for row in DECISIONS] != candidate_ids:
        errors.append("reviewed decision catalog is incomplete or reordered")
    lesson_ids = {row["final_owner_id"] for row in data["final_lesson_capabilities"]}
    support_ids = {row["support_owner_id"] for row in data["support_owners"]}
    if support_ids != SUPPORT_OWNER_IDS:
        errors.append("support-owner inventory changed")
    valid_owners = lesson_ids | support_ids
    decision_index = {row["candidate_id"]: row for row in decisions}
    for row in decisions:
        if not set(row["final_owner_ids"]).issubset(valid_owners):
            errors.append(f"decision points to a non-final owner: {row['candidate_id']}")
        if row["primary_transfer_owner_id"] not in row["final_owner_ids"]:
            errors.append(f"primary transfer owner is not a final owner: {row['candidate_id']}")
        if row["survives_as_learner_lesson"] != (row["candidate_id"] in lesson_ids):
            errors.append(f"survival flag and owner inventory disagree: {row['candidate_id']}")
        if row["decision"] == "revise" and not row["revised_outcome_statement"]:
            errors.append(f"revised lesson has no final outcome: {row['candidate_id']}")
        if row["a1_fit_status"] != "fits_a1_boundary" and row["decision"] == "keep":
            errors.append(f"scope revision was ignored: {row['candidate_id']}")
    expected_transfers = {
        (row["candidate_id"], role, item)
        for row in decisions if not row["survives_as_learner_lesson"]
        for role, field in (("introduction", "exact_introduction_item_ids"), ("recycle", "exact_recycle_item_ids"))
        for item in row[field]
    }
    actual_transfers = {
        (row["source_candidate_id"], row["role"], row["item_id"])
        for row in data["ownership_transfers"]
    }
    if expected_transfers != actual_transfers or len(actual_transfers) != len(data["ownership_transfers"]):
        errors.append("exact role transfers are missing or duplicated")
    for row in data["ownership_transfers"]:
        source = decision_index[row["source_candidate_id"]]
        if row["destination_owner_id"] not in source["final_owner_ids"]:
            errors.append(f"transfer leaves the candidate decision: {row['source_candidate_id']}")
    expected_items = {row["item_id"] for row in dependency["exact_item_sequence"]}
    actual_items = {
        item for row in data["final_lesson_capabilities"] + data["support_owners"]
        for field in ("introduction_item_ids", "recycle_item_ids") for item in row[field]
    }
    if expected_items != actual_items:
        errors.append("final exact-item ownership is incomplete")
    for role, field in (("introduction", "introduction_item_ids"), ("recycle", "recycle_item_ids")):
        role_items = {
            item for row in data["final_lesson_capabilities"] + data["support_owners"]
            for item in row[field]
        }
        if role_items != expected_items:
            errors.append(f"final {role} ownership is incomplete")
    for row in data["exit_anchor_resolutions"]:
        if row["resolved_owner_ids"] != decision_index[row["anchor_candidate_id"]]["final_owner_ids"]:
            errors.append(f"exit anchor resolution is stale: {row['anchor_candidate_id']}")
    if data["audit"]["unresolved_questions"]:
        errors.append("final decisions retain unresolved questions")
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
