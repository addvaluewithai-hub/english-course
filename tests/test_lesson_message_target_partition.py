"""Acceptance tests for the remaining message-target partition."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import MESSAGE_REMAINING_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.leave_a_simple_whereabouts_and_return_message",
    "lesson_candidate.relay_names_numbers_and_prices_from_slow_speech",
    "lesson_candidate.identify_a_headline_news_topic_from_visual_media",
    "lesson_candidate.identify_a_product_in_a_short_video_advertisement",
    "lesson_candidate.react_politely_to_a_simple_online_post",
    "lesson_candidate.convey_simple_information_from_a_sign_or_notice",
    "lesson_candidate.give_a_rough_oral_translation_of_everyday_sign_words",
    "lesson_candidate.translate_simple_written_phrases_with_a_dictionary",
}


class LessonMessageTargetPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_eight_named_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(MESSAGE_REMAINING_DECISIONS))

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

    def test_visual_media_candidates_keep_distinct_target_purposes(self) -> None:
        headline = self.candidates[
            "lesson_candidate.identify_a_headline_news_topic_from_visual_media"
        ]
        advert = self.candidates[
            "lesson_candidate.identify_a_product_in_a_short_video_advertisement"
        ]
        self.assertIn("topic", headline["language_targets"]["vocabulary"][0]["purpose"])
        self.assertIn("product", advert["language_targets"]["vocabulary"][0]["purpose"])

    def test_written_translation_preserves_dictionary_meaning_risk(self) -> None:
        candidate = self.candidates[
            "lesson_candidate.translate_simple_written_phrases_with_a_dictionary"
        ]
        self.assertEqual([], candidate["language_targets"]["pronunciation"])
        hypothesis = candidate["error_hypotheses"][0]
        self.assertIn("appropriate meaning", hypothesis["basis"])
        self.assertIn("first dictionary meaning", hypothesis["error"])


if __name__ == "__main__":
    unittest.main()
