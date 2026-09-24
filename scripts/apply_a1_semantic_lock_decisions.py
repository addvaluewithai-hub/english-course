#!/usr/bin/env python3
"""Apply reviewed A1 semantic-lock decisions after conservative candidate generation."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "curriculum/levels/a1/semantic-lock"
CANDIDATE = LOCK / "semantic-lock-candidate.json"
DECISIONS = LOCK / "manual-decisions.json"
PHRASE_DECISIONS = LOCK / "phrase-control-decisions.json"
WORD_DECISIONS = LOCK / "word-control-decisions.json"
REPORT = LOCK / "semantic-lock-report.json"
COMPACT = LOCK / "review-queue-compact.json"
CATEGORIES = ("grammar", "phrases", "words")
ALLOWED_ROLES = {
    "grammar": {
        "productive_control_required", "receptive_control_required",
        "formulaic_productive_control_required", "embedded_support_required",
    },
    "phrases": {"productive_required", "receptive_required", "formulaic_productive_required"},
    "words": {"productive_required", "receptive_required", "grammar_owned_required"},
}


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def role_counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(row["semantic_role"] for row in rows).items()))


def ids_digest(ids: set[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def apply_one(
    row: dict[str, Any], role: str, rationale: str,
    evidence_refs: list[str], boundary: str | None,
) -> None:
    row["semantic_role"] = role
    row["decision_state"] = "manually_locked_from_design_review_v1"
    row["manual_decision"] = {
        "rationale": rationale,
        "evidence_refs": evidence_refs,
        "control_boundary": boundary,
    }


def main() -> None:
    candidate = load(CANDIDATE)
    manual = load(DECISIONS)
    if manual.get("level") != "A1":
        raise SystemExit("manual decisions must target A1")

    pending = {(row["category"], row["item_id"]) for row in candidate["review_queue"]}
    applied_pending: set[tuple[str, str]] = set()

    # Item-specific decisions are used for the manually reviewed grammar partition.
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
            apply_one(
                by_id[item_id], role, rationale,
                decision.get("evidence_refs", []), decision.get("control_boundary"),
            )
            applied_pending.add((category, item_id))

    # Stage-02 reviewed all phrases; the control map covers every phrase exactly once.
    phrase_map = load(PHRASE_DECISIONS)
    phrase_by_id = {row["item_id"]: row for row in candidate["phrases"]}
    phrase_seen: set[str] = set()
    for group in phrase_map["role_groups"]:
        role = group["semantic_role"]
        rationale = str(group.get("rationale", "")).strip()
        if role not in ALLOWED_ROLES["phrases"] or not rationale:
            raise SystemExit(f"invalid phrase control group: {role}")
        for item_id in group["item_ids"]:
            if item_id in phrase_seen or item_id not in phrase_by_id:
                raise SystemExit(f"invalid phrase control item: {item_id}")
            phrase_seen.add(item_id)
            apply_one(
                phrase_by_id[item_id], role, rationale,
                [phrase_map["evidence_ref"]], group.get("control_boundary"),
            )
            if ("phrases", item_id) in pending:
                applied_pending.add(("phrases", item_id))
    if len(phrase_seen) != int(phrase_map["expected_item_count"]) or phrase_seen != set(phrase_by_id):
        raise SystemExit("phrase control map must cover all phrases exactly once")

    # Stage-04 reviewed all words. Only the frozen former reference-pool set needs new
    # productive/receptive decisions; the exact set is protected by a digest.
    if manual.get("decisions", {}).get("words"):
        raise SystemExit("word-specific decisions belong in word-control-decisions.json")
    word_map = load(WORD_DECISIONS)
    word_pending_ids = {item_id for category, item_id in pending if category == "words"}
    if len(word_pending_ids) != int(word_map["expected_pending_count"]):
        raise SystemExit(f"word pending count changed: {len(word_pending_ids)}")
    if ids_digest(word_pending_ids) != word_map["pending_item_ids_sha256"]:
        raise SystemExit("word pending ID digest changed; re-review the word set")

    word_by_id = {row["item_id"]: row for row in candidate["words"]}
    headword_index: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item_id in word_pending_ids:
        headword_index[word_by_id[item_id]["headword"]].append(word_by_id[item_id])

    word_seen: set[str] = set()
    word_evidence = list(word_map.get("evidence_refs", []))
    for key in ("productive_promotion", "grammar_owned"):
        group = word_map[key]
        role = group["semantic_role"]
        if role not in ALLOWED_ROLES["words"]:
            raise SystemExit(f"invalid word control role: {role}")
        for headword in group["headwords"]:
            matches = headword_index.get(headword, [])
            if len(matches) != 1:
                raise SystemExit(f"word control headword must resolve exactly once: {headword} -> {len(matches)}")
            row = matches[0]
            if row["item_id"] in word_seen:
                raise SystemExit(f"duplicate word control decision: {row['item_id']}")
            word_seen.add(row["item_id"])
            apply_one(row, role, group["rationale"], word_evidence, group.get("control_boundary"))
            applied_pending.add(("words", row["item_id"]))

    default = word_map["default_pending_role"]
    default_role = default["semantic_role"]
    if default_role not in ALLOWED_ROLES["words"]:
        raise SystemExit(f"invalid default word role: {default_role}")
    for item_id in sorted(word_pending_ids - word_seen):
        apply_one(
            word_by_id[item_id], default_role, default["rationale"],
            word_evidence, default.get("control_boundary"),
        )
        word_seen.add(item_id)
        applied_pending.add(("words", item_id))
    if word_seen != word_pending_ids:
        raise SystemExit("word control review did not cover the frozen pending set exactly once")

    candidate["review_queue"] = [
        row for row in candidate["review_queue"]
        if (row["category"], row["item_id"]) not in applied_pending
    ]
    manual_locked = sum(
        1 for category in CATEGORIES for row in candidate[category]
        if row.get("decision_state") == "manually_locked_from_design_review_v1"
    )
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
    candidate["status"] = (
        "semantic_lock_candidate_pending_review" if candidate["review_queue"]
        else "semantic_lock_reviewed_ready_for_manifest_authorization"
    )

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
            "all_primary_items_required_at_exit": all(
                row.get("required_at_a1_exit") is True
                for category in ("words", "phrases", "grammar", "abilities", "pronunciation")
                for row in candidate[category]
            ),
            "phrase_control_map_complete": len(phrase_seen) == 199,
            "word_control_review_complete": word_seen == word_pending_ids,
            "lesson_design_authorized": False,
        },
    }
    if not all(v for k, v in report["invariants"].items() if k != "lesson_design_authorized"):
        raise SystemExit(f"semantic lock invariant failed: {report['invariants']}")

    compact = {
        "schema_version": 1,
        "level": "A1",
        "status": candidate["status"],
        "pending_total": len(candidate["review_queue"]),
        "pending_by_category": report["review_queue_by_category"],
        "pending": grouped,
    }
    write(CANDIDATE, candidate)
    write(REPORT, report)
    write(COMPACT, compact)
    print(json.dumps({
        "status": candidate["status"],
        "pending": compact["pending_by_category"],
        "manual_locked": manual_locked,
        "word_roles": candidate["summary"]["words"]["roles"],
    }, indent=2))


if __name__ == "__main__":
    main()
