"""CLI gate for TEST-001 learner-test readiness."""

from scripts.learner_test_v1_validation_core import validate


def main() -> int:
    errors = validate()
    if errors:
        print("FAIL learner-test v1 readiness")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS learner-test v1 readiness (TEST-001)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
