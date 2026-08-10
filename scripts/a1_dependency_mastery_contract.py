"""Paths and controlled values for the A1 dependency/mastery audit."""

from scripts.a1_ability_coverage_contract import OUTPUT as ABILITY_AUDIT
from scripts.a1_grammar_ownership_contract import OUTPUT as GRAMMAR
from scripts.a1_lexical_ownership_contract import OUTPUT as LEXICAL
from scripts.a1_outcome_review_contract import OUTPUT as OUTCOME_REVIEW
from scripts.a1_pronunciation_ownership_contract import OUTPUT as PRONUNCIATION
from scripts.a1_reconciliation_contract import A1_MAP, PROFILES, ROOT
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST


OUTPUT = ROOT / "data" / "reviewed" / "a1-prerequisite-recycling-mastery-exit-audit-v1.json"
REPORT = ROOT / "docs" / "A1_PREREQUISITE_RECYCLING_MASTERY_EXIT_AUDIT_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-prerequisite-recycling-mastery-exit-audit.schema.json"
INPUTS = (A1_MAP, WORKLIST, OUTCOME_REVIEW, ABILITY_AUDIT, GRAMMAR, LEXICAL, PRONUNCIATION, PROFILES)
REVIEWED_AT = "2026-08-10T15:44:07+03:00"
REVIEWER = "codex_primary_curriculum_agent"

SUPPORT_PROBES = {
    "support.a1_exit_grammar_probe",
    "support.a1_exit_lexical_probe",
    "support.a1_exit_pronunciation_probe",
}

SEQUENCE_STATUSES = (
    "aligned",
    "early_use_requires_introduction_transfer_or_reorder",
    "no_later_recycle_requires_reorder_or_new_recycle",
)
