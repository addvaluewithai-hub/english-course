"""Shared paths and reviewed policy metadata for source dispositions."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"
OUTPUT = ROOT / "data" / "reviewed" / "source-dispositions-v1.json"
REPORT = ROOT / "docs" / "SOURCE_DISPOSITION_AUDIT.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "source-dispositions.schema.json"

REVIEWED_AT = "2026-08-10T12:54:12+03:00"
REVIEWER = "codex_primary_curriculum_agent"

DATASET_FILES = {
    "cefr_all_descriptors": "cefr-all-descriptors.json",
    "gse_all_objectives": "gse-all-objectives.json",
    "egp_all_levels": "egp-all-levels.json",
    "gse_grammar_all": "gse-grammar-all.json",
    "oxford_3000_all": "oxford-3000-all.json",
    "oxford_5000_all": "oxford-5000-all.json",
}

POLICIES = {
    "cefr_boundary_v1": {
        "source_role": "level_boundary_evidence",
        "base_disposition": "supporting_evidence",
        "rationale": (
            "CEFR descriptors define activity, competence, and qualitative level "
            "boundaries; they support the spine but are not a lesson inventory."
        ),
    },
    "gse_communicative_v1": {
        "source_role": "communicative_target_evidence",
        "base_disposition": "include_for_spine",
        "rationale": (
            "Adult GSE objectives are granular evidence for communicative progression; "
            "published scores remain source facts rather than automatic lesson owners."
        ),
    },
    "egp_grammar_v1": {
        "source_role": "language_system_evidence",
        "base_disposition": "include_for_spine",
        "rationale": (
            "EGP features are productively attested grammar evidence to reconcile with "
            "communicative need; inclusion does not make each feature a lesson."
        ),
    },
    "gse_grammar_v1": {
        "source_role": "language_system_evidence",
        "base_disposition": "include_for_spine",
        "rationale": (
            "GSE Grammar is a productive grammar cross-check; exact ownership is a "
            "later progression-strand decision."
        ),
    },
    "oxford_3000_pool_v1": {
        "source_role": "lexical_reference_pool",
        "base_disposition": "reference_pool",
        "rationale": (
            "Oxford 3000 supplies a levelled lexical pool through B2, not an automatic "
            "target list or teaching order."
        ),
    },
    "oxford_5000_pool_v1": {
        "source_role": "lexical_reference_pool",
        "base_disposition": "reference_pool",
        "rationale": (
            "Oxford 5000 supplies additional B2-C1 lexical evidence, not an automatic "
            "target list and not a C2 lexical specification."
        ),
    },
}

DATASET_POLICIES = {
    "cefr_all_descriptors": "cefr_boundary_v1",
    "gse_all_objectives": "gse_communicative_v1",
    "egp_all_levels": "egp_grammar_v1",
    "gse_grammar_all": "gse_grammar_v1",
    "oxford_3000_all": "oxford_3000_pool_v1",
    "oxford_5000_all": "oxford_5000_pool_v1",
}
