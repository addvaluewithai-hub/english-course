"""Paths and evidence-role rules for reviewed level-exit bundles."""

from pathlib import Path

from scripts.source_disposition_contract import REVIEWED_AT, REVIEWER, ROOT


DISPOSITIONS = ROOT / "data" / "reviewed" / "source-dispositions-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "level-exit-evidence-v1.json"
SCHEMA = ROOT / "schemas" / "curriculum" / "level-exit-evidence.schema.json"
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")

EVIDENCE_ROLES = {
    "cefr_all_descriptors": "primary_level_boundary",
    "gse_all_objectives": "granular_communicative_cross_check",
    "egp_all_levels": "grammar_feature_pool",
    "gse_grammar_all": "productive_grammar_cross_check",
    "oxford_3000_all": "lexical_reference_pool",
    "oxford_5000_all": "lexical_reference_pool",
}

SOURCE_DATASETS = tuple(EVIDENCE_ROLES)


def bundle_id(dataset_id: str, level: str, strand: str) -> str:
    return f"{dataset_id}.{level}.{strand}"
