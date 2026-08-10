"""Contract tests for A1 function, dimension, overlap, and Unit 1 coverage."""

import json
import unittest

from scripts.a1_ability_coverage_contract import OUTPUT
from scripts.create_a1_ability_coverage_overlap_audit import build
from scripts.validate_a1_ability_coverage_overlap_audit import validate


class A1AbilityCoverageOverlapAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_audit_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_a1_functions_and_exit_dimensions_have_owners(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(24, audit["a1_function_count"])
        self.assertEqual(21, audit["candidate_owned_function_count"])
        self.assertEqual(3, audit["support_owned_function_count"])
        self.assertEqual([], audit["uncovered_function_codes"])
        self.assertEqual([], audit["uncovered_exit_dimensions"])

    def test_overlap_groups_are_constraints_not_final_merges(self) -> None:
        self.assertEqual(19, len(self.data["overlap_groups"]))
        self.assertTrue(all(row["decision_status"] == "requires_later_passes" for row in self.data["overlap_groups"]))
        self.assertEqual(0, self.data["audit"]["final_candidate_decisions_made"])

    def test_unit_one_is_revisable_and_retains_integrated_mastery(self) -> None:
        unit = self.data["unit1_audit"]
        self.assertEqual("requires_revision_not_rejection", unit["status"])
        self.assertEqual(8, len(unit["candidate_ids"]))
        self.assertEqual(3, unit["mastery_station_count"])
        self.assertEqual(1, len(unit["helpful_before_order_violations"]))
        self.assertEqual(3, len(unit["findings"]))


if __name__ == "__main__":
    unittest.main()
