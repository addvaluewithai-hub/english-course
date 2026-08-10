"""Paths and ordered levels for communicative-function strands."""

from scripts.communicative_tag_contract import OUTPUT as TAGS
from scripts.level_exit_profile_contract import OUTPUT as PROFILES
from scripts.source_disposition_contract import ROOT


OUTPUT = ROOT / "data" / "reviewed" / "communicative-function-strands-v1.json"
REPORT = ROOT / "docs" / "COMMUNICATIVE_FUNCTION_PROGRESSION_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "communicative-function-strands.schema.json"
REVIEWED_AT = "2026-08-10T13:18:23+03:00"
REVIEWER = "codex_primary_curriculum_agent"
LEVELS = ("pre_a1", "a1", "a2", "b1", "b2", "c1", "c2")
EXIT_LEVELS = LEVELS[1:]
LIFECYCLE = ("expose", "introduce", "practise", "recycle", "consolidate", "extend")
