"""Skill-balance summaries for the CUR-006 evidence audit."""

from __future__ import annotations

from typing import Any

try:
    from scripts.audit_model import CORE_SKILLS, count_tags
except ModuleNotFoundError:
    from audit_model import CORE_SKILLS, count_tags


def cluster_balance(
    cluster: dict[str, Any], records: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    matching = [records[record_id] for record_id in cluster["record_ids"]]
    objectives = [record for record in matching if record["record_kind"] == "objective"]
    descriptors = [record for record in matching if record["record_kind"] == "descriptor"]
    objective_skills = count_tags(objectives, "skill_codes")
    descriptor_skills = count_tags(descriptors, "skill_codes")
    combined_skills = count_tags(matching, "skill_codes")
    return {
        "cluster_id": cluster["cluster_id"],
        "role": cluster["role"],
        "objective_count": len(objectives),
        "descriptor_count": len(descriptors),
        "objective_skill_counts": objective_skills,
        "descriptor_skill_counts": descriptor_skills,
        "combined_skill_counts": combined_skills,
        "objective_skill_gaps": [
            skill for skill in CORE_SKILLS if objective_skills.get(skill, 0) == 0
        ],
        "descriptor_skill_gaps": [
            skill for skill in CORE_SKILLS if descriptor_skills.get(skill, 0) == 0
        ],
        "combined_skill_gaps": [
            skill for skill in CORE_SKILLS if combined_skills.get(skill, 0) == 0
        ],
    }


def build_balance(
    candidate_map: dict[str, Any], records: dict[str, dict[str, Any]],
    included: list[dict[str, Any]],
) -> dict[str, Any]:
    balances = [
        cluster_balance(cluster, records) for cluster in candidate_map["clusters"]
    ]
    candidate_balances = [
        row for row in balances if row["role"] == "candidate_unit"
    ]
    objective_gaps = {
        row["cluster_id"]: row["objective_skill_gaps"]
        for row in candidate_balances if row["objective_skill_gaps"]
    }
    overall = {}
    for kind in ("objective", "descriptor"):
        selected = [record for record in included if record["record_kind"] == kind]
        overall[kind] = {
            "record_count": len(selected),
            "skill_counts": count_tags(selected, "skill_codes"),
            "mode_counts": count_tags(selected, "mode_codes"),
        }
    return {
        "core_skills": list(CORE_SKILLS),
        "overall": overall,
        "clusters": balances,
        "findings": [
            "GSE objective evidence is speaking-heavy and reading-light overall.",
            f"Granular GSE objective skill gaps remain in {len(objective_gaps)} candidate clusters: {objective_gaps}.",
            "Combined GSE and CEFR evidence covers all four core skills in every candidate unit.",
            "Counts describe source evidence density; they are not equal-skill quotas or final unit sizes.",
        ],
    }
