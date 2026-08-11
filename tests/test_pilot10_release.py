import json
import unittest
from pathlib import Path

from scripts.pilot10_release_contract import ROOT, build_release_contract


RELEASE_PATH = ROOT / "data/reviewed/a1-first-10-lessons-pilot-v1.json"


class Pilot10ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))

    def test_release_is_deterministic_and_current(self):
        self.assertEqual(self.actual, build_release_contract())

    def test_release_contains_actual_first_ten(self):
        lessons = self.actual["lessons"]
        self.assertEqual([x["global_sequence_position"] for x in lessons], list(range(1, 11)))
        self.assertEqual([x["lesson_id"] for x in lessons[:9]], [f"U1-L{i:02d}" for i in range(1, 10)])
        self.assertEqual(lessons[9]["lesson_id"], "U2-L01")

    def test_every_lesson_is_unique_and_source_linked(self):
        lessons = self.actual["lessons"]
        self.assertEqual(len({x["final_owner_id"] for x in lessons}), 10)
        for lesson in lessons:
            self.assertTrue(lesson["source_candidate_ids"])
            self.assertTrue(lesson["outcome_statement"])
            self.assertTrue(lesson["content_path"].startswith("units/a1-v1/"))

    def test_gold_is_real_third_lesson(self):
        gold = self.actual["lessons"][2]
        self.assertEqual(gold["lesson_id"], "U1-L03")
        self.assertIn("preserve_accepted_gold", gold["production_requirement"])


if __name__ == "__main__":
    unittest.main()
