#!/usr/bin/env python3
"""Expand human-authored B1 semantic/control decisions into an exact role ledger.

NON-SEMANTIC by design. Automation may parse, join, expand, count and validate
only. It must fail rather than infer a role for any exact B1 source record.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B1 = ROOT / "curriculum/levels/b1"
REVIEW = B1 / "design-review"
SEMANTIC = REVIEW / "08-semantic-lock"
DECISIONS_PATH = SEMANTIC / "semantic-decisions.json"
COVERAGE_PATH = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"
DEFAULT_OUTPUT = SEMANTIC / "generated/semantic-role-ledger.json"
DEFAULT_REPORT = SEMANTIC / "generated/semantic-role-report.md"

EXPECTED_CATEGORY_COUNTS = {
    "ability": 249,
    "phrase": 175,
    "grammar": 338,
    "word": 809,
    "pronunciation": 10,
}
EXPECTED_TOTAL = 1581
VALID_MASTERY = {"productive", "receptive", "interactive", "integrated_support"}
VALID_SCOPE = {"generative", "bounded_pattern", "formulaic", "contextual", "quality_constraint"}
VALID_EXIT = {"independent_possible", "integrated_required", "support_condition"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_role(role: dict, where: str) -> dict:
    required = {"mastery_mode", "control_scope", "exit_evidence"}
    if set(role) != required:
        raise ValueError(f"{where}: role must contain exactly {sorted(required)}; got {sorted(role)}")
    if role["mastery_mode"] not in VALID_MASTERY:
        raise ValueError(f"{where}: invalid mastery_mode {role['mastery_mode']!r}")
    if role["control_scope"] not in VALID_SCOPE:
        raise ValueError(f"{where}: invalid control_scope {role['control_scope']!r}")
    if role["exit_evidence"] not in VALID_EXIT:
        raise ValueError(f"{where}: invalid exit_evidence {role['exit_evidence']!r}")
    return dict(role)


def source_mode(item: dict) -> str:
    modes = item.get("mode_codes") or []
    if len(modes) != 1:
        raise ValueError(f"ability {item.get('item_id')} must expose exactly one source mode; got {modes}")
    mode = modes[0]
    if mode not in {"reception", "production", "interaction"}:
        raise ValueError(f"ability {item.get('item_id')} has unsupported source mode {mode!r}")
    return mode


def add_semantic(record: dict, role: dict, basis: str, extra: dict | None = None) -> dict:
    out = dict(record)
    out["semantic_role"] = validate_role(role, basis)
    out["semantic_decision_basis"] = basis
    out["semantic_decision_source"] = "human_stage08"
    if extra:
        out.update(extra)
    return out


def category_counter(records: list[dict], field: str) -> dict[str, Counter]:
    result: dict[str, Counter] = defaultdict(Counter)
    for record in records:
        result[record["category"]][record["semantic_role"][field]] += 1
    return result


def render_counter(counter: Counter) -> str:
    if not counter:
        return "—"
    return ", ".join(f"{k}: {v}" for k, v in sorted(counter.items()))


def grouped_owner(groups: dict[str, list[str]], label: str) -> dict[str, str]:
    owner: dict[str, str] = {}
    for group, values in groups.items():
        for value in values:
            if value in owner:
                raise ValueError(f"{label} {value} assigned to multiple role groups: {owner[value]}, {group}")
            owner[value] = group
    return owner


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    ap.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = ap.parse_args()

    decisions = load_json(DECISIONS_PATH)
    coverage = load_json(COVERAGE_PATH)
    base_records = coverage.get("records", [])
    if len(base_records) != EXPECTED_TOTAL:
        raise ValueError(f"coverage ledger record drift: {len(base_records)} != {EXPECTED_TOTAL}")
    base_counts = Counter(x["category"] for x in base_records)
    if dict(base_counts) != EXPECTED_CATEGORY_COUNTS:
        raise ValueError(f"coverage category drift: {dict(base_counts)} != {EXPECTED_CATEGORY_COUNTS}")

    abilities = {x["item_id"]: x for x in load_json(B1 / "abilities.json")["items"]}
    if len(abilities) != 249:
        raise ValueError(f"B1 ability inventory drift: {len(abilities)} != 249")

    ability_decisions = decisions["abilities"]
    mode_policy = ability_decisions["capability_source_mode_policy"]
    cross_policy = ability_decisions["cross_cutting_home_policy"]
    if set(cross_policy) != {f"X{i:02d}" for i in range(1, 8)}:
        raise ValueError("B1 Stage-08 ability cross policy must cover X01..X07 exactly")

    phrase_decisions = decisions["phrases"]
    phrase_groups = {
        "productive_formulaic": phrase_decisions["productive_formulaic_homes"],
        "receptive_contextual": phrase_decisions["receptive_contextual_homes"],
        "integrated_support": phrase_decisions["integrated_support_homes"],
    }
    phrase_owner = grouped_owner(phrase_groups, "phrase home")

    grammar_decisions = decisions["grammar"]
    grammar_groups = {
        "productive_bounded": grammar_decisions["productive_bounded_systems"],
        "integrated_support": grammar_decisions["integrated_support_systems"],
    }
    grammar_owner = grouped_owner(grammar_groups, "grammar system")
    expected_systems = {f"G{i:02d}" for i in range(1, 60)}
    if set(grammar_owner) != expected_systems:
        raise ValueError(
            f"grammar role groups must cover G01..G59 exactly; missing={sorted(expected_systems-set(grammar_owner))} "
            f"extra={sorted(set(grammar_owner)-expected_systems)}"
        )
    row_overrides = {int(k): v for k, v in grammar_decisions.get("review_row_overrides", {}).items()}
    valid_grammar_role_names = set(grammar_decisions["role_templates"])
    for row, override in row_overrides.items():
        if not 1 <= row <= 338:
            raise ValueError(f"grammar semantic override outside review rows 1..338: {row}")
        if override.get("role") not in valid_grammar_role_names:
            raise ValueError(f"grammar row {row} override uses unknown role {override.get('role')!r}")
        if not override.get("reason"):
            raise ValueError(f"grammar row {row} override must include human reason")

    word_decisions = decisions["words"]
    word_groups = {
        "productive_contextual": word_decisions["productive_contextual_homes"],
        "integrated_support": word_decisions["integrated_support_homes"],
        "receptive_contextual": word_decisions["receptive_contextual_homes"],
    }
    word_owner = grouped_owner(word_groups, "word home")
    expected_word_homes = {f"L{i:02d}" for i in range(1, 28)} | {"LX-GENERAL"}
    if set(word_owner) != expected_word_homes:
        raise ValueError(
            f"word role homes must cover L01..L27 + LX-GENERAL exactly; "
            f"missing={sorted(expected_word_homes-set(word_owner))} extra={sorted(set(word_owner)-expected_word_homes)}"
        )

    pronunciation_decisions = decisions["pronunciation"]
    if len(pronunciation_decisions) != 10:
        raise ValueError(f"pronunciation decisions must cover 10 items; got {len(pronunciation_decisions)}")

    records: list[dict] = []
    seen: set[str] = set()
    phrase_homes_seen: set[str] = set()
    word_homes_seen: set[str] = set()
    grammar_systems_seen: set[str] = set()

    for record in base_records:
        iid = record["item_id"]
        category = record["category"]
        if iid in seen:
            raise ValueError(f"duplicate item_id in exact coverage ledger: {iid}")
        seen.add(iid)

        if category == "ability":
            item = abilities.get(iid)
            if item is None:
                raise ValueError(f"coverage ability missing canonical B1 item: {iid}")
            mode = source_mode(item)
            home = record["homes"][0]
            if home.startswith("C"):
                role = dict(mode_policy[mode])
                basis = f"ability.capability_home:{home};source_mode:{mode}"
            elif home.startswith("X"):
                if home not in cross_policy:
                    raise ValueError(f"ability cross-cutting home lacks Stage-08 role: {home}")
                role = dict(cross_policy[home])
                if role["mastery_mode"] == "source_mode":
                    role["mastery_mode"] = mode_policy[mode]["mastery_mode"]
                basis = f"ability.cross_cutting_home:{home};source_mode:{mode}"
            else:
                raise ValueError(f"ability has invalid semantic home: {iid} -> {home}")
            records.append(add_semantic(record, role, basis, {"source_mode": mode}))

        elif category == "phrase":
            home = record["homes"][0]
            phrase_homes_seen.add(home)
            group = phrase_owner.get(home)
            if group is None:
                raise ValueError(f"phrase home lacks explicit human Stage-08 role: {iid} -> {home}")
            template = phrase_decisions["role_templates"][group]
            records.append(add_semantic(record, template, f"phrase.home:{home};group:{group}"))

        elif category == "grammar":
            system = record.get("grammar_system")
            grammar_systems_seen.add(system)
            group = grammar_owner.get(system)
            if group is None:
                raise ValueError(f"grammar system lacks explicit human Stage-08 role: {iid} -> {system}")
            row = int(record["review_row"])
            if row in row_overrides:
                role_name = row_overrides[row]["role"]
                template = grammar_decisions["role_templates"][role_name]
                basis = f"grammar.review_row_override:{row};system:{system};role:{role_name}"
                records.append(add_semantic(record, template, basis, {"semantic_override_reason": row_overrides[row]["reason"]}))
            else:
                template = grammar_decisions["role_templates"][group]
                records.append(add_semantic(record, template, f"grammar.system:{system};group:{group}"))

        elif category == "word":
            home = record["homes"][0]
            word_homes_seen.add(home)
            group = word_owner.get(home)
            if group is None:
                raise ValueError(f"word home lacks explicit human Stage-08 role: {iid} -> {home}")
            template = word_decisions["role_templates"][group]
            records.append(add_semantic(record, template, f"word.reviewed_home:{home};group:{group}"))

        elif category == "pronunciation":
            if iid not in pronunciation_decisions:
                raise ValueError(f"pronunciation item lacks explicit Stage-08 decision: {iid}")
            records.append(add_semantic(record, pronunciation_decisions[iid], f"pronunciation.item:{iid}"))

        else:
            raise ValueError(f"unknown coverage category: {category}")

    if len(records) != EXPECTED_TOTAL or len(seen) != EXPECTED_TOTAL:
        raise ValueError("semantic expansion did not preserve exactly 1,581 B1 records")
    if not phrase_homes_seen <= set(phrase_owner):
        raise ValueError(f"unowned phrase homes: {sorted(phrase_homes_seen-set(phrase_owner))}")
    if word_homes_seen != expected_word_homes:
        raise ValueError(f"exact word ledger did not exercise all reviewed homes: missing={sorted(expected_word_homes-word_homes_seen)}")
    if grammar_systems_seen != expected_systems:
        raise ValueError(f"exact grammar ledger did not exercise G01..G59 exactly")

    category_counts = Counter(x["category"] for x in records)
    if dict(category_counts) != EXPECTED_CATEGORY_COUNTS:
        raise ValueError(f"semantic category count mismatch: {dict(category_counts)}")

    mastery_counts = Counter(x["semantic_role"]["mastery_mode"] for x in records)
    scope_counts = Counter(x["semantic_role"]["control_scope"] for x in records)
    exit_counts = Counter(x["semantic_role"]["exit_evidence"] for x in records)
    mastery_by_category = category_counter(records, "mastery_mode")
    scope_by_category = category_counter(records, "control_scope")

    grammar_system_defaults = Counter(grammar_owner.values())
    grammar_override_roles = Counter(v["role"] for v in row_overrides.values())
    phrase_role_counts = Counter(
        x["semantic_role"]["mastery_mode"] for x in records if x["category"] == "phrase"
    )
    word_role_counts = Counter(
        x["semantic_role"]["mastery_mode"] for x in records if x["category"] == "word"
    )

    out = {
        "schema_version": 1,
        "level": "B1",
        "status": "expanded_from_human_stage08_semantic_decisions",
        "record_count": EXPECTED_TOTAL,
        "record_counts": EXPECTED_CATEGORY_COUNTS,
        "automation_inferred_semantic_roles": 0,
        "human_semantic_orphans": 0,
        "mastery_counts": dict(sorted(mastery_counts.items())),
        "control_scope_counts": dict(sorted(scope_counts.items())),
        "exit_evidence_counts": dict(sorted(exit_counts.items())),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = [
        "# B1 Semantic Role Expansion Audit",
        "",
        "Status: **GENERATED FROM EXPLICIT HUMAN STAGE-08 DECISIONS — NON-SEMANTIC EXPANSION**",
        "",
        f"- exact source records assigned a semantic/control role: **{len(records)} / {EXPECTED_TOTAL}**",
        "- human semantic orphans: **0**",
        "- automation-inferred semantic roles: **0**",
        "",
        "## Exact category accounting",
        "",
        "| Category | Records | Mastery modes | Control scopes |",
        "|---|---:|---|---|",
    ]
    for category in ("ability", "phrase", "grammar", "word", "pronunciation"):
        report.append(
            f"| {category} | {category_counts[category]} | {render_counter(mastery_by_category[category])} | "
            f"{render_counter(scope_by_category[category])} |"
        )
    report += [
        "",
        "## Whole-level semantic role counts",
        "",
        f"- mastery modes: **{render_counter(mastery_counts)}**",
        f"- control scopes: **{render_counter(scope_counts)}**",
        f"- exit-evidence roles: **{render_counter(exit_counts)}**",
        "",
        "## Human policy accounting",
        "",
        f"- phrase mastery rows after home policy: **{render_counter(phrase_role_counts)}**",
        f"- word mastery rows after reviewed-home policy: **{render_counter(word_role_counts)}**",
        f"- grammar system defaults: **{render_counter(grammar_system_defaults)}**",
        f"- explicit grammar review-row overrides: **{len(row_overrides)}** ({render_counter(grammar_override_roles)})",
        "",
        "## Integrity verdict",
        "",
        "**PASS — all 1,581 exact B1 source records have an explicit human-owned Stage-08 semantic/control role; automation inferred none.**",
        "",
        "This is the base Stage-08 lock candidate. Stage 08.5 must now challenge role-aware lesson load, modality boundaries, formulaic vs generative control and every Stage-06 warning before the lock can be treated as reconciled.",
        "",
    ]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
