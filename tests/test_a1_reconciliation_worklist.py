"""Contract tests for the 81-candidate A1 reconciliation worklist."""

import json
import unittest

from scripts.a1_reconciliation_contract import OUTPUT
from scripts.create_a1_reconciliation_worklist import build
from scripts.validate_a1_reconciliation_worklist import validate


class A1ReconciliationWorklistTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_worklist_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_81_candidates_crosswalk_to_a1_source_evidence(self) -> None:
        self.assertEqual(81, len(self.data["candidates"]))
        self.assertEqual({"a1_only_evidence": 81}, self.data["audit"]["source_level_fit_counts"])
        for row in self.data["candidates"]:
            fit = row["evidence"]["level_fit"]
            self.assertEqual("a1_only_evidence", fit["status"])
            self.assertEqual([], fit["unmatched_record_ids"])
            self.assertEqual(["a1"], fit["all_level_codes"])

    def test_unit_one_membership_is_preserved_for_review(self) -> None:
        included = [row for row in self.data["candidates"] if row["unit1_membership"]["included"]]
        self.assertEqual(8, len(included))
        self.assertEqual(
            [f"U1-L{number:02d}" for number in range(1, 9)],
            sorted(row["unit1_membership"]["lesson_id"] for row in included),
        )

    def test_inventory_does_not_preapprove_any_candidate(self) -> None:
        for row in self.data["candidates"]:
            review = row["reconciliation"]
            self.assertEqual("pending", review["review_status"])
            self.assertIsNone(review["decision"])
            self.assertIsNone(review["rationale"])


if __name__ == "__main__":
    unittest.main()
