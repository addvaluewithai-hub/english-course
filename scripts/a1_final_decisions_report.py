"""Markdown rendering for final A1 candidate dispositions."""


def render(data: dict) -> str:
    audit = data["audit"]
    counts = audit["decision_counts"]
    lines = [
        "# A1 Final Candidate Decisions v1", "",
        "Status: SPINE-005 passed; final units and order remain blocked on SPINE-006.", "",
        f"- Reviewed source candidates: {audit['candidate_count']}",
        f"- Final learner-facing capability owners: {audit['final_lesson_capability_count']}",
        f"- Keep: {counts.get('keep', 0)}",
        f"- Revise: {counts.get('revise', 0)}",
        f"- Merge: {counts.get('merge', 0)}",
        f"- Support only: {counts.get('support_only', 0)}",
        f"- Split: {counts.get('split', 0)}",
        f"- Exact ownership-role transfers: {audit['ownership_transfer_count']}",
        f"- Protected exit anchors resolved: {audit['resolved_exit_anchor_count']}", "",
        "The old 81 candidates were evidence containers, not a promised lesson count. This",
        "pass preserves every source-backed capability but reduces duplication to 45",
        "learner-facing capability owners plus one cross-cutting politeness support owner.", "",
        "## Decisions", "", "| # | Candidate | Decision | Final owner(s) |",
        "| ---: | --- | --- | --- |",
    ]
    for row in data["decisions"]:
        owners = ", ".join(row["final_owner_ids"])
        lines.append(
            f"| {row['original_sequence_position']} | `{row['candidate_id']}` | "
            f"{row['decision']} | {owners} |"
        )
    lines += ["", "## Final learner-facing capabilities", "",
              "| Owner | Sources absorbed | Final outcome |", "| --- | ---: | --- |"]
    for row in data["final_lesson_capabilities"]:
        lines.append(
            f"| `{row['final_owner_id']}` | {len(row['source_candidate_ids'])} | "
            f"{row['outcome_statement']} |"
        )
    lines += ["", "## Gate to SPINE-006", "",
              f"SPINE-006 must resolve {audit['sequence_findings_carried_forward']} exact-item",
              "introduction/recycle order findings, transfer the Unit 1 ordering correction,",
              "group the 45 capabilities into final units, and define fresh unit/exit mastery.",
              "No mass lesson production is authorised before that lock.", ""]
    return "\n".join(lines)
