"""Expand the reviewed A1 lesson map with social-contact candidates."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, load
    from scripts.create_message_lesson_partition import build_map as build_message_map
    from scripts.lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from scripts.lesson_map_io import SOURCE_PATHS
    from scripts.lesson_social_specs import SOCIAL_SPECS
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH, load
    from create_message_lesson_partition import build_map as build_message_map
    from lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from lesson_map_io import SOURCE_PATHS
    from lesson_social_specs import SOCIAL_SPECS


REVIEWED_AT = "2026-07-17T22:52:27+03:00"
GREETING_SPELLING_ID = "gse.adult.2022.p37.013"


def build_map() -> dict[str, Any]:
    lesson_map = build_message_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    social = [build_candidate(spec, index) for spec in SOCIAL_SPECS]
    social_ids = [candidate["candidate_id"] for candidate in social]
    lesson_map["candidates"].extend(social)
    lesson_map["sequence"].extend(social_ids)

    basic, repair = lesson_map["support_definitions"]
    basic["evidence_refs"].append(evidence_ref(
        index, GREETING_SPELLING_ID, "cross_cutting", "full",
        "Spelling common greetings is orthographic support, not a standalone communicative ability.",
    ))
    basic["applies_to_candidate_ids"].extend(social_ids)
    repair["applies_to_candidate_ids"].extend(
        candidate["candidate_id"] for candidate in social
        if {"interaction", "online_interaction"} & set(candidate["mode_codes"])
    )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "All topical evidence partitions are normalized as reviewed drafts.",
            "The sequence is a partition-local working order, not a final global sequence.",
            "Global coverage, overlap, balance, and relationship audit remain open.",
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
