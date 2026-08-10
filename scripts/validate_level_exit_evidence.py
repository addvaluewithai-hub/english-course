"""Validate level-exit evidence bundles against reviewed dispositions."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.level_exit_evidence_contract import DISPOSITIONS, OUTPUT, SCHEMA
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
    if file_sha256(DISPOSITIONS) != data["source_dispositions"]["sha256"]:
        errors.append("source disposition hash mismatch")
    dispositions = _load(DISPOSITIONS)
    groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for row in dispositions["records"]:
        for level in row["source_level_codes"]:
            for strand in row["strand_codes"]:
                groups[(row["source_dataset_id"], level, strand)].append(row["source_record_id"])
    seen = set()
    for bundle in data["bundles"]:
        if bundle["bundle_id"] in seen:
            errors.append(f"duplicate bundle id: {bundle['bundle_id']}")
        seen.add(bundle["bundle_id"])
        selector = bundle["selector"]
        key = (
            selector["source_dataset_id"], selector["source_level_code"],
            selector["strand_code"],
        )
        ids = sorted(groups.get(key, []))
        if len(ids) != bundle["matched_record_count"]:
            errors.append(f"{bundle['bundle_id']}: matched count changed")
        if _hash_ids(ids) != bundle["matched_record_ids_sha256"]:
            errors.append(f"{bundle['bundle_id']}: matched ids changed")
        if not set(bundle["representative_record_ids"]).issubset(ids):
            errors.append(f"{bundle['bundle_id']}: representative id is outside selection")
    if data["audit"]["bundle_count"] != len(data["bundles"]):
        errors.append("audit bundle_count does not match bundles")
    if data["audit"]["empty_selectors"]:
        errors.append("accepted evidence cannot retain empty selectors")
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
