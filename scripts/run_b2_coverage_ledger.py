#!/usr/bin/env python3
"""Run the B2 Stage-06 ledger with Stage-07 lesson-semantic routing feedback.

Stage 06 proved exact coverage/lifecycle completeness. Stage 07 authoring inspection then
exposed a narrower scheduling issue: round-robin balancing inside a valid capability or
cross-cutting home can still place a source ability in the wrong *lesson* inside that
reviewed window.

This wrapper keeps Stage-1 semantic homes authoritative and keeps all scheduling inside
the Stage-06 reviewed introduction windows. It adds three bounded routing constraints:
1. SUPPORTING X-* ability rows cannot first appear in a clearly incompatible modality
   block (e.g. spoken production first introduced in a reading unit).
2. Within the remaining reviewed window, source text/function tags are matched against
   the Stage-5 lesson title/outcome so exact introductions prefer the most defensible
   lesson-level home.
3. Semantic routing is globally balanced against the existing Stage-06 ability warning
   threshold (9 introductions) so a generic similarity signal cannot collapse a whole
   capability into one lesson. Strong semantic matches are placed first; weaker ties use
   remaining capacity deterministically.

No final productive/receptive/formulaic/support role is inferred here; Stage 8 owns that
lock and Stage 8.5 must re-audit role-aware lifecycle/load.
"""
from __future__ import annotations

import re
from collections import Counter

import build_b2_coverage_ledger as ledger

MAP_PATH = ledger.REVIEW / "05-curriculum-map/curriculum-map.md"
ABILITY_LIMIT = 9

STOP = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "by", "can", "could",
    "do", "for", "from", "give", "in", "into", "is", "it", "language", "of", "on", "or",
    "range", "some", "that", "the", "their", "them", "they", "this", "to", "use", "using",
    "with", "within", "wide", "clear", "clearly", "detail", "detailed", "different",
}

CONCEPT_GROUPS = [
    {"argument", "claim", "reason", "reasons", "evidence", "conclusion", "support", "supporting"},
    {"fact", "opinion", "inference", "interpretation", "evaluate", "evaluation"},
    {"contrast", "contrasting", "compare", "comparison", "viewpoint", "viewpoints", "position", "positions"},
    {"purpose", "audience", "persuade", "persuasion", "persuasive", "rhetorical"},
    {"tone", "attitude", "irony", "stance", "certainty", "enthusiasm", "reluctance", "emphasis"},
    {"locate", "scan", "search", "specific", "find"},
    {"integrate", "synthesise", "synthesize", "sources", "source", "combine"},
    {"diagram", "graph", "graphs", "chart", "charts", "table", "tables", "visual", "data"},
    {"instruction", "instructions", "process", "procedure", "procedures", "stage", "stages", "steps", "technical", "advice"},
    {"narrative", "narrate", "story", "plot", "event", "events", "character", "characters"},
    {"main", "points", "sequence", "extended", "presentation", "presentations", "broadcast", "media"},
    {"describe", "description", "person", "people", "place", "places", "product", "products", "characteristics"},
    {"explain", "explanation", "factual", "field", "information", "informative"},
    {"background", "prior", "chronology", "reaction", "reactions", "experience", "experiences"},
    {"trend", "trends", "change", "development", "developed", "increase", "decrease"},
    {"presentation", "presentations", "announce", "announcement", "announcements", "notes", "script"},
    {"intelligibility", "pronunciation", "stress", "prominence", "chunking", "repair", "accent"},
    {"viewpoint", "opinion", "position", "claim", "reasons", "examples", "justify", "justification"},
    {"advantages", "disadvantages", "criteria", "alternatives", "options", "compare", "evaluate"},
    {"recommend", "recommendation", "solution", "solutions", "priority", "priorities", "action"},
    {"cause", "causes", "consequence", "consequences", "result", "results", "condition", "conditions"},
    {"probability", "likelihood", "likely", "certainty", "expectation", "deduction", "predict", "prediction"},
    {"past", "regret", "possibility", "possibilities", "speculate", "speculation", "missed"},
    {"hypothetical", "counterfactual", "imagined", "alternative", "alternatives"},
    {"discussion", "contribute", "contribution", "participate", "participation", "turn", "conversation"},
    {"develop", "idea", "ideas", "support", "qualification", "qualify", "example", "consequence"},
    {"redirect", "perspective", "topic", "shift", "angle"},
    {"agree", "agreement", "disagree", "disagreement", "hedge", "tact", "reservation"},
    {"repair", "clarify", "clarification", "misunderstanding", "reformulate", "reformulation"},
    {"spontaneous", "unexpected", "changing", "unprepared"},
    {"problem", "problems", "complaint", "complaints", "service", "transaction", "transactional"},
    {"negotiate", "negotiation", "compromise", "resolve", "resolution", "dispute", "disputes"},
    {"formal", "interview", "interviews", "survey", "question", "questions", "answer", "answers"},
    {"relay", "paraphrase", "paraphrasing", "summarise", "summarize", "summary", "mediate", "mediation", "facilitate"},
    {"write", "writing", "paragraph", "paragraphs", "edit", "editing"},
    {"counterargument", "counter", "synthesis", "synthesise", "synthesize", "evidence", "argument"},
    {"correspondence", "application", "enquiry", "invitation", "request", "recipient", "register"},
    {"report", "reports", "review", "reviews", "recommendation", "findings"},
]


