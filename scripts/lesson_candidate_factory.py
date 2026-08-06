"""Build source-exact lesson candidates from reviewed authoring specifications."""

from __future__ import annotations

import copy
from typing import Any


COHERENCE_TESTS = {
    "one_purpose": True,
    "same_task": True,
    "single_judgment": True,
    "a1_load": True,
    "source_fidelity": True,
    "independence": True,
}
DEFAULT_REVIEWED_AT = "2026-07-17T15:47:40+03:00"


def source_index(collections: list[dict[str, Any]]) -> dict[str, tuple[str, dict[str, Any]]]:
    return {
        record["record_id"]: (collection["dataset_id"], record)
        for collection in collections
        for record in collection["records"]
    }


def evidence_ref(
    index: dict[str, tuple[str, dict[str, Any]]],
    record_id: str,
    role: str,
    coverage: str,
    note: str,
) -> dict[str, Any]:
    dataset_id, record = index[record_id]
    source = record["source"]
    return {
        "record_id": record_id,
        "dataset_id": dataset_id,
        "source_id": source["source_id"],
        "raw_file": source["raw_file"],
        "location": copy.deepcopy(source["location"]),
        "source_text_sha256": source["source_text_sha256"],
        "role": role,
        "coverage": coverage,
        "interpretation_note": note,
    }


def build_candidate(
    spec: dict[str, Any], index: dict[str, tuple[str, dict[str, Any]]]
) -> dict[str, Any]:
    refs = [
        evidence_ref(
            index, item["record_id"], item["role"], item["coverage"],
            item["interpretation_note"],
        )
        for item in spec["evidence"]
    ]
    input_ids = [item["record_id"] for item in spec["evidence"]]
    supports = [_basic_support(spec["basic_support_ids"])]
    if {"interaction", "online_interaction"} & set(spec["mode_codes"]):
        supports.append(_interaction_support())
    band, load = spec["scope"]
    return {
        "schema_version": 1,
        "candidate_id": spec["candidate_id"],
        "version": 1,
        "status": "needs_review",
        "candidate_cluster_ids": spec.get(
            "candidate_cluster_ids", ["identity_personal_information"]
        ),
        "outcome": spec["outcome"],
        "evidence_refs": refs,
        "skill_codes": spec["skill_codes"],
        "mode_codes": spec["mode_codes"],
        "function_codes": spec["function_codes"],
        "normalization": {
            "decision": "direct" if len(refs) == 1 else "merged",
            "inputs": input_ids,
            "coherence_tests": copy.deepcopy(COHERENCE_TESTS),
            "rationale": spec["normalization_rationale"],
        },
        "relationships": {
            "required_before": [],
            "helpful_before": [],
            "successors": [],
            "concurrent_support": supports,
        },
        "language_targets": {
            "grammar": [], "vocabulary": [], "phrases": [], "pronunciation": [],
        },
        "error_hypotheses": [],
        "mastery": spec["mastery"],
        "scope": {
            "band": band,
            "load_rationale": load,
            "time_range_hypothesis": None,
            "no_split_rationale": None,
        },
        "risks": spec["risks"],
        "review": {
            "status": "needs_review",
            "reviewer": "lesson_002_primary",
            "reviewed_at": spec.get("reviewed_at", DEFAULT_REVIEWED_AT),
            "issues": [
                "Independent review and cross-cluster reconciliation remain required before candidate approval."
            ],
        },
    }


def _basic_support(record_ids: list[str]) -> dict[str, Any]:
    return {
        "support_id": "support.basic_language_control",
        "rationale": "Basic A1 language control accompanies the fresh performance.",
        "evidence_record_ids": record_ids,
    }


def _interaction_support() -> dict[str, Any]:
    return {
        "support_id": "support.interaction_repair",
        "rationale": "Clarification and repair remain available within an interaction task.",
        "evidence_record_ids": [
            "cefr.cv2020.p072.overall_oral_interaction.01",
            "cefr.cv2020.p089.asking_for_clarification.01",
            "cefr.cv2020.p089.asking_for_clarification.02",
        ],
    }
