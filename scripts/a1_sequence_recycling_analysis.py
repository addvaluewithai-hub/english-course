"""Derive explicit dependency and exact-item recycling constraints."""

from __future__ import annotations

from typing import Iterable

from scripts.a1_dependency_mastery_contract import SUPPORT_PROBES


def position_index(sequence: list[str]) -> dict[str, int]:
    positions = {candidate_id: index for index, candidate_id in enumerate(sequence, start=1)}
    positions.update({support_id: len(sequence) + 1 for support_id in SUPPORT_PROBES})
    return positions


def explicit_edges(candidates: list[dict], positions: dict[str, int]) -> list[dict]:
    rows = []
    for candidate in candidates:
        candidate_id = candidate["candidate_id"]
        for relationship in ("required_before", "helpful_before"):
            for dependency_id in candidate["current_relationships"][relationship]:
                known = dependency_id in positions and candidate_id in positions
                aligned = known and positions[dependency_id] < positions[candidate_id]
                rows.append({
                    "candidate_id": candidate_id,
                    "relationship": relationship,
                    "dependency_id": dependency_id,
                    "dependency_position": positions.get(dependency_id),
                    "candidate_position": positions.get(candidate_id),
                    "status": "aligned" if aligned else "requires_resolution",
                })
    return rows


def _row(system: str, item_id: str, introductions: Iterable[str], recycles: Iterable[str],
         positions: dict[str, int]) -> dict:
    intro_ids, recycle_ids = list(introductions), list(recycles)
    intro_positions = [positions[item] for item in intro_ids]
    earliest_intro = min(intro_positions)
    early = [item for item in recycle_ids if positions[item] <= earliest_intro]
    later = [item for item in recycle_ids if positions[item] > earliest_intro]
    if not later:
        status = "no_later_recycle_requires_reorder_or_new_recycle"
    elif early:
        status = "early_use_requires_introduction_transfer_or_reorder"
    else:
        status = "aligned"
    return {
        "system": system,
        "item_id": item_id,
        "introduction_location_ids": intro_ids,
        "recycle_location_ids": recycle_ids,
        "earliest_introduction_position": earliest_intro,
        "early_recycle_location_ids": early,
        "later_recycle_location_ids": later,
        "status": status,
    }


def exact_item_rows(grammar: dict, lexical: dict, pronunciation: dict,
                    positions: dict[str, int]) -> list[dict]:
    rows = [
        _row("grammar", item["item_id"], item["introduction_owner_ids"],
             item["recycle_owner_ids"], positions)
        for item in grammar["course_items"]
    ]
    rows += [
        _row("lexical", item["lexical_item_id"], [item["introduction_location"]],
             item["recycle_locations"], positions)
        for item in lexical["course_items"]
    ]
    rows += [
        _row("pronunciation", item["target_id"], [item["introduction_location"]],
             item["recycle_locations"], positions)
        for item in pronunciation["targets"]
    ]
    return rows
