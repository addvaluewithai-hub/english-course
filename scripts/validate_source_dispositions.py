"""Validate reviewed source dispositions and their normalized inputs."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from scripts.source_disposition_contract import OUTPUT, ROOT, SCHEMA
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]
    if errors:
        return errors
    expected: dict[str, set[str]] = {}
    for source in data["source_datasets"]:
        source_path = ROOT / source["path"]
        if not source_path.is_file():
            errors.append(f"missing source dataset: {source['path']}")
            continue
        source_data = _load(source_path)
        source_ids = {
            str(row.get("record_id", row.get("id"))) for row in source_data["records"]
        }
        expected[source["dataset_id"]] = source_ids
        if len(source_ids) != source["record_count"]:
            errors.append(f"{source['dataset_id']}: record count or ids do not reconcile")
        if file_sha256(source_path) != source["sha256"]:
            errors.append(f"{source['dataset_id']}: source dataset hash mismatch")
    actual: dict[str, list[str]] = {}
    for row in data["records"]:
        actual.setdefault(row["source_dataset_id"], []).append(row["source_record_id"])
    for dataset_id, expected_ids in expected.items():
        actual_ids = actual.get(dataset_id, [])
        duplicates = [key for key, count in Counter(actual_ids).items() if count > 1]
        missing = expected_ids - set(actual_ids)
        extra = set(actual_ids) - expected_ids
        if duplicates or missing or extra:
            errors.append(
                f"{dataset_id}: duplicates={len(duplicates)}, missing={len(missing)}, extra={len(extra)}"
            )
    if set(actual) != set(expected):
        errors.append("disposition source datasets do not match the declared source set")
    if data["audit"]["total_records"] != len(data["records"]):
        errors.append("audit total_records does not match records")
    if data["audit"]["unclassified_records"] or data["audit"]["unexplained_orphans"]:
        errors.append("accepted audit cannot retain unclassified records or unexplained orphans")
    known_policies = {row["policy_id"] for row in data["policy_catalog"]}
    if any(row["policy_id"] not in known_policies for row in data["records"]):
        errors.append("record references an unknown policy")
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
