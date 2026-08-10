"""Paths and policy constants for the locked A1 scope and sequence."""

from scripts.a1_ability_coverage_contract import OUTPUT as ABILITY_AUDIT
from scripts.a1_dependency_mastery_contract import OUTPUT as DEPENDENCY_AUDIT
from scripts.a1_final_decisions_contract import OUTPUT as FINAL_DECISIONS
from scripts.a1_grammar_ownership_contract import OUTPUT as GRAMMAR
from scripts.a1_lexical_ownership_contract import OUTPUT as LEXICAL
from scripts.a1_pronunciation_ownership_contract import OUTPUT as PRONUNCIATION
from scripts.a1_reconciliation_contract import PROFILES, ROOT, UNIT1
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST


GOLD_MANIFEST = ROOT / "gold" / "introduce-yourself" / "lesson-manifest.json"
OUTPUT = ROOT / "data" / "reviewed" / "a1-scope-and-sequence-v1.json"
REPORT = ROOT / "docs" / "A1_SCOPE_AND_SEQUENCE_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-scope-and-sequence.schema.json"
INPUTS = (
    FINAL_DECISIONS, WORKLIST, DEPENDENCY_AUDIT, ABILITY_AUDIT, PROFILES,
    GRAMMAR, LEXICAL, PRONUNCIATION, UNIT1, GOLD_MANIFEST,
)
REVIEWED_AT = "2026-08-10T16:16:49+03:00"
REVIEWER = "codex_primary_curriculum_agent"
EXIT_PROBE_ID = "assessment.a1_exit_language_probe"
POLITENESS_SUPPORT_ID = "support.a1_politeness_control"
