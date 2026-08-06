"""Apply candidate clusters while preserving curriculum source evidence."""

from __future__ import annotations

import copy
from typing import Any

try:
    from scripts.cluster_rules import choose_candidate_clusters
except ModuleNotFoundError:
    from cluster_rules import choose_candidate_clusters


def cluster_record(record: dict[str, Any]) -> dict[str, Any]:
    clustered = copy.deepcopy(record)
    clustered["interpretation"]["candidate_cluster_ids"] = choose_candidate_clusters(record)
    return clustered


def cluster_collection(
    collection: dict[str, Any], *, reviewer: str | None = None, reviewed_at: str | None = None
) -> dict[str, Any]:
    """Return a clustered collection with optional paired review metadata."""
    if (reviewer is None) != (reviewed_at is None):
        raise ValueError("reviewer and reviewed_at are required together")
    clustered = copy.deepcopy(collection)
    clustered["records"] = [cluster_record(record) for record in collection["records"]]
    for record in clustered["records"]:
        included = record["interpretation"]["inclusion_status"] == "included"
        cluster_ids = record["interpretation"]["candidate_cluster_ids"]
        if included and not cluster_ids:
            raise ValueError(f"Included record is unmapped: {record['record_id']}")
        if not included and cluster_ids:
            raise ValueError(f"Excluded record is mapped: {record['record_id']}")
        if reviewer:
            record["review"].update(
                {"status": "accepted", "reviewer": reviewer, "reviewed_at": reviewed_at}
            )
    return clustered
