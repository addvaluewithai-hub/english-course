"""Apply reviewed overlap merges without changing source records."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

try:
    from scripts.lesson_overlap_specs import MERGE_SPECS
except ModuleNotFoundError:
    from lesson_overlap_specs import MERGE_SPECS

REVIEWED_AT = "2026-07-18T01:54:56+03:00"


def reconcile_overlaps(lesson_map: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(lesson_map)
    for spec in MERGE_SPECS:
        _merge_candidates(result, spec)
    _resolve_mastery_alignment(result)
    result["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "All five reviewed overlap groups and both mastery-alignment cases are resolved.",
            "The relationship and sequence model still requires reviewed authorship.",
            "Language targets, labelled error decisions, and candidate approval remain open.",
        ],
    }
    return result


def _merge_candidates(lesson_map: dict[str, Any], spec: dict[str, Any]) -> None:
    by_id = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    old_ids = list(spec["old_ids"])
    old = [by_id[candidate_id] for candidate_id in old_ids]
    merged = deepcopy(old[0])
    merged["candidate_id"] = spec["new_id"]
    merged["version"] = 2
    merged["candidate_cluster_ids"] = _unique(
        value for item in old for value in item["candidate_cluster_ids"]
    )
    merged["outcome"].update({
        "situation": spec["situation"],
        "observable_action": spec["action"],
        "essential_content": spec["content"],
        "success_condition": spec["success"],
        "statement": spec["statement"],
    })
    merged["evidence_refs"] = _merged_evidence(old, spec["new_id"])
    merged["skill_codes"] = _unique(value for item in old for value in item["skill_codes"])
    merged["mode_codes"] = _unique(value for item in old for value in item["mode_codes"])
    merged["function_codes"] = _unique(
        value for item in old for value in item["function_codes"]
    )
    merged["normalization"].update({
        "decision": "merged",
        "inputs": [ref["record_id"] for ref in merged["evidence_refs"]],
        "rationale": spec["rationale"],
    })
    merged["relationships"]["concurrent_support"] = _merged_support_relations(old)
    merged["mastery"]["fresh_task_family"] = spec["fresh_task"]
    merged["mastery"]["required_dimensions"] = list(spec["level_2"])
    merged["mastery"]["level_2_evidence"] = spec["level_2"]
    merged["scope"]["load_rationale"] = spec["scope"]
    merged["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": ["Overlap is resolved; later relationship, target, error, and approval review remains."],
    }
    first_index = min(
        index for index, item in enumerate(lesson_map["candidates"])
        if item["candidate_id"] in old_ids
    )
    lesson_map["candidates"] = [
        item for item in lesson_map["candidates"] if item["candidate_id"] not in old_ids
    ]
    lesson_map["candidates"].insert(first_index, merged)
    _replace_ids(lesson_map, old_ids, spec["new_id"])


def _merged_evidence(old: list[dict[str, Any]], new_id: str) -> list[dict[str, Any]]:
    refs: dict[str, dict[str, Any]] = {}
    for item in old:
        for ref in item["evidence_refs"]:
            current = refs.get(ref["record_id"])
            if current is None or ref["coverage"] == "full":
                refs[ref["record_id"]] = deepcopy(ref)
    complete_claims = {
        "lesson_candidate.complete_a_simple_information_form": {
            "cefr.cv2020.p084.notes_messages_and_forms.01": "The merged candidate covers the descriptor's personal, date, arrival, and hotel-registration fields in one form-completion performance.",
        },
        "lesson_candidate.locate_names_places_and_times_in_slow_recordings": {
            "gse.adult.2022.p14.007": "The merged candidate covers both people-name and place-name extraction clauses.",
        },
        "lesson_candidate.relay_predictable_person_time_or_place_details": {
            "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01": "The merged candidate covers personal details and other very simple predictable information with formulation help.",
        },
    }
    for record_id, note in complete_claims.get(new_id, {}).items():
        refs[record_id]["coverage"] = "full"
        refs[record_id]["interpretation_note"] = note
    return list(refs.values())


def _merged_support_relations(old: list[dict[str, Any]]) -> list[dict[str, Any]]:
    relations: dict[str, dict[str, Any]] = {}
    for item in old:
        for relation in item["relationships"]["concurrent_support"]:
            support_id = relation["support_id"]
            if support_id not in relations:
                relations[support_id] = deepcopy(relation)
            else:
                relations[support_id]["evidence_record_ids"] = _unique(
                    relations[support_id]["evidence_record_ids"]
                    + relation["evidence_record_ids"]
                )
    return list(relations.values())


def _replace_ids(lesson_map: dict[str, Any], old_ids: list[str], new_id: str) -> None:
    inserted = False
    sequence = []
    for candidate_id in lesson_map["sequence"]:
        if candidate_id in old_ids:
            if not inserted:
                sequence.append(new_id)
                inserted = True
        else:
            sequence.append(candidate_id)
    lesson_map["sequence"] = sequence
    for support in lesson_map["support_definitions"]:
        applies = support["applies_to_candidate_ids"]
        if any(candidate_id in applies for candidate_id in old_ids):
            applies = [candidate_id for candidate_id in applies if candidate_id not in old_ids]
            if new_id not in applies:
                applies.append(new_id)
            support["applies_to_candidate_ids"] = applies


def _resolve_mastery_alignment(lesson_map: dict[str, Any]) -> None:
    by_id = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    service = by_id["lesson_candidate.follow_a_slow_everyday_service_exchange"]
    service["skill_codes"] = ["listening"]
    service["mode_codes"] = ["reception"]
    service["relationships"]["concurrent_support"] = [
        relation for relation in service["relationships"]["concurrent_support"]
        if relation["support_id"] != "support.interaction_repair"
    ]
    repair = next(
        item for item in lesson_map["support_definitions"]
        if item["support_id"] == "support.interaction_repair"
    )
    repair["applies_to_candidate_ids"] = [
        candidate_id for candidate_id in repair["applies_to_candidate_ids"]
        if candidate_id != service["candidate_id"]
    ]
    service["normalization"]["rationale"] += " The assessed performance is reception, so interaction repair is not a required mastery dimension."
    message = by_id["lesson_candidate.leave_a_simple_whereabouts_and_return_message"]
    message["mastery"]["required_dimensions"].append("control_or_repair")
    message["mastery"]["level_2_evidence"]["control_or_repair"] = (
        "Rereads and corrects one materially wrong destination or return-time detail when prompted."
    )


def _unique(values: Any) -> list[str]:
    return list(dict.fromkeys(values))
