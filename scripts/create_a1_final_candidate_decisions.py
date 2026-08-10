"""Build final evidence-led dispositions for all 81 current A1 candidates."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from scripts.a1_final_decision_analysis import (
    enrich_decisions, exit_resolutions, final_capabilities, ownership_transfers,
)
from scripts.a1_final_decision_catalog import DECISIONS
from scripts.a1_final_decisions_contract import INPUTS, OUTPUT, REPORT, REVIEWED_AT, REVIEWER, ROOT
from scripts.a1_final_decisions_report import render
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build() -> dict:
    worklist, outcomes, _abilities, _grammar, _lexical, _pronunciation, dependency = [
        _load(path) for path in INPUTS
    ]
    decisions = enrich_decisions(DECISIONS, worklist, outcomes, dependency)
    transfers = ownership_transfers(decisions)
    lessons, supports = final_capabilities(decisions, transfers)
    decision_index = {row["candidate_id"]: row for row in decisions}
    exits = exit_resolutions(dependency, decision_index)
    counts = Counter(row["decision"] for row in decisions)
    all_final_items = {
        item for owner in lessons + supports
        for field in ("introduction_item_ids", "recycle_item_ids") for item in owner[field]
    }
    unit1_ids = {
        row["candidate_id"] for row in worklist["candidates"] if row["unit1_membership"]["included"]
    }
    return {
        "schema_version": 1,
        "decision_set_id": "a1_final_candidate_decisions",
        "version": 1,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in INPUTS
        ],
        "policy": {
            "old_candidate_count_is_not_a_target": True,
            "no_preservation_bias": True,
            "source_capability_survival_rule": "Every source capability survives as a lesson, merged variant, split arm, or explicit support owner.",
            "exact_ownership_transfer_rule": "Every introduction and recycle role on a non-surviving candidate has a named final destination.",
            "mass_production_status": "blocked_until_SPINE_006",
        },
        "decisions": decisions,
        "ownership_transfers": transfers,
        "final_lesson_capabilities": lessons,
        "support_owners": supports,
        "exit_anchor_resolutions": exits,
        "audit": {
            "candidate_count": len(decisions),
            "decision_counts": dict(sorted(counts.items())),
            "final_lesson_capability_count": len(lessons),
            "support_owner_count": len(supports),
            "non_surviving_candidate_count": sum(not row["survives_as_learner_lesson"] for row in decisions),
            "ownership_transfer_count": len(transfers),
            "final_exact_item_count": len(all_final_items),
            "resolved_exit_anchor_count": sum(row["status"] == "resolved" for row in exits),
            "unresolved_exit_anchor_count": sum(row["status"] != "resolved" for row in exits),
            "scope_revision_candidates_kept_without_revision": sum(
                row["a1_fit_status"] != "fits_a1_boundary" and row["decision"] == "keep"
                for row in decisions
            ),
            "surviving_unit1_capability_count": sum(
                row["candidate_id"] in unit1_ids and row["survives_as_learner_lesson"]
                for row in decisions
            ),
            "sequence_findings_carried_forward": dependency["audit"]["items_requiring_sequence_resolution"],
            "unresolved_questions": [],
        },
        "review": {
            "status": "SPINE_005_passed_for_scope_and_sequence",
            "reviewer": REVIEWER,
            "reviewed_at": REVIEWED_AT,
            "statement": "All 81 candidates have final evidence-led dispositions; SPINE-006 now owns unit grouping and order.",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({data['audit']['final_lesson_capability_count']} final capabilities)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
