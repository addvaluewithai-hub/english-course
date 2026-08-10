"""Validate the locked A1 units, order, item lifecycle, and mastery coverage."""

import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.a1_scope_sequence_contract import INPUTS, OUTPUT, POLITENESS_SUPPORT_ID, ROOT, SCHEMA
from scripts.a1_scope_sequence_mastery_catalog import EXIT_STATIONS, UNIT_STATIONS
from scripts.a1_scope_sequence_unit_catalog import UNITS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, item.absolute_path)) or '$'}: {item.message}"
        for item in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    if [row["path"] for row in data["inputs"]] != [item.relative_to(ROOT).as_posix() for item in INPUTS]:
        errors.append("scope-sequence input order changed")
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    final, dependency = _load(INPUTS[0]), _load(INPUTS[2])
    units = data["units"]
    lessons = [lesson for unit in units for lesson in unit["lessons"]]
    expected_owners = {row["final_owner_id"] for row in final["final_lesson_capabilities"]}
    actual_owners = [row["final_owner_id"] for row in lessons]
    if set(actual_owners) != expected_owners or len(actual_owners) != len(set(actual_owners)):
        errors.append("final capability owners are missing or duplicated")
    if [row["global_sequence_position"] for row in lessons] != list(range(1, 46)):
        errors.append("global lesson sequence is not contiguous")
    if [unit["unit_id"] for unit in units] != [unit["unit_id"] for unit in UNITS]:
        errors.append("reviewed unit catalog changed")
    positions = {POLITENESS_SUPPORT_ID: 0, "assessment.a1_exit_language_probe": 10000}
    for unit in units:
        for lesson in unit["lessons"]:
            positions[lesson["final_owner_id"]] = lesson["global_sequence_position"] * 10
        positions[unit["unit_review_id"]] = unit["lessons"][-1]["global_sequence_position"] * 10 + 5
    expected_items = {row["item_id"] for row in dependency["exact_item_sequence"]}
    placements = {row["item_id"]: row for row in data["exact_item_placements"]}
    if set(placements) != expected_items:
        errors.append("exact-item placement inventory changed")
    for item_id, row in placements.items():
        chain = [row["final_introduction_location_id"], row["first_fresh_recycle_location_id"], row["consolidation_location_id"]]
        if any(location not in positions for location in chain):
            errors.append(f"unknown lifecycle location: {item_id}")
        elif not positions[chain[0]] < positions[chain[1]] < positions[chain[2]]:
            errors.append(f"lifecycle order is invalid: {item_id}")
    for edge in data["mapped_prerequisite_edges"]:
        if edge["before_position"] >= edge["after_position"]:
            errors.append(f"mapped prerequisite is reversed: {edge['after_owner_id']}")
    all_station_ids, covered = set(), set()
    for unit in units:
        unit_owners = {row["final_owner_id"] for row in unit["lessons"]}
        catalog_ids = {row["station_id"] for row in UNIT_STATIONS[unit["unit_id"]]}
        actual_ids = {row["station_id"] for row in unit["unit_review"]["mastery_stations"]}
        if catalog_ids != actual_ids:
            errors.append(f"unit mastery catalog changed: {unit['unit_id']}")
        for station in unit["unit_review"]["mastery_stations"]:
            all_station_ids.add(station["station_id"])
            covered.update(station["owner_ids"])
            if not set(station["owner_ids"]).issubset(unit_owners):
                errors.append(f"unit station crosses unit boundaries: {station['station_id']}")
    if covered != expected_owners:
        errors.append("one or more final capabilities lacks unit mastery")
    exit_ids = {row["station_id"] for row in data["exit_assessment"]["stations"]}
    if exit_ids != {row["station_id"] for row in EXIT_STATIONS}:
        errors.append("exit station catalog changed")
    dimensions = {code for row in data["exit_assessment"]["stations"] for code in row["dimension_codes"]}
    required = {"listening_reception", "reading_reception", "speaking_production", "writing_production", "oral_interaction", "written_online_interaction", "mediation"}
    if dimensions != required:
        errors.append("exit dimension coverage is incomplete")
    if data["audit"]["unresolved_questions"] or data["audit"]["unresolved_item_placements"]:
        errors.append("scope and sequence retains unresolved findings")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print(f"FAIL {OUTPUT}")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"PASS {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
