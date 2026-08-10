"""Paths and claim-to-evidence rules for approved exit profiles."""

from scripts.level_exit_evidence_contract import OUTPUT as EVIDENCE, bundle_id
from scripts.source_disposition_contract import REVIEWED_AT, REVIEWER, ROOT


PROPOSAL = ROOT / "data" / "reviewed" / "level-exit-profiles-v0.json"
OUTPUT = ROOT / "data" / "reviewed" / "level-exit-profiles-v1.json"
REPORT = ROOT / "docs" / "LEVEL_EXIT_PROFILES_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "level-exit-profiles-v1.schema.json"
CLAIM_SCHEMA = ROOT / "schemas" / "curriculum" / "profile-claim.schema.json"

LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
EXPECTED_GSE = {
    "a1": "22-29", "a2": "30-42", "b1": "43-58",
    "b2": "59-75", "c1": "76-84", "c2": "85-90",
}

CLAIM_STRANDS = {
    "reception.listening": "listening_reception",
    "reception.reading": "reading_reception",
    "production.speaking": "speaking_production",
    "production.writing": "writing_production",
    "interaction.oral": "oral_interaction",
    "interaction.written_online": "written_online_interaction",
    "interaction.mediation": "mediation",
    "language_control.range": "language_range",
    "language_control.grammar": "grammar",
    "language_control.vocabulary": "vocabulary",
    "language_control.pronunciation": "pronunciation",
    "language_control.discourse": "discourse",
    "language_control.fluency": "fluency",
}


def source_bundle(dataset_id: str, level: str, strand: str) -> str:
    return bundle_id(dataset_id, level, strand)
