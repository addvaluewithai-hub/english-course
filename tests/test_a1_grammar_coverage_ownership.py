"""Contract tests for exact A1 grammar selection and ownership."""

import json
import unittest

from scripts.a1_grammar_ownership_contract import OUTPUT
from scripts.create_a1_grammar_coverage_ownership import build
from scripts.validate_a1_grammar_coverage_ownership import validate


class A1GrammarCoverageOwnershipTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.items = {row["item_id"]: row for row in cls.data["course_items"]}

    def test_artifact_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_source_records_have_one_primary_disposition(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(109, audit["egp_a1_source_count"])
        self.assertEqual(43, audit["gse_grammar_a1_source_count"])
        self.assertEqual(152, audit["total_source_count"])
        ids = [row["source_record_id"] for row in self.data["source_dispositions"]]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([], audit["orphan_source_ids"])

    def test_course_inventory_is_bounded_and_owned(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(34, audit["course_item_count"])
        self.assertEqual([], audit["unknown_owner_ids"])
        self.assertEqual([], audit["items_without_source_evidence"])
        self.assertEqual([], audit["items_without_recycle_owners"])

    def test_tense_and_variety_boundaries_are_explicit(self) -> None:
        self.assertEqual("productive_limited", self.items["grammar.past_simple_limited"]["control_status"])
        self.assertIn("Past questions", self.items["grammar.past_simple_limited"]["not_yet"])
        self.assertEqual("productive_limited", self.items["grammar.present_continuous_now"]["control_status"])
        self.assertIn("have is the course default", self.data["policy"]["variety_policy"])

    def test_broad_legacy_targets_all_resolve_to_exact_items(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(32, audit["legacy_target_count"])
        self.assertEqual([], audit["unmapped_legacy_candidate_ids"])
        self.assertGreater(len(audit["new_system_item_ids"]), 0)
        self.assertEqual(0, audit["final_lesson_decisions_made"])


if __name__ == "__main__":
    unittest.main()
