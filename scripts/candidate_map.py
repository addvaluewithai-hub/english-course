"""Build the traceable candidate unit-map artifact from clustered records."""

from __future__ import annotations

from collections import Counter
from typing import Any

try:
    from scripts.cluster_model import CLUSTERS, CLUSTER_BY_ID
except ModuleNotFoundError:
    from cluster_model import CLUSTERS, CLUSTER_BY_ID


PRIOR_UNITS = (
    "Identity", "People & Relationships", "Everyday Life", "Places & Movement",
    "Needs & Transactions", "Simple Communication", "Reading, Signs & Forms",
)


def mapping_fit(cluster_ids: list[str], included: bool) -> str:
    if not included:
        return "explicit_exclusion"
    roles = {CLUSTER_BY_ID[value].role for value in cluster_ids}
    if roles == {"cross_cutting_support"}:
        return "cross_cutting"
    if "cross_cutting_support" in roles:
        return "natural_with_support"
    return "natural"


def prior_fit(cluster_ids: list[str], included: bool) -> str:
    if not included:
        return "not_applicable"
    fits = {CLUSTER_BY_ID[value].prior_fit for value in cluster_ids}
    if "forced" in fits:
        return "forced"
    if "overlap" in fits:
        return "overlap"
    return "natural"


def assignment(record: dict[str, Any], dataset_id: str) -> dict[str, Any]:
    interpretation = record["interpretation"]
    included = interpretation["inclusion_status"] == "included"
    cluster_ids = interpretation["candidate_cluster_ids"]
    source = record["source"]
    return {
        "record_id": record["record_id"],
        "record_kind": record["record_kind"],
        "dataset_id": dataset_id,
        "source_id": source["source_id"],
        "raw_file": source["raw_file"],
        "location": source["location"],
        "source_text_sha256": source["source_text_sha256"],
        "candidate_cluster_ids": cluster_ids,
        "mapping_fit": mapping_fit(cluster_ids, included),
        "prior_seven_unit_fit": prior_fit(cluster_ids, included),
    }


def build_candidate_map(collections: list[dict[str, Any]], reviewed_at: str) -> dict[str, Any]:
    assignments = [
        assignment(record, collection["dataset_id"])
        for collection in collections
        for record in collection["records"]
    ]
    fit_counts = Counter(item["mapping_fit"] for item in assignments)
    prior_counts = Counter(item["prior_seven_unit_fit"] for item in assignments)
    objective_prior_counts = Counter(
        item["prior_seven_unit_fit"] for item in assignments
        if item["record_kind"] == "objective"
    )
    descriptor_prior_counts = Counter(
        item["prior_seven_unit_fit"] for item in assignments
        if item["record_kind"] == "descriptor"
    )

    cluster_rows = []
    for cluster in CLUSTERS:
        matching = [
            item for item in assignments
            if cluster.cluster_id in item["candidate_cluster_ids"]
        ]
        kinds = Counter(item["record_kind"] for item in matching)
        cluster_rows.append({
            "cluster_id": cluster.cluster_id,
            "title": cluster.title,
            "role": cluster.role,
            "goal": cluster.goal,
            "prior_unit": cluster.prior_unit,
            "prior_fit": cluster.prior_fit,
            "assignment_count": len(matching),
            "objective_count": kinds["objective"],
            "descriptor_count": kinds["descriptor"],
            "record_ids": [item["record_id"] for item in matching],
        })

    return {
        "schema_version": 1,
        "map_id": "a1_candidate_unit_map_cur_005",
        "status": "candidate_not_final",
        "reviewed_at": reviewed_at,
        "evidence_dataset_ids": [item["dataset_id"] for item in collections],
        "prior_proposal_test": {
            "proposed_units": list(PRIOR_UNITS),
            "verdict": "not_supported_as_an_exact_final_map",
            "fit_counts": dict(sorted(prior_counts.items())),
            "objective_fit_counts": dict(sorted(objective_prior_counts.items())),
            "descriptor_fit_counts": dict(sorted(descriptor_prior_counts.items())),
            "findings": [
                "Home, objects, and descriptions overlaps earlier topic boundaries.",
                "Reading, Signs & Forms mixes a channel with several communicative purposes.",
                "Simple Communication absorbs distinct social, repair, mediation, and language-control evidence.",
                "Cross-cutting support should not be forced into standalone topical units.",
            ],
        },
        "coverage": {
            "record_count": len(assignments),
            "included_count": sum(item["mapping_fit"] != "explicit_exclusion" for item in assignments),
            "excluded_count": fit_counts["explicit_exclusion"],
            "mapping_fit_counts": dict(sorted(fit_counts.items())),
        },
        "clusters": cluster_rows,
        "assignments": assignments,
    }
