"""Resolve exact-item introductions, fresh recycling, and consolidation."""

from __future__ import annotations

from scripts.a1_scope_sequence_contract import EXIT_PROBE_ID, POLITENESS_SUPPORT_ID
from scripts.a1_scope_sequence_lessons import lesson_index


def _metadata(grammar: dict, lexical: dict, pronunciation: dict) -> dict[str, dict]:
    rows = {
        item["item_id"]: {"system": "grammar", "label": item["title"]}
        for item in grammar["course_items"]
    }
    rows.update({
        item["lexical_item_id"]: {"system": "lexical", "label": item["canonical_form"]}
        for item in lexical["course_items"]
    })
    rows.update({
        item["target_id"]: {"system": "pronunciation", "label": item["title"]}
        for item in pronunciation["targets"]
    })
    return rows


def _role_index(final_decisions: dict) -> dict[str, dict[str, list[str]]]:
    index: dict[str, dict[str, list[str]]] = {}
    for owner in final_decisions["final_lesson_capabilities"] + final_decisions["support_owners"]:
        owner_id = owner.get("final_owner_id", owner.get("support_owner_id"))
        for role, field in (("intro", "introduction_item_ids"), ("recycle", "recycle_item_ids")):
            for item_id in owner[field]:
                index.setdefault(item_id, {"intro": [], "recycle": []})[role].append(owner_id)
    return index


def _positions(units: list[dict]) -> dict[str, int]:
    positions = {POLITENESS_SUPPORT_ID: 0, EXIT_PROBE_ID: 10000}
    for unit in units:
        for lesson in unit["lessons"]:
            positions[lesson["final_owner_id"]] = lesson["global_sequence_position"] * 10
        positions[unit["unit_review_id"]] = unit["lessons"][-1]["global_sequence_position"] * 10 + 5
    return positions


def _review_after(location: str, owner_unit: dict[str, int], review_unit: dict[str, int],
                  unit_count: int) -> str:
    if location == POLITENESS_SUPPORT_ID:
        return "unit_review.U1"
    if location in owner_unit:
        return f"unit_review.U{owner_unit[location]}"
    if location in review_unit:
        next_unit = review_unit[location] + 1
        return f"unit_review.U{next_unit}" if next_unit <= unit_count else EXIT_PROBE_ID
    return EXIT_PROBE_ID


def build_item_placements(units: list[dict], final_decisions: dict, dependency: dict,
                          grammar: dict, lexical: dict, pronunciation: dict) -> list[dict]:
    _lessons, owner_unit, review_unit = lesson_index(units)
    positions, roles = _positions(units), _role_index(final_decisions)
    metadata = _metadata(grammar, lexical, pronunciation)
    old_status = {row["item_id"]: row["status"] for row in dependency["exact_item_sequence"]}
    placements = []
    for item_id in [row["item_id"] for row in dependency["exact_item_sequence"]]:
        role = roles[item_id]
        all_owners = sorted(set(role["intro"] + role["recycle"]), key=positions.__getitem__)
        introduction = all_owners[0]
        later = [owner for owner in all_owners[1:] if positions[owner] > positions[introduction]]
        first_recycle = later[0] if later else _review_after(
            introduction, owner_unit, review_unit, len(units)
        )
        consolidation = _review_after(first_recycle, owner_unit, review_unit, len(units))
        placements.append({
            "item_id": item_id, **metadata[item_id],
            "candidate_introduction_owner_ids": sorted(role["intro"]),
            "candidate_recycle_owner_ids": sorted(role["recycle"]),
            "final_introduction_location_id": introduction,
            "introduction_resolution": (
                "retained_named_introduction" if introduction in role["intro"]
                else "transferred_to_earliest_final_use"
            ),
            "first_fresh_recycle_location_id": first_recycle,
            "first_recycle_resolution": (
                "existing_final_owner" if first_recycle in all_owners else "unit_review_added"
            ),
            "consolidation_location_id": consolidation,
            "prior_sequence_status": old_status[item_id],
            "final_status": "resolved_introduction_recycle_consolidation",
        })
    return placements


def review_item_index(units: list[dict], placements: list[dict]) -> tuple[dict[str, list[str]], list[str]]:
    review_ids = {unit["unit_review_id"] for unit in units}
    index = {item: [] for item in review_ids}
    exit_items = []
    for row in placements:
        for location in (row["first_fresh_recycle_location_id"], row["consolidation_location_id"]):
            if location in index:
                index[location].append(row["item_id"])
            elif location == EXIT_PROBE_ID:
                exit_items.append(row["item_id"])
    return {key: sorted(set(value)) for key, value in index.items()}, sorted(set(exit_items))
