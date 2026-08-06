"""Convert CEFR A1 descriptor cells to curriculum source records."""

from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Any

try:
    from scripts.cefr_a1_parser import Descriptor
except ModuleNotFoundError:
    from cefr_a1_parser import Descriptor


SOURCE_ID = "coe.cefr_companion_2020_en"
SOURCE_VERSION = "2020"
RAW_FILE = "sources/raw/frameworks/cefr-companion-2020-en.pdf"
RAW_SHA256 = "BFBD8C74090419AC4B9B352D6BA26E180713B31F45265D7D775B7C36DD7AD1B1"


def _slug(value: str) -> str:
    words = re.findall(r"[a-z0-9]+", value.lower())
    return "_".join(words[:7])


def _record(descriptor: Descriptor, reviewer: str | None, reviewed_at: str | None) -> dict[str, Any]:
    reviewed = reviewer is not None
    return {
        "record_id": f"cefr.cv2020.p{descriptor.page:03d}.{_slug(descriptor.scale)}.{descriptor.ordinal_in_scale:02d}",
        "record_kind": "descriptor",
        "source": {
            "source_id": SOURCE_ID,
            "source_version": SOURCE_VERSION,
            "raw_file": RAW_FILE,
            "source_file_sha256": RAW_SHA256,
            "location": {
                "kind": "pdf_page",
                "page": descriptor.page,
                "page_end": descriptor.page,
                "printed_page": str(descriptor.page),
                "section": descriptor.scale,
            },
            "source_text": descriptor.text,
            "source_text_sha256": hashlib.sha256(descriptor.text.encode("utf-8")).hexdigest(),
            "transcription_notes": list(descriptor.transcription_notes),
        },
        "source_facts": {
            "source_record_id": None,
            "level_text": "A1",
            "gse_score_or_range": None,
            "skill_text": descriptor.skill,
            "mode_text": descriptor.mode,
            "function_text": None,
            "scale_text": descriptor.scale,
            "other_verbatim": {},
        },
        "interpretation": {
            "inclusion_status": "included",
            "exclusion_reason": None,
            "cefr_codes": ["a1"],
            "skill_codes": [],
            "mode_codes": [],
            "function_codes": [],
            "candidate_cluster_ids": [],
            "notes": ["Included because the CEFR scale publishes this descriptor at A1."],
            "ambiguities": [],
        },
        "review": {
            "status": "accepted" if reviewed else "unreviewed",
            "reviewer": reviewer,
            "reviewed_at": reviewed_at,
            "issues": [],
        },
    }


def build_collection(
    descriptors: list[Descriptor], reviewer: str | None = None, reviewed_at: str | None = None
) -> dict[str, Any]:
    if bool(reviewer) != bool(reviewed_at):
        raise ValueError("reviewer and reviewed_at are required together")
    if reviewed_at:
        datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
    return {
        "schema_version": "1.0.0",
        "dataset_id": "cefr_a1_descriptors",
        "records": [_record(item, reviewer, reviewed_at) for item in descriptors],
    }
