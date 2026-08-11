from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = ROOT / "data/reviewed/a1-scope-and-sequence-v1.json"
INPUT_PATHS = (
    SCOPE_PATH,
    ROOT / "data/reviewed/a1-final-candidate-decisions-v1.json",
    ROOT / "data/reviewed/a1-grammar-coverage-ownership-v1.json",
    ROOT / "data/reviewed/a1-lexical-chunk-ownership-v1.json",
    ROOT / "data/reviewed/a1-pronunciation-ownership-v1.json",
)


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _item_roles(scope: dict, owner_id: str) -> dict[str, list[str]]:
    roles = {"introduce": [], "fresh_recycle": [], "consolidate": []}
    for placement in scope["exact_item_placements"]:
        if placement["final_introduction_location_id"] == owner_id:
            roles["introduce"].append(placement["item_id"])
        if placement["first_fresh_recycle_location_id"] == owner_id:
            roles["fresh_recycle"].append(placement["item_id"])
        if placement["consolidation_location_id"] == owner_id:
            roles["consolidate"].append(placement["item_id"])
    return roles


def _mapped_prerequisites(scope: dict, owner_id: str) -> list[dict]:
    return [
        {
            "owner_id": edge["before_owner_id"],
            "relationship": edge["relationship"],
        }
        for edge in scope["mapped_prerequisite_edges"]
        if edge["after_owner_id"] == owner_id
    ]


def build_release_contract() -> dict:
    scope = _read_json(SCOPE_PATH)
    ordered = sorted(
        (lesson for unit in scope["units"] for lesson in unit["lessons"]),
        key=lambda lesson: lesson["global_sequence_position"],
    )[:10]
    unit_by_lesson = {
        lesson["lesson_id"]: unit["unit_id"]
        for unit in scope["units"]
        for lesson in unit["lessons"]
    }
    lessons = []
    for lesson in ordered:
        lesson_id = lesson["lesson_id"]
        lessons.append(
            {
                "lesson_id": lesson_id,
                "global_sequence_position": lesson["global_sequence_position"],
                "unit_id": unit_by_lesson[lesson_id],
                "final_owner_id": lesson["final_owner_id"],
                "title": lesson["title"],
                "outcome_statement": lesson["outcome_statement"],
                "mastery_action": lesson["mastery_action"],
                "source_candidate_ids": lesson["source_candidate_ids"],
                "content_path": lesson["planned_content_path"],
                "prototype_lineage": lesson["prototype_lineage"],
                "mapped_prerequisites": _mapped_prerequisites(
                    scope, lesson["final_owner_id"]
                ),
                "exact_item_roles": _item_roles(scope, lesson["final_owner_id"]),
                "production_requirement": (
                    "preserve_accepted_gold_and_validate_against_batch_contract"
                    if lesson_id == "U1-L03"
                    else "author_final_pilot_package"
                ),
            }
        )
    role_counts = {
        role: sum(len(lesson["exact_item_roles"][role]) for lesson in lessons)
        for role in ("introduce", "fresh_recycle", "consolidate")
    }
    return {
        "schema_version": 1,
        "release_id": "a1.first_10_lessons.pilot_v1",
        "status": "locked_for_content_production",
        "owner_decision": "Produce and evaluate the actual first ten final lessons, not a detached showcase set.",
        "inputs": [
            {"path": _relative(path), "sha256": _sha256(path)}
            for path in INPUT_PATHS
        ],
        "policy": {
            "scope_sequence": "locked A1 v1 positions 1-10",
            "composition": "all nine Unit 1 lessons followed by Unit 2 Lesson 1",
            "delivery": "single-teacher bilingual explanation video; application starts after video",
            "english_voice_markup": "every spoken English span requires en-US SSML and IPA",
            "mastery": "fresh performance; completion and coached practice never imply mastery",
            "pilot_question": "Does the teaching design work across progression, recycling, review, and transition—not only in one gold lesson?",
            "downstream_gate": "Reusable system and architecture decisions remain after the ten-lesson learner pilot.",
        },
        "lessons": lessons,
        "audit": {
            "lesson_count": len(lessons),
            "unit1_lesson_count": sum(x["unit_id"].startswith("a1.unit01") for x in lessons),
            "unit2_lesson_count": sum(x["unit_id"].startswith("a1.unit02") for x in lessons),
            "global_positions": [x["global_sequence_position"] for x in lessons],
            "lesson_ids": [x["lesson_id"] for x in lessons],
            "exact_item_role_counts": role_counts,
            "duplicate_owner_count": len(lessons)
            - len({x["final_owner_id"] for x in lessons}),
        },
        "review": {
            "status": "approved_for_pilot_content_production",
            "reviewer": "codex_primary_curriculum_agent",
            "reviewed_at": "2026-08-11",
        },
    }
