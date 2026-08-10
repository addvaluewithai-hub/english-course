"""CLI validation gate for migrated gold lesson U1-L03."""

from scripts.gold_v1_validation_core import validate


def main() -> int:
    errors = validate()
    if errors:
        print("FAIL migrated gold lesson U1-L03")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("PASS migrated gold lesson U1-L03 (GOLD-003)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
