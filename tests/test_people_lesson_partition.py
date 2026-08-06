"""Acceptance tests for the people-and-relationships lesson-map partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_people_lesson_partition import build_map
from scripts.lesson_map_validation import validation_errors
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
PEOPLE_CLUSTER = "people_relationships"
IDENTITY_FULL = {
    "gse.adult.2022.p22.006",
    "gse.adult.2022.p23.004",
    "gse.adult.2022.p37.010",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class PeopleLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_people_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if PEOPLE_CLUSTER in item["candidate_cluster_ids"]
        }
        used = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(21, len(assigned))
        self.assertEqual(set(), assigned - used - support)

    def test_shared_full_identity_anchors_are_not_duplicated(self) -> None:
        full_claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"]
            if ref["coverage"] == "full"
        )
        self.assertTrue(all(full_claims[record_id] == 1 for record_id in IDENTITY_FULL))
        people_refs = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            if PEOPLE_CLUSTER in candidate["candidate_cluster_ids"]
            for ref in candidate["evidence_refs"]
        }
        self.assertTrue(IDENTITY_FULL.isdisjoint(people_refs))

    def test_shared_compound_clauses_remain_named_partial_claims(self) -> None:
        shared = {
            "cefr.cv2020.p079.information_exchange.03": 2,
            "cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01": 2,
        }
        for record_id, expected_count in shared.items():
            refs = [
                ref for candidate in self.lesson_map["candidates"]
                for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
            ]
            self.assertEqual(expected_count, len(refs))
            self.assertTrue(all(ref["coverage"] == "partial" for ref in refs))
            self.assertTrue(all(ref["interpretation_note"].strip() for ref in refs))

    def test_people_candidates_stay_provisional_and_balanced(self) -> None:
        candidates = [
            item for item in self.lesson_map["candidates"]
            if PEOPLE_CLUSTER in item["candidate_cluster_ids"]
        ]
        self.assertEqual(9, len(candidates))
        self.assertEqual("in_progress", self.lesson_map["status"])
        self.assertTrue(all(item["status"] == "needs_review" for item in candidates))
        skills = {code for item in candidates for code in item["skill_codes"]}
        modes = {code for item in candidates for code in item["mode_codes"]}
        self.assertEqual({"listening", "reading", "speaking", "writing"}, skills)
        self.assertEqual({"reception", "production", "interaction", "mediation"}, modes)
        for candidate in candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])


if __name__ == "__main__":
    unittest.main()
