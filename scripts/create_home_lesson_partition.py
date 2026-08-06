"""Expand the reviewed A1 lesson map with home/object candidates."""

from __future__ import annotations

import json
from typing import Any

try:
    from scripts.create_identity_lesson_partition import OUTPUT_PATH, load
    from scripts.create_routines_lesson_partition import build_map as build_routines_map
    from scripts.lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from scripts.lesson_home_specs import HOME_SPECS
    from scripts.lesson_map_io import SOURCE_PATHS
except ModuleNotFoundError:
    from create_identity_lesson_partition import OUTPUT_PATH, load
    from create_routines_lesson_partition import build_map as build_routines_map
    from lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from lesson_home_specs import HOME_SPECS
    from lesson_map_io import SOURCE_PATHS


REVIEWED_AT = "2026-07-17T18:51:30+03:00"
ORTHOGRAPHIC_ID = "cefr.cv2020.p136.orthographic_control.01"


def build_map() -> dict[str, Any]:
    lesson_map = build_routines_map()
    index = source_index([load(path) for path in SOURCE_PATHS])
    home = [build_candidate(spec, index) for spec in HOME_SPECS]
    home_ids = [candidate["candidate_id"] for candidate in home]
    lesson_map["candidates"].extend(home)
    lesson_map["sequence"].extend(home_ids)

    basic, repair = lesson_map["support_definitions"]
    basic["evidence_refs"].append(evidence_ref(
        index, ORTHOGRAPHIC_ID, "cross_cutting", "full",
        "Copying familiar object names remains concurrent form support, not a standalone ability.",
    ))
    basic["applies_to_candidate_ids"].extend(home_ids)
    repair["applies_to_candidate_ids"].extend(
        candidate["candidate_id"] for candidate in home
        if "interaction" in candidate["mode_codes"]
    )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": "lesson_002_primary",
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "Only identity, people, routines, and home/object evidence is normalized.",
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
