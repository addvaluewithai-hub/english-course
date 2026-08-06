"""Acceptance tests for the identity lesson-map partition."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.create_identity_lesson_partition import build_map
from scripts.lesson_map_validation import validation_errors
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
IDENTITY_CLUSTER = "identity_personal_information"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class IdentityLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_identity_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if IDENTITY_CLUSTER in item["candidate_cluster_ids"]
        }
        candidate_refs = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support_refs = {
            ref["record_id"] for support in self.lesson_map["support_definitions"]
            for ref in support["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(24, len(assigned))
        self.assertEqual(set(), assigned - candidate_refs - support_refs)

    def test_partial_clauses_are_explicit(self) -> None:
        partial = {
            ref["record_id"]: ref["interpretation_note"]
            for candidate in self.lesson_map["candidates"]
            if candidate["candidate_cluster_ids"] == [IDENTITY_CLUSTER]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "partial"
        }
        self.assertEqual({
            "cefr.cv2020.p067.creative_writing.01",
            "cefr.cv2020.p079.information_exchange.03",
            "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01",
        }, set(partial))
        self.assertTrue(all(note.strip() for note in partial.values()))

    def test_partition_stays_provisional_without_hard_order(self) -> None:
        lesson_map = self.lesson_map
        candidates = [
            item for item in lesson_map["candidates"]
            if item["candidate_cluster_ids"] == [IDENTITY_CLUSTER]
        ]
        self.assertEqual("in_progress", lesson_map["status"])
        self.assertEqual("needs_review", lesson_map["review"]["status"])
        self.assertEqual(9, len(candidates))
        for candidate in candidates:
            self.assertEqual("needs_review", candidate["status"])
            self.assertEqual([IDENTITY_CLUSTER], candidate["candidate_cluster_ids"])
            relationships = candidate["relationships"]
            self.assertEqual([], relationships["required_before"])
            self.assertEqual([], relationships["helpful_before"])
            self.assertEqual([], relationships["successors"])

    def test_partition_represents_core_skills_and_relevant_modes(self) -> None:
        candidates = [
            item for item in self.lesson_map["candidates"]
            if item["candidate_cluster_ids"] == [IDENTITY_CLUSTER]
        ]
        skills = {
            skill for candidate in candidates
            for skill in candidate["skill_codes"]
        }
        modes = {
            mode for candidate in candidates
            for mode in candidate["mode_codes"]
        }
        self.assertEqual({"listening", "reading", "speaking", "writing"}, skills)
        self.assertEqual({"reception", "production", "interaction", "mediation"}, modes)


if __name__ == "__main__":
    unittest.main()
