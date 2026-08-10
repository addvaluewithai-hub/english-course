"""Paths and stable vocabulary-progression contract values."""

from scripts.source_disposition_contract import ROOT


OXFORD_3000 = ROOT / "data" / "derived" / "oxford-3000-all.json"
OXFORD_5000 = ROOT / "data" / "derived" / "oxford-5000-all.json"
PROFILES = ROOT / "data" / "reviewed" / "level-exit-profiles-v1.json"
FUNCTIONS = ROOT / "data" / "reviewed" / "communicative-function-strands-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "lexical-progression-strands-v1.json"
REPORT = ROOT / "docs" / "LEXICAL_PROGRESSION_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "lexical-progression-strands.schema.json"
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
DATASETS = ("oxford_3000_all", "oxford_5000_all")
REVIEWED_AT = "2026-08-10T14:04:49+03:00"
REVIEWER = "codex_primary_curriculum_agent"

REQUIRED_ITEM_FIELDS = (
    "lexical_item_id",
    "canonical_form",
    "item_type",
    "meaning_or_function",
    "communicative_owner_ids",
    "source_refs",
    "first_exposure_level",
    "first_guided_production_level",
    "consolidation_level",
    "recycle_locations",
    "receptive_expectation",
    "productive_expectation",
    "register",
    "collocations_or_frames",
    "arabic_learner_risks",
    "decision_rationale",
    "review",
)
