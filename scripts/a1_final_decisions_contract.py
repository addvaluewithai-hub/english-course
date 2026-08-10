"""Paths and controlled values for final A1 candidate dispositions."""

from scripts.a1_ability_coverage_contract import OUTPUT as ABILITY_AUDIT
from scripts.a1_dependency_mastery_contract import OUTPUT as DEPENDENCY_AUDIT
from scripts.a1_grammar_ownership_contract import OUTPUT as GRAMMAR
from scripts.a1_lexical_ownership_contract import OUTPUT as LEXICAL
from scripts.a1_outcome_review_contract import OUTPUT as OUTCOME_REVIEW
from scripts.a1_pronunciation_ownership_contract import OUTPUT as PRONUNCIATION
from scripts.a1_reconciliation_contract import ROOT
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST


OUTPUT = ROOT / "data" / "reviewed" / "a1-final-candidate-decisions-v1.json"
REPORT = ROOT / "docs" / "A1_FINAL_CANDIDATE_DECISIONS_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-final-candidate-decisions.schema.json"
INPUTS = (WORKLIST, OUTCOME_REVIEW, ABILITY_AUDIT, GRAMMAR, LEXICAL, PRONUNCIATION, DEPENDENCY_AUDIT)
REVIEWED_AT = "2026-08-10T16:05:50+03:00"
REVIEWER = "codex_primary_curriculum_agent"
DECISION_CODES = ("keep", "revise", "merge", "support_only", "split")
SUPPORT_OWNER_IDS = {"support.a1_politeness_control"}
