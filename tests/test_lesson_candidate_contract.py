"""Contract tests for LESSON-001 lesson-sized ability candidates."""

from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PROJECT_ROOT / "schemas/curriculum/lesson-candidate.schema.json"
SOURCE_SCHEMA_PATH = PROJECT_ROOT / "schemas/curriculum/source-record.schema.json"


def evidence_ref() -> dict:
    return {
        "record_id": "example.record.001",
        "dataset_id": "example_dataset",
        "source_id": "example_source",
        "raw_file": "sources/raw/frameworks/example.pdf",
        "location": {"kind": "pdf", "page": 1, "page_end": 1},
        "source_text_sha256": "A" * 64,
        "role": "anchor",
        "coverage": "full",
        "interpretation_note": "Contract fixture only; not curriculum evidence.",
    }


def valid_candidate() -> dict:
    source = evidence_ref()
    return {
        "schema_version": 1,
        "candidate_id": "lesson_candidate.contract_fixture",
        "version": 1,
        "status": "draft",
        "candidate_cluster_ids": ["identity_personal_information"],
        "outcome": {
            "situation": "a bounded fresh situation",
            "observable_action": "perform a communicative action",
            "essential_content": "the required A1 content",
            "independence": "without a complete model",
            "success_condition": "the essential meaning is clear",
            "statement": "In a fresh situation, the learner performs the action independently.",
        },
        "evidence_refs": [source],
        "skill_codes": ["speaking"],
        "mode_codes": ["production"],
        "function_codes": ["introduce"],
        "normalization": {
            "decision": "direct",
            "inputs": ["example.record.001"],
            "coherence_tests": {
                "one_purpose": True,
                "same_task": True,
                "single_judgment": True,
                "a1_load": True,
                "source_fidelity": True,
                "independence": True,
            },
            "rationale": "One source action already forms one testable performance.",
        },
        "relationships": {
            "required_before": [],
            "helpful_before": [],
            "successors": [],
            "concurrent_support": [],
        },
        "language_targets": {
            "grammar": [], "vocabulary": [], "phrases": [], "pronunciation": []
        },
        "error_hypotheses": [],
        "mastery": {
            "fresh_task_family": "One primary task and an equivalent replacement.",
            "required_dimensions": ["comprehension", "outcome_performance"],
            "level_2_evidence": {
                "comprehension": "Interprets the prompt without revealing help.",
                "outcome_performance": "Completes the essential action independently.",
            },
            "critical_failures": ["Does not complete the essential action."],
            "non_blocking_errors": ["Harmless hesitation."],
            "permitted_support": ["Neutral instruction repetition."],
            "disallowed_help": ["A complete model answer."],
            "delayed_probe": "Use a different fresh situation after a delay.",
        },
        "scope": {
            "band": "focused",
            "load_rationale": "One bounded move with limited content.",
            "time_range_hypothesis": None,
            "no_split_rationale": None,
        },
        "risks": [],
        "review": {
            "status": "unreviewed", "reviewer": None,
            "reviewed_at": None, "issues": []
        },
    }


class LessonCandidateContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        with SCHEMA_PATH.open(encoding="utf-8") as handle:
            cls.schema = json.load(handle)
        with SOURCE_SCHEMA_PATH.open(encoding="utf-8") as handle:
            source_schema = json.load(handle)
        registry = Registry().with_resource(
            source_schema["$id"], Resource.from_contents(source_schema)
        )
        cls.validator = Draft202012Validator(cls.schema, registry=registry)

    def errors(self, candidate: dict) -> list:
        return sorted(self.validator.iter_errors(candidate), key=lambda error: list(error.path))

    def test_schema_and_complete_fixture_are_valid(self) -> None:
        Draft202012Validator.check_schema(self.schema)
        self.assertEqual([], self.errors(valid_candidate()))

    def test_source_traceability_is_required(self) -> None:
        candidate = valid_candidate()
        candidate["evidence_refs"] = []
        self.assertTrue(self.errors(candidate))

    def test_every_coherence_test_must_pass(self) -> None:
        candidate = copy.deepcopy(valid_candidate())
        candidate["normalization"]["coherence_tests"]["same_task"] = False
        self.assertTrue(self.errors(candidate))

    def test_language_target_requires_its_own_evidence(self) -> None:
        candidate = valid_candidate()
        candidate["language_targets"]["grammar"] = [
            {"target": "a form", "purpose": "supports the outcome", "evidence_refs": []}
        ]
        self.assertTrue(self.errors(candidate))

    def test_partial_coverage_names_the_covered_part(self) -> None:
        candidate = valid_candidate()
        candidate["evidence_refs"][0]["coverage"] = "partial"
        candidate["evidence_refs"][0]["interpretation_note"] = ""
        self.assertTrue(self.errors(candidate))

    def test_complex_scope_requires_no_split_rationale(self) -> None:
        candidate = valid_candidate()
        candidate["scope"]["band"] = "complex"
        self.assertTrue(self.errors(candidate))


if __name__ == "__main__":
    unittest.main()
