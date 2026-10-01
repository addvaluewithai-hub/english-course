#!/usr/bin/env python3
"""Run the B2 Stage-06 ledger with Stage-07 lesson-semantic routing feedback.

Stage 06 proved exact coverage/lifecycle completeness. Stage 07 authoring inspection then
exposed a narrower scheduling issue: round-robin balancing inside a valid capability or
cross-cutting home can still place a source ability in the wrong *lesson* inside that
reviewed window.

This wrapper keeps Stage-1 semantic homes authoritative and keeps all scheduling inside
the Stage-06 reviewed introduction windows. It adds bounded Stage-07 feedback:
1. SUPPORTING X-* rows cannot first appear in a clearly incompatible modality block.
2. Direct C01-C18 rows use explicit subfunction-to-lesson routing where Stage 5 provides
   a clear boundary (e.g. C08 procedure -> U4-L02, trend -> U4-L05, narrative -> U4-L04).
3. Remaining rows use source-text/function similarity against the Stage-5 lesson outcome.
4. A global soft capacity of 9 ability introductions per lesson prevents generic semantic
   similarity from collapsing an entire capability into one lesson; explicit high-signal
   routes remain visible if they genuinely exceed that capacity.

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


def source_text(record: dict) -> str:
    return " ".join(
        [
            str(record.get("source_text", "")),
            " ".join(str(x) for x in record.get("function_codes", [])),
            " ".join(str(x) for x in record.get("skill_codes", [])),
        ]
    ).lower()


def has(text: str, *terms: str) -> bool:
    return any(term in text for term in terms)


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


def explicit_lesson(key: str, record: dict) -> str | None:
    """Return a high-confidence Stage-5 sublesson home for direct capability rows."""
    text = source_text(record)

    if key == "C01":
        if has(text, "purpose", "intended audience", "persuad", "rhetorical question"):
            return "U1-L04"
        if has(text, "irony", "tone", "attitude", "connotation", "enthusiasm", "reluctance", "scept"):
            return "U1-L05"
        if has(text, "contrasting argument", "differences and similarities", "points of view", "viewpoints"):
            return "U1-L03"
        if has(text, "conclusion", "claim", "main argument", "supporting reason"):
            return "U1-L01"
        if has(text, "fact and opinion", "fact from opinion", "evidence"):
            return "U1-L02"

    if key == "C02":
        if has(text, "diagram", "visual information", "graph", "chart", "table"):
            return "U2-L02"
        if has(text, "different sources", "related texts", "compare information", "synthes"):
            return "U2-L03"
        if has(text, "scan", "specific information", "supporting details", "locate information"):
            return "U2-L01"

    if key == "C03":
        if has(text, "correspondence", "questionnaire", "form", "letter", "email", "application"):
            return "U2-L05"
        if has(text, "instruction", "technical information", "specification", "advice", "procedure"):
            return "U2-L04"

    if key == "C05":
        if has(text, "tv ", "television", "radio", "news", "documentar", "film", "broadcast", "current affairs"):
            return "U3-L03"
        if has(text, "specific detail", "details", "examples", "chronological", "sequence", "relevant and irrelevant", "poor quality public announcement"):
            return "U3-L02"
        return "U3-L01"

    if key == "C06":
        if has(text, "attitude", "point of view", "ironic", "irony", "concern", "avoiding answering", "rhetorical", "certainty", "tone", "intention"):
            return "U3-L05"
        return "U3-L04"

    if key == "C08":
        if has(text, "instruction", "how to do", "procedure", "how to carry out", "technical instructions"):
            return "U4-L02"
        if has(text, "trend", "change over time", "quantities", "increase", "decrease"):
            return "U4-L05"
        if has(text, "story", "plot", "narrat", "event", "experience", "life changing", "feelings and reactions", "personal significance"):
            return "U4-L04"
        if has(text, "presentation", "announcement", "announce", "from notes"):
            return "U4-L06"
        if has(text, "fluently", "long contribution", "linking words", "keep the turn", "stock phrases", "monitor speech", "intelligib"):
            return "U4-L07"
        if has(text, "financial problem", "issue or problem", "factual information", "work", "field", "goals", "necessity", "objective way"):
            return "U4-L03"
        if has(text, "describe", "description", "people", "personality", "places", "objects", "possessions", "products", "characteristics"):
            return "U4-L01"

    if key == "C09":
        if has(text, "recommend", "solution", "solutions", "priority", "action"):
            return "U5-L03"
        if has(text, "advantages", "disadvantages", "compare", "evaluate", "criteria", "options"):
            return "U5-L02"
        if has(text, "cause", "consequence", "linked change"):
            return "U5-L04"
        return "U5-L01"

    if key == "C10":
        if has(text, "past", "regret", "missed", "causes of an issue"):
            return "U5-L06"
        if has(text, "hypothetical", "would do", "counterfactual", "imagined"):
            return "U5-L07"
        return "U5-L05"

    if key == "C11":
        if has(text, "misunderstanding", "clarif", "reformulat", "repair", "lexical gap"):
            return "U6-L05"
        if has(text, "spontaneous", "unexpected", "changing information", "changes of direction"):
            return "U6-L06"
        if has(text, "disagree", "agree", "feelings", "sympathy", "surprise", "tact", "hedg"):
            return "U6-L04"
        if has(text, "redirect", "new perspective", "change topic", "topic"):
            return "U6-L03"
        if has(text, "develop", "another", "other people's", "others'", "build on"):
            return "U6-L02"
        return "U6-L01"

    if key == "C12":
        if has(text, "blame", "challenge", "disagree"):
            return "U7-L05"
        if has(text, "resolve", "dispute", "reach agreement", "less-routine"):
            return "U7-L06"
        if has(text, "request", "demand", "complaint"):
            return "U7-L02"
        if has(text, "constraint", "compromise", "non-negotiable", "priority"):
            return "U7-L03"
        if has(text, "solution", "alternative", "proposal", "propose", "remedy"):
            return "U7-L04"
        return "U7-L01"

    if key == "C13":
        if has(text, "handle presentation questions", "presentation questions", "respond to questions"):
            return "U8-L06"
        if has(text, "presentation", "present "):
            return "U8-L05"
        if has(text, "interview", "survey"):
            return "U8-L03"
        if has(text, "formal discussion", "meeting"):
            return "U8-L04"
        if has(text, "ask", "question"):
            return "U8-L01"
        return "U8-L02"

    if key == "C14":
        if has(text, "misunderstanding", "clarif", "reframe"):
            return "U9-L06"
        if has(text, "facilitat", "connect", "develop others"):
            return "U9-L07"
        if has(text, "multiple sources", "different sources", "compare information", "integrate"):
            return "U9-L05"
        if has(text, "argument", "positions", "point of view"):
            return "U9-L04"
        if has(text, "summar"):
            return "U9-L03"
        if has(text, "paraphras", "re-express"):
            return "U9-L02"
        return "U9-L01"

    if key == "C15":
        if has(text, "process", "procedure", "instructions", "repair an object"):
            return "U10-L02"
        if has(text, "cause", "change", "development", "consequence"):
            return "U10-L03"
        if has(text, "narrative", "events", "feelings", "personal significance", "story"):
            return "U10-L04"
        if has(text, "edit", "concise", "cohesive", "reference", "repetition"):
            return "U10-L05"
        if has(text, "plan", "check and correct", "spelling", "punctuation", "draft"):
            return "U10-L06"
        return "U10-L01"

    if key == "C16":
        if has(text, "more than one source", "number of sources", "compare information from different sources", "synthesise", "synthesize"):
            return "U11-L06"
        if has(text, "source evidence", "attribute", "sources", "source information"):
            return "U11-L05"
        if has(text, "opposing", "contrasting point", "other people's argument", "other people’s argument"):
            return "U11-L03"
        if has(text, "concede", "qualif", "counter-argument", "counter argument"):
            return "U11-L04"
        if has(text, "advantages", "disadvantages", "compare and evaluate", "criteria"):
            return "U11-L02"
        if has(text, "edit", "audience", "style", "register", "conclusion"):
            return "U11-L07"
        return "U11-L01"

    if key == "C17":
        if has(text, "complaint", "problem message"):
            return "U12-L03"
        if has(text, "application", "enquiry", "invitation", "formal request"):
            return "U12-L02"
        if has(text, "online", "respond", "response chain", "collaborat", "misunderstanding"):
            return "U12-L04"
        return "U12-L01"

    if key == "C18":
        if has(text, "review"):
            return "U12-L06"
        if has(text, "recommend", "problem and solution", "problem-solution", "problem/solution"):
            return "U12-L07"
        return "U12-L05"

    return None


def semantic_score(record: dict, lesson_id: str) -> int:
    text = source_text(record)
    lesson = LESSONS[lesson_id]
    source_tokens = tokens(text)
    title_tokens = tokens(lesson["title"])
    outcome_tokens = tokens(lesson["outcome"])

    score = 5 * len(source_tokens & title_tokens) + 2 * len(source_tokens & outcome_tokens)
    lesson_raw = (lesson["title"] + " " + lesson["outcome"]).lower()
    for group in CONCEPT_GROUPS:
        if any(term in text for term in group) and any(term in lesson_raw for term in group):
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

        explicit = explicit_lesson(key, record)
        if explicit in windows:
            preferred = [explicit]
            route_kind = "explicit_stage5_subfunction"
        else:
            preferred = list(windows)
            route_kind = "semantic_fallback"

        scores = {lid: semantic_score(record, lid) for lid in preferred}
        ordered_scores = sorted(scores.values(), reverse=True)
        best = ordered_scores[0]
        second = ordered_scores[1] if len(ordered_scores) > 1 else best
        confidence = 1000 if route_kind == "explicit_stage5_subfunction" else best - second
        plans.append((confidence, best, record["item_id"], record, windows, preferred, scores, route_kind))

    plans.sort(key=lambda x: (-x[0], -x[1], x[2]))
    loads: Counter = Counter()
    assigned = {}

    for _, _, _, record, all_windows, preferred, scores, route_kind in plans:
        # Explicit Stage-5 subfunction routes are authoritative lesson-level feedback.
        # Fallback routes respect the soft capacity and can move inside the reviewed
        # capability window if their similarity signal is weak/tied.
        if route_kind == "explicit_stage5_subfunction":
            candidates = preferred
        else:
            under_limit = [lid for lid in preferred if loads[lid] < ABILITY_LIMIT]
            candidates = under_limit or [lid for lid in all_windows if loads[lid] < ABILITY_LIMIT] or list(preferred)
            for lid in candidates:
                scores.setdefault(lid, semantic_score(record, lid))

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
        key = "+".join(homes)
        allowed = compatible_intro_units(item) if any(str(h).startswith("X-") for h in homes) else set()
        if allowed and unit_of(intro) not in allowed:
            raise ValueError(
                f"Stage-07 modality routing failed for {item['item_id']}: "
                f"intro={intro} allowed={sorted(allowed)}"
            )
        record["stage_07_intro_routing"] = {
            "reason": "explicit_stage5_subfunction_or_semantic_fallback_within_reviewed_stage06_window",
            "source_mode_codes": item.get("mode_codes", []),
            "source_skill_codes": item.get("skill_codes", []),
            "cross_cutting_allowed_intro_units": sorted(allowed),
            "explicit_lesson_candidate": explicit_lesson(key, item),
            "stage_1_homes_unchanged": True,
            "ability_warning_threshold_used_as_soft_capacity_for_fallbacks": ABILITY_LIMIT,
        }
    return record


ledger.balanced = balanced_with_stage07_semantics
ledger.build_record = build_record_with_routing


if __name__ == "__main__":
    ledger.main()
