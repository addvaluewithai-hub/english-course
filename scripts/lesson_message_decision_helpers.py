"""Shared helpers for reviewed message target decisions."""


def error_hypothesis(
    error: str,
    impact: str,
    demand: str,
    source_note: str | None = None,
) -> dict[str, str]:
    basis = (
        "Candidate-specific hypothesis for Arabic-speaking A1 adults based on "
        f"{demand}; it is not a source fact and requires expert review and "
        "learner observation."
    )
    if source_note:
        basis = (
            f"{source_note} The candidate-specific error pattern is not a source fact "
            "and requires Arabic-English expert review and learner observation."
        )
    return {"error": error, "impact": impact, "basis": basis}
