"""Apply the consolidated final approval audit to the complete A1 lesson map."""

from __future__ import annotations

import copy
from typing import Any

try:
    from scripts.lesson_language_target_model import build_reviewed_map
except ModuleNotFoundError:
    from lesson_language_target_model import build_reviewed_map


REVIEWED_AT = "2026-07-19T01:13:48+03:00"
REVIEWER = "lesson_002_consolidated_approval"
RISK_RESOLUTIONS = {
    "The unclaimed imaginary-person clause needs reconciliation in the people partition.":
        "Resolved: fictional-person practice is covered as a permitted variant without a separate mastery claim.",
    "Later map review must decide whether request and reply need separate variants, not separate lessons.":
        "Resolved: request and reply remain matched variants within one bounded written exchange.",
    "A later lexical review must define which common jobs form the A1 practice range.":
        "Resolved: the target range is limited to familiar jobs supported by the candidate evidence.",
    "Later vocabulary review must define the small common-weather range.":
        "Resolved: the target range is limited to one or two common weather conditions.",
    "Objects and features need later vocabulary review before lesson approval.":
        "Resolved: object language is limited to familiar names, shape, colour, and size.",
}


def build_approved_map() -> dict[str, Any]:
    lesson_map = copy.deepcopy(build_reviewed_map())
    errors = approval_errors(lesson_map)
    if errors:
        raise ValueError("consolidated approval failed:\n- " + "\n- ".join(errors))
    for candidate in lesson_map["candidates"]:
        candidate["version"] += 1
        candidate["status"] = "approved_candidate"
        candidate["risks"] = [RISK_RESOLUTIONS.get(item, item) for item in candidate["risks"]]
        candidate["review"] = {
            "status": "accepted",
            "reviewer": REVIEWER,
            "reviewed_at": REVIEWED_AT,
            "issues": [],
        }
    lesson_map["version"] += 1
    lesson_map["status"] = "approved"
    lesson_map["review"] = {
        "status": "accepted",
        "reviewer": REVIEWER,
        "reviewed_at": REVIEWED_AT,
        "issues": [],
    }
    return lesson_map


def approval_errors(lesson_map: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for candidate in lesson_map["candidates"]:
        candidate_id = candidate["candidate_id"]
        tests = candidate["normalization"]["coherence_tests"]
        if not all(tests.values()):
            errors.append(f"{candidate_id}: a coherence test is not passed")
        if candidate["scope"]["band"] == "complex" and not candidate["scope"]["no_split_rationale"]:
            errors.append(f"{candidate_id}: complex scope lacks a no-split rationale")
        evidence_ids = {item["record_id"] for item in candidate["evidence_refs"]}
        targets = [
            target for family in candidate["language_targets"].values() for target in family
        ]
        if not targets:
            errors.append(f"{candidate_id}: has no explicit language-target decision")
        for target in targets:
            cited = {item["record_id"] for item in target["evidence_refs"]}
            if not cited or not cited <= evidence_ids:
                errors.append(f"{candidate_id}: a target cites evidence outside the candidate")
        hypotheses = candidate["error_hypotheses"]
        if len(hypotheses) != 1 or hypotheses[0]["validation_status"] not in {
            "hypothesis", "expert_reviewed", "learner_observed"
        }:
            errors.append(f"{candidate_id}: lacks one explicit labelled error decision")
        mastery = candidate["mastery"]
        if set(mastery["required_dimensions"]) != set(mastery["level_2_evidence"]):
            errors.append(f"{candidate_id}: mastery dimensions and evidence do not align")
        if candidate["review"]["status"] != "needs_review":
            errors.append(f"{candidate_id}: was not ready for consolidated approval")
    return errors
