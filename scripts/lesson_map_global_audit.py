"""Build the reviewed global audit for the in-progress A1 lesson map."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from typing import Any

try:
    from scripts.lesson_map_overlap_review import MASTERY_ALIGNMENT_DECISIONS, OVERLAP_DECISIONS
except ModuleNotFoundError:
    from lesson_map_overlap_review import MASTERY_ALIGNMENT_DECISIONS, OVERLAP_DECISIONS

REVIEWED_AT = "2026-07-19T01:13:48+03:00"


def canonical_hash(value: dict[str, Any]) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest().upper()


def build_global_audit(
    lesson_map: dict[str, Any],
    included_record_ids: set[str],
    relationship_review: dict[str, Any],
) -> dict[str, Any]:
    candidates = lesson_map["candidates"]
    candidate_refs = [ref for item in candidates for ref in item["evidence_refs"]]
    support_refs = [
        ref for support in lesson_map["support_definitions"]
        for ref in support["evidence_refs"]
    ]
    cited = {
        ref["record_id"] for ref in candidate_refs + support_refs
        if ref["coverage"] != "context_only"
    }
    shared: dict[str, list[str]] = defaultdict(list)
    for item in candidates:
        for ref in item["evidence_refs"]:
            if ref["coverage"] != "context_only":
                shared[ref["record_id"]].append(item["candidate_id"])
    shared = {key: value for key, value in shared.items() if len(value) > 1}
    mastery_alignment = _mastery_alignment_issues(candidates)
    target_gaps = [
        item["candidate_id"] for item in candidates
        if not any(item["language_targets"].values())
    ]
    error_gaps = [
        item["candidate_id"] for item in candidates if not item["error_hypotheses"]
    ]
    target_decisions_complete = not target_gaps and not error_gaps
    candidates_approved = all(
        item["status"] == "approved_candidate"
        and item["review"]["status"] == "accepted"
        for item in candidates
    )
    relation_counts = {
        key: sum(len(item["relationships"][key]) for item in candidates)
        for key in ("required_before", "helpful_before", "successors")
    }
    unresolved_overlap = [item for item in OVERLAP_DECISIONS if item[0].endswith("required")]
    return {
        "schema_version": 1,
        "audit_id": "a1_lesson_map_global_audit",
        "reviewed_at": REVIEWED_AT,
        "reviewer": "lesson_002_consolidated_approval",
        "map_sha256": canonical_hash(lesson_map),
        "coverage": {
            "included_records": len(included_record_ids),
            "cited_included_records": len(cited & included_record_ids),
            "orphan_record_ids": sorted(included_record_ids - cited),
            "candidate_references": len(candidate_refs),
            "support_references": len(support_refs),
            "shared_candidate_record_groups": len(shared),
        },
        "overlap_review": [
            {"status": status, "group_id": group_id, "candidate_ids": list(ids), "rationale": rationale}
            for status, group_id, ids, rationale in OVERLAP_DECISIONS
        ],
        "balance": {
            "candidate_count": len(candidates),
            "skill_candidate_counts": _tag_counts(candidates, "skill_codes"),
            "mode_candidate_counts": _tag_counts(candidates, "mode_codes"),
            "scope_counts": dict(sorted(Counter(item["scope"]["band"] for item in candidates).items())),
            "finding": "All four core skills are present; counts are source-led and not equal quotas.",
        },
        "relationships_and_sequence": {
            **relation_counts,
            "sequence_covers_every_candidate_once": len(lesson_map["sequence"]) == len(candidates) == len(set(lesson_map["sequence"])),
            "sequence_bands": relationship_review["counts"]["sequence_bands"],
            "review_id": relationship_review["review_id"],
            "status": relationship_review["status"],
            "source_proven_strict_order": relationship_review[
                "interpretation_boundary"
            ]["source_proven_strict_order"],
            "finding": (
                "The complete order is an accepted pedagogical hypothesis with hard and "
                "helpful links separated; it is not a source-proven topical or unit order."
            ),
        },
        "mastery": {
            "candidate_count": len(candidates),
            "alignment_issues": mastery_alignment,
            "alignment_decisions": list(MASTERY_ALIGNMENT_DECISIONS),
            "status": "needs_review" if mastery_alignment else "pass",
        },
        "approval": {
            "candidate_status_counts": dict(sorted(Counter(item["status"] for item in candidates).items())),
            "candidate_review_counts": dict(sorted(Counter(item["review"]["status"] for item in candidates).items())),
            "empty_language_target_candidate_ids": target_gaps,
            "empty_error_hypothesis_candidate_ids": error_gaps,
            "map_status": lesson_map["status"],
            "map_review_status": lesson_map["review"]["status"],
        },
        "decision": {
            "status": (
                "passed" if candidates_approved and lesson_map["status"] == "approved"
                else "approval_required" if target_decisions_complete
                else "remediation_required"
            ),
            "lesson_002_may_pass": (
                candidates_approved
                and lesson_map["status"] == "approved"
                and lesson_map["review"]["status"] == "accepted"
                and not mastery_alignment
                and not unresolved_overlap
                and not (included_record_ids - cited)
            ),
            "open_overlap_groups": len(unresolved_overlap),
            "next_partition": (
                "Select the gold lesson and assemble its source packet."
                if candidates_approved and lesson_map["status"] == "approved" else
                "Begin the separate candidate-approval audit with the nine foundational "
                "reception candidates now that every candidate has source-linked targets "
                "and an explicit labelled error decision."
                if target_decisions_complete else
                "Continue source-linked language targets and explicit labelled error "
                "decisions for the next coherent candidate subset before approval."
            ),
        },
    }


def _tag_counts(candidates: list[dict[str, Any]], field: str) -> dict[str, int]:
    return dict(sorted(Counter(tag for item in candidates for tag in item[field]).items()))


def _mastery_alignment_issues(candidates: list[dict[str, Any]]) -> list[dict[str, str]]:
    issues = []
    for item in candidates:
        modes = set(item["mode_codes"])
        dimensions = set(item["mastery"]["required_dimensions"])
        if "interaction" in modes and "control_or_repair" not in dimensions:
            issues.append({
                "candidate_id": item["candidate_id"],
                "issue": "Interaction is tagged but control_or_repair is not required; confirm non-applicability or revise the task.",
            })
    return issues
