"""Paths and fixed boundaries for migrating the accepted gold lesson to A1 v1."""

from scripts.a1_final_decisions_contract import OUTPUT as FINAL_DECISIONS
from scripts.a1_grammar_ownership_contract import OUTPUT as GRAMMAR
from scripts.a1_lexical_ownership_contract import OUTPUT as LEXICAL
from scripts.a1_pronunciation_ownership_contract import OUTPUT as PRONUNCIATION
from scripts.a1_reconciliation_contract import ROOT
from scripts.a1_scope_sequence_contract import OUTPUT as SCOPE_SEQUENCE


LEGACY = ROOT / "gold" / "introduce-yourself"
OUTPUT = ROOT / "units" / "a1-v1" / "unit-01-first-connections" / "lessons" / "u1-l03"
QA_OUTPUT = ROOT / "data" / "reviewed" / "gold-lesson-v1-qa.json"
QA_REPORT = ROOT / "docs" / "GOLD_LESSON_V1_QA.md"
SOURCE_INPUTS = (
    SCOPE_SEQUENCE, FINAL_DECISIONS, GRAMMAR, LEXICAL, PRONUNCIATION,
    LEGACY / "source-packet.json",
)
REVIEWED_AT = "2026-08-10T16:37:00+03:00"
REVIEWER = "codex_primary_curriculum_agent"
CANDIDATE_ID = "lesson_candidate.give_short_self_introduction"
LESSON_ID = "U1-L03"
UNIT_ID = "a1.unit01.first_connections"

REQUIRED_INTRODUCTIONS = {
    "grammar.basic_clause_order", "grammar.possessive_forms", "grammar.articles",
    "lexical.own_country_nationality", "lexical.self_introduction_frames",
    "a1_pronunciation.lesson_critical_word_stress", "a1_pronunciation.sense_group_chunking",
}
REQUIRED_RECYCLES = {
    "grammar.be_affirmative", "grammar.personal_pronouns", "lexical.identity_place_labels",
}
