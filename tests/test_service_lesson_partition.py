"""Acceptance tests for the food, shopping, and services partition."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.create_service_lesson_partition import build_map
from scripts.lesson_map_validation import validation_errors
from scripts.lesson_service_specs import SERVICE_SPECS
from tests.lesson_partition_assertions import assert_partition_prefix


ROOT = Path(__file__).resolve().parents[1]
MAP_PATH = ROOT / "data/reviewed/a1-lesson-map.json"
CLUSTER_MAP_PATH = ROOT / "data/reviewed/a1-candidate-unit-map.json"
SERVICE_CLUSTER = "food_shopping_services"
PRIOR_FULL = {
    "gse.adult.2022.p22.011": "lesson_candidate.buy_a_basic_public_transport_ticket",
    "cefr.cv2020.p072.overall_oral_interaction.01": None,
}


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


class ServiceLessonPartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.lesson_map = build_map()
        cls.cluster_map = load(CLUSTER_MAP_PATH)
        cls.service_ids = {item["candidate_id"] for item in SERVICE_SPECS}

    def test_reviewed_map_matches_deterministic_builder(self) -> None:
        assert_partition_prefix(self, build_map(), self.lesson_map)

    def test_map_passes_schema_and_semantic_validation(self) -> None:
        self.assertEqual([], validation_errors(MAP_PATH))

    def test_all_service_assignments_are_reconciled(self) -> None:
        assigned = {
            item["record_id"] for item in self.cluster_map["assignments"]
            if SERVICE_CLUSTER in item["candidate_cluster_ids"]
        }
        used = {
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] != "context_only"
        }
        support = {
            ref["record_id"] for item in self.lesson_map["support_definitions"]
            for ref in item["evidence_refs"] if ref["coverage"] != "context_only"
        }
        self.assertEqual(30, len(assigned))
        self.assertEqual(set(), assigned - used - support)

    def test_prior_full_owners_are_not_duplicated(self) -> None:
        claims = Counter(
            ref["record_id"] for candidate in self.lesson_map["candidates"]
            for ref in candidate["evidence_refs"] if ref["coverage"] == "full"
        )
        self.assertEqual(1, claims["gse.adult.2022.p22.011"])
        service_refs = {
            ref["record_id"] for candidate in self.service_candidates
            for ref in candidate["evidence_refs"]
        }
        self.assertTrue(PRIOR_FULL.keys().isdisjoint(service_refs))

    def test_shared_price_clauses_are_named_partial_claims(self) -> None:
        expected = {
            "gse.adult.2022.p15.008": "prices clause",
            "cefr.cv2020.p051.understanding_announcements_and_instructions.03": "shop-price",
        }
        for record_id, phrase in expected.items():
            refs = [
                ref for candidate in self.service_candidates
                for ref in candidate["evidence_refs"] if ref["record_id"] == record_id
            ]
            self.assertEqual(1, len(refs))
            self.assertEqual("partial", refs[0]["coverage"])
            self.assertIn(phrase, refs[0]["interpretation_note"])

    def test_repeated_ask_and_give_wording_keeps_both_scale_records(self) -> None:
        candidate = self.by_id("lesson_candidate.ask_for_and_give_an_everyday_item")
        ids = {ref["record_id"] for ref in candidate["evidence_refs"]}
        self.assertIn("cefr.cv2020.p077.goal_oriented_co_operation.03", ids)
        self.assertIn("cefr.cv2020.p078.obtaining_goods_and_services.01", ids)

    def test_shared_form_and_strategy_candidates_are_explicit(self) -> None:
        expected = {
            "lesson_candidate.find_key_details_in_a_simple_advertisement_or_leaflet": {
                "food_shopping_services", "messages_signs_forms"
            },
            "lesson_candidate.leave_a_simple_whereabouts_and_return_message": {
                "messages_signs_forms"
            },
            "lesson_candidate.relay_names_numbers_and_prices_from_slow_speech": {
                "food_shopping_services", "communication_strategies"
            },
        }
        for candidate_id, clusters in expected.items():
            self.assertEqual(clusters, set(self.by_id(candidate_id)["candidate_cluster_ids"]))

    def test_online_transaction_has_reciprocal_repair_support(self) -> None:
        candidate = self.by_id(
            "lesson_candidate.complete_a_very_simple_online_purchase_or_application"
        )
        support_ids = {
            item["support_id"] for item in candidate["relationships"]["concurrent_support"]
        }
        self.assertIn("support.interaction_repair", support_ids)
        repair = self.lesson_map["support_definitions"][1]
        self.assertIn(candidate["candidate_id"], repair["applies_to_candidate_ids"])

    def test_service_candidates_stay_provisional_and_cover_source_modes(self) -> None:
        self.assertEqual(13, len(self.service_candidates))
        self.assertTrue(all(item["status"] == "needs_review" for item in self.service_candidates))
        skills = {code for item in self.service_candidates for code in item["skill_codes"]}
        modes = {code for item in self.service_candidates for code in item["mode_codes"]}
        self.assertTrue({"listening", "reading", "speaking", "writing"} <= skills)
        self.assertEqual(
            {"reception", "production", "interaction", "online_interaction", "mediation"},
            modes,
        )
        for candidate in self.service_candidates:
            self.assertEqual([], candidate["relationships"]["required_before"])
            self.assertEqual([], candidate["relationships"]["successors"])

    @property
    def service_candidates(self) -> list[dict]:
        return [
            item for item in self.lesson_map["candidates"]
            if item["candidate_id"] in self.service_ids
        ]

    def by_id(self, candidate_id: str) -> dict:
        return next(item for item in self.lesson_map["candidates"] if item["candidate_id"] == candidate_id)


if __name__ == "__main__":
    unittest.main()
