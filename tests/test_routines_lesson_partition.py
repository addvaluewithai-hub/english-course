"""Acceptance tests for the routines, time, and leisure lesson partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_routines_lesson_partition import build_map
from scripts.lesson_map_validation import validation_errors
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
ROUTINES_CLUSTER = "routines_time_leisure"
IDENTITY_FULL = "gse.adult.2022.p22.023"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class RoutinesLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_routines_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if ROUTINES_CLUSTER in item["candidate_cluster_ids"]
        }
        used = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(38, len(assigned))
        self.assertEqual(set(), assigned - used - support)

    def test_identity_hobby_anchor_is_not_duplicated(self) -> None:
        refs = [
            (candidate["candidate_id"], ref)
            for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["record_id"] == IDENTITY_FULL
        ]
        self.assertEqual(1, len(refs))
        self.assertEqual("lesson_candidate.give_short_self_introduction", refs[0][0])
        self.assertEqual("full", refs[0][1]["coverage"])

    def test_shared_family_and_personal_relevance_clauses_are_partial(self) -> None:
        shared = {
            "cefr.cv2020.p049.understanding_conversation_between_other_people.01": 2,
            "cefr.cv2020.p066.overall_written_production.01": 2,
        }
        for record_id, expected_count in shared.items():
            refs = [
                ref for candidate in self.lesson_map["candidates"]
                for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
            ]
            self.assertEqual(expected_count, len(refs))
            self.assertTrue(all(ref["coverage"] == "partial" for ref in refs))
            self.assertTrue(all(ref["interpretation_note"].strip() for ref in refs))

    def test_full_shared_claims_have_one_owner(self) -> None:
        shared = {
            "gse.adult.2022.p09.010",
            "cefr.cv2020.p055.reading_correspondence.02",
            "cefr.cv2020.p083.correspondence.01",
            "cefr.cv2020.p086.online_conversation_and_discussion.01",
            "cefr.cv2020.p095.relaying_specific_information_in_speech_or_sign.01",
        }
        claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        )
        self.assertTrue(all(claims[record_id] == 1 for record_id in shared))

    def test_routines_candidates_stay_provisional_and_balanced(self) -> None:
        candidates = [
            item for item in self.lesson_map["candidates"]
            if item["candidate_cluster_ids"] == [ROUTINES_CLUSTER]
        ]
        self.assertEqual(14, len(candidates))
        self.assertEqual("in_progress", self.lesson_map["status"])
        self.assertTrue(all(item["status"] == "needs_review" for item in candidates))
        skills = {code for item in candidates for code in item["skill_codes"]}
        modes = {code for item in candidates for code in item["mode_codes"]}
        self.assertEqual({"listening", "reading", "speaking", "writing"}, skills)
        self.assertEqual(
            {"reception", "production", "interaction", "online_interaction", "mediation"},
            modes,
        )
        for candidate in candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])


if __name__ == "__main__":
    unittest.main()
