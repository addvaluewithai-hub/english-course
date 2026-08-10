"""Create an English-specific A1-C2 intelligibility progression."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from scripts.arabic_pronunciation_risk_catalog import RISK_HYPOTHESES, VALIDATION_ROUTE
from scripts.pronunciation_progression_contract import (
    ASSESSMENT_RULES, DECISIONS, DISPOSITIONS, LEVELS, OUTPUT, PROFILES,
    REPORT, REVIEWED_AT, REVIEWER, ROOT,
)
from scripts.pronunciation_strand_catalog import PRONUNCIATION_STRANDS
from scripts.source_disposition_inputs import file_sha256


def _hash(ids: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ids)).encode("utf-8")).hexdigest()


def _representatives(ids: list[str]) -> list[str]:
    ordered = sorted(ids)
    return [ordered[index] for index in sorted({0, len(ordered) // 2, len(ordered) - 1})]


def _states(level: str, control: str, consolidate: str) -> list[str]:
    index = LEVELS.index(level)
    control_index = LEVELS.index(control)
    consolidate_index = LEVELS.index(consolidate)
    if index < control_index:
        return ["expose"]
    if index == control_index == consolidate_index:
        return ["introduce", "practise", "consolidate"]
    if index == control_index:
        return ["introduce", "practise"]
    if index < consolidate_index:
        return ["recycle", "practise"]
    if index == consolidate_index:
        return ["recycle", "consolidate"]
    return ["recycle", "extend"]


def _evidence_by_level(dispositions: list[dict]) -> dict[str, list[str]]:
    return {
        level: sorted(
            row["source_record_id"] for row in dispositions
            if row["source_dataset_id"] == "cefr_all_descriptors"
            and level in row["source_level_codes"]
            and "pronunciation" in row["strand_codes"]
        )
        for level in LEVELS
    }


def _strand(code: str, row: dict, profiles: dict, evidence: dict) -> dict:
    stages = []
    for level in LEVELS:
        claim = profiles[level]["language_control"]["pronunciation"]
        ids = evidence[level]
        states = _states(level, row["control"], row["consolidate"])
        stages.append({
            "level": level, "expectation": row["expectations"][level],
            "exit_boundary": claim["text"], "profile_claim_id": claim["claim_id"],
            "control_focus": "receptive" if states == ["expose"] else "both",
            "lifecycle_states": states,
            "cefr_boundary_evidence_count": len(ids),
            "cefr_boundary_evidence_ids_sha256": _hash(ids),
            "representative_cefr_evidence_ids": _representatives(ids),
            "evidence_role": "level_boundary_not_sequence_proof",
        })
    return {
        "strand_id": f"pronunciation.{code}", "strand_code": code, "title": row["title"],
        "prerequisite_strand_ids": [f"pronunciation.{item}" for item in row["prerequisites"]],
        "first_guided_productive_level": row["control"],
        "first_family_consolidation_level": row["consolidate"],
        "stages": stages,
        "review": {
            "status": "accepted_internal_v1",
            "basis": "cefr_boundary_plus_english_specific_intelligibility_product_decision",
        },
    }


def _risk(risk_id: str, strand: str, statement: str) -> dict:
    return {
        "risk_id": f"arabic_pronunciation.{risk_id}",
        "strand_id": f"pronunciation.{strand}",
        "statement": statement,
        "evidence_status": "learner_risk_hypothesis_not_source_fact",
        "universality": "not_assumed_across_arabic_dialects_or_individuals",
        "validation_route": list(VALIDATION_ROUTE),
    }


def build() -> dict[str, Any]:
    disposition_data = json.loads(DISPOSITIONS.read_text(encoding="utf-8"))
    profile_data = json.loads(PROFILES.read_text(encoding="utf-8"))
    profiles = {row["level"]: row for row in profile_data["levels"]}
    evidence = _evidence_by_level(disposition_data["records"])
    strands = [
        _strand(code, PRONUNCIATION_STRANDS[code], profiles, evidence)
        for code in PRONUNCIATION_STRANDS
    ]
    risks = [_risk(*row) for row in RISK_HYPOTHESES]
    return {
        "schema_version": 1, "dataset_id": "pronunciation_progression_strands", "version": 1,
        "level_order": list(LEVELS),
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in (DISPOSITIONS, PROFILES, DECISIONS)
        ],
        "target_model": {
            "teaching_reference": "General American pronunciation for models and IPA",
            "success_standard": "intelligible effective meaning with level-appropriate listener effort and repair",
            "accent_policy": "A retained accent is acceptable whenever intelligibility and effectiveness are preserved.",
            "non_goals": ["accent removal", "native-speaker imitation", "one mandatory learner accent"],
        },
        "evidence_contract": {
            "cefr_role": "exit_intelligibility_boundary",
            "english_sequence_role": "reviewed_product_decision_not_claimed_as_cefr_sequence",
            "arabic_risk_role": "hypothesis_pending_specialist_and_learner_validation",
        },
        "strands": strands,
        "arabic_learner_risk_hypotheses": risks,
        "assessment_contract": {"status": "accepted", "rules": list(ASSESSMENT_RULES)},
        "audit": {
            "strand_count": len(strands), "stage_count": sum(len(row["stages"]) for row in strands),
            "risk_hypothesis_count": len(risks),
            "empty_cefr_boundary_stages": [], "invalid_prerequisites": [],
            "invalid_lifecycle_order": [], "risks_presented_as_source_facts": [],
            "accent_removal_requirements": [],
        },
        "review": {
            "status": "accepted_internal_v1", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "cefr_boundary_review_english_intelligibility_sequence_and_labelled_arabic_risk_audit",
            "limitations": [
                "CEFR evidence validates level boundaries, not this English-specific teaching order.",
                "Arabic-learner risks are dialect-sensitive hypotheses until specialist review and learner observation.",
                "Exact phoneme targets and task locations are selected during level reconciliation from communication need and observed breakdowns.",
            ],
        },
    }


def _report(data: dict) -> str:
    lines = [
        "# Pronunciation Progression v1", "", "Status: accepted internal curriculum contract.", "",
        "The goal is intelligible, effective communication—not accent removal. General American",
        "is the teaching reference for models and IPA; a retained learner accent remains acceptable.", "",
        "| Strand | Guided production begins | Family consolidation | A1 | C2 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for strand in data["strands"]:
        lines.append(
            f"| {strand['title']} | {strand['first_guided_productive_level'].upper()} | "
            f"{strand['first_family_consolidation_level'].upper()} | {strand['stages'][0]['expectation']} | "
            f"{strand['stages'][-1]['expectation']} |"
        )
    lines += [
        "", "## Arabic-speaking learner risks", "",
        "The 12 risk entries are hypotheses, not facts about every Arabic speaker. Each requires",
        "dialect-aware specialist review and learner observation before it may drive a target.", "",
        "Mastery is demonstrated in fresh communication. Isolated imitation is diagnostic only,",
        "and no assessment may penalise an accent that preserves meaning and intelligibility.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['strands'])} strands)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
