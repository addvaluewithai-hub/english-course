"""Acceptance tests for foundational productive and interactive target decisions."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import FOUNDATION_OUTPUT_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.use_basic_everyday_polite_forms",
    "lesson_candidate.open_and_close_a_basic_social_exchange",
    "lesson_candidate.give_short_self_introduction",
    "lesson_candidate.exchange_personal_details_orally",
    "lesson_candidate.complete_a_simple_information_form",
    "lesson_candidate.write_short_personal_profile",
    "lesson_candidate.exchange_personal_details_in_writing",
    "lesson_candidate.write_a_short_message_to_a_friend",
    "lesson_candidate.respond_politely_to_an_introduction",
    "lesson_candidate.introduce_another_person",
}


class LessonFoundationOutputPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_ten_selected_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(FOUNDATION_OUTPUT_DECISIONS))

    def test_saved_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_each_candidate_has_targets_and_one_labelled_error(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            self.assertTrue(any(candidate["language_targets"].values()))
            self.assertEqual(1, len(candidate["error_hypotheses"]))
            hypothesis = candidate["error_hypotheses"][0]
            self.assertEqual("hypothesis", hypothesis["validation_status"])
            self.assertIn("not a source fact", hypothesis["basis"])

    def test_targets_use_only_candidate_evidence(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            candidate_ids = {ref["record_id"] for ref in candidate["evidence_refs"]}
            for targets in candidate["language_targets"].values():
                for target in targets:
                    target_ids = {ref["record_id"] for ref in target["evidence_refs"]}
                    self.assertTrue(target_ids <= candidate_ids)

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


if __name__ == "__main__":
    unittest.main()
