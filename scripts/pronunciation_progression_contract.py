"""Paths and stable values for the pronunciation-progression contract."""

from scripts.source_disposition_contract import ROOT


DISPOSITIONS = ROOT / "data" / "reviewed" / "source-dispositions-v1.json"
PROFILES = ROOT / "data" / "reviewed" / "level-exit-profiles-v1.json"
DECISIONS = ROOT / "docs" / "DECISIONS.md"
OUTPUT = ROOT / "data" / "reviewed" / "pronunciation-progression-strands-v1.json"
REPORT = ROOT / "docs" / "PRONUNCIATION_PROGRESSION_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "pronunciation-progression-strands.schema.json"
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
REVIEWED_AT = "2026-08-10T14:04:49+03:00"
REVIEWER = "codex_primary_curriculum_agent"

ASSESSMENT_RULES = (
    "Assess intelligibility inside fresh communicative performance; isolated imitation may diagnose but cannot prove mastery.",
    "Score listener effort, preservation of key meaning, segmental clarity, stress and prominence, chunking, and repair at the level boundary.",
    "Keep receptive sound discrimination separate from productive pronunciation control.",
    "Permit the clarification and repair support named by the learner's level; do not silently score an A1 speaker as C2.",
    "Never deduct for a retained accent when meaning, intelligibility, effectiveness, and situational appropriateness are preserved.",
)
