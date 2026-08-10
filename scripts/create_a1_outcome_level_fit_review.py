"""Create the reviewed first pass over all current A1 candidate outcomes."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from scripts.a1_outcome_review_contract import (
    FIT_STATUSES, INDEPENDENCE_SIGNALS, INPUTS, OUTPUT, REPORT, REVIEWED_AT,
    REVIEWER, ROOT,
)
from scripts.a1_outcome_reviews_01_identity_routines import REVIEWS as REVIEWS_01
from scripts.a1_outcome_reviews_02_home_travel import REVIEWS as REVIEWS_02
from scripts.a1_outcome_reviews_03_services_messages import REVIEWS as REVIEWS_03
from scripts.a1_outcome_reviews_04_social_foundations import REVIEWS as REVIEWS_04
from scripts.a1_reconciliation_contract import PROFILES
from scripts.a1_reconciliation_contract import OUTPUT as WORKLIST
from scripts.source_disposition_inputs import file_sha256


def _load(path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _catalog() -> dict:
    result = {}
    for partition in (REVIEWS_01, REVIEWS_02, REVIEWS_03, REVIEWS_04):
        overlap = set(result) & set(partition)
        if overlap:
            raise ValueError(f"duplicate outcome reviews: {sorted(overlap)}")
        result.update(partition)
    return result


def _claim_ids(row: dict) -> list[str]:
    claims = ["a1.exit_promise"]
    skills, modes = set(row["skill_codes"]), set(row["mode_codes"])
    if "listening" in skills and "reception" in modes:
        claims.append("a1.reception.listening")
    if "reading" in skills and "reception" in modes:
        claims.append("a1.reception.reading")
    if "speaking" in skills and "production" in modes:
        claims.append("a1.production.speaking")
    if "writing" in skills and "production" in modes:
        claims.append("a1.production.writing")
    if "interaction" in modes:
        if "speaking" in skills or "listening" in skills:
            claims.append("a1.interaction.oral")
        if "writing" in skills or "reading" in skills:
            claims.append("a1.interaction.written_online")
    if "online_interaction" in modes:
        claims.append("a1.interaction.written_online")
    if "mediation" in modes:
        claims.append("a1.interaction.mediation")
    if "communicative_competence" in modes:
        claims.append("a1.language_control.range")
    return list(dict.fromkeys(claims))


def _known_claims() -> set[str]:
    profile = next(row for row in _load(PROFILES)["levels"] if row["level"] == "a1")
    claims = {profile["exit_promise"]["claim_id"]}
    for section in ("reception", "production", "interaction", "language_control"):
        claims.update(row["claim_id"] for row in profile[section].values())
    return claims


def build() -> dict[str, Any]:
    worklist = _load(WORKLIST)
    catalog = _catalog()
    rows = []
    for candidate in worklist["candidates"]:
        fit, signal, risks, rationale = catalog[candidate["candidate_id"]]
        rows.append({
            "candidate_id": candidate["candidate_id"],
            "original_sequence_position": candidate["original_sequence_position"],
            "a1_source_fit_confirmed": candidate["evidence"]["level_fit"]["status"] == "a1_only_evidence",
            "profile_claim_ids": _claim_ids(candidate),
            "a1_fit_status": fit, "independence_signal": signal,
            "risk_codes": risks, "rationale": rationale,
            "review_status": "accepted_first_pass",
        })
    fit_counts = Counter(row["a1_fit_status"] for row in rows)
    signal_counts = Counter(row["independence_signal"] for row in rows)
    risk_counts = Counter(code for row in rows for code in row["risk_codes"])
    known_claims = _known_claims()
    unknown_claims = sorted({claim for row in rows for claim in row["profile_claim_ids"] if claim not in known_claims})
    return {
        "schema_version": 1, "review_id": "a1_outcome_level_fit_review", "version": 1,
        "inputs": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)}
            for path in INPUTS
        ],
        "reviews": rows,
        "audit": {
            "review_count": len(rows), "source_fit_confirmed_count": sum(row["a1_source_fit_confirmed"] for row in rows),
            "fit_status_counts": dict(sorted(fit_counts.items())),
            "independence_signal_counts": dict(sorted(signal_counts.items())),
            "risk_code_counts": dict(sorted(risk_counts.items())),
            "missing_candidate_ids": [], "unknown_candidate_ids": [], "unknown_profile_claim_ids": unknown_claims,
            "final_candidate_decisions_made": 0,
        },
        "review": {
            "status": "accepted_first_pass", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "method": "candidate_by_candidate_outcome_independence_and_a1_exit_boundary_review",
            "statement": "A level-fit or independence signal is evidence for later reconciliation, not a final keep, merge, or retire decision.",
        },
    }


def _report(data: dict) -> str:
    audit = data["audit"]
    lines = [
        "# A1 Outcome and Level-Fit Review v1", "", "Status: first reconciliation pass accepted.", "",
        f"All {audit['source_fit_confirmed_count']} candidates cross-walk to A1-only source evidence.",
        "That confirms level relevance but does not prove standalone lesson value.", "",
        "| # | Candidate | A1 fit | Independence signal | Risks |", "| ---: | --- | --- | --- | --- |",
    ]
    for row in data["reviews"]:
        lines.append(
            f"| {row['original_sequence_position']} | `{row['candidate_id']}` | {row['a1_fit_status']} | "
            f"{row['independence_signal']} | {', '.join(row['risk_codes']) or '-'} |"
        )
    lines += [
        "", "No final candidate decision is made in this pass. Merge, support, split, and",
        "standalone signals must still survive global ability coverage, language ownership,",
        "sequence/recycling, mastery, and exit-assessment review.", "",
    ]
    return "\n".join(lines)


def main() -> int:
    data = build()
    OUTPUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(_report(data), encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} ({len(data['reviews'])} reviews)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
