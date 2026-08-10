"""Markdown rendering for the A1 dependency/mastery audit."""


def render(data: dict) -> str:
    audit = data["audit"]
    counts = audit["exact_item_sequence_status_counts"]
    lines = [
        "# A1 Prerequisite, Recycling, Mastery, and Exit Audit v1", "",
        "Status: accepted as a constraint audit; final candidates and order remain open.", "",
        f"- Explicit dependency edges aligned: {audit['aligned_explicit_dependency_edges']}/{audit['explicit_dependency_edge_count']}",
        f"- Exact system items audited: {audit['exact_item_count']}",
        f"- Sequence-aligned exact items: {counts.get('aligned', 0)}",
        f"- Items with an earlier use than their named introduction: {counts.get('early_use_requires_introduction_transfer_or_reorder', 0)}",
        f"- Items with no later recycle in the provisional order: {counts.get('no_later_recycle_requires_reorder_or_new_recycle', 0)}",
        f"- Structurally complete mastery records: {audit['structurally_complete_mastery_records']}/{audit['candidate_count']}",
        f"- Mastery constructs requiring revision: {audit['mastery_constructs_requiring_revision']}",
        f"- Protected A1 exit dimensions: {audit['protected_exit_dimension_count']}/7", "",
        "The 60 sequence findings do not mean 60 bad items. They show that the old",
        "provisional order and the new exact ownership decisions were created at different",
        "times. SPINE-006 must move the named introduction, move the candidate, or add a",
        "fresh later recycle before the final sequence can lock.", "",
        "## Exact-item sequence findings", "",
        "| System | Item | Status | Earlier uses | Later recycles |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in data["exact_item_sequence"]:
        if row["status"] == "aligned":
            continue
        early = ", ".join(row["early_recycle_location_ids"]) or "-"
        later = ", ".join(row["later_recycle_location_ids"]) or "-"
        lines.append(f"| {row['system']} | `{row['item_id']}` | {row['status']} | {early} | {later} |")
    lines += ["", "## Mastery constructs requiring revision", "",
              "| Candidate | Risks | Required actions |", "| --- | --- | --- |"]
    for row in data["mastery_reviews"]:
        if row["construct_alignment_status"] == "aligned_with_current_outcome":
            continue
        risks = ", ".join(row["risk_codes"])
        actions = " ".join(row["required_revision_actions"])
        lines.append(f"| `{row['candidate_id']}` | {risks} | {actions} |")
    lines += ["", "## Exit safeguards", "", "| Dimension | Current owners | Protected anchors |",
              "| --- | ---: | --- |"]
    for row in data["exit_safeguards"]:
        anchors = ", ".join(row["protected_capability_anchor_ids"])
        lines.append(f"| {row['dimension_code']} | {row['current_owner_count']} | {anchors} |")
    lines += ["", "These anchors protect capabilities, not the current lesson count. A candidate",
              "may merge, split, or become support as long as its capability and exact-item",
              "ownership are transferred explicitly.", ""]
    return "\n".join(lines)
