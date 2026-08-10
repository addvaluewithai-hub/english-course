"""Paths and fixed review metadata for all-level communicative tags."""

from scripts.source_disposition_contract import ROOT


CEFR = ROOT / "data" / "derived" / "cefr-all-descriptors.json"
GSE = ROOT / "data" / "derived" / "gse-all-objectives.json"
DISPOSITIONS = ROOT / "data" / "reviewed" / "source-dispositions-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "communicative-tag-assignments-v1.json"
REPORT = ROOT / "docs" / "COMMUNICATIVE_TAG_AUDIT_ALL_LEVELS.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "communicative-tag-assignments.schema.json"
REVIEWED_AT = "2026-08-10T13:18:23+03:00"
REVIEWER = "codex_primary_curriculum_agent"
