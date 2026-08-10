"""Validate grammar families, lifecycle order, and GSE Grammar crosswalk coverage."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.grammar_crosswalk_rules import RULES
from scripts.grammar_strand_contract import EGP, EXIT_LEVELS, GSE_GRAMMAR, LEVELS, LIFECYCLE, OUTPUT, ROOT, SCHEMA
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
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    egp = _load(EGP)["records"]
    grouped = {}
    for row in egp:
        grouped.setdefault((row["SuperCategory"], row["SubCategory"]), []).append(row)
    seen_features = set()
    for family in data["families"]:
        key = (family["supercategory"], family["subcategory"])
        features = grouped.get(key, [])
        ids = sorted(str(row["id"]) for row in features)
        seen_features.update(ids)
        if family["evidence"]["feature_count"] != len(ids) or family["evidence"]["feature_ids_sha256"] != _hash_ids(ids):
            errors.append(f"{family['family_id']}: feature evidence changed")
        life = family["lifecycle"]
        consolidation = life["consolidation_level"]
        expected_recycle = list(EXIT_LEVELS[EXIT_LEVELS.index(consolidation) + 1 :])
        if life["recycle_levels"] != expected_recycle:
            errors.append(f"{family['family_id']}: recycle levels are incomplete")
        stage_levels = [stage["level"] for stage in life["stages"]]
        if stage_levels != sorted(stage_levels, key=LEVELS.index):
            errors.append(f"{family['family_id']}: stage level regression")
        for stage in life["stages"]:
            states = stage["lifecycle_states"]
            if states != sorted(states, key=LIFECYCLE.index):
                errors.append(f"{family['family_id']}/{stage['level']}: lifecycle state regression")
    if seen_features != {str(row["id"]) for row in egp}:
        errors.append("EGP family coverage is incomplete")
    gse_ids = {row["record_id"] for row in _load(GSE_GRAMMAR)["records"]}
    cross_ids = [row["source_record_id"] for row in data["gse_crosswalk"]]
    if len(cross_ids) != len(set(cross_ids)) or set(cross_ids) != gse_ids:
        errors.append("GSE Grammar crosswalk coverage is incomplete or duplicated")
    known = set(RULES)
    if any(not set(row["supercategory_codes"]).issubset(known) for row in data["gse_crosswalk"]):
        errors.append("GSE Grammar crosswalk uses an unknown supercategory")
    integrity = (
        "unassigned_egp_features", "unassigned_gse_records", "missing_consolidation",
        "invalid_level_regressions", "missing_post_consolidation_recycle",
    )
    if any(data["audit"][field] for field in integrity):
        errors.append("accepted grammar audit retains an integrity finding")
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
