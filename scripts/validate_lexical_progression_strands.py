"""Validate lexical source coverage, progression, and selection gates."""

import hashlib
import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.lexical_progression_contract import (
    FUNCTIONS, LEVELS, OUTPUT, REQUIRED_ITEM_FIELDS, ROOT, SCHEMA,
)
from scripts.lexical_resource_catalog import RESOURCE_STRANDS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def _validate_pool(data: dict, errors: list[str]) -> None:
    all_ids = []
    for summary in data["reference_pool"]["datasets"]:
        source = _load(ROOT / summary["path"])
        rows = source["records"]
        ids = [row["record_id"] for row in rows]
        all_ids.extend(ids)
        counts = Counter(row["interpretation"]["cefr_codes"][0] for row in rows)
        labels = {
            row["source_facts"]["other_verbatim"]["headword_source"].casefold()
            for row in rows
        }
        if summary["entry_line_count"] != len(rows):
            errors.append(f"{summary['dataset_id']}: entry-line count changed")
        if summary["distinct_printed_headword_labels"] != len(labels):
            errors.append(f"{summary['dataset_id']}: headword-label count changed")
        if summary["level_counts"] != {level: counts[level] for level in LEVELS if counts[level]}:
            errors.append(f"{summary['dataset_id']}: level counts changed")
        if summary["record_ids_sha256"] != _hash(ids):
            errors.append(f"{summary['dataset_id']}: record-id inventory changed")
    if data["reference_pool"]["all_source_record_ids_sha256"] != _hash(all_ids):
        errors.append("combined Oxford record-id inventory changed")


def _validate_strands(data: dict, errors: list[str]) -> None:
    if {row["strand_code"] for row in data["resource_strands"]} != set(RESOURCE_STRANDS):
        errors.append("lexical resource catalog changed")
    for strand in data["resource_strands"]:
        code = strand["strand_code"]
        stages = strand["stages"]
        if [stage["level"] for stage in stages] != list(LEVELS):
            errors.append(f"{code}: level order changed")
            continue
        if len({stage["expectation"] for stage in stages}) != len(LEVELS):
            errors.append(f"{code}: stage expectations do not progress")
        control = LEVELS.index(strand["first_guided_productive_level"])
        consolidation = LEVELS.index(strand["first_family_consolidation_level"])
        if control > consolidation:
            errors.append(f"{code}: consolidation precedes guided control")
        for index, stage in enumerate(stages):
            states = set(stage["lifecycle_states"])
            if index < control and states != {"expose"}:
                errors.append(f"{code}/{stage['level']}: premature productive state")
            if index == control and not {"introduce", "practise"}.issubset(states):
                errors.append(f"{code}/{stage['level']}: first guided control is incomplete")
            if index == consolidation and "consolidate" not in states:
                errors.append(f"{code}/{stage['level']}: consolidation state missing")
            if index > consolidation and not {"recycle", "extend"}.issubset(states):
                errors.append(f"{code}/{stage['level']}: post-consolidation extension missing")


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
    _validate_pool(data, errors)
    _validate_strands(data, errors)
    functions = _load(FUNCTIONS)
    selection = data["selection_contract"]
    if selection["communicative_owner_count"] != len(functions["strands"]):
        errors.append("communicative owner count changed")
    if tuple(selection["required_item_fields"]) != REQUIRED_ITEM_FIELDS:
        errors.append("required lexical item contract changed")
    empty_audits = (
        "unaccounted_source_records", "missing_stage_boundaries",
        "invalid_lifecycle_order", "missing_selection_fields",
    )
    if any(data["audit"][field] for field in empty_audits):
        errors.append("accepted lexical audit retains an integrity finding")
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
