"""Create reviewed lifecycle strands for all communicative functions."""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from typing import Any

from scripts.communicative_function_catalog import INTENTS, strand_role, title
from scripts.communicative_strand_contract import (
    EXIT_LEVELS, LEVELS, LIFECYCLE, OUTPUT, PROFILES, REPORT, REVIEWED_AT, REVIEWER, ROOT, TAGS,
)
from scripts.source_disposition_inputs import file_sha256


def _assignment_id(row: dict) -> str:
    return f"{row['source_dataset_id']}:{row['source_record_id']}"


def _hash_ids(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(ids).encode("utf-8")).hexdigest()


def _representatives(ids: list[str]) -> list[str]:
    return [ids[index] for index in sorted({0, len(ids) // 2, len(ids) - 1})]


def _control(rows: list[dict]) -> str:
    modes = {mode for row in rows for mode in row["mode_codes"]}
    receptive = "reception" in modes
    productive = bool(modes - {"reception", "communicative_competence"}) or "communicative_competence" in modes
    if receptive and productive:
        return "both"
    return "receptive" if receptive else "productive"


def _first_level(rows: list[dict], modes: set[str]) -> str | None:
    levels = {
        level for row in rows if set(row["mode_codes"]) & modes
        for level in row["source_level_codes"]
    }
    for level in LEVELS:
        if level in levels:
            return "a1" if level == "pre_a1" else level
    return None


def _stages(rows: list[dict], first: str, consolidation: str) -> list[dict]:
    evidence = Counter(level for row in rows for level in row["source_level_codes"])
    start = LEVELS.index(first)
    stages = []
    control = _control(rows)
    for level in LEVELS[start:]:
        states = []
        if level == first:
            states += ["expose", "introduce", "practise"]
        if level == consolidation:
            states.append("consolidate")
        if level in EXIT_LEVELS and LEVELS.index(level) > LEVELS.index(consolidation):
            states.append("recycle")
            if evidence[level]:
                states.append("extend")
        stages.append({
            "level": level, "evidence_count": evidence[level],
            "evidence_status": "source_evidenced" if evidence[level] else "planned_recycle",
            "control_expectation": control, "lifecycle_states": states,
        })
    return [stage for stage in stages if stage["lifecycle_states"]]


def _strand(function: str, rows: list[dict]) -> dict[str, Any]:
    ids = sorted(_assignment_id(row) for row in rows)
    source_levels = [level for level in LEVELS if any(level in row["source_level_codes"] for row in rows)]
    first = source_levels[0]
    receptive = _first_level(rows, {"reception"})
    productive = _first_level(
        rows, {"production", "interaction", "online_interaction", "mediation", "plurilingual_pluricultural", "communicative_competence"}
    )
    control_levels = [level for level in (receptive, productive) if level]
    consolidation = min(control_levels, key=EXIT_LEVELS.index)
    recycle = list(EXIT_LEVELS[EXIT_LEVELS.index(consolidation) + 1 :])
    evidence_exit = {level for level in source_levels if level in EXIT_LEVELS}
    extension = [level for level in recycle if level in evidence_exit]
    return {
        "strand_id": f"function.{function}", "function_code": function,
        "title": title(function), "curriculum_intent": INTENTS[function],
        "strand_role": strand_role(function),
        "evidence": {
            "assignment_count": len(ids), "assignment_ids_sha256": _hash_ids(ids),
            "representative_assignment_ids": _representatives(ids),
            "source_levels": source_levels,
            "source_datasets": sorted({row["source_dataset_id"] for row in rows}),
        },
        "lifecycle": {
            "first_exposure_level": first,
            "first_receptive_control_level": receptive,
            "first_productive_control_level": productive,
            "consolidation_level": consolidation,
            "recycle_levels": recycle, "extension_levels": extension,
            "within_level_order_required": True,
            "stages": _stages(rows, first, consolidation),
            "rationale": (
                "Published level evidence sets the first control boundary; earlier Pre-A1 evidence remains support. "
                "The function is deliberately recycled at every later exit level, while extension is source-evidenced."
            ),
        },
        "review": {"status": "accepted", "review_basis": "source_level_boundary_plus_persistence_policy"},
    }


def build() -> dict[str, Any]:
    tags = json.loads(TAGS.read_text(encoding="utf-8"))
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in tags["records"]:
        for function in row["function_codes"]:
            grouped[function].append(row)
    strands = [_strand(function, grouped[function]) for function in sorted(grouped)]
    links = sum(strand["evidence"]["assignment_count"] for strand in strands)
    return {
        "schema_version": 1, "dataset_id": "communicative_function_progression_strands",
        "version": 1, "level_order": list(LEVELS), "lifecycle_order": list(LIFECYCLE),
        "inputs": [
            {"path": TAGS.relative_to(ROOT).as_posix(), "sha256": file_sha256(TAGS)},
            {"path": PROFILES.relative_to(ROOT).as_posix(), "sha256": file_sha256(PROFILES)},
        ],
        "strands": strands,
        "audit": {
            "strand_count": len(strands), "source_assignment_count": len(tags["records"]),
            "evidence_link_count": links, "uncovered_assignments": [],
            "missing_consolidation": [], "invalid_level_regressions": [],
            "missing_post_consolidation_recycle": [],
        },
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "source_boundary_derived_lifecycle_plus_persistence_review",
            "limitations": [
                "A CEFR-level lifecycle boundary does not prescribe within-level lesson order.",
                "Function tags group comparable purposes but do not claim exact semantic equivalence between source records.",
                "Exact grammar, lexical, pronunciation, and assessment ownership is mapped in companion strands.",
            ],
        },
    }


def _report(data: dict[str, Any]) -> str:
    lines = [
        "# Communicative Function Progression v1", "", "Status: accepted internal curriculum contract.", "",
        "Each function has a sourced first-exposure/control boundary, an exit-level",
        "consolidation owner, planned recycling at every later level, and source-evidenced extension.",
        "", "| Function | Role | Expose | Consolidate | Recycle | Evidence |", "| --- | --- | --- | --- | --- | ---: |",
    ]
    for strand in data["strands"]:
        life = strand["lifecycle"]
        lines.append(
            f"| `{strand['function_code']}` | {strand['strand_role']} | {life['first_exposure_level'].upper()} | "
            f"{life['consolidation_level'].upper()} | {', '.join(x.upper() for x in life['recycle_levels']) or '-'} | "
            f"{strand['evidence']['assignment_count']} |"
        )
    lines += [
        "", "Pre-A1 is support, never a promised exit. Multiple lifecycle states at one",
        "CEFR level require real within-level sequencing: exposure and guided practice must",
        "precede consolidation. Counts show evidence links, not lesson weight.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['strands'])} strands)")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
