"""Human-readable summary of the exact A1 lexical and chunk syllabus."""


def render(data: dict) -> str:
    audit = data["audit"]
    lines = [
        "# A1 Lexical and Chunk Ownership v1", "",
        "Status: exact lexical-system pass accepted; final lesson placement remains open.", "",
        "## Result", "",
        f"- All {audit['oxford_a1_record_count']} Oxford A1 entry lines have one disposition.",
        f"- {audit['course_item_count']} course-controlled resources contain "
        f"{audit['member_line_count']} explicit member lines ({audit['distinct_member_count']} distinct forms).",
        f"- {audit['selected_oxford_record_count']} Oxford rows support selected items; "
        f"{audit['grammar_owned_oxford_record_count']} are owned by grammar; "
        f"{audit['reference_pool_record_count']} remain deliberate reserve evidence.",
        f"- All {audit['legacy_vocabulary_candidate_count']} vocabulary-target candidates and "
        f"all {audit['legacy_phrase_candidate_count']} phrase-target candidates have exact owners.",
        "- Oxford counts remain evidence coverage, never a promised learner word count.", "",
        "## Item profile", "", "| Type | Items |", "|---|---:|",
    ]
    for item_type, count in sorted(audit["item_type_counts"].items()):
        lines.append(f"| `{item_type}` | {count} |")
    lines.extend(["", "## Oxford dispositions", "", "| Disposition | Rows |", "|---|---:|"])
    for status, count in sorted(audit["oxford_disposition_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## Controlled resources", ""])
    for item in data["course_items"]:
        intro = item["introduction_location"].split(".")[-1]
        recycle = ", ".join(value.split(".")[-1] for value in item["recycle_locations"])
        lines.extend([
            f"### {item['canonical_form']} (`{item['lexical_item_id']}`)", "",
            f"Type: `{item['item_type']}`. Register: `{item['register']}`.", "",
            "Members: " + "; ".join(item["members"]), "",
            f"Function: {item['meaning_or_function']}", "",
            f"Introduce in: {intro}. Recycle in: {recycle}.", "",
            f"Production: {item['productive_expectation']}", "",
        ])
    lines.extend([
        "## Boundary decisions", "",
        "- Closed sets and frames are bounded; learners are not required to memorise every Oxford A1 row.",
        "- Country and nationality language uses a personalised slot instead of an arbitrary world list.",
        "- A headword is selected only with a stated A1 meaning or function; additional senses remain later work.",
        "- Chunks are taught as usable whole frames, while their grammar remains owned by the grammar syllabus.",
        "- Every selected resource has a later fresh retrieval context before A1 consolidation.", "",
        "No current candidate, unit boundary, or final lesson count is frozen by this pass.", "",
    ])
    return "\n".join(lines)
