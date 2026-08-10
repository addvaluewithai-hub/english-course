"""Expand unit/exit mastery and map legacy prerequisites to final owners."""

from __future__ import annotations

from scripts.a1_final_decision_helpers import cid
from scripts.a1_scope_sequence_mastery_catalog import EXIT_STATIONS, UNIT_STATIONS


def _expand_station(row: dict) -> dict:
    return {
        "station_id": row["station_id"], "title": row["title"],
        "owner_ids": [cid(item) for item in row["owner_short_ids"]],
        "dimension_codes": list(row["dimension_codes"]),
        "fresh_task": row["fresh_task"], "critical_failure": row["critical_failure"],
        "answer_revealing_support_allowed": False,
    }


def attach_unit_mastery(units: list[dict], review_items: dict[str, list[str]]) -> list[dict]:
    rows = []
    for unit in units:
        review_id = unit["unit_review_id"]
        stations = [_expand_station(item) for item in UNIT_STATIONS[unit["unit_id"]]]
        rows.append({
            **unit,
            "unit_review": {
                "review_id": review_id,
                "review_item_ids": review_items[review_id],
                "fresh_variant_policy": "Change people, details, order, visuals, roles, or context; never reuse an answer-bearing model.",
                "mastery_stations": stations,
                "all_station_support_non_answer_revealing": True,
            },
        })
    return rows


def exit_assessment(exit_language_items: list[str]) -> dict:
    return {
        "assessment_id": "a1.exit_assessment.v1",
        "language_probe_id": "assessment.a1_exit_language_probe",
        "language_probe_item_ids": exit_language_items,
        "fresh_variant_policy": "Use unseen concrete tasks with changed details; clarify the task but never supply the response.",
        "stations": [_expand_station(item) for item in EXIT_STATIONS],
        "all_seven_dimensions_required": True,
        "decision_rule": "Pass requires every station's essential meaning and task outcome; strengths do not cancel a critical failure in another dimension.",
    }


def capability_station_coverage(units: list[dict]) -> list[dict]:
    index: dict[str, list[str]] = {}
    for unit in units:
        for station in unit["unit_review"]["mastery_stations"]:
            for owner in station["owner_ids"]:
                index.setdefault(owner, []).append(station["station_id"])
    return [
        {"final_owner_id": lesson["final_owner_id"], "unit_station_ids": index.get(lesson["final_owner_id"], [])}
        for unit in units for lesson in unit["lessons"]
    ]


def mapped_dependencies(worklist: dict, final_decisions: dict, units: list[dict]) -> tuple[list[dict], int]:
    primary = {row["candidate_id"]: row["primary_transfer_owner_id"] for row in final_decisions["decisions"]}
    positions = {
        lesson["final_owner_id"]: lesson["global_sequence_position"]
        for unit in units for lesson in unit["lessons"]
    }
    grouped: dict[tuple[str, str, str], int] = {}
    absorbed = 0
    for candidate in worklist["candidates"]:
        for relationship in ("required_before", "helpful_before"):
            for dependency in candidate["current_relationships"][relationship]:
                before, after = primary[dependency], primary[candidate["candidate_id"]]
                if before == after or before.startswith("support.") or after.startswith("support."):
                    absorbed += 1
                    continue
                key = (before, after, relationship)
                grouped[key] = grouped.get(key, 0) + 1
    rows = []
    for (before, after, relationship), source_count in sorted(grouped.items()):
        rows.append({
            "before_owner_id": before, "after_owner_id": after,
            "relationship": relationship, "source_edge_count": source_count,
            "before_position": positions[before], "after_position": positions[after],
            "status": "aligned" if positions[before] < positions[after] else "invalid_order",
        })
    return rows, absorbed
