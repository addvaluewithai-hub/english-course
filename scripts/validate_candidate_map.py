"""Validate the candidate unit map against its reviewed source collections."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "schemas/curriculum/candidate-unit-map.schema.json"
SOURCE_PATHS = (
    PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json",
    PROJECT_ROOT / "data/reviewed/cefr-a1-descriptors.json",
)


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def semantic_errors(candidate_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    collections = [load(path) for path in SOURCE_PATHS]
    records = {
        record["record_id"]: (collection["dataset_id"], record)
        for collection in collections
        for record in collection["records"]
    }
    assignments = candidate_map["assignments"]
    assignment_ids = [item["record_id"] for item in assignments]
    if len(assignment_ids) != len(set(assignment_ids)):
        errors.append("assignments contain duplicate record ids")
    if set(assignment_ids) != set(records):
        errors.append("assignments do not exactly cover reviewed source records")

    for item in assignments:
        record_id = item["record_id"]
        if record_id not in records:
            continue
        dataset_id, record = records[record_id]
        source = record["source"]
        expected = {
            "dataset_id": dataset_id,
            "source_id": source["source_id"],
            "raw_file": source["raw_file"],
            "location": source["location"],
            "source_text_sha256": source["source_text_sha256"],
            "candidate_cluster_ids": record["interpretation"]["candidate_cluster_ids"],
        }
        for field, value in expected.items():
            if item[field] != value:
                errors.append(f"{record_id}: {field} does not match source collection")
        included = record["interpretation"]["inclusion_status"] == "included"
        if included and not item["candidate_cluster_ids"]:
            errors.append(f"{record_id}: included record is unmapped")
        if not included and item["candidate_cluster_ids"]:
            errors.append(f"{record_id}: excluded record has a cluster")

    assignment_by_id = {item["record_id"]: item for item in assignments}
    for cluster in candidate_map["clusters"]:
        cluster_id = cluster["cluster_id"]
        expected_ids = [
            item["record_id"] for item in assignments
            if cluster_id in item["candidate_cluster_ids"]
        ]
        if cluster["record_ids"] != expected_ids:
            errors.append(f"{cluster_id}: record_ids do not match assignments")
        kinds = Counter(assignment_by_id[value]["record_kind"] for value in expected_ids)
        if cluster["assignment_count"] != len(expected_ids):
            errors.append(f"{cluster_id}: assignment count is inconsistent")
        if cluster["objective_count"] != kinds["objective"]:
            errors.append(f"{cluster_id}: objective count is inconsistent")
        if cluster["descriptor_count"] != kinds["descriptor"]:
            errors.append(f"{cluster_id}: descriptor count is inconsistent")

    coverage = candidate_map["coverage"]
    fits = Counter(item["mapping_fit"] for item in assignments)
    if coverage["record_count"] != len(assignments):
        errors.append("coverage record count is inconsistent")
    if coverage["mapping_fit_counts"] != dict(sorted(fits.items())):
        errors.append("coverage mapping-fit counts are inconsistent")
    if coverage["included_count"] + coverage["excluded_count"] != len(assignments):
        errors.append("coverage included/excluded counts are inconsistent")
    return errors


def validate(path: Path) -> list[str]:
    schema = load(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    candidate_map = load(path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(candidate_map), key=lambda item: list(item.path))
    ]
    return errors or semantic_errors(candidate_map)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path", nargs="?", type=Path,
        default=PROJECT_ROOT / "data/reviewed/a1-candidate-unit-map.json",
    )
    args = parser.parse_args()
    errors = validate(args.path)
    if errors:
        print(f"FAIL {args.path}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
