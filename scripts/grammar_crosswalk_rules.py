"""Auditable GSE Grammar to EGP supercategory crosswalk rules."""


RULES = {
    "ADJECTIVES": ("adjective", "comparison"),
    "ADVERBS": ("adverb",),
    "CLAUSES": ("clause", "phrase", "conditional", "relative", "basic construction", "complementiser"),
    "CONJUNCTIONS": ("conjunction", "coordinating", "concession", "cause and result"),
    "DETERMINERS": ("determiner", "articles", "quantifier"),
    "DISCOURSE MARKERS": ("discourse marker", "linking expression"),
    "FOCUS": ("cleft", "fronting", "topicalis", "emphasi"),
    "FUTURE": ("future", "going to", "shall"),
    "MODALITY": ("modal", "obligation", "ability", "likelihood", "wishes and intentions"),
    "NEGATION": ("negation", "negative"),
    "NOUNS": ("noun",),
    "PASSIVES": ("passive",),
    "PAST": ("past", "used to"),
    "PREPOSITIONS": ("preposition",),
    "PRESENT": ("present",),
    "PRONOUNS": ("pronoun", "personal", "possessive", "demonstrative"),
    "QUESTIONS": ("question", "tags and question forms"),
    "REPORTED SPEECH": ("reported speech", "reported ideas"),
    "VERBS": ("verb", "infinitive", "auxiliary"),
}


def crosswalk(categories: str, structure: str, source_text: str) -> tuple[list[str], list[str]]:
    haystack = " ".join((categories, structure, source_text)).casefold()
    matched, rules = [], []
    for supercategory, terms in RULES.items():
        if any(term in haystack for term in terms):
            matched.append(supercategory)
            rules.append(f"gse_grammar_keyword_{supercategory.lower().replace(' ', '_')}")
    if not matched:
        matched, rules = ["CLAUSES"], ["gse_grammar_fallback_clause"]
    return matched, rules
