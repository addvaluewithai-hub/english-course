"""Paths and primary source ownership for the SPINE-004 completion audit."""

from scripts.source_disposition_contract import ROOT


DISPOSITIONS = ROOT / "data" / "reviewed" / "source-dispositions-v1.json"
COMMUNICATIVE = ROOT / "data" / "reviewed" / "communicative-function-strands-v1.json"
GRAMMAR = ROOT / "data" / "reviewed" / "grammar-family-strands-v1.json"
LEXICAL = ROOT / "data" / "reviewed" / "lexical-progression-strands-v1.json"
PRONUNCIATION = ROOT / "data" / "reviewed" / "pronunciation-progression-strands-v1.json"
PERFORMANCE = ROOT / "data" / "reviewed" / "performance-complexity-strands-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "spine-004-completion-audit-v1.json"
REPORT = ROOT / "docs" / "SPINE_004_COMPLETION_AUDIT.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "spine-004-completion-audit.schema.json"
REVIEWED_AT = "2026-08-10T14:04:49+03:00"
REVIEWER = "codex_primary_curriculum_agent"

PRIMARY_PARTITIONS = {
    "communicative_boundary_evidence": ("cefr_all_descriptors", "gse_all_objectives"),
    "grammar_system_evidence": ("egp_all_levels", "gse_grammar_all"),
    "lexical_reference_evidence": ("oxford_3000_all", "oxford_5000_all"),
}
