"""Apply one reviewed language-target and error-decision partition."""

from __future__ import annotations

import copy
from typing import Any

try:
    from scripts.lesson_social_collaboration_decisions import SOCIAL_COLLABORATION_DECISIONS
    from scripts.lesson_social_response_decisions import SOCIAL_RESPONSE_DECISIONS
    from scripts.lesson_message_direct_decisions import MESSAGE_DIRECT_DECISIONS
    from scripts.lesson_message_mediation_decisions import MESSAGE_MEDIATION_DECISIONS
    from scripts.lesson_familiar_home_spoken_decisions import FAMILIAR_HOME_SPOKEN_DECISIONS
    from scripts.lesson_familiar_remaining_output_decisions import FAMILIAR_REMAINING_OUTPUT_DECISIONS
    from scripts.lesson_familiar_written_decisions import FAMILIAR_WRITTEN_DECISIONS
    from scripts.lesson_wayfinding_decisions import WAYFINDING_DECISIONS
    from scripts.lesson_travel_reception_decisions import TRAVEL_RECEPTION_DECISIONS
    from scripts.lesson_navigation_action_decisions import NAVIGATION_ACTION_DECISIONS
    from scripts.lesson_service_reception_decisions import SERVICE_RECEPTION_DECISIONS
    from scripts.lesson_service_output_decisions import SERVICE_OUTPUT_DECISIONS
    from scripts.lesson_service_remaining_decisions import SERVICE_REMAINING_DECISIONS
    from scripts.lesson_familiar_people_output_decisions import FAMILIAR_PEOPLE_OUTPUT_DECISIONS
    from scripts.lesson_familiar_listening_decisions import FAMILIAR_LISTENING_DECISIONS
    from scripts.lesson_familiar_reading_decisions import FAMILIAR_READING_DECISIONS
    from scripts.lesson_familiar_routine_output_decisions import FAMILIAR_ROUTINE_OUTPUT_DECISIONS
    from scripts.lesson_foundation_social_decisions import FOUNDATION_SOCIAL_DECISIONS
    from scripts.lesson_foundation_spoken_personal_decisions import FOUNDATION_SPOKEN_PERSONAL_DECISIONS
    from scripts.lesson_foundation_written_personal_decisions import FOUNDATION_WRITTEN_PERSONAL_DECISIONS
    from scripts.lesson_listening_reception_decisions import LISTENING_RECEPTION_DECISIONS
    from scripts.lesson_postcard_reception_decision import POSTCARD_RECEPTION_DECISION
    from scripts.lesson_reading_reception_decisions import READING_RECEPTION_DECISIONS
    from scripts.lesson_relationship_model import build_map as build_relationship_map
except ModuleNotFoundError:
    from lesson_social_collaboration_decisions import SOCIAL_COLLABORATION_DECISIONS
    from lesson_social_response_decisions import SOCIAL_RESPONSE_DECISIONS
    from lesson_message_direct_decisions import MESSAGE_DIRECT_DECISIONS
    from lesson_message_mediation_decisions import MESSAGE_MEDIATION_DECISIONS
    from lesson_familiar_home_spoken_decisions import FAMILIAR_HOME_SPOKEN_DECISIONS
    from lesson_familiar_remaining_output_decisions import FAMILIAR_REMAINING_OUTPUT_DECISIONS
    from lesson_familiar_written_decisions import FAMILIAR_WRITTEN_DECISIONS
    from lesson_wayfinding_decisions import WAYFINDING_DECISIONS
    from lesson_travel_reception_decisions import TRAVEL_RECEPTION_DECISIONS
    from lesson_navigation_action_decisions import NAVIGATION_ACTION_DECISIONS
    from lesson_service_reception_decisions import SERVICE_RECEPTION_DECISIONS
    from lesson_service_output_decisions import SERVICE_OUTPUT_DECISIONS
    from lesson_service_remaining_decisions import SERVICE_REMAINING_DECISIONS
    from lesson_familiar_people_output_decisions import FAMILIAR_PEOPLE_OUTPUT_DECISIONS
    from lesson_familiar_listening_decisions import FAMILIAR_LISTENING_DECISIONS
    from lesson_familiar_reading_decisions import FAMILIAR_READING_DECISIONS
    from lesson_familiar_routine_output_decisions import FAMILIAR_ROUTINE_OUTPUT_DECISIONS
    from lesson_foundation_social_decisions import FOUNDATION_SOCIAL_DECISIONS
    from lesson_foundation_spoken_personal_decisions import FOUNDATION_SPOKEN_PERSONAL_DECISIONS
    from lesson_foundation_written_personal_decisions import FOUNDATION_WRITTEN_PERSONAL_DECISIONS
    from lesson_listening_reception_decisions import LISTENING_RECEPTION_DECISIONS
    from lesson_postcard_reception_decision import POSTCARD_RECEPTION_DECISION
    from lesson_reading_reception_decisions import READING_RECEPTION_DECISIONS
    from lesson_relationship_model import build_map as build_relationship_map


