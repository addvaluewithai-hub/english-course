"""Small synthetic fixtures for lesson-map contract tests."""

from __future__ import annotations

import copy


def source_record(
    record_id: str,
    source_id: str,
    page: int,
    hash_character: str,
    *,
    skills: list[str],
    modes: list[str],
    functions: list[str],
    clusters: list[str] | None = None,
) -> dict:
    return {
        "record_id": record_id,
        "source": {
            "source_id": source_id,
            "raw_file": f"sources/raw/frameworks/{source_id}.pdf",
            "location": {"kind": "pdf", "page": page, "page_end": page},
            "source_text_sha256": hash_character * 64,
        },
        "interpretation": {
            "inclusion_status": "included",
            "skill_codes": skills,
            "mode_codes": modes,
            "function_codes": functions,
            "candidate_cluster_ids": clusters or ["identity_personal_information"],
        },
    }


def evidence_ref(
    record: dict,
    dataset_id: str,
    role: str,
    coverage: str = "full",
) -> dict:
    source = record["source"]
    return {
        "record_id": record["record_id"],
        "dataset_id": dataset_id,
        "source_id": source["source_id"],
        "raw_file": source["raw_file"],
        "location": copy.deepcopy(source["location"]),
        "source_text_sha256": source["source_text_sha256"],
        "role": role,
        "coverage": coverage,
        "interpretation_note": "Synthetic contract evidence only.",
    }


def valid_fixture() -> tuple[dict, list[dict]]:
    anchor = source_record(
        "fixture.anchor", "fixture_one", 1, "A",
        skills=["listening", "reading", "speaking", "writing"],
        modes=["interaction"], functions=["exchange_information"],
    )
    basic = source_record(
        "fixture.basic", "fixture_two", 2, "B",
        skills=["language_system"], modes=["communicative_competence"],
        functions=["control_language_form"],
        clusters=["language_foundations"],
    )
    repair = source_record(
        "fixture.repair", "fixture_two", 3, "C",
        skills=["speaking"], modes=["interaction"],
        functions=["clarify_or_repair"],
        clusters=["communication_strategies"],
    )
    collections = [
        {"dataset_id": "fixture_dataset_one", "records": [anchor]},
        {"dataset_id": "fixture_dataset_two", "records": [basic, repair]},
    ]
    candidate_id = "lesson_candidate.fixture_exchange"
    candidate = {
        "schema_version": 1,
        "candidate_id": candidate_id,
        "version": 1,
        "status": "approved_candidate",
        "candidate_cluster_ids": ["identity_personal_information"],
        "outcome": {
            "situation": "a bounded fresh exchange",
            "observable_action": "exchange essential personal information",
            "essential_content": "one question and one relevant answer",
            "independence": "without a complete model",
            "success_condition": "the essential meaning is clear",
            "statement": "In a fresh exchange, the learner exchanges essential information independently.",
        },
        "evidence_refs": [evidence_ref(anchor, "fixture_dataset_one", "anchor")],
        "skill_codes": ["listening", "reading", "speaking", "writing"],
        "mode_codes": ["interaction"],
        "function_codes": ["exchange_information"],
        "normalization": {
            "decision": "direct", "inputs": ["fixture.anchor"],
            "coherence_tests": {
                "one_purpose": True, "same_task": True, "single_judgment": True,
                "a1_load": True, "source_fidelity": True, "independence": True,
            },
            "rationale": "One bounded exchange supports one judgment.",
        },
        "relationships": {
            "required_before": [], "helpful_before": [], "successors": [],
            "concurrent_support": [
                {
                    "support_id": "support.basic_language_control",
                    "rationale": "Basic control accompanies the task.",
                    "evidence_record_ids": ["fixture.basic"],
                },
                {
                    "support_id": "support.interaction_repair",
                    "rationale": "Repair remains available in interaction.",
                    "evidence_record_ids": ["fixture.repair"],
                },
            ],
        },
        "language_targets": {
            "grammar": [], "vocabulary": [], "phrases": [], "pronunciation": [],
        },
        "error_hypotheses": [],
        "mastery": {
            "fresh_task_family": "A fresh exchange plus one equivalent replacement.",
            "required_dimensions": [
                "comprehension", "outcome_performance", "interaction_or_transfer",
                "control_or_repair",
            ],
            "level_2_evidence": {
                "comprehension": "Understands without revealing help.",
                "outcome_performance": "Exchanges the essential information.",
                "interaction_or_transfer": "Responds to the fresh turn.",
                "control_or_repair": "Meaning is intelligible and repairable.",
            },
            "critical_failures": ["Essential information is absent."],
            "non_blocking_errors": ["Harmless hesitation."],
            "permitted_support": ["Neutral instruction repetition."],
            "disallowed_help": ["A complete model answer."],
            "delayed_probe": "Use a new exchange after a delay.",
        },
        "scope": {
            "band": "standard", "load_rationale": "One short bounded exchange.",
            "time_range_hypothesis": None, "no_split_rationale": None,
        },
        "risks": [],
        "review": {
            "status": "accepted", "reviewer": "contract-reviewer",
            "reviewed_at": "2026-07-17T12:00:00+03:00", "issues": [],
        },
    }
    lesson_map = {
        "schema_version": 1, "map_id": "a1_lesson_map_fixture", "level": "a1",
        "version": 1, "status": "approved",
        "evidence_dataset_ids": ["fixture_dataset_one", "fixture_dataset_two"],
        "candidates": [candidate], "sequence": [candidate_id],
        "support_definitions": [
            {
                "support_id": "support.basic_language_control", "title": "Basic control",
                "evidence_refs": [evidence_ref(basic, "fixture_dataset_two", "cross_cutting")],
                "applies_to_candidate_ids": [candidate_id],
            },
            {
                "support_id": "support.interaction_repair", "title": "Interaction repair",
                "evidence_refs": [evidence_ref(repair, "fixture_dataset_two", "cross_cutting")],
                "applies_to_candidate_ids": [candidate_id],
            },
        ],
        "review": {
            "status": "accepted", "reviewer": "contract-reviewer",
            "reviewed_at": "2026-07-17T12:00:00+03:00", "issues": [],
        },
    }
    return lesson_map, collections
