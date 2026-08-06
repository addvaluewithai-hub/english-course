"""Authoring helper for foundation and communication-strategy candidates."""

from __future__ import annotations

from typing import Any

try:
    from scripts.lesson_identity_spec_helpers import evidence, mastery, outcome
except ModuleNotFoundError:
    from lesson_identity_spec_helpers import evidence, mastery, outcome


REVIEWED_AT = "2026-07-17T23:53:24+03:00"


def foundation_spec(
    *, candidate_id: str, clusters: list[str], situation: str, action: str,
    content: str, success: str, statement: str,
    evidence_items: list[dict[str, str]], skill_codes: list[str],
    mode_codes: list[str], function_codes: list[str], rationale: str,
    fresh_task: str, level_2: dict[str, str], critical_failure: str,
    permitted_support: list[str], delayed_probe: str, scope_rationale: str,
    risks: list[str], basic_support_ids: list[str],
    independence: str = "without a complete model or answer-revealing cue",
) -> dict[str, Any]:
    return {
        "candidate_cluster_ids": clusters,
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
            ["Minor form errors that do not change the required meaning or action."],
            permitted_support,
            delayed_probe,
        ),
        "scope": ["focused", scope_rationale],
        "basic_support_ids": basic_support_ids,
        "risks": risks,
    }


__all__ = ["evidence", "foundation_spec"]
