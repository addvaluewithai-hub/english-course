"""Stable inputs and decision vocabulary for A1 reconciliation."""

from scripts.source_disposition_contract import ROOT


A1_MAP = ROOT / "data" / "reviewed" / "a1-lesson-map.json"
UNIT1 = ROOT / "units" / "unit-01-first-connections" / "unit-manifest.json"
TAGS = ROOT / "data" / "reviewed" / "communicative-tag-assignments-v1.json"
ALL_GSE = ROOT / "data" / "derived" / "gse-all-objectives.json"
ALL_CEFR = ROOT / "data" / "derived" / "cefr-all-descriptors.json"
PROFILES = ROOT / "data" / "reviewed" / "level-exit-profiles-v1.json"
FUNCTIONS = ROOT / "data" / "reviewed" / "communicative-function-strands-v1.json"
GRAMMAR = ROOT / "data" / "reviewed" / "grammar-family-strands-v1.json"
LEXICAL = ROOT / "data" / "reviewed" / "lexical-progression-strands-v1.json"
PRONUNCIATION = ROOT / "data" / "reviewed" / "pronunciation-progression-strands-v1.json"
PERFORMANCE = ROOT / "data" / "reviewed" / "performance-complexity-strands-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "a1-reconciliation-worklist-v1.json"
REPORT = ROOT / "docs" / "A1_RECONCILIATION_WORKLIST_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-reconciliation-worklist.schema.json"

INPUTS = (
    A1_MAP, UNIT1, TAGS, ALL_GSE, ALL_CEFR, PROFILES, FUNCTIONS,
    GRAMMAR, LEXICAL, PRONUNCIATION, PERFORMANCE,
)
DECISIONS = ("keep", "revise", "split", "merge", "defer", "support_only", "replace", "retire")
REVIEW_PASSES = (
    "outcome_and_level_fit",
    "global_ability_coverage",
    "grammar_ownership",
    "vocabulary_and_chunk_ownership",
    "pronunciation_progression",
    "sequence_and_recycling",
    "mastery_and_exit_assessment",
)

REVIEWED_AT = "2026-08-10T14:10:00+03:00"
REVIEWER = "codex_primary_curriculum_agent"
