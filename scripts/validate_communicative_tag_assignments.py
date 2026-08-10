"""Validate all-level communicative tags and their source coverage."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.communicative_tag_contract import OUTPUT, ROOT, SCHEMA
from scripts.progression_tag_model import FUNCTION_CODES, MODE_CODES, SKILL_CODES
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
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
    expected = {}
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
            continue
        if item["path"].startswith("data/derived/"):
            source_data = _load(source)
            expected[source_data["dataset_id"]] = {
                str(row["record_id"]) for row in source_data["records"]
            }
    actual: dict[str, list[str]] = {}
    unknown = set()
    for row in data["records"]:
        actual.setdefault(row["source_dataset_id"], []).append(row["source_record_id"])
        unknown |= set(row["skill_codes"]) - SKILL_CODES
        unknown |= set(row["mode_codes"]) - MODE_CODES
        unknown |= set(row["function_codes"]) - FUNCTION_CODES
    for dataset_id, ids in expected.items():
        assigned = actual.get(dataset_id, [])
        duplicates = [key for key, count in Counter(assigned).items() if count > 1]
        if duplicates or set(assigned) != ids:
            errors.append(f"{dataset_id}: incomplete or duplicate tag assignment")
    if unknown:
        errors.append(f"unknown taxonomy codes: {sorted(unknown)}")
    if set(actual) != set(expected):
        errors.append("tagged datasets do not match expected source datasets")
    if any(data["audit"][field] for field in ("untagged_records", "unknown_codes", "missing_dispositions")):
        errors.append("accepted audit retains an integrity finding")
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
