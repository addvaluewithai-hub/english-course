"""Expand the reviewed A1 lesson map with people-and-relationships candidates."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, build_map as build_identity_map, load
    from scripts.lesson_candidate_factory import build_candidate, source_index
    from scripts.lesson_map_io import SOURCE_PATHS
    from scripts.lesson_people_specs import PEOPLE_SPECS
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH, build_map as build_identity_map, load
    from lesson_candidate_factory import build_candidate, source_index
    from lesson_map_io import SOURCE_PATHS
    from lesson_people_specs import PEOPLE_SPECS


REVIEWED_AT = "2026-07-17T16:48:13+03:00"


def build_map() -> dict[str, Any]:
    lesson_map = build_identity_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    people = [build_candidate(spec, index) for spec in PEOPLE_SPECS]
    people_ids = [candidate["candidate_id"] for candidate in people]
    lesson_map["candidates"].extend(people)
    lesson_map["sequence"] = [*lesson_map["sequence"], *people_ids]

    basic, repair = lesson_map["support_definitions"]
    basic["applies_to_candidate_ids"] = [
        *basic["applies_to_candidate_ids"], *people_ids
    ]
    repair["applies_to_candidate_ids"].extend(
        candidate["candidate_id"] for candidate in people
        if "interaction" in candidate["mode_codes"]
    )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Only identity and people-and-relationships evidence is normalized.",
            "The sequence is a partition-local working order, not a final global sequence.",
            "Global coverage, balance, cross-cluster overlap, and independent review remain open.",
        ],
    }
    return lesson_map


def main() -> None:
    OUTPUT_PATH.write_text(
        json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
