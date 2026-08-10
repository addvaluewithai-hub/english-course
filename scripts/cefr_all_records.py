"""Build source-record collections for all CEFR illustrative descriptors."""

from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from typing import Any

try:
    from scripts.cefr_all_parser import Descriptor
except ModuleNotFoundError:
    from cefr_all_parser import Descriptor


SOURCE_ID = "coe.cefr_companion_2020_en"
SOURCE_VERSION = "2020"
RAW_FILE = "sources/raw/frameworks/cefr-companion-2020-en.pdf"
RAW_SHA256 = "BFBD8C74090419AC4B9B352D6BA26E180713B31F45265D7D775B7C36DD7AD1B1"


def _slug(value: str) -> str:
    return "_".join(re.findall(r"[a-z0-9]+", value.lower())[:7])


def _repetitions(rows: list[Descriptor]) -> dict[tuple[str, str], list[Descriptor]]:
    groups: dict[tuple[str, str], list[Descriptor]] = defaultdict(list)
    for row in rows:
        groups[(row.level_text, row.text)].append(row)
    return {key: values for key, values in groups.items() if len(values) > 1}


def _record_id(row: Descriptor) -> str:
    return (
        f"cefr.cv2020.p{row.page:03d}.{_slug(row.level_text)}."
        f"{_slug(row.scale)}.{row.ordinal_in_level_scale:03d}"
    )


def _record(row: Descriptor, repeated: list[Descriptor] | None) -> dict[str, Any]:
    warning = None
    if repeated:
        contexts = ", ".join(f"{item.scale} page {item.page}" for item in repeated)
        warning = f"The source repeats this exact {row.level_text} wording in: {contexts}."
    notes = ["Source evidence retained; curriculum disposition is pending SPINE-003."]
    if row.level_text.endswith("+"):
        notes.append("CEFR plus-level label is preserved and mapped to its base CEFR code.")
    issues = [] if not warning else [
        {"code": "source_repetition", "severity": "warning", "message": warning}
    ]
    return {
        "record_id": _record_id(row),
        "record_kind": "descriptor",
        "source": {
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "raw_file": RAW_FILE,
            "source_file_sha256": RAW_SHA256,
            "location": {
                "kind": "pdf_page",
                "page": row.page,
                "page_end": row.page,
                "printed_page": str(row.page),
                "section": row.scale,
            },
            "source_text": row.text,
            "source_text_sha256": hashlib.sha256(row.text.encode("utf-8")).hexdigest(),
            "transcription_notes": list(row.transcription_notes),
        },
        "source_facts": {
            "source_record_id": None,
            "level_text": row.level_text,
            "gse_score_or_range": None,
            "skill_text": row.skill,
            "mode_text": row.mode,
            "function_text": None,
            "scale_text": row.scale,
            "other_verbatim": {},
        },
        "interpretation": {
            "inclusion_status": "undecided",
            "exclusion_reason": None,
            "cefr_codes": [row.cefr_code],
            "skill_codes": [],
            "mode_codes": [],
            "function_codes": [],
            "candidate_cluster_ids": [],
            "notes": notes,
            "ambiguities": [warning] if warning else [],
        },
        "review": {
            "status": "unreviewed",
            "reviewer": None,
            "reviewed_at": None,
            "issues": issues,
        },
    }


def build_collection(rows: list[Descriptor]) -> dict[str, Any]:
    repeated = _repetitions(rows)
    records = [_record(row, repeated.get((row.level_text, row.text))) for row in rows]
    return {"schema_version": "1.0.0", "dataset_id": "cefr_all_descriptors", "records": records}
