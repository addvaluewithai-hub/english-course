#!/usr/bin/env python3
"""Expand reviewed A1 curriculum decisions into an auditable source-record lifecycle ledger.

This script is deliberately non-semantic. It parses the manual review artifacts and the
manual lifecycle plan; it must fail rather than invent a home for an unmapped source item.
"""
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
A1 = ROOT / "curriculum/levels/a1"
REVIEW = A1 / "design-review"
PLAN_PATH = REVIEW / "06-coverage-ledger/lifecycle-plan.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def canon(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = value.replace("’", "'").replace("…", "...")
    return re.sub(r"[^a-z0-9']+", "", value)


def lesson_ids(curriculum: str) -> list[str]:
    seen = []
    for lid in re.findall(r"\|\s*(U\d+-L\d+)\s*\|", curriculum):
        if lid not in seen:
            seen.append(lid)
    return seen


def all_plan_lesson_refs(plan: dict):
    for family_group in ("capabilities", "cross_cutting", "lexical_sets", "pronunciation"):
        for family in plan[family_group].values():
            for values in family.values():
                if isinstance(values, list):
                    yield from values
    yield from plan["phrase_intro"].keys()
    yield from plan["grammar_intro"].keys()


def invert_exact(mapping: dict[str, list], expected: set, label: str):
    inverted = {}
    duplicates = []
    for lesson, values in mapping.items():
        for value in values:
            if value in inverted:
                duplicates.append(value)
            inverted[value] = lesson
    missing = sorted(expected - set(inverted), key=str)
    extra = sorted(set(inverted) - expected, key=str)
    if duplicates or missing or extra:
        raise ValueError(
            f"{label} intro map invalid: duplicates={duplicates[:20]} "
            f"missing={missing[:40]} extra={extra[:20]}"
        )
    return inverted


def parse_phrase_homes(markdown: str) -> dict[str, list[str]]:
    homes = defaultdict(list)
    current = None
    for line in markdown.splitlines():
        m = re.match(r"##\s+(C\d{2}|X\d{2})\b", line)
        if m:
            current = m.group(1)
            continue
        m = re.match(r"-\s+`(oxford\.phrase\.online\.\d+)`", line)
        if m and current:
            homes[m.group(1)].append(current)
    return dict(homes)


def parse_grammar_review(markdown: str) -> dict[int, str]:
    rows = {}
    for line in markdown.splitlines():
        if not line.startswith("|") or "EGP row" in line or line.startswith("|---"):
            continue
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) < 4 or not parts[0].isdigit() or not parts[1].isdigit():
            continue
        rows[int(parts[1])] = parts[3]
    return rows


def parse_ability_sources(markdown: str) -> dict[int, str]:
    result = {}
    rx = re.compile(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|")
    for line in markdown.splitlines():
        m = rx.match(line)
        if m:
            result[int(m.group(1))] = m.group(2)
    return result


def parse_ability_homes(markdown: str) -> dict[int, list[str]]:
    homes = defaultdict(list)
    current = None
    for line in markdown.splitlines():
        m = re.match(r"##\s+(C\d{2}|X\d{2})\b", line)
        if m:
            current = m.group(1)
            continue
        if not current or ("Ability-review" not in line and "Supporting" not in line):
            continue
        for block in re.findall(r"\*\*([^*]+)\*\*", line):
            for number in re.findall(r"\d+", block):
                row = int(number)
                if current not in homes[row]:
                    homes[row].append(current)
    return dict(homes)


def parse_word_memberships(markdown: str, words: list[dict], overrides: dict) -> dict[str, list[str]]:
    index = defaultdict(set)
    for item in words:
        for field in (item.get("headword"), item.get("headword_source")):
            if field:
                index[canon(field)].add(item["item_id"])

    memberships = defaultdict(set)
    current = None
    for line in markdown.splitlines():
        m = re.match(r"##\s+(L\d{2})\b", line)
        if m:
            current = m.group(1)
        elif line.startswith("# Remaining general high-frequency lexical material"):
            current = "LX-GENERAL"
        elif line.startswith("## 3. Grammar/function vocabulary"):
            current = "X10"
        elif line.startswith("# Required lexical/content sets"):
            current = None

        if not current:
            continue
        for token in re.findall(r"`([^`]+)`", line):
            for item_id in index.get(canon(token), set()):
                memberships[item_id].add(current)

    for home, labels in overrides.items():
        for label in labels:
            matches = index.get(canon(label), set())
            for item_id in matches:
                memberships[item_id].add(home)

    return {key: sorted(values) for key, values in memberships.items()}


def family(plan: dict, home: str) -> dict:
    if home.startswith("C"):
        return plan["capabilities"][home]
    if home.startswith("X"):
        return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]


def union_stage(plan: dict, homes: list[str], stage: str, order: dict, after: int | None = None):
    values = set()
    for home in homes:
        values.update(family(plan, home).get(stage, []))
    return sorted(
        (v for v in values if after is None or order[v] >= after),
        key=order.__getitem__,
    )


