"""Apply and review the A1 pedagogical sequence and candidate relationships."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

try:
    from scripts.create_lesson_overlap_partition import build_map as build_overlap_map
    from scripts.lesson_relationship_specs import HELPFUL_LINKS, REQUIRED_LINKS
    from scripts.lesson_sequence_specs import SEQUENCE_BANDS, reviewed_sequence
except ModuleNotFoundError:
    from create_lesson_overlap_partition import build_map as build_overlap_map
    from lesson_relationship_specs import HELPFUL_LINKS, REQUIRED_LINKS
    from lesson_sequence_specs import SEQUENCE_BANDS, reviewed_sequence


REVIEWED_AT = "2026-07-18T02:54:10+03:00"
REVIEWER = "lesson_002_primary"


def build_map() -> dict[str, Any]:
    """Return the overlap-remediated map with the reviewed relationship model."""
    lesson_map = deepcopy(build_overlap_map())
    candidates = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    sequence = reviewed_sequence()
    if set(sequence) != set(candidates) or len(sequence) != len(candidates):
        raise ValueError("reviewed sequence must cover every candidate exactly once")
    lesson_map["sequence"] = sequence
    for candidate in candidates.values():
        relationships = candidate["relationships"]
        relationships["required_before"] = []
        relationships["helpful_before"] = []
        relationships["successors"] = []
        candidate["review"] = {
            "status": "needs_review",
            "reviewer": REVIEWER,
            "reviewed_at": REVIEWED_AT,
            "issues": [
                "Relationship and sequence review is complete; language targets, labelled error decisions, and candidate approval remain open."
            ],
        }
    for prerequisite_id, target_id, rationale in REQUIRED_LINKS:
        evidence = _link_evidence(candidates, prerequisite_id, target_id)
        candidates[target_id]["relationships"]["required_before"].append(
            _relation(prerequisite_id, rationale, evidence)
        )
        candidates[prerequisite_id]["relationships"]["successors"].append(
            _relation(target_id, rationale, evidence)
        )
    for prerequisite_id, target_id, rationale in HELPFUL_LINKS:
        evidence = _link_evidence(candidates, prerequisite_id, target_id)
        candidates[target_id]["relationships"]["helpful_before"].append(
            _relation(prerequisite_id, rationale, evidence)
        )
    lesson_map["review"] = {
        "status": "needs_review",
        "reviewer": REVIEWER,
        "reviewed_at": REVIEWED_AT,
        "issues": [
            "The reviewed pedagogical sequence and typed relationship model are complete.",
            "Language targets, labelled error decisions, and candidate approval remain open.",
        ],
    }
    return lesson_map


def build_review(lesson_map: dict[str, Any] | None = None) -> dict[str, Any]:
    """Build the reviewed interpretation artifact tied to the resulting map."""
    lesson_map = lesson_map or build_map()
    candidates = {item["candidate_id"]: item for item in lesson_map["candidates"]}
    return {
        "schema_version": 1,
        "review_id": "a1_lesson_relationship_sequence_review",
        "reviewed_at": REVIEWED_AT,
        "reviewer": REVIEWER,
        "status": "accepted",
        "interpretation_boundary": {
            "source_proven_strict_order": False,
            "unit_boundaries_defined": False,
            "statement": (
                "The order is a reviewed pedagogical hypothesis. Source records support "
                "the abilities but do not prove a strict topical or unit sequence."
            ),
        },
        "sequence_bands": deepcopy(SEQUENCE_BANDS),
        "required_links": [
            _review_link(candidates, *spec) for spec in REQUIRED_LINKS
        ],
        "helpful_links": [
            _review_link(candidates, *spec) for spec in HELPFUL_LINKS
        ],
        "counts": {
            "candidates": len(candidates),
            "sequence_bands": len(SEQUENCE_BANDS),
            "required_before": len(REQUIRED_LINKS),
            "helpful_before": len(HELPFUL_LINKS),
            "successors": len(REQUIRED_LINKS),
        },
    }


def _relation(candidate_id: str, rationale: str, evidence: list[str]) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "rationale": rationale,
        "evidence_record_ids": evidence,
    }


def _review_link(
    candidates: dict[str, dict[str, Any]],
    prerequisite_id: str,
    target_id: str,
    rationale: str,
) -> dict[str, Any]:
    return {
        "prerequisite_id": prerequisite_id,
        "target_id": target_id,
        "rationale": rationale,
        "evidence_record_ids": _link_evidence(candidates, prerequisite_id, target_id),
    }


def _link_evidence(
    candidates: dict[str, dict[str, Any]], prerequisite_id: str, target_id: str
) -> list[str]:
    evidence: list[str] = []
    for candidate_id in (prerequisite_id, target_id):
        refs = candidates[candidate_id]["evidence_refs"]
        ref = next(item for item in refs if item["coverage"] != "context_only")
        if ref["record_id"] not in evidence:
            evidence.append(ref["record_id"])
    return evidence
