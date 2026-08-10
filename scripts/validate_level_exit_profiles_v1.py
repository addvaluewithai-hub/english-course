"""Validate approved level-exit claims and evidence references."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

from scripts.level_exit_profile_contract import (
    CLAIM_SCHEMA, EVIDENCE, EXPECTED_GSE, LEVELS, OUTPUT, SCHEMA,
)
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _validator() -> Draft202012Validator:
    schemas = [_load(CLAIM_SCHEMA), _load(SCHEMA)]
    for schema in schemas:
        Draft202012Validator.check_schema(schema)
    registry = Registry().with_resources(
        (schema["$id"], Resource.from_contents(schema)) for schema in schemas
    )
    return Draft202012Validator(schemas[-1], registry=registry, format_checker=FormatChecker())


def _claims(profile: dict) -> list[dict]:
    result = [profile["exit_promise"]]
    for section in ("reception", "production", "interaction", "language_control"):
        result.extend(profile[section].values())
    result.extend(profile["assessment_evidence"])
    return result


def validate(path: Path = OUTPUT) -> list[str]:
    data = _load(path)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in sorted(_validator().iter_errors(data), key=lambda item: list(item.path))
    ]
    if errors:
        return errors
    evidence = _load(EVIDENCE)
    if file_sha256(EVIDENCE) != data["evidence_bundles"]["sha256"]:
        errors.append("evidence bundle hash mismatch")
    known = {bundle["bundle_id"] for bundle in evidence["bundles"]}
    levels = [profile["level"] for profile in data["levels"]]
    if levels != list(LEVELS) or data["exit_levels"] != list(LEVELS):
        errors.append("level order or exit level contract changed")
    claim_ids: list[str] = []
    for index, profile in enumerate(data["levels"], 1):
        level = profile["level"]
        if profile["progression_index"] != index:
            errors.append(f"{level}: progression index must be {index}")
        if profile["gse_range"] != EXPECTED_GSE[level]:
            errors.append(f"{level}: GSE range changed")
        for claim in _claims(profile):
            claim_ids.append(claim["claim_id"])
            unknown = set(claim["evidence_bundle_ids"]) - known
            if unknown:
                errors.append(f"{claim['claim_id']}: unknown evidence bundles {sorted(unknown)}")
            if claim["claim_type"] == "source_boundary" and not claim["evidence_bundle_ids"]:
                errors.append(f"{claim['claim_id']}: source boundary has no evidence")
    if len(claim_ids) != 102 or len(claim_ids) != len(set(claim_ids)):
        errors.append("expected 102 unique reviewed claims")
    profile_text = json.dumps(data["levels"], ensure_ascii=False).casefold()
    if "native speaker" in profile_text or "accent removal" in profile_text:
        errors.append("exit profiles must not use native-speaker imitation as the target")
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
