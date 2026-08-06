"""Source-fidelity and coverage checks for A1 lesson maps."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable


TRACE_FIELDS = (
    "dataset_id", "source_id", "raw_file", "location", "source_text_sha256"
)
TAG_FIELDS = ("skill_codes", "mode_codes", "function_codes")
SUPPORT_CLUSTERS = {
    "support.basic_language_control": "language_foundations",
    "support.interaction_repair": "communication_strategies",
}


def candidate_refs(candidate: dict[str, Any]) -> Iterable[tuple[str, dict[str, Any]]]:
    for ref in candidate["evidence_refs"]:
        yield "evidence_refs", ref
    for family, targets in candidate["language_targets"].items():
        for target in targets:
            for ref in target["evidence_refs"]:
                yield f"language_targets.{family}", ref


def expected_trace(dataset_id: str, record: dict[str, Any]) -> dict[str, Any]:
    source = record["source"]
    return {
        "dataset_id": dataset_id,
        "source_id": source["source_id"],
        "raw_file": source["raw_file"],
        "location": source["location"],
        "source_text_sha256": source["source_text_sha256"],
    }


def check_ref(
    label: str,
    ref: dict[str, Any],
    index: dict[str, tuple[str, dict[str, Any]]],
) -> tuple[list[str], dict[str, Any] | None]:
    record_id = ref["record_id"]
    if record_id not in index:
        return [f"{label}: unknown evidence record {record_id}"], None
    dataset_id, record = index[record_id]
    errors = []
    for field, value in expected_trace(dataset_id, record).items():
        if ref[field] != value:
            errors.append(f"{label}: {record_id} {field} does not match reviewed source")
    if record["interpretation"]["inclusion_status"] != "included":
        errors.append(f"{label}: excluded record {record_id} cannot be used")
    return errors, record


def evidence_errors(
    lesson_map: dict[str, Any],
    index: dict[str, tuple[str, dict[str, Any]]],
) -> list[str]:
    errors: list[str] = []
    datasets = sorted({dataset_id for dataset_id, _ in index.values()})
    if sorted(lesson_map["evidence_dataset_ids"]) != datasets:
        errors.append("evidence_dataset_ids do not match reviewed source collections")

    used_ids: set[str] = set()
    full_anchors: dict[str, list[str]] = defaultdict(list)
    for candidate in lesson_map["candidates"]:
        candidate_id = candidate["candidate_id"]
        primary_ids = [ref["record_id"] for ref in candidate["evidence_refs"]]
        if len(primary_ids) != len(set(primary_ids)):
            errors.append(f"{candidate_id}: evidence_refs repeat a record id")
        supported_tags = {field: set() for field in TAG_FIELDS}
        for label, ref in candidate_refs(candidate):
            ref_label = f"{candidate_id}.{label}"
            ref_errors, record = check_ref(ref_label, ref, index)
            errors.extend(ref_errors)
            if record is None:
                continue
            if label != "evidence_refs" and ref["record_id"] not in primary_ids:
                errors.append(
                    f"{ref_label}: target evidence is absent from candidate evidence_refs"
                )
            if label == "evidence_refs":
                if ref["coverage"] != "context_only":
                    used_ids.add(ref["record_id"])
                for field in TAG_FIELDS:
                    supported_tags[field].update(record["interpretation"][field])
                if ref["role"] == "anchor" and ref["coverage"] == "full":
                    full_anchors[ref["record_id"]].append(candidate_id)
        for field in TAG_FIELDS:
            unsupported = set(candidate[field]) - supported_tags[field]
            if unsupported:
                errors.append(f"{candidate_id}: unsupported {field} {sorted(unsupported)}")

    errors.extend(_support_evidence_errors(lesson_map, index, used_ids))
    for record_id, candidate_ids in full_anchors.items():
        if len(set(candidate_ids)) > 1:
            errors.append(
                f"{record_id}: full anchor is duplicated across {sorted(set(candidate_ids))}"
            )
    if lesson_map["status"] == "approved":
        included = {
            record_id for record_id, (_, record) in index.items()
            if record["interpretation"]["inclusion_status"] == "included"
        }
        missing = sorted(included - used_ids)
        if missing:
            errors.append(f"approved map leaves included records uncovered: {missing}")
    return errors


def _support_evidence_errors(
    lesson_map: dict[str, Any],
    index: dict[str, tuple[str, dict[str, Any]]],
    used_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    for support in lesson_map["support_definitions"]:
        support_id = support["support_id"]
        ids = [ref["record_id"] for ref in support["evidence_refs"]]
        if len(ids) != len(set(ids)):
            errors.append(f"{support_id}: evidence_refs repeat a record id")
        for ref in support["evidence_refs"]:
            ref_errors, record = check_ref(f"{support_id}.evidence_refs", ref, index)
            errors.extend(ref_errors)
            if ref["role"] != "cross_cutting":
                errors.append(f"{support_id}: support evidence role must be cross_cutting")
            if ref["coverage"] == "context_only":
                errors.append(f"{support_id}: context-only evidence cannot define support")
            else:
                used_ids.add(ref["record_id"])
            expected_cluster = SUPPORT_CLUSTERS.get(support_id)
            if record is not None and expected_cluster is not None:
                clusters = record["interpretation"]["candidate_cluster_ids"]
                if expected_cluster not in clusters:
                    errors.append(
                        f"{support_id}: {ref['record_id']} is outside {expected_cluster}"
                    )
    return errors
