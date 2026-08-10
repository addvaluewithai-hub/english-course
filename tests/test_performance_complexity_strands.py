"""Contract tests for A1-C2 performance complexity."""

import json
import unittest

from scripts.create_performance_complexity_strands import build
from scripts.performance_complexity_contract import OUTPUT
from scripts.validate_performance_complexity_strands import validate


class PerformanceComplexityStrandTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_dataset_is_valid_and_deterministic(self) -> None:
        self.assertEqual([], validate())
        self.assertEqual(self.data, build())

    def test_every_dimension_has_six_distinct_boundaries(self) -> None:
        self.assertEqual(15, len(self.data["strands"]))
        for strand in self.data["strands"]:
            self.assertEqual(6, len(strand["stages"]))
            self.assertEqual(6, len({stage["expectation"] for stage in strand["stages"]}))

    def test_every_stage_has_cefr_evidence(self) -> None:
        for strand in self.data["strands"]:
            for stage in strand["stages"]:
                self.assertGreater(stage["evidence_count"], 0)

    def test_c2_pronunciation_keeps_accent_compatible(self) -> None:
        pronunciation = next(row for row in self.data["strands"] if row["strand_code"] == "pronunciation")
        self.assertIn("retained accent", pronunciation["stages"][-1]["expectation"].casefold())


if __name__ == "__main__":
    unittest.main()
