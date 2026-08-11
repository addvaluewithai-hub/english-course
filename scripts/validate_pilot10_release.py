from __future__ import annotations

import json
from pathlib import Path

from scripts.pilot10_release_contract import ROOT, build_release_contract


RELEASE_PATH = ROOT / "data/reviewed/a1-first-10-lessons-pilot-v1.json"


def main() -> None:
    actual = json.loads(RELEASE_PATH.read_text(encoding="utf-8"))
    expected = build_release_contract()
    if actual != expected:
        raise SystemExit(
            "FAIL first-ten release is stale; run python -m scripts.create_pilot10_release"
        )
    audit = actual["audit"]
    assert audit["lesson_count"] == 10
    assert audit["unit1_lesson_count"] == 9
    assert audit["unit2_lesson_count"] == 1
    assert audit["global_positions"] == list(range(1, 11))
    assert audit["duplicate_owner_count"] == 0
    assert actual["lessons"][2]["lesson_id"] == "U1-L03"
    print("PASS locked first-ten A1 pilot release")


if __name__ == "__main__":
    main()
