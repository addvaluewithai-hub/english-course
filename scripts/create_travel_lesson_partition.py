"""Expand the reviewed A1 lesson map with places/directions/travel candidates."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_home_lesson_partition import build_map as build_home_map
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, load
    from scripts.lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from scripts.lesson_map_io import SOURCE_PATHS
    from scripts.lesson_travel_specs import TRAVEL_SPECS
except ModuleNotFoundError:
    from create_home_lesson_partition import build_map as build_home_map
    from create_identity_lesson_partition import OUTPUT_PATH, load
    from lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from lesson_map_io import SOURCE_PATHS
    from lesson_travel_specs import TRAVEL_SPECS


REVIEWED_AT = "2026-07-17T19:51:11+03:00"
DIRECTION_COPY_ID = "gse.adult.2022.p37.002"


def build_map() -> dict[str, Any]:
    lesson_map = build_home_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    travel = [build_candidate(spec, index) for spec in TRAVEL_SPECS]
    travel_ids = [candidate["candidate_id"] for candidate in travel]
    lesson_map["candidates"].extend(travel)
    lesson_map["sequence"].extend(travel_ids)

    basic, repair = lesson_map["support_definitions"]
    basic["evidence_refs"].append(evidence_ref(
        index, DIRECTION_COPY_ID, "cross_cutting", "full",
        "Copying a short direction sentence remains form support, not a standalone ability.",
    ))
    basic["applies_to_candidate_ids"].extend(travel_ids)
    repair["applies_to_candidate_ids"].extend(
        candidate["candidate_id"] for candidate in travel
        if "interaction" in candidate["mode_codes"]
    )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Only identity, people, routines, home, and travel evidence is normalized.",
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
