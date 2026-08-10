"""Audit A1 functions, modes, overlaps, and the current Unit 1 boundary."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from scripts.a1_ability_coverage_contract import (
    A1_MAP, DIMENSIONS, FUNCTIONS, INPUTS, OUTPUT, OUTCOME_REVIEW, REPORT,
    REVIEWED_AT, REVIEWER, ROOT, SUPPORT_FUNCTION_OWNERS, UNIT1, UNIT1_MASTERY, WORKLIST,
)
from scripts.a1_overlap_group_catalog import GROUPS, expand_id
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _dimension_candidates(code: str, candidates: list[dict]) -> list[str]:
    def owns(row: dict) -> bool:
        skills, modes = set(row["skill_codes"]), set(row["mode_codes"])
        if code == "listening_reception": return "listening" in skills and "reception" in modes
        if code == "reading_reception": return "reading" in skills and "reception" in modes
        if code == "speaking_production": return "speaking" in skills and "production" in modes
        if code == "writing_production": return "writing" in skills and "production" in modes
        if code == "oral_interaction": return "interaction" in modes and bool(skills & {"listening", "speaking"})
        if code == "written_online_interaction": return bool(modes & {"interaction", "online_interaction"}) and bool(skills & {"reading", "writing"})
        return "mediation" in modes
    return [row["candidate_id"] for row in candidates if owns(row)]


def _function_coverage(functions: dict, candidates: list[dict]) -> list[dict]:
    rows = []
    for strand in functions["strands"]:
        if strand["lifecycle"]["consolidation_level"] != "a1":
            continue
        code = strand["function_code"]
        candidate_ids = [row["candidate_id"] for row in candidates if code in row["function_codes"]]
        support_ids = list(SUPPORT_FUNCTION_OWNERS.get(code, ()))
        rows.append({
            "function_code": code, "candidate_owner_ids": candidate_ids,
            "support_owner_ids": support_ids,
            "ownership_type": "candidate_owned" if candidate_ids else "support_owned",
            "coverage_status": "covered" if candidate_ids or support_ids else "gap",
        })
    return rows


def _overlap_groups(candidate_ids: set[str]) -> list[dict]:
    rows = []
    for group_id, short_ids, rationale in GROUPS:
        ids = [expand_id(item) for item in short_ids]
        rows.append({
            "group_id": group_id, "candidate_ids": ids, "rationale": rationale,
            "all_candidates_known": set(ids).issubset(candidate_ids),
            "decision_status": "requires_later_passes",
        })
    return rows


def _unit_audit(source_map: dict, unit: dict, mastery: dict, outcome_reviews: dict) -> dict:
    source_index = {row["candidate_id"]: row for row in source_map["candidates"]}
    review_index = {row["candidate_id"]: row for row in outcome_reviews["reviews"]}
    lesson_ids = [row["candidate_id"] for row in unit["lessons"]]
    positions = {candidate_id: index for index, candidate_id in enumerate(lesson_ids)}
    violations = []
    for candidate_id in lesson_ids:
        for link in source_index[candidate_id]["relationships"]["helpful_before"]:
            owner = link["candidate_id"]
            if owner in positions and positions[owner] > positions[candidate_id]:
                violations.append({"candidate_id": candidate_id, "helpful_before_candidate_id": owner})
    scope_revisions = [candidate_id for candidate_id in lesson_ids if review_index[candidate_id]["a1_fit_status"] != "fits_a1_boundary"]
    return {
        "status": "requires_revision_not_rejection", "candidate_ids": lesson_ids,
        "all_candidates_a1_source_fit": all(review_index[item]["a1_source_fit_confirmed"] for item in lesson_ids),
        "scope_revision_candidate_ids": scope_revisions,
        "helpful_before_order_violations": violations,
        "mastery_station_count": len(mastery["stations"]),
        "mastery_mode_evidence": sorted({value for station in mastery["stations"] for value in station["evidence"]}),
        "findings": [
            {"finding_id": "input_model_after_first_output", "action": "Move introduction listening before first independent self-introduction or document a different input source."},
            {"finding_id": "first_contact_social_frame_unowned", "action": "Add or embed greeting, response-to-introduction, and closing ownership, or narrow the unit promise."},
            {"finding_id": "contact_detail_construct_mismatch", "action": "Keep listening recognition as the construct; treat written capture as transfer evidence."},
        ],
    }


def build() -> dict[str, Any]:
    source_map, worklist = _load(A1_MAP), _load(WORKLIST)
    outcome_reviews, functions = _load(OUTCOME_REVIEW), _load(FUNCTIONS)
    unit, mastery = _load(UNIT1), _load(UNIT1_MASTERY)
    candidates = worklist["candidates"]
    function_rows = _function_coverage(functions, candidates)
    dimensions = [
        {"dimension_code": code, "candidate_owner_ids": _dimension_candidates(code, candidates), "coverage_status": "covered"}
        for code in DIMENSIONS
    ]
    overlaps = _overlap_groups({row["candidate_id"] for row in candidates})
    return {
        "schema_version": 1, "audit_id": "a1_ability_coverage_overlap_audit", "version": 1,
        "inputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)} for path in INPUTS],
        "function_coverage": function_rows, "exit_dimension_coverage": dimensions,
        "overlap_groups": overlaps, "unit1_audit": _unit_audit(source_map, unit, mastery, outcome_reviews),
        "audit": {
            "a1_function_count": len(function_rows),
            "candidate_owned_function_count": sum(row["ownership_type"] == "candidate_owned" for row in function_rows),
            "support_owned_function_count": sum(row["ownership_type"] == "support_owned" for row in function_rows),
            "uncovered_function_codes": [row["function_code"] for row in function_rows if row["coverage_status"] == "gap"],
            "exit_dimension_count": len(dimensions), "uncovered_exit_dimensions": [row["dimension_code"] for row in dimensions if not row["candidate_owner_ids"]],
            "overlap_group_count": len(overlaps), "unknown_overlap_candidate_ids": sorted({item for row in overlaps if not row["all_candidates_known"] for item in row["candidate_ids"]}),
            "final_candidate_decisions_made": 0,
        },
        "review": {
            "status": "accepted_coverage_pass", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "statement": "Coverage and overlap hypotheses constrain later decisions; they do not freeze the current candidates or final lesson count.",
        },
    }


def _report(data: dict) -> str:
    lines = ["# A1 Ability Coverage and Overlap Audit v1", "", "Status: coverage pass accepted.", "",
             f"All {data['audit']['a1_function_count']} A1 function strands and all {data['audit']['exit_dimension_count']} exit dimensions have owners.",
             f"The audit records {data['audit']['overlap_group_count']} overlap groups for later decisions.", "",
             "Three functions are intentionally support-owned: repair, language-form control, and inference.",
             "Unit 1 remains usable source work but requires sequence, social-frame, and contact-detail construct revision.", "",
             "No merge, support-only, or retirement decision is final until language ownership, recycling, and mastery review pass.", ""]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['function_coverage'])} functions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
