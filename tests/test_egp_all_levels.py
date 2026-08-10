"""Integrity checks for the all-level English Grammar Profile snapshot."""

from __future__ import annotations

import json
import hashlib
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ALL_LEVELS = ROOT / "data/derived/egp-all-levels.json"
A1_ONLY = ROOT / "data/derived/egp-a1.json"
EXPECTED = {"A1": 109, "A2": 291, "B1": 338, "B2": 243, "C1": 129, "C2": 112}


class EgpAllLevelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.all_data = json.loads(ALL_LEVELS.read_text(encoding="utf-8"))
        cls.a1_data = json.loads(A1_ONLY.read_text(encoding="utf-8"))

    def test_counts_and_unique_ids(self) -> None:
        records = self.all_data["records"]
        self.assertEqual(1222, self.all_data["count"])
        self.assertEqual(EXPECTED, dict(Counter(item["Level"] for item in records)))
        self.assertEqual(EXPECTED, self.all_data["level_counts"])
        self.assertEqual(len(records), len({item["id"] for item in records}))

    def test_existing_a1_snapshot_is_preserved(self) -> None:
        all_a1 = [item for item in self.all_data["records"] if item["Level"] == "A1"]
        self.assertEqual(
            {item["id"]: item for item in self.a1_data["records"]},
            {item["id"]: item for item in all_a1},
        )

    def test_source_locator_is_explicit(self) -> None:
        source = self.all_data["source"]
        self.assertEqual("Data", source["sheet"])
        self.assertEqual("A1:H1223", source["range"])
        raw_file = ROOT / source["raw_file"]
        self.assertTrue(raw_file.is_file())
        self.assertEqual(
            source["source_file_sha256"].lower(), hashlib.sha256(raw_file.read_bytes()).hexdigest()
        )
        for expected_row, record in enumerate(self.all_data["records"], 2):
            self.assertEqual(expected_row, record["_source"]["spreadsheet_row"])
            self.assertTrue(record["_source"]["raw_level_text"].strip())


if __name__ == "__main__":
    unittest.main()
