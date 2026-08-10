"""Human-readable summary of exact A1 pronunciation ownership."""


def render(data: dict) -> str:
    audit = data["audit"]
    lines = [
        "# A1 Pronunciation and Intelligibility Ownership v1", "",
        "Status: exact pronunciation pass accepted; final lesson placement remains open.", "",
        "## Result", "",
        f"- {audit['target_count']} high-impact targets cover all {audit['strand_count']} progression strands.",
        f"- All {audit['legacy_pronunciation_candidate_count']} current pronunciation-target candidates have exact owners.",
        f"- All {audit['arabic_risk_hypothesis_count']} Arabic-learner risks have a disposition; none is treated as universal.",
        "- General American broad IPA is a modelling reference only. Success is intelligibility plus successful repair.",
        "- Accent removal, native imitation, and natural-rhythm mastery are explicitly excluded.", "",
        "## Target inventory", "",
    ]
    for target in data["targets"]:
        intro = target["introduction_location"].split(".")[-1]
        recycle = ", ".join(value.split(".")[-1] for value in target["recycle_locations"])
        examples = "; ".join(f"{item['text']} {item['reference_ipa']}" for item in target["course_examples"])
        lines.extend([
            f"### {target['title']} (`{target['target_id']}`)", "",
            f"Strand: `{target['strand_id']}`. Control: `{target['control_status']}`.", "",
            f"Focus: {target['feature_or_contrast']}", "",
            f"Examples: {examples}", "",
            f"Introduce in: {intro}. Recycle in: {recycle}.", "",
            f"Mastery: {target['mastery_evidence']}", "",
            f"Tolerance: {target['assessment_tolerance']}", "",
            f"Boundary: {target['not_yet']}", "",
        ])
    lines.extend([
        "## Arabic-learner risk handling", "",
        "Risk rows are diagnostic hypotheses only. Teach a risk target when the contrast affects the task or learner observation confirms the need.",
        "The /ŋ/ hypothesis remains monitor-only at A1 because no current high-value outcome justifies pre-teaching it.", "",
        "No current candidate, unit boundary, or final lesson count is frozen by this pass.", "",
    ])
    return "\n".join(lines)
