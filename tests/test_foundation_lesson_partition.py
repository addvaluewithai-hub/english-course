"""Acceptance tests for foundation and communication-strategy reconciliation."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.create_foundation_lesson_partition import EXTENSIONS, build_map
from scripts.create_social_lesson_partition import build_map as build_social_map
from scripts.lesson_foundation_candidate_specs import FOUNDATION_CANDIDATE_SPECS
from scripts.lesson_foundation_supports import (
    BASIC_ADDITIONS,
    NUMBER_IDS,
    RECEPTIVE_IDS,
    REPAIR_ADDITIONS,
    SPOKEN_IDS,
    WRITTEN_IDS,
)
from scripts.lesson_map_validation import validation_errors


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
SOURCE_PATHS = (
    ROOT / "data/reviewed/gse-a1-objectives.json",
    ROOT / "data/reviewed/cefr-a1-descriptors.json",
)
NEW_SUPPORT_IDS = {
    record_id for record_id, _ in BASIC_ADDITIONS + REPAIR_ADDITIONS
} | set(RECEPTIVE_IDS + NUMBER_IDS + SPOKEN_IDS + WRITTEN_IDS)
NEW_DIRECT_IDS = {
    item["record_id"]
    for spec in FOUNDATION_CANDIDATE_SPECS for item in spec["evidence"]
} | {record_id for record_id, _ in EXTENSIONS.values()}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def cited_ids(lesson_map: dict) -> set[str]:
    candidate_ids = {
        ref["record_id"] for candidate in lesson_map["candidates"]
        for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
    }
    support_ids = {
        ref["record_id"] for support in lesson_map["support_definitions"]
        for ref in support["evidence_refs"] if ref["coverage"] != "context_only"
    }
    return candidate_ids | support_ids


class FoundationLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.predecessor = build_social_map()
        cls.new_candidate_ids = {
            item["candidate_id"] for item in FOUNDATION_CANDIDATE_SPECS
        }

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_exact_predecessor_gap_is_reconciled(self) -> None:
        included = {
            record["record_id"] for path in SOURCE_PATHS
            for record in load(path)["records"]
            if record["interpretation"]["inclusion_status"] == "included"
        }
        prior_gap = included - cited_ids(self.predecessor)
        self.assertEqual(42, len(prior_gap))
        self.assertEqual(prior_gap, NEW_DIRECT_IDS | NEW_SUPPORT_IDS)
        self.assertEqual(set(), included - cited_ids(self.lesson_map))

    def test_direct_and_support_classifications_do_not_overlap(self) -> None:
        self.assertEqual(8, len(NEW_DIRECT_IDS))
        self.assertEqual(34, len(NEW_SUPPORT_IDS))
        self.assertEqual(set(), NEW_DIRECT_IDS & NEW_SUPPORT_IDS)
        support_ids = {
            ref["record_id"] for support in self.lesson_map["support_definitions"]
            for ref in support["evidence_refs"]
        }
        self.assertTrue(NEW_SUPPORT_IDS <= support_ids)

    def test_three_existing_candidates_receive_source_exact_extensions(self) -> None:
        candidates = {
            item["candidate_id"]: item for item in self.lesson_map["candidates"]
        }
        for candidate_id, (record_id, _) in EXTENSIONS.items():
            refs = [
                ref for ref in candidates[candidate_id]["evidence_refs"]
                if ref["record_id"] == record_id
            ]
            self.assertEqual(1, len(refs))
            self.assertEqual(("supporting", "full"), (refs[0]["role"], refs[0]["coverage"]))

    def test_new_candidates_are_individually_assessable_drafts(self) -> None:
        candidates = [
            item for item in self.lesson_map["candidates"]
            if item["candidate_id"] in self.new_candidate_ids
        ]
        self.assertEqual(3, len(candidates))
        self.assertTrue(all(item["status"] == "needs_review" for item in candidates))
        for candidate in candidates:
            self.assertTrue(all(candidate["normalization"]["coherence_tests"].values()))
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])

    def test_support_definitions_are_reciprocal_and_channel_scoped(self) -> None:
        supports = {
            item["support_id"]: item for item in self.lesson_map["support_definitions"]
        }
        candidates = {
            item["candidate_id"]: item for item in self.lesson_map["candidates"]
        }
        for support_id in {
            "support.receptive_processing", "support.number_processing",
            "support.spoken_intelligibility", "support.written_form_control",
        }:
            support = supports[support_id]
            self.assertTrue(support["applies_to_candidate_ids"])
            for candidate_id in support["applies_to_candidate_ids"]:
                relations = {
                    item["support_id"]
                    for item in candidates[candidate_id]["relationships"]["concurrent_support"]
                }
                self.assertIn(support_id, relations)

    def test_partition_leaves_global_approval_open(self) -> None:
        self.assertEqual("in_progress", self.lesson_map["status"])
        self.assertEqual("needs_review", self.lesson_map["review"]["status"])
        self.assertEqual(87, len(self.lesson_map["candidates"]))
        self.assertTrue(all(not item["relationships"]["required_before"] for item in self.lesson_map["candidates"]))


if __name__ == "__main__":
    unittest.main()
