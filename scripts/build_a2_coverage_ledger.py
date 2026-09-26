#!/usr/bin/env python3
"""Expand reviewed A2 curriculum decisions into an auditable lifecycle ledger.

NON-SEMANTIC by design. All semantic homes and allowed introduction windows are
human-authored in Stage 01-06 artifacts. This script may only join exact source
records, balance them inside approved windows, count, validate, and report gaps.
It must fail rather than invent a capability, lexical home, grammar home, or lesson.
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
PLAN_PATH = REVIEW / "06-coverage-ledger/lifecycle-plan.json"
OVERRIDES_PATH = REVIEW / "06-coverage-ledger/manual-source-overrides.json"
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
    """Parse specs such as '2–10', '75–77, 82', or '1'."""
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
        bold = re.findall(r"\*\*([^*]+)\*\*", line)
        source = " ".join(bold) if bold else line
        for row in [int(x) for x in re.findall(r"\d+", source)]:
            if row in homes and homes[row] != current:
                raise ValueError(f"ability review row {row} mapped to multiple primary homes: {homes[row]}, {current}")
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
                raise ValueError(f"phrase review row {row} mapped to multiple primary homes: {homes[row]}, {current}")
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
            homes = list(dict.fromkeys(re.findall(r"\b[CX]\d{2}\b", line)))
            system_homes[current] = homes
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


def validate_refs(plan: dict, overrides: dict, lessons: list[str]) -> None:
    allowed = set(lessons)
    refs: list[tuple[str, str]] = []
    for group in ("capabilities", "cross_cutting", "lexical_sets", "pronunciation"):
        for home, lifecycle in plan[group].items():
            for stage, values in lifecycle.items():
                if isinstance(values, list):
                    refs.extend((f"{group}.{home}.{stage}", x) for x in values)
    for system, values in plan["grammar_system_intro"].items():
        refs.extend((f"grammar_system_intro.{system}", x) for x in values)
    refs.extend((f"grammar_review_row_intro_overrides.{k}", v) for k, v in plan.get("grammar_review_row_intro_overrides", {}).items())
    refs.extend((f"phrase_item_intro_overrides.{k}", v) for k, v in plan.get("phrase_item_intro_overrides", {}).items())
    for category, mapping in overrides.get("source_intro_overrides", {}).items():
        refs.extend((f"source_intro_overrides.{category}.{k}", v) for k, v in mapping.items())
    bad = [(where, lid) for where, lid in refs if lid not in allowed]
    if bad:
        raise ValueError(f"manual lifecycle plan references unknown lessons: {bad[:30]}")


def balanced_assignment(records: list[dict], key_fn, windows_fn, exact_overrides: dict[str, str]) -> dict[str, str]:
    assigned: dict[str, str] = {}
    groups: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        iid = record["item_id"]
        if iid in exact_overrides:
            assigned[iid] = exact_overrides[iid]
        else:
            groups[key_fn(record)].append(record)
    for key, values in groups.items():
        windows = windows_fn(key)
        if not windows:
            raise ValueError(f"no human-approved introduction window for {key}")
        for i, record in enumerate(values):
            assigned[record["item_id"]] = windows[i % len(windows)]
    return assigned


def later_lessons(plan: dict, homes: list[str], stage: str, order: dict[str, int], intro: str, *, strictly_later: bool) -> list[str]:
    intro_idx = order[intro]
    values: set[str] = set()
    for home in homes:
        lifecycle = family_plan(plan, home)
        values.update(lifecycle.get(stage, []))
    if strictly_later:
        values = {x for x in values if order[x] > intro_idx}
    else:
        values = {x for x in values if order[x] >= intro_idx}
    return sorted(values, key=order.__getitem__)


def build_record(category: str, item: dict, label: str, homes: list[str], intro: str, plan: dict, order: dict[str, int], extra: dict | None = None) -> dict:
    lifecycle = {
        "introduce": [intro],
        "practice": later_lessons(plan, homes, "practice", order, intro, strictly_later=False),
        "fresh_retrieval": later_lessons(plan, homes, "fresh_retrieval", order, intro, strictly_later=True),
        "recycle": later_lessons(plan, homes, "recycle", order, intro, strictly_later=True),
        "consolidate": later_lessons(plan, homes, "consolidate", order, intro, strictly_later=True),
        "exit_verify": later_lessons(plan, homes, "exit_verify", order, intro, strictly_later=True),
    }
    record = {
        "category": category,
        "item_id": item["item_id"],
        "label": label,
        "homes": homes,
        "lifecycle": lifecycle,
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
    overrides = load_json(OVERRIDES_PATH)
    curriculum = text(REVIEW / "05-curriculum-map/curriculum-map.md")
    lessons = lesson_ids(curriculum)
    if len(lessons) != plan["lesson_count_baseline"]:
        raise ValueError(f"lesson skeleton count mismatch: map={len(lessons)} plan={plan['lesson_count_baseline']}")
    order = {lid: i for i, lid in enumerate(lessons)}
    validate_refs(plan, overrides, lessons)

    # --- Exact source inputs ---
    abilities_all = load_json(A2 / "abilities.json")["items"]
    abilities = [x for x in abilities_all if x.get("curriculum_role") == "include_for_spine"]
    phrases = load_json(A2 / "phrases.json")["items"]
    grammar = load_json(A2 / "grammar.json")["items"]
    words = load_json(A2 / "words.json")["items"]
    pronunciation = load_json(A2 / "pronunciation.json")["items"]

    expected_counts = {"ability": 269, "phrase": 176, "grammar": 291, "word": 871, "pronunciation": 10}
    source_counts = {
        "ability": len(abilities), "phrase": len(phrases), "grammar": len(grammar),
        "word": len(words), "pronunciation": len(pronunciation),
    }
    if source_counts != expected_counts:
        raise ValueError(f"A2 source count drift: {source_counts} != {expected_counts}")

    # --- Ability exact row -> source -> canonical item -> manual home ---
    ability_aid = text(REVIEW / "01-abilities/generated/ability-review-aid.md")
    ability_row_source = parse_aid_row_ids(ability_aid, r"[^`]+")
    ability_row_home = parse_ability_homes(text(REVIEW / "01-abilities/final-capability-map.md"))
    if set(ability_row_source) != set(range(1, 270)):
        raise ValueError("ability review aid does not expose exact rows 1..269")
    if set(ability_row_home) != set(range(1, 270)):
        missing = sorted(set(range(1, 270)) - set(ability_row_home))
        raise ValueError(f"required ability rows missing manual home: {missing[:40]}")
    ability_by_source = {x["source_record_id"]: x for x in abilities}
    ability_records: list[dict] = []
    for row in range(1, 270):
        source_id = ability_row_source[row]
        if source_id not in ability_by_source:
            raise ValueError(f"ability aid source row not found in required inventory: row={row} source={source_id}")
        item = ability_by_source[source_id]
        ability_records.append({**item, "review_row": row, "primary_home": ability_row_home[row]})
    ability_intro = balanced_assignment(
        ability_records,
        lambda x: x["primary_home"],
        lambda home: family_plan(plan, home)["introduce"],
        overrides.get("source_intro_overrides", {}).get("ability", {}),
    )

    # --- Phrase exact review row -> canonical ID -> manual home ---
    phrase_row_id = parse_aid_row_ids(text(REVIEW / "02-phrases/generated/phrase-review-aid.md"), r"oxford\.phrase\.online\.\d+")
    phrase_row_home = parse_phrase_homes(text(REVIEW / "02-phrases/phrase-review.md"))
    if set(phrase_row_id) != set(range(1, 177)) or set(phrase_row_home) != set(range(1, 177)):
        raise ValueError(
            f"phrase review coverage mismatch: aid_missing={sorted(set(range(1,177))-set(phrase_row_id))[:20]} "
            f"home_missing={sorted(set(range(1,177))-set(phrase_row_home))[:20]}"
        )
    phrase_by_id = {x["item_id"]: x for x in phrases}
    phrase_records: list[dict] = []
    for row in range(1, 177):
        iid = phrase_row_id[row]
        phrase_records.append({**phrase_by_id[iid], "review_row": row, "primary_home": phrase_row_home[row]})
    phrase_exact = dict(plan.get("phrase_item_intro_overrides", {}))
    phrase_exact.update(overrides.get("source_intro_overrides", {}).get("phrase", {}))
    unknown_phrase_overrides = sorted(set(phrase_exact) - set(phrase_by_id))
    if unknown_phrase_overrides:
        raise ValueError(f"unknown phrase intro override IDs: {unknown_phrase_overrides}")
    phrase_intro = balanced_assignment(
        phrase_records,
        lambda x: x["primary_home"],
        lambda home: family_plan(plan, home)["introduce"],
        phrase_exact,
    )

    # --- Grammar review rows -> G systems -> exact EGP source records ---
    grammar_review_index_to_egp_row = parse_grammar_aid(text(REVIEW / "03-grammar/generated/grammar-review-aid.md"))
    grammar_review_system, grammar_system_homes = parse_grammar_systems(text(REVIEW / "03-grammar/grammar-review.md"))
    expected_review_rows = set(range(1, 292))
    if set(grammar_review_index_to_egp_row) != expected_review_rows:
        raise ValueError("grammar review aid does not expose exact review rows 1..291")
    if set(grammar_review_system) != expected_review_rows:
        missing = sorted(expected_review_rows - set(grammar_review_system))
        raise ValueError(f"grammar review rows missing G-system: {missing[:40]}")
    grammar_by_egp_row = {int(x["source_ref"]["spreadsheet_row"]): x for x in grammar}
    grammar_records: list[dict] = []
    system_manual_homes = overrides.get("grammar_system_homes", {})
    for review_row in range(1, 292):
        egp_row = grammar_review_index_to_egp_row[review_row]
        if egp_row not in grammar_by_egp_row:
            raise ValueError(f"EGP row {egp_row} from review aid missing canonical A2 grammar item")
        system = grammar_review_system[review_row]
        homes = grammar_system_homes.get(system, []) or system_manual_homes.get(system, [])
        if not homes:
            raise ValueError(f"grammar system {system} has no explicit manual C/X lifecycle homes")
        for home in homes:
            family_plan(plan, home)  # fail if unknown
        grammar_records.append({
            **grammar_by_egp_row[egp_row],
            "review_row": review_row,
            "grammar_system": system,
            "manual_homes": homes,
        })
    grammar_intro: dict[str, str] = {}
    grouped_grammar: dict[str, list[dict]] = defaultdict(list)
    grammar_source_override = overrides.get("source_intro_overrides", {}).get("grammar", {})
    review_overrides = {int(k): v for k, v in plan.get("grammar_review_row_intro_overrides", {}).items()}
    for record in grammar_records:
        iid = record["item_id"]
        rr = record["review_row"]
        if iid in grammar_source_override:
            grammar_intro[iid] = grammar_source_override[iid]
        elif rr in review_overrides:
            grammar_intro[iid] = review_overrides[rr]
        else:
            grouped_grammar[record["grammar_system"]].append(record)
    for system, records in grouped_grammar.items():
        windows = plan["grammar_system_intro"].get(system, [])
        if not windows:
            raise ValueError(f"grammar system {system} has no manual introduction windows")
        for i, record in enumerate(records):
            grammar_intro[record["item_id"]] = windows[i % len(windows)]

    # --- Exact frozen word home map ---
    word_map = load_json(WORD_MAP_PATH)
    if word_map.get("record_count") != 871:
        raise ValueError("generated A2 word-home map is missing or stale")
    word_home_by_id = {x["item_id"]: x["primary_home"] for x in word_map["records"]}
    word_by_id = {x["item_id"]: x for x in words}
    if set(word_home_by_id) != set(word_by_id):
        raise ValueError("exact word-home map IDs do not match canonical A2 words")
    word_records = [{**item, "primary_home": word_home_by_id[item["item_id"]]} for item in words]
    word_intro = balanced_assignment(
        word_records,
        lambda x: x["primary_home"],
        lambda home: family_plan(plan, home)["introduce"],
        overrides.get("source_intro_overrides", {}).get("word", {}),
    )

    # --- Expand all categories ---
    records: list[dict] = []
    for item in ability_records:
        homes = [item["primary_home"]]
        records.append(build_record(
            "ability", item, item.get("source_text") or item["item_id"], homes,
            ability_intro[item["item_id"]], plan, order,
            {"review_row": item["review_row"], "source_record_id": item["source_record_id"]},
        ))
    for item in phrase_records:
        homes = [item["primary_home"]]
        records.append(build_record(
            "phrase", item, item.get("phrase") or item["item_id"], homes,
            phrase_intro[item["item_id"]], plan, order,
            {"review_row": item["review_row"]},
        ))
    for item in grammar_records:
        records.append(build_record(
            "grammar", item, item.get("guideword") or item["item_id"], item["manual_homes"],
            grammar_intro[item["item_id"]], plan, order,
            {
                "review_row": item["review_row"],
                "egp_spreadsheet_row": int(item["source_ref"]["spreadsheet_row"]),
                "grammar_system": item["grammar_system"],
            },
        ))
    for item in word_records:
        homes = [item["primary_home"]]
        records.append(build_record(
            "word", item, item.get("headword_source") or item.get("headword") or item["item_id"], homes,
            word_intro[item["item_id"]], plan, order,
        ))

    pron_by_id = {x["item_id"]: x for x in pronunciation}
    if set(pron_by_id) != set(plan["pronunciation"]):
        raise ValueError("pronunciation lifecycle plan must exactly match the 10 A2 source items")
    for iid, lifecycle in plan["pronunciation"].items():
        item = pron_by_id[iid]
        intro = lifecycle["introduce"][0]
        record = {
            "category": "pronunciation",
            "item_id": iid,
            "label": item["title"],
            "homes": [iid],
            "lifecycle": {
                "introduce": lifecycle["introduce"],
                "practice": lifecycle["practice"],
                "fresh_retrieval": lifecycle["fresh_retrieval"],
                "recycle": lifecycle["recycle"],
                "consolidate": lifecycle["consolidate"],
                "exit_verify": lifecycle["exit_verify"],
            },
        }
        # Pronunciation is explicit, but still require fresh evidence after introduction.
        if any(order[x] <= order[intro] for x in record["lifecycle"]["fresh_retrieval"]):
            raise ValueError(f"pronunciation fresh retrieval not later than introduction: {iid}")
        records.append(record)

    actual_counts = Counter(x["category"] for x in records)
    if dict(actual_counts) != expected_counts:
        raise ValueError(f"expanded record count mismatch: {dict(actual_counts)} != {expected_counts}")

    required_stages = ["practice", "fresh_retrieval", "recycle", "consolidate", "exit_verify"]
    lifecycle_gaps: dict[str, list[str]] = {}
    for stage in required_stages:
        lifecycle_gaps[stage] = [x["item_id"] for x in records if not x["lifecycle"][stage]]

    intro_counts = {lesson: Counter() for lesson in lessons}
    intro_items: dict[str, dict[str, list[str]]] = {lesson: defaultdict(list) for lesson in lessons}
    for record in records:
        intro = record["lifecycle"]["introduce"][0]
        intro_counts[intro][record["category"]] += 1
        intro_counts[intro]["total"] += 1
        intro_items[intro][record["category"]].append(record["label"])

    threshold_key = {
        "ability": "abilities_introduced", "phrase": "phrases_introduced",
        "grammar": "grammar_introduced", "word": "words_introduced",
        "pronunciation": "pronunciation_introduced", "total": "total_source_introductions",
    }
    overloads: list[tuple[str, str, int, int]] = []
    for lesson, counts in intro_counts.items():
        for category in ("ability", "phrase", "grammar", "word", "pronunciation", "total"):
            count = counts[category]
            limit = plan["load_thresholds"][threshold_key[category]]
            if count > limit:
                overloads.append((lesson, category, count, limit))

    transfer_lessons = [
        "U1-L07","U2-L07","U3-L07","U4-L07","U5-L07","U6-L08",
        "U7-L07","U8-L06","U9-L06","U10-L07","U11-L07",
        "U12-L04","U12-L05","U12-L06","U12-L07",
    ]
    transfer_new = {lid: intro_counts[lid]["total"] for lid in transfer_lessons if intro_counts[lid]["total"]}

    report: list[str] = [
        "# A2 Coverage Ledger Audit",
        "",
        "Status: **PROVISIONAL PRE-SEMANTIC-LOCK LIFECYCLE AUDIT**",
        "",
        f"Source records expanded: **{len(records)} / 1617**",
        "",
        "- abilities: 269",
        "- phrases: 176",
        "- grammar: 291",
        "- words: 871",
        "- pronunciation: 10",
        "- orphan source records: **0**",
        "",
        "This ledger is intentionally pre-semantic-lock: every source record is scheduled, but Stage 08/8.5 may later make lifecycle evidence role-aware (productive/receptive/formulaic/embedded).",
        "",
        "## Lifecycle completeness",
        "",
    ]
    for stage in required_stages:
        report.append(f"- records missing `{stage}`: **{len(lifecycle_gaps[stage])}**")
    report += [
        "",
        "## Introduction load by lesson",
        "",
        "| Lesson | Abilities | Phrases | Grammar | Words | Pron. | Total |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for lesson in lessons:
        c = intro_counts[lesson]
        report.append(
            f"| {lesson} | {c['ability']} | {c['phrase']} | {c['grammar']} | {c['word']} | {c['pronunciation']} | {c['total']} |"
        )

    report += ["", "## Mechanical load result", ""]
    if overloads:
        report.append("**OVERLOADS FOUND — human scheduling revision required; do not raise thresholds merely to pass.**")
        for lesson, category, count, limit in overloads:
            report.append(f"- {lesson}: {category} = {count} > {limit}")
    else:
        report.append("**PASS — no mechanical introduction threshold exceeded.**")

    report += ["", "## Transfer / evidence lessons with new source introductions", ""]
    if transfer_new:
        report.append("These are critic flags, not automatically errors. A lesson labelled transfer should normally trend toward zero-new content.")
        for lesson, count in transfer_new.items():
            report.append(f"- {lesson}: **{count}** new source records")
    else:
        report.append("**PASS — all designated transfer/evidence lessons are zero-new.**")

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
        report.append(f"**FAIL — {gap_count} lifecycle-stage gaps require manual plan revision.**")
    elif overloads:
        report.append(f"**FAIL — lifecycle complete, but {len(overloads)} introduction-load threshold violations require manual rebalancing.**")
    else:
        report.append("**PASS — exact source coverage and provisional lifecycle are complete with no mechanical overloads. Human load critic is still required before Stage 07.**")

    ledger = {
        "schema_version": 1,
        "level": "A2",
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

    if gap_count:
        raise SystemExit(3)
    if overloads:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
