"""Completeness and compatibility tests for all-level GSE extraction."""

from __future__ import annotations

import json
import unittest
from collections import Counter
from pathlib import Path

from scripts.gse_a1_parser import extract_objectives as extract_a1
from scripts.gse_all_parser import EXPECTED_SOURCE_CODES, extract_objectives
from scripts.gse_all_records import build_collection
from scripts.gse_level_bands import BANDS, SKILLS
from scripts.validate_source_records import validate_dataset


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/frameworks/gse-learning-objectives-adult-general-english-2022.pdf"
DATASET = ROOT / "data/derived/gse-all-objectives.json"
EXPECTED_COUNTS = {
    "below_a1": (7, 15, 32, 5),
    "a1": (14, 34, 54, 19),
    "a2": (16, 20, 78, 18),
    "a2_plus": (19, 21, 65, 32),
    "b1": (17, 20, 53, 31),
    "b1_plus": (16, 24, 53, 37),
    "b2": (17, 25, 71, 42),
    "b2_plus": (23, 20, 48, 26),
    "c1": (7, 12, 24, 16),
    "c2": (6, 2, 6, 5),
}


class GseAllExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PDF.exists():
            raise unittest.SkipTest("GSE source PDF is unavailable")
        cls.rows = extract_objectives(PDF)

    def test_every_band_and_skill_is_present(self) -> None:
        combinations = {(row.band.key, row.skill) for row in self.rows}
        self.assertEqual(
            {(band.key, skill) for band in BANDS for skill in SKILLS}, combinations
        )

    def test_source_table_counts_are_locked(self) -> None:
        counts = Counter((row.band.key, row.skill) for row in self.rows)
        actual = {
            band: tuple(counts[(band, skill)] for skill in SKILLS)
            for band in EXPECTED_COUNTS
        }
        self.assertEqual(EXPECTED_COUNTS, actual)
        self.assertEqual(1050, len(self.rows))

    def test_scores_text_and_codes_are_valid(self) -> None:
        for row in self.rows:
            self.assertLessEqual(row.band.minimum, row.score)
            self.assertGreaterEqual(row.band.maximum, row.score)
            self.assertTrue(row.text.startswith("Can "))
            self.assertTrue(row.text.endswith(f"({row.source_code})"))
            self.assertIn(row.source_code, EXPECTED_SOURCE_CODES)
            self.assertNotRegex(row.text, r"’\s+[,.!?;:]")

    def test_a1_partition_matches_existing_parser(self) -> None:
        all_a1 = [row for row in self.rows if row.band.key == "a1"]
        expected = extract_a1(PDF)
        actual_keys = Counter((row.skill, str(row.score), row.page, row.text) for row in all_a1)
        expected_keys = Counter((row.skill, row.score, row.page, row.text) for row in expected)
        self.assertEqual(expected_keys, actual_keys)

    def test_records_are_unique_and_duplicates_are_explicit(self) -> None:
        records = build_collection(self.rows)["records"]
        self.assertEqual(len(records), len({row["record_id"] for row in records}))
        exact = Counter((row.skill, row.text) for row in self.rows)
        repeated_rows = sum(count for count in exact.values() if count > 1)
        warned = sum(bool(row["review"]["issues"]) for row in records)
        self.assertEqual(repeated_rows, warned)

    def test_checked_in_dataset_matches_parser_and_schema(self) -> None:
        data = json.loads(DATASET.read_text(encoding="utf-8"))
        self.assertEqual(len(self.rows), len(data["records"]))
        self.assertEqual([], validate_dataset(DATASET))


if __name__ == "__main__":
    unittest.main()
