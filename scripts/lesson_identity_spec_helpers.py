"""Concise authoring helpers for the identity lesson-candidate partition."""

from __future__ import annotations

from typing import Any


def outcome(
    situation: str,
    action: str,
    content: str,
    independence: str,
    success: str,
    statement: str,
) -> dict[str, str]:
    return {
        "situation": situation,
        "observable_action": action,
        "essential_content": content,
        "independence": independence,
        "success_condition": success,
        "statement": statement,
    }


def evidence(
    record_id: str,
    role: str,
    note: str,
    coverage: str = "full",
) -> dict[str, str]:
    return {
        "record_id": record_id,
        "role": role,
        "coverage": coverage,
        "interpretation_note": note,
    }


def mastery(
    task_family: str,
    level_2_evidence: dict[str, str],
    critical_failures: list[str],
    non_blocking_errors: list[str],
    permitted_support: list[str],
    delayed_probe: str,
    disallowed_help: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "fresh_task_family": task_family,
        "required_dimensions": list(level_2_evidence),
        "level_2_evidence": level_2_evidence,
        "critical_failures": critical_failures,
        "non_blocking_errors": non_blocking_errors,
        "permitted_support": permitted_support,
        "disallowed_help": disallowed_help or [
            "A complete model answer or answer-revealing cue."
        ],
        "delayed_probe": delayed_probe,
    }


BASIC_WRITTEN = [
    "cefr.cv2020.p131.general_linguistic_range.01",
    "cefr.cv2020.p132.grammatical_accuracy.01",
    "cefr.cv2020.p136.orthographic_control.02",
]
BASIC_SPOKEN = [
    "cefr.cv2020.p131.general_linguistic_range.01",
    "cefr.cv2020.p132.grammatical_accuracy.01",
    "cefr.cv2020.p135.overall_phonological_control.01",
]
BASIC_RECEPTIVE = [
    "cefr.cv2020.p131.general_linguistic_range.01",
]
