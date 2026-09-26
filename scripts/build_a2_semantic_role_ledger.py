#!/usr/bin/env python3
"""Expand human-authored A2 semantic/mastery decisions into an exact role ledger.

NON-SEMANTIC by design.

This script is allowed to parse, join, expand, count, validate, and report only.
It MUST fail rather than infer a mastery role for any ability, phrase, grammar row,
word, or pronunciation strand that is not covered by the explicit Stage-08 human
semantic decisions.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A2 = ROOT / "curriculum/levels/a2"
REVIEW = A2 / "design-review"
SEMANTIC = REVIEW / "08-semantic-lock"
DECISIONS_PATH = SEMANTIC / "semantic-decisions.json"
COVERAGE_PATH = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"
WORD_AID_PATH = REVIEW / "04-words/generated/word-review-aid.md"
DEFAULT_OUTPUT = SEMANTIC / "generated/semantic-role-ledger.json"
DEFAULT_REPORT = SEMANTIC / "generated/semantic-role-report.md"

EXPECTED_CATEGORY_COUNTS = {
    "ability": 269,
    "phrase": 176,
    "grammar": 291,
    "word": 871,
    "pronunciation": 10,
}
EXPECTED_TOTAL = 1617
VALID_MASTERY = {"productive", "receptive", "interactive", "integrated_support"}
VALID_SCOPE = {"generative", "bounded_pattern", "formulaic", "contextual", "quality_constraint"}
VALID_EXIT = {"independent_possible", "integrated_required", "support_condition"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def expand_number_spec(value: str) -> set[int]:
    """Parse human-authored number specs such as '2-5, 9, 11-13'."""
    value = value.replace("–", "-").replace("—", "-")
    out: set[int] = set()
    for raw in re.split(r"[,;]", value):
        part = raw.strip().strip(".")
        if not part:
            continue
        m = re.fullmatch(r"(\d+)\s*-\s*(\d+)", part)
        if m:
            a, b = map(int, m.groups())
            if b < a:
                raise ValueError(f"descending review-row range is not allowed: {part}")
            out.update(range(a, b + 1))
            continue
        if not part.isdigit():
            raise ValueError(f"unparseable review-row token: {part!r}")
        out.add(int(part))
    return out


def word_review_rows(markdown: str) -> tuple[dict[int, str], dict[str, int]]:
    by_row: dict[int, str] = {}
    by_id: dict[str, int] = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|")
    for line in markdown.splitlines():
        m = rx.match(line)
        if not m:
            continue
        row = int(m.group(1))
        iid = m.group(2)
        if row in by_row or iid in by_id:
            raise ValueError(f"duplicate word review mapping: row={row} item={iid}")
        by_row[row] = iid
        by_id[iid] = row
    return by_row, by_id


def validate_role(role: dict, where: str) -> dict:
    keys = {"mastery_mode", "control_scope", "exit_evidence"}
    if set(role) != keys:
        raise ValueError(f"{where}: semantic role must contain exactly {sorted(keys)}, got {sorted(role)}")
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
    base_category_counts = Counter(x["category"] for x in base_records)
    if dict(base_category_counts) != EXPECTED_CATEGORY_COUNTS:
        raise ValueError(f"coverage category drift: {dict(base_category_counts)} != {EXPECTED_CATEGORY_COUNTS}")

    abilities_all = load_json(A2 / "abilities.json")["items"]
    abilities = {x["item_id"]: x for x in abilities_all if x.get("curriculum_role") == "include_for_spine"}
    if len(abilities) != 269:
        raise ValueError(f"required ability inventory drift: {len(abilities)} != 269")

    # Human row/set/system decisions.
    ability_decisions = decisions["abilities"]
    formulaic_ability_rows = expand_number_spec(
        ability_decisions["capability_rows"]["formulaic_scope_review_rows"]
    )
    source_mode_policy = ability_decisions["capability_rows"]["source_mode_policy"]
    cross_policy = ability_decisions["cross_cutting_home_policy"]

    phrase_decisions = decisions["phrases"]
    phrase_groups = {
        "productive_formulaic": set(phrase_decisions["productive_formulaic_homes"]),
        "receptive_contextual": set(phrase_decisions["receptive_contextual_homes"]),
        "integrated_support": set(phrase_decisions["integrated_support_homes"]),
    }
    phrase_home_owner: dict[str, str] = {}
    for group, homes in phrase_groups.items():
        for home in homes:
            if home in phrase_home_owner:
                raise ValueError(f"phrase home {home} assigned to multiple semantic groups")
            phrase_home_owner[home] = group

    grammar_decisions = decisions["grammar"]
    grammar_groups = {
        "productive_bounded": set(grammar_decisions["productive_bounded_systems"]),
        "integrated_support": set(grammar_decisions["integrated_support_systems"]),
        "receptive_bounded": set(grammar_decisions["receptive_bounded_systems"]),
    }
    grammar_owner: dict[str, str] = {}
    for group, systems in grammar_groups.items():
        for system in systems:
            if system in grammar_owner:
                raise ValueError(f"grammar system {system} assigned to multiple semantic groups")
            grammar_owner[system] = group
    if set(grammar_owner) != {f"G{i:02d}" for i in range(1, 47)}:
        missing = sorted({f"G{i:02d}" for i in range(1, 47)} - set(grammar_owner))
        extra = sorted(set(grammar_owner) - {f"G{i:02d}" for i in range(1, 47)})
        raise ValueError(f"grammar semantic groups must cover G01..G46 exactly; missing={missing}, extra={extra}")

    word_decisions = decisions["words"]
    productive_word_rows = expand_number_spec(word_decisions["productive_review_rows"])
    support_word_rows = expand_number_spec(word_decisions["integrated_support_review_rows"])
    expected_word_rows = set(range(1, 872))
    if productive_word_rows & support_word_rows:
        raise ValueError(f"word semantic row overlap: {sorted(productive_word_rows & support_word_rows)[:40]}")
    if not productive_word_rows <= expected_word_rows or not support_word_rows <= expected_word_rows:
        raise ValueError("word semantic row decision outside 1..871")
    receptive_word_rows = expected_word_rows - productive_word_rows - support_word_rows
    actual_word_role_counts = {
        "productive": len(productive_word_rows),
        "integrated_support": len(support_word_rows),
        "receptive_contextual": len(receptive_word_rows),
    }
    if actual_word_role_counts != word_decisions["expected_counts"]:
        raise ValueError(
            f"word semantic decision count drift: {actual_word_role_counts} != {word_decisions['expected_counts']}"
        )
    word_aid_text = WORD_AID_PATH.read_text(encoding="utf-8")
    word_row_to_id, word_id_to_row = word_review_rows(word_aid_text)
    if set(word_row_to_id) != expected_word_rows:
        raise ValueError("word review aid must expose exact rows 1..871")

    pronunciation_decisions = decisions["pronunciation"]

    records: list[dict] = []
    seen_ids: set[str] = set()
    for record in base_records:
        iid = record["item_id"]
        category = record["category"]
        if iid in seen_ids:
            raise ValueError(f"duplicate item_id in coverage ledger: {iid}")
        seen_ids.add(iid)

        if category == "ability":
            if iid not in abilities:
                raise ValueError(f"coverage ability missing canonical required item: {iid}")
            row = int(record["review_row"])
            home = record["homes"][0]
            mode = source_mode(abilities[iid])
            if home.startswith("C"):
                if mode not in source_mode_policy:
                    raise ValueError(f"ability source mode lacks human policy: {mode}")
                role = dict(source_mode_policy[mode])
                basis = f"ability.source_mode:{mode};home:{home}"
                if row in formulaic_ability_rows:
                    role["control_scope"] = "formulaic"
                    basis += ";formulaic_review_row"
            elif home.startswith("X"):
                if home not in cross_policy:
                    raise ValueError(f"cross-cutting ability home lacks human semantic policy: {home}")
                role = dict(cross_policy[home])
                if role["mastery_mode"] == "source_mode":
                    role["mastery_mode"] = source_mode_policy[mode]["mastery_mode"]
                basis = f"ability.cross_cutting:{home};source_mode:{mode}"
            else:
                raise ValueError(f"ability has non C/X home: {iid} -> {home}")
            records.append(add_semantic(record, role, basis, {"source_mode": mode}))

        elif category == "phrase":
            home = record["homes"][0]
            group = phrase_home_owner.get(home)
            if group is None:
                raise ValueError(f"phrase home lacks explicit semantic group: {iid} -> {home}")
            template = phrase_decisions["role_templates"][group]
            records.append(add_semantic(record, template, f"phrase.home:{home};group:{group}"))

        elif category == "grammar":
            system = record.get("grammar_system")
            group = grammar_owner.get(system)
            if group is None:
                raise ValueError(f"grammar row lacks explicit semantic system group: {iid} -> {system}")
            template = grammar_decisions["role_templates"][group]
            records.append(add_semantic(record, template, f"grammar.system:{system};group:{group}"))

        elif category == "word":
            if iid not in word_id_to_row:
                raise ValueError(f"word coverage item absent from exact review aid: {iid}")
            row = word_id_to_row[iid]
            if row in productive_word_rows:
                group = "productive"
            elif row in support_word_rows:
                group = "integrated_support"
            else:
                group = "receptive_contextual"
            template = word_decisions["role_templates"][group]
            records.append(add_semantic(
                record,
                template,
                f"word.manual_review_row:{row};group:{group}",
                {"review_row": row},
            ))

        elif category == "pronunciation":
            if iid not in pronunciation_decisions:
                raise ValueError(f"pronunciation item lacks explicit semantic decision: {iid}")
            records.append(add_semantic(record, pronunciation_decisions[iid], f"pronunciation.item:{iid}"))

        else:
            raise ValueError(f"unknown coverage category: {category}")

    if len(records) != EXPECTED_TOTAL or len(seen_ids) != EXPECTED_TOTAL:
        raise ValueError("semantic expansion did not preserve exact 1,617 source records")

    # Validate category counts after expansion.
    semantic_category_counts = Counter(x["category"] for x in records)
    if dict(semantic_category_counts) != EXPECTED_CATEGORY_COUNTS:
        raise ValueError(f"semantic category count mismatch: {dict(semantic_category_counts)}")

    # Human-locked phrase count check.
    phrase_role_counts = Counter(
        x["semantic_role"]["mastery_mode"] for x in records if x["category"] == "phrase"
    )
    expected_phrase_mastery = Counter({"productive": 118, "receptive": 28, "integrated_support": 30})
    if phrase_role_counts != expected_phrase_mastery:
        raise ValueError(f"phrase semantic count drift: {phrase_role_counts} != {expected_phrase_mastery}")

    # Human-locked grammar system count check and expanded row accounting.
    grammar_system_role_counts = Counter()
    for system, group in grammar_owner.items():
        grammar_system_role_counts[group] += 1
    expected_grammar_system_counts = Counter({"productive_bounded": 30, "integrated_support": 14, "receptive_bounded": 2})
    if grammar_system_role_counts != expected_grammar_system_counts:
        raise ValueError(
            f"grammar semantic system count drift: {grammar_system_role_counts} != {expected_grammar_system_counts}"
        )

    # Exact pronunciation count check.
    if len(pronunciation_decisions) != 10:
        raise ValueError(f"pronunciation decisions must cover exactly 10 items; got {len(pronunciation_decisions)}")

    mastery_counts = Counter(x["semantic_role"]["mastery_mode"] for x in records)
    scope_counts = Counter(x["semantic_role"]["control_scope"] for x in records)
    exit_counts = Counter(x["semantic_role"]["exit_evidence"] for x in records)
    mastery_by_category = category_counter(records, "mastery_mode")

    # Role-aware introduction load. Active means independent learner output/exchange,
    # while receptive and integrated support remain visible separately.
    lesson_ids: list[str] = []
    for record in records:
        for lesson in record["lifecycle"]["introduce"]:
            if lesson not in lesson_ids:
                lesson_ids.append(lesson)
    # Preserve course order from first appearance in the Stage-06 ledger, then sort U/L numerically.
    def lesson_key(lid: str):
        m = re.fullmatch(r"U(\d+)-L(\d+)", lid)
        return tuple(map(int, m.groups())) if m else (999, 999)
    lesson_ids = sorted(set(lesson_ids), key=lesson_key)

    lesson_load: dict[str, Counter] = {lid: Counter() for lid in lesson_ids}
    grammar_systems_by_lesson: dict[str, set[str]] = defaultdict(set)
    for record in records:
        intro = record["lifecycle"]["introduce"][0]
        role = record["semantic_role"]
        mastery = role["mastery_mode"]
        lesson_load[intro]["all"] += 1
        if mastery in {"productive", "interactive"}:
            lesson_load[intro]["active_rows"] += 1
            lesson_load[intro][f"active_{record['category']}"] += 1
            if role["control_scope"] == "formulaic":
                lesson_load[intro]["active_formulaic"] += 1
            if record["category"] == "grammar":
                grammar_systems_by_lesson[intro].add(record["grammar_system"])
        elif mastery == "receptive":
            lesson_load[intro]["receptive_rows"] += 1
        elif mastery == "integrated_support":
            lesson_load[intro]["support_rows"] += 1

    # Output exact ledger.
    output = {
        "schema_version": 1,
        "level": "A2",
        "status": "expanded_from_human_semantic_decisions",
        "source_coverage_status": coverage.get("status"),
        "record_count": len(records),
        "category_counts": dict(semantic_category_counts),
        "mastery_mode_counts": dict(mastery_counts),
        "control_scope_counts": dict(scope_counts),
        "exit_evidence_counts": dict(exit_counts),
        "records": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Human-readable audit report.
    lines: list[str] = [
        "# A2 Semantic / Mastery Role Audit",
        "",
        "Status: **GENERATED FROM HUMAN SEMANTIC DECISIONS — NON-SEMANTIC EXPANSION**",
        "",
        f"Exact records assigned: **{len(records)} / {EXPECTED_TOTAL}**",
        "",
        "## Overall semantic counts",
        "",
        f"- mastery modes: {render_counter(mastery_counts)}",
        f"- control scopes: {render_counter(scope_counts)}",
        f"- exit-evidence roles: {render_counter(exit_counts)}",
        "",
        "## Category mastery breakdown",
        "",
        "| Category | productive | interactive | receptive | integrated support | Total |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for category in ("ability", "phrase", "grammar", "word", "pronunciation"):
        c = mastery_by_category[category]
        lines.append(
            f"| {category} | {c['productive']} | {c['interactive']} | {c['receptive']} | {c['integrated_support']} | {sum(c.values())} |"
        )

    lines += [
        "",
        "## Locked semantic checks",
        "",
        f"- word roles: productive **{len(productive_word_rows)}**, integrated support **{len(support_word_rows)}**, receptive **{len(receptive_word_rows)}** — total **871**",
        f"- phrase roles: productive/formulaic **{phrase_role_counts['productive']}**, receptive/contextual **{phrase_role_counts['receptive']}**, integrated support **{phrase_role_counts['integrated_support']}** — total **176**",
        f"- grammar systems: productive bounded **{grammar_system_role_counts['productive_bounded']}**, integrated support **{grammar_system_role_counts['integrated_support']}**, receptive bounded **{grammar_system_role_counts['receptive_bounded']}** — total **46**",
        "- semantic orphans: **0**",
        "- automation-inferred semantic roles: **0**",
        "",
        "## Role-aware introduction load by lesson",
        "",
        "`active rows` = productive + interactive source records. Grammar is additionally compressed into distinct productive systems so raw EGP-row density is not mistaken for the number of teachable grammar systems.",
        "",
        "| Lesson | Active rows | Active abilities | Active phrases | Active grammar rows | Productive grammar systems | Active words | Formulaic active | Receptive rows | Support rows | All source rows |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for lid in lesson_ids:
        c = lesson_load[lid]
        lines.append(
            f"| {lid} | {c['active_rows']} | {c['active_ability']} | {c['active_phrase']} | {c['active_grammar']} | {len(grammar_systems_by_lesson[lid])} | {c['active_word']} | {c['active_formulaic']} | {c['receptive_rows']} | {c['support_rows']} | {c['all']} |"
        )

    ranked = sorted(lesson_ids, key=lambda lid: (lesson_load[lid]["active_rows"], lesson_load[lid]["all"]), reverse=True)
    lines += [
        "",
        "## Human Stage-08.5 critic queue",
        "",
        "The following lessons have the highest active-source introduction counts after semantic compression. This is a **review queue, not an automatic failure list**:",
        "",
    ]
    for lid in ranked[:12]:
        c = lesson_load[lid]
        lines.append(
            f"- **{lid}** — active rows {c['active_rows']}; active words {c['active_word']}; active abilities {c['active_ability']}; active phrases {c['active_phrase']}; productive grammar systems {len(grammar_systems_by_lesson[lid])}; receptive/support rows {c['receptive_rows']}/{c['support_rows']}."
        )

    lines += [
        "",
        "## Audit verdict",
        "",
        "**PASS — all 1,617 exact A2 source records have an explicit human-authored semantic role.**",
        "",
        "This report does **not** by itself close Milestone 3. Stage 08.5 must now perform a human role-aware lifecycle/load reconciliation against the locked 83-slot architecture.",
    ]
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
