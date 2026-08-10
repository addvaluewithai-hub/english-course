"""Human-readable report for the A1 grammar ownership artifact."""

from collections import Counter


def render(data: dict) -> str:
    audit = data["audit"]
    lines = [
        "# A1 Grammar Coverage and Ownership v1", "",
        "Status: exact language-system pass accepted; final lesson placement is still open.", "",
        "## Result", "",
        f"- {audit['total_source_count']} A1 grammar source records accounted for: "
        f"{audit['egp_a1_source_count']} EGP and {audit['gse_grammar_a1_source_count']} GSE Grammar.",
        f"- {audit['course_item_count']} course-controlled learner items replace the misleading idea of 152 separate rules.",
        f"- {audit['legacy_target_count']} existing broad candidate targets crosswalk to exact forms.",
        "- No source record, course item, owner, or legacy target is orphaned.", "",
        "EGP is empirical learner evidence and GSE Grammar is a source inventory; neither is copied into the course as a checklist.",
        "The course items below are the A1 syllabus contract. Candidate owners are provisional contexts until final merge and sequence decisions.", "",
        "## Control profile", "",
        "| Control status | Items |", "|---|---:|",
    ]
    for status, count in sorted(audit["control_status_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## Source dispositions", "", "| Disposition | Records |", "|---|---:|"])
    for status, count in sorted(audit["disposition_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## Controlled items", ""])
    for item in data["course_items"]:
        intro = ", ".join(value.split(".")[-1] for value in item["introduction_owner_ids"])
        recycle = ", ".join(value.split(".")[-1] for value in item["recycle_owner_ids"])
        lines.extend([
            f"### {item['title']} (`{item['item_id']}`)", "",
            f"Control: `{item['control_status']}`. Sources: {item['source_evidence']['source_count']}.", "",
            "Forms: " + "; ".join(item["exact_forms"]), "",
            f"Use: {item['meaning_use']}", "",
            f"Introduce in: {intro}. Recycle in: {recycle}.", "",
            f"Mastery: {item['mastery_evidence']}", "",
            f"Boundary: {item['not_yet']}", "",
        ])
    lines.extend([
        "## Decisions this pass makes", "",
        "- Present be and present simple include affirmative, negative, question, and bounded short-answer control.",
        "- Present continuous, past simple, and will remain limited A1 targets; their broader systems wait.",
        "- `have` is the productive course default; BrE `have got` is registered and usable, not treated as an error.",
        "- Fixed social chunks, common/compound noun inventory, and capitalization move to their proper phrase, lexical, or writing layers.",
        "- Exact mastery is demonstrated inside fresh communicative tasks, not by naming a rule.", "",
        "No current candidate or lesson count is frozen by this pass.", "",
    ])
    return "\n".join(lines)
