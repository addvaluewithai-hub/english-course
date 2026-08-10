"""Create a traceable worklist for reviewing all 81 A1 candidates."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from scripts.a1_reconciliation_contract import (
    A1_MAP, ALL_CEFR, ALL_GSE, DECISIONS, INPUTS, OUTPUT, REPORT,
    REVIEW_PASSES, REVIEWED_AT, REVIEWER, ROOT, TAGS, UNIT1,
)
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _relationship_ids(candidate: dict, key: str) -> list[str]:
    values = candidate["relationships"][key]
    return [value if isinstance(value, str) else value["candidate_id"] for value in values]


def _targets(candidate: dict) -> dict[str, list[str]]:
    return {
        family: [row["target"] for row in candidate["language_targets"][family]]
        for family in ("grammar", "vocabulary", "phrases", "pronunciation")
    }


def _source_key(row: dict) -> tuple[str, int, str]:
    source = row["source"] if "source" in row else row
    return (
        source["source_id"], source["location"]["page"], source["source_text_sha256"],
    )


def _normalized_index(*datasets: dict) -> dict[tuple[str, int, str], list[dict]]:
    index: dict[tuple[str, int, str], list[dict]] = {}
    for dataset in datasets:
        for row in dataset["records"]:
            index.setdefault(_source_key(row), []).append(row)
    return index


def _level_fit(evidence_refs: list[dict], normalized: dict, tag_index: dict[str, dict]) -> dict:
    matched_ids, unmatched = [], []
    for ref in evidence_refs:
        rows = normalized.get(_source_key(ref), [])
        if not rows:
            unmatched.append(ref["record_id"])
        else:
            matched_ids.extend(row["record_id"] for row in rows)
    matched_ids = sorted(set(matched_ids))
    matched = [tag_index[item] for item in matched_ids if item in tag_index]
    levels = sorted({level for row in matched for level in row["source_level_codes"]})
    above_a1 = [level for level in levels if level not in ("pre_a1", "a1")]
    if unmatched:
        status = "missing_all_level_match"
    elif above_a1:
        status = "mixed_level_evidence_review"
    elif "pre_a1" in levels:
        status = "a1_with_pre_a1_support"
    else:
        status = "a1_only_evidence"
    return {
        "matched_source_ref_count": len(evidence_refs) - len(unmatched),
        "matched_all_level_record_ids": matched_ids,
        "unmatched_record_ids": sorted(unmatched),
        "all_level_codes": levels, "above_a1_level_codes": above_a1, "status": status,
    }


def _unit_index(unit: dict) -> dict[str, dict]:
    return {row["candidate_id"]: row for row in unit["lessons"]}


def _candidate(candidate: dict, position: int, normalized: dict, tag_index: dict, units: dict) -> dict:
    evidence_ids = [row["record_id"] for row in candidate["evidence_refs"]]
    unit = units.get(candidate["candidate_id"])
    targets = _targets(candidate)
    return {
        "candidate_id": candidate["candidate_id"], "original_sequence_position": position,
        "current_internal_status": candidate["status"],
        "cluster_ids": candidate["candidate_cluster_ids"], "outcome": candidate["outcome"],
        "skill_codes": candidate["skill_codes"], "mode_codes": candidate["mode_codes"],
        "function_codes": candidate["function_codes"],
        "evidence": {
            "record_count": len(evidence_ids), "record_ids": evidence_ids,
            "level_fit": _level_fit(candidate["evidence_refs"], normalized, tag_index),
        },
        "current_language_targets": targets,
        "current_target_counts": {family: len(values) for family, values in targets.items()},
        "current_error_hypothesis_count": len(candidate["error_hypotheses"]),
        "current_relationships": {
            "required_before": _relationship_ids(candidate, "required_before"),
            "helpful_before": _relationship_ids(candidate, "helpful_before"),
            "successors": _relationship_ids(candidate, "successors"),
            "concurrent_support": [row["support_id"] for row in candidate["relationships"]["concurrent_support"]],
        },
        "current_mastery": {
            "fresh_task_family": candidate["mastery"]["fresh_task_family"],
            "critical_failures": candidate["mastery"]["critical_failures"],
            "delayed_probe": candidate["mastery"]["delayed_probe"],
        },
        "unit1_membership": {
            "included": unit is not None,
            "lesson_id": None if unit is None else unit["lesson_id"],
            "package_status": None if unit is None else unit["status"],
        },
        "reconciliation": {
            "review_status": "pending", "decision": None, "rationale": None,
            "related_candidate_ids": [], "unresolved_questions": [],
        },
    }


def build() -> dict[str, Any]:
    source_map, unit, tags = _load(A1_MAP), _load(UNIT1), _load(TAGS)
    normalized = _normalized_index(_load(ALL_GSE), _load(ALL_CEFR))
    tag_index = {row["source_record_id"]: row for row in tags["records"]}
    unit_index = _unit_index(unit)
    candidates = [
        _candidate(candidate, position, normalized, tag_index, unit_index)
        for position, candidate in enumerate(source_map["candidates"], start=1)
    ]
    fit_counts = Counter(row["evidence"]["level_fit"]["status"] for row in candidates)
    unmatched = sorted({
        record_id for row in candidates
        for record_id in row["evidence"]["level_fit"]["unmatched_record_ids"]
    })
    return {
        "schema_version": 1, "worklist_id": "a1_reconciliation_worklist", "version": 1,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in INPUTS
        ],
        "decision_codes": list(DECISIONS), "review_passes": list(REVIEW_PASSES),
        "candidates": candidates,
        "audit": {
            "candidate_count": len(candidates), "unit1_candidate_count": len(unit_index),
            "unique_sequence_positions": len({row["original_sequence_position"] for row in candidates}),
            "source_level_fit_counts": dict(sorted(fit_counts.items())),
            "unmatched_evidence_record_ids": unmatched,
            "unknown_unit1_candidate_ids": sorted(set(unit_index) - {row["candidate_id"] for row in candidates}),
            "decision_counts": {"pending": len(candidates)},
        },
        "review": {
            "status": "worklist_ready", "reviewer": REVIEWER, "created_at": REVIEWED_AT,
            "statement": "This inventory does not approve candidates; every row still requires all seven reconciliation passes.",
        },
    }


def _report(data: dict) -> str:
    audit = data["audit"]
    lines = [
        "# A1 Reconciliation Worklist v1", "", "Status: worklist ready; no final candidate decisions yet.", "",
        f"- Current candidates: {audit['candidate_count']}",
        f"- Current Unit 1 candidates: {audit['unit1_candidate_count']}",
        f"- Unmatched evidence records: {len(audit['unmatched_evidence_record_ids'])}",
        "", "Every candidate must pass outcome/level fit, ability coverage, grammar, lexical,",
        "pronunciation, sequence/recycling, and mastery/exit-assessment review. The final",
        "lesson count is open and the current internal approval status has no preservation bias.", "",
        "| Position | Candidate | Evidence fit | Unit 1 | Decision |", "| ---: | --- | --- | --- | --- |",
    ]
    for row in data["candidates"]:
        unit = row["unit1_membership"]["lesson_id"] or "-"
        lines.append(
            f"| {row['original_sequence_position']} | `{row['candidate_id']}` | "
            f"{row['evidence']['level_fit']['status']} | {unit} | pending |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['candidates'])} candidates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
