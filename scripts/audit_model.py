"""Controlled definitions and shared helpers for the CUR-006 audit."""

from __future__ import annotations

import hashlib
import re
from collections import Counter
from typing import Any


CORE_SKILLS = ("listening", "reading", "speaking", "writing")
CANDIDATE_ROLES = {"candidate_unit"}

SUPPORT_NEEDS = (
    {
        "need_id": "basic_language_control",
        "support_cluster_id": "language_foundations",
        "summary": (
            "Basic range, form, intelligibility, and orthographic control must be "
            "available alongside topical work; the evidence does not justify a "
            "standalone foundation unit or a strict topical-unit order."
        ),
        "evidence_record_ids": (
            "cefr.cv2020.p131.general_linguistic_range.01",
            "cefr.cv2020.p132.grammatical_accuracy.01",
            "cefr.cv2020.p135.overall_phonological_control.01",
            "cefr.cv2020.p136.orthographic_control.02",
        ),
        "target_rule": "all_candidate_units",
    },
    {
        "need_id": "interaction_repair",
        "support_cluster_id": "communication_strategies",
        "summary": (
            "Repair and clarification must be taught before or with interaction tasks; "
            "this is a support dependency, not evidence for a fixed unit sequence."
        ),
        "evidence_record_ids": (
            "cefr.cv2020.p072.overall_oral_interaction.01",
            "cefr.cv2020.p089.asking_for_clarification.01",
            "cefr.cv2020.p089.asking_for_clarification.02",
        ),
        "target_rule": "clusters_with_interaction",
    },
)


def normalized_text(value: str) -> str:
    """Normalize only for exact repeated-wording detection."""
    return re.sub(r"\W+", " ", value.casefold()).strip()


def duplicate_group_id(value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    return f"duplicate_{digest}"


def record_ref(record: dict[str, Any], dataset_id: str) -> dict[str, Any]:
    source = record["source"]
    return {
        "record_id": record["record_id"],
        "dataset_id": dataset_id,
        "raw_file": source["raw_file"],
        "location": source["location"],
        "source_text_sha256": source["source_text_sha256"],
    }


def count_tags(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    counts = Counter(
        value for record in records for value in record["interpretation"][field]
    )
    return dict(sorted(counts.items()))
