"""Acceptance tests for the social-contact and collaboration partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_social_lesson_partition import GREETING_SPELLING_ID, build_map
from scripts.lesson_map_validation import validation_errors
from scripts.lesson_social_specs import SOCIAL_SPECS
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
SOCIAL_CLUSTER = "social_contact_collaboration"
PRIOR_FULL = {
    "gse.adult.2022.p15.014", "gse.adult.2022.p22.022",
    "cefr.cv2020.p086.online_conversation_and_discussion.02",
}
NEW_RECORDS = {
    "gse.adult.2022.p22.012", "gse.adult.2022.p22.013",
    "gse.adult.2022.p23.001", "gse.adult.2022.p23.002",
    "gse.adult.2022.p23.010", "gse.adult.2022.p23.012",
    "gse.adult.2022.p24.003", GREETING_SPELLING_ID,
    "cefr.cv2020.p066.addressing_audiences.01",
    "cefr.cv2020.p074.conversation.03", "cefr.cv2020.p074.conversation.04",
    "cefr.cv2020.p107.expressing_a_personal_response_to_creative_texts.01",
    "cefr.cv2020.p111.facilitating_collaborative_interaction_with_peers.01",
    "cefr.cv2020.p111.collaborating_to_construct_meaning.01",
    "cefr.cv2020.p113.encouraging_conceptual_talk.01",
    "cefr.cv2020.p115.facilitating_pluricultural_space.01",
    "cefr.cv2020.p117.facilitating_communication_in_delicate_situations_and_disagreements.01",
    "cefr.cv2020.p137.sociolinguistic_appropriateness.01",
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class SocialLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)
        cls.new_ids = {item["candidate_id"] for item in SOCIAL_SPECS}

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_social_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if SOCIAL_CLUSTER in item["candidate_cluster_ids"]
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

    def test_prior_full_owners_are_retained_once(self) -> None:
        claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        )
        self.assertTrue(all(claims[record_id] == 1 for record_id in PRIOR_FULL))

    def test_all_eighteen_previously_uncited_records_are_explicit(self) -> None:
        refs = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"]
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"]
        }
        self.assertTrue(NEW_RECORDS <= refs | support)

    def test_compound_social_descriptors_have_named_partial_claims(self) -> None:
        expected = {
            "gse.adult.2022.p23.012": 2,
            "cefr.cv2020.p074.conversation.03": 2,
            "cefr.cv2020.p092.overall_mediation.01": 2,
            "cefr.cv2020.p115.facilitating_pluricultural_space.01": 2,
            "cefr.cv2020.p137.sociolinguistic_appropriateness.01": 3,
        }
        for record_id, count in expected.items():
            refs = [
                ref for candidate in self.lesson_map["candidates"]
                for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
            ]
            self.assertEqual(count, len(refs), record_id)
            self.assertTrue(all(ref["coverage"] == "partial" for ref in refs))
            self.assertTrue(all(ref["interpretation_note"].strip() for ref in refs))

    def test_greeting_spelling_is_cross_cutting_support(self) -> None:
        candidate_refs = [
            ref for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["record_id"] == GREETING_SPELLING_ID
        ]
        basic_refs = [
            ref for ref in self.lesson_map["support_definitions"][0]["evidence_refs"]
            if ref["record_id"] == GREETING_SPELLING_ID
        ]
        self.assertEqual([], candidate_refs)
        self.assertEqual(("cross_cutting", "full"), (basic_refs[0]["role"], basic_refs[0]["coverage"]))

    def test_new_candidates_stay_provisional_and_source_balanced(self) -> None:
        candidates = [
            item for item in self.lesson_map["candidates"]
            if item["candidate_id"] in self.new_ids
        ]
        self.assertEqual(11, len(candidates))
        self.assertTrue(all(item["status"] == "needs_review" for item in candidates))
        skills = {code for item in candidates for code in item["skill_codes"]}
        modes = {code for item in candidates for code in item["mode_codes"]}
        self.assertTrue({"listening", "speaking", "writing", "non_verbal", "language_system"} <= skills)
        self.assertEqual({"production", "interaction", "mediation", "communicative_competence"}, modes)
        for candidate in candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])


if __name__ == "__main__":
    unittest.main()
