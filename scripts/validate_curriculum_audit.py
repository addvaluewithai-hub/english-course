"""Validate the CUR-006 audit schema and deterministic evidence result."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

try:
    from scripts.curriculum_audit import build_curriculum_audit
except ModuleNotFoundError:
    from curriculum_audit import build_curriculum_audit


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "schemas/curriculum/curriculum-audit.schema.json"
SOURCE_PATHS = (
    PROJECT_ROOT / "data/reviewed/gse-a1-objectives.json",
    PROJECT_ROOT / "data/reviewed/cefr-a1-descriptors.json",
)
MAP_PATH = PROJECT_ROOT / "data/reviewed/a1-candidate-unit-map.json"
DEFAULT_PATH = PROJECT_ROOT / "data/reviewed/a1-curriculum-audit.json"


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validation_errors(path: Path) -> list[str]:
    schema = load(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    audit = load(path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(audit), key=lambda item: list(item.path))
    ]
    if errors:
        return errors

    expected = build_curriculum_audit(
        [load(source_path) for source_path in SOURCE_PATHS],
        load(MAP_PATH),
        audit["reviewed_at"],
    )
    if audit != expected:
        errors.append("audit does not match deterministic regeneration")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args()
    errors = validation_errors(args.path)
    if errors:
        print(f"FAIL {args.path}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
