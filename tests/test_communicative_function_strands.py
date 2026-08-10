"""Contract tests for communicative-function lifecycle strands."""

import json
import unittest

from scripts.communicative_strand_contract import EXIT_LEVELS, OUTPUT
from scripts.create_communicative_function_strands import build
from scripts.validate_communicative_function_strands import validate


class CommunicativeFunctionStrandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))
        cls.by_code = {row["function_code"]: row for row in cls.data["strands"]}

    def test_strands_are_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())
        self.assertEqual(41, len(self.data["strands"]))

    def test_every_strand_has_control_and_consolidation(self) -> None:
        for strand in self.data["strands"]:
            life = strand["lifecycle"]
            self.assertTrue(
                life["first_receptive_control_level"] or life["first_productive_control_level"]
            )
            self.assertIn(life["consolidation_level"], EXIT_LEVELS)
            self.assertTrue(any(
                "consolidate" in stage["lifecycle_states"] for stage in life["stages"]
            ))

    def test_pre_a1_never_owns_consolidation(self) -> None:
        self.assertTrue(all(
            row["lifecycle"]["consolidation_level"] != "pre_a1"
            for row in self.data["strands"]
        ))

    def test_foundational_functions_persist_beyond_a1(self) -> None:
        for function in ("comprehend_information", "give_information", "exchange_information"):
            life = self.by_code[function]["lifecycle"]
            self.assertEqual("a1", life["consolidation_level"])
            self.assertEqual(["a2", "b1", "b2", "c1", "c2"], life["recycle_levels"])

    def test_advanced_functions_have_later_control_boundaries(self) -> None:
        for function in ("analyze_or_criticize", "interpret_attitude_or_implication"):
            self.assertIn(self.by_code[function]["lifecycle"]["consolidation_level"], {"b1", "b2", "c1"})


if __name__ == "__main__":
    unittest.main()
