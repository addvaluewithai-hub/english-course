"""Validate the saved relationship review and its deterministic map application."""

from __future__ import annotations

try:
    from scripts.create_lesson_relationship_partition import REVIEW_PATH
    from scripts.lesson_map_io import DEFAULT_MAP_PATH, load
    from scripts.lesson_map_validation import validation_errors
    from scripts.lesson_relationship_model import build_map, build_review
    from scripts.lesson_sequence_specs import reviewed_sequence
except ModuleNotFoundError:
    from create_lesson_relationship_partition import REVIEW_PATH
    from lesson_map_io import DEFAULT_MAP_PATH, load
    from lesson_map_validation import validation_errors
    from lesson_relationship_model import build_map, build_review
    from lesson_sequence_specs import reviewed_sequence


def review_errors() -> list[str]:
    errors: list[str] = []
    lesson_map = load(DEFAULT_MAP_PATH)
    review = load(REVIEW_PATH)
    relationship_map = build_map()
    expected_relationships = {
        item["candidate_id"]: item["relationships"]
        for item in relationship_map["candidates"]
    }
    actual_relationships = {
        item["candidate_id"]: item["relationships"]
        for item in lesson_map["candidates"]
    }
    if actual_relationships != expected_relationships:
        errors.append("saved lesson-map relationships differ from the reviewed builder")
    if review != build_review(lesson_map):
        errors.append("saved relationship review differs from its deterministic builder")
    if review["status"] != "accepted":
        errors.append("relationship review is not accepted")
    if review["interpretation_boundary"]["source_proven_strict_order"]:
        errors.append("pedagogical sequence is mislabeled as source-proven")
    if lesson_map["sequence"] != reviewed_sequence():
        errors.append("lesson-map sequence differs from the reviewed bands")
    errors.extend(validation_errors(DEFAULT_MAP_PATH))
    return errors


def main() -> int:
    errors = review_errors()
    if errors:
        print("FAIL relationship review")
        for error in errors:
            print(f"- {error}")
        return 1
    review = load(REVIEW_PATH)
    print(
        "PASS relationship review: "
        f"{review['counts']['candidates']} candidates, "
        f"{review['counts']['required_before']} required, "
        f"{review['counts']['helpful_before']} helpful"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
