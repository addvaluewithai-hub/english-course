"""Product rules for selecting lexical items from source reference pools."""

SELECTION_PRINCIPLES = (
    "Start from an approved communicative outcome, never from an isolated word-list row.",
    "Select a specific meaning, grammatical use, chunk, or collocation; a headword is not one indivisible target.",
    "Prefer high-utility language that recurs across more than one approved task or domain.",
    "Keep receptive exposure and productive control as separate decisions.",
    "Require a planned fresh recycle after guided production and before consolidation.",
    "Record deliberate omissions so breadth can be audited without forcing every reference-pool entry into the course.",
    "Test register, cultural fit, adult relevance, and Arabic explanation needs before authoring.",
    "Count source entry lines as evidence coverage, never as promised learner word counts.",
)

PROMOTION_GATES = {
    "expose_to_introduce": (
        "The meaning or function is needed by an approved outcome.",
        "The learner can notice it in comprehensible context without an independent-production demand.",
    ),
    "introduce_to_practise": (
        "Meaning, form, pronunciation when spoken, and at least one usable frame are specified.",
        "The practice task requires the target meaning rather than allowing unrelated substitution.",
    ),
    "practise_to_consolidate": (
        "The item has returned in at least one distinct context after introduction.",
        "Fresh performance requires retrieval without copying and meets the level control boundary.",
    ),
    "consolidate_to_extend": (
        "The consolidated meaning remains retrievable.",
        "The new use adds sense, collocation, domain, register, nuance, or independence.",
    ),
}

C2_METHOD = {
    "status": "accepted_method_before_item_selection",
    "trigger": "Oxford 3000 and 5000 provide no C2-specific lexical pool.",
    "required_evidence": (
        "an approved C2 communicative, discourse, professional, academic, or cultural need",
        "attested contemporary use in a registered general corpus or comparable usage resource",
        "domain-corpus or expert evidence when the item is specialist",
        "context samples sufficient to judge sense, collocation, register, connotation, and dispersion",
    ),
    "selection_tests": (
        "utility for precise meaning or synthesis rather than rarity alone",
        "distribution across relevant speakers, texts, registers, or domains rather than raw frequency alone",
        "teachable contrast with a known alternative, paraphrase, or phraseological frame",
        "clear receptive and productive expectations with a documented recycle plan",
    ),
    "prohibitions": (
        "No invented C2 word-count target.",
        "No single-corpus frequency cutoff as automatic inclusion.",
        "No obscure vocabulary selected merely to make the course appear advanced.",
        "No source may be used until its version, licence, provenance, and extraction method are registered.",
    ),
}
