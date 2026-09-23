import json
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a1", "a2", "b1", "b2", "c1", "c2")
FILES = (
    "manifest.json",
    "words.json",
    "phrases.json",
    "grammar.json",
    "abilities.json",
    "pronunciation.json",
    "exit_contract.json",
    "sources.json",
)
OXFORD_PHRASE_COUNTS = {"a1": 199, "a2": 176, "b1": 175, "b2": 125, "c1": 75}


class LevelSourceOfTruthTests(unittest.TestCase):
    def load(self, level, name):
        return json.loads(
            (ROOT / "curriculum" / "levels" / level / name).read_text(encoding="utf-8")
        )

    def test_all_level_contract_files_exist(self):
        for level in LEVELS:
            for name in FILES:
                self.assertTrue(
                    (ROOT / "curriculum" / "levels" / level / name).exists(),
                    f"{level}/{name}",
                )

    def test_manifests_keep_lesson_design_locked(self):
        for level in LEVELS:
            manifest = self.load(level, "manifest.json")
            self.assertFalse(manifest["lesson_design_authorized"])
            self.assertEqual(manifest["level"], level.upper())

    def test_inventory_semantics_are_explicit(self):
        for level in LEVELS:
            contract = self.load(level, "exit_contract.json")
            self.assertEqual(contract["inventory_semantics"]["level_files"], "new_at_level")
            self.assertEqual(
                contract["inventory_semantics"]["exit_obligation"],
                "cumulative_through_level",
            )

    def test_source_refs_are_assigned(self):
        for level in LEVELS:
            sources = self.load(level, "sources.json")
            self.assertTrue(sources["sources"], level)

    def test_current_oxford_phrase_list_is_fully_partitioned(self):
        total = 0
        for level, expected in OXFORD_PHRASE_COUNTS.items():
            phrases = self.load(level, "phrases.json")
            self.assertEqual(len(phrases["items"]), expected, level)
            self.assertFalse(phrases["status"].startswith("blocked_"), level)
            total += len(phrases["items"])
        self.assertEqual(total, 750)

    def test_c2_pearson_lexical_partition_is_complete(self):
        words = self.load("c2", "words.json")
        phrases = self.load("c2", "phrases.json")
        manifest = self.load("c2", "manifest.json")
        self.assertEqual(len(words["items"]), 609)
        self.assertEqual(len(phrases["items"]), 41)
        self.assertEqual(manifest["counts"]["words"], 609)
        self.assertEqual(manifest["counts"]["phrases"], 41)
        self.assertEqual(manifest["blocking_categories"], [])
        self.assertIn("commercial_permission_required", manifest["production_gates"])
        self.assertFalse(words["status"].startswith("blocked_"))
        self.assertFalse(phrases["status"].startswith("blocked_"))

    def test_c2_phrase_partition_preserves_source_semantics(self):
        phrases = self.load("c2", "phrases.json")["items"]
        subtype_counts = Counter(item["subtype"] for item in phrases)
        self.assertEqual(subtype_counts["source_phrase"], 9)
        self.assertEqual(subtype_counts["source_phrasal_verb"], 5)
        self.assertEqual(subtype_counts["collocation"], 27)
        for item in phrases:
            self.assertEqual(item["license_gate"], "commercial_permission_required")
            if item["subtype"] == "collocation":
                self.assertFalse(item["independent_gse_score"])
                self.assertEqual(item["level_inheritance"], "owner_record")
            else:
                self.assertTrue(item["independent_gse_score"])

    def test_c2_words_exclude_source_phrase_categories(self):
        words = self.load("c2", "words.json")["items"]
        for item in words:
            categories = set(item["grammatical_categories"])
            self.assertFalse({"phrase", "phrasal verb"}.intersection(categories))
            self.assertEqual(item["license_gate"], "commercial_permission_required")


if __name__ == "__main__":
    unittest.main()
