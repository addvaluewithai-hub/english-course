#!/usr/bin/env python3
"""Build a conservative A1 semantic-lock candidate from reviewed evidence.

This does NOT authorize lesson design. It converts the complete A1 source inventory into
explicit mastery roles while preserving uncertainty as a review queue.
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
A1 = ROOT / "curriculum/levels/a1"
OUT = A1 / "semantic-lock"
LEVEL = "A1"


def read(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    return json.loads(p.read_text(encoding="utf-8"))


def write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def walk_dicts(node: Any) -> Iterable[dict[str, Any]]:
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from walk_dicts(value)
    elif isinstance(node, list):
        for value in node:
            yield from walk_dicts(value)


def normalize_form(value: str) -> str:
    value = value.lower().replace("…", "...")
    value = value.replace("’", "'")
    value = re.sub(r"[.!?,;:()\[\]{}\"“”]", " ", value)
    value = value.replace("...", " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value


def lexical_source_records(ownership: dict[str, Any]) -> list[dict[str, Any]]:
    records = [
        row for row in walk_dicts(ownership)
        if {"source_record_id", "disposition", "headword", "part_of_speech"}.issubset(row)
        and str(row.get("source_record_id", "")).startswith("oxford.o3000.")
    ]
    # The recursive walk can see no duplicates today, but keep the builder defensive.
    by_id: dict[str, dict[str, Any]] = {}
    for row in records:
        by_id[row["source_record_id"]] = row
    return list(by_id.values())


def build_word_lock(words: dict[str, Any], ownership: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    course_items = {row["lexical_item_id"]: row for row in ownership["course_items"]}
    dispositions = {row["source_record_id"]: row for row in lexical_source_records(ownership)}

    inventory_ids = {row["item_id"] for row in words["items"]}
    if len(inventory_ids) != 900 or set(dispositions) != inventory_ids:
        raise SystemExit(
            f"A1 word ownership mismatch: inventory={len(inventory_ids)} reviewed={len(dispositions)} "
            f"missing_review={len(inventory_ids-set(dispositions))} extra_review={len(set(dispositions)-inventory_ids)}"
        )

    locked: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []
    for source in words["items"]:
        review = dispositions[source["item_id"]]
        disposition = review["disposition"]
        owners = review.get("course_item_ids", [])
        owner_rows = [course_items[o] for o in owners if o in course_items]

        if disposition == "selected_course_item":
            production_ready = bool(owner_rows) and all(
                row.get("first_guided_production_level") == "a1"
                and bool(row.get("productive_expectation"))
                and row.get("review", {}).get("status") == "accepted_for_a1_reconciliation"
                for row in owner_rows
            )
            if production_ready:
                role = "productive_required"
                decision_state = "auto_locked_from_reviewed_a1_ownership"
                needs_review = False
            else:
                role = "required_pending_control_decision"
                decision_state = "needs_human_review"
                needs_review = True
        elif disposition == "grammar_system_owned":
            role = "grammar_owned_required"
            decision_state = "auto_locked_from_reviewed_a1_ownership"
            needs_review = False
        elif disposition == "reference_pool_not_selected_v1":
            # New architecture change: complete level coverage means these no longer disappear.
            role = "receptive_required"
            decision_state = "candidate_requires_productive_review"
            needs_review = True
        else:
            role = "required_pending_control_decision"
            decision_state = "needs_human_review"
            needs_review = True

        item = {
            "item_id": source["item_id"],
            "headword": source["headword"],
            "part_of_speech": source.get("part_of_speech"),
            "published_level": source["published_level"],
            "semantic_role": role,
            "required_at_a1_exit": True,
            "independent_lexical_mastery": role != "grammar_owned_required",
            "decision_state": decision_state,
            "previous_reviewed_disposition": disposition,
            "reviewed_owner_ids": owners,
            "bounded_meaning_policy": (
                "Only the A1 meaning/function established by reviewed owners is implied."
                if owners else
                "Published A1 entry is required receptively; productive sense/function remains to be bounded."
            ),
            "source_ref": source["source_ref"],
        }
        locked.append(item)
        if needs_review:
            review_queue.append({
                "category": "words",
                "item_id": source["item_id"],
                "display": source["headword"],
                "current_role": role,
                "question": (
                    "Which A1 sense/function is required, and should the learner produce it independently?"
                ),
                "reason": disposition,
            })
    return locked, review_queue


def phrase_member_index(ownership: dict[str, Any]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = defaultdict(set)
    for row in ownership["course_items"]:
        if row.get("review", {}).get("status") != "accepted_for_a1_reconciliation":
            continue
        values: list[str] = []
        values.extend(v for v in row.get("members", []) if isinstance(v, str))
        values.extend(v for v in row.get("collocations_or_frames", []) if isinstance(v, str))
        for value in values:
            norm = normalize_form(value)
            if norm:
                index[norm].add(row["lexical_item_id"])
    return index


def build_phrase_lock(phrases: dict[str, Any], ownership: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(phrases["items"]) != 199:
        raise SystemExit(f"Expected 199 Oxford A1 phrases, got {len(phrases['items'])}")
    member_index = phrase_member_index(ownership)
    course_items = {row["lexical_item_id"]: row for row in ownership["course_items"]}
    locked: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []

    for source in phrases["items"]:
        norm = normalize_form(source["phrase"])
        owners = sorted(member_index.get(norm, set()))
        production_ready = bool(owners) and all(
            course_items[o].get("first_guided_production_level") == "a1"
            and bool(course_items[o].get("productive_expectation"))
            for o in owners
        )
        if production_ready:
            role = "productive_required"
            state = "auto_locked_exact_match_to_reviewed_a1_chunk"
            needs_review = False
        else:
            role = "receptive_required"
            state = "candidate_requires_productive_review"
            needs_review = True

        item = {
            "item_id": source["item_id"],
            "phrase": source["phrase"],
            "published_level": source["published_level"],
            "semantic_role": role,
            "required_at_a1_exit": True,
            "decision_state": state,
            "reviewed_owner_ids": owners,
            "matching_rule": "normalized_exact_member_match_only" if owners else None,
            "source_ref": source["source_ref"],
        }
        locked.append(item)
        if needs_review:
            review_queue.append({
                "category": "phrases",
                "item_id": source["item_id"],
                "display": source["phrase"],
                "current_role": role,
                "question": "Should this A1 phrase remain receptive-only or become independently productive?",
                "reason": "no_safe_exact_match_to_reviewed_productive_chunk",
            })
    return locked, review_queue


def build_grammar_lock(grammar: dict[str, Any], ownership: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    course_items = ownership["course_items"]
    feature_owners: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for course in course_items:
        for feature_id in course.get("source_evidence", {}).get("egp_feature_ids", []):
            feature_owners[feature_id].append(course)

    if len(grammar["items"]) != 109:
        raise SystemExit(f"Expected 109 EGP A1 features, got {len(grammar['items'])}")

    locked: list[dict[str, Any]] = []
    review_queue: list[dict[str, Any]] = []
    for source in grammar["items"]:
        feature_id = source["item_id"].removeprefix("egp.")
        owners = feature_owners.get(feature_id, [])
        statuses = sorted({str(row.get("control_status")) for row in owners})
        owner_ids = sorted(row["item_id"] for row in owners)

        if owners and any(status == "productive_core" for status in statuses):
            role = "productive_control_required"
            state = "auto_locked_from_reviewed_a1_grammar_control"
            needs_review = False
        elif owners and all(status.startswith("receptive") for status in statuses):
            role = "receptive_control_required"
            state = "auto_locked_from_reviewed_a1_grammar_control"
            needs_review = False
        elif owners:
            role = "required_control_pending_review"
            state = "needs_human_review"
            needs_review = True
        else:
            # Complete source coverage means the feature stays in the contract; absence of a
            # prior owner cannot silently demote or delete it.
            role = "required_feature_pending_control_decision"
            state = "needs_human_review"
            needs_review = True

        item = {
            "item_id": source["item_id"],
            "guideword": source.get("guideword"),
            "can_do": source.get("can_do"),
            "published_level": source["published_level"],
            "semantic_role": role,
            "required_at_a1_exit": True,
            "decision_state": state,
            "reviewed_control_owner_ids": owner_ids,
            "reviewed_control_statuses": statuses,
            "source_ref": source["source_ref"],
        }
        locked.append(item)
        if needs_review:
            review_queue.append({
                "category": "grammar",
                "item_id": source["item_id"],
                "display": source.get("guideword") or source.get("can_do"),
                "current_role": role,
                "question": "What exact A1 control obligation should this EGP feature have, and which grammar family owns it?",
                "reason": "no_unambiguous_reviewed_productive_or_receptive_control_owner",
            })
    return locked, review_queue


def build_ability_lock(abilities: dict[str, Any]) -> list[dict[str, Any]]:
    if len(abilities["items"]) != 119:
        raise SystemExit(f"Expected 119 required A1 abilities, got {len(abilities['items'])}")
    out = []
    for source in abilities["items"]:
        modes = source.get("mode_codes", [])
        if modes == ["reception"]:
            performance_role = "receptive_performance_required"
        elif "interaction" in modes:
            performance_role = "interactive_performance_required"
        elif "mediation" in modes:
            performance_role = "mediated_performance_required"
        elif "production" in modes:
            performance_role = "productive_performance_required"
        else:
            performance_role = "performance_required"
        out.append({
            "item_id": source["item_id"],
            "source_record_id": source["source_record_id"],
            "source_text": source["source_text"],
            "skill_codes": source.get("skill_codes", []),
            "mode_codes": modes,
            "strand_ids": source.get("strand_ids", []),
            "semantic_role": performance_role,
            "required_at_a1_exit": True,
            "decision_state": "locked_from_reviewed_include_for_spine_disposition",
            "source_ref": source["source_ref"],
        })
    return out


def build_pronunciation_lock(pronunciation: dict[str, Any]) -> list[dict[str, Any]]:
    if len(pronunciation["items"]) != 10:
        raise SystemExit(f"Expected 10 A1 pronunciation strands, got {len(pronunciation['items'])}")
    out = []
    for source in pronunciation["items"]:
        row = dict(source)
        row["semantic_role"] = "supporting_intelligibility_required"
        row["required_at_a1_exit"] = True
        row["decision_state"] = "locked_from_reviewed_pronunciation_progression"
        out.append(row)
    return out


def counts(rows: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(row["semantic_role"] for row in rows).items()))


def main() -> None:
    words = read(A1 / "words.json")
    phrases = read(A1 / "phrases.json")
    grammar = read(A1 / "grammar.json")
    abilities = read(A1 / "abilities.json")
    pronunciation = read(A1 / "pronunciation.json")
    lexical_ownership = read("data/reviewed/a1-lexical-chunk-ownership-v1.json")
    grammar_ownership = read("data/reviewed/a1-grammar-coverage-ownership-v1.json")

    word_rows, word_review = build_word_lock(words, lexical_ownership)
    phrase_rows, phrase_review = build_phrase_lock(phrases, lexical_ownership)
    grammar_rows, grammar_review = build_grammar_lock(grammar, grammar_ownership)
    ability_rows = build_ability_lock(abilities)
    pronunciation_rows = build_pronunciation_lock(pronunciation)
    review_queue = word_review + phrase_review + grammar_review

    auto_locked = sum(
        1 for group in (word_rows, phrase_rows, grammar_rows, ability_rows, pronunciation_rows)
        for row in group if not row["decision_state"].startswith("candidate") and row["decision_state"] != "needs_human_review"
    )
    total = sum(map(len, (word_rows, phrase_rows, grammar_rows, ability_rows, pronunciation_rows)))

    payload = {
        "schema_version": 1,
        "level": LEVEL,
        "status": "semantic_lock_candidate_pending_review",
        "lesson_design_authorized": False,
        "architecture_change": (
            "Complete level inventory is now an exit-coverage contract. Items previously left in the "
            "Oxford A1 reference pool are retained as receptive requirements until a bounded productive "
            "decision is made; they are not silently excluded."
        ),
        "policy": {
            "all_source_inventory_items_require_explicit_exit_disposition": True,
            "completion_is_not_mastery": True,
            "receptive_does_not_imply_productive": True,
            "productive_does_not_imply_all_dictionary_senses": True,
            "grammar_owned_words_are_not_double_assessed_as_independent_lexical_items": True,
            "uncertain_items_remain_required_and_enter_review_queue": True,
            "no_lesson_design_until_semantic_lock_reviewed": True,
        },
        "summary": {
            "total_primary_items": total,
            "auto_locked_from_existing_reviewed_evidence": auto_locked,
            "human_review_queue": len(review_queue),
            "words": {"total": len(word_rows), "roles": counts(word_rows)},
            "phrases": {"total": len(phrase_rows), "roles": counts(phrase_rows)},
            "grammar": {"total": len(grammar_rows), "roles": counts(grammar_rows)},
            "abilities": {"total": len(ability_rows), "roles": counts(ability_rows)},
            "pronunciation": {"total": len(pronunciation_rows), "roles": counts(pronunciation_rows)},
        },
        "words": word_rows,
        "phrases": phrase_rows,
        "grammar": grammar_rows,
        "abilities": ability_rows,
        "pronunciation": pronunciation_rows,
        "review_queue": review_queue,
        "evidence_sources": [
            "curriculum/levels/a1/words.json",
            "curriculum/levels/a1/phrases.json",
            "curriculum/levels/a1/grammar.json",
            "curriculum/levels/a1/abilities.json",
            "curriculum/levels/a1/pronunciation.json",
            "data/reviewed/a1-lexical-chunk-ownership-v1.json",
            "data/reviewed/a1-grammar-coverage-ownership-v1.json",
        ],
    }

    report = {
        "level": LEVEL,
        "status": payload["status"],
        "summary": payload["summary"],
        "review_queue_by_category": dict(sorted(Counter(row["category"] for row in review_queue).items())),
        "review_queue_examples": review_queue[:40],
        "invariants": {
            "words_complete": len(word_rows) == 900,
            "phrases_complete": len(phrase_rows) == 199,
            "grammar_complete": len(grammar_rows) == 109,
            "abilities_complete": len(ability_rows) == 119,
            "pronunciation_complete": len(pronunciation_rows) == 10,
            "all_primary_items_required_at_exit": all(
                row.get("required_at_a1_exit") is True
                for group in (word_rows, phrase_rows, grammar_rows, ability_rows, pronunciation_rows)
                for row in group
            ),
            "lesson_design_authorized": False,
        },
    }
    if not all(v for k, v in report["invariants"].items() if k != "lesson_design_authorized"):
        raise SystemExit(f"Semantic lock invariant failed: {report['invariants']}")

    write(OUT / "semantic-lock-candidate.json", payload)
    write(OUT / "semantic-lock-report.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
