"""Build and render the post-migration gold-lesson QA decision."""

from scripts.gold_v1_contract import OUTPUT, QA_OUTPUT, REVIEWED_AT, REVIEWER, ROOT
from scripts.source_disposition_inputs import file_sha256


FINDINGS = (
    ("stale_package_identity", "medium", "Moved the package to versioned U1-L03 with final IDs and lineage."),
    ("stale_first_lesson_wording", "medium", "Changed the opening and declared U1-L01/U1-L02 prior learning."),
    ("out_of_sequence_live_vowel_contrast", "medium", "Removed systematic /lɪv/-/laɪv/ contrast and retained one modelled word."),
    ("bounded_possessive_and_article_intro_implicit", "medium", "Added my + name and a/an + job explanation and application."),
    ("v1_exact_targets_not_traceable", "medium", "Added a compact v2 packet for seven introductions and three recycles."),
    ("arabic_conversational_tanween", "info", "Confirmed شخص جديد and موضوع يقدر while retaining natural مثلًا."),
    ("mixed_language_tts_pronunciation", "info", "Confirmed one speaker and SSML wrapping for every spoken English span."),
)


def build_qa() -> dict:
    files = sorted(path for path in OUTPUT.rglob("*") if path.is_file())
    findings = [
        {"finding_id": item, "severity": severity, "status": "resolved", "resolution": resolution}
        for item, severity, resolution in FINDINGS
    ]
    return {
        "schema_version": 1, "qa_id": "gold_lesson_v1_qa", "version": 1,
        "package_path": OUTPUT.relative_to(ROOT).as_posix(),
        "package_files": [
            {"path": path.relative_to(ROOT).as_posix(), "sha256": file_sha256(path)} for path in files
        ],
        "findings": findings,
        "audit": {
            "finding_count": len(findings),
            "major_open": sum(row["severity"] == "major" and row["status"] != "resolved" for row in findings),
            "medium_open": sum(row["severity"] == "medium" and row["status"] != "resolved" for row in findings),
            "resolved_medium": sum(row["severity"] == "medium" and row["status"] == "resolved" for row in findings),
            "owner_accepted_content_preserved": True,
        },
        "review": {
            "status": "GOLD_003_passed", "reviewer": REVIEWER, "reviewed_at": REVIEWED_AT,
            "statement": "No major defect remains and every medium migration finding is resolved in the v1 package.",
        },
    }


def render(data: dict) -> str:
    lines = ["# Gold Lesson v1 QA", "", "Status: GOLD-003 passed for migrated U1-L03.", "",
             f"- Package files: {len(data['package_files'])}",
             f"- Open major findings: {data['audit']['major_open']}",
             f"- Open medium findings: {data['audit']['medium_open']}",
             f"- Resolved medium findings: {data['audit']['resolved_medium']}", "",
             "| Finding | Severity | Status | Resolution |", "| --- | --- | --- | --- |"]
    for row in data["findings"]:
        lines.append(f"| {row['finding_id']} | {row['severity']} | {row['status']} | {row['resolution']} |")
    lines += ["", "The owner-approved one-teacher Egyptian-Arabic explanation and fresh mastery",
              "shape are preserved. The lesson now follows social opening and listening input,",
              "uses only its locked exact targets, and remains interaction-free during video.", ""]
    return "\n".join(lines)
