"""Read normalized source datasets through one small adapter."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from scripts.source_disposition_contract import DATASET_FILES, DERIVED


def load_inputs() -> list[tuple[str, Path, dict[str, Any]]]:
    result = []
    for expected_id, filename in DATASET_FILES.items():
        path = DERIVED / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["dataset_id"] != expected_id:
            raise ValueError(f"{path}: expected {expected_id}, got {data['dataset_id']}")
        result.append((expected_id, path, data))
    return result


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record_id(dataset_id: str, record: dict[str, Any]) -> str:
    return str(record["id"] if dataset_id == "egp_all_levels" else record["record_id"])


def level_codes(dataset_id: str, record: dict[str, Any]) -> list[str]:
    if dataset_id == "egp_all_levels":
        return [record["Level"].lower()]
    return list(record["interpretation"]["cefr_codes"])


def level_text(dataset_id: str, record: dict[str, Any]) -> str | None:
    if dataset_id == "egp_all_levels":
        return record["_source"]["raw_level_text"]
    return record["source_facts"]["level_text"]


def score_text(dataset_id: str, record: dict[str, Any]) -> str | None:
    if dataset_id == "egp_all_levels":
        return None
    return record["source_facts"]["gse_score_or_range"]


def exact_text(dataset_id: str, record: dict[str, Any]) -> str:
    if dataset_id == "egp_all_levels":
        fields = ("SuperCategory", "SubCategory", "Guideword", "Can-do statement")
        return " | ".join(str(record.get(field, "")) for field in fields)
    return record["source"]["source_text"]


def normalized_text(dataset_id: str, record: dict[str, Any]) -> str:
    return re.sub(r"\s+", " ", exact_text(dataset_id, record)).strip().casefold()
