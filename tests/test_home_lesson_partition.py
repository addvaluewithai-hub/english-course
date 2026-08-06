"""Acceptance tests for the home, objects, and descriptions partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_home_lesson_partition import ORTHOGRAPHIC_ID, build_map
from scripts.lesson_map_validation import validation_errors
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
HOME_CLUSTER = "home_objects_descriptions"
PRIOR_FULL = {
    "gse.adult.2022.p22.006",
    "gse.adult.2022.p22.027",
    "gse.adult.2022.p23.004",
    "gse.adult.2022.p23.008",
    "gse.adult.2022.p37.010",
    "cefr.cv2020.p063.sustained_monologue_describing_experience.01",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class HomeLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_home_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if HOME_CLUSTER in item["candidate_cluster_ids"]
        }
        used = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(29, len(assigned))
        self.assertEqual(set(), assigned - used - support)

    def test_prior_full_owners_are_not_duplicated(self) -> None:
        claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        )
        self.assertTrue(all(claims[record_id] == 1 for record_id in PRIOR_FULL))
        home_refs = {
            ref["record_id"] for candidate in self.home_candidates
            for ref in candidate["evidence_refs"]
        }
        self.assertTrue(PRIOR_FULL.isdisjoint(home_refs))

    def test_surroundings_and_possessions_are_named_partials(self) -> None:
        expected = {
            "cefr.cv2020.p049.understanding_conversation_between_other_people.01": "surroundings",
            "cefr.cv2020.p079.information_exchange.03": "things-they-have",
        }
        for record_id, phrase in expected.items():
            refs = [
                ref for candidate in self.home_candidates
                for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
            ]
            self.assertEqual(1, len(refs))
            self.assertEqual("partial", refs[0]["coverage"])
            self.assertIn(phrase, refs[0]["interpretation_note"])

    def test_object_copying_is_cross_cutting_support(self) -> None:
        candidates = [
            candidate["candidate_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["record_id"] == ORTHOGRAPHIC_ID
        ]
        self.assertEqual([], candidates)
        basic = self.lesson_map["support_definitions"][0]
        refs = [ref for ref in basic["evidence_refs"] if ref["record_id"] == ORTHOGRAPHIC_ID]
        self.assertEqual(1, len(refs))
        self.assertEqual(("cross_cutting", "full"), (refs[0]["role"], refs[0]["coverage"]))

    def test_home_candidates_stay_provisional_and_balanced(self) -> None:
        self.assertEqual(9, len(self.home_candidates))
        self.assertEqual("in_progress", self.lesson_map["status"])
        self.assertTrue(all(item["status"] == "needs_review" for item in self.home_candidates))
        skills = {code for item in self.home_candidates for code in item["skill_codes"]}
        modes = {code for item in self.home_candidates for code in item["mode_codes"]}
        self.assertEqual({"listening", "reading", "speaking", "writing"}, skills)
        self.assertEqual({"reception", "production", "interaction"}, modes)
        for candidate in self.home_candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])

    @property
    def home_candidates(self) -> list[dict]:
        return [
            item for item in self.lesson_map["candidates"]
            if item["candidate_cluster_ids"] == [HOME_CLUSTER]
        ]


if __name__ == "__main__":
    unittest.main()
