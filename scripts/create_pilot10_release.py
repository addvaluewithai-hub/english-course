from __future__ import annotations

import argparse
import json
from pathlib import Path

from scripts.pilot10_release_contract import ROOT, build_release_contract


DEFAULT_OUTPUT = ROOT / "data/reviewed/a1-first-10-lessons-pilot-v1.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the locked first-ten release.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build_release_contract()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"WROTE {args.output} ({len(payload['lessons'])} lessons)")


if __name__ == "__main__":
    main()
