"""Completeness and source-integrity tests for CUR-003."""

from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path

import fitz

from scripts.cefr_a1_parser import extract_descriptors
from scripts.cefr_a1_specs import TABLE_SPECS


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "sources/raw/frameworks/cefr-companion-2020-en.pdf"
DERIVED = ROOT / "data/derived/cefr-a1-descriptors.json"
REVIEWED = ROOT / "data/reviewed/cefr-a1-descriptors.json"
EXPECTED_MODES = {
    "Reception": 24,
    "Production": 11,
    "Interaction": 30,
    "Online interaction": 3,
    "Mediation": 15,
    "Communicative language competences": 15,
}


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _compact(text: str) -> str:
    text = text.replace("\xad", "")
    text = re.sub(r"(?<=\w)([-/])\s+(?=\w)", r"\1", text)
    return re.sub(r"\s+", "", text)


class CefrA1ExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not PDF.exists():
            raise unittest.SkipTest(
                'CEFR source PDF is local-only; see sources/registry/SOURCES.md'
            )
        cls.descriptors, cls.inventory = extract_descriptors(PDF)
        cls.derived = _load(DERIVED)["records"]
        cls.reviewed = _load(REVIEWED)["records"]

    def test_inventory_and_counts_are_complete(self) -> None:
        self.assertEqual(len(TABLE_SPECS), 71)
        self.assertEqual(len(self.inventory), 82)
        self.assertEqual(sum(count == 0 for count in self.inventory.values()), 23)
        self.assertEqual(len(self.descriptors), 98)
        self.assertEqual(Counter(item.mode for item in self.descriptors), EXPECTED_MODES)

    def test_generated_collection_matches_parser(self) -> None:
        self.assertEqual(len(self.derived), 98)
        self.assertEqual(len({item["record_id"] for item in self.derived}), 98)
        parsed = [(item.page, item.scale, item.text) for item in self.descriptors]
        generated = [
            (
                item["source"]["location"]["page"],
                item["source_facts"]["scale_text"],
                item["source"]["source_text"],
            )
            for item in self.derived
        ]
        self.assertEqual(generated, parsed)

    def test_every_descriptor_occurs_on_its_cited_pdf_page(self) -> None:
        document = fitz.open(PDF)
        page_text = {}
        for item in self.descriptors:
            page_text.setdefault(item.page, _compact(document[item.page - 1].get_text("text")))
            self.assertIn(_compact(item.text), page_text[item.page])

    def test_source_facts_and_normalized_tags_are_consistent(self) -> None:
        for item in self.derived:
            self.assertEqual(item["record_kind"], "descriptor")
            self.assertEqual(item["source_facts"]["level_text"], "A1")
            self.assertEqual(item["interpretation"]["cefr_codes"], ["a1"])
            self.assertEqual(item["interpretation"]["inclusion_status"], "included")
            self.assertTrue(item["interpretation"]["skill_codes"])
            self.assertTrue(item["interpretation"]["mode_codes"])
            self.assertTrue(item["interpretation"]["function_codes"])
            self.assertTrue(item["interpretation"]["candidate_cluster_ids"])

    def test_reviewed_lifecycle_is_final(self) -> None:
        self.assertEqual(len(self.reviewed), 98)
        self.assertTrue(all(item["review"]["status"] == "accepted" for item in self.reviewed))
        self.assertTrue(all(item["review"]["reviewer"] == "cur_005_primary" for item in self.reviewed))
        derived_text = [item["source"]["source_text"] for item in self.derived]
        reviewed_text = [item["source"]["source_text"] for item in self.reviewed]
        self.assertEqual(reviewed_text, derived_text)

    def test_repeated_source_wording_retains_distinct_scale_evidence(self) -> None:
        repeated = "Can understand questions and instructions addressed carefully and slowly to them and follow short, simple directions."
        matches = [item for item in self.derived if item["source"]["source_text"] == repeated]
        self.assertEqual(len(matches), 3)
        self.assertEqual(len({item["source_facts"]["scale_text"] for item in matches}), 3)


if __name__ == "__main__":
    unittest.main()
