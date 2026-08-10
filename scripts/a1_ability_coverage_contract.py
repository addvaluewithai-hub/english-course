"""Inputs and support ownership for A1 global ability coverage."""

from scripts.a1_outcome_review_contract import OUTPUT as OUTCOME_REVIEW
from scripts.a1_reconciliation_contract import A1_MAP, FUNCTIONS, PROFILES, ROOT, UNIT1
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST


UNIT1_MASTERY = ROOT / "units" / "unit-01-first-connections" / "unit-mastery.json"
OUTPUT = ROOT / "data" / "reviewed" / "a1-ability-coverage-overlap-audit-v1.json"
REPORT = ROOT / "docs" / "A1_ABILITY_COVERAGE_OVERLAP_AUDIT_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-ability-coverage-overlap-audit.schema.json"
INPUTS = (A1_MAP, WORKLIST, OUTCOME_REVIEW, FUNCTIONS, PROFILES, UNIT1, UNIT1_MASTERY)
REVIEWED_AT = "2026-08-10T14:28:12+03:00"
REVIEWER = "codex_primary_curriculum_agent"

SUPPORT_FUNCTION_OWNERS = {
    "clarify_or_repair": ("support.interaction_repair",),
    "control_language_form": ("support.basic_language_control", "support.written_form_control"),
    "infer_meaning": ("support.receptive_processing",),
}

DIMENSIONS = (
    "listening_reception", "reading_reception", "speaking_production",
    "writing_production", "oral_interaction", "written_online_interaction", "mediation",
)
