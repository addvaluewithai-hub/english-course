"""Contract tests for all-level communicative comparison tags."""

import json
import unittest

from scripts.communicative_tag_contract import OUTPUT
from scripts.create_communicative_tag_assignments import build
from scripts.validate_communicative_tag_assignments import validate


class CommunicativeTagAssignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_complete_assignment_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())
        self.assertEqual(2274, len(self.data["records"]))

    def test_every_record_has_auditable_nonempty_tags(self) -> None:
        for row in self.data["records"]:
            self.assertTrue(row["skill_codes"])
            self.assertTrue(row["mode_codes"])
            self.assertTrue(row["function_codes"])
            self.assertTrue(row["rule_ids"])

    def test_plurilingual_mode_is_not_orphaned(self) -> None:
        rows = [row for row in self.data["records"] if "plurilingual_pluricultural" in row["mode_codes"]]
        self.assertEqual(52, len(rows))
        self.assertTrue(all(row["source_dataset_id"] == "cefr_all_descriptors" for row in rows))

    def test_advanced_levels_have_advanced_function_evidence(self) -> None:
        advanced = {
            "justify_or_argue", "evaluate", "synthesize", "summarize", "compare",
            "speculate_or_hypothesize", "analyze_or_criticize", "negotiate_or_resolve",
        }
        for level in ("b2", "c1", "c2"):
            functions = {
                function for row in self.data["records"] if level in row["source_level_codes"]
                for function in row["function_codes"]
            }
            self.assertTrue(advanced & functions, level)

    def test_source_dispositions_remain_separate(self) -> None:
        dispositions = {row["source_disposition"] for row in self.data["records"]}
        self.assertEqual(
            {"include_for_spine", "supporting_evidence", "duplicate_or_overlap"}, dispositions
        )


if __name__ == "__main__":
    unittest.main()
