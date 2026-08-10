"""Contract tests for exact A1 pronunciation and intelligibility ownership."""

import json
import unittest

from scripts.a1_pronunciation_ownership_contract import OUTPUT
from scripts.create_a1_pronunciation_ownership import build
from scripts.validate_a1_pronunciation_ownership import validate


class A1PronunciationOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.targets = {row["target_id"]: row for row in cls.data["targets"]}

    def test_artifact_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_strands_and_legacy_targets_have_exact_owners(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(20, audit["target_count"])
        self.assertEqual(10, audit["strand_count"])
        self.assertEqual(54, audit["legacy_pronunciation_candidate_count"])
        self.assertEqual([], audit["uncovered_pronunciation_candidate_ids"])
        self.assertEqual([], audit["uncovered_strand_ids"])

    def test_every_example_has_reference_ipa_and_fresh_recycle(self) -> None:
        audit = self.data["audit"]
        self.assertEqual([], audit["examples_without_reference_ipa"])
        self.assertEqual([], audit["targets_without_recycle_locations"])
        for row in self.data["targets"]:
            self.assertNotIn(row["introduction_location"], row["recycle_locations"])

    def test_arabic_risks_are_hypotheses_not_presumed_deficits(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(12, audit["arabic_risk_hypothesis_count"])
        self.assertEqual(1, audit["risk_disposition_counts"]["monitor_if_observed_not_pre_taught"])
        velar = next(row for row in self.data["risk_dispositions"] if row["risk_id"].endswith("velar_nasal"))
        self.assertEqual([], velar["selected_target_ids"])
        self.assertIn("never infer", velar["rationale"])

    def test_goal_is_intelligibility_not_accent_removal(self) -> None:
        self.assertIn("never remove an accent", self.data["policy"]["goal"])
        self.assertIn("not an imitation target", self.data["policy"]["reference_model"])
        self.assertEqual("receptive_with_guided_imitation", self.targets["a1_pronunciation.frequent_contractions"]["control_status"])

    def test_can_cant_reversal_is_explicit(self) -> None:
        target = self.targets["a1_pronunciation.can_cant_contrast"]
        self.assertIn("reverses the message", target["meaning_risk"])
        self.assertEqual(0, self.data["audit"]["final_lesson_decisions_made"])


if __name__ == "__main__":
    unittest.main()
