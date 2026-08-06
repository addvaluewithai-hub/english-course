"""Acceptance tests for the opening service-output target partition."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import SERVICE_OUTPUT_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.state_a_basic_food_or_drink_preference",
    "lesson_candidate.ask_for_basic_food_or_drink",
    "lesson_candidate.ask_for_and_give_an_everyday_item",
    "lesson_candidate.exchange_information_about_an_immediate_need",
}


class LessonServiceOutputTargetPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_four_named_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(SERVICE_OUTPUT_DECISIONS))

    def test_saved_map_matches_deterministic_builder(self) -> None:
        self.assertEqual(build_map(), self.lesson_map)

    def test_targets_and_labelled_errors_are_present(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            self.assertTrue(any(candidate["language_targets"].values()))
            hypothesis = candidate["error_hypotheses"]
            self.assertEqual(1, len(hypothesis))
            self.assertEqual("hypothesis", hypothesis[0]["validation_status"])
            self.assertIn("not a source fact", hypothesis[0]["basis"])

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

    def test_immediate_need_keeps_both_information_fields(self) -> None:
        candidate = self.candidates[
            "lesson_candidate.exchange_information_about_an_immediate_need"
        ]
        purposes = " ".join(
            target["purpose"]
            for targets in candidate["language_targets"].values()
            for target in targets
        )
        self.assertIn("what is needed", purposes)
        self.assertIn("practical detail", purposes)

    def test_item_exchange_keeps_request_and_response_roles(self) -> None:
        candidate = self.candidates[
            "lesson_candidate.ask_for_and_give_an_everyday_item"
        ]
        phrase = candidate["language_targets"]["phrases"][0]
        self.assertIn("request and handover", phrase["target"].lower())
        self.assertIn("both partner roles", phrase["purpose"])


if __name__ == "__main__":
    unittest.main()
