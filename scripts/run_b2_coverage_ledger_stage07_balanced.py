#!/usr/bin/env python3
"""Run the B2 ledger with Stage-7 semantic routing constrained by the Stage-6 ability cap.

The Stage-7 authoring pass exposed two valid but competing needs:
- first-introduction placement should prefer the most defensible Stage-5 sublesson; and
- a semantic preference must not create a new raw ability-load overload merely because
  several related source statements name the same subfunction.

This runner reuses the reviewed Stage-7 routing helpers from ``run_b2_coverage_ledger``
but treats an explicit sublesson as a strong preference rather than an unlimited hard
assignment. All candidates remain inside the already-reviewed Stage-6 introduction
window; SUPPORTING X-* rows also retain the modality guard. Final productive/receptive/
formulaic/support roles remain pending Stage 8.
"""
from __future__ import annotations

from collections import Counter

import run_b2_coverage_ledger as stage07

ledger = stage07.ledger
ABILITY_LIMIT = stage07.ABILITY_LIMIT
_original_balanced = stage07._original_balanced


def balanced_capacity_aware(records, key_fn, windows_fn, salt):
    if salt != "ability":
        return _original_balanced(records, key_fn, windows_fn, salt)

    plans = []
    for record in records:
        key = key_fn(record)
        windows = windows_fn(key)
        if not windows:
            raise ValueError(f"no B2 ability introduction window for {key}")

        allowed = stage07.compatible_intro_units(record) if "X-" in key else set()
        if allowed:
            windows = [lid for lid in windows if stage07.unit_of(lid) in allowed]
        if not windows:
            raise ValueError(
                "cross-cutting ability introduction has no mode-compatible lesson: "
                f"home={key} allowed_units={sorted(allowed)}"
            )

        explicit = stage07.explicit_lesson(key, record)
        scores = {lid: stage07.semantic_score(record, lid) for lid in windows}
        if explicit in scores:
            # Strong enough to win while capacity remains, but not strong enough to
            # manufacture a new >9 ability warning. Overflow can move only within the
            # same reviewed capability/modality window.
            scores[explicit] += 100

        ordered = sorted(scores.values(), reverse=True)
        best = ordered[0]
        second = ordered[1] if len(ordered) > 1 else best
        confidence = best - second
        plans.append((confidence, best, record["item_id"], record, windows, scores, explicit))

    # High-confidence semantic matches claim capacity first. Generic/tied records fill
    # remaining capacity deterministically.
    plans.sort(key=lambda x: (-x[0], -x[1], x[2]))
    loads: Counter = Counter()
    assigned = {}

    for _, _, _, record, windows, scores, explicit in plans:
        under_limit = [lid for lid in windows if loads[lid] < ABILITY_LIMIT]
        candidates = under_limit or list(windows)

        best_score = max(scores[lid] for lid in candidates)
        best = [lid for lid in candidates if scores[lid] == best_score]
        min_load = min(loads[lid] for lid in best)
        best = [lid for lid in best if loads[lid] == min_load]
        idx = ledger.stable_offset(f"ability-stage07-cap:{record['item_id']}", len(best))
        chosen = best[idx]
        assigned[record["item_id"]] = chosen
        loads[chosen] += 1

    over = {lid: n for lid, n in loads.items() if n > ABILITY_LIMIT}
    if over:
        raise ValueError(f"Stage-07 semantic ability routing exceeded soft capacity: {over}")
    return assigned


ledger.balanced = balanced_capacity_aware


if __name__ == "__main__":
    ledger.main()
