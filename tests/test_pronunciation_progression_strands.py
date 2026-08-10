"""Contract tests for A1-C2 pronunciation progression."""

import json
import unittest

from scripts.create_pronunciation_progression_strands import build
from scripts.pronunciation_progression_contract import OUTPUT
from scripts.validate_pronunciation_progression_strands import validate


class PronunciationProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_dataset_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_ten_strands_have_six_evidenced_stages(self) -> None:
        self.assertEqual(10, len(self.data["strands"]))
        for strand in self.data["strands"]:
            self.assertEqual(6, len(strand["stages"]))
            self.assertTrue(all(stage["cefr_boundary_evidence_count"] > 0 for stage in strand["stages"]))

    def test_arabic_risks_are_hypotheses_not_universal_facts(self) -> None:
        risks = self.data["arabic_learner_risk_hypotheses"]
        self.assertEqual(12, len(risks))
        for risk in risks:
            self.assertEqual("learner_risk_hypothesis_not_source_fact", risk["evidence_status"])
            self.assertIn("dialect_aware_learner_observation", risk["validation_route"])

    def test_accent_removal_is_explicitly_rejected(self) -> None:
        model = self.data["target_model"]
        self.assertIn("accent removal", model["non_goals"])
        self.assertIn("retained accent", model["accent_policy"].casefold())
        self.assertTrue(any("Never deduct" in rule for rule in self.data["assessment_contract"]["rules"]))


if __name__ == "__main__":
    unittest.main()
