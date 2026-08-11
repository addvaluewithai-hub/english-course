import json
import unittest

from scripts.pilot10_qa_report import QA_JSON, QA_MD, build_qa, render


class Pilot10QATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.actual = json.loads(QA_JSON.read_text(encoding="utf-8"))

    def test_qa_artifacts_are_deterministic(self):
        expected = build_qa()
        self.assertEqual(expected, self.actual)
        self.assertEqual(render(expected), QA_MD.read_text(encoding="utf-8"))

    def test_all_ten_packages_and_sixty_five_roles_pass(self):
        checks = self.actual["global_checks"]
        self.assertEqual(10, checks["package_count"])
        self.assertEqual(120, checks["package_file_count"])
        self.assertEqual(65, checks["exact_introduction_and_recycle_roles"])
        self.assertTrue(checks["all_package_contracts_pass"])

    def test_release_boundary_is_honest(self):
        decision = self.actual["decision"]
        self.assertEqual("not_yet_generated_or_listened_to", decision["rendered_media"])
        self.assertEqual("not_approved", decision["learner_release"])
        self.assertEqual("U1-L08", self.actual["findings"]["highest_load_lesson"])


if __name__ == "__main__":
    unittest.main()
