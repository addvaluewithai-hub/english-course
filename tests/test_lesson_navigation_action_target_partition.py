"""Acceptance tests for the next navigation and travel-action target partition."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import (
    NAVIGATION_ACTION_DECISIONS,
    build_map,
)
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.relay_predictable_person_time_or_place_details",
    "lesson_candidate.follow_simple_game_or_activity_instructions",
    "lesson_candidate.buy_a_basic_public_transport_ticket",
    "lesson_candidate.check_in_at_a_hotel",
}


class LessonNavigationActionTargetPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_four_named_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(NAVIGATION_ACTION_DECISIONS))

    def test_saved_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_targets_and_labelled_errors_are_present(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            self.assertEqual(3, sum(map(len, candidate["language_targets"].values())))
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

    def test_empty_grammar_family_has_an_explicit_rationale(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            self.assertFalse(candidate["language_targets"]["grammar"])
            note = next(
                risk for risk in candidate["risks"]
                if risk.startswith("Target-decision note:")
            ).lower()
            self.assertIn("grammar", note)

    def test_output_and_reception_boundaries_are_explicit(self) -> None:
        activity = self.candidates[
            "lesson_candidate.follow_simple_game_or_activity_instructions"
        ]
        ticket = self.candidates[
            "lesson_candidate.buy_a_basic_public_transport_ticket"
        ]
        hotel = self.candidates["lesson_candidate.check_in_at_a_hotel"]
        self.assertIn("recognition", activity["language_targets"]["pronunciation"][0]["target"].lower())
        self.assertIn("fixed expressions", ticket["language_targets"]["phrases"][0]["target"])
        self.assertIn("fixed expressions", hotel["language_targets"]["phrases"][0]["target"])


if __name__ == "__main__":
    unittest.main()
