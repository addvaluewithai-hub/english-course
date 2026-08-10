"""Build source records for the Pearson GSE Grammar inventory."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

try:
    from scripts.gse_grammar_parser import GrammarEntry
except ModuleNotFoundError:
    from gse_grammar_parser import GrammarEntry


SOURCE_ID = "pearson.gse_grammar_adult_2023"
SOURCE_VERSION = "2023"
RAW_FILE = "sources/raw/grammar/gse-grammar-guide-adult-framework.pdf"
RAW_SHA256 = "5F25E7603BD03DFA3D771BBFDCD36C123CA971DA34F81B29457A1D35C45B6BA9"


def _repetitions(rows: list[GrammarEntry]) -> dict[str, list[GrammarEntry]]:
    groups: dict[str, list[GrammarEntry]] = defaultdict(list)
    for row in rows:
        groups[row.objective].append(row)
    return {text: items for text, items in groups.items() if len(items) > 1}


def _record(row: GrammarEntry, repeated: list[GrammarEntry] | None) -> dict[str, Any]:
    warning = None
    if repeated:
        locations = ", ".join(f"GSE {item.score} page {item.page}" for item in repeated)
        warning = f"The source repeats this exact grammar objective at: {locations}."
    issues = [] if not warning else [
        {"code": "source_repetition", "severity": "warning", "message": warning}
    ]
    notes = ["Productive grammar evidence retained; curriculum disposition is pending SPINE-003."]
    if row.level_text.endswith("+"):
        notes.append("Pearson plus band is preserved and mapped to its base CEFR code.")
    return {
        "record_id": f"gse.grammar.2023.p{row.page:02d}.{row.ordinal_on_page:03d}",
        "record_kind": "grammar_feature",
        "source": {
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "raw_file": RAW_FILE,
            "source_file_sha256": RAW_SHA256,
            "location": {
                "kind": "pdf_page", "page": row.page, "page_end": row.page,
                "printed_page": str(row.page), "section": row.printed_level_heading,
            },
            "source_text": row.objective,
            "source_text_sha256": hashlib.sha256(row.objective.encode("utf-8")).hexdigest(),
            "transcription_notes": list(row.transcription_notes),
        },
        "source_facts": {
            "source_record_id": None,
            "level_text": row.level_text,
            "gse_score_or_range": str(row.score),
            "skill_text": "Grammar",
            "mode_text": "Productive use",
            "function_text": None,
            "scale_text": "GSE Grammar for adult learners",
            "other_verbatim": {
                "structure": row.structure,
                "example": row.example,
                "grammatical_categories": row.categories,
                "printed_level_heading": row.printed_level_heading,
            },
        },
        "interpretation": {
            "inclusion_status": "undecided", "exclusion_reason": None,
            "cefr_codes": [row.cefr_code], "skill_codes": ["language_system"],
            "mode_codes": ["production"], "function_codes": ["control_language_form"],
            "candidate_cluster_ids": [], "notes": notes,
            "ambiguities": [warning] if warning else [],
        },
        "review": {
            "status": "unreviewed", "reviewer": None, "reviewed_at": None,
            "issues": issues,
        },
    }


def build_collection(rows: list[GrammarEntry]) -> dict[str, Any]:
    repeated = _repetitions(rows)
    records = [_record(row, repeated.get(row.objective)) for row in rows]
    return {"schema_version": "1.0.0", "dataset_id": "gse_grammar_all", "records": records}
