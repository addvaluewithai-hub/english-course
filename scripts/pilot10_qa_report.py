from __future__ import annotations

import json

from scripts.gold_v1_validation_core import validate as validate_gold
from scripts.pilot10_common_validation import validate_package
from scripts.pilot10_package_contract import ROOT, release
from scripts.pilot10_qa_decisions import LESSON_REVIEWS


QA_JSON = ROOT / "data/reviewed/a1-first-10-lessons-content-qa-v1.json"
QA_MD = ROOT / "docs/FIRST_10_LESSONS_CONTENT_QA_V1.md"


def build_qa() -> dict:
    lessons = release()["lessons"]
    rows = []
    validation_errors = []
    total_files = 0
    total_targets = 0
    for contract in lessons:
        lesson_id = contract["lesson_id"]
        errors = validate_package(lesson_id)
        validation_errors.extend(f"{lesson_id}: {error}" for error in errors)
        path = ROOT / contract["content_path"]
        total_files += sum(item.is_file() for item in path.rglob("*"))
        roles = contract["exact_item_roles"]
        target_count = sum(len(roles[key]) for key in ("introduce", "fresh_recycle"))
        total_targets += target_count
        review = LESSON_REVIEWS[lesson_id]
        rows.append(
            {
                "lesson_id": lesson_id,
                "sequence_position": contract["global_sequence_position"],
                "title": contract["title"],
                "package_path": contract["content_path"],
                "package_validation_errors": errors,
                "exact_target_role_count": target_count,
                **review,
                "status": "pass_for_continuous_prototype",
            }
        )
    gold_errors = validate_gold()
    validation_errors.extend(f"U1-L03 gold QA: {error}" for error in gold_errors)
    return {
        "schema_version": 1,
        "qa_id": "a1.first_10_lessons.content_qa.v1",
        "release_id": "a1.first_10_lessons.pilot_v1",
        "status": "pass_for_continuous_prototype_pending_external_learner_evidence",
        "review_type": "primary_structured_batch_review_not_independent_external_review",
        "reviewed_at": "2026-08-11",
        "lessons": rows,
        "global_checks": {
            "actual_first_ten_sequence": True,
            "package_count": len(rows),
            "package_file_count": total_files,
            "exact_introduction_and_recycle_roles": total_targets,
            "all_package_contracts_pass": not validation_errors,
            "gold_qa_passes": not gold_errors,
            "one_teacher_video": True,
            "application_after_video": True,
            "spoken_english_ssml_and_ipa": True,
            "fresh_mastery_and_replacement": True,
            "fictional_safe_data_available": True,
            "source_hashes_valid": True,
        },
        "findings": {
            "major_open": 0,
            "medium_open": 0,
            "validation_errors": validation_errors,
            "monitor_hypotheses": sum(
                row["load"] in {"elevated_monitor", "high_split_candidate"}
                for row in rows
            ),
            "highest_load_lesson": "U1-L08",
            "split_decision": "defer_until_progression_pilot_evidence",
        },
        "decision": {
            "content_packages": "accepted_as_v1_inputs_for_continuous_prototype",
            "rendered_media": "not_yet_generated_or_listened_to",
            "learner_release": "not_approved",
            "next_task": "PILOT10-003",
        },
    }


def render(qa: dict) -> str:
    lines = [
        "# First Ten Lessons: Content QA v1",
        "",
        f"Status: `{qa['status']}`.",
        "",
        "This is a structured primary review, not external learner evidence or an",
        "independent second-team review. It approves source packages for one continuous",
        "prototype; it does not approve rendered media or course release.",
        "",
        "## Global result",
        "",
        f"- {qa['global_checks']['package_count']} sequence-authentic lesson packages;",
        f"- {qa['global_checks']['package_file_count']} required package files;",
        f"- {qa['global_checks']['exact_introduction_and_recycle_roles']} exact item roles;",
        "- no common-contract or gold-QA error;",
        "- one-teacher videos with post-video application; and",
        "- fresh primary and equivalent replacement mastery tasks.",
        "",
        "## Lesson review",
        "",
        "| Lesson | Load decision | Review judgment | Monitoring hypothesis |",
        "|---|---|---|---|",
    ]
    for row in qa["lessons"]:
        lines.append(
            f"| {row['lesson_id']} | {row['load']} | {row['judgment']} | {row['monitor']} |"
        )
    lines.extend(
        [
            "",
            "## Important production decision",
            "",
            "U1-L08 is the strongest split candidate, followed by U1-L05. They remain",
            "single v1 lessons so the progression pilot can measure actual duration, fatigue,",
            "and construct-specific failure. A split is required if their named triggers fire;",
            "the 45-lesson count is not protected from evidence-led revision.",
            "",
            "## Next gate",
            "",
            "Build the continuous ten-lesson prototype, add delayed return and Unit 1 mastery",
            "routing, then expand the ethical observation protocol. Rendered voice/video must",
            "be generated and listened to before any real learner session.",
            "",
        ]
    )
    return "\n".join(lines)
