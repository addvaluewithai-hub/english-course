"""Build a compact traceable v2 source packet for U1-L03."""

from scripts.gold_v1_contract import (
    CANDIDATE_ID, LESSON_ID, REQUIRED_INTRODUCTIONS, REQUIRED_RECYCLES,
    REVIEWED_AT, REVIEWER, ROOT, SOURCE_INPUTS, UNIT_ID,
)
from scripts.source_disposition_inputs import file_sha256


BOUNDED_FORM_SCOPE = {
    "grammar.basic_clause_order": "subject-first short identity statements",
    "grammar.possessive_forms": "my + name only at first introduction",
    "grammar.articles": "a/an + selected job only at first introduction",
    "lexical.own_country_nationality": "the learner's own pair, not a world list",
    "lexical.self_introduction_frames": "select relevant slots; never memorise one paragraph",
    "a1_pronunciation.lesson_critical_word_stress": "selected country, job, and interest words",
    "a1_pronunciation.sense_group_chunking": "one safe pause between short information groups",
}


def _evidence(item_id: str, grammar: dict, lexical: dict, pronunciation: dict) -> dict:
    if item_id.startswith("grammar."):
        row = next(item for item in grammar["course_items"] if item["item_id"] == item_id)
        refs = row["source_evidence"]["egp_feature_ids"] + row["source_evidence"]["gse_grammar_record_ids"]
        return {"label": row["title"], "source_refs": refs, "later_boundary": row["not_yet"]}
    if item_id.startswith("lexical."):
        row = next(item for item in lexical["course_items"] if item["lexical_item_id"] == item_id)
        return {"label": row["canonical_form"], "source_refs": row["source_refs"], "later_boundary": row["productive_expectation"]}
    row = next(item for item in pronunciation["targets"] if item["target_id"] == item_id)
    return {"label": row["title"], "source_refs": row["source_refs"], "later_boundary": row["not_yet"]}


def build(scope: dict, final: dict, grammar: dict, lexical: dict, pronunciation: dict) -> dict:
    lesson = next(
        lesson for unit in scope["units"] for lesson in unit["lessons"]
        if lesson["final_owner_id"] == CANDIDATE_ID
    )
    placements = {row["item_id"]: row for row in scope["exact_item_placements"]}
    introduced = sorted(item for item in REQUIRED_INTRODUCTIONS if placements[item]["final_introduction_location_id"] == CANDIDATE_ID)
    recycled = sorted(item for item in REQUIRED_RECYCLES if placements[item]["first_fresh_recycle_location_id"] == CANDIDATE_ID)
    capability = next(row for row in final["final_lesson_capabilities"] if row["final_owner_id"] == CANDIDATE_ID)
    return {
        "schema_version": 2, "packet_id": "a1.v1.U1-L03.sources", "lesson_id": LESSON_ID,
        "unit_id": UNIT_ID, "candidate_id": CANDIDATE_ID,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in SOURCE_INPUTS
        ],
        "outcome_statement": lesson["outcome_statement"],
        "source_candidate_ids": capability["source_candidate_ids"],
        "prior_lesson_owners": [
            "lesson_candidate.open_and_close_a_basic_social_exchange",
            "lesson_candidate.understand_spoken_personal_introductions",
        ],
        "exact_introductions": [
            {"item_id": item, "bounded_scope": BOUNDED_FORM_SCOPE[item], **_evidence(item, grammar, lexical, pronunciation)}
            for item in introduced
        ],
        "exact_recycles": [
            {"item_id": item, **_evidence(item, grammar, lexical, pronunciation)}
            for item in recycled
        ],
        "mastery": {
            "fresh_task": "Give a four-detail self-introduction in a changed first-meeting context.",
            "support_boundary": "Field labels only; no complete sentence frame or answer-bearing model.",
            "critical_meaning": "The listener can identify the person and every required detail.",
        },
        "legacy_packet": {
            "path": "gold/introduce-yourself/source-packet.json",
            "sha256": file_sha256(SOURCE_INPUTS[-1]),
            "status": "preserved_as_traceable_prototype_input",
        },
        "review": {"status": "accepted_for_gold_v1_qa", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT},
    }
