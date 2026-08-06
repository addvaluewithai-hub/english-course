"""Expand the reviewed A1 lesson map with messages/signs/forms candidates."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, load
    from scripts.create_service_lesson_partition import build_map as build_service_map
    from scripts.lesson_candidate_factory import build_candidate, source_index
    from scripts.lesson_map_io import SOURCE_PATHS
    from scripts.lesson_message_specs import MESSAGE_SPECS
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH, load
    from create_service_lesson_partition import build_map as build_service_map
    from lesson_candidate_factory import build_candidate, source_index
    from lesson_map_io import SOURCE_PATHS
    from lesson_message_specs import MESSAGE_SPECS


REVIEWED_AT = "2026-07-17T21:52:40+03:00"


def build_map() -> dict[str, Any]:
    lesson_map = build_service_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    message = [build_candidate(spec, index) for spec in MESSAGE_SPECS]
    message_ids = [candidate["candidate_id"] for candidate in message]
    lesson_map["candidates"].extend(message)
    lesson_map["sequence"].extend(message_ids)

    basic, repair = lesson_map["support_definitions"]
    basic["applies_to_candidate_ids"].extend(message_ids)
    repair["applies_to_candidate_ids"].extend(
        candidate["candidate_id"] for candidate in message
        if {"interaction", "online_interaction"} & set(candidate["mode_codes"])
    )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Seven topical partitions are normalized; social contact remains.",
            "The sequence is a partition-local working order, not a final global sequence.",
            "Global coverage, balance, cross-cluster overlap, and final review remain open.",
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
