"""Markdown rendering for the locked A1 scope and sequence."""


def render(data: dict) -> str:
    audit = data["audit"]
    intro = audit["introduction_resolution_counts"]
    recycle = audit["first_recycle_resolution_counts"]
    lines = [
        "# A1 Scope and Sequence v1", "",
        "Status: SPINE-006 passed; six units and 45 learner-facing capabilities are locked.", "",
        f"- Units: {audit['unit_count']}", f"- Lessons/capabilities: {audit['lesson_count']}",
        f"- Exact language/pronunciation items placed: {audit['exact_item_count']}",
        f"- Named introductions retained: {intro.get('retained_named_introduction', 0)}",
        f"- Introductions transferred to earliest final use: {intro.get('transferred_to_earliest_final_use', 0)}",
        f"- Existing-owner first recycles: {recycle.get('existing_final_owner', 0)}",
        f"- Unit-review first recycles added: {recycle.get('unit_review_added', 0)}",
        f"- Carried sequence findings resolved: {audit['carried_sequence_findings_resolved']}",
        f"- Unit mastery stations: {audit['unit_mastery_station_count']}",
        f"- Exit stations: {audit['exit_station_count']}", "",
        "Every exact item now has an introduction, a later fresh recycle, and a still-later",
        "unit-review or exit consolidation. The old 60 order findings are resolved rather",
        "than hidden. Lesson content must follow these placements during authoring.", "",
    ]
    for unit in data["units"]:
        lines += [f"## Unit {unit['unit_number']}: {unit['title']['en']}", "",
                  f"{unit['title']['ar']}", "", unit["unit_outcome"]["en"], "",
                  "| Lesson | Title | Capability owner |", "| --- | --- | --- |"]
        for lesson in unit["lessons"]:
            lines.append(f"| {lesson['lesson_id']} | {lesson['title']['en']} | `{lesson['final_owner_id']}` |")
        lines += ["", f"Unit review: {unit['unit_review']['review_id']} — "
                  f"{len(unit['unit_review']['review_item_ids'])} exact items and "
                  f"{len(unit['unit_review']['mastery_stations'])} fresh mastery stations.", ""]
    migration = data["unit1_prototype_migration"]
    lines += ["## Unit 1 prototype migration", "",
              f"The eight existing Unit 1 packages are preserved as prototypes. The gold",
              f"`Introduce Yourself` package moves from {migration['old_gold_lesson_id']} to",
              f"{migration['new_gold_lesson_id']} after an input model; a new social-opening",
              "lesson becomes U1-L01. Packages must be rebuilt against v1 ownership before release.", "",
              "## Authoring gate", "",
              "The A1 content factory is now authorised to migrate Unit 1 and author the remaining",
              "locked lessons. Scope, order, exact ownership, review locations, and exit stations",
              "must not drift without a new reviewed curriculum version.", ""]
    return "\n".join(lines)
