"""Validate the A1 reconciliation inventory without implying final approval."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_reconciliation_contract import A1_MAP, INPUTS, OUTPUT, ROOT, SCHEMA, UNIT1
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
    if [row["path"] for row in data["inputs"]] != [path.relative_to(ROOT).as_posix() for path in INPUTS]:
        errors.append("reconciliation input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    source_map, unit = _load(A1_MAP), _load(UNIT1)
    source_index = {row["candidate_id"]: row for row in source_map["candidates"]}
    rows = data["candidates"]
    ids = [row["candidate_id"] for row in rows]
    if ids != [row["candidate_id"] for row in source_map["candidates"]]:
        errors.append("candidate order or inventory changed")
    if len(ids) != len(set(ids)):
        errors.append("candidate inventory contains duplicate ids")
    unit_index = {row["candidate_id"]: row for row in unit["lessons"]}
    for position, row in enumerate(rows, start=1):
        source = source_index[row["candidate_id"]]
        if row["original_sequence_position"] != position:
            errors.append(f"{row['candidate_id']}: sequence position changed")
        source_evidence = [item["record_id"] for item in source["evidence_refs"]]
        if row["evidence"]["record_ids"] != source_evidence:
            errors.append(f"{row['candidate_id']}: source evidence changed")
        if row["evidence"]["level_fit"]["status"] != "a1_only_evidence":
            errors.append(f"{row['candidate_id']}: source evidence is not wholly A1")
        expected_unit = unit_index.get(row["candidate_id"])
        if row["unit1_membership"]["included"] != (expected_unit is not None):
            errors.append(f"{row['candidate_id']}: Unit 1 membership changed")
        if row["reconciliation"] != {
            "review_status": "pending", "decision": None, "rationale": None,
            "related_candidate_ids": [], "unresolved_questions": [],
        }:
            errors.append(f"{row['candidate_id']}: worklist implies a decision before review")
    audit = data["audit"]
    if audit["unmatched_evidence_record_ids"] or audit["unknown_unit1_candidate_ids"]:
        errors.append("worklist retains an unmatched source or Unit 1 candidate")
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
