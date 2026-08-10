"""Contract tests for all-level grammar family progression."""

import json
import unittest

from scripts.create_grammar_family_strands import build
from scripts.grammar_strand_contract import OUTPUT
from scripts.validate_grammar_family_strands import validate


class GrammarFamilyStrandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_grammar_dataset_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_all_egp_and_gse_records_are_accounted_for(self) -> None:
        self.assertEqual(1222, sum(row["evidence"]["feature_count"] for row in self.data["families"]))
        self.assertEqual(456, len(self.data["gse_crosswalk"]))
        self.assertTrue(all(row["supercategory_codes"] for row in self.data["gse_crosswalk"]))

    def test_families_have_prior_exposure_and_later_recycling(self) -> None:
        for family in self.data["families"]:
            life = family["lifecycle"]
            self.assertNotEqual(life["first_exposure_level"], life["consolidation_level"])
            self.assertEqual(life["first_productive_control_level"], life["consolidation_level"])

    def test_known_crosscheck_limits_are_explicit(self) -> None:
        audit = self.data["audit"]
        self.assertEqual(["c2"], audit["gse_levels_without_records"])
        self.assertIn("DISCOURSE MARKERS", audit["supercategories_without_gse_crosscheck"])

    def test_family_scope_does_not_turn_every_feature_into_a_target(self) -> None:
        self.assertEqual(
            "family_range_evidence_not_one_feature_one_target", self.data["feature_use_policy"]
        )


if __name__ == "__main__":
    unittest.main()
