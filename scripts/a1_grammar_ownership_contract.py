"""Paths and controlled vocabularies for the A1 grammar ownership pass."""

from pathlib import Path

from scripts.a1_ability_coverage_contract import OUTPUT as ABILITY_AUDIT
from scripts.a1_outcome_review_contract import OUTPUT as OUTCOME_REVIEW
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST
from scripts.a1_reconciliation_contract import ROOT


EGP = ROOT / "data" / "derived" / "egp-all-levels.json"
GSE_GRAMMAR = ROOT / "data" / "derived" / "gse-grammar-all.json"
GRAMMAR_FAMILIES = ROOT / "data" / "reviewed" / "grammar-family-strands-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "a1-grammar-coverage-ownership-v1.json"
REPORT = ROOT / "docs" / "A1_GRAMMAR_COVERAGE_OWNERSHIP_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-grammar-coverage-ownership.schema.json"
INPUTS = (EGP, GSE_GRAMMAR, GRAMMAR_FAMILIES, WORKLIST, OUTCOME_REVIEW, ABILITY_AUDIT)
REVIEWED_AT = "2026-08-10T14:50:00+03:00"
REVIEWER = "codex_primary_curriculum_agent"

DISPOSITIONS = (
    "selected_core",
    "selected_limited",
    "folded_duplicate",
    "support_not_separate",
    "transfer_phrase_layer",
    "transfer_lexical_layer",
    "transfer_writing_support",
)

CONTROL_STATUSES = (
    "productive_core",
    "productive_limited",
    "formulaic_productive",
    "receptive_formulaic",
    "embedded_support",
)

SUPPORT_OWNER_IDS = {
    "support.a1_exit_grammar_probe",
    "support.basic_language_control",
    "support.lexical_syllabus",
    "support.phrase_syllabus",
    "support.written_form_control",
}
