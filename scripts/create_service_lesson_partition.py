"""Expand the reviewed A1 lesson map with food/shopping/service candidates."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, load
    from scripts.create_travel_lesson_partition import build_map as build_travel_map
    from scripts.lesson_candidate_factory import build_candidate, source_index
    from scripts.lesson_map_io import SOURCE_PATHS
    from scripts.lesson_service_specs import SERVICE_SPECS
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH, load
    from create_travel_lesson_partition import build_map as build_travel_map
    from lesson_candidate_factory import build_candidate, source_index
    from lesson_map_io import SOURCE_PATHS
    from lesson_service_specs import SERVICE_SPECS


REVIEWED_AT = "2026-07-17T20:52:14+03:00"


def build_map() -> dict[str, Any]:
    lesson_map = build_travel_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    service = [build_candidate(spec, index) for spec in SERVICE_SPECS]
    service_ids = [candidate["candidate_id"] for candidate in service]
    lesson_map["candidates"].extend(service)
    lesson_map["sequence"].extend(service_ids)

    basic, repair = lesson_map["support_definitions"]
    basic["applies_to_candidate_ids"].extend(service_ids)
    repair["applies_to_candidate_ids"].extend(
        candidate["candidate_id"] for candidate in service
        if {"interaction", "online_interaction"} & set(candidate["mode_codes"])
    )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Six topical partitions are normalized; messages and social contact remain.",
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
