"""Validate pronunciation boundaries, lifecycle, prerequisites, and risk labels."""

import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from scripts.pronunciation_progression_contract import (
    DECISIONS, DISPOSITIONS, LEVELS, OUTPUT, ROOT, SCHEMA,
)
from scripts.pronunciation_strand_catalog import PRONUNCIATION_STRANDS
from scripts.source_disposition_inputs import file_sha256


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _hash(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def _boundary_ids(rows: list[dict], level: str) -> list[str]:
    return sorted(
        row["source_record_id"] for row in rows
        if row["source_dataset_id"] == "cefr_all_descriptors"
        and level in row["source_level_codes"]
        and "pronunciation" in row["strand_codes"]
    )


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    visiting, visited = set(), set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(parent) for parent in graph[node]):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def _validate_strand(strand: dict, evidence: dict[str, list[str]], errors: list[str]) -> None:
    code = strand["strand_code"]
    stages = strand["stages"]
    if [stage["level"] for stage in stages] != list(LEVELS):
        errors.append(f"{code}: level order changed")
        return
    if len({stage["expectation"] for stage in stages}) != len(LEVELS):
        errors.append(f"{code}: stage expectations do not progress")
    control = LEVELS.index(strand["first_guided_productive_level"])
    consolidation = LEVELS.index(strand["first_family_consolidation_level"])
    if control > consolidation:
        errors.append(f"{code}: consolidation precedes guided production")
    for index, stage in enumerate(stages):
        level, states = stage["level"], set(stage["lifecycle_states"])
        ids = evidence[level]
        if stage["cefr_boundary_evidence_count"] != len(ids):
            errors.append(f"{code}/{level}: CEFR boundary count changed")
        if stage["cefr_boundary_evidence_ids_sha256"] != _hash(ids):
            errors.append(f"{code}/{level}: CEFR boundary evidence changed")
        if index < control and states != {"expose"}:
            errors.append(f"{code}/{level}: premature productive state")
        if index == control and not {"introduce", "practise"}.issubset(states):
            errors.append(f"{code}/{level}: first guided production incomplete")
        if index == consolidation and "consolidate" not in states:
            errors.append(f"{code}/{level}: consolidation missing")
        if index > consolidation and not {"recycle", "extend"}.issubset(states):
            errors.append(f"{code}/{level}: later recycling or extension missing")


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
    dispositions = _load(DISPOSITIONS)["records"]
    evidence = {level: _boundary_ids(dispositions, level) for level in LEVELS}
    if any(not ids for ids in evidence.values()):
        errors.append("one or more levels lack CEFR pronunciation evidence")
    if {row["strand_code"] for row in data["strands"]} != set(PRONUNCIATION_STRANDS):
        errors.append("pronunciation strand catalog changed")
    for strand in data["strands"]:
        _validate_strand(strand, evidence, errors)
    graph = {row["strand_id"]: row["prerequisite_strand_ids"] for row in data["strands"]}
    if any(parent not in graph for parents in graph.values() for parent in parents):
        errors.append("pronunciation prerequisite points outside the catalog")
    elif _has_cycle(graph):
        errors.append("pronunciation prerequisite graph contains a cycle")
    strand_ids = set(graph)
    if any(risk["strand_id"] not in strand_ids for risk in data["arabic_learner_risk_hypotheses"]):
        errors.append("Arabic learner risk points outside the pronunciation catalog")
    if "General American pronunciation" not in DECISIONS.read_text(encoding="utf-8"):
        errors.append("teaching reference is no longer present in the product decisions")
    empty_audits = (
        "empty_cefr_boundary_stages", "invalid_prerequisites", "invalid_lifecycle_order",
        "risks_presented_as_source_facts", "accent_removal_requirements",
    )
    if any(data["audit"][field] for field in empty_audits):
        errors.append("accepted pronunciation audit retains an integrity finding")
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
