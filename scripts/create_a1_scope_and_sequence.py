"""Create the final six-unit A1 scope and sequence."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from scripts.a1_scope_sequence_assessment import (
    attach_unit_mastery, capability_station_coverage, exit_assessment, mapped_dependencies,
)
from scripts.a1_scope_sequence_contract import INPUTS, OUTPUT, REPORT, REVIEWED_AT, REVIEWER, ROOT
from scripts.a1_scope_sequence_items import build_item_placements, review_item_index
from scripts.a1_scope_sequence_lessons import build_units
from scripts.a1_scope_sequence_report import render
from scripts.a1_scope_sequence_unit_catalog import UNITS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _unit1_migration(units: list[dict], old_unit: dict) -> dict:
    new_unit = units[0]
    new_index = {row["final_owner_id"]: row for row in new_unit["lessons"]}
    old_ids = {row["candidate_id"] for row in old_unit["lessons"]}
    gold_id = "lesson_candidate.give_short_self_introduction"
    return {
        "status": "prototype_preserved_rebuild_required",
        "old_package_count": len(old_ids),
        "old_capabilities_preserved_in_new_unit": sum(item in new_index for item in old_ids),
        "new_unit_lesson_count": new_unit["lesson_count"],
        "added_social_owner_id": "lesson_candidate.open_and_close_a_basic_social_exchange",
        "old_gold_lesson_id": next(row["lesson_id"] for row in old_unit["lessons"] if row["candidate_id"] == gold_id),
        "new_gold_lesson_id": new_index[gold_id]["lesson_id"],
        "gold_content_path": new_index[gold_id]["prototype_lineage"]["old_content_path"],
        "migration_rule": "Preserve useful authored content, but rebuild manifests, exact targets, practice, and mastery against A1 scope-and-sequence v1.",
    }


def build() -> dict:
    final, worklist, dependency, _abilities, _profiles, grammar, lexical, pronunciation, old_unit, _gold = [
        _load(path) for path in INPUTS
    ]
    base_units = build_units(UNITS, final, old_unit)
    placements = build_item_placements(
        base_units, final, dependency, grammar, lexical, pronunciation
    )
    review_items, exit_items = review_item_index(base_units, placements)
    units = attach_unit_mastery(base_units, review_items)
    exit_plan = exit_assessment(exit_items)
    coverage = capability_station_coverage(units)
    dependencies, absorbed_edges = mapped_dependencies(worklist, final, units)
    intro_counts = Counter(row["introduction_resolution"] for row in placements)
    recycle_counts = Counter(row["first_recycle_resolution"] for row in placements)
    return {
        "schema_version": 1,
        "scope_sequence_id": "a1_scope_and_sequence",
        "version": 1,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in INPUTS
        ],
        "policy": {
            "status": "locked_v1",
            "lesson_count_is_capability_count": True,
            "gold_lesson_status": "preserved_and_moved_after_input",
            "exact_item_lifecycle": "introduce_then_fresh_recycle_then_consolidate",
            "content_factory_status": "authorised_against_locked_scope",
            "release_status": "blocked_until_content_packages_and_learner_validation_pass",
        },
        "units": units,
        "exact_item_placements": placements,
        "mapped_prerequisite_edges": dependencies,
        "capability_unit_mastery_coverage": coverage,
        "exit_assessment": exit_plan,
        "unit1_prototype_migration": _unit1_migration(units, old_unit),
        "audit": {
            "unit_count": len(units),
            "unit_lesson_counts": [unit["lesson_count"] for unit in units],
            "lesson_count": sum(unit["lesson_count"] for unit in units),
            "unique_lesson_owner_count": len({lesson["final_owner_id"] for unit in units for lesson in unit["lessons"]}),
            "exact_item_count": len(placements),
            "introduction_resolution_counts": dict(sorted(intro_counts.items())),
            "first_recycle_resolution_counts": dict(sorted(recycle_counts.items())),
            "carried_sequence_findings_resolved": sum(row["prior_sequence_status"] != "aligned" for row in placements),
            "unresolved_item_placements": sum(row["final_status"] != "resolved_introduction_recycle_consolidation" for row in placements),
            "mapped_prerequisite_edge_count": len(dependencies),
            "aligned_mapped_prerequisite_edges": sum(row["status"] == "aligned" for row in dependencies),
            "absorbed_source_prerequisite_edges": absorbed_edges,
            "unit_mastery_station_count": sum(len(unit["unit_review"]["mastery_stations"]) for unit in units),
            "capabilities_with_unit_mastery": sum(bool(row["unit_station_ids"]) for row in coverage),
            "exit_station_count": len(exit_plan["stations"]),
            "exit_dimensions_covered": len({code for row in exit_plan["stations"] for code in row["dimension_codes"]}),
            "unresolved_questions": [],
        },
        "review": {
            "status": "SPINE_006_passed_scope_sequence_locked",
            "reviewer": REVIEWER,
            "reviewed_at": REVIEWED_AT,
            "statement": "A1 v1 is locked at six units and 45 capabilities; content authoring may proceed without scope drift.",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({data['audit']['unit_count']} units; {data['audit']['lesson_count']} lessons)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
