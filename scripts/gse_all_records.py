"""Build provenance-complete source records for all Pearson GSE objectives."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from typing import Any

try:
    from scripts.gse_all_parser import Objective
except ModuleNotFoundError:
    from gse_all_parser import Objective


SOURCE_ID = "pearson.gse_adult_general_english_2022"
SOURCE_VERSION = "September 2022"
RAW_FILE = "sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf"
RAW_SHA256 = "CE5713618E4583F416C02276F7EC7FEBA7EBDD2CA4E55EC2BB0FAFC29DD8604D"


def record_id(objective: Objective) -> str:
    return (
        f"gse.adult.2022.{objective.band.key}.p{objective.page:02d}."
        f"{objective.ordinal_in_section_on_page:03d}"
    )


def _duplicate_groups(objectives: list[Objective]) -> dict[tuple[str, str], list[Objective]]:
    groups: dict[tuple[str, str], list[Objective]] = defaultdict(list)
    for objective in objectives:
        groups[(objective.skill, objective.text)].append(objective)
    return {key: rows for key, rows in groups.items() if len(rows) > 1}


def _duplicate_warning(
    objective: Objective, groups: dict[tuple[str, str], list[Objective]]
) -> str | None:
    group = groups.get((objective.skill, objective.text))
    if not group:
        return None
    locations = ", ".join(
        f"{row.band.source_level} GSE {row.score} page {row.page}" for row in group
    )
    return f"The source repeats this exact {objective.skill} wording at: {locations}."


def _record(objective: Objective, warning: str | None) -> dict[str, Any]:
    issues = []
    ambiguities = []
    if warning:
        issues.append({"code": "source_duplicate", "severity": "warning", "message": warning})
        ambiguities.append(warning)
    notes = ["Source evidence retained; curriculum disposition is pending SPINE-003."]
    if objective.band.key.endswith("_plus"):
        notes.append(
            "Pearson plus-band milestone is preserved in source facts and mapped to its base CEFR code."
        )
    return {
        "record_id": record_id(objective),
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
                "section": objective.scale_text,
            },
            "source_text": objective.text,
            "source_text_sha256": hashlib.sha256(objective.text.encode("utf-8")).hexdigest(),
            "transcription_notes": list(objective.transcription_notes),
        },
        "source_facts": {
            "source_record_id": None,
            "level_text": objective.band.source_level,
            "gse_score_or_range": str(objective.score),
            "skill_text": objective.skill,
            "mode_text": None,
            "function_text": None,
            "scale_text": objective.scale_text,
            "other_verbatim": {
                "descriptor_origin_code": objective.source_code,
                "gse_band_key": objective.band.key,
            },
        },
        "interpretation": {
            "inclusion_status": "undecided",
            "exclusion_reason": None,
            "cefr_codes": [objective.band.cefr_code],
            "skill_codes": [objective.skill.lower()],
            "mode_codes": [],
            "function_codes": [],
            "candidate_cluster_ids": [],
            "notes": notes,
            "ambiguities": ambiguities,
        },
        "review": {
            "status": "unreviewed",
            "reviewer": None,
            "reviewed_at": None,
            "issues": issues,
        },
    }


def build_collection(objectives: list[Objective]) -> dict[str, Any]:
    duplicates = _duplicate_groups(objectives)
    records = [_record(row, _duplicate_warning(row, duplicates)) for row in objectives]
    return {"schema_version": "1.0.0", "dataset_id": "gse_all_objectives", "records": records}
