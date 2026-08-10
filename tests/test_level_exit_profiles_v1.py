"""Contract tests for approved, evidence-linked A1-C2 exit profiles."""

from __future__ import annotations

import json
import unittest

from scripts.create_level_exit_profiles import build
from scripts.level_exit_profile_contract import OUTPUT
from scripts.validate_level_exit_evidence import validate as validate_evidence
from scripts.validate_level_exit_profiles_v1 import validate


class LevelExitProfilesV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_evidence_and_profiles_validate(self) -> None:
        self.assertEqual([], validate_evidence())
        self.assertEqual([], validate())

    def test_generation_is_deterministic(self) -> None:
        self.assertEqual(self.data, build())

    def test_profiles_are_approved_and_strictly_ordered(self) -> None:
        self.assertEqual("approved", self.data["status"])
        self.assertEqual("accepted", self.data["review"]["status"])
        self.assertEqual(list(range(1, 7)), [row["progression_index"] for row in self.data["levels"]])

    def test_source_claims_have_evidence_and_policy_claims_have_decisions(self) -> None:
        for profile in self.data["levels"]:
            claims = [profile["exit_promise"], *profile["assessment_evidence"]]
            for section in ("reception", "production", "interaction", "language_control"):
                claims.extend(profile[section].values())
            for claim in claims:
                if claim["claim_type"] in {"source_boundary", "synthesis"}:
                    self.assertTrue(claim["evidence_bundle_ids"], claim["claim_id"])
                if claim["claim_type"] in {"product_policy", "synthesis"}:
                    self.assertTrue(claim["decision_refs"], claim["claim_id"])

    def test_c2_target_is_effectiveness_not_accent_imitation(self) -> None:
        c2 = self.data["levels"][-1]
        text = json.dumps(c2, ensure_ascii=False).casefold()
        self.assertNotIn("native speaker", text)
        self.assertIn("retained accent", text)


if __name__ == "__main__":
    unittest.main()
