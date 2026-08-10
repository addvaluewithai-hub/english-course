"""Contract tests for the first reviewed A1 candidate pass."""

import json
import unittest

from scripts.a1_outcome_review_contract import OUTPUT
from scripts.create_a1_outcome_level_fit_review import build
from scripts.validate_a1_outcome_level_fit_review import validate


class A1OutcomeLevelFitReviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_review_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_candidates_are_reviewed_against_a1_claims(self) -> None:
        self.assertEqual(81, len(self.data["reviews"]))
        for row in self.data["reviews"]:
            self.assertTrue(row["a1_source_fit_confirmed"])
            self.assertIn("a1.exit_promise", row["profile_claim_ids"])
            self.assertEqual("accepted_first_pass", row["review_status"])

    def test_scope_and_independence_risks_are_not_hidden(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(14, audit["fit_status_counts"]["fits_a1_with_scope_revision"])
        self.assertEqual(25, audit["independence_signal_counts"]["merge_review"])
        self.assertEqual(10, audit["independence_signal_counts"]["support_only_review"])
        self.assertEqual(1, audit["independence_signal_counts"]["split_review"])

    def test_first_pass_does_not_make_final_candidate_decisions(self) -> None:
        self.assertEqual(0, self.data["audit"]["final_candidate_decisions_made"])
        self.assertTrue(all("decision" not in row for row in self.data["reviews"]))


if __name__ == "__main__":
    unittest.main()
