"""Contract tests for the complete all-level source disposition audit."""

from __future__ import annotations

import json
import unittest

from scripts.create_source_dispositions import build
from scripts.source_disposition_contract import OUTPUT
from scripts.validate_source_dispositions import validate


class SourceDispositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_complete_reviewed_collection_is_valid(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(9274, self.data["audit"]["total_records"])
        self.assertEqual([], self.data["audit"]["unexplained_orphans"])
        self.assertEqual([], self.data["audit"]["unclassified_records"])

    def test_generation_is_deterministic(self) -> None:
        self.assertEqual(self.data, build())

    def test_receptive_gse_objectives_remain_targets(self) -> None:
        rows = [
            row for row in self.data["records"]
            if row["source_dataset_id"] == "gse_all_objectives"
            and row["control_expectation"] == "receptive"
        ]
        self.assertTrue(rows)
        self.assertTrue(
            all(
                row["disposition"] in {"include_for_spine", "duplicate_or_overlap"}
                for row in rows
            )
        )

    def test_lexical_lists_are_reference_pools(self) -> None:
        rows = [
            row for row in self.data["records"]
            if row["source_dataset_id"].startswith("oxford_")
        ]
        self.assertEqual(5322, len(rows))
        self.assertTrue(all(row["disposition"] == "reference_pool" for row in rows))
        self.assertTrue(all(row["control_expectation"] == "not_applicable" for row in rows))

    def test_exact_overlap_is_explicit_without_cross_level_equivalence(self) -> None:
        overlaps = [row for row in self.data["records"] if row["overlap"]]
        self.assertTrue(overlaps)
        self.assertTrue(all(row["disposition"] == "duplicate_or_overlap" for row in overlaps))
        self.assertEqual([], self.data["audit"]["cross_level_exact_text_conflicts"])


if __name__ == "__main__":
    unittest.main()
