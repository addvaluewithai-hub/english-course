"""Acceptance tests for the opening wayfinding target partition."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import (
    NAVIGATION_WAYFINDING_DECISIONS,
    build_map,
)
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.follow_simple_written_wayfinding_directions",
    "lesson_candidate.follow_slow_spoken_route_directions",
    "lesson_candidate.follow_simple_directions_from_an_interlocutor",
    "lesson_candidate.exchange_basic_wayfinding_information",
}


class LessonWayfindingTargetPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_four_wayfinding_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(NAVIGATION_WAYFINDING_DECISIONS))

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

    def test_channel_and_scope_boundaries_remain_explicit(self) -> None:
        written = self.candidates[
            "lesson_candidate.follow_simple_written_wayfinding_directions"
        ]
        listening = self.candidates[
            "lesson_candidate.follow_slow_spoken_route_directions"
        ]
        interlocutor = self.candidates[
            "lesson_candidate.follow_simple_directions_from_an_interlocutor"
        ]
        exchange = self.candidates[
            "lesson_candidate.exchange_basic_wayfinding_information"
        ]
        self.assertFalse(written["language_targets"]["grammar"])
        self.assertFalse(written["language_targets"]["pronunciation"])
        self.assertFalse(listening["language_targets"]["grammar"])
        self.assertFalse(interlocutor["language_targets"]["grammar"])
        self.assertTrue(all(exchange["language_targets"].values()))
        self.assertIn(
            "times-and-numbers clause remains outside",
            next(risk for risk in interlocutor["risks"] if risk.startswith("Target-decision note:")),
        )


if __name__ == "__main__":
    unittest.main()
