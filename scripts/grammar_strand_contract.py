"""Paths and review metadata for grammar family strands."""

from scripts.source_disposition_contract import ROOT


EGP = ROOT / "data" / "derived" / "egp-all-levels.json"
GSE_GRAMMAR = ROOT / "data" / "derived" / "gse-grammar-all.json"
DISPOSITIONS = ROOT / "data" / "reviewed" / "source-dispositions-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "grammar-family-strands-v1.json"
REPORT = ROOT / "docs" / "GRAMMAR_FAMILY_PROGRESSION_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "grammar-family-strands.schema.json"
REVIEWED_AT = "2026-08-10T13:18:23+03:00"
REVIEWER = "codex_primary_curriculum_agent"
LEVELS = ("pre_a1", "a1", "a2", "b1", "b2", "c1", "c2")
EXIT_LEVELS = LEVELS[1:]
LIFECYCLE = ("expose", "introduce", "practise", "recycle", "consolidate", "extend")
