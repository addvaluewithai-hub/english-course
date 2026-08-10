"""Validate communicative lifecycle strands and source-assignment coverage."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.communicative_function_catalog import INTENTS
from scripts.communicative_strand_contract import EXIT_LEVELS, LEVELS, LIFECYCLE, OUTPUT, ROOT, SCHEMA, TAGS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _assignment_id(row: dict) -> str:
    return f"{row['source_dataset_id']}:{row['source_record_id']}"


def _hash_ids(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


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
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    tags = _load(TAGS)
    groups = {function: [] for function in INTENTS}
    for row in tags["records"]:
        for function in row["function_codes"]:
            groups[function].append(row)
    functions = [strand["function_code"] for strand in data["strands"]]
    if len(functions) != len(set(functions)) or set(functions) != set(INTENTS):
        errors.append("function strands do not match the controlled catalog")
    for strand in data["strands"]:
        function = strand["function_code"]
        ids = sorted(_assignment_id(row) for row in groups[function])
        if strand["evidence"]["assignment_count"] != len(ids):
            errors.append(f"{function}: evidence count changed")
        if strand["evidence"]["assignment_ids_sha256"] != _hash_ids(ids):
            errors.append(f"{function}: evidence ids changed")
        lifecycle = strand["lifecycle"]
        consolidation = lifecycle["consolidation_level"]
        expected_recycle = list(EXIT_LEVELS[EXIT_LEVELS.index(consolidation) + 1 :])
        if lifecycle["recycle_levels"] != expected_recycle:
            errors.append(f"{function}: post-consolidation recycling is incomplete")
        if not set(lifecycle["extension_levels"]).issubset(expected_recycle):
            errors.append(f"{function}: extension precedes consolidation")
        stage_levels = [stage["level"] for stage in lifecycle["stages"]]
        if stage_levels != sorted(stage_levels, key=LEVELS.index):
            errors.append(f"{function}: stage levels regress")
        consolidated = False
        for stage in lifecycle["stages"]:
            states = stage["lifecycle_states"]
            if states != sorted(states, key=LIFECYCLE.index):
                errors.append(f"{function}/{stage['level']}: lifecycle states are out of order")
            if stage["level"] == consolidation and "consolidate" in states:
                consolidated = True
            expected_status = "source_evidenced" if stage["evidence_count"] else "planned_recycle"
            if stage["evidence_status"] != expected_status:
                errors.append(f"{function}/{stage['level']}: evidence status mismatch")
        if not consolidated:
            errors.append(f"{function}: consolidation stage is missing")
    if any(data["audit"][key] for key in (
        "uncovered_assignments", "missing_consolidation", "invalid_level_regressions",
        "missing_post_consolidation_recycle",
    )):
        errors.append("accepted strand audit retains an integrity finding")
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
