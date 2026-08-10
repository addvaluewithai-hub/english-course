"""Validate every SPINE-004 component and the global source/lifecycle gate."""

import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.source_disposition_inputs import file_sha256
from scripts.spine_004_audit_contract import (
    COMMUNICATIVE, DISPOSITIONS, GRAMMAR, LEXICAL, OUTPUT, PERFORMANCE,
    PRIMARY_PARTITIONS, PRONUNCIATION, ROOT, SCHEMA,
)
from scripts.validate_communicative_function_strands import validate as validate_communicative
from scripts.validate_grammar_family_strands import validate as validate_grammar
from scripts.validate_lexical_progression_strands import validate as validate_lexical
from scripts.validate_performance_complexity_strands import validate as validate_performance
from scripts.validate_pronunciation_progression_strands import validate as validate_pronunciation
from scripts.validate_source_dispositions import validate as validate_dispositions


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _component_errors() -> list[str]:
    validators = (
        ("source_dispositions", validate_dispositions),
        ("communicative", validate_communicative),
        ("grammar", validate_grammar),
        ("lexical", validate_lexical),
        ("pronunciation", validate_pronunciation),
        ("performance", validate_performance),
    )
    return [f"{name}: {error}" for name, validator in validators for error in validator()]


def _expected_components() -> dict[str, tuple[int, int, int]]:
    comm, grammar = _load(COMMUNICATIVE), _load(GRAMMAR)
    lexical, pronunciation = _load(LEXICAL), _load(PRONUNCIATION)
    performance = _load(PERFORMANCE)
    return {
        "communicative_abilities": (len(comm["strands"]), sum(len(row["lifecycle"]["stages"]) for row in comm["strands"]), 2274),
        "grammar_and_sentence_patterns": (len(grammar["families"]), sum(len(row["lifecycle"]["stages"]) for row in grammar["families"]), 1678),
        "vocabulary_phraseology_and_register": (len(lexical["resource_strands"]), lexical["audit"]["stage_count"], 5322),
        "pronunciation_and_intelligibility": (len(pronunciation["strands"]), pronunciation["audit"]["stage_count"], 1224),
        "discourse_interaction_and_complexity": (len(performance["strands"]), performance["audit"]["stage_count"], 1224),
    }


def validate(path: Path = OUTPUT) -> list[str]:
    schema, data = _load(SCHEMA), _load(path)
    Draft202012Validator.check_schema(schema)
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data)
    ]
    if errors:
        return errors
    for item in data["inputs"]:
        source = ROOT / item["path"]
        if not source.is_file() or file_sha256(source) != item["sha256"]:
            errors.append(f"input missing or changed: {item['path']}")
    errors.extend(_component_errors())
    source_rows = _load(DISPOSITIONS)["records"]
    counts = Counter(row["source_dataset_id"] for row in source_rows)
    seen = []
    actual_partitions = {row["partition"]: row for row in data["source_ownership"]["primary_partitions"]}
    for name, datasets in PRIMARY_PARTITIONS.items():
        row = actual_partitions.get(name)
        if not row or tuple(row["source_dataset_ids"]) != datasets:
            errors.append(f"{name}: primary datasets changed")
            continue
        if row["source_record_count"] != sum(counts[item] for item in datasets):
            errors.append(f"{name}: source-record count changed")
        seen.extend(datasets)
    if len(seen) != len(set(seen)) or set(seen) != set(counts):
        errors.append("source datasets are missing or multiply owned")
    expected = _expected_components()
    actual = {row["component"]: row for row in data["components"]}
    for name, values in expected.items():
        row = actual.get(name)
        observed = None if not row else (
            row["controlled_family_count"], row["lifecycle_stage_count"], row["source_record_coverage"]
        )
        if observed != values:
            errors.append(f"{name}: component coverage changed")
    performance_codes = {row["strand_code"] for row in _load(PERFORMANCE)["strands"]}
    if not {"discourse", "fluency", "communication_strategy", "sociolinguistic"}.issubset(performance_codes):
        errors.append("discourse or supporting performance strands are missing")
    integrity = (
        "invalid_level_regressions", "missing_consolidation",
        "missing_post_consolidation_recycle", "unexplained_orphans",
    )
    if any(data["global_lifecycle_audit"][field] for field in integrity):
        errors.append("SPINE-004 passes while retaining an integrity blocker")
    if len({row["limit_id"] for row in data["named_non_blocking_limits"]}) != 5:
        errors.append("named limits are duplicated")
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
