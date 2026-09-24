#!/usr/bin/env python3
"""Apply reviewed A1 semantic-lock decisions after conservative candidate generation."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "curriculum/levels/a1/semantic-lock"
CANDIDATE = LOCK / "semantic-lock-candidate.json"
DECISIONS = LOCK / "manual-decisions.json"
PHRASE_DECISIONS = LOCK / "phrase-control-decisions.json"
REPORT = LOCK / "semantic-lock-report.json"
COMPACT = LOCK / "review-queue-compact.json"
CATEGORIES = ("grammar", "phrases", "words")
ALLOWED_ROLES = {
    "grammar": {"productive_control_required", "receptive_control_required", "formulaic_productive_control_required", "embedded_support_required"},
    "phrases": {"productive_required", "receptive_required", "formulaic_productive_required"},
    "words": {"productive_required", "receptive_required", "grammar_owned_required"},
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def role_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(row["semantic_role"] for row in rows).items()))


def apply_one(row: dict[str, Any], role: str, rationale: str, evidence_refs: list[str], boundary: str | None) -> None:
    row["semantic_role"] = role
    row["decision_state"] = "manually_locked_from_design_review_v1"
    row["manual_decision"] = {"rationale": rationale, "evidence_refs": evidence_refs, "control_boundary": boundary}


def main() -> None:
    candidate = load(CANDIDATE)
    manual = load(DECISIONS)
    if manual.get("level") != "A1":
        raise SystemExit("manual decisions must target A1")

    pending = {(row["category"], row["item_id"]) for row in candidate["review_queue"]}
    applied_pending: set[tuple[str, str]] = set()

    # Item-specific manual decisions remain strict: they must resolve a conservative pending item.
    for category in CATEGORIES:
        by_id = {row["item_id"]: row for row in candidate[category]}
        seen: set[str] = set()
        for decision in manual.get("decisions", {}).get(category, []):
            item_id = decision["item_id"]
            role = decision["semantic_role"]
            if item_id in seen:
                raise SystemExit(f"duplicate manual decision: {category}:{item_id}")
            seen.add(item_id)
            if role not in ALLOWED_ROLES[category] or item_id not in by_id:
                raise SystemExit(f"invalid manual decision: {category}:{item_id}:{role}")
            if (category, item_id) not in pending:
                raise SystemExit(f"manual decision does not reference a pending item: {category}:{item_id}")
            rationale = str(decision.get("rationale", "")).strip()
            if not rationale:
                raise SystemExit(f"manual decision needs rationale: {category}:{item_id}")
            apply_one(by_id[item_id], role, rationale, decision.get("evidence_refs", []), decision.get("control_boundary"))
            applied_pending.add((category, item_id))

    # Stage-02 manually reviewed all 199 phrases; this control map deliberately reviews all
    # of them again for productive/receptive/formulaic obligation, including prior auto-locks.
    phrase_map = load(PHRASE_DECISIONS)
    phrase_by_id = {row["item_id"]: row for row in candidate["phrases"]}
    phrase_seen: set[str] = set()
    phrase_evidence = [phrase_map["evidence_ref"]]
    for group in phrase_map["role_groups"]:
        role = group["semantic_role"]
        if role not in ALLOWED_ROLES["phrases"]:
            raise SystemExit(f"invalid phrase role: {role}")
        rationale = str(group.get("rationale", "")).strip()
        if not rationale:
            raise SystemExit(f"phrase group {role} needs rationale")
        for item_id in group["item_ids"]:
            if item_id in phrase_seen:
                raise SystemExit(f"duplicate phrase control decision: {item_id}")
            if item_id not in phrase_by_id:
                raise SystemExit(f"unknown phrase control item: {item_id}")
            phrase_seen.add(item_id)
            apply_one(phrase_by_id[item_id], role, rationale, phrase_evidence, group.get("control_boundary"))
            if ("phrases", item_id) in pending:
                applied_pending.add(("phrases", item_id))
    expected = int(phrase_map["expected_item_count"])
    if len(phrase_seen) != expected or phrase_seen != set(phrase_by_id):
        raise SystemExit(f"phrase control map must cover all phrases exactly once: mapped={len(phrase_seen)} inventory={len(phrase_by_id)}")

    candidate["review_queue"] = [row for row in candidate["review_queue"] if (row["category"], row["item_id"]) not in applied_pending]

    manual_locked = sum(1 for category in CATEGORIES for row in candidate[category] if row.get("decision_state") == "manually_locked_from_design_review_v1")
    auto_locked = sum(
        1 for category in ("words", "phrases", "grammar", "abilities", "pronunciation")
        for row in candidate[category]
        if row.get("decision_state") != "manually_locked_from_design_review_v1"
        and not str(row.get("decision_state", "")).startswith("candidate")
        and row.get("decision_state") != "needs_human_review"
    )
    candidate["summary"]["auto_locked_from_existing_reviewed_evidence"] = auto_locked
    candidate["summary"]["manually_locked_from_design_review"] = manual_locked
    candidate["summary"]["human_review_queue"] = len(candidate["review_queue"])
    for category in ("words", "phrases", "grammar", "abilities", "pronunciation"):
        candidate["summary"][category]["roles"] = role_counts(candidate[category])
    candidate["status"] = "semantic_lock_candidate_pending_review" if candidate["review_queue"] else "semantic_lock_reviewed_ready_for_manifest_authorization"

    grouped: dict[str, list[dict[str, Any]]] = {category: [] for category in CATEGORIES}
    for row in candidate["review_queue"]:
        grouped.setdefault(row["category"], []).append(row)
    report = {
        "level": "A1",
        "status": candidate["status"],
        "summary": candidate["summary"],
        "review_queue_by_category": dict(sorted(Counter(row["category"] for row in candidate["review_queue"]).items())),
        "review_queue_examples_by_category": {category: rows[:12] for category, rows in grouped.items()},
        "invariants": {
            "words_complete": len(candidate["words"]) == 900,
            "phrases_complete": len(candidate["phrases"]) == 199,
            "grammar_complete": len(candidate["grammar"]) == 109,
            "abilities_complete": len(candidate["abilities"]) == 119,
            "pronunciation_complete": len(candidate["pronunciation"]) == 10,
            "all_primary_items_required_at_exit": all(row.get("required_at_a1_exit") is True for category in ("words", "phrases", "grammar", "abilities", "pronunciation") for row in candidate[category]),
            "phrase_control_map_complete": len(phrase_seen) == 199,
            "lesson_design_authorized": False,
        },
    }
    if not all(v for k, v in report["invariants"].items() if k != "lesson_design_authorized"):
        raise SystemExit(f"semantic lock invariant failed: {report['invariants']}")
    compact = {"schema_version": 1, "level": "A1", "status": candidate["status"], "pending_total": len(candidate["review_queue"]), "pending_by_category": report["review_queue_by_category"], "pending": grouped}
    write(CANDIDATE, candidate)
    write(REPORT, report)
    write(COMPACT, compact)
    print(json.dumps({"status": candidate["status"], "pending": compact["pending_by_category"], "manual_locked": manual_locked}, indent=2))


if __name__ == "__main__":
    main()
