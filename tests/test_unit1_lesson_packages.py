"""Progressive contract tests for authored Unit 1 lesson packages."""

from __future__ import annotations

import unittest

from scripts.validate_unit1_lessons import validation_errors


class Unit1LessonPackageTests(unittest.TestCase):
    def test_every_existing_package_is_valid(self) -> None:
        self.assertEqual([], validation_errors(require_complete=False))


if __name__ == "__main__":
    unittest.main()
