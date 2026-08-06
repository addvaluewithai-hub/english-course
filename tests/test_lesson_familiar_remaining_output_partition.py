"""Acceptance tests for the remaining familiar output and mediation tasks."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import FAMILIAR_FINAL_OUTPUT_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.describe_common_weather",
    "lesson_candidate.deliver_a_rehearsed_formal_introduction",
    "lesson_candidate.state_how_a_simple_work_made_them_feel",
}


class LessonFamiliarRemainingOutputPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_three_selected_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(FAMILIAR_FINAL_OUTPUT_DECISIONS))

    def test_saved_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_targets_and_labelled_errors_are_present(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            self.assertTrue(any(candidate["language_targets"].values()))
            self.assertEqual(1, len(candidate["error_hypotheses"]))
            hypothesis = candidate["error_hypotheses"][0]
            self.assertEqual("hypothesis", hypothesis["validation_status"])
            self.assertIn("not a source fact", hypothesis["basis"])

    def test_targets_reuse_only_owning_candidate_evidence(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            owned_ids = {ref["record_id"] for ref in candidate["evidence_refs"]}
            for targets in candidate["language_targets"].values():
                for target in targets:
                    cited_ids = {ref["record_id"] for ref in target["evidence_refs"]}
                    self.assertTrue(cited_ids <= owned_ids)

    def test_empty_target_families_have_explicit_rationales(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            note = next(
                risk for risk in candidate["risks"]
                if risk.startswith("Target-decision note:")
            ).lower()
            for family, targets in candidate["language_targets"].items():
                if not targets:
                    self.assertIn(family, note)

    def test_source_boundaries_remain_explicit(self) -> None:
        introduction = self.candidates[
            "lesson_candidate.deliver_a_rehearsed_formal_introduction"
        ]
        response = self.candidates[
            "lesson_candidate.state_how_a_simple_work_made_them_feel"
        ]
        introduction_note = next(
            risk for risk in introduction["risks"]
            if risk.startswith("Target-decision note:")
        )
        response_note = next(
            risk for risk in response["risks"]
            if risk.startswith("Target-decision note:")
        )
        self.assertIn("learner-prepared text remains permitted", introduction_note)
        self.assertIn("spoken-or-written channel ambiguity", response_note)


if __name__ == "__main__":
    unittest.main()
