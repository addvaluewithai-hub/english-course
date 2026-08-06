"""Convert parsed Pearson GSE A1 objectives to source-record collections."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import datetime
from typing import Any

try:
    from scripts.gse_a1_parser import Objective
except ModuleNotFoundError:  # Direct invocation through the sibling CLI.
    from gse_a1_parser import Objective


SOURCE_ID = "pearson.gse_adult_general_english_2022"
SOURCE_VERSION = "September 2022"
RAW_FILE = "sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf"
RAW_SHA256 = "CE5713618E4583F416C02276F7EC7FEBA7EBDD2CA4E55EC2BB0FAFC29DD8604D"


def _record_id(objective: Objective) -> str:
    return (
        f"gse.adult.2022.p{objective.page:02d}."
        f"{objective.ordinal_on_page:03d}"
    )


def _duplicate_groups(objectives: list[Objective]) -> dict[tuple[str, str], list[Objective]]:
    groups: dict[tuple[str, str], list[Objective]] = defaultdict(list)
    for objective in objectives:
        groups[(objective.skill, objective.text)].append(objective)
    return {key: values for key, values in groups.items() if len(values) > 1}


def _duplicate_context(
    objective: Objective, groups: dict[tuple[str, str], list[Objective]]
) -> tuple[Objective | None, str | None]:
    group = groups.get((objective.skill, objective.text))
    if not group:
        return None, None
    canonical = group[0]
    others = [item for item in group if item != objective]
    locations = ", ".join(f"GSE {item.score} on page {item.page}" for item in others)
    return canonical, f"The source repeats this exact {objective.skill} wording at {locations}."


def _review_block(
    reviewed: bool, reviewer: str | None, reviewed_at: str | None, warning: str | None
) -> dict[str, Any]:
    issues = []
    if warning:
        issues.append({"code": "source_duplicate", "severity": "warning", "message": warning})
    return {
        "status": "accepted" if reviewed else "unreviewed",
        "reviewer": reviewer if reviewed else None,
        "reviewed_at": reviewed_at if reviewed else None,
        "issues": issues,
    }


def build_collection(
    objectives: list[Objective],
    *,
    reviewer: str | None = None,
    reviewed_at: str | None = None,
) -> dict[str, Any]:
    reviewed = reviewer is not None or reviewed_at is not None
    if reviewed and (not reviewer or not reviewed_at):
        raise ValueError("reviewer and reviewed_at are required together")
    if reviewed:
        datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
    duplicates = _duplicate_groups(objectives)
    records = []
    for objective in objectives:
        canonical, warning = _duplicate_context(objective, duplicates)
        is_duplicate = canonical is not None and objective != canonical
        canonical_id = _record_id(canonical) if canonical else None
        exclusion = None
        notes = ["Included because Pearson places this objective in GSE 22–29/A1."]
        if is_duplicate:
            exclusion = f"Exact duplicate of {canonical_id}; evidence row retained for provenance."
            notes = ["Excluded from the canonical objective count as an exact source duplicate."]
        records.append(
            {
                "record_id": _record_id(objective),
                "record_kind": "objective",
                "source": {
                    "source_id": SOURCE_ID,
                    "source_version": SOURCE_VERSION,
                    "raw_file": RAW_FILE,
                    "source_file_sha256": RAW_SHA256,
                    "location": {
                        "kind": "pdf_page",
                        "page": objective.page,
                        "page_end": objective.page,
                        "printed_page": str(objective.page),
                        "section": f"GSE 22–29/A1: {objective.skill}",
                    },
                    "source_text": objective.text,
                    "source_text_sha256": hashlib.sha256(
                        objective.text.encode("utf-8")
                    ).hexdigest(),
                    "transcription_notes": list(objective.transcription_notes),
                },
                "source_facts": {
                    "source_record_id": None,
                    "level_text": "A1",
                    "gse_score_or_range": objective.score,
                    "skill_text": objective.skill,
                    "mode_text": None,
                    "function_text": None,
                    "scale_text": f"GSE 22–29/A1: {objective.skill}",
                    "other_verbatim": {"descriptor_origin_code": objective.source_code},
                },
                "interpretation": {
                    "inclusion_status": "excluded" if is_duplicate else "included",
                    "exclusion_reason": exclusion,
                    "cefr_codes": ["a1"],
                    "skill_codes": [],
                    "mode_codes": [],
                    "function_codes": [],
                    "candidate_cluster_ids": [],
                    "notes": notes,
                    "ambiguities": [warning] if warning else [],
                },
                "review": _review_block(reviewed, reviewer, reviewed_at, warning),
            }
        )
    return {"schema_version": "1.0.0", "dataset_id": "gse_a1_objectives", "records": records}
