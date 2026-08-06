"""Sequence, relationship, support, and mastery checks for lesson maps."""

from __future__ import annotations

from typing import Any


DIMENSIONS = {
    "comprehension", "outcome_performance", "interaction_or_transfer",
    "control_or_repair",
}
BASIC_SUPPORT = "support.basic_language_control"
REPAIR_SUPPORT = "support.interaction_repair"


def relationship_errors(
    lesson_map: dict[str, Any], source_record_ids: set[str]
) -> list[str]:
    errors: list[str] = []
    candidates = lesson_map["candidates"]
    ids = [candidate["candidate_id"] for candidate in candidates]
    if len(ids) != len(set(ids)):
        errors.append("candidates repeat a candidate_id")
    candidate_by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    if set(lesson_map["sequence"]) != set(ids):
        errors.append("sequence does not exactly cover candidate ids")
    positions = {candidate_id: position for position, candidate_id in enumerate(lesson_map["sequence"])}

    for candidate in candidates:
        errors.extend(_candidate_relationship_errors(candidate, candidate_by_id, source_record_ids))
        errors.extend(_mastery_errors(candidate))
    errors.extend(_ordering_errors(candidate_by_id, positions))
    errors.extend(_support_errors(lesson_map, candidate_by_id, source_record_ids))
    errors.extend(_approval_errors(lesson_map))
    return errors


