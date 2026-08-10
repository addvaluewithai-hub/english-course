"""Validate all 81 first-pass A1 outcome reviews and their spine links."""

import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_outcome_review_contract import INPUTS, OUTPUT, PROFILES, ROOT, SCHEMA
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _known_claims() -> set[str]:
    profile = next(row for row in _load(PROFILES)["levels"] if row["level"] == "a1")
    claims = {profile["exit_promise"]["claim_id"]}
    for section in ("reception", "production", "interaction", "language_control"):
        claims.update(row["claim_id"] for row in profile[section].values())
    return claims


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    if [row["path"] for row in data["inputs"]] != [item.relative_to(ROOT).as_posix() for item in INPUTS]:
        errors.append("outcome-review input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    worklist = _load(WORKLIST)["candidates"]
    expected_ids = [row["candidate_id"] for row in worklist]
    rows = data["reviews"]
    if [row["candidate_id"] for row in rows] != expected_ids:
        errors.append("outcome-review coverage or order changed")
    known_claims = _known_claims()
    for source, review in zip(worklist, rows):
        if review["original_sequence_position"] != source["original_sequence_position"]:
            errors.append(f"{review['candidate_id']}: original sequence changed")
        if source["evidence"]["level_fit"]["status"] != "a1_only_evidence" or not review["a1_source_fit_confirmed"]:
            errors.append(f"{review['candidate_id']}: A1 source fit is not confirmed")
        unknown = set(review["profile_claim_ids"]) - known_claims
        if unknown:
            errors.append(f"{review['candidate_id']}: unknown profile claims {sorted(unknown)}")
    expected_counts = {
        "fit_status_counts": Counter(row["a1_fit_status"] for row in rows),
        "independence_signal_counts": Counter(row["independence_signal"] for row in rows),
        "risk_code_counts": Counter(code for row in rows for code in row["risk_codes"]),
    }
    for field, counts in expected_counts.items():
        if data["audit"][field] != dict(sorted(counts.items())):
            errors.append(f"{field}: audit counts changed")
    integrity = ("missing_candidate_ids", "unknown_candidate_ids", "unknown_profile_claim_ids")
    if any(data["audit"][field] for field in integrity):
        errors.append("outcome review retains a coverage or profile error")
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
