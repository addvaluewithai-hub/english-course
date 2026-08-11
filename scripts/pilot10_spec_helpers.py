from __future__ import annotations


COMMON_AI_BEHAVIOR = [
    "Ask one question at a time.",
    "Accept safe fictional information without challenge.",
    "Ignore harmless hesitation when meaning is clear.",
    "Correct at most one important issue per turn.",
    "Prefer a neutral clarification signal before giving a correction.",
    "Require one retry after an important correction.",
    "Never claim mastery from the coached attempt.",
]


def assessment(
    lesson_id: str,
    mastery: dict,
    rubric_level_2: dict[str, str],
    teach_back_prompt_ar: str,
    delayed_review: list[dict],
) -> dict:
    primary = dict(mastery["primary"])
    replacement = dict(mastery["replacement"])
    primary["construct_id"] = mastery["construct_id"]
    replacement["construct_id"] = mastery["construct_id"]
    return {
        "schema_version": 2,
        "lesson_id": lesson_id,
        "mastery_task": primary,
        "replacement_mastery_task": replacement,
        "rubric": [
            {"dimension": dimension, "level_2": text}
            for dimension, text in rubric_level_2.items()
        ],
        "decision": {
            "demonstrated": "Level 2 or above on every required dimension.",
            "needs_review": "Any required dimension below level 2; use targeted practice and a new task.",
            "completion_rule": "Opening sections or finishing exercises never grants mastery.",
        },
        "teach_back_variant": {
            "position": "after the fresh performance",
            "prompt_ar": teach_back_prompt_ar,
            "scored_separately": True,
            "cannot_rescue_failed_mastery": True,
        },
        "omit_variant": {
            "position": "after the fresh performance",
            "content": "Proceed directly to the matched close and review card.",
        },
        "delayed_review": delayed_review,
        "mastery_attempt_policy": {
            "maximum_fresh_attempts": 2,
            "replacement_required_after_answer_revealing_help": True,
            "second_failure_result": "practiced_or_needs_review_not_demonstrated",
        },
    }


def ai_contract(
    lesson_id: str,
    goal: str,
    opening_en: str,
    opening_ar: str,
    priority_errors: list[str],
    curriculum_limits: list[str],
    turn_limit: int = 6,
) -> dict:
    return {
        "schema_version": 2,
        "lesson_id": lesson_id,
        "role": "bounded A1 coach",
        "goal": goal,
        "turn_limit": turn_limit,
        "opening": {"en": opening_en, "ar_support": opening_ar},
        "behavior": list(COMMON_AI_BEHAVIOR),
        "feedback_order": [
            "Name the successful communicative action.",
            "Quote only the important problem.",
            "Give one natural correction or repair cue.",
            "Explain briefly in Modern Standard Arabic.",
            "Ask for a retry.",
        ],
        "priority_errors": priority_errors,
        "ending": "Elicit one final changed coached attempt, then close without assigning mastery.",
        "prototype_limit": "The pilot may use deterministic checks; no coached result assigns mastery.",
        "curriculum_limits": curriculum_limits,
    }


def video_readme(lesson_id: str, title: str) -> str:
    return f"""# Video source — {lesson_id}: {title}

1. Paste `scene.txt` into Scene.
2. Paste `sample-context.txt` into Sample Context.
3. Paste `transcript.txt` into Text.
4. Assign one warm Arabic-capable voice to Speaker 1.

The video contains explanation and models only. Application begins after it.

Every spoken English span has `en-US` plus IPA markup. Markup and bracketed direction
must remain silent. Reject a take if English is read with Arabic phonology after the
code-switch, if wording is skipped, or if the teacher sounds theatrical or childish.

Use natural Egyptian Arabic. Avoid artificial case-ending tanween in conversation;
retain established natural forms such as `مثلًا`.
"""
