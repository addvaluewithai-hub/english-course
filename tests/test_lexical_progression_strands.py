"""Contract tests for the A1-C2 lexical progression."""

import json
import unittest

from scripts.create_lexical_progression_strands import build
from scripts.lexical_progression_contract import OUTPUT
from scripts.validate_lexical_progression_strands import validate


class LexicalProgressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_dataset_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_every_oxford_line_is_accounted_for_as_reference_evidence(self) -> None:
        pool = self.data["reference_pool"]
        self.assertEqual(5322, pool["total_entry_lines"])
        self.assertTrue(pool["all_records_accounted_for"])
        self.assertEqual(["c2"], pool["levels_without_published_pool"])

    def test_resource_families_have_valid_six_level_lifecycles(self) -> None:
        self.assertEqual(10, len(self.data["resource_strands"]))
        for strand in self.data["resource_strands"]:
            self.assertEqual(6, len(strand["stages"]))
            self.assertIn(
                "consolidate",
                next(
                    stage["lifecycle_states"] for stage in strand["stages"]
                    if stage["level"] == strand["first_family_consolidation_level"]
                ),
            )

    def test_c2_requires_registered_usage_evidence_without_word_count(self) -> None:
        method = self.data["c2_selection_method"]
        self.assertEqual("accepted_method_before_item_selection", method["status"])
        self.assertTrue(any("No invented C2 word-count" in rule for rule in method["prohibitions"]))
        self.assertTrue(any("licence" in rule for rule in method["prohibitions"]))


if __name__ == "__main__":
    unittest.main()
