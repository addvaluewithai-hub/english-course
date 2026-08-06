"""Acceptance tests for familiar home, object, and location speech."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import FAMILIAR_HOME_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.describe_people_and_object_locations_orally",
    "lesson_candidate.describe_a_familiar_object_orally",
    "lesson_candidate.exchange_visible_object_information",
    "lesson_candidate.exchange_basic_information_about_a_home",
}


class LessonFamiliarHomeSpokenPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_four_selected_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(FAMILIAR_HOME_DECISIONS))

    def test_saved_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_all_four_target_families_and_labelled_errors_are_present(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            self.assertTrue(all(candidate["language_targets"].values()))
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

    def test_privacy_and_scope_notes_remain_explicit(self) -> None:
        home = self.candidates[
            "lesson_candidate.exchange_basic_information_about_a_home"
        ]
        note = next(
            risk for risk in home["risks"]
            if risk.startswith("Target-decision note:")
        )
        self.assertIn("fictional answers", note)
        self.assertIn("private disclosure", note)


if __name__ == "__main__":
    unittest.main()
