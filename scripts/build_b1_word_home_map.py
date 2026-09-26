#!/usr/bin/env python3
"""Expand reviewed B1 lexical-home decisions to exact source-record IDs.

Human semantic decisions live in
`curriculum/levels/b1/design-review/04-words/word-home-decisions.json`.
This script only validates the frozen inventory, resolves exact unique headword
labels, assigns the explicitly reviewed remainder to LX-GENERAL, and emits
audit artifacts. It does not infer semantic homes or mastery roles.
"""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B1 = ROOT / "curriculum/levels/b1"
REVIEW = B1 / "design-review/04-words"
SOURCE = B1 / "words.json"
DECISIONS = REVIEW / "word-home-decisions.json"
OUT_MAP = REVIEW / "generated/word-home-map.json"
OUT_REPORT = REVIEW / "generated/word-home-report.md"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob_sha(path: Path) -> str:
    payload = path.read_bytes()
    header = f"blob {len(payload)}\0".encode("utf-8")
    return hashlib.sha1(header + payload).hexdigest()


def norm(value: str) -> str:
    return " ".join(str(value).casefold().strip().split())


def main() -> None:
    source = load(SOURCE)
    decisions = load(DECISIONS)
    items = source.get("items", [])

    expected_count = decisions["policy"]["human_reviewed_inventory_count"]
    if len(items) != expected_count:
        raise ValueError(f"B1 word count changed: expected={expected_count} actual={len(items)}")

    actual_blob = git_blob_sha(SOURCE)
    expected_blob = decisions["expected_git_blob_sha"]
    if actual_blob != expected_blob:
        raise ValueError(
            "B1 words.json changed after human review; renewed manual review required: "
            f"expected_blob={expected_blob} actual_blob={actual_blob}"
        )

    by_id = {x["item_id"]: x for x in items}
    by_headword = defaultdict(list)
    for item in items:
        by_headword[norm(item["headword"])].append(item["item_id"])

    assignments: dict[str, str] = {}
    decision_source: dict[str, str] = {}
    errors: list[str] = []

    for iid, home in decisions.get("exact_item_overrides", {}).items():
        if iid not in by_id:
            errors.append(f"unknown exact item override: {iid}")
            continue
        assignments[iid] = home
        decision_source[iid] = "exact_item_override"

    seen_labels: dict[str, str] = {}
    for home, labels in decisions.get("explicit_headword_homes", {}).items():
        for raw in labels:
            label = norm(raw)
            previous = seen_labels.get(label)
            if previous and previous != home:
                errors.append(f"headword listed in multiple homes: {raw!r} -> {previous}, {home}")
                continue
            seen_labels[label] = home
            ids = by_headword.get(label, [])
            if not ids:
                errors.append(f"explicit headword not in frozen B1 inventory: {raw!r} ({home})")
                continue
            unresolved = [iid for iid in ids if iid not in assignments]
            if len(ids) > 1:
                if unresolved:
                    errors.append(
                        f"ambiguous headword requires exact item overrides: {raw!r} -> {ids}; "
                        f"unresolved={unresolved}"
                    )
                continue
            iid = ids[0]
            if iid in assignments and assignments[iid] != home:
                errors.append(
                    f"conflicting assignment for {iid}/{raw!r}: "
                    f"{assignments[iid]} vs {home}"
                )
                continue
            assignments[iid] = home
            decision_source[iid] = "explicit_headword_home"

    if errors:
        raise ValueError("B1 manual word-home decisions invalid:\n- " + "\n- ".join(errors))

    default_home = decisions["policy"]["default_home"]
    for item in items:
        iid = item["item_id"]
        if iid not in assignments:
            assignments[iid] = default_home
            decision_source[iid] = "frozen_reviewed_remainder"

    if set(assignments) != set(by_id):
        missing = sorted(set(by_id) - set(assignments))
        extra = sorted(set(assignments) - set(by_id))
        raise ValueError(f"word-home coverage mismatch: missing={missing[:20]} extra={extra[:20]}")

    counts = Counter(assignments.values())
    general = [x for x in items if assignments[x["item_id"]] == default_home]

    OUT_MAP.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "level": "B1",
        "status": "expanded_from_frozen_manual_word_home_policy",
        "source_git_blob_sha": actual_blob,
        "record_count": len(items),
        "default_home": default_home,
        "home_counts": dict(sorted(counts.items())),
        "records": [
            {
                "item_id": item["item_id"],
                "headword": item["headword"],
                "part_of_speech": item.get("part_of_speech"),
                "qualifier": item.get("qualifier"),
                "primary_home": assignments[item["item_id"]],
                "decision_source": decision_source[item["item_id"]],
            }
            for item in items
        ],
    }
    OUT_MAP.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# B1 Exact Word-Home Expansion Audit",
        "",
        "Status: **GENERATED FROM FROZEN MANUAL REVIEW POLICY — NON-SEMANTIC EXPANSION**",
        "",
        f"- frozen source blob: `{actual_blob}`",
        f"- source records: **{len(items)} / {expected_count}**",
        f"- exact primary homes assigned: **{len(assignments)}**",
        f"- explicit headword / exact-ID decisions: **{len(items) - len(general)}**",
        f"- intentional reviewed remainder (`{default_home}`): **{len(general)}**",
        "- orphans: **0**",
        "",
        "## Home counts",
        "",
        "| Home | Records |",
        "|---|---:|",
    ]
    for home, count in sorted(counts.items()):
        lines.append(f"| {home} | {count} |")

    lines += [
        "",
        f"## `{default_home}` critic queue",
        "",
        "These records were manually reviewed in Stage 04 and intentionally use the frozen general",
        "factual/descriptive/high-frequency home because no stronger single primary semantic home was",
        "recorded. This exact list remains visible for human critic before the lifecycle ledger is locked.",
        "",
        "| Item ID | Headword | POS | Qualifier |",
        "|---|---|---|---|",
    ]
    for item in general:
        lines.append(
            f"| `{item['item_id']}` | {item['headword']} | {item.get('part_of_speech') or ''} | "
            f"{item.get('qualifier') or ''} |"
        )
    lines += [
        "",
        "## Integrity result",
        "",
        "**PASS — every frozen B1 word record has exactly one primary instructional home.**",
        "",
    ]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:50]))


if __name__ == "__main__":
    main()
