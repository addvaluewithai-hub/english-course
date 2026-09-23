#!/usr/bin/env python3
"""Report the exact reviewed grammar-family lifecycle stage coverage."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/reviewed/grammar-family-strands-v1.json"
LEVELS = ("pre_a1", "a1", "a2", "b1", "b2", "c1", "c2")


def main() -> None:
    families = json.loads(DATA.read_text(encoding="utf-8"))["families"]
    pairs = []
    missing = Counter()
    length_counts = Counter()
    stage_level_counts = Counter()
    for family in families:
        stages = family["lifecycle"]["stages"]
        length_counts[len(stages)] += 1
        levels = [s["level"] for s in stages]
        stage_level_counts.update(levels)
        pairs.extend((family["family_id"], level) for level in levels)
        for level in LEVELS:
            if level not in levels:
                missing[level] += 1
    print("FAMILIES", len(families))
    print("STAGE_COUNT", len(pairs), "UNIQUE", len(set(pairs)))
    print("STAGES_PER_FAMILY", dict(sorted(length_counts.items())))
    print("STAGES_BY_LEVEL", dict(stage_level_counts))
    print("FAMILIES_MISSING_LEVEL", dict(missing))
    for family in families[:20]:
        print("FAMILY", family["family_id"], [s["level"] for s in family["lifecycle"]["stages"]])


if __name__ == "__main__":
    main()
