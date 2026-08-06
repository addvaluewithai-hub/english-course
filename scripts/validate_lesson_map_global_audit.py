"""Validate the saved global lesson-map audit against a deterministic rebuild."""

from __future__ import annotations

try:
    from scripts.create_lesson_map_global_audit import JSON_PATH, build_audit
    from scripts.lesson_map_io import load
except ModuleNotFoundError:
    from create_lesson_map_global_audit import JSON_PATH, build_audit
    from lesson_map_io import load


def main() -> int:
    expected = build_audit()
    actual = load(JSON_PATH)
    if actual != expected:
        print(f"FAIL {JSON_PATH}: saved audit differs from deterministic rebuild")
        return 1
    decision = actual["decision"]
    if not decision["lesson_002_may_pass"] or decision["status"] != "passed":
        print(f"FAIL {JSON_PATH}: final approval decision does not pass the phase gate")
        return 1
    print(f"PASS {JSON_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
