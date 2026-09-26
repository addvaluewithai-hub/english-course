#!/usr/bin/env python3
"""Expand reviewed B1 curriculum decisions into an auditable provisional lifecycle ledger.

NON-SEMANTIC by design. Human decisions live in B1 Stage 01-06 artifacts.
This script may only join exact source records, balance records inside explicitly
approved introduction windows, count, validate, and report gaps/overloads.
It must fail rather than invent semantic homes, grammar systems, or lessons.
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
PLAN_PATH = REVIEW / "06-coverage-ledger/lifecycle-plan.json"
WORD_MAP_PATH = REVIEW / "04-words/generated/word-home-map.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lesson_ids(markdown: str) -> list[str]:
    seen: list[str] = []
    for lid in re.findall(r"^###\s+(U\d+-L\d+)\b", markdown, flags=re.MULTILINE):
        if lid not in seen:
            seen.append(lid)
    return seen


def expand_number_spec(value: str) -> list[int]:
    value = value.replace("–", "-").replace("—", "-")
    out: list[int] = []
    for part in re.split(r"[,;]", value):
        part = part.strip().strip(".")
        if not part:
            continue
        m = re.search(r"(\d+)\s*-\s*(\d+)", part)
        if m:
            a, b = map(int, m.groups())
            out.extend(range(a, b + 1))
            continue
        m = re.search(r"\d+", part)
        if m:
            out.append(int(m.group()))
    return out


def parse_aid_row_ids(markdown: str, id_pattern: str) -> dict[int, str]:
    result: dict[int, str] = {}
    rx = re.compile(rf"^\|\s*(\d+)\s*\|\s*`({id_pattern})`\s*\|")
    for line in markdown.splitlines():
        m = rx.match(line)
        if m:
            result[int(m.group(1))] = m.group(2)
    return result


def parse_ability_homes(markdown: str) -> dict[int, str]:
    homes: dict[int, str] = {}
    current: str | None = None
    for line in markdown.splitlines():
        h = re.match(r"##\s+([CX]\d{2})\b", line)
        if h:
            current = h.group(1)
            continue
        if line.startswith("#") and not line.startswith("##"):
            current = None
            continue
        if not current or "Source-review row" not in line:
            continue
        for row in [int(x) for x in re.findall(r"\d+", line)]:
            if row in homes and homes[row] != current:
                raise ValueError(f"ability row {row} mapped to multiple homes: {homes[row]}, {current}")
            homes[row] = current
    return homes


def parse_phrase_homes(markdown: str) -> dict[int, str]:
    homes: dict[int, str] = {}
    current: str | None = None
    for line in markdown.splitlines():
        h = re.match(r"##\s+([CX]\d{2})\b", line)
        if h:
            current = h.group(1)
            continue
        if line.startswith("#") and not line.startswith("##"):
            current = None
            continue
        if not current or not re.match(r"Rows?:", line.strip()):
            continue
        bold = re.findall(r"\*\*([^*]+)\*\*", line)
        source = " ".join(bold) if bold else line
        for row in expand_number_spec(source):
            if row in homes and homes[row] != current:
                raise ValueError(f"phrase row {row} mapped to multiple homes: {homes[row]}, {current}")
            homes[row] = current
    return homes


def parse_grammar_aid(markdown: str) -> dict[int, int]:
    result: dict[int, int] = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|")
    for line in markdown.splitlines():
        m = rx.match(line)
        if m:
            result[int(m.group(1))] = int(m.group(2))
    return result


def parse_grammar_systems(markdown: str) -> tuple[dict[int, str], dict[str, list[str]]]:
    row_system: dict[int, str] = {}
    system_homes: dict[str, list[str]] = {}
    current: str | None = None
    pending_rows: list[int] = []
    for line in markdown.splitlines():
        h = re.match(r"##\s+(G\d{2})\b", line)
        if h:
            if current and pending_rows:
                for row in pending_rows:
                    row_system[row] = current
            current = h.group(1)
            pending_rows = []
            continue
        if line.startswith("#") and not line.startswith("##"):
            if current and pending_rows:
                for row in pending_rows:
                    row_system[row] = current
            current = None
            pending_rows = []
            continue
        if not current:
            continue
        if line.startswith("**Review row"):
            content = line.split(":", 1)[1] if ":" in line else line
            pending_rows = expand_number_spec(content.replace("**", ""))
        elif line.startswith("**Homes:**"):
            system_homes[current] = list(dict.fromkeys(re.findall(r"\b[CX]\d{2}\b", line)))
    if current and pending_rows:
        for row in pending_rows:
            row_system[row] = current
    return row_system, system_homes


def family_plan(plan: dict, home: str) -> dict:
    if home.startswith("C"):
        return plan["capabilities"][home]
    if home.startswith("X"):
        return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]


def validate_refs(plan: dict, lessons: list[str]) -> None:
    allowed = set(lessons)
    refs: list[tuple[str, str]] = []
    for group in ("capabilities", "cross_cutting", "lexical_sets", "pronunciation"):
        for home, lifecycle in plan[group].items():
            for stage, values in lifecycle.items():
                refs.extend((f"{group}.{home}.{stage}", x) for x in values)
    for system, values in plan["grammar_system_intro"].items():
        refs.extend((f"grammar_system_intro.{system}", x) for x in values)
    bad = [(where, lid) for where, lid in refs if lid not in allowed]
    if bad:
        raise ValueError(f"lifecycle plan references unknown lessons: {bad[:30]}")


def stable_offset(key: str, size: int) -> int:
    if size <= 1:
        return 0
    return sum((i + 1) * ord(ch) for i, ch in enumerate(key)) % size


def balanced_assignment(records: list[dict], key_fn, windows_fn, *, salt: str) -> dict[str, str]:
    """Mechanically round-robin only inside human-approved windows.

    The stable salt/key offset prevents every independent family/category from
    stacking its first record onto the first approved lesson. It does not change
    any semantic home or introduce a lesson outside the human-approved window.
    """
    assigned: dict[str, str] = {}
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        groups[key_fn(record)].append(record)
    for key, values in groups.items():
        windows = windows_fn(key)
        if not windows:
            raise ValueError(f"no human-approved introduction window for {key}")
        offset = stable_offset(f"{salt}:{key}", len(windows))
        for i, record in enumerate(values):
            assigned[record["item_id"]] = windows[(i + offset) % len(windows)]
    return assigned


def later_lessons(plan: dict, homes: list[str], stage: str, order: dict[str, int], intro: str, *, strictly_later: bool) -> list[str]:
    intro_idx = order[intro]
    values: set[str] = set()
    for home in homes:
        values.update(family_plan(plan, home).get(stage, []))
    if strictly_later:
        values = {x for x in values if order[x] > intro_idx}
    else:
        values = {x for x in values if order[x] >= intro_idx}
    return sorted(values, key=order.__getitem__)


def build_record(category: str, item: dict, label: str, homes: list[str], intro: str, plan: dict, order: dict[str, int], extra: dict | None = None) -> dict:
    record = {
        "category": category,
        "item_id": item["item_id"],
        "label": label,
        "homes": homes,
        "lifecycle": {
            "introduce": [intro],
            "practice": later_lessons(plan, homes, "practice", order, intro, strictly_later=False),
            "fresh_retrieval": later_lessons(plan, homes, "fresh_retrieval", order, intro, strictly_later=True),
            "recycle": later_lessons(plan, homes, "recycle", order, intro, strictly_later=True),
            "consolidate": later_lessons(plan, homes, "consolidate", order, intro, strictly_later=True),
            "exit_verify": later_lessons(plan, homes, "exit_verify", order, intro, strictly_later=True),
        },
    }
    if extra:
        record.update(extra)
    return record


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    plan = load_json(PLAN_PATH)
    curriculum = text(REVIEW / "05-curriculum-map/curriculum-map.md")
    lessons = lesson_ids(curriculum)
    if len(lessons) != plan["lesson_count_baseline"]:
        raise ValueError(f"lesson skeleton mismatch: map={len(lessons)} plan={plan['lesson_count_baseline']}")
    order = {lid: i for i, lid in enumerate(lessons)}
    validate_refs(plan, lessons)

    abilities = load_json(B1 / "abilities.json")["items"]
    phrases = load_json(B1 / "phrases.json")["items"]
    grammar = load_json(B1 / "grammar.json")["items"]
    words = load_json(B1 / "words.json")["items"]
    pronunciation = load_json(B1 / "pronunciation.json")["items"]

    expected_counts = {"ability": 249, "phrase": 175, "grammar": 338, "word": 809, "pronunciation": 10}
    source_counts = {
        "ability": len(abilities), "phrase": len(phrases), "grammar": len(grammar),
        "word": len(words), "pronunciation": len(pronunciation),
    }
    if source_counts != expected_counts:
        raise ValueError(f"B1 source count drift: {source_counts} != {expected_counts}")

    ability_row_source = parse_aid_row_ids(text(REVIEW / "01-abilities/generated/ability-review-aid.md"), r"[^`]+")
    ability_row_home = parse_ability_homes(text(REVIEW / "01-abilities/final-capability-map.md"))
    expected_ability_rows = set(range(1, 250))
    if set(ability_row_source) != expected_ability_rows or set(ability_row_home) != expected_ability_rows:
        raise ValueError("B1 ability review rows must map exactly 1..249")
    ability_by_source = {x["source_record_id"]: x for x in abilities}
    ability_records: list[dict] = []
    for row in range(1, 250):
        source_id = ability_row_source[row]
        if source_id not in ability_by_source:
            raise ValueError(f"ability source row missing from canonical inventory: row={row} source={source_id}")
        ability_records.append({**ability_by_source[source_id], "review_row": row, "primary_home": ability_row_home[row]})
    ability_intro = balanced_assignment(ability_records, lambda x: x["primary_home"], lambda h: family_plan(plan, h)["introduce"], salt="ability")

    phrase_row_id = parse_aid_row_ids(text(REVIEW / "02-phrases/generated/phrase-review-aid.md"), r"oxford\.phrase\.online\.\d+")
    phrase_row_home = parse_phrase_homes(text(REVIEW / "02-phrases/phrase-review.md"))
    expected_phrase_rows = set(range(1, 176))
    if set(phrase_row_id) != expected_phrase_rows or set(phrase_row_home) != expected_phrase_rows:
        raise ValueError("B1 phrase review rows must map exactly 1..175")
    phrase_by_id = {x["item_id"]: x for x in phrases}
    phrase_records = [{**phrase_by_id[phrase_row_id[row]], "review_row": row, "primary_home": phrase_row_home[row]} for row in range(1, 176)]
    phrase_intro = balanced_assignment(phrase_records, lambda x: x["primary_home"], lambda h: family_plan(plan, h)["introduce"], salt="phrase")

    grammar_row_to_source = parse_grammar_aid(text(REVIEW / "03-grammar/generated/grammar-review-aid.md"))
    grammar_row_system, grammar_system_homes = parse_grammar_systems(text(REVIEW / "03-grammar/grammar-review.md"))
    expected_grammar_rows = set(range(1, 339))
    if set(grammar_row_to_source) != expected_grammar_rows or set(grammar_row_system) != expected_grammar_rows:
        raise ValueError("B1 grammar review rows must map exactly 1..338")
    grammar_by_source_row = {int(x["source_ref"]["spreadsheet_row"]): x for x in grammar}
    grammar_records: list[dict] = []
    manual_system_homes = plan.get("grammar_system_homes", {})
    for review_row in range(1, 339):
        source_row = grammar_row_to_source[review_row]
        if source_row not in grammar_by_source_row:
            raise ValueError(f"EGP row {source_row} missing from canonical B1 grammar")
        system = grammar_row_system[review_row]
        homes = grammar_system_homes.get(system, []) or manual_system_homes.get(system, [])
        if not homes:
            raise ValueError(f"grammar system {system} has no explicit C/X homes")
        for home in homes:
            family_plan(plan, home)
        grammar_records.append({**grammar_by_source_row[source_row], "review_row": review_row, "grammar_system": system, "manual_homes": homes})
    grammar_intro: dict[str, str] = {}
    grouped_grammar: dict[str, list[dict]] = defaultdict(list)
    for record in grammar_records:
        grouped_grammar[record["grammar_system"]].append(record)
    for system, values in grouped_grammar.items():
        windows = plan["grammar_system_intro"].get(system, [])
        if not windows:
            raise ValueError(f"grammar system {system} has no human-approved intro windows")
        offset = stable_offset(f"grammar:{system}", len(windows))
        for i, record in enumerate(values):
            grammar_intro[record["item_id"]] = windows[(i + offset) % len(windows)]

    word_map = load_json(WORD_MAP_PATH)
    if word_map.get("record_count") != 809:
        raise ValueError("generated B1 word-home map is missing or stale")
    word_home_by_id = {x["item_id"]: x["primary_home"] for x in word_map["records"]}
    word_by_id = {x["item_id"]: x for x in words}
    if set(word_home_by_id) != set(word_by_id):
        raise ValueError("exact B1 word-home map IDs do not match canonical B1 words")
    word_records = [{**item, "primary_home": word_home_by_id[item["item_id"]]} for item in words]
    word_intro = balanced_assignment(word_records, lambda x: x["primary_home"], lambda h: family_plan(plan, h)["introduce"], salt="word")

    records: list[dict] = []
    for item in ability_records:
        records.append(build_record("ability", item, item.get("source_text") or item["item_id"], [item["primary_home"]], ability_intro[item["item_id"]], plan, order, {"review_row": item["review_row"], "source_record_id": item["source_record_id"]}))
    for item in phrase_records:
        records.append(build_record("phrase", item, item.get("phrase") or item["item_id"], [item["primary_home"]], phrase_intro[item["item_id"]], plan, order, {"review_row": item["review_row"]}))
    for item in grammar_records:
        records.append(build_record("grammar", item, item.get("guideword") or item["item_id"], item["manual_homes"], grammar_intro[item["item_id"]], plan, order, {"review_row": item["review_row"], "egp_spreadsheet_row": int(item["source_ref"]["spreadsheet_row"]), "grammar_system": item["grammar_system"]}))
    for item in word_records:
        records.append(build_record("word", item, item.get("headword_source") or item.get("headword") or item["item_id"], [item["primary_home"]], word_intro[item["item_id"]], plan, order))

    pron_by_id = {x["item_id"]: x for x in pronunciation}
    if set(pron_by_id) != set(plan["pronunciation"]):
        raise ValueError("pronunciation lifecycle plan must exactly match the 10 B1 pronunciation items")
    for iid, lifecycle in plan["pronunciation"].items():
        item = pron_by_id[iid]
        records.append({
            "category": "pronunciation",
            "item_id": iid,
            "label": item["title"],
            "homes": [iid],
            "lifecycle": {stage: lifecycle[stage] for stage in plan["policy"]["required_stages"]},
        })

    actual_counts = Counter(x["category"] for x in records)
    if dict(actual_counts) != expected_counts:
        raise ValueError(f"expanded record count mismatch: {dict(actual_counts)} != {expected_counts}")

    required_later_stages = ["practice", "fresh_retrieval", "recycle", "consolidate", "exit_verify"]
    lifecycle_gaps = {stage: [x["item_id"] for x in records if not x["lifecycle"][stage]] for stage in required_later_stages}

    intro_counts = {lesson: Counter() for lesson in lessons}
    intro_items: dict[str, dict[str, list[str]]] = {lesson: defaultdict(list) for lesson in lessons}
    for record in records:
        intro = record["lifecycle"]["introduce"][0]
        intro_counts[intro][record["category"]] += 1
        intro_counts[intro]["total"] += 1
        intro_items[intro][record["category"]].append(record["label"])

    threshold_key = {
        "ability": "abilities_introduced", "phrase": "phrases_introduced", "grammar": "grammar_introduced",
        "word": "words_introduced", "pronunciation": "pronunciation_introduced", "total": "total_source_introductions",
    }
    overloads: list[tuple[str, str, int, int]] = []
    for lesson, counts in intro_counts.items():
        for category in ("ability", "phrase", "grammar", "word", "pronunciation", "total"):
            limit = plan["load_thresholds"][threshold_key[category]]
            if counts[category] > limit:
                overloads.append((lesson, category, counts[category], limit))

    transfer_lessons = [
        "U1-L07","U2-L07","U3-L08","U4-L09","U5-L07","U6-L07","U7-L07","U8-L07",
        "U9-L07","U10-L07","U11-L07","U12-L01","U12-L02","U12-L03","U12-L04","U12-L05",
    ]
    transfer_new = {lid: intro_counts[lid]["total"] for lid in transfer_lessons if intro_counts[lid]["total"]}

    report = [
        "# B1 Coverage Ledger Audit", "", "Status: **PROVISIONAL PRE-SEMANTIC-LOCK LIFECYCLE AUDIT**", "",
        f"Source records expanded: **{len(records)} / 1581**", "",
        "- abilities: 249", "- phrases: 175", "- grammar: 338", "- words: 809", "- pronunciation: 10",
        "- orphan source records: **0**", "",
        "This ledger schedules exact B1 source records before semantic-role lock. Stage 08/8.5 may later make lifecycle evidence role-aware; raw source rows are not automatically independent teaching objects.", "",
        "## Lifecycle completeness", "",
    ]
    for stage in required_later_stages:
        report.append(f"- records missing `{stage}`: **{len(lifecycle_gaps[stage])}**")
    report += ["", "## Introduction load by lesson", "", "| Lesson | Abilities | Phrases | Grammar | Words | Pron. | Total |", "|---|---:|---:|---:|---:|---:|---:|"]
    for lesson in lessons:
        c = intro_counts[lesson]
        report.append(f"| {lesson} | {c['ability']} | {c['phrase']} | {c['grammar']} | {c['word']} | {c['pronunciation']} | {c['total']} |")

    report += ["", "## Mechanical load result", ""]
    if overloads:
        report.append("**OVERLOAD WARNINGS FOUND — human scheduling review required; do not raise thresholds merely to pass.**")
        for lesson, category, count, limit in overloads:
            report.append(f"- {lesson}: {category} = {count} > {limit}")
    else:
        report.append("**PASS — no mechanical introduction warning threshold exceeded.**")

    report += ["", "## Transfer / integration lessons with new source introductions", ""]
    if transfer_new:
        report.append("**FAIL — designated zero-new slots received new source introductions.**")
        for lesson, count in transfer_new.items():
            report.append(f"- {lesson}: **{count}** new source records")
    else:
        report.append("**PASS — all 16 designated transfer/integration slots are zero-new.**")

    if overloads:
        report += ["", "## Overload attribution", ""]
        for lesson in sorted({x[0] for x in overloads}, key=order.__getitem__):
            report.append(f"### {lesson}")
            for category in ("ability", "phrase", "grammar", "word", "pronunciation"):
                labels = intro_items[lesson][category]
                if labels:
                    report.append(f"- **{category} ({len(labels)})**: " + "; ".join(labels))
            report.append("")

    gap_count = sum(len(v) for v in lifecycle_gaps.values())
    report += ["", "## Audit verdict", ""]
    if gap_count:
        report.append(f"**FAIL — {gap_count} lifecycle-stage gaps require manual lifecycle revision.**")
    elif transfer_new:
        report.append("**FAIL — lifecycle complete, but zero-new transfer/integration protection was violated.**")
    elif overloads:
        report.append(f"**REVIEW REQUIRED — lifecycle complete, but {len(overloads)} mechanical load warnings require a human cognitive/load critic.**")
    else:
        report.append("**PASS — exact B1 source coverage and provisional lifecycle are complete with no mechanical load warnings. Human Stage-06 load critic is still required.**")

    ledger = {
        "schema_version": 1,
        "level": "B1",
        "status": "expanded_from_manual_review_and_provisional_lifecycle_plan",
        "lesson_count": len(lessons),
        "record_counts": expected_counts,
        "records": records,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text("\n".join(report) + "\n", encoding="utf-8")
    print("\n".join(report))

    if gap_count or transfer_new:
        raise SystemExit(3)
    if overloads:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
