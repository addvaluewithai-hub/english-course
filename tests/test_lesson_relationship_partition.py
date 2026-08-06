"""Acceptance tests for the LESSON-002 relationship and sequence partition."""

from __future__ import annotations

import unittest

from scripts.create_lesson_relationship_partition import REVIEW_PATH
from scripts.lesson_language_target_model import DECISIONS
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load
from scripts.lesson_map_validation import validation_errors
from scripts.lesson_relationship_model import build_map, build_review
from scripts.lesson_sequence_specs import reviewed_sequence
from scripts.validate_lesson_relationship_review import review_errors


class LessonRelationshipPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.review = load(REVIEW_PATH)

    def test_saved_artifacts_retain_reviewed_relationship_model(self) -> None:
        relationship_map = build_map()
        expected = {
            item["candidate_id"]: item["relationships"]
            for item in relationship_map["candidates"]
        }
        actual = {
            item["candidate_id"]: item["relationships"]
            for item in self.lesson_map["candidates"]
        }
        self.assertEqual(expected, actual)
        self.assertEqual(build_review(self.lesson_map), self.review)

    def test_sequence_bands_cover_every_candidate_once(self) -> None:
        sequence = reviewed_sequence()
        candidate_ids = {
            item["candidate_id"] for item in self.lesson_map["candidates"]
        }
        self.assertEqual(81, len(sequence))
        self.assertEqual(81, len(set(sequence)))
        self.assertEqual(candidate_ids, set(sequence))
        self.assertEqual(sequence, self.lesson_map["sequence"])

    def test_hard_helpful_and_successor_links_are_typed(self) -> None:
        counts = self.review["counts"]
        self.assertEqual(5, counts["required_before"])
        self.assertEqual(43, counts["helpful_before"])
        self.assertEqual(5, counts["successors"])
        self.assertFalse(
            self.review["interpretation_boundary"]["source_proven_strict_order"]
        )

    def test_map_and_review_validation_pass(self) -> None:
        self.assertEqual([], validation_errors(DEFAULT_MAP_PATH))
        self.assertEqual([], review_errors())

    def test_final_gate_is_approved(self) -> None:
        self.assertEqual("approved", self.lesson_map["status"])
        self.assertEqual("accepted", self.lesson_map["review"]["status"])
        self.assertTrue(
            all(candidate["status"] == "approved_candidate" for candidate in self.lesson_map["candidates"])
        )
        self.assertEqual(0, sum(not any(candidate["language_targets"].values()) for candidate in self.lesson_map["candidates"]))


if __name__ == "__main__":
    unittest.main()
