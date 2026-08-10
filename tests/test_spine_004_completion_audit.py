"""Completion tests for the full A1-C2 progression-strand gate."""

import json
import unittest

from scripts.create_spine_004_completion_audit import build
from scripts.spine_004_audit_contract import OUTPUT
from scripts.validate_spine_004_completion_audit import validate


class Spine004CompletionAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_audit_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_sources_have_one_primary_evidence_treatment(self) -> None:
        ownership = self.data["source_ownership"]
        self.assertEqual(9274, ownership["normalized_record_count"])
        self.assertEqual(9274, ownership["owned_record_count"])
        self.assertEqual([], ownership["unowned_source_dataset_ids"])
        self.assertEqual([], ownership["duplicate_primary_dataset_owners"])

    def test_all_required_spine_components_pass(self) -> None:
        self.assertEqual(5, len(self.data["components"]))
        self.assertTrue(all(row["validation_status"] == "pass" for row in self.data["components"]))
        lifecycle = self.data["global_lifecycle_audit"]
        self.assertEqual(167, lifecycle["controlled_family_count"])
        self.assertEqual(1015, lifecycle["lifecycle_stage_count"])

    def test_item_selection_boundary_is_honest(self) -> None:
        boundary = self.data["controlled_item_boundary"]
        self.assertTrue(boundary["source_rows_are_not_automatic_targets"])
        self.assertFalse(boundary["current_a1_working_targets_are_final"])
        self.assertIn("SPINE-005", boundary["next_required_action"])

    def test_gate_opens_reconciliation_not_mass_production(self) -> None:
        gate = self.data["gate_decision"]
        self.assertEqual("pass_for_a1_reconciliation", gate["status"])
        self.assertEqual("SPINE-005", gate["next_task"])
        self.assertEqual("remains_blocked_until_SPINE-006", gate["mass_a1_production"])


if __name__ == "__main__":
    unittest.main()
