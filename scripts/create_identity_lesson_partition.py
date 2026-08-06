"""Create the reviewed identity partition of the in-progress A1 lesson map."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from scripts.lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from scripts.lesson_identity_specs import IDENTITY_SPECS
    from scripts.lesson_map_io import PROJECT_ROOT, SOURCE_PATHS
except ModuleNotFoundError:
    from lesson_candidate_factory import build_candidate, evidence_ref, source_index
    from lesson_identity_specs import IDENTITY_SPECS
    from lesson_map_io import PROJECT_ROOT, SOURCE_PATHS


OUTPUT_PATH = PROJECT_ROOT / "data/reviewed/a1-lesson-map.json"
BASIC_IDS = [
    "cefr.cv2020.p131.general_linguistic_range.01",
    "cefr.cv2020.p132.grammatical_accuracy.01",
    "cefr.cv2020.p135.overall_phonological_control.01",
    "cefr.cv2020.p136.orthographic_control.02",
]
REPAIR_IDS = [
    "cefr.cv2020.p072.overall_oral_interaction.01",
    "cefr.cv2020.p089.asking_for_clarification.01",
    "cefr.cv2020.p089.asking_for_clarification.02",
]


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_map() -> dict[str, Any]:
    collections = [load(path) for path in SOURCE_PATHS]
    index = source_index(collections)
    candidates = [build_candidate(spec, index) for spec in IDENTITY_SPECS]
    candidate_ids = [candidate["candidate_id"] for candidate in candidates]
    interaction_ids = [
        candidate["candidate_id"] for candidate in candidates
        if "interaction" in candidate["mode_codes"]
    ]
    return {
        "schema_version": 1,
        "map_id": "a1_lesson_map",
        "level": "a1",
        "version": 1,
        "status": "in_progress",
        "evidence_dataset_ids": [collection["dataset_id"] for collection in collections],
        "candidates": candidates,
        "sequence": candidate_ids,
        "support_definitions": [
            support_definition(
                index, "support.basic_language_control", "Basic A1 language control",
                BASIC_IDS, candidate_ids,
            ),
            support_definition(
                index, "support.interaction_repair", "Interaction clarification and repair",
                REPAIR_IDS, interaction_ids,
            ),
        ],
        "review": {
            "status": "needs_review",
            "reviewer": "lesson_002_primary",
            "reviewed_at": "2026-07-17T15:47:40+03:00",
            "issues": [
                "Only identity and personal-information evidence is normalized.",
                "The sequence is a partition-local working order, not a final global sequence.",
                "Global coverage, balance, cross-cluster overlap, and independent review remain open.",
            ],
        },
    }


def support_definition(
    index: dict[str, tuple[str, dict[str, Any]]],
    support_id: str,
    title: str,
    record_ids: list[str],
    candidate_ids: list[str],
) -> dict[str, Any]:
    refs = [
        evidence_ref(
            index, record_id, "cross_cutting", "full",
            "The passed CUR-006 audit assigns this record to concurrent support.",
        )
        for record_id in record_ids
    ]
    return {
        "support_id": support_id,
        "title": title,
        "evidence_refs": refs,
        "applies_to_candidate_ids": candidate_ids,
    }


def main() -> None:
    OUTPUT_PATH.write_text(
        json.dumps(build_map(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"WROTE {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