def balanced_assign(items: list, homes_by_id: dict, plan: dict, order: dict) -> dict:
    primary = {}
    groups = defaultdict(list)
    for item in items:
        iid = item["item_id"]
        homes = homes_by_id[iid]
        chosen = min(homes, key=lambda h: min(order[x] for x in family(plan, h)["introduce"]))
        primary[iid] = chosen
        groups[chosen].append(iid)

    assigned = {}
    for home, ids in groups.items():
        windows = sorted(family(plan, home)["introduce"], key=order.__getitem__)
        for idx, iid in enumerate(ids):
            assigned[iid] = windows[idx % len(windows)]
    return assigned, primary


def build_record(category, iid, label, homes, intro, plan, order):
    intro_idx = order[intro]
    practice = union_stage(plan, homes, "practice", order, intro_idx)
    fresh = union_stage(plan, homes, "fresh_retrieval", order, intro_idx + 1)
    recycle = union_stage(plan, homes, "recycle", order, intro_idx + 1)
    consolidate = union_stage(plan, homes, "consolidate", order, intro_idx + 1)
    exit_verify = union_stage(plan, homes, "exit_verify", order, intro_idx + 1)
    return {
        "category": category,
        "item_id": iid,
        "label": label,
        "homes": homes,
        "lifecycle": {
            "introduce": [intro],
            "practice": practice,
            "fresh_retrieval": fresh,
            "recycle": recycle,
            "consolidate": consolidate,
            "exit_verify": exit_verify,
        },
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    plan = load_json(PLAN_PATH)
    curriculum = text(REVIEW / "05-curriculum-map/curriculum-map.md")
    lessons = lesson_ids(curriculum)
    order = {lesson: idx for idx, lesson in enumerate(lessons)}
    bad_refs = sorted(set(all_plan_lesson_refs(plan)) - set(lessons))
    if len(lessons) != 62 or bad_refs:
        raise ValueError(f"lesson skeleton invalid: count={len(lessons)} bad_refs={bad_refs}")

    abilities = load_json(A1 / "abilities.json")["items"]
    phrases = load_json(A1 / "phrases.json")["items"]
    grammar = load_json(A1 / "grammar.json")["items"]
    words = load_json(A1 / "words.json")["items"]
    pronunciation = load_json(A1 / "pronunciation.json")["items"]

    phrase_homes = parse_phrase_homes(text(REVIEW / "02-phrases/phrase-review.md"))
    phrase_ids = {x["item_id"] for x in phrases}
    if set(phrase_homes) != phrase_ids:
        raise ValueError(f"phrase home mismatch: missing={sorted(phrase_ids-set(phrase_homes))[:20]}")
    phrase_intro = invert_exact(plan["phrase_intro"], phrase_ids, "phrase")

    grammar_review = parse_grammar_review(text(REVIEW / "03-grammar/grammar-review.md"))
    grammar_rows = {int(x["source_ref"]["spreadsheet_row"]) for x in grammar}
    grammar_intro = invert_exact(plan["grammar_intro"], grammar_rows, "grammar")
    if set(grammar_review) != grammar_rows:
        raise ValueError(f"grammar review mismatch: missing={sorted(grammar_rows-set(grammar_review))[:20]}")

    ability_sources = parse_ability_sources(text(REVIEW / "01-abilities/manual-review-log.md"))
    ability_homes_by_row = parse_ability_homes(text(REVIEW / "01-abilities/final-capability-map.md"))
    ability_ids = {x["item_id"] for x in abilities}
    if set(ability_sources.values()) != ability_ids:
        raise ValueError("ability manual log does not exactly match abilities.json")
    missing_ability_homes = sorted(set(ability_sources) - set(ability_homes_by_row))
    if missing_ability_homes:
        raise ValueError(f"abilities without final homes: {missing_ability_homes}")
    ability_homes = {ability_sources[row]: ability_homes_by_row[row] for row in ability_sources}
    ability_intro, _ = balanced_assign(abilities, ability_homes, plan, order)

    word_homes = parse_word_memberships(
        text(REVIEW / "04-words/word-review.md"), words, plan["word_home_overrides"]
    )
    word_ids = {x["item_id"] for x in words}
    uncovered_words = [x for x in words if x["item_id"] not in word_homes]
    if uncovered_words:
        labels = [f"{x['item_id']}::{x['headword_source']}" for x in uncovered_words]
        raise ValueError("words without manual lexical home:\n" + "\n".join(labels))
    if set(word_homes) != word_ids:
        raise ValueError("word home expansion mismatch")
    word_intro, _ = balanced_assign(words, word_homes, plan, order)

    records = []
    ability_by_id = {x["item_id"]: x for x in abilities}
    for iid in sorted(ability_ids):
        item = ability_by_id[iid]
        label = item.get("text") or item.get("can_do") or iid
        records.append(build_record("ability", iid, label, ability_homes[iid], ability_intro[iid], plan, order))

    phrase_by_id = {x["item_id"]: x for x in phrases}
    for iid in sorted(phrase_ids):
        item = phrase_by_id[iid]
        label = item.get("phrase") or item.get("text") or iid
        records.append(build_record("phrase", iid, label, phrase_homes[iid], phrase_intro[iid], plan, order))

    grammar_by_row = {int(x["source_ref"]["spreadsheet_row"]): x for x in grammar}
    for row in sorted(grammar_rows):
        item = grammar_by_row[row]
        homes = re.findall(r"\b[CX]\d{2}\b", grammar_review[row])
        homes += plan["grammar_home_overrides"].get(str(row), [])
        if "core" in grammar_review[row].lower() and "X10" not in homes:
            homes.append("X10")
        homes = list(dict.fromkeys(homes))
        if not homes:
            raise ValueError(f"grammar row {row} has no explicit manual home")
        records.append(build_record(
            "grammar", item["item_id"], item.get("guideword") or str(row), homes,
            grammar_intro[row], plan, order
        ))

    word_by_id = {x["item_id"]: x for x in words}
    for iid in sorted(word_ids):
        item = word_by_id[iid]
        records.append(build_record(
            "word", iid, item["headword_source"], word_homes[iid], word_intro[iid], plan, order
        ))

    pron_by_id = {x["item_id"]: x for x in pronunciation}
    if set(pron_by_id) != set(plan["pronunciation"]):
        raise ValueError("pronunciation plan does not exactly match source inventory")
    for iid, pplan in plan["pronunciation"].items():
        intro = pplan["introduce"][0]
        records.append(build_record("pronunciation", iid, pron_by_id[iid]["title"], [iid], intro,
                                    {**plan, "lexical_sets": {**plan["lexical_sets"], iid: pplan}}, order))

    no_fresh = [r["item_id"] for r in records if not r["lifecycle"]["fresh_retrieval"]]
    no_exit = [r["item_id"] for r in records if not r["lifecycle"]["exit_verify"]]
    if no_fresh or no_exit:
        raise ValueError(f"lifecycle gaps: no_fresh={no_fresh[:30]} no_exit={no_exit[:30]}")

    intro_counts = {lesson: defaultdict(int) for lesson in lessons}
    for record in records:
        lesson = record["lifecycle"]["introduce"][0]
        intro_counts[lesson][record["category"]] += 1
        intro_counts[lesson]["total"] += 1

    overloads = []
    threshold_key = {
        "word": "words_introduced", "phrase": "phrases_introduced", "grammar": "grammar_introduced",
        "ability": "abilities_introduced", "pronunciation": "pronunciation_introduced", "total": "total_source_introductions"
    }
    for lesson, counts in intro_counts.items():
        for category, count in counts.items():
            limit = plan["load_thresholds"][threshold_key[category]]
            if count > limit:
                overloads.append((lesson, category, count, limit))

    expected_counts = {"ability": 119, "phrase": 199, "grammar": 109, "word": 900, "pronunciation": 10}
    actual_counts = defaultdict(int)
    for record in records:
        actual_counts[record["category"]] += 1
    if dict(actual_counts) != expected_counts:
        raise ValueError(f"record count mismatch: {dict(actual_counts)}")

    report_lines = [
        "# A1 Coverage Ledger Audit",
        "",
        f"Source records expanded: **{len(records)}**",
        "",
        "- abilities: 119",
        "- phrases: 199",
        "- grammar: 109",
        "- words: 900",
        "- pronunciation: 10",
        "- orphan records: 0",
        "- records without later fresh retrieval: 0",
        "- records without exit verification: 0",
        "",
        "## Introduction load by lesson",
        "",
        "| Lesson | Abilities | Phrases | Grammar | Words | Pron. | Total |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for lesson in lessons:
        c = intro_counts[lesson]
        report_lines.append(
            f"| {lesson} | {c['ability']} | {c['phrase']} | {c['grammar']} | {c['word']} | {c['pronunciation']} | {c['total']} |"
        )
    report_lines += ["", "## Threshold result", ""]
    if overloads:
        report_lines.append("**OVERLOADS FOUND — manual scheduling revision required.**")
        for lesson, category, count, limit in overloads:
            report_lines.append(f"- {lesson}: {category}={count} > {limit}")
    else:
        report_lines.append("**PASS — no introduction-load threshold exceeded.**")

    report = "\n".join(report_lines) + "\n"
    ledger = {
        "schema_version": 1,
        "level": "A1",
        "status": "expanded_from_manual_review_and_lifecycle_plan",
        "lesson_count": len(lessons),
        "record_counts": expected_counts,
        "records": records,
    }
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    print(report)
    if overloads:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
