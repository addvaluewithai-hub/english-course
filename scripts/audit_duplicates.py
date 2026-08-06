"""Repeated-source-wording reconciliation for CUR-006."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

try:
    from scripts.audit_model import duplicate_group_id, normalized_text, record_ref
except ModuleNotFoundError:
    from audit_model import duplicate_group_id, normalized_text, record_ref


def build_duplicates(
    entries: list[tuple[str, dict[str, Any]]]
) -> list[dict[str, Any]]:
    groups: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for dataset_id, record in entries:
        groups[normalized_text(record["source"]["source_text"])].append(
            (dataset_id, record)
        )

    results = []
    for text, group in sorted(groups.items()):
        if len(group) < 2:
            continue
        included = [
            (dataset_id, record) for dataset_id, record in group
            if record["interpretation"]["inclusion_status"] == "included"
        ]
        excluded = [
            record for _, record in group
            if record["interpretation"]["inclusion_status"] == "excluded"
        ]
        scales = {record["source_facts"]["scale_text"] for _, record in group}
        if excluded and len(included) == 1:
            resolution = "exclude_repeated_source_row"
            canonical_id = included[0][1]["record_id"]
            rationale = "One canonical included record; repeated source row retained as evidence."
        elif not excluded and len(scales) == len(group):
            resolution = "retain_distinct_scale_placements"
            canonical_id = None
            rationale = "Identical published wording serves distinct CEFR scale contexts."
        else:
            resolution = "unresolved"
            canonical_id = None
            rationale = "Repeated wording requires manual reconciliation."
        results.append({
            "group_id": duplicate_group_id(text),
            "record_refs": [record_ref(record, dataset_id) for dataset_id, record in group],
            "resolution": resolution,
            "canonical_record_id": canonical_id,
            "rationale": rationale,
        })
    return results
