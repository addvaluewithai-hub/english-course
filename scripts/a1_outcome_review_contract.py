"""Contract for the first A1 reconciliation pass: outcome and level fit."""

from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST
from scripts.a1_reconciliation_contract import PROFILES, FUNCTIONS, PERFORMANCE, ROOT


OUTPUT = ROOT / "data" / "reviewed" / "a1-outcome-level-fit-review-v1.json"
REPORT = ROOT / "docs" / "A1_OUTCOME_LEVEL_FIT_REVIEW_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-outcome-level-fit-review.schema.json"
INPUTS = (WORKLIST, PROFILES, FUNCTIONS, PERFORMANCE)
FIT_STATUSES = ("fits_a1_boundary", "fits_a1_with_scope_revision", "not_a1_defer_review")
INDEPENDENCE_SIGNALS = (
    "standalone_plausible", "merge_review", "support_only_review",
    "unit_synthesis_review", "split_review", "replace_or_reframe_review",
)
RISK_CODES = (
    "ambiguous_language_direction", "assessment_channel_ambiguous", "channel_or_mode_mismatch",
    "compound_scope", "content_scope_vague", "cross_cutting_support", "generic_strategy_not_context_owned",
    "label_outcome_mismatch", "micro_move", "overlap_likely", "prepared_text_support_contradiction",
)
REVIEWED_AT = "2026-08-10T14:24:00+03:00"
REVIEWER = "codex_primary_curriculum_agent"
