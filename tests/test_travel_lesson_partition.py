"""Acceptance tests for the places, directions, and travel partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_travel_lesson_partition import DIRECTION_COPY_ID, build_map
from scripts.lesson_map_validation import validation_errors
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
TRAVEL_CLUSTER = "places_directions_travel"
PRIOR_FULL = {
    "gse.adult.2022.p09.010",
    "gse.adult.2022.p22.001",
    "cefr.cv2020.p055.reading_correspondence.02",
    "cefr.cv2020.p084.notes_messages_and_forms.01",
    "cefr.cv2020.p095.relaying_specific_information_in_speech_or_sign.01",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class TravelLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_travel_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if TRAVEL_CLUSTER in item["candidate_cluster_ids"]
        }
        used = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(31, len(assigned))
        self.assertEqual(set(), assigned - used - support)

    def test_prior_full_owners_are_not_duplicated(self) -> None:
        claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        )
        self.assertTrue(all(claims[record_id] == 1 for record_id in PRIOR_FULL))
        travel_refs = {
            ref["record_id"] for candidate in self.travel_candidates
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        }
        self.assertTrue(PRIOR_FULL.isdisjoint(travel_refs))

    def test_shared_clauses_are_named_partial_claims(self) -> None:
        expected = {
            "gse.adult.2022.p14.007": "place names",
            "cefr.cv2020.p048.overall_oral_comprehension.02": "place information",
            "cefr.cv2020.p057.reading_for_information_and_argument.02": "travel-text",
            "cefr.cv2020.p077.goal_oriented_co_operation.02": "locations",
            "cefr.cv2020.p084.notes_messages_and_forms.01": "arrival-in-country",
        }
        for record_id, phrase in expected.items():
            refs = [
                ref for candidate in self.travel_candidates
                for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
            ]
            self.assertEqual(1, len(refs))
            self.assertEqual("partial", refs[0]["coverage"])
            self.assertIn(phrase, refs[0]["interpretation_note"])

    def test_immediate_location_extends_the_existing_home_candidate(self) -> None:
        record_id = "cefr.cv2020.p051.understanding_announcements_and_instructions.02"
        owners = [
            candidate["candidate_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
        ]
        self.assertEqual(
            ["lesson_candidate.understand_where_things_or_people_are"], owners
        )

    def test_direction_copying_is_cross_cutting_support(self) -> None:
        candidate_refs = [
            ref for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["record_id"] == DIRECTION_COPY_ID
        ]
        basic_refs = [
            ref for ref in self.lesson_map["support_definitions"][0]["evidence_refs"]
            if ref["record_id"] == DIRECTION_COPY_ID
        ]
        self.assertEqual([], candidate_refs)
        self.assertEqual(1, len(basic_refs))
        self.assertEqual(("cross_cutting", "full"), (basic_refs[0]["role"], basic_refs[0]["coverage"]))

    def test_travel_candidates_stay_provisional_and_balanced(self) -> None:
        self.assertEqual(12, len(self.travel_candidates))
        self.assertTrue(all(item["status"] == "needs_review" for item in self.travel_candidates))
        skills = {code for item in self.travel_candidates for code in item["skill_codes"]}
        modes = {code for item in self.travel_candidates for code in item["mode_codes"]}
        self.assertEqual({"listening", "reading", "speaking", "writing"}, skills)
        self.assertEqual({"reception", "production", "interaction"}, modes)
        for candidate in self.travel_candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])

    @property
    def travel_candidates(self) -> list[dict]:
        return [
            item for item in self.lesson_map["candidates"]
            if item["candidate_cluster_ids"] == [TRAVEL_CLUSTER]
        ]


if __name__ == "__main__":
    unittest.main()
