"""Acceptance tests for the final social-contact target partition."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import SOCIAL_REMAINING_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.agree_to_a_simple_request",
    "lesson_candidate.accept_a_simple_offer",
    "lesson_candidate.show_basic_sympathy_during_a_problem_or_disagreement",
    "lesson_candidate.invite_input_and_check_understanding_in_a_simple_task",
    "lesson_candidate.show_interest_and_welcome_an_idea",
    "lesson_candidate.share_an_idea_and_ask_what_others_think",
}


class LessonSocialTargetPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_six_named_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(SOCIAL_REMAINING_DECISIONS))

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

    def test_request_and_offer_decisions_remain_distinct(self) -> None:
        request = self.candidates["lesson_candidate.agree_to_a_simple_request"]
        offer = self.candidates["lesson_candidate.accept_a_simple_offer"]
        self.assertIn("request", request["language_targets"]["phrases"][0]["target"])
        self.assertIn("offer", offer["language_targets"]["phrases"][0]["target"])

    def test_interest_decision_preserves_non_verbal_requirement(self) -> None:
        candidate = self.candidates[
            "lesson_candidate.show_interest_and_welcome_an_idea"
        ]
        target = candidate["language_targets"]["phrases"][0]
        self.assertIn("non-verbal", target["target"])
        self.assertIn("non-verbal", candidate["error_hypotheses"][0]["error"])

    def test_all_candidates_now_have_target_and_error_decisions(self) -> None:
        self.assertEqual(81, len(self.lesson_map["candidates"]))
        for candidate in self.lesson_map["candidates"]:
            self.assertTrue(any(candidate["language_targets"].values()))
            self.assertEqual(1, len(candidate["error_hypotheses"]))


if __name__ == "__main__":
    unittest.main()
