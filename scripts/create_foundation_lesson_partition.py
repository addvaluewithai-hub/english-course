"""Complete the source-exact foundation and strategy evidence partition."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, load
    from scripts.create_social_lesson_partition import build_map as build_social_map
    from scripts.lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from scripts.lesson_foundation_candidate_specs import FOUNDATION_CANDIDATE_SPECS
    from scripts.lesson_foundation_supports import add_foundation_supports
    from scripts.lesson_map_io import SOURCE_PATHS
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH, load
    from create_social_lesson_partition import build_map as build_social_map
    from lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from lesson_foundation_candidate_specs import FOUNDATION_CANDIDATE_SPECS
    from lesson_foundation_supports import add_foundation_supports
    from lesson_map_io import SOURCE_PATHS


REVIEWED_AT = "2026-07-17T23:53:24+03:00"
EXTENSIONS = {
    "lesson_candidate.follow_simple_game_or_activity_instructions": (
        "gse.adult.2022.p14.006",
        "Slow, carefully addressed short instructions directly support the same action task.",
    ),
    "lesson_candidate.understand_talk_about_leisure_preferences_and_abilities": (
        "gse.adult.2022.p14.010",
        "The can/can't contrast is directly assessed in the candidate's ability-information input.",
    ),
    "lesson_candidate.exchange_routine_and_preference_information": (
        "gse.adult.2022.p24.006",
        "Answering simple habit and routine questions is directly elicited in this exchange.",
    ),
}


def build_map() -> dict[str, Any]:
    lesson_map = build_social_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    _extend_existing_candidates(lesson_map, index)

    candidates = [build_candidate(spec, index) for spec in FOUNDATION_CANDIDATE_SPECS]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    lesson_map["candidates"].extend(candidates)
    lesson_map["sequence"].extend(candidate_ids)
    lesson_map["support_definitions"][0]["applies_to_candidate_ids"].extend(candidate_ids)
    add_foundation_supports(lesson_map, index)
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "All 218 included source records are explicit in candidates or support.",
            "The sequence is a partition-local working order, not a final global sequence.",
            "Global overlap, balance, relationship, and candidate-approval audit remain open.",
        ],
    }
    return lesson_map


def _extend_existing_candidates(
    lesson_map: dict[str, Any], index: dict[str, tuple[str, dict[str, Any]]]
) -> None:
    candidates = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    for candidate_id, (record_id, note) in EXTENSIONS.items():
        candidate = candidates[candidate_id]
        candidate["evidence_refs"].append(
            evidence_ref(index, record_id, "supporting", "full", note)
        )
        candidate["normalization"]["inputs"].append(record_id)
        candidate["review"]["reviewed_at"] = REVIEWED_AT


def main() -> None:
    OUTPUT_PATH.write_text(
        json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
