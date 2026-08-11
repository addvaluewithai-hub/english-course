"""Contract tests for TEST-001 learner-test readiness."""

import copy
import json
import unittest

from jsonschema import Draft202012Validator

from scripts.learner_session_record_rules import semantic_errors
from scripts.learner_test_v1_contract import (
    GATING_METRICS, PROTOTYPE, SCHEMA, TEMPLATE, THRESHOLDS,
)
from scripts.learner_test_v1_validation_core import validate


class LearnerTestV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.template = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        cls.thresholds = json.loads(THRESHOLDS.read_text(encoding="utf-8"))

    def _valid_record(self) -> dict:
        record = copy.deepcopy(self.template)
        record["participant"].update({
            "adult_confirmed": True, "arabic_speaking": True,
            "entry_band": "a1", "eligible_primary_sample": True,
        })
        record["consent"].update({
            "voluntary_confirmed": True, "data_boundary_confirmed": True,
            "participation_agreed": True,
        })
        record["completion"].update({
            "outcome": "completed", "last_step": 9, "fresh_task_attempted": True,
        })
        record["mastery"].update({
            "evidence_valid": True, "full_model_visible": False,
            "ratings": {
                "comprehension": 2, "outcome_performance": 2,
                "context_transfer": 2, "control_or_repair": 2,
            },
            "decision": "demonstrated",
        })
        record["data_controls"]["withdrawal_route_given"] = True
        return record

    def test_complete_kit_passes_repository_gate(self) -> None:
        self.assertEqual([], validate())

    def test_blank_template_matches_json_schema(self) -> None:
        self.assertEqual([], list(Draft202012Validator(self.schema).iter_errors(self.template)))

    def test_valid_private_session_record_passes_semantics(self) -> None:
        record = self._valid_record()
        self.assertEqual([], list(Draft202012Validator(self.schema).iter_errors(record)))
        self.assertEqual([], semantic_errors(record))

    def test_mastery_cannot_pass_with_a_visible_model(self) -> None:
        record = self._valid_record()
        record["mastery"]["full_model_visible"] = True
        self.assertTrue(any("invalidates" in error or "independent" in error for error in semantic_errors(record)))

    def test_condition_allocation_is_pre_registered(self) -> None:
        record = self._valid_record()
        record["condition"]["post_performance"] = "omit"
        self.assertIn("post-performance condition violates odd/even allocation", semantic_errors(record))

    def test_double_rating_requires_consistent_agreement(self) -> None:
        record = self._valid_record()
        record["reliability"] = {
            "double_rated": True,
            "secondary_ratings": dict(record["mastery"]["ratings"]),
            "secondary_decision": "practiced",
            "exact_decision_agreement": True,
        }
        self.assertIn("double-rated agreement flag does not match the two decisions", semantic_errors(record))

    def test_all_nine_gating_metrics_are_fixed(self) -> None:
        metrics = {row["metric_id"] for row in self.thresholds["gating_metrics"]}
        self.assertEqual(GATING_METRICS, metrics)
        self.assertEqual(8, self.thresholds["sample"]["target_completed_sessions"])
        self.assertEqual(6, self.thresholds["sample"]["minimum_eligible_completed_sessions"])

    def test_prototype_tracks_timing_without_reading_answers(self) -> None:
        research = (PROTOTYPE / "scripts/research.js").read_text(encoding="utf-8")
        self.assertIn("contains_raw_answer: false", research)
        self.assertNotIn("masteryAnswer", research)
        self.assertNotIn("localStorage", research)


if __name__ == "__main__":
    unittest.main()
