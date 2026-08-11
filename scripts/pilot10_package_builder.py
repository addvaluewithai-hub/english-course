from __future__ import annotations

import json
from pathlib import Path

from scripts.pilot10_package_contract import (
    ROOT,
    exact_records,
    input_records,
    lesson_contract,
    package_path,
    sha256,
)


def _curriculum_boundary(contract: dict, spec: dict) -> dict:
    roles = contract["exact_item_roles"]
    return {
        "introduce_item_ids": roles["introduce"],
        "fresh_recycle_item_ids": roles["fresh_recycle"],
        "consolidate_item_ids": roles["consolidate"],
        "bounded_scope_notes": spec["bounded_scope_notes"],
        "not_yet": spec["not_yet"],
    }


def _manifest(contract: dict, spec: dict) -> dict:
    return {
        "schema_version": 2,
        "lesson_id": contract["lesson_id"],
        "status": "pilot10_v1_qa_ready",
        "candidate_id": contract["final_owner_id"],
        "source_packet": "source-packet.json",
        "title": contract["title"],
        "goal": {"en": contract["outcome_statement"], "ar": spec["goal_ar"]},
        "learner": "Arabic-speaking adult beginner at A1",
        "scope": spec["scope"],
        "section_order": [
            "video_explanation",
            "applied_questions",
            "guided_practice",
            "ai_practice",
            "fresh_mastery",
            "teach_back_variant",
            "review",
        ],
        "video": {
            "provider": "Gemini TTS",
            "format": "bilingual_single_teacher_video",
            "directory": "video",
            "speaker_count": 1,
            "arabic_voice": "natural Egyptian Arabic",
            "english_pronunciation": "General American with inline SSML IPA",
            "interaction_during_video": False,
            "interaction_starts_after_video": True,
        },
        "variants": {
            "teach_back": spec["teach_back_summary"],
            "omit": "Matched close without teach-back.",
        },
        "non_goals": spec["non_goals"],
        "privacy": [
            "The learner may use fictional safe information.",
            "No microphone permission or raw-answer retention is required.",
        ],
        "accessibility": [
            "Every spoken model has visible text.",
            "All controls are keyboard reachable.",
            "Colour is never the only feedback signal.",
            "Arabic and English reading directions are explicit.",
        ],
        "unit_id": contract["unit_id"],
        "global_sequence_position": contract["global_sequence_position"],
        "scope_sequence_ref": "data/reviewed/a1-scope-and-sequence-v1.json",
        "pilot_release_ref": "data/reviewed/a1-first-10-lessons-pilot-v1.json",
        "prototype_lineage": contract["prototype_lineage"],
        "prerequisites": spec["prerequisites"],
        "curriculum_boundary": _curriculum_boundary(contract, spec),
    }


def _source_packet(contract: dict, spec: dict) -> dict:
    lineage_path = contract["prototype_lineage"].get("old_content_path")
    old_packet = ROOT / lineage_path / "source-packet.json" if lineage_path else None
    extra = (old_packet,) if old_packet and old_packet.is_file() else ()
    lineage = None
    if old_packet and old_packet.is_file():
        lineage = {
            "path": old_packet.relative_to(ROOT).as_posix(),
            "sha256": sha256(old_packet),
            "status": "traceable_prototype_input_not_automatically_accepted",
        }
    return {
        "schema_version": 2,
        "packet_id": f"a1.pilot10.{contract['lesson_id']}.sources",
        "lesson_id": contract["lesson_id"],
        "unit_id": contract["unit_id"],
        "candidate_id": contract["final_owner_id"],
        "inputs": input_records(extra),
        "outcome_statement": contract["outcome_statement"],
        "source_candidate_ids": contract["source_candidate_ids"],
        "prior_lesson_ids": spec["prerequisites"],
        "exact_introductions": exact_records(contract, "introduce"),
        "exact_recycles": exact_records(contract, "fresh_recycle"),
        "exact_consolidations": exact_records(contract, "consolidate"),
        "mastery": {
            "construct_id": spec["mastery"]["construct_id"],
            "fresh_task": spec["mastery"]["primary"]["prompt_en"],
            "support_boundary": spec["mastery"]["primary"]["support"],
            "critical_meaning": spec["mastery"]["critical_meaning"],
        },
        "prototype_lineage": lineage,
        "review": {
            "status": "accepted_for_pilot10_package_qa",
            "reviewer": "codex_primary_curriculum_agent",
            "reviewed_at": "2026-08-11",
        },
    }


def _content(contract: dict, spec: dict) -> dict:
    data = dict(spec["content"])
    alignment = _curriculum_boundary(contract, spec)
    alignment["target_coverage"] = spec["target_coverage"]
    data.update(
        {
            "schema_version": 2,
            "delivery": {
                "primary_explanation": "video/single-teacher",
                "scene": "video/scene.txt",
                "sample_context": "video/sample-context.txt",
                "transcript": "video/transcript.txt",
                "readable_equivalent": True,
                "interaction_starts_after_video": True,
            },
            "curriculum_alignment": alignment,
        }
    )
    return data


def _activities(spec: dict) -> dict:
    return {
        "schema_version": 2,
        "delivery": {
            "placement": "after_video_explanation",
            "interaction_during_video": False,
            "sequence": "comprehension_then_application_then_production",
        },
        "activities": spec["activities"],
        "curriculum_rule": "Application follows the video; mastery is a fresh unsupported task.",
    }


def build_outputs(spec: dict) -> dict[str, dict | str]:
    contract = lesson_contract(spec["lesson_id"])
    return {
        "lesson-manifest.json": _manifest(contract, spec),
        "source-packet.json": _source_packet(contract, spec),
        "content.json": _content(contract, spec),
        "activities.json": _activities(spec),
        "assessment.json": spec["assessment"],
        "ai-contract.json": spec["ai_contract"],
        "ASSET_BRIEFS.md": spec["asset_briefs"],
        "video/scene.txt": spec["scene"].rstrip() + "\n",
        "video/sample-context.txt": spec["sample_context"].rstrip() + "\n",
        "video/transcript.txt": spec["transcript"].rstrip() + "\n",
        "video/pronunciation-map.json": spec["pronunciation_map"],
        "video/README.md": spec["video_readme"],
    }


def write_package(spec: dict) -> Path:
    contract = lesson_contract(spec["lesson_id"])
    output = package_path(contract)
    for relative, value in build_outputs(spec).items():
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(value, dict):
            path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        else:
            path.write_text(value, encoding="utf-8")
    return output
