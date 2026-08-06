"""Source-cited support dependencies for CUR-006."""

from __future__ import annotations

from typing import Any

try:
    from scripts.audit_model import CANDIDATE_ROLES, SUPPORT_NEEDS, record_ref
except ModuleNotFoundError:
    from audit_model import CANDIDATE_ROLES, SUPPORT_NEEDS, record_ref


def build_support_needs(
    candidate_map: dict[str, Any], records: dict[str, dict[str, Any]],
    dataset_by_id: dict[str, str],
) -> list[dict[str, Any]]:
    candidates = [
        cluster for cluster in candidate_map["clusters"]
        if cluster["role"] in CANDIDATE_ROLES
    ]
    results = []
    for need in SUPPORT_NEEDS:
        if need["target_rule"] == "all_candidate_units":
            targets = [cluster["cluster_id"] for cluster in candidates]
        else:
            targets = [
                cluster["cluster_id"] for cluster in candidates
                if any(
                    set(records[record_id]["interpretation"]["mode_codes"])
                    & {"interaction", "online_interaction"}
                    for record_id in cluster["record_ids"]
                )
            ]
        results.append({
            "need_id": need["need_id"],
            "support_cluster_id": need["support_cluster_id"],
            "summary": need["summary"],
            "target_cluster_ids": targets,
            "evidence_refs": [
                record_ref(records[record_id], dataset_by_id[record_id])
                for record_id in need["evidence_record_ids"]
            ],
        })
    return results


def build_prerequisite_audit(
    candidate_map: dict[str, Any], records: dict[str, dict[str, Any]],
    dataset_by_id: dict[str, str],
) -> dict[str, Any]:
    return {
        "strict_cluster_prerequisites": [],
        "support_needs": build_support_needs(candidate_map, records, dataset_by_id),
        "sequencing_status": "deferred_to_phase_3_lesson_normalization",
        "finding": (
            "No strict order among topical clusters is source-proven; language-control "
            "and repair support dependencies must remain explicit during sequencing."
        ),
    }
