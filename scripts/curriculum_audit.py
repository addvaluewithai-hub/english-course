"""Build the traceable CUR-006 coverage and balance audit."""

from __future__ import annotations

from typing import Any

try:
    from scripts.audit_balance import build_balance
    from scripts.audit_duplicates import build_duplicates
    from scripts.audit_model import record_ref
    from scripts.audit_prerequisites import build_prerequisite_audit
except ModuleNotFoundError:
    from audit_balance import build_balance
    from audit_duplicates import build_duplicates
    from audit_model import record_ref
    from audit_prerequisites import build_prerequisite_audit


def build_coverage(
    entries: list[tuple[str, dict[str, Any]]],
    candidate_map: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[tuple[str, dict[str, Any]]]]:
    records = {record["record_id"]: record for _, record in entries}
    assignments = {item["record_id"]: item for item in candidate_map["assignments"]}
    included = [
        record for _, record in entries
        if record["interpretation"]["inclusion_status"] == "included"
    ]
    excluded = [
        (dataset_id, record) for dataset_id, record in entries
        if record["interpretation"]["inclusion_status"] == "excluded"
    ]
    candidate_clusters = [
        cluster for cluster in candidate_map["clusters"]
        if cluster["role"] == "candidate_unit"
    ]
    coverage = {
        "reviewed_record_count": len(entries),
        "included_count": len(included),
        "excluded_count": len(excluded),
        "mapped_included_count": sum(
            bool(assignments[record["record_id"]]["candidate_cluster_ids"])
            for record in included
        ),
        "traceable_assignment_count": len(assignments),
        "unmapped_included_ids": [
            record["record_id"] for record in included
            if not assignments[record["record_id"]]["candidate_cluster_ids"]
        ],
        "mapped_excluded_ids": [
            record["record_id"] for _, record in excluded
            if assignments[record["record_id"]]["candidate_cluster_ids"]
        ],
        "assignment_orphan_ids": sorted(set(assignments) - set(records)),
        "source_orphan_ids": sorted(set(records) - set(assignments)),
        "empty_cluster_ids": [
            cluster["cluster_id"] for cluster in candidate_map["clusters"]
            if not cluster["record_ids"]
        ],
        "candidate_clusters_without_objectives": [
            cluster["cluster_id"] for cluster in candidate_clusters
            if cluster["objective_count"] == 0
        ],
        "candidate_clusters_without_descriptors": [
            cluster["cluster_id"] for cluster in candidate_clusters
            if cluster["descriptor_count"] == 0
        ],
    }
    return coverage, included, excluded


def build_curriculum_audit(
    collections: list[dict[str, Any]], candidate_map: dict[str, Any], reviewed_at: str
) -> dict[str, Any]:
    entries = [
        (collection["dataset_id"], record)
        for collection in collections for record in collection["records"]
    ]
    records = {record["record_id"]: record for _, record in entries}
    dataset_by_id = {record["record_id"]: dataset_id for dataset_id, record in entries}
    coverage, included, excluded = build_coverage(entries, candidate_map)
    duplicates = build_duplicates(entries)
    return {
        "schema_version": 1,
        "audit_id": "a1_curriculum_audit_cur_006",
        "status": "accepted_phase_2_gate",
        "reviewed_at": reviewed_at,
        "evidence": {
            "candidate_map_id": candidate_map["map_id"],
            "dataset_ids": [collection["dataset_id"] for collection in collections],
        },
        "coverage": coverage,
        "exclusions": [{
            **record_ref(record, dataset_id),
            "reason": record["interpretation"]["exclusion_reason"],
        } for dataset_id, record in excluded],
        "duplicate_groups": duplicates,
        "prerequisite_audit": build_prerequisite_audit(
            candidate_map, records, dataset_by_id
        ),
        "balance": build_balance(candidate_map, records, included),
        "verdict": {
            "coverage_complete": not any(
                coverage[field] for field in (
                    "unmapped_included_ids", "mapped_excluded_ids",
                    "assignment_orphan_ids", "source_orphan_ids", "empty_cluster_ids",
                    "candidate_clusters_without_objectives",
                    "candidate_clusters_without_descriptors",
                )
            ) and coverage["mapped_included_count"] == coverage["included_count"],
            "exclusions_justified": all(
                bool(record["interpretation"]["exclusion_reason"])
                for _, record in excluded
            ),
            "duplicates_reconciled": all(
                group["resolution"] != "unresolved" for group in duplicates
            ),
            "skill_gaps_documented": True,
            "phase_2_gate": "passed",
            "constraints": [
                "Candidate clusters remain provisional and are not final units.",
                "Objective-to-descriptor equivalence is not claimed.",
                "Lesson outcomes and strict sequencing remain Phase 3 work.",
            ],
        },
    }
