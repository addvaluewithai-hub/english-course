"""Acceptance tests for overlap and mastery remediation."""

from __future__ import annotations

import unittest

from scripts.create_lesson_overlap_partition import build_map
from scripts.lesson_map_io import DEFAULT_MAP_PATH, load


class LessonOverlapReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.saved = load(DEFAULT_MAP_PATH)
        cls.by_id = {item["candidate_id"]: item for item in cls.saved["candidates"]}

    def test_saved_map_preserves_deterministic_overlap_result(self) -> None:
        predecessor = build_map()
        expected = {item["candidate_id"]: item for item in predecessor["candidates"]}
        self.assertEqual(set(expected), set(self.by_id))
        for candidate_id, candidate in expected.items():
            self.assertEqual(candidate["evidence_refs"], self.by_id[candidate_id]["evidence_refs"])
            self.assertEqual(candidate["mastery"], self.by_id[candidate_id]["mastery"])
        self.assertEqual(81, len(self.saved["candidates"]))

    def test_five_overlap_groups_are_merged(self) -> None:
        expected = {
            "lesson_candidate.identify_familiar_referents_from_spoken_clues",
            "lesson_candidate.complete_a_simple_information_form",
            "lesson_candidate.locate_names_places_and_times_in_slow_recordings",
            "lesson_candidate.describe_people_and_object_locations_orally",
            "lesson_candidate.relay_predictable_person_time_or_place_details",
        }
        self.assertTrue(expected <= set(self.by_id))
        old_ids = {
            "lesson_candidate.identify_objects_from_slow_spoken_clues",
            "lesson_candidate.complete_personal_details_form",
            "lesson_candidate.locate_people_names_in_dialogue",
            "lesson_candidate.say_where_people_are",
            "lesson_candidate.relay_personal_details_in_english",
        }
        self.assertFalse(old_ids & set(self.by_id))

    def test_compound_claims_are_reconciled_as_full(self) -> None:
        checks = {
            "lesson_candidate.complete_a_simple_information_form": "cefr.cv2020.p084.notes_messages_and_forms.01",
            "lesson_candidate.locate_names_places_and_times_in_slow_recordings": "gse.adult.2022.p14.007",
            "lesson_candidate.relay_predictable_person_time_or_place_details": "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01",
        }
        for candidate_id, record_id in checks.items():
            refs = {ref["record_id"]: ref for ref in self.by_id[candidate_id]["evidence_refs"]}
            self.assertEqual("full", refs[record_id]["coverage"])

    def test_mastery_alignment_cases_are_resolved(self) -> None:
        service = self.by_id["lesson_candidate.follow_a_slow_everyday_service_exchange"]
        self.assertEqual(["reception"], service["mode_codes"])
        self.assertNotIn("support.interaction_repair", {
            relation["support_id"] for relation in service["relationships"]["concurrent_support"]
        })
        message = self.by_id["lesson_candidate.leave_a_simple_whereabouts_and_return_message"]
        self.assertIn("control_or_repair", message["mastery"]["required_dimensions"])
        self.assertIn("control_or_repair", message["mastery"]["level_2_evidence"])


if __name__ == "__main__":
    unittest.main()
