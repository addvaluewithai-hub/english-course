"""Contract tests for the first-unit blueprint."""

from __future__ import annotations

import unittest

from scripts.validate_unit1 import MANIFEST, MASTERY, load, validation_errors


class Unit1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load(MANIFEST)
        cls.mastery = load(MASTERY)

    def test_blueprint_validates(self) -> None:
        self.assertEqual([], validation_errors())

    def test_gold_lesson_is_first_reference(self) -> None:
        first = self.manifest["lessons"][0]
        self.assertEqual("U1-L01", first["lesson_id"])
        self.assertEqual("gold_reference_ready", first["status"])

    def test_unit_has_eight_unique_lessons(self) -> None:
        lessons = self.manifest["lessons"]
        self.assertEqual(8, len(lessons))
        self.assertEqual(8, len({item["candidate_id"] for item in lessons}))

    def test_mastery_requires_all_fresh_stations(self) -> None:
        passing = self.mastery["passing_rule"]
        self.assertTrue(passing["require_all_stations"])
        self.assertFalse(passing["completion_is_mastery"])


if __name__ == "__main__":
    unittest.main()
