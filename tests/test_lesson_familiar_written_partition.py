"""Acceptance tests for familiar written people, routine, and home tasks."""

from __future__ import annotations

import unittest

from scripts.lesson_language_target_model import FAMILIAR_WRITING_DECISIONS, build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


EXPECTED_IDS = {
    "lesson_candidate.write_simple_people_profile_cards",
    "lesson_candidate.write_a_short_hobbies_and_likes_post",
    "lesson_candidate.write_schedule_dates_and_times",
    "lesson_candidate.write_simple_life_and_routine_sentences",
    "lesson_candidate.write_a_simple_object_description",
    "lesson_candidate.write_a_simple_room_description",
}


class LessonFamiliarWrittenPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = load(DEFAULT_MAP_PATH)
        cls.candidates = {
            item["candidate_id"]: item for item in cls.lesson_map["candidates"]
        }

    def test_partition_is_exactly_the_six_selected_candidates(self) -> None:
        self.assertEqual(EXPECTED_IDS, set(FAMILIAR_WRITING_DECISIONS))

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

    def test_empty_families_have_explicit_written_channel_rationales(self) -> None:
        for candidate_id in EXPECTED_IDS:
            candidate = self.candidates[candidate_id]
            note = next(
                risk for risk in candidate["risks"]
                if risk.startswith("Target-decision note:")
            ).lower()
            for family, targets in candidate["language_targets"].items():
                if not targets:
                    self.assertIn(family, note)

    def test_room_and_post_scope_guards_remain_explicit(self) -> None:
        room = self.candidates["lesson_candidate.write_a_simple_room_description"]
        post = self.candidates["lesson_candidate.write_a_short_hobbies_and_likes_post"]
        room_note = next(risk for risk in room["risks"] if risk.startswith("Target-decision note:"))
        post_note = next(risk for risk in post["risks"] if risk.startswith("Target-decision note:"))
        self.assertIn("culturally neutral", room_note)
        self.assertIn("complete-sentence generation", post_note)


if __name__ == "__main__":
    unittest.main()
