"""Acceptance tests for the messages, signs, and forms partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_message_lesson_partition import build_map
from scripts.lesson_map_validation import validation_errors
from scripts.lesson_message_specs import MESSAGE_SPECS
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
MESSAGE_CLUSTER = "messages_signs_forms"
PRIOR_FULL = {
    "gse.adult.2022.p09.010", "gse.adult.2022.p15.011",
    "gse.adult.2022.p37.001", "gse.adult.2022.p37.011",
    "gse.adult.2022.p37.016", "cefr.cv2020.p055.reading_correspondence.02",
    "cefr.cv2020.p056.reading_for_orientation.04",
    "cefr.cv2020.p083.correspondence.01", "cefr.cv2020.p083.correspondence.03",
    "cefr.cv2020.p084.notes_messages_and_forms.01",
    "cefr.cv2020.p084.notes_messages_and_forms.02",
    "cefr.cv2020.p086.online_conversation_and_discussion.01",
    "cefr.cv2020.p087.goal_oriented_online_transactions_and_collaboration.01",
}
NEW_RECORDS = {
    "gse.adult.2022.p09.005", "cefr.cv2020.p053.watching_tv_film_and_video.01",
    "cefr.cv2020.p055.reading_correspondence.01",
    "cefr.cv2020.p056.reading_for_orientation.01",
    "cefr.cv2020.p083.correspondence.02",
    "cefr.cv2020.p086.online_conversation_and_discussion.02",
    "cefr.cv2020.p092.overall_mediation.01",
    "cefr.cv2020.p101.processing_text_in_speech_or_sign.01",
    "cefr.cv2020.p104.translating_a_written_text_in_speech_or.01",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class MessageLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)
        cls.message_ids = {item["candidate_id"] for item in MESSAGE_SPECS}

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_message_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if MESSAGE_CLUSTER in item["candidate_cluster_ids"]
        }
        used = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(22, len(assigned))
        self.assertEqual(set(), assigned - used - support)

    def test_prior_full_owners_are_not_duplicated(self) -> None:
        claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        )
        self.assertTrue(all(claims[record_id] == 1 for record_id in PRIOR_FULL))
        message_refs = {
            ref["record_id"] for candidate in self.message_candidates
            for ref in candidate["evidence_refs"]
        }
        self.assertTrue(PRIOR_FULL.isdisjoint(message_refs))

    def test_all_nine_previously_uncited_records_are_now_explicit(self) -> None:
        all_refs = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"]
        }
        self.assertTrue(NEW_RECORDS <= all_refs)
        message_refs = {
            ref["record_id"] for candidate in self.message_candidates
            for ref in candidate["evidence_refs"]
        }
        self.assertEqual(
            NEW_RECORDS - {"cefr.cv2020.p083.correspondence.02"}, message_refs
        )

    def test_postcard_writing_extends_the_existing_friend_message(self) -> None:
        candidate = self.by_id("lesson_candidate.write_a_short_message_to_a_friend")
        refs = {ref["record_id"] for ref in candidate["evidence_refs"]}
        self.assertIn("cefr.cv2020.p083.correspondence.02", refs)
        self.assertIn("postcard", candidate["outcome"]["situation"])
        self.assertEqual(
            {"people_relationships", MESSAGE_CLUSTER},
            set(candidate["candidate_cluster_ids"]),
        )

    def test_visual_media_descriptor_is_split_into_named_partial_claims(self) -> None:
        record_id = "cefr.cv2020.p053.watching_tv_film_and_video.01"
        refs = [
            ref for candidate in self.message_candidates
            for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
        ]
        self.assertEqual(2, len(refs))
        self.assertTrue(all(ref["coverage"] == "partial" for ref in refs))
        notes = " ".join(ref["interpretation_note"] for ref in refs)
        self.assertIn("headline-news topic clause", notes)
        self.assertIn("advertised-products clause", notes)
        product = self.by_id(
            "lesson_candidate.identify_a_product_in_a_short_video_advertisement"
        )
        self.assertEqual({"listening", "viewing"}, set(product["skill_codes"]))
        self.assertIn("video advertisement", product["outcome"]["situation"])

    def test_overall_mediation_keeps_social_clause_open(self) -> None:
        record_id = "cefr.cv2020.p092.overall_mediation.01"
        refs = [
            ref for candidate in self.message_candidates
            for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
        ]
        self.assertEqual(1, len(refs))
        self.assertEqual("partial", refs[0]["coverage"])
        self.assertIn("showing interest in an idea remains", refs[0]["interpretation_note"])

    def test_online_reaction_has_reciprocal_repair_support(self) -> None:
        candidate = self.by_id("lesson_candidate.react_politely_to_a_simple_online_post")
        support_ids = {
            item["support_id"] for item in candidate["relationships"]["concurrent_support"]
        }
        self.assertIn("support.interaction_repair", support_ids)
        repair = self.lesson_map["support_definitions"][1]
        self.assertIn(candidate["candidate_id"], repair["applies_to_candidate_ids"])

    def test_message_candidates_stay_provisional_and_cover_source_modes(self) -> None:
        self.assertEqual(7, len(self.message_candidates))
        self.assertTrue(all(item["status"] == "needs_review" for item in self.message_candidates))
        partition = [
            *self.message_candidates,
            self.by_id("lesson_candidate.write_a_short_message_to_a_friend"),
        ]
        skills = {code for item in partition for code in item["skill_codes"]}
        modes = {code for item in partition for code in item["mode_codes"]}
        self.assertTrue({"listening", "reading", "speaking", "writing", "viewing"} <= skills)
        self.assertEqual({"reception", "interaction", "online_interaction", "mediation"}, modes)
        for candidate in self.message_candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])

    @property
    def message_candidates(self) -> list[dict]:
        return [
            item for item in self.lesson_map["candidates"]
            if item["candidate_id"] in self.message_ids
        ]

    def by_id(self, candidate_id: str) -> dict:
        return next(item for item in self.lesson_map["candidates"] if item["candidate_id"] == candidate_id)


if __name__ == "__main__":
    unittest.main()
