"""Build final unit and lesson rows while preserving prototype lineage."""

from scripts.a1_final_decision_helpers import cid
from scripts.a1_scope_sequence_titles import TITLES


def _prototype(candidate_id: str, old_index: dict[str, dict]) -> dict:
    old = old_index.get(candidate_id)
    if old is None:
        return {"old_lesson_id": None, "old_content_path": None, "reuse_status": "author_new_package"}
    if candidate_id == cid("give_short_self_introduction"):
        status = "gold_reference_preserved_requires_id_rebind"
    else:
        status = "prototype_requires_rebuild_to_v1_scope"
    return {
        "old_lesson_id": old["lesson_id"], "old_content_path": old["content_path"],
        "reuse_status": status,
    }


def build_units(unit_catalog: tuple[dict, ...], final_decisions: dict, old_unit: dict) -> list[dict]:
    capabilities = {row["final_owner_id"]: row for row in final_decisions["final_lesson_capabilities"]}
    old_index = {row["candidate_id"]: row for row in old_unit["lessons"]}
    units, global_position = [], 0
    for unit_number, source in enumerate(unit_catalog, start=1):
        lessons = []
        directory = f"units/unit-{unit_number:02d}-{source['unit_id'].split('.', 2)[2].replace('_', '-')}"
        for local_position, short_id in enumerate(source["lesson_short_ids"], start=1):
            global_position += 1
            owner = cid(short_id)
            capability = capabilities[owner]
            title_en, title_ar = TITLES[short_id]
            lesson_id = f"U{unit_number}-L{local_position:02d}"
            lessons.append({
                "lesson_id": lesson_id, "global_sequence_position": global_position,
                "final_owner_id": owner, "title": {"en": title_en, "ar": title_ar},
                "outcome_statement": capability["outcome_statement"],
                "mastery_action": capability["mastery_action"],
                "source_candidate_ids": capability["source_candidate_ids"],
                "planned_content_path": f"{directory}/lessons/{lesson_id.lower()}",
                "prototype_lineage": _prototype(owner, old_index),
                "status": "scope_sequence_locked_content_pending",
            })
        units.append({
            "unit_id": source["unit_id"], "unit_number": unit_number,
            "directory": directory, "title": source["title"], "unit_outcome": source["unit_outcome"],
            "lesson_count": len(lessons), "lessons": lessons,
            "unit_review_id": f"unit_review.U{unit_number}",
        })
    return units


def lesson_index(units: list[dict]) -> tuple[dict[str, dict], dict[str, int], dict[str, int]]:
    rows = [lesson for unit in units for lesson in unit["lessons"]]
    by_owner = {row["final_owner_id"]: row for row in rows}
    owner_unit = {
        lesson["final_owner_id"]: unit["unit_number"] for unit in units for lesson in unit["lessons"]
    }
    review_unit = {unit["unit_review_id"]: unit["unit_number"] for unit in units}
    return by_owner, owner_unit, review_unit