REVIEWED_AT = "2026-07-18T23:36:35+03:00"
RECEPTION_DECISIONS = {**READING_RECEPTION_DECISIONS, **LISTENING_RECEPTION_DECISIONS}
FOUNDATION_OUTPUT_DECISIONS = {
    **FOUNDATION_SOCIAL_DECISIONS,
    **FOUNDATION_SPOKEN_PERSONAL_DECISIONS,
    **FOUNDATION_WRITTEN_PERSONAL_DECISIONS,
}
FAMILIAR_RECEPTION_DECISIONS = {
    **POSTCARD_RECEPTION_DECISION,
    **FAMILIAR_READING_DECISIONS,
    **FAMILIAR_LISTENING_DECISIONS,
}
FAMILIAR_OUTPUT_DECISIONS = {
    **FAMILIAR_PEOPLE_OUTPUT_DECISIONS,
    **FAMILIAR_ROUTINE_OUTPUT_DECISIONS,
}
FAMILIAR_HOME_DECISIONS = {**FAMILIAR_HOME_SPOKEN_DECISIONS}
FAMILIAR_WRITING_DECISIONS = {**FAMILIAR_WRITTEN_DECISIONS}
FAMILIAR_FINAL_OUTPUT_DECISIONS = {**FAMILIAR_REMAINING_OUTPUT_DECISIONS}
NAVIGATION_WAYFINDING_DECISIONS = {**WAYFINDING_DECISIONS}
NAVIGATION_RECEPTION_DECISIONS = {**TRAVEL_RECEPTION_DECISIONS}
NAVIGATION_REMAINING_ACTION_DECISIONS = {**NAVIGATION_ACTION_DECISIONS}
SERVICE_OPENING_RECEPTION_DECISIONS = {**SERVICE_RECEPTION_DECISIONS}
SERVICE_OPENING_OUTPUT_DECISIONS = {**SERVICE_OUTPUT_DECISIONS}
SERVICE_REMAINING_TARGET_DECISIONS = {**SERVICE_REMAINING_DECISIONS}
MESSAGE_REMAINING_DECISIONS = {
    **MESSAGE_DIRECT_DECISIONS,
    **MESSAGE_MEDIATION_DECISIONS,
}
SOCIAL_REMAINING_DECISIONS = {
    **SOCIAL_RESPONSE_DECISIONS,
    **SOCIAL_COLLABORATION_DECISIONS,
}
DECISIONS = {
    **RECEPTION_DECISIONS,
    **FOUNDATION_OUTPUT_DECISIONS,
    **FAMILIAR_RECEPTION_DECISIONS,
    **FAMILIAR_OUTPUT_DECISIONS,
    **FAMILIAR_HOME_DECISIONS,
    **FAMILIAR_WRITING_DECISIONS,
    **FAMILIAR_FINAL_OUTPUT_DECISIONS,
    **NAVIGATION_WAYFINDING_DECISIONS,
    **NAVIGATION_RECEPTION_DECISIONS,
    **NAVIGATION_REMAINING_ACTION_DECISIONS,
    **SERVICE_OPENING_RECEPTION_DECISIONS,
    **SERVICE_OPENING_OUTPUT_DECISIONS,
    **SERVICE_REMAINING_TARGET_DECISIONS,
    **MESSAGE_REMAINING_DECISIONS,
    **SOCIAL_REMAINING_DECISIONS,
}


def build_reviewed_map() -> dict[str, Any]:
    lesson_map = build_relationship_map()
    candidates = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    if set(DECISIONS) - set(candidates):
        raise ValueError("language-target partition references an unknown candidate")
    for candidate_id, decision in DECISIONS.items():
        _apply_decision(candidates[candidate_id], decision)
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Language targets and labelled error hypotheses are reviewed for all 81 candidates across the five sequence bands.",
            "Candidate approval and final map acceptance remain separate later partitions.",
        ],
    }
    return lesson_map


def build_map() -> dict[str, Any]:
    """Return the final approved map while preserving the review-stage builder."""
    try:
        from scripts.lesson_approval_model import build_approved_map
    except ModuleNotFoundError:
        from lesson_approval_model import build_approved_map
    return build_approved_map()


def _apply_decision(candidate: dict[str, Any], decision: dict[str, Any]) -> None:
    evidence = {ref["record_id"]: ref for ref in candidate["evidence_refs"]}
    targets = {}
    for family, entries in decision["targets"].items():
        targets[family] = [
            _target(target, purpose, record_ids, evidence)
            for target, purpose, record_ids in entries
        ]
    candidate["version"] += 1
    candidate["language_targets"] = targets
    candidate["error_hypotheses"] = [
        {**copy.deepcopy(decision["error"]), "validation_status": "hypothesis"}
    ]
    candidate["risks"].append(f"Target-decision note: {decision['decision_note']}")
    candidate["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Targets and the labelled learner-error hypothesis are reviewed; independent candidate approval remains required."
        ],
    }


def _target(
    target: str,
    purpose: str,
    record_ids: list[str],
    evidence: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    missing = set(record_ids) - set(evidence)
    if missing:
        raise ValueError(f"target cites evidence absent from candidate: {sorted(missing)}")
    return {
        "target": target,
        "purpose": purpose,
        "evidence_refs": [copy.deepcopy(evidence[record_id]) for record_id in record_ids],
    }
