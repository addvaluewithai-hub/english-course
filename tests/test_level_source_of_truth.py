import json
import unittest
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

    def test_c2_lexical_gap_is_not_hidden(self):
        words = self.load("c2", "words.json")
        phrases = self.load("c2", "phrases.json")
        self.assertTrue(words["status"].startswith("blocked_"))
        self.assertTrue(phrases["status"].startswith("blocked_"))


if __name__ == "__main__":
    unittest.main()