def _candidate_relationship_errors(
    candidate: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
    source_record_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    candidate_id = candidate["candidate_id"]
    for relation_type in ("required_before", "helpful_before", "successors"):
        relations = candidate["relationships"][relation_type]
        targets = [relation["candidate_id"] for relation in relations]
        if len(targets) != len(set(targets)):
            errors.append(f"{candidate_id}: {relation_type} repeats a target")
        for relation in relations:
            target = relation["candidate_id"]
            if target not in candidates:
                errors.append(f"{candidate_id}: {relation_type} target {target} is unknown")
            if target == candidate_id:
                errors.append(f"{candidate_id}: {relation_type} cannot target itself")
            unknown = set(relation["evidence_record_ids"]) - source_record_ids
            if unknown:
                errors.append(f"{candidate_id}: {relation_type} has unknown evidence {sorted(unknown)}")
            if target in candidates:
                pair_evidence = {
                    ref["record_id"] for item in (candidate, candidates[target])
                    for ref in item["evidence_refs"]
                    if ref["coverage"] != "context_only"
                }
                outside = set(relation["evidence_record_ids"]) - pair_evidence
                if outside:
                    errors.append(
                        f"{candidate_id}: {relation_type} cites evidence outside the candidate pair {sorted(outside)}"
                    )
    return errors


def _ordering_errors(
    candidates: dict[str, dict[str, Any]], positions: dict[str, int]
) -> list[str]:
    errors: list[str] = []
    graph: dict[str, list[str]] = {candidate_id: [] for candidate_id in candidates}
    for candidate_id, candidate in candidates.items():
        required = {
            relation["candidate_id"] for relation in candidate["relationships"]["required_before"]
        }
        for prerequisite in required:
            if prerequisite not in candidates:
                continue
            graph[candidate_id].append(prerequisite)
            if positions.get(prerequisite, -1) >= positions.get(candidate_id, -1):
                errors.append(f"{candidate_id}: required prerequisite {prerequisite} is not earlier")
            successor_ids = {
                relation["candidate_id"]
                for relation in candidates[prerequisite]["relationships"]["successors"]
            }
            if candidate_id not in successor_ids:
                errors.append(f"{candidate_id}: {prerequisite} lacks reciprocal successor link")
        for successor in candidate["relationships"]["successors"]:
            target = successor["candidate_id"]
            if target in candidates:
                target_required = {
                    relation["candidate_id"]
                    for relation in candidates[target]["relationships"]["required_before"]
                }
                if candidate_id not in target_required:
                    errors.append(f"{candidate_id}: successor {target} lacks reciprocal prerequisite")
        for relation in candidate["relationships"]["helpful_before"]:
            prerequisite = relation["candidate_id"]
            if prerequisite in candidates and positions.get(prerequisite, -1) >= positions.get(candidate_id, -1):
                errors.append(
                    f"{candidate_id}: helpful prerequisite {prerequisite} is not earlier"
                )
    if _has_cycle(graph):
        errors.append("required_before relationships contain a cycle")
    return errors


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    active: set[str] = set()
    complete: set[str] = set()

    def visit(node: str) -> bool:
        if node in active:
            return True
        if node in complete:
            return False
        active.add(node)
        if any(visit(target) for target in graph[node]):
            return True
        active.remove(node)
        complete.add(node)
        return False

    return any(visit(node) for node in graph)


def _support_errors(
    lesson_map: dict[str, Any],
    candidates: dict[str, dict[str, Any]],
    source_record_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    supports = lesson_map["support_definitions"]
    ids = [support["support_id"] for support in supports]
    if len(ids) != len(set(ids)):
        errors.append("support_definitions repeat a support_id")
    support_by_id = {support["support_id"]: support for support in supports}
    for support in supports:
        for candidate_id in support["applies_to_candidate_ids"]:
            if candidate_id not in candidates:
                errors.append(f"{support['support_id']}: unknown candidate {candidate_id}")
                continue
            candidate_supports = {
                relation["support_id"]
                for relation in candidates[candidate_id]["relationships"]["concurrent_support"]
            }
            if support["support_id"] not in candidate_supports:
                errors.append(f"{support['support_id']}: applicability is not reciprocal for {candidate_id}")
    for candidate_id, candidate in candidates.items():
        relations = candidate["relationships"]["concurrent_support"]
        relation_ids = [relation["support_id"] for relation in relations]
        if len(relation_ids) != len(set(relation_ids)):
            errors.append(f"{candidate_id}: concurrent_support repeats a support id")
        required = {BASIC_SUPPORT}
        if {"interaction", "online_interaction"} & set(candidate["mode_codes"]):
            required.add(REPAIR_SUPPORT)
        if missing := required - set(relation_ids):
            errors.append(f"{candidate_id}: missing required concurrent support {sorted(missing)}")
        for relation in relations:
            support = support_by_id.get(relation["support_id"])
            if support is None:
                errors.append(f"{candidate_id}: unknown support {relation['support_id']}")
                continue
            if candidate_id not in support["applies_to_candidate_ids"]:
                errors.append(f"{candidate_id}: support applicability is not reciprocal")
            support_evidence = {ref["record_id"] for ref in support["evidence_refs"]}
            if not set(relation["evidence_record_ids"]) <= support_evidence:
                errors.append(f"{candidate_id}: support relation cites evidence outside definition")
            if not set(relation["evidence_record_ids"]) <= source_record_ids:
                errors.append(f"{candidate_id}: support relation has unknown evidence")
    return errors


def _mastery_errors(candidate: dict[str, Any]) -> list[str]:
    candidate_id = candidate["candidate_id"]
    mastery = candidate["mastery"]
    dimensions = set(mastery["required_dimensions"])
    errors = []
    if not {"comprehension", "outcome_performance"} <= dimensions:
        errors.append(f"{candidate_id}: mastery omits an always-required dimension")
    if not dimensions <= DIMENSIONS:
        errors.append(f"{candidate_id}: mastery uses an unknown dimension")
    if set(mastery["level_2_evidence"]) != dimensions:
        errors.append(f"{candidate_id}: level_2_evidence keys do not match required dimensions")
    return errors


def _approval_errors(lesson_map: dict[str, Any]) -> list[str]:
    if lesson_map["status"] != "approved":
        return []
    errors = []
    if lesson_map["review"]["status"] != "accepted":
        errors.append("approved map must have an accepted map review")
    for candidate in lesson_map["candidates"]:
        if candidate["status"] != "approved_candidate" or candidate["review"]["status"] != "accepted":
            errors.append(f"{candidate['candidate_id']}: approved map contains an unapproved candidate")
    represented = {
        skill for candidate in lesson_map["candidates"] for skill in candidate["skill_codes"]
    }
    missing = {"listening", "reading", "speaking", "writing"} - represented
    if missing:
        errors.append(f"approved map lacks core-skill presence {sorted(missing)}")
    return errors
