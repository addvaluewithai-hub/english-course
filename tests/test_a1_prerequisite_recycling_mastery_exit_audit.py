"""Contract tests for A1 prerequisites, recycling, mastery, and exit safeguards."""

import json
import unittest

from scripts.a1_dependency_mastery_contract import OUTPUT
from scripts.create_a1_prerequisite_recycling_mastery_exit_audit import build
from scripts.validate_a1_prerequisite_recycling_mastery_exit_audit import validate


class A1PrerequisiteRecyclingMasteryExitAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_artifact_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_explicit_dependencies_fit_the_provisional_order(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(48, audit["explicit_dependency_edge_count"])
        self.assertEqual(48, audit["aligned_explicit_dependency_edges"])
        self.assertEqual(0, audit["unresolved_explicit_dependency_edges"])

    def test_exact_item_sequence_conflicts_are_visible_not_hidden(self) -> None:
        counts = self.data["audit"]["exact_item_sequence_status_counts"]
        self.assertEqual(98, counts["aligned"])
        self.assertEqual(51, counts["early_use_requires_introduction_transfer_or_reorder"])
        self.assertEqual(9, counts["no_later_recycle_requires_reorder_or_new_recycle"])
        self.assertEqual(60, self.data["audit"]["items_requiring_sequence_resolution"])

    def test_every_candidate_transfers_exact_roles_if_architecture_changes(self) -> None:
        impacts = self.data["candidate_ownership_impacts"]
        self.assertEqual(81, len(impacts))
        self.assertTrue(all(row["transfer_required_if_merged_supported_or_retired"] for row in impacts))
        self.assertTrue(all(row["introduction_item_ids"] or row["recycle_item_ids"] for row in impacts))

    def test_mastery_is_structurally_complete_and_construct_risks_are_actioned(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(81, audit["structurally_complete_mastery_records"])
        self.assertEqual(67, audit["mastery_constructs_aligned"])
        self.assertEqual(14, audit["mastery_constructs_requiring_revision"])
        revisions = [row for row in self.data["mastery_reviews"] if row["construct_alignment_status"].startswith("requires")]
        self.assertTrue(all(row["required_revision_actions"] for row in revisions))

    def test_all_exit_dimensions_have_protected_capability_anchors(self) -> None:
        safeguards = self.data["exit_safeguards"]
        self.assertEqual(7, len(safeguards))
        self.assertTrue(all(row["all_anchors_are_current_owners"] for row in safeguards))
        self.assertEqual(0, self.data["audit"]["final_candidate_decisions_made"])


if __name__ == "__main__":
    unittest.main()
