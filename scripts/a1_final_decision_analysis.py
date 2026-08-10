"""Derive enriched decisions, ownership transfers, and final capability owners."""

from __future__ import annotations

from scripts.a1_final_decision_catalog import TRANSFER_OVERRIDES


def enrich_decisions(catalog: tuple[dict, ...], worklist: dict, outcomes: dict,
                     dependency: dict) -> list[dict]:
    candidates = {row["candidate_id"]: row for row in worklist["candidates"]}
    outcome_index = {row["candidate_id"]: row for row in outcomes["reviews"]}
    mastery_index = {row["candidate_id"]: row for row in dependency["mastery_reviews"]}
    impact_index = {row["candidate_id"]: row for row in dependency["candidate_ownership_impacts"]}
    anchors = {
        item for row in dependency["exit_safeguards"]
        for item in row["protected_capability_anchor_ids"]
    }
    rows = []
    for item in catalog:
        cid = item["candidate_id"]
        candidate, outcome, mastery, impact = (
            candidates[cid], outcome_index[cid], mastery_index[cid], impact_index[cid]
        )
        rows.append({
            **item,
            "original_sequence_position": candidate["original_sequence_position"],
            "original_outcome_statement": candidate["outcome"]["statement"],
            "a1_fit_status": outcome["a1_fit_status"],
            "original_architecture_hypothesis": outcome["independence_signal"],
            "construct_revision_actions": mastery["required_revision_actions"],
            "exact_introduction_item_ids": impact["introduction_item_ids"],
            "exact_recycle_item_ids": impact["recycle_item_ids"],
            "protected_exit_anchor": cid in anchors,
            "unresolved_questions": [],
            "review_status": "accepted",
        })
    return rows


def ownership_transfers(decisions: list[dict]) -> list[dict]:
    rows = []
    for decision in decisions:
        if decision["survives_as_learner_lesson"]:
            continue
        overrides = TRANSFER_OVERRIDES.get(decision["candidate_id"], {})
        for role, field in (("introduction", "exact_introduction_item_ids"),
                            ("recycle", "exact_recycle_item_ids")):
            for item_id in decision[field]:
                rows.append({
                    "source_candidate_id": decision["candidate_id"],
                    "role": role,
                    "item_id": item_id,
                    "destination_owner_id": overrides.get(
                        item_id, decision["primary_transfer_owner_id"]
                    ),
                    "status": "accepted_transfer",
                })
    return rows


def _final_role_index(decisions: list[dict], transfers: list[dict]) -> dict[str, dict[str, set[str]]]:
    owners = {
        owner for row in decisions for owner in row["final_owner_ids"]
        if row["survives_as_learner_lesson"] or owner.startswith("support.")
    }
    index = {owner: {"introduction": set(), "recycle": set()} for owner in owners}
    for row in decisions:
        if not row["survives_as_learner_lesson"]:
            continue
        owner = row["candidate_id"]
        index[owner]["introduction"].update(row["exact_introduction_item_ids"])
        index[owner]["recycle"].update(row["exact_recycle_item_ids"])
    for row in transfers:
        index[row["destination_owner_id"]][row["role"]].add(row["item_id"])
    return index


def final_capabilities(decisions: list[dict], transfers: list[dict]) -> tuple[list[dict], list[dict]]:
    role_index = _final_role_index(decisions, transfers)
    lesson_ids = {row["candidate_id"] for row in decisions if row["survives_as_learner_lesson"]}
    lessons, supports = [], []
    for row in decisions:
        if not row["survives_as_learner_lesson"]:
            continue
        owner = row["candidate_id"]
        sources = [item["candidate_id"] for item in decisions if owner in item["final_owner_ids"]]
        lessons.append({
            "final_owner_id": owner,
            "decision": row["decision"],
            "source_candidate_ids": sources,
            "outcome_statement": row["revised_outcome_statement"] or row["original_outcome_statement"],
            "mastery_action": row["mastery_action"],
            "introduction_item_ids": sorted(role_index[owner]["introduction"]),
            "recycle_item_ids": sorted(role_index[owner]["recycle"]),
            "status": "accepted_for_scope_and_sequence",
        })
    for owner in sorted(set(role_index) - lesson_ids):
        sources = [item["candidate_id"] for item in decisions if owner in item["final_owner_ids"]]
        supports.append({
            "support_owner_id": owner,
            "source_candidate_ids": sources,
            "introduction_item_ids": sorted(role_index[owner]["introduction"]),
            "recycle_item_ids": sorted(role_index[owner]["recycle"]),
            "status": "accepted_cross_cutting_support",
        })
    return lessons, supports


def exit_resolutions(dependency: dict, decision_index: dict[str, dict]) -> list[dict]:
    rows = []
    for safeguard in dependency["exit_safeguards"]:
        for anchor in safeguard["protected_capability_anchor_ids"]:
            decision = decision_index[anchor]
            rows.append({
                "dimension_code": safeguard["dimension_code"],
                "anchor_candidate_id": anchor,
                "decision": decision["decision"],
                "resolved_owner_ids": decision["final_owner_ids"],
                "status": "resolved",
            })
    return rows
