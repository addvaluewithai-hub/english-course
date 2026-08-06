"""Acceptance tests for the opening service-reception target partition."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import (
    SERVICE_RECEPTION_DECISIONS,
    build_map,
)
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.identify_a_price_in_slow_spoken_service_information",
    "lesson_candidate.follow_a_slow_everyday_service_exchange",
    "lesson_candidate.find_key_details_in_a_simple_advertisement_or_leaflet",
}


class LessonServiceReceptionTargetPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_three_named_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(SERVICE_RECEPTION_DECISIONS))

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

    def test_reception_channels_remain_explicit(self) -> None:
        price = self.candidates[
            "lesson_candidate.identify_a_price_in_slow_spoken_service_information"
        ]
        exchange = self.candidates[
            "lesson_candidate.follow_a_slow_everyday_service_exchange"
        ]
        leaflet = self.candidates[
            "lesson_candidate.find_key_details_in_a_simple_advertisement_or_leaflet"
        ]
        self.assertIn("Recognition", price["language_targets"]["pronunciation"][0]["target"])
        self.assertIn("Recognition", exchange["language_targets"]["pronunciation"][0]["target"])
        self.assertFalse(leaflet["language_targets"]["pronunciation"])
        self.assertFalse(leaflet["language_targets"]["grammar"])


if __name__ == "__main__":
    unittest.main()
