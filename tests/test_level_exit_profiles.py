"""Contract tests for the proposed A1-C2 level exit profiles."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validate_level_exit_profiles import DEFAULT_DATA, validate


ROOT = Path(__file__).resolve().parents[1]


class LevelExitProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(DEFAULT_DATA.read_text(encoding="utf-8"))

    def test_profile_contract_and_semantics(self) -> None:
        self.assertEqual([], validate())

    def test_profiles_are_explicitly_pending_review(self) -> None:
        self.assertEqual("proposal", self.data["status"])
        self.assertEqual("needs_review", self.data["review"]["status"])
        self.assertTrue(
            all(item["decision_state"] == "needs_review" for item in self.data["levels"])
        )

    def test_pre_a1_and_plus_bands_do_not_become_exit_claims(self) -> None:
        self.assertFalse(self.data["onboarding_support"]["exit_claim"])
        exit_levels = set(self.data["exit_levels"])
        self.assertNotIn("pre_a1", exit_levels)
        for milestone in self.data["internal_milestones"]:
            self.assertNotIn(milestone["id"], exit_levels)

    def test_lifecycle_order_is_locked(self) -> None:
        self.assertEqual(
            ["expose", "introduce", "practise", "recycle", "consolidate", "extend"],
            self.data["lifecycle"],
        )


if __name__ == "__main__":
    unittest.main()