def unit_of(lesson_id: str) -> str:
    return lesson_id.split("-", 1)[0]


def simple_stem(token: str) -> str:
    token = token.lower()
    for suffix in ("ingly", "edly", "ation", "ions", "ing", "ed", "es", "s"):
        if len(token) > len(suffix) + 3 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


def tokens(text: str) -> set[str]:
    raw = re.findall(r"[a-zA-Z]+", text.lower().replace("_", " "))
    return {simple_stem(x) for x in raw if x not in STOP and len(x) > 2}


def lesson_contexts() -> dict[str, dict[str, str]]:
    lines = MAP_PATH.read_text(encoding="utf-8").splitlines()
    out: dict[str, dict[str, str]] = {}
    current: str | None = None
    buffer: list[str] = []

    def flush() -> None:
        nonlocal current, buffer
        if not current:
            return
        body = []
        started = False
        for raw in buffer:
            line = raw.strip()
            if not line:
                if started:
                    break
                continue
            if line.startswith("**Unit critic:**"):
                break
            started = True
            body.append(line)
        out[current]["outcome"] = " ".join(body)
        current = None
        buffer = []

    for raw in lines:
        m = re.match(r"^###\s+(U\d+-L\d+)\s+[—-]\s+(.+?)\s*$", raw)
        if m:
            flush()
            current = m.group(1)
            out[current] = {"title": m.group(2), "outcome": ""}
            buffer = []
        elif current:
            buffer.append(raw)
    flush()
    if len(out) != 95:
        raise ValueError(f"Stage-07 semantic router expected 95 lesson contexts, got {len(out)}")
    return out


LESSONS = lesson_contexts()


def compatible_intro_units(item: dict) -> set[str]:
    modes = {str(x).lower() for x in item.get("mode_codes", [])}
    skills = {str(x).lower() for x in item.get("skill_codes", [])}
    units: set[str] = set()

    reception = any("reception" in x for x in modes)
    production = any("production" in x for x in modes)
    interaction = any("interaction" in x for x in modes)
    mediation = any("mediation" in x for x in modes)

    reading = any("read" in x for x in skills)
    listening = any("listen" in x for x in skills)
    speaking = any("speak" in x or "oral" in x for x in skills)
    writing = any("writ" in x for x in skills)

    if reception:
        if reading:
            units.update({"U1", "U2"})
        if listening:
            units.add("U3")
        if not reading and not listening:
            units.update({"U1", "U2", "U3"})

    if production:
        if speaking:
            units.update({"U4", "U5", "U6", "U7", "U8", "U9"})
        if writing:
            units.update({"U10", "U11", "U12"})
        if not speaking and not writing:
            units.update({"U4", "U5", "U6", "U7", "U8", "U9", "U10", "U11", "U12"})

    if interaction:
        if writing:
            units.add("U12")
        if speaking or not writing:
            units.update({"U6", "U7", "U8", "U9"})

    if mediation:
        units.add("U9")

    return units


