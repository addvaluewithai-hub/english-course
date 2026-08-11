"""Render a de-identified aggregate learner-test decision report."""


def render(data: dict) -> str:
    lines = [
        "# Gold Lesson Learner-Test Analysis", "",
        f"- Study: `{data['study_id']}`",
        f"- Evidence mode: `{data['evidence_mode']}`",
        f"- Gate effect: `{data['gate_effect']}`",
        f"- Hypothetical decision from supplied records: `{data['hypothetical_decision']}`",
        "", "## Sample", "",
    ]
    for key, value in data["sample"].items():
        lines.append(f"- {key}: {value}")
    lines += ["", "## Pre-registered gates", "",
              "| Metric | Numerator | Denominator | Value | Rule | Status |", "| --- | ---: | ---: | ---: | --- | --- |"]
    for row in data["gating_metrics"]:
        lines.append(
            f"| {row['metric_id']} | {row['numerator']} | {row['denominator']} | "
            f"{row['value']} | {row['operator']} {row['threshold']} | {row['status']} |"
        )
    lines += ["", "## Descriptive evidence", "",
              f"- Completion outcomes: {data['descriptive']['completion_outcomes']}",
              f"- Mastery decisions: {data['descriptive']['mastery_decisions']}",
              f"- Total seconds: {data['descriptive']['total_seconds']}",
              f"- Issue counts: {data['descriptive']['issues']}", ""]
    for condition, row in data["descriptive"]["conditions"].items():
        lines.append(f"### {condition}")
        lines.append("")
        lines.append(f"Sessions: {row['sessions']}; ratings: {row['experience']}")
        lines.append("")
    lines += ["## Privacy boundary", "",
              "This aggregate contains no raw learner answer, direct identifier, or individual issue note.", ""]
    if data["evidence_mode"] != "real_consented_sessions":
        lines += ["## No gate effect", "",
                  "These records are synthetic fixtures. They test the analysis pipeline only and cannot",
                  "complete TEST-002 or authorize lesson-system decisions.", ""]
    return "\n".join(lines)
