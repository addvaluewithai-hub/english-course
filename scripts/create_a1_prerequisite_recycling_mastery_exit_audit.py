"""Create the cross-artifact A1 prerequisite, recycling, mastery, and exit audit."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from scripts.a1_dependency_mastery_contract import INPUTS, OUTPUT, REPORT, REVIEWED_AT, REVIEWER, ROOT
from scripts.a1_dependency_mastery_report import render
from scripts.a1_mastery_exit_analysis import candidate_impacts, exit_safeguards, mastery_reviews
from scripts.a1_sequence_recycling_analysis import exact_item_rows, explicit_edges, position_index
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict:
    lesson_map, worklist, outcomes, abilities, grammar, lexical, pronunciation, _profiles = [
        _load(path) for path in INPUTS
    ]
    sequence = lesson_map["sequence"]
    positions = position_index(sequence)
    outcome_index = {row["candidate_id"]: row for row in outcomes["reviews"]}
    signals = {item: row["independence_signal"] for item, row in outcome_index.items()}
    edges = explicit_edges(worklist["candidates"], positions)
    items = exact_item_rows(grammar, lexical, pronunciation, positions)
    impacts = candidate_impacts(worklist["candidates"], items, positions, signals)
    mastery = mastery_reviews(worklist["candidates"], outcome_index)
    exits = exit_safeguards(abilities["exit_dimension_coverage"])
    item_counts = Counter(row["status"] for row in items)
    return {
        "schema_version": 1,
        "audit_id": "a1_prerequisite_recycling_mastery_exit_audit",
        "version": 1,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in INPUTS
        ],
        "policy": {
            "sequence_status": "provisional_not_locked",
            "ownership_transfer_rule": "Any merge, split, support-only, defer, or retire decision must transfer every exact introduction and recycle role.",
            "recycling_rule": "Every exact item needs a named introduction and a distinct later fresh retrieval before or at the A1 exit probe.",
            "mastery_rule": "Mastery uses a fresh task, construct-aligned critical failures, no answer-revealing model, and a delayed probe.",
            "exit_rule": "All seven exit dimensions and their protected capability anchors must survive final architecture decisions.",
        },
        "provisional_sequence": sequence,
        "explicit_dependency_edges": edges,
        "exact_item_sequence": items,
        "candidate_ownership_impacts": impacts,
        "mastery_reviews": mastery,
        "exit_safeguards": exits,
        "audit": {
            "candidate_count": len(worklist["candidates"]),
            "explicit_dependency_edge_count": len(edges),
            "aligned_explicit_dependency_edges": sum(row["status"] == "aligned" for row in edges),
            "unresolved_explicit_dependency_edges": sum(row["status"] != "aligned" for row in edges),
            "unit1_order_findings_carried_forward": len(abilities["unit1_audit"]["helpful_before_order_violations"]),
            "exact_item_count": len(items),
            "exact_item_sequence_status_counts": dict(sorted(item_counts.items())),
            "items_requiring_sequence_resolution": sum(row["status"] != "aligned" for row in items),
            "candidates_with_exact_item_roles": sum(bool(row["introduction_item_ids"] or row["recycle_item_ids"]) for row in impacts),
            "structurally_complete_mastery_records": sum(row["structural_status"] == "complete" for row in mastery),
            "mastery_constructs_aligned": sum(row["construct_alignment_status"] == "aligned_with_current_outcome" for row in mastery),
            "mastery_constructs_requiring_revision": sum(row["construct_alignment_status"] != "aligned_with_current_outcome" for row in mastery),
            "protected_exit_dimension_count": sum(row["all_anchors_are_current_owners"] for row in exits),
            "unknown_location_ids": [],
            "final_candidate_decisions_made": 0,
        },
        "review": {
            "status": "accepted_for_final_candidate_decisions",
            "reviewer": REVIEWER,
            "reviewed_at": REVIEWED_AT,
            "statement": "This pass locks constraints, not the final lesson count or sequence.",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({data['audit']['exact_item_count']} exact items)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