def semantic_score(record: dict, lesson_id: str) -> int:
    source_text = " ".join(
        [
            str(record.get("source_text", "")),
            " ".join(str(x) for x in record.get("function_codes", [])),
            " ".join(str(x) for x in record.get("skill_codes", [])),
        ]
    )
    lesson = LESSONS[lesson_id]
    source_tokens = tokens(source_text)
    title_tokens = tokens(lesson["title"])
    outcome_tokens = tokens(lesson["outcome"])

    score = 5 * len(source_tokens & title_tokens) + 2 * len(source_tokens & outcome_tokens)
    source_raw = source_text.lower()
    lesson_raw = (lesson["title"] + " " + lesson["outcome"]).lower()
    for group in CONCEPT_GROUPS:
        if any(term in source_raw for term in group) and any(term in lesson_raw for term in group):
            score += 6
    return score


_original_balanced = ledger.balanced
_original_build_record = ledger.build_record


def balanced_with_stage07_semantics(records, key_fn, windows_fn, salt):
    if salt != "ability":
        return _original_balanced(records, key_fn, windows_fn, salt)

    plans = []
    for record in records:
        key = key_fn(record)
        windows = windows_fn(key)
        if not windows:
            raise ValueError(f"no B2 ability introduction window for {key}")

        allowed = compatible_intro_units(record) if "X-" in key else set()
        if allowed:
            windows = [lid for lid in windows if unit_of(lid) in allowed]
        if not windows:
            raise ValueError(
                f"cross-cutting ability introduction has no mode-compatible lesson: "
                f"home={key} allowed_units={sorted(allowed)}"
            )

        scores = {lid: semantic_score(record, lid) for lid in windows}
        ordered_scores = sorted(scores.values(), reverse=True)
        best = ordered_scores[0]
        second = ordered_scores[1] if len(ordered_scores) > 1 else best
        confidence = best - second
        plans.append((best, confidence, record["item_id"], record, windows, scores))

    # Strong/unique semantic matches get first access to their natural lesson. Generic
    # or tied items fill remaining capacity afterwards.
    plans.sort(key=lambda x: (-x[1], -x[0], x[2]))
    loads: Counter = Counter()
    assigned = {}

    for _, _, _, record, windows, scores in plans:
        under_limit = [lid for lid in windows if loads[lid] < ABILITY_LIMIT]
        candidates = under_limit or list(windows)
        best_score = max(scores[lid] for lid in candidates)
        best = [lid for lid in candidates if scores[lid] == best_score]
        min_load = min(loads[lid] for lid in best)
        best = [lid for lid in best if loads[lid] == min_load]
        idx = ledger.stable_offset(f"ability-semantic:{record['item_id']}", len(best))
        chosen = best[idx]
        assigned[record["item_id"]] = chosen
        loads[chosen] += 1

    return assigned


def build_record_with_routing(category, item, label, homes, intro, plan, order, extra=None):
    record = _original_build_record(category, item, label, homes, intro, plan, order, extra)
    if category == "ability":
        allowed = compatible_intro_units(item) if any(str(h).startswith("X-") for h in homes) else set()
        if allowed and unit_of(intro) not in allowed:
            raise ValueError(
                f"Stage-07 modality routing failed for {item['item_id']}: "
                f"intro={intro} allowed={sorted(allowed)}"
            )
        record["stage_07_intro_routing"] = {
            "reason": "lesson_semantic_match_within_reviewed_stage06_window_with_global_load_guard",
            "source_mode_codes": item.get("mode_codes", []),
            "source_skill_codes": item.get("skill_codes", []),
            "cross_cutting_allowed_intro_units": sorted(allowed),
            "stage_1_homes_unchanged": True,
            "ability_warning_threshold_used_as_soft_capacity": ABILITY_LIMIT,
        }
    return record


ledger.balanced = balanced_with_stage07_semantics
ledger.build_record = build_record_with_routing


if __name__ == "__main__":
    ledger.main()
