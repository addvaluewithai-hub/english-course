"""Build curriculum source records from parsed Oxford word-list entries."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

try:
    from scripts.oxford_wordlist_parser import WordEntry
except ModuleNotFoundError:
    from oxford_wordlist_parser import WordEntry


SOURCE_META = {
    "oxford_3000": {
        "source_id": "oup.oxford_3000_by_cefr",
        "raw_file": "sources/raw/vocabulary/oxford-3000-by-cefr-level.pdf",
        "sha256": "B81E3F65C976FC93EB342BA34C40F0FF8C3A59646312D09AC50F9C648E461CD3",
    },
    "oxford_5000": {
        "source_id": "oup.oxford_5000_by_cefr",
        "raw_file": "sources/raw/vocabulary/oxford-5000-by-cefr-level.pdf",
        "sha256": "6577E6EB8745226AB7AB80912E83D285CF421EC70E61C92D74D5FEF5F2C99570",
    },
}


def _repetitions(rows: list[WordEntry]) -> dict[str, list[WordEntry]]:
    groups: dict[str, list[WordEntry]] = defaultdict(list)
    for row in rows:
        groups[row.source_text].append(row)
    return {text: items for text, items in groups.items() if len(items) > 1}


def _record(row: WordEntry, repeated: list[WordEntry] | None) -> dict[str, Any]:
    meta = SOURCE_META[row.list_id]
    warning = None
    if repeated:
        locations = ", ".join(f"{item.level_text} page {item.page}" for item in repeated)
        warning = f"The source repeats this exact lexical entry at: {locations}."
    issues = [] if not warning else [
        {"code": "source_repetition", "severity": "warning", "message": warning}
    ]
    prefix = "o3000" if row.list_id == "oxford_3000" else "o5000"
    return {
        "record_id": f"oxford.{prefix}.p{row.page:02d}.{row.ordinal_on_page:03d}",
        "record_kind": "vocabulary_item",
        "source": {
            "source_id": meta["source_id"], "source_version": "published PDF snapshot",
            "raw_file": meta["raw_file"], "source_file_sha256": meta["sha256"],
            "location": {
                "kind": "pdf_page", "page": row.page, "page_end": row.page,
                "printed_page": str(row.page), "section": row.level_text,
            },
            "source_text": row.source_text,
            "source_text_sha256": hashlib.sha256(row.source_text.encode("utf-8")).hexdigest(),
            "transcription_notes": [
                "Reconstructed from a single visual PDF line to preserve complete headword and part of speech."
            ],
        },
        "source_facts": {
            "source_record_id": None, "level_text": row.level_text,
            "gse_score_or_range": None, "skill_text": "Vocabulary",
            "mode_text": None, "function_text": None,
            "scale_text": row.list_id.replace("_", " ").title(),
            "other_verbatim": {
                "headword_source": row.headword_source, "headword": row.headword,
                "homograph_number": row.homograph_number,
                "qualifier": row.qualifier, "part_of_speech": row.part_of_speech,
            },
        },
        "interpretation": {
            "inclusion_status": "undecided", "exclusion_reason": None,
            "cefr_codes": [row.cefr_code], "skill_codes": ["language_system"],
            "mode_codes": [], "function_codes": [], "candidate_cluster_ids": [],
            "notes": [
                "Levelled lexical-pool evidence retained; listing does not make this an automatic target."
            ],
            "ambiguities": [warning] if warning else [],
        },
        "review": {
            "status": "unreviewed", "reviewer": None, "reviewed_at": None,
            "issues": issues,
        },
    }


def build_collection(rows: list[WordEntry]) -> dict[str, Any]:
    repeated = _repetitions(rows)
    records = [_record(row, repeated.get(row.source_text)) for row in rows]
    dataset = "oxford_3000_all" if rows[0].list_id == "oxford_3000" else "oxford_5000_all"
    return {"schema_version": "1.0.0", "dataset_id": dataset, "records": records}
