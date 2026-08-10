"""Contract tests for the locked A1 v1 scope and sequence."""

import json
import unittest

from scripts.a1_scope_sequence_contract import OUTPUT
from scripts.create_a1_scope_and_sequence import build
from scripts.validate_a1_scope_and_sequence import validate


class A1ScopeAndSequenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_artifact_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_six_units_contain_all_45_final_capabilities_once(self) -> None:
        audit = self.data["audit"]
        self.assertEqual([9, 9, 7, 7, 5, 8], audit["unit_lesson_counts"])
        self.assertEqual(45, audit["lesson_count"])
        self.assertEqual(45, audit["unique_lesson_owner_count"])

    def test_all_exact_items_have_ordered_lifecycles(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(158, audit["exact_item_count"])
        self.assertEqual({"retained_named_introduction": 118, "transferred_to_earliest_final_use": 40}, audit["introduction_resolution_counts"])
        self.assertEqual({"existing_final_owner": 146, "unit_review_added": 12}, audit["first_recycle_resolution_counts"])
        self.assertEqual(60, audit["carried_sequence_findings_resolved"])
        self.assertEqual(0, audit["unresolved_item_placements"])

    def test_all_final_prerequisites_are_in_order(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(24, audit["mapped_prerequisite_edge_count"])
        self.assertEqual(24, audit["aligned_mapped_prerequisite_edges"])

    def test_every_capability_has_fresh_unit_mastery(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(19, audit["unit_mastery_station_count"])
        self.assertEqual(45, audit["capabilities_with_unit_mastery"])
        stations = [station for unit in self.data["units"] for station in unit["unit_review"]["mastery_stations"]]
        self.assertTrue(all(not row["answer_revealing_support_allowed"] for row in stations))

    def test_exit_assessment_covers_all_dimensions(self) -> None:
        self.assertEqual(7, self.data["audit"]["exit_station_count"])
        self.assertEqual(7, self.data["audit"]["exit_dimensions_covered"])
        self.assertTrue(self.data["exit_assessment"]["all_seven_dimensions_required"])

    def test_gold_lesson_is_preserved_after_input(self) -> None:
        migration = self.data["unit1_prototype_migration"]
        self.assertEqual(8, migration["old_capabilities_preserved_in_new_unit"])
        self.assertEqual("U1-L01", migration["old_gold_lesson_id"])
        self.assertEqual("U1-L03", migration["new_gold_lesson_id"])
        self.assertEqual("gold/introduce-yourself", migration["gold_content_path"])


if __name__ == "__main__":
    unittest.main()
