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

    def load_path(self, path):
        return json.loads((ROOT / path).read_text(encoding="utf-8"))

    def test_all_level_contract_files_exist(self):
        for level in LEVELS:
            for name in FILES:
                self.assertTrue(
                    (ROOT / "curriculum" / "levels" / level / name).exists(),
                    f"{level}/{name}",
                )

    def test_reviewed_levels_are_authorized_only_after_explicit_lock(self):
        a1_manifest = self.load("a1", "manifest.json")
        a1_contract = self.load("a1", "exit_contract.json")
        a1_report = self.load_path(
            "curriculum/levels/a1/semantic-lock/semantic-lock-report.json"
        )
        self.assertTrue(a1_manifest["lesson_design_authorized"])
        self.assertFalse(a1_manifest["delivery_content_production_authorized"])
        self.assertEqual(a1_report["status"], "semantic_lock_reviewed_locked_v1")
        self.assertTrue(a1_report["lesson_design_authorized"])
        self.assertEqual(a1_report["summary"]["human_review_queue"], 0)
        self.assertEqual(a1_contract["status"], "semantic_inventory_locked_v1")
        self.assertTrue(a1_contract["semantic_lock"]["lesson_design_authorized"])

        a2_auth_path = ROOT / "curriculum/levels/a2/design-review/10-authorization-gate/authorization.json"
        a2_manifest = self.load("a2", "manifest.json")
        a2_contract = self.load("a2", "exit_contract.json")
        if a2_auth_path.exists():
            a2_auth = json.loads(a2_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(
                a2_auth["status"],
                "human_lesson_design_authorization_reviewed_locked_v1",
            )
            self.assertTrue(a2_auth["lesson_design_authorized"])
            self.assertFalse(a2_auth["delivery_content_production_authorized"])
            self.assertEqual(a2_auth["human_review_queue"], 0)
            self.assertTrue(a2_manifest["lesson_design_authorized"])
            self.assertFalse(a2_manifest["delivery_content_production_authorized"])
            self.assertEqual(
                a2_manifest["status"],
                "semantic_design_lock_reviewed_lesson_design_authorized",
            )
            self.assertEqual(a2_contract["status"], "semantic_inventory_locked_v1")
            self.assertTrue(a2_contract["semantic_lock"]["lesson_design_authorized"])
            self.assertFalse(a2_contract["delivery_content_production_authorized"])
        else:
            self.assertFalse(a2_manifest["lesson_design_authorized"])

        b1_auth_path = ROOT / "curriculum/levels/b1/design-review/09-authorization-gate/authorization.json"
        b1_manifest = self.load("b1", "manifest.json")
        b1_contract = self.load("b1", "exit_contract.json")
        if b1_auth_path.exists():
            b1_auth = json.loads(b1_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(
                b1_auth["status"],
                "human_lesson_design_authorization_reviewed_locked_v1",
            )
            self.assertTrue(b1_auth["lesson_design_authorized"])
            self.assertFalse(b1_auth["delivery_content_production_authorized"])
            self.assertEqual(b1_auth["human_review_queue"], 0)
            self.assertEqual(b1_auth["architecture"], {"units": 12, "lesson_slots": 85})
            self.assertTrue(b1_manifest["lesson_design_authorized"])
            self.assertFalse(b1_manifest["delivery_content_production_authorized"])
            self.assertEqual(
                b1_manifest["status"],
                "semantic_design_lock_reviewed_lesson_design_authorized",
            )
            self.assertEqual(b1_manifest["semantic_lock"]["human_review_queue"], 0)
            self.assertEqual(b1_contract["status"], "semantic_inventory_locked_v1")
            self.assertTrue(b1_contract["semantic_lock"]["lesson_design_authorized"])
            self.assertEqual(b1_contract["semantic_lock"]["human_review_queue"], 0)
            self.assertFalse(b1_contract["delivery_content_production_authorized"])
        else:
            self.assertFalse(b1_manifest["lesson_design_authorized"])

        b2_auth_path = ROOT / "curriculum/levels/b2/design-review/09-authorization-gate/authorization.json"
        b2_manifest = self.load("b2", "manifest.json")
        b2_contract = self.load("b2", "exit_contract.json")
        if b2_auth_path.exists():
            b2_auth = json.loads(b2_auth_path.read_text(encoding="utf-8"))
            self.assertEqual(
                b2_auth["status"],
                "human_lesson_design_authorization_reviewed_locked_v1",
            )
            self.assertTrue(b2_auth["lesson_design_authorized"])
            self.assertFalse(b2_auth["delivery_content_production_authorized"])
            self.assertEqual(b2_auth["human_review_queue"], 0)
            self.assertEqual(b2_auth["architecture"]["units"], 13)
            self.assertEqual(b2_auth["architecture"]["lesson_slots"], 95)
            self.assertEqual(b2_auth["architecture"]["zero_new_transfer_exit_slots"], 18)
            self.assertTrue(b2_manifest["lesson_design_authorized"])
            self.assertFalse(b2_manifest["delivery_content_production_authorized"])
            self.assertEqual(
                b2_manifest["status"],
                "semantic_design_lock_reviewed_lesson_design_authorized",
            )
            self.assertEqual(b2_manifest["semantic_lock"]["human_review_queue"], 0)
            self.assertEqual(b2_contract["status"], "semantic_inventory_locked_v1")
            self.assertTrue(b2_contract["semantic_lock"]["lesson_design_authorized"])
            self.assertEqual(b2_contract["semantic_lock"]["human_review_queue"], 0)
            self.assertFalse(b2_contract["delivery_content_production_authorized"])
        else:
            self.assertFalse(b2_manifest["lesson_design_authorized"])

        for level in LEVELS[4:]:
            other = self.load(level, "manifest.json")
            self.assertFalse(other["lesson_design_authorized"])
            self.assertEqual(other["level"], level.upper())

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
