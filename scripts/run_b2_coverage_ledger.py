#!/usr/bin/env python3
"""Run the B2 Stage-06 ledger with Stage-07 modality-aware introduction routing.

Stage 06 initially balanced source rows inside reviewed semantic-home windows. Stage 07
brief inspection exposed one important scheduling weakness: SUPPORTING cross-cutting
ability rows can span several capability families, so a purely semantic round-robin can
first introduce a production-coded source row inside a reception lesson (or vice versa).

This wrapper does NOT change Stage-1 semantic homes and does NOT infer final Stage-8
control roles. It only narrows first-introduction windows for SUPPORTING cross-cutting
ability records to units compatible with their canonical source mode/skill. Direct
C01-C18 capability ownership remains authoritative, including families that deliberately
contain source-mode subcomponents. Existing Stage-06 lifecycle, coverage, zero-new, and
load checks remain in force.
"""
from __future__ import annotations

from collections import defaultdict

import build_b2_coverage_ledger as ledger


def unit_of(lesson_id: str) -> str:
    return lesson_id.split("-", 1)[0]


def compatible_intro_units(item: dict) -> set[str]:
    modes = {str(x).lower() for x in item.get("mode_codes", [])}
    skills = {str(x).lower() for x in item.get("skill_codes", [])}
    units: set[str] = set()

    reception = any("reception" in x for x in modes)
    production = any("production" in x for x in modes)
    interaction = any("interaction" in x for x in modes)
    mediation = any("mediation" in x for x in modes)

    reading = any("read" in x for x in skills)
    listening = any("listen" in x for x in skills)
    speaking = any("speak" in x or "oral" in x for x in skills)
    writing = any("writ" in x for x in skills)

    if reception:
        if reading:
            units.update({"U1", "U2"})
        if listening:
            units.add("U3")
        if not reading and not listening:
            units.update({"U1", "U2", "U3"})

    if production:
        if speaking:
            units.update({"U4", "U5"})
        if writing:
            units.update({"U10", "U11", "U12"})
        if not speaking and not writing:
            units.update({"U4", "U5", "U10", "U11", "U12"})

    if interaction:
        if writing:
            units.add("U12")
        if speaking or not writing:
            units.update({"U6", "U7", "U8"})

    if mediation:
        units.add("U9")

    return units


_original_balanced = ledger.balanced
_original_build_record = ledger.build_record


def balanced_with_modality(records, key_fn, windows_fn, salt):
    if salt != "ability":
        return _original_balanced(records, key_fn, windows_fn, salt)

    groups = defaultdict(list)
    for record in records:
        key = key_fn(record)
        # Only SUPPORTING cross-cutting homes need this guard. Direct C01-C18
        # capability homes retain the Stage-1 reviewed family even when that family
        # intentionally contains different source-mode subcomponents.
        allowed = compatible_intro_units(record) if "X-" in key else set()
        groups[(key, tuple(sorted(allowed)))].append(record)

    assigned = {}
    for (key, allowed_tuple), values in groups.items():
        windows = windows_fn(key)
        if not windows:
            raise ValueError(f"no B2 ability introduction window for {key}")
        if allowed_tuple:
            allowed = set(allowed_tuple)
            filtered = [lid for lid in windows if unit_of(lid) in allowed]
        else:
            filtered = list(windows)
        if not filtered:
            raise ValueError(
                f"cross-cutting ability introduction has no mode-compatible lesson: "
                f"home={key} allowed_units={list(allowed_tuple)} candidate_windows={windows}"
            )
        offset = ledger.stable_offset(
            f"{salt}:{key}:mode:{','.join(allowed_tuple) if allowed_tuple else 'unfiltered'}",
            len(filtered),
        )
        for i, record in enumerate(values):
            assigned[record["item_id"]] = filtered[(i + offset) % len(filtered)]
    return assigned


def build_record_with_routing(category, item, label, homes, intro, plan, order, extra=None):
    record = _original_build_record(category, item, label, homes, intro, plan, order, extra)
    if category == "ability" and any(str(h).startswith("X-") for h in homes):
        allowed = compatible_intro_units(item)
        if allowed:
            if unit_of(intro) not in allowed:
                raise ValueError(
                    f"Stage-07 modality routing failed for {item['item_id']}: "
                    f"intro={intro} allowed={sorted(allowed)}"
                )
            record["stage_07_intro_routing"] = {
                "reason": "cross_cutting_ability_source_modality_guard",
                "source_mode_codes": item.get("mode_codes", []),
                "source_skill_codes": item.get("skill_codes", []),
                "allowed_intro_units": sorted(allowed),
            }
    return record


ledger.balanced = balanced_with_modality
ledger.build_record = build_record_with_routing


if __name__ == "__main__":
    ledger.main()
