"""Build candidate ownership impact, mastery reviews, and exit safeguards."""

from __future__ import annotations

from scripts.a1_dependency_mastery_policies import EXIT_ANCHORS, REVISION_ACTIONS, candidate_id


def _ownership_index(candidate_ids: list[str]) -> dict[str, dict[str, list[str]]]:
    roles = ("introduction_item_ids", "recycle_item_ids")
    return {item: {role: [] for role in roles} for item in candidate_ids}


def candidate_impacts(candidates: list[dict], item_rows: list[dict],
                      positions: dict[str, int], signals: dict[str, str]) -> list[dict]:
    index = _ownership_index([row["candidate_id"] for row in candidates])
    for item in item_rows:
        for location in item["introduction_location_ids"]:
            if location in index:
                index[location]["introduction_item_ids"].append(item["item_id"])
        for location in item["recycle_location_ids"]:
            if location in index:
                index[location]["recycle_item_ids"].append(item["item_id"])
    rows = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        intro = sorted(index[cid]["introduction_item_ids"])
        recycle = sorted(index[cid]["recycle_item_ids"])
        rows.append({
            "candidate_id": cid,
            "provisional_position": positions[cid],
            "architecture_hypothesis": signals[cid],
            "introduction_item_ids": intro,
            "recycle_item_ids": recycle,
            "transfer_required_if_merged_supported_or_retired": bool(intro or recycle),
        })
    return rows


def mastery_reviews(candidates: list[dict], outcome_reviews: dict[str, dict]) -> list[dict]:
    rows = []
    for candidate in candidates:
        cid = candidate["candidate_id"]
        outcome = outcome_reviews[cid]
        mastery = candidate["current_mastery"]
        revisions = [REVISION_ACTIONS[code] for code in outcome["risk_codes"] if code in REVISION_ACTIONS]
        aligned = outcome["a1_fit_status"] == "fits_a1_boundary"
        rows.append({
            "candidate_id": cid,
            "fresh_task_family": mastery["fresh_task_family"],
            "critical_failure_count": len(mastery["critical_failures"]),
            "delayed_probe": mastery["delayed_probe"],
            "structural_status": "complete",
            "construct_alignment_status": (
                "aligned_with_current_outcome" if aligned else "requires_scope_or_construct_revision"
            ),
            "risk_codes": outcome["risk_codes"],
            "required_revision_actions": revisions,
            "no_answer_revealing_support_required": True,
        })
    return rows


def exit_safeguards(exit_coverage: list[dict]) -> list[dict]:
    owner_index = {row["dimension_code"]: set(row["candidate_owner_ids"]) for row in exit_coverage}
    rows = []
    for dimension, short_ids in EXIT_ANCHORS.items():
        anchors = [candidate_id(item) for item in short_ids]
        rows.append({
            "dimension_code": dimension,
            "current_owner_count": len(owner_index[dimension]),
            "protected_capability_anchor_ids": anchors,
            "all_anchors_are_current_owners": all(item in owner_index[dimension] for item in anchors),
            "survival_rule": "The capability must survive as a lesson, integrated mastery station, or explicit support owner after merge/split decisions.",
        })
    return rows
