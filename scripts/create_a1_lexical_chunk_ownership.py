"""Build exact A1 lexical sets, chunks, Oxford dispositions, and owners."""

from __future__ import annotations

import copy
import json
from collections import Counter, defaultdict

from scripts.a1_lexical_item_catalog import ITEMS
from scripts.a1_lexical_ownership_contract import (
    FUNCTIONS, GRAMMAR_HEADWORDS, INPUTS, OUTPUT, OXFORD, REPORT, REVIEWED_AT,
    REVIEWER, ROOT, WORKLIST,
)
from scripts.a1_lexical_ownership_report import render
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _a1_oxford() -> list[dict]:
    return [row for row in _load(OXFORD)["records"] if row["interpretation"]["cefr_codes"] == ["a1"]]


def _headword(row: dict) -> str:
    return row["source_facts"]["other_verbatim"]["headword"]


def _normalise_headword(value: str) -> str:
    return " ".join(value.replace("’", "'").split()).casefold()


def _candidate_evidence(worklist: dict) -> dict[str, list[str]]:
    return {
        row["candidate_id"]: row["evidence"]["level_fit"]["matched_all_level_record_ids"]
        for row in worklist["candidates"]
    }


def _course_items(worklist: dict, oxford: list[dict]) -> tuple[list[dict], dict[str, list[str]]]:
    headword_index = defaultdict(list)
    for row in oxford:
        headword_index[_normalise_headword(_headword(row))].append(row["record_id"])
    candidate_evidence = _candidate_evidence(worklist)
    item_to_oxford, rows = {}, []
    for source in ITEMS:
        row = copy.deepcopy(source)
        requested = row.pop("_source_headwords")
        matched = sorted({record_id for word in requested for record_id in headword_index[_normalise_headword(word)]})
        unmatched = sorted({word for word in requested if not headword_index[_normalise_headword(word)]})
        locations = [row["introduction_location"]] + row["recycle_locations"]
        communicative_refs = sorted({ref for location in locations for ref in candidate_evidence.get(location, [])})
        row["source_refs"] = matched + communicative_refs
        row["oxford_source_headwords"] = sorted({_headword(next(item for item in oxford if item["record_id"] == ref)) for ref in matched})
        row["unmatched_source_headwords"] = unmatched
        row["review"] = {"status": "accepted_for_a1_reconciliation", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT}
        item_to_oxford[row["lexical_item_id"]] = matched
        rows.append(row)
    return rows, item_to_oxford


def _is_grammar_owned(row: dict) -> bool:
    facts = row["source_facts"]["other_verbatim"]
    pos = (facts.get("part_of_speech") or "").casefold()
    return _normalise_headword(_headword(row)) in GRAMMAR_HEADWORDS or any(
        value in pos for value in ("article", "pronoun", "preposition", "conjunction", "determiner", "modal", "auxiliary", "prep.", "pron.", "conj.", "det.")
    )


def _oxford_dispositions(oxford: list[dict], item_to_oxford: dict[str, list[str]]) -> list[dict]:
    owners = defaultdict(list)
    for item_id, record_ids in item_to_oxford.items():
        for record_id in record_ids:
            owners[record_id].append(item_id)
    rows = []
    for source in oxford:
        record_id = source["record_id"]
        if owners[record_id]:
            disposition, rationale = "selected_course_item", "supports_selected_meaning_or_function"
        elif _is_grammar_owned(source):
            disposition, rationale = "grammar_system_owned", "function_word_or_grammar_form_owned_in_exact_grammar_pass"
        else:
            disposition, rationale = "reference_pool_not_selected_v1", "not_required_by_current_approved_a1_outcomes_or_bounded_selection"
        facts = source["source_facts"]["other_verbatim"]
        rows.append({
            "source_record_id": record_id, "source_text": source["source"]["source_text"],
            "headword": facts["headword"], "part_of_speech": facts["part_of_speech"],
            "disposition": disposition, "course_item_ids": sorted(owners[record_id]),
            "rationale_code": rationale,
        })
    return rows


