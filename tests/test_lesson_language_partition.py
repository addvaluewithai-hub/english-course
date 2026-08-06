"""Acceptance tests for foundational reception target and error decisions."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import DECISIONS, RECEPTION_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load
from scripts.lesson_map_validation import validation_errors


class LessonLanguagePartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_saved_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_reception_partition_remains_bounded_to_nine_candidates(self) -> None:
        self.assertEqual(9, len(RECEPTION_DECISIONS))
        self.assertTrue(set(RECEPTION_DECISIONS) <= set(self.candidates))

    def test_saved_map_contains_all_current_target_decisions(self) -> None:
        self.assertEqual(81, len(DECISIONS))
        self.assertEqual(
            len(DECISIONS),
            sum(any(item["language_targets"].values()) for item in self.candidates.values()),
        )

    def test_targets_reuse_candidate_evidence(self) -> None:
        for candidate_id in DECISIONS:
            candidate = self.candidates[candidate_id]
            primary_ids = {ref["record_id"] for ref in candidate["evidence_refs"]}
            for targets in candidate["language_targets"].values():
                for target in targets:
                    self.assertTrue(target["target"])
                    self.assertTrue(target["purpose"])
                    self.assertTrue(
                        {ref["record_id"] for ref in target["evidence_refs"]}
                        <= primary_ids
                    )

    def test_empty_target_families_have_explicit_decisions(self) -> None:
        for candidate_id in DECISIONS:
            candidate = self.candidates[candidate_id]
            empty = [
                family for family, targets in candidate["language_targets"].items()
                if not targets
            ]
            if empty:
                notes = [risk for risk in candidate["risks"] if risk.startswith("Target-decision note:")]
                self.assertEqual(1, len(notes))
                for family in empty:
                    self.assertIn(family, notes[0].lower())

    def test_error_decisions_are_labelled_hypotheses(self) -> None:
        for candidate_id in DECISIONS:
            hypotheses = self.candidates[candidate_id]["error_hypotheses"]
            self.assertEqual(1, len(hypotheses))
            self.assertEqual("hypothesis", hypotheses[0]["validation_status"])
            self.assertIn("not a source fact", hypotheses[0]["basis"])

    def test_final_map_validation_and_approval_pass(self) -> None:
        self.assertEqual([], validation_errors(DEFAULT_MAP_PATH))
        self.assertEqual("approved", self.lesson_map["status"])
        self.assertTrue(
            all(item["status"] == "approved_candidate" for item in self.lesson_map["candidates"])
        )


if __name__ == "__main__":
    unittest.main()
