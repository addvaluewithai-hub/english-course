import unittest

from scripts.pilot10_common_validation import validate_package
from scripts.pilot10_package_contract import EXPECTED_FILES, lesson_contract, release
from scripts.pilot10_specs.registry import SPECS


class Pilot10PackageContractTests(unittest.TestCase):
    def test_contract_has_twelve_modular_files(self):
        self.assertEqual(12, len(EXPECTED_FILES))

    def test_gold_passes_the_common_batch_contract(self):
        self.assertEqual([], validate_package("U1-L03"))

    def test_gold_contract_owns_its_exact_roles(self):
        contract = lesson_contract("U1-L03")
        self.assertEqual(7, len(contract["exact_item_roles"]["introduce"]))
        self.assertEqual(3, len(contract["exact_item_roles"]["fresh_recycle"]))

    def test_all_ten_packages_pass_common_validation(self):
        for lesson in release()["lessons"]:
            with self.subTest(lesson_id=lesson["lesson_id"]):
                self.assertEqual([], validate_package(lesson["lesson_id"]))

    def test_every_new_package_is_deterministically_authored(self):
        expected_new = {row["lesson_id"] for row in release()["lessons"]} - {"U1-L03"}
        self.assertEqual(expected_new, set(SPECS))

    def test_pilot_code_modules_stay_modular(self):
        for path in (lesson_contract.__globals__["ROOT"] / "scripts").glob("pilot10*.py"):
            with self.subTest(path=path.name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 200)


if __name__ == "__main__":
    unittest.main()