def _candidate_rows(worklist: dict, items: list[dict]) -> list[dict]:
    ownership = defaultdict(list)
    for item in items:
        for location in [item["introduction_location"]] + item["recycle_locations"]:
            if location.startswith("lesson_candidate."):
                ownership[location].append(item["lexical_item_id"])
    rows = []
    for candidate in worklist["candidates"]:
        targets = candidate["current_language_targets"]
        if not targets["vocabulary"] and not targets["phrases"]:
            continue
        rows.append({
            "candidate_id": candidate["candidate_id"],
            "legacy_vocabulary_targets": targets["vocabulary"], "legacy_phrase_targets": targets["phrases"],
            "lexical_item_ids": sorted(set(ownership[candidate["candidate_id"]])),
        })
    return rows


def build() -> dict:
    worklist, oxford = _load(WORKLIST), _a1_oxford()
    items, item_to_oxford = _course_items(worklist, oxford)
    dispositions = _oxford_dispositions(oxford, item_to_oxford)
    candidates = _candidate_rows(worklist, items)
    candidate_ids = {row["candidate_id"] for row in worklist["candidates"]}
    function_ids = {row["function_code"] for row in _load(FUNCTIONS)["strands"]}
    used_functions = {value for row in items for value in row["communicative_owner_ids"]}
    locations = {value for row in items for value in [row["introduction_location"]] + row["recycle_locations"]}
    vocab_candidates = {row["candidate_id"] for row in worklist["candidates"] if row["current_language_targets"]["vocabulary"]}
    phrase_candidates = {row["candidate_id"] for row in worklist["candidates"] if row["current_language_targets"]["phrases"]}
    covered_candidates = {row["candidate_id"] for row in candidates if row["lexical_item_ids"]}
    member_lines = [member for row in items for member in row["members"]]
    counts = Counter(row["disposition"] for row in dispositions)
    return {
        "schema_version": 1, "dataset_id": "a1_lexical_chunk_ownership", "version": 1,
        "inputs": [{"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)} for path in INPUTS],
        "policy": {
            "reference_pool_role": "Oxford A1 entry lines are reference evidence, not an automatic word-count promise or lesson checklist.",
            "sense_policy": "Each selected set or chunk states the bounded meaning or function required at A1; unselected senses are not implied.",
            "recycling_policy": "Guided production must be followed by retrieval in a distinct listed context before A1 consolidation.",
            "personalisation_policy": "Open personal categories use bounded learner-relevant slots rather than arbitrary exhaustive lists.",
            "supplement_policy": "A communicative need may justify a bounded form without a direct Oxford A1 line; the candidate evidence is then retained as its source reference.",
        },
        "course_items": items, "oxford_a1_dispositions": dispositions, "candidate_ownership": candidates,
        "audit": {
            "oxford_a1_record_count": len(oxford), "course_item_count": len(items),
            "item_type_counts": dict(sorted(Counter(row["item_type"] for row in items).items())),
            "member_line_count": len(member_lines), "distinct_member_count": len({value.casefold() for value in member_lines}),
            "selected_oxford_record_count": counts["selected_course_item"],
            "grammar_owned_oxford_record_count": counts["grammar_system_owned"],
            "reference_pool_record_count": counts["reference_pool_not_selected_v1"],
            "oxford_disposition_counts": dict(sorted(counts.items())),
            "legacy_vocabulary_candidate_count": len(vocab_candidates), "legacy_phrase_candidate_count": len(phrase_candidates),
            "uncovered_vocabulary_candidate_ids": sorted(vocab_candidates - covered_candidates),
            "uncovered_phrase_candidate_ids": sorted(phrase_candidates - covered_candidates),
            "unknown_candidate_location_ids": sorted(value for value in locations if value.startswith("lesson_candidate.") and value not in candidate_ids),
            "unknown_communicative_owner_ids": sorted(used_functions - function_ids),
            "items_without_source_refs": sorted(row["lexical_item_id"] for row in items if not row["source_refs"]),
            "items_without_recycle_locations": sorted(row["lexical_item_id"] for row in items if not row["recycle_locations"]),
            "items_without_oxford_refs": sorted(row["lexical_item_id"] for row in items if not item_to_oxford[row["lexical_item_id"]]),
            "unmatched_source_headword_request_count": sum(len(row["unmatched_source_headwords"]) for row in items),
            "final_lesson_decisions_made": 0,
        },
        "review": {
            "status": "accepted_exact_lexical_system_pass", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "statement": "Every Oxford A1 row has a disposition and each selected lexical set or chunk has a bounded function, evidence, communicative ownership, fresh recycle location, production expectation, register, and Arabic-learner risk decision.",
        },
    }


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['course_items'])} items; {len(data['oxford_a1_dispositions'])} Oxford rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
