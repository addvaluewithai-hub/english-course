#!/usr/bin/env python3
"""Export the locked A1 lexical/chunk curriculum for learner apps.

This deliberately exports only course-authored curriculum fields. Publisher/source
snapshots, source_refs, Oxford headword reconciliation, and review internals stay in
this private curriculum repository. The CI contract verifies the locked A1 counts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LEXICAL_PATH = ROOT / "data/reviewed/a1-lexical-chunk-ownership-v1.json"
SCOPE_PATH = ROOT / "data/reviewed/a1-scope-and-sequence-v1.json"
DEFAULT_OUTPUT = ROOT / "dist/app/a1-vocab-catalog-v1.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def lesson_lookup(scope: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    lookup: dict[str, dict[str, Any]] = {}
    units: list[dict[str, Any]] = []

    for unit in scope["units"]:
        exported_lessons: list[dict[str, Any]] = []
        for lesson in unit["lessons"]:
            summary = {
                "lessonId": lesson["lesson_id"],
                "sequence": lesson["global_sequence_position"],
                "title": lesson["title"],
                "outcome": lesson["outcome_statement"],
                "unitId": unit["unit_id"],
                "unitNumber": unit["unit_number"],
            }
            exported_lessons.append({
                "lessonId": summary["lessonId"],
                "sequence": summary["sequence"],
                "title": summary["title"],
                "outcome": summary["outcome"],
            })
            for owner_id in [lesson["final_owner_id"], *lesson.get("source_candidate_ids", [])]:
                lookup.setdefault(owner_id, summary)

        units.append({
            "unitId": unit["unit_id"],
            "unitNumber": unit["unit_number"],
            "title": unit["title"],
            "outcome": unit["unit_outcome"],
            "lessons": exported_lessons,
        })

    return lookup, units


def resolve_lesson(item: dict[str, Any], lookup: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = [item.get("introduction_location"), *item.get("recycle_locations", [])]
    for location in candidates:
        if not location:
            continue
        lesson = lookup.get(location)
        if lesson:
            return lesson
    return None


def export_catalog() -> dict[str, Any]:
    lexical = read_json(LEXICAL_PATH)
    scope = read_json(SCOPE_PATH)
    lookup, units = lesson_lookup(scope)

    items: list[dict[str, Any]] = []
    unresolved: list[str] = []
    member_line_count = 0
    distinct_members: set[str] = set()

    for source in lexical["course_items"]:
        members = [member.strip() for member in source.get("members", []) if member.strip()]
        member_line_count += len(members)
        distinct_members.update(member.casefold() for member in members)
        lesson = resolve_lesson(source, lookup)
        if lesson is None:
            unresolved.append(source["lexical_item_id"])

        exported: dict[str, Any] = {
            "lexicalItemId": source["lexical_item_id"],
            "canonicalForm": source["canonical_form"],
            "itemType": source["item_type"],
            "members": members,
            "meaningOrFunction": source["meaning_or_function"],
            "register": source.get("register", "neutral"),
            "arabicLearnerRisks": source.get("arabic_learner_risks", []),
            "communicativeOwnerIds": source.get("communicative_owner_ids", []),
            "introductionLocation": source.get("introduction_location"),
        }
        if lesson:
            exported["lesson"] = lesson
        items.append(exported)

    if unresolved:
        raise SystemExit(
            "Every exported lexical/chunk item must resolve to an A1 lesson. Unresolved: "
            + ", ".join(unresolved)
        )

    audit = lexical.get("audit", {})
    expected_course_items = audit.get("course_item_count")
    expected_member_lines = audit.get("member_line_count")
    expected_distinct_members = audit.get("distinct_member_count")
    if expected_course_items is not None and expected_course_items != len(items):
        raise SystemExit(f"Course item count drift: expected {expected_course_items}, got {len(items)}")
    if expected_member_lines is not None and expected_member_lines != member_line_count:
        raise SystemExit(f"Member line count drift: expected {expected_member_lines}, got {member_line_count}")
    if expected_distinct_members is not None and expected_distinct_members != len(distinct_members):
        raise SystemExit(
            f"Distinct member count drift: expected {expected_distinct_members}, got {len(distinct_members)}"
        )

    return {
        "schemaVersion": 1,
        "catalogId": "english-course.a1.vocab-app",
        "curriculumStatus": scope.get("policy", {}).get("status", "locked_v1"),
        "language": "en",
        "learnerReferenceLanguage": "ar",
        "source": {
            "lexicalDatasetId": lexical.get("dataset_id"),
            "lexicalVersion": lexical.get("version"),
            "scopeSequenceId": scope.get("scope_sequence_id"),
            "scopeVersion": scope.get("version"),
            "lexicalSha256": sha256(LEXICAL_PATH),
            "scopeSha256": sha256(SCOPE_PATH),
        },
        "stats": {
            "unitCount": len(units),
            "lessonCount": sum(len(unit["lessons"]) for unit in units),
            "courseItemCount": len(items),
            "memberLineCount": member_line_count,
            "distinctMemberCount": len(distinct_members),
            "itemTypeCounts": audit.get("item_type_counts", {}),
        },
        "units": units,
        "lexicalItems": items,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    catalog = export_catalog()
    output.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stats = catalog["stats"]
    print(
        f"Exported {stats['courseItemCount']} course items / "
        f"{stats['memberLineCount']} member lines / "
        f"{stats['distinctMemberCount']} distinct members to {output.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
