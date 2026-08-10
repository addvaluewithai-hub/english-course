"""Validate the A1 prerequisite, recycling, mastery, and exit audit."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_dependency_mastery_contract import INPUTS, OUTPUT, ROOT, SCHEMA, SUPPORT_PROBES
from scripts.a1_dependency_mastery_policies import EXIT_ANCHORS, candidate_id
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
        errors.append("audit input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    sequence = data["provisional_sequence"]
    positions = {item: index for index, item in enumerate(sequence, start=1)}
    positions.update({item: len(sequence) + 1 for item in SUPPORT_PROBES})
    if len(sequence) != len(set(sequence)):
        errors.append("provisional sequence contains duplicates")
    for row in data["explicit_dependency_edges"]:
        expected = positions[row["dependency_id"]] < positions[row["candidate_id"]]
        if (row["status"] == "aligned") != expected:
            errors.append(f"dependency status is stale: {row['candidate_id']}")
    for row in data["exact_item_sequence"]:
        locations = row["introduction_location_ids"] + row["recycle_location_ids"]
        if any(item not in positions for item in locations):
            errors.append(f"unknown exact-item location: {row['item_id']}")
        if not row["later_recycle_location_ids"] and not row["status"].startswith("no_later"):
            errors.append(f"missing later-recycle finding: {row['item_id']}")
    if any(not row["transfer_required_if_merged_supported_or_retired"] for row in data["candidate_ownership_impacts"]):
        errors.append("a candidate has no exact-item ownership role")
    freshness = ("fresh", "new", "changed", "different", "unseen", "replacement", "another")
    for row in data["mastery_reviews"]:
        if not any(marker in row["fresh_task_family"].lower() for marker in freshness):
            errors.append(f"mastery task is not demonstrably fresh: {row['candidate_id']}")
        if row["construct_alignment_status"].startswith("requires") and not row["required_revision_actions"]:
            errors.append(f"mastery revision has no action: {row['candidate_id']}")
    safeguards = {row["dimension_code"]: row for row in data["exit_safeguards"]}
    if set(safeguards) != set(EXIT_ANCHORS):
        errors.append("exit dimension safeguard inventory changed")
    for dimension, short_ids in EXIT_ANCHORS.items():
        expected = [candidate_id(item) for item in short_ids]
        if safeguards[dimension]["protected_capability_anchor_ids"] != expected:
            errors.append(f"exit anchors changed: {dimension}")
        if not safeguards[dimension]["all_anchors_are_current_owners"]:
            errors.append(f"exit anchor is not a current owner: {dimension}")
    integrity_fields = ("unresolved_explicit_dependency_edges", "unknown_location_ids")
    if any(data["audit"][field] for field in integrity_fields):
        errors.append("audit retains an integrity error")
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
