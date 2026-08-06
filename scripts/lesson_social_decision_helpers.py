"""Shared helpers for final social-contact target decisions."""


def error_hypothesis(
    error: str,
    impact: str,
    demand: str,
) -> dict[str, str]:
    return {
        "error": error,
        "impact": impact,
        "basis": (
            "Candidate-specific hypothesis for Arabic-speaking A1 adults based on "
            f"{demand}; it is not a source fact and requires Arabic-English expert "
            "review and learner observation."
        ),
    }
