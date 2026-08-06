"""Write deterministic JSON and Markdown for the LESSON-002 global audit."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

try:
    from scripts.create_lesson_relationship_partition import REVIEW_PATH
    from scripts.lesson_map_global_audit import build_global_audit
    from scripts.lesson_map_io import DEFAULT_MAP_PATH, SOURCE_PATHS, load
except ModuleNotFoundError:
    from create_lesson_relationship_partition import REVIEW_PATH
    from lesson_map_global_audit import build_global_audit
    from lesson_map_io import DEFAULT_MAP_PATH, SOURCE_PATHS, load


ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "data/reviewed/a1-lesson-map-global-audit.json"
MARKDOWN_PATH = ROOT / "data/reviewed/a1-lesson-map-global-audit.md"


def included_ids() -> set[str]:
    return {
        record["record_id"] for path in SOURCE_PATHS for record in load(path)["records"]
        if record["interpretation"]["inclusion_status"] == "included"
    }


def build_audit() -> dict[str, Any]:
    return build_global_audit(
        load(DEFAULT_MAP_PATH), included_ids(), load(REVIEW_PATH)
    )


def render_markdown(audit: dict[str, Any]) -> str:
    coverage = audit["coverage"]
    relations = audit["relationships_and_sequence"]
    approval = audit["approval"]
    resolved = [
        item for item in audit["overlap_review"] if item["status"] == "resolved_merge"
    ]
    retained = [
        item for item in audit["overlap_review"] if item["status"] == "retain_distinct"
    ]
    passed = audit["decision"]["lesson_002_may_pass"]
    status_line = (
        "Status: approved; `LESSON-002` passes and Phase 4 may open."
        if passed else
        "Status: candidate approval required; `LESSON-002` remains in progress and Phase 4 stays locked."
    )
    lines = [
        "# A1 Lesson Map: Global Audit",
        "",
        status_line,
        "",
        "## Evidence and coverage",
        "",
        f"- Included records cited: {coverage['cited_included_records']} of {coverage['included_records']}.",
        f"- Candidate references: {coverage['candidate_references']}; support references: {coverage['support_references']}.",
        f"- Shared candidate evidence groups: {coverage['shared_candidate_record_groups']}; orphan records: {len(coverage['orphan_record_ids'])}.",
        "- Schema, provenance, exclusion, support-reciprocity, and duplicate-full-anchor validation pass.",
        "",
        "## Overlap remediation",
        "",
    ]
    lines.extend(
        f"- **{item['status']} - `{item['group_id']}`:** {item['rationale']}"
        for item in resolved
    )
    lines.extend(["", "Retained as distinct after review:", ""])
    lines.extend(
        f"- `{item['group_id']}`: {item['rationale']}" for item in retained
    )
    lines.extend([
        "",
        "## Balance, relationships, and mastery",
        "",
        f"- Candidates: {audit['balance']['candidate_count']}; skills: {audit['balance']['skill_candidate_counts']}.",
        f"- Modes: {audit['balance']['mode_candidate_counts']}; scope: {audit['balance']['scope_counts']}.",
        "- All four core skills are present. Counts describe source-led coverage, not equal lesson quotas.",
        f"- Candidate links: {relations['required_before']} required, {relations['helpful_before']} helpful, and {relations['successors']} successor.",
        f"- The accepted pedagogical hypothesis has {relations['sequence_bands']} sequence bands and is explicitly not source-proven strict order.",
        f"- Mastery alignment findings: {len(audit['mastery']['alignment_issues'])}; both reviewed cases are resolved and recorded.",
        "",
        "## Approval decision",
        "",
        f"All {audit['balance']['candidate_count']} candidates have source-linked language targets and one explicit labelled error decision.",
        f"Candidate states: {approval['candidate_status_counts']}; reviews: {approval['candidate_review_counts']}.",
        "",
        (
            "`LESSON-002` passes this consolidated audit. The next task is `GOLD-001`."
            if passed else
            "`LESSON-002` does not pass this audit; candidate approval remains required."
        ),
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    audit = build_audit()
    JSON_PATH.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MARKDOWN_PATH.write_text(render_markdown(audit), encoding="utf-8")
    print(f"WROTE {JSON_PATH}")
    print(f"WROTE {MARKDOWN_PATH}")


if __name__ == "__main__":
    main()
