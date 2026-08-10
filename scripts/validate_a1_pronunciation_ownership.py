"""Validate exact A1 pronunciation targets, risks, and provisional owners."""

import json

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_pronunciation_ownership_contract import (
    CONTROL_STATUSES, INPUTS, OUTPUT, PROGRESSION, RISK_DISPOSITIONS, ROOT, SCHEMA,
    SUPPORT_OWNER_IDS, WORKLIST,
)
from scripts.a1_pronunciation_target_catalog import TARGETS
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path=OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    expected_paths = [item.relative_to(ROOT).as_posix() for item in INPUTS]
    if [row["path"] for row in data["inputs"]] != expected_paths:
        errors.append("pronunciation ownership input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    progression, worklist = _load(PROGRESSION), _load(WORKLIST)
    strand_ids = {row["strand_id"] for row in progression["strands"]}
    risk_ids = {row["risk_id"] for row in progression["arabic_learner_risk_hypotheses"]}
    source_refs = {
        ref for strand in progression["strands"]
        for stage in strand["stages"] if stage["level"] == "a1"
        for ref in stage["representative_cefr_evidence_ids"]
    }
    candidate_ids = {row["candidate_id"] for row in worklist["candidates"]}
    target_ids = [row["target_id"] for row in data["targets"]]
    expected_target_ids = [row["target_id"] for row in TARGETS]
    if target_ids != expected_target_ids or len(target_ids) != len(set(target_ids)):
        errors.append("pronunciation target catalog or order changed")
    known_targets = set(target_ids)
    for row in data["targets"]:
        if row["control_status"] not in CONTROL_STATUSES or row["strand_id"] not in strand_ids:
            errors.append(f"{row['target_id']}: uncontrolled status or strand")
        if not set(row["source_refs"]).issubset(source_refs):
            errors.append(f"{row['target_id']}: unknown CEFR source reference")
        if set(row["arabic_risk_hypothesis_ids"]) - risk_ids:
            errors.append(f"{row['target_id']}: unknown Arabic-risk hypothesis")
        locations = {row["introduction_location"], *row["recycle_locations"]}
        unknown = locations - candidate_ids - SUPPORT_OWNER_IDS
        if unknown:
            errors.append(f"{row['target_id']}: unknown owner locations {sorted(unknown)}")
        if row["introduction_location"] in row["recycle_locations"]:
            errors.append(f"{row['target_id']}: introduction reused as recycle")
    actual_risks = {row["risk_id"]: row for row in data["risk_dispositions"]}
    if set(actual_risks) != risk_ids:
        errors.append("Arabic-risk disposition inventory changed")
    for risk_id, row in actual_risks.items():
        if row["disposition"] not in RISK_DISPOSITIONS or set(row["selected_target_ids"]) - known_targets:
            errors.append(f"{risk_id}: uncontrolled disposition or target")
        selected = row["disposition"] == "selected_monitor_target"
        if selected != bool(row["selected_target_ids"]):
            errors.append(f"{risk_id}: disposition/target mismatch")
    expected_candidates = {
        row["candidate_id"] for row in worklist["candidates"]
        if row["current_language_targets"]["pronunciation"]
    }
    candidate_rows = {row["candidate_id"]: row for row in data["candidate_ownership"]}
    if set(candidate_rows) != expected_candidates:
        errors.append("legacy pronunciation candidate inventory changed")
    for candidate_id, row in candidate_rows.items():
        if not row["exact_target_ids"] or set(row["exact_target_ids"]) - known_targets:
            errors.append(f"{candidate_id}: missing or unknown exact target")
    integrity = (
        "uncovered_pronunciation_candidate_ids", "uncovered_strand_ids", "unknown_strand_ids",
        "unknown_risk_ids", "unknown_candidate_location_ids", "targets_without_source_refs",
        "targets_without_recycle_locations", "examples_without_reference_ipa",
    )
    if any(data["audit"][field] for field in integrity):
        errors.append("pronunciation ownership audit retains an integrity error")
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
