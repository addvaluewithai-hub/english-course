"""Validate the cross-level exit-profile proposal and its source references."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/curriculum/level-exit-profiles.schema.json"
DEFAULT_DATA = ROOT / "data/reviewed/level-exit-profiles-v0.json"
EXPECTED_LEVELS = ["a1", "a2", "b1", "b2", "c1", "c2"]
EXPECTED_GSE = {
    "a1": "22-29",
    "a2": "30-42",
    "b1": "43-58",
    "b2": "59-75",
    "c1": "76-84",
    "c2": "85-90",
}


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path = DEFAULT_DATA) -> list[str]:
    schema = _load(SCHEMA)
    Draft202012Validator.check_schema(schema)
    data = _load(path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in sorted(validator.iter_errors(data), key=lambda item: list(item.path))
    ]
    if errors:
        return errors

    levels = [item["level"] for item in data["levels"]]
    if levels != EXPECTED_LEVELS:
        errors.append(f"levels must be ordered {EXPECTED_LEVELS}, got {levels}")
    if data["exit_levels"] != EXPECTED_LEVELS:
        errors.append("exit_levels must match the ordered level profiles")
    for profile in data["levels"]:
        if profile["gse_range"] != EXPECTED_GSE[profile["level"]]:
            errors.append(f"{profile['level']}: unexpected GSE range")

    source_ids = [item["source_id"] for item in data["source_catalog"]]
    if len(source_ids) != len(set(source_ids)):
        errors.append("source_catalog contains duplicate source ids")
    known = set(source_ids)
    for source in data["source_catalog"]:
        if not (ROOT / source["raw_file"]).is_file():
            errors.append(f"missing source file: {source['raw_file']}")
    for profile in data["levels"]:
        unknown = sorted(set(profile["source_refs"]) - known)
        if unknown:
            errors.append(f"{profile['level']}: unknown source refs {unknown}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT_DATA)
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
