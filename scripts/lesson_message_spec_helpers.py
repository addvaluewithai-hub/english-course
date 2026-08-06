"""Authoring helper for the messages, signs, and forms partition."""

from __future__ import annotations

from typing import Any

try:
    from scripts.lesson_identity_spec_helpers import evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import evidence, mastery, outcome


REVIEWED_AT = "2026-07-17T21:52:40+03:00"
MESSAGE_CLUSTER = ["messages_signs_forms"]


def message_spec(
    *, candidate_id: str, situation: str, action: str, content: str,
    success: str, statement: str, evidence_items: list[dict[str, str]],
    skill_codes: list[str], mode_codes: list[str], function_codes: list[str],
    rationale: str, fresh_task: str, level_2: dict[str, str],
    critical_failure: str, permitted_support: list[str], delayed_probe: str,
    scope_rationale: str, risks: list[str], basic_support_ids: list[str],
    scope_band: str = "focused", clusters: list[str] | None = None,
    independence: str = "without a complete model or answer-revealing cue",
) -> dict[str, Any]:
    """Create one focused, provisional message/sign candidate specification."""
    return {
        "candidate_cluster_ids": clusters or MESSAGE_CLUSTER,
        "reviewed_at": REVIEWED_AT,
        "candidate_id": candidate_id,
        "outcome": outcome(
            situation, action, content, independence, success, statement,
        ),
        "evidence": evidence_items,
        "skill_codes": skill_codes,
        "mode_codes": mode_codes,
        "function_codes": function_codes,
        "normalization_rationale": rationale,
        "mastery": mastery(
            fresh_task,
            level_2,
            [critical_failure],
            ["Minor form errors that preserve the intended practical meaning."],
            permitted_support,
            delayed_probe,
        ),
        "scope": [scope_band, scope_rationale],
        "basic_support_ids": basic_support_ids,
        "risks": risks,
    }


__all__ = ["evidence", "message_spec"]
