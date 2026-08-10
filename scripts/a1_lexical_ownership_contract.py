"""Paths and policy constants for exact A1 lexical and chunk ownership."""

from scripts.a1_grammar_ownership_contract import OUTPUT as GRAMMAR_OWNERSHIP
from scripts.a1_reconciliation_contract import FUNCTIONS, ROOT
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST


OXFORD = ROOT / "data" / "derived" / "oxford-3000-all.json"
LEXICAL_STRANDS = ROOT / "data" / "reviewed" / "lexical-progression-strands-v1.json"
OUTPUT = ROOT / "data" / "reviewed" / "a1-lexical-chunk-ownership-v1.json"
REPORT = ROOT / "docs" / "A1_LEXICAL_CHUNK_OWNERSHIP_V1.md"
SCHEMA = ROOT / "schemas" / "curriculum" / "a1-lexical-chunk-ownership.schema.json"
INPUTS = (OXFORD, LEXICAL_STRANDS, WORKLIST, GRAMMAR_OWNERSHIP, FUNCTIONS)
REVIEWED_AT = "2026-08-10T15:15:00+03:00"
REVIEWER = "codex_primary_curriculum_agent"

ITEM_TYPES = ("lexical_set", "chunk_set", "frame_set", "personalized_slot")
REGISTERS = ("neutral", "neutral_polite", "informal_neutral", "public_notice", "form_label")
OXFORD_DISPOSITIONS = (
    "selected_course_item",
    "grammar_system_owned",
    "reference_pool_not_selected_v1",
)

GRAMMAR_HEADWORDS = {
    "a, an", "all", "always", "an", "and", "any", "be", "because", "but", "can", "could",
    "do", "each", "every", "have", "he", "her", "him", "his", "how", "i", "in",
    "it", "its", "may", "me", "might", "my", "of", "on", "or", "our", "she",
    "not", "really", "some", "sometimes", "that", "the", "their", "them", "there", "these", "they", "this", "to",
    "us", "very", "we", "what", "when", "where", "which", "who", "will", "with",
    "would", "you", "your",
}
