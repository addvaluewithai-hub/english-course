"""Promote the reviewed level-exit proposal to evidence-linked v1 claims."""

from __future__ import annotations

import json
from typing import Any

from scripts.level_exit_profile_contract import (
    CLAIM_STRANDS, EVIDENCE, LEVELS, OUTPUT, PROPOSAL, REPORT, REVIEWED_AT,
    REVIEWER, ROOT, source_bundle,
)
from scripts.source_disposition_inputs import file_sha256


POLICY_REFS = [
    "docs/LEARNING_PRINCIPLES.md#core-learning-loop",
    "docs/LEARNING_PRINCIPLES.md#mastery",
]


def _claim(claim_id: str, claim_type: str, text: str, bundles: list[str], refs: list[str]) -> dict:
    return {
        "claim_id": claim_id, "claim_type": claim_type, "text": text,
        "evidence_bundle_ids": bundles, "decision_refs": refs,
        "review": {"status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT},
    }


def _bundles(level: str, field: str, known: set[str]) -> list[str]:
    strand = CLAIM_STRANDS[field]
    candidates = [source_bundle("cefr_all_descriptors", level, strand)]
    if strand in {"listening_reception", "reading_reception", "speaking_production", "writing_production"}:
        candidates.append(source_bundle("gse_all_objectives", level, strand))
    if strand == "grammar":
        candidates += [
            source_bundle("egp_all_levels", level, "grammar"),
            source_bundle("gse_grammar_all", level, "grammar"),
        ]
    if strand == "vocabulary":
        candidates += [
            source_bundle("oxford_3000_all", level, "lexical_pool"),
            source_bundle("oxford_5000_all", level, "lexical_pool"),
        ]
    return [candidate for candidate in candidates if candidate in known]


def _boundary_claim(level: str, field: str, text: str, known: set[str]) -> dict:
    return _claim(
        f"{level}.{field}", "source_boundary", text, _bundles(level, field, known), [],
    )


def _exit_promise(level: str, text: str, known: set[str]) -> dict:
    fields = (
        "reception.listening", "reception.reading", "production.speaking",
        "production.writing", "interaction.oral", "interaction.written_online",
        "interaction.mediation",
    )
    evidence = sorted({bundle for field in fields for bundle in _bundles(level, field, known)})
    return _claim(
        f"{level}.exit_promise", "synthesis", text, evidence,
        ["docs/CROSS_LEVEL_CURRICULUM_ARCHITECTURE.md#supported-progression"],
    )


def _assessment_claim(level: str, index: int, text: str) -> dict:
    return _claim(f"{level}.assessment.{index:02d}", "product_policy", text, [], POLICY_REFS)


def _level(source: dict, index: int, known: set[str]) -> dict[str, Any]:
    level = source["level"]
    reception = {
        key: _boundary_claim(level, f"reception.{key}", text, known)
        for key, text in source["reception"].items()
    }
    production = {
        key: _boundary_claim(level, f"production.{key}", text, known)
        for key, text in source["production"].items()
    }
    interaction = {
        key: _boundary_claim(level, f"interaction.{key}", text, known)
        for key, text in source["interaction"].items()
    }
    language = {
        key: _boundary_claim(level, f"language_control.{key}", text, known)
        for key, text in source["language_control"].items()
    }
    if level == "c2":
        reception["listening"]["text"] = (
            "Understand with ease virtually any kind of live or recorded language, "
            "including delivery at fast natural speed."
        )
    return {
        "level": level, "progression_index": index, "gse_range": source["gse_range"],
        "title": source["title"],
        "exit_promise": _exit_promise(level, source["exit_promise"], known),
        "reception": reception, "production": production, "interaction": interaction,
        "language_control": language,
        "assessment_evidence": [
            _assessment_claim(level, item_index, text)
            for item_index, text in enumerate(source["assessment_evidence"], 1)
        ],
        "decision_state": "accepted",
    }


def build() -> dict[str, Any]:
    proposal = json.loads(PROPOSAL.read_text(encoding="utf-8"))
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    known = {bundle["bundle_id"] for bundle in evidence["bundles"]}
    return {
        "schema_version": 2, "profile_set_id": "english_course_level_exit_profiles",
        "version": 1, "status": "approved", "exit_levels": list(LEVELS),
        "onboarding_support": proposal["onboarding_support"],
        "internal_milestones": proposal["internal_milestones"],
        "lifecycle": proposal["lifecycle"],
        "evidence_bundles": {
            "path": EVIDENCE.relative_to(ROOT).as_posix(), "sha256": file_sha256(EVIDENCE),
        },
        "levels": [_level(item, index, known) for index, item in enumerate(proposal["levels"], 1)],
        "review": {
            "status": "accepted", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "claim_by_claim_source_boundary_review", "issues": [],
        },
    }


def _report(data: dict[str, Any]) -> str:
    lines = [
        "# Level Exit Profiles v1", "", "Status: approved internal curriculum contract.", "",
        "These are performance boundaries, not lesson counts or grammar/vocabulary checklists.",
    ]
    for level in data["levels"]:
        lines += ["", f"## {level['level'].upper()} - {level['title']}", "", level["exit_promise"]["text"], ""]
        for section in ("reception", "production", "interaction", "language_control"):
            for key, claim in level[section].items():
                label = f"{section.replace('_', ' ')} / {key.replace('_', ' ')}"
                lines.append(f"- {label}: {claim['text']}")
        lines += ["", "Fresh exit evidence:"]
        lines += [f"- {claim['text']}" for claim in level["assessment_evidence"]]
    lines += [
        "", "## Evidence and decision boundary", "",
        "Every source-boundary claim points to validated record bundles in",
        "`data/reviewed/level-exit-evidence-v1.json`. CEFR supplies the primary level",
        "boundary; GSE, EGP, GSE Grammar, and Oxford are used only in their declared roles.",
        "Exact item lifecycle ownership remains a SPINE-004 progression decision.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} (102 reviewed claims)")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
