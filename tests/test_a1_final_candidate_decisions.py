"""Contract tests for final A1 candidate dispositions."""

import json
import unittest

from scripts.a1_final_decisions_contract import OUTPUT
from scripts.create_a1_final_candidate_decisions import build
from scripts.validate_a1_final_candidate_decisions import validate


class A1FinalCandidateDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_artifact_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_81_candidates_have_final_decisions(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(81, audit["candidate_count"])
        self.assertEqual({"keep": 23, "merge": 21, "revise": 22, "split": 1, "support_only": 14}, audit["decision_counts"])
        self.assertTrue(all(not row["unresolved_questions"] for row in self.data["decisions"]))

    def test_final_architecture_is_lean_without_losing_sources(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(45, audit["final_lesson_capability_count"])
        self.assertEqual(1, audit["support_owner_count"])
        self.assertEqual(158, audit["final_exact_item_count"])
        self.assertEqual(216, audit["ownership_transfer_count"])
        owners = self.data["final_lesson_capabilities"] + self.data["support_owners"]
        self.assertEqual(158, len({item for row in owners for item in row["introduction_item_ids"]}))
        self.assertEqual(158, len({item for row in owners for item in row["recycle_item_ids"]}))

    def test_scope_revision_signals_are_resolved(self) -> None:
        self.assertEqual(0, self.data["audit"]["scope_revision_candidates_kept_without_revision"])
        revised = [row for row in self.data["decisions"] if row["decision"] == "revise"]
        self.assertTrue(all(row["revised_outcome_statement"] for row in revised))

    def test_exit_and_unit_one_capabilities_survive(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(31, audit["resolved_exit_anchor_count"])
        self.assertEqual(0, audit["unresolved_exit_anchor_count"])
        self.assertEqual(8, audit["surviving_unit1_capability_count"])

    def test_final_order_remains_a_separate_gate(self) -> None:
        self.assertEqual(60, self.data["audit"]["sequence_findings_carried_forward"])
        self.assertEqual("blocked_until_SPINE_006", self.data["policy"]["mass_production_status"])


if __name__ == "__main__":
    unittest.main()
