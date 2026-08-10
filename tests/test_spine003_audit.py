"""Completion tests for SPINE-003."""

import json
import unittest

from scripts.create_spine003_audit import OUTPUT, build
from scripts.validate_spine003_audit import validate


class Spine003AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_audit_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_no_integrity_gap_remains(self) -> None:
        for findings in self.data["integrity"].values():
            self.assertEqual([], findings)

    def test_each_level_has_receptive_productive_and_language_evidence(self) -> None:
        for row in self.data["levels"]:
            self.assertGreater(row["gse_receptive_records"], 0)
            self.assertGreater(row["gse_productive_records"], 0)
            self.assertGreater(row["egp_grammar_features"], 0)
            self.assertGreaterEqual(row["cefr_strands"], 15)

    def test_known_source_limits_are_named_not_hidden(self) -> None:
        c2 = self.data["levels"][-1]
        self.assertEqual(0, c2["lexical_pool_records"])
        self.assertEqual(0, c2["gse_grammar_features"])
        limits = " ".join(self.data["named_limits"]).casefold()
        self.assertIn("c2 lexical", limits)
        self.assertIn("pronunciation", limits)


if __name__ == "__main__":
    unittest.main()
