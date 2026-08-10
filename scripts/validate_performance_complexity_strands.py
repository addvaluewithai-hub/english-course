"""Validate performance-complexity stages and CEFR evidence links."""

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.performance_complexity_contract import DISPOSITIONS, LEVELS, OUTPUT, ROOT, SCHEMA, STRANDS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    dispositions = _load(DISPOSITIONS)["records"]
    if {row["strand_code"] for row in data["strands"]} != set(STRANDS):
        errors.append("performance strand catalog changed")
    for strand in data["strands"]:
        code = strand["strand_code"]
        if [stage["level"] for stage in strand["stages"]] != list(LEVELS):
            errors.append(f"{code}: level order changed")
        texts = [stage["expectation"] for stage in strand["stages"]]
        if len(texts) != len(set(texts)):
            errors.append(f"{code}: adjacent boundaries do not progress")
        for stage in strand["stages"]:
            ids = sorted(
                row["source_record_id"] for row in dispositions
                if row["source_dataset_id"] == "cefr_all_descriptors"
                and stage["level"] in row["source_level_codes"] and code in row["strand_codes"]
            )
            if len(ids) != stage["evidence_count"] or _hash(ids) != stage["evidence_ids_sha256"]:
                errors.append(f"{code}/{stage['level']}: evidence selection changed")
    integrity = ("empty_stages", "duplicate_stage_expectations", "invalid_level_order")
    if any(data["audit"][field] for field in integrity):
        errors.append("accepted performance audit retains an integrity finding")
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
