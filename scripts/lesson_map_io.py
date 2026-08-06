"""Loading and schema-registry helpers for A1 lesson-map validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = PROJECT_ROOT / "schemas/curriculum"
MAP_SCHEMA_PATH = SCHEMA_DIR / "lesson-map.schema.json"
DEPENDENCY_SCHEMA_PATHS = (
    SCHEMA_DIR / "source-record.schema.json",
    SCHEMA_DIR / "lesson-candidate.schema.json",
)
SOURCE_PATHS = (
    PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json",
    PROJECT_ROOT / "data/reviewed/cefr-a1-descriptors.json",
)
DEFAULT_MAP_PATH = PROJECT_ROOT / "data/reviewed/a1-lesson-map.json"


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def schema_validator() -> Draft202012Validator:
    schema = load(MAP_SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    registry = Registry()
    for path in DEPENDENCY_SCHEMA_PATHS:
        dependency = load(path)
        registry = registry.with_resource(
            dependency["$id"], Resource.from_contents(dependency)
        )
    return Draft202012Validator(
        schema, registry=registry, format_checker=FormatChecker()
    )


def source_index(
    collections: Iterable[dict[str, Any]],
) -> tuple[dict[str, tuple[str, dict[str, Any]]], list[str]]:
    index: dict[str, tuple[str, dict[str, Any]]] = {}
    errors: list[str] = []
    for collection in collections:
        dataset_id = collection["dataset_id"]
        for record in collection["records"]:
            record_id = record["record_id"]
            if record_id in index:
                errors.append(f"source collections repeat record id {record_id}")
            index[record_id] = (dataset_id, record)
    return index, errors


def schema_errors(lesson_map: dict[str, Any]) -> list[str]:
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(
            schema_validator().iter_errors(lesson_map), key=lambda item: list(item.path)
        )
    ]
