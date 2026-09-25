#!/usr/bin/env python3
"""Generate compact, non-authoritative review aids for manual level design.

This script NEVER makes semantic/curriculum decisions. It only projects exact
source records into compact Markdown so a human can read/review them efficiently.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEVELS = ("a2", "b1", "b2", "c1", "c2")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def esc(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def build_ability_aid(level: str) -> None:
    level_dir = ROOT / "curriculum" / "levels" / level
    data = load_json(level_dir / "abilities.json")
    required = [x for x in data.get("items", []) if x.get("curriculum_role") == "include_for_spine"]

    out_dir = level_dir / "design-review" / "01-abilities" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "ability-review-aid.md"

    lines = [
        f"# {level.upper()} Required Ability Review Aid",
        "",
        "Status: **GENERATED REVIEW AID — NON-AUTHORITATIVE**  ",
        "Purpose: compact projection of exact source records for manual curriculum review.  ",
        "Rule: this file makes **no** KEEP/MERGE/SPLIT/SUPPORTING or capability decisions.",
        "",
        f"Required records: **{len(required)}**",
        "",
        "| # | Source record ID | Mode | Skill | Function tags | Source ability |",
        "|---:|---|---|---|---|---|",
    ]
    for i, item in enumerate(required, 1):
        lines.append(
            "| {i} | `{sid}` | {mode} | {skill} | {func} | {text} |".format(
                i=i,
                sid=esc(item.get("source_record_id", item.get("item_id", ""))),
                mode=esc(", ".join(item.get("mode_codes", []))),
                skill=esc(", ".join(item.get("skill_codes", []))),
                func=esc(", ".join(item.get("function_codes", []))),
                text=esc(item.get("source_text", "")),
            )
        )

    lines.extend([
        "",
        "## Integrity",
        "",
        f"- Manifest/source required count expected: **{data.get('counts', {}).get('required_items')}**",
        f"- Projected required count: **{len(required)}**",
        "- IDs and texts are copied from `abilities.json`; no semantic inference is performed.",
        "",
    ])
    out.write_text("\n".join(lines), encoding="utf-8")


def build_phrase_aid(level: str) -> None:
    level_dir = ROOT / "curriculum" / "levels" / level
    data = load_json(level_dir / "phrases.json")
    items = data.get("items", [])

    out_dir = level_dir / "design-review" / "02-phrases" / "generated"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "phrase-review-aid.md"

    lines = [
        f"# {level.upper()} Phrase Review Aid",
        "",
        "Status: **GENERATED REVIEW AID — NON-AUTHORITATIVE**  ",
        "Purpose: compact projection of exact phrase records for manual curriculum review.  ",
        "Rule: this file makes **no** capability-home, productivity, or semantic-role decisions.",
        "",
        f"Phrase records: **{len(items)}**",
        "",
        "| # | Item ID | Phrase |",
        "|---:|---|---|",
    ]
    for i, item in enumerate(items, 1):
        lines.append(
            "| {i} | `{iid}` | {phrase} |".format(
                i=i,
                iid=esc(item.get("item_id", "")),
                phrase=esc(item.get("phrase", "")),
            )
        )

    lines.extend([
        "",
        "## Integrity",
        "",
        f"- Projected phrase count: **{len(items)}**",
        "- IDs and phrase text are copied from `phrases.json`; no semantic inference is performed.",
        "",
    ])
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    for level in LEVELS:
        level_dir = ROOT / "curriculum" / "levels" / level
        if (level_dir / "abilities.json").exists():
            build_ability_aid(level)
        if (level_dir / "phrases.json").exists():
            build_phrase_aid(level)


if __name__ == "__main__":
    main()
