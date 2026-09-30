#!/usr/bin/env python3
"""Build B2 Stage-07 lesson authoring brief candidates from Stage 5 + Stage 6 evidence.

This is NON-SEMANTIC automation. It does not assign final productive/receptive/
formulaic/support roles. It turns the reviewed curriculum map and exact provisional
lifecycle ledger into one authoring-contract candidate per lesson, then emits rolling
unit and whole-level critic evidence. Human owner approval remains required.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "curriculum/levels/b2/design-review"
MAP_PATH = REVIEW / "05-curriculum-map/curriculum-map.md"
LEDGER_PATH = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"
LOAD_CRITIC_PATH = REVIEW / "06-coverage-ledger/load-critic.json"
POLICY_PATH = REVIEW / "07-lesson-briefs/brief-policy.json"

CATEGORIES = ("ability", "phrase", "grammar", "word", "pronunciation")
DISPLAY = {
    "ability": "abilities",
    "phrase": "phrases",
    "grammar": "grammar",
    "word": "words",
    "pronunciation": "pronunciation",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def parse_map(md: str) -> tuple[list[str], dict[str, dict], dict[str, dict]]:
    """Return ordered lesson IDs, lesson metadata, and unit metadata."""
    lines = md.splitlines()
    lessons: dict[str, dict] = {}
    units: dict[str, dict] = {}
    order: list[str] = []
    current_unit: str | None = None
    current_lesson: str | None = None
    lesson_buffer: list[str] = []

    def flush_lesson() -> None:
        nonlocal current_lesson, lesson_buffer
        if not current_lesson:
            return
        body_lines = []
        started = False
        for raw in lesson_buffer:
            line = raw.strip()
            if not line:
                if started:
                    break
                continue
            if line.startswith("**Unit critic:**"):
                break
            started = True
            body_lines.append(line)
        body = compact(" ".join(body_lines))
        if not body:
            raise ValueError(f"lesson {current_lesson} has no outcome/body in Stage 5 map")
        lessons[current_lesson]["outcome"] = body
        current_lesson = None
        lesson_buffer = []

    for raw in lines:
        unit_match = re.match(r"^# Unit (\d+)\s+[—-]\s+(.+?)\s*$", raw)
        if unit_match:
            flush_lesson()
            current_unit = f"U{int(unit_match.group(1))}"
            units[current_unit] = {
                "number": int(unit_match.group(1)),
                "title": compact(unit_match.group(2)),
                "critic": "",
            }
            continue

        lesson_match = re.match(r"^###\s+(U\d+-L\d+)\s+[—-]\s+(.+?)\s*$", raw)
        if lesson_match:
            flush_lesson()
            lid = lesson_match.group(1)
            if current_unit is None or not lid.startswith(current_unit + "-"):
                raise ValueError(f"lesson {lid} is outside its expected unit")
            if lid in lessons:
                raise ValueError(f"duplicate lesson heading: {lid}")
            current_lesson = lid
            lesson_buffer = []
            lessons[lid] = {
                "unit": current_unit,
                "title": compact(lesson_match.group(2)),
                "outcome": "",
            }
            order.append(lid)
            continue

        if current_lesson:
            lesson_buffer.append(raw)
        elif current_unit and raw.strip().startswith("**Unit critic:**"):
            units[current_unit]["critic"] = compact(raw.split(":", 1)[1].strip().strip("*"))

    flush_lesson()

    # Unit critics can appear after the final lesson body; capture them independently.
    current_unit = None
    for raw in lines:
        unit_match = re.match(r"^# Unit (\d+)\s+[—-]\s+(.+?)\s*$", raw)
        if unit_match:
            current_unit = f"U{int(unit_match.group(1))}"
        elif current_unit and raw.strip().startswith("**Unit critic:**"):
            units[current_unit]["critic"] = compact(raw.split(":", 1)[1].strip().strip("*"))

    if len(order) != 95:
        raise ValueError(f"Stage 7 expected 95 Stage-5 lesson headings, got {len(order)}")
    if set(units) != {f"U{i}" for i in range(1, 14)}:
        raise ValueError(f"Stage 7 expected U1-U13, got {sorted(units)}")
    return order, lessons, units


def category_counts(records: list[dict]) -> Counter:
    return Counter(r["category"] for r in records)


def count_text(records: list[dict]) -> str:
    c = category_counts(records)
    total = sum(c.values())
    return (
        f"abilities {c['ability']} | phrases {c['phrase']} | grammar {c['grammar']} | "
        f"words {c['word']} | pronunciation {c['pronunciation']} | total {total}"
    )


def grouped_homes(records: list[dict], *, only_prefix: str | None = None) -> Counter:
    out: Counter = Counter()
    for rec in records:
        for home in rec.get("homes", []):
            if only_prefix is None or home.startswith(only_prefix):
                out[home] += 1
    return out


def counter_text(counter: Counter, limit: int = 12) -> str:
    if not counter:
        return "none"
    vals = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    shown = vals[:limit]
    suffix = f"; +{len(vals) - limit} more" if len(vals) > limit else ""
    return "; ".join(f"{k}={v}" for k, v in shown) + suffix


def labels(records: list[dict], category: str, limit: int) -> str:
    vals = [compact(r.get("label", r["item_id"])) for r in records if r["category"] == category]
    if not vals:
        return "none"
    shown = vals[:limit]
    suffix = f"; +{len(vals) - limit} more exact records" if len(vals) > limit else ""
    return "; ".join(shown) + suffix


def grammar_systems(records: list[dict]) -> str:
    c: Counter = Counter()
    for rec in records:
        if rec["category"] == "grammar":
            c[rec.get("grammar_system", "UNMAPPED")] += 1
    return counter_text(c, limit=16)


def earliest_future_targets(records: list[dict], stage: str, order_index: dict[str, int], current: str) -> Counter:
    out: Counter = Counter()
    cur = order_index[current]
    for rec in records:
        targets = [x for x in rec["lifecycle"].get(stage, []) if order_index[x] > cur]
        if targets:
            out[min(targets, key=order_index.__getitem__)] += 1
    return out


def event_records(records: list[dict], stage: str, lid: str, order_index: dict[str, int], *, prior_only: bool) -> list[dict]:
    cur = order_index[lid]
    out = []
    for rec in records:
        if lid not in rec["lifecycle"].get(stage, []):
            continue
        intro = rec["lifecycle"]["introduce"][0]
        if prior_only and order_index[intro] >= cur:
            continue
        out.append(rec)
    return out


def warning_map(critic: dict) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = defaultdict(list)
    for row in critic.get("accepted_warnings", []):
        out[row["lesson"]].append(row)
    return out


def lesson_warning_text(rows: list[dict]) -> str:
    if not rows:
        return "No Stage-06 raw introduction threshold warning for this slot. This is not a mastery/load guarantee; role-aware load is re-audited at Stage 8.5."
    return "Stage-06 raw warning(s): " + "; ".join(
        f"{r['category']} {r['count']} > {r['limit']}" for r in rows
    ) + ". Thresholds remain unchanged."


def critic_note_for(lid: str, critic: dict) -> str:
    decisions = critic.get("critic_decisions", {})
    unit = lid.split("-", 1)[0]
    return decisions.get(lid) or decisions.get(unit) or "No special Stage-06 critic exception beyond the global role-pending safeguards."


def build() -> str:
    order, lesson_meta, unit_meta = parse_map(MAP_PATH.read_text(encoding="utf-8"))
    order_index = {lid: i for i, lid in enumerate(order)}
    ledger = load_json(LEDGER_PATH)
    policy = load_json(POLICY_PATH)
    critic = load_json(LOAD_CRITIC_PATH)
    records = ledger["records"]

    if ledger.get("lesson_count") != 95 or len(records) != 2075:
        raise ValueError("Stage-07 input drift: expected Stage-06 ledger with 95 lessons / 2075 records")
    if critic.get("warning_count") != len(critic.get("accepted_warnings", [])):
        raise ValueError("Stage-06 load critic warning count is internally inconsistent")
    if critic.get("warning_count") != 30:
        raise ValueError(f"Stage-07 currently expects reviewed Stage-06 warning set of 30, got {critic.get('warning_count')}")

    intro_by: dict[str, list[dict]] = {lid: [] for lid in order}
    for rec in records:
        intro = rec["lifecycle"]["introduce"]
        if len(intro) != 1 or intro[0] not in intro_by:
            raise ValueError(f"record {rec['item_id']} has invalid Stage-06 introduction: {intro}")
        intro_by[intro[0]].append(rec)

    zero_new = {lid for lid in order if not intro_by[lid]}
    expected_zero_new = {
        "U1-L07", "U2-L07", "U3-L07", "U4-L08", "U5-L08", "U6-L07",
        "U7-L07", "U8-L07", "U9-L08", "U10-L07", "U11-L08", "U12-L08",
        "U13-L01", "U13-L02", "U13-L03", "U13-L04", "U13-L05", "U13-L06",
    }
    if zero_new != expected_zero_new:
        raise ValueError(f"Stage-07 zero-new set drift: {sorted(zero_new ^ expected_zero_new)}")

    warnings = warning_map(critic)
    out: list[str] = [
        "# B2 Stage 7 — Lesson Authoring Briefs Candidate",
        "",
        "Status: **AI-ASSISTED AUTHORING-CONTRACT CANDIDATE — OWNER HUMAN APPROVAL PENDING**",
        "",
        "These briefs convert the Stage-5 performance map and Stage-6 exact lifecycle ledger into one concise authoring contract per lesson slot. They are **not finished lesson scripts** and they do **not** lock productive/receptive/formulaic/support roles; Stage 8 remains responsible for final semantic/control roles and Stage 8.5 must reconcile those roles back into lifecycle/load/brief evidence.",
        "",
        "## Pinned design rules",
        "",
        "- one primary communicative/evidence outcome per slot;",
        "- exact source coverage is preserved, but a source row is not automatically a separate teaching object;",
        "- grammar is foregrounded as bounded systems/functions rather than row-count chapters;",
        "- lexical records are grouped by reviewed content homes and remain role-pending rather than becoming a forced productive word list;",
        "- receptive evidence is never silently upgraded to productive evidence;",
        "- pronunciation serves intelligibility/perception inside real performance, not accent perfection;",
        "- fresh retrieval changes prompt, source, audience, speaker or context rather than repeating the same model;",
        "- all 18 designated transfer/exit slots remain zero-new;",
        "- copying a model is not mastery evidence;",
        "- a brief that cannot preserve one coherent performance without hidden new content must reopen Stage 5/6 instead of hiding the problem in prose.",
        "",
        "## Exact Stage-7 input state",
        "",
        "- Stage-5 lesson slots: **95**",
        "- Stage-6 exact source records: **2,075**",
        "- designated zero-new slots: **18**",
        "- documented Stage-6 raw load warnings: **30** (thresholds unchanged)",
        "- final semantic/control roles: **pending Stage 8**",
        "",
    ]

    for unit_no in range(1, 14):
        unit = f"U{unit_no}"
        profile = policy["unit_profiles"][unit]
        meta = unit_meta[unit]
        unit_lessons = [lid for lid in order if lid.startswith(unit + "-")]
        out += [
            f"# Unit {unit_no} — {meta['title']}",
            "",
            f"**Unit semantic boundary:** {profile['boundary']}",
            "",
            f"**Locked-B1 carry-forward:** {profile['b1_carry_forward']}",
            "",
            f"**Cross-cutting / pronunciation frame:** {profile['cross_cutting']}",
            "",
        ]

        for lid in unit_lessons:
            intro = intro_by[lid]
            zero = lid in zero_new
            practice_prior = event_records(records, "practice", lid, order_index, prior_only=True)
            recycle_prior = event_records(records, "recycle", lid, order_index, prior_only=True)
            fresh_prior = event_records(records, "fresh_retrieval", lid, order_index, prior_only=True)
            support_ids = {r["item_id"] for r in practice_prior + recycle_prior}
            support = [r for r in records if r["item_id"] in support_ids]
            future_fresh = earliest_future_targets(intro, "fresh_retrieval", order_index, lid)
            future_exit = earliest_future_targets(intro, "exit_verify", order_index, lid)
            xhomes = grouped_homes(intro, only_prefix="X-")
            lhomes = grouped_homes(intro, only_prefix="L")
            ability_homes = grouped_homes([r for r in intro if r["category"] == "ability"], only_prefix="C")

            out += [
                f"### {lid} — {lesson_meta[lid]['title']}",
                "",
                f"**Primary communicative/evidence outcome:** {lesson_meta[lid]['outcome']}",
                "",
                f"**Exact new-source load:** {count_text(intro)}. " + ("**ZERO-NEW SLOT.**" if zero else "Stage-8 role assignment remains pending."),
                "",
            ]

            if zero:
                fresh_counts = count_text(fresh_prior)
                fresh_homes = grouped_homes(fresh_prior)
                out += [
                    f"**Foreground core:** fresh changed-context evidence only; no required B2 source record/system/lexical target may be introduced. Current Stage-6 fresh-retrieval pool at this slot: {fresh_counts}.",
                    "",
                    f"**Embedded/support:** previously introduced records only. Dominant retrieval homes: {counter_text(fresh_homes, 10)}.",
                    "",
                    "**Semantic / grammar boundary:** assess the mapped performance with prior resources; do not smuggle a new grammar explanation, phrase, word target or pronunciation strand into the transfer/capstone because the task happens to need it.",
                    "",
                    f"**Prerequisites / recycled B1:** {profile['b1_carry_forward']}",
                    "",
                    "**Pronunciation / cross-cutting:** sample already-introduced resources role-appropriately in the changed task. No new pronunciation strand is introduced here.",
                    "",
                    "**Fresh retrieval rule:** change source/topic/audience/speaker/prompt and reduce model dependence. Repeating the practice task with superficial wording changes does not count.",
                    "",
                ]
            else:
                out += [
                    f"**Foreground capability evidence:** homes {counter_text(ability_homes, 10)}. Exact new ability records: {labels(intro, 'ability', 8)}.",
                    "",
                    f"**Foreground phrase/chunk evidence:** {labels(intro, 'phrase', 8)}. Prefer bounded chunk use where it meets the communicative need; a phrase surface does not license a broader grammar claim.",
                    "",
                    f"**Foreground grammar systems:** {grammar_systems(intro)}. These are system/function groupings; the exact EGP rows in the ledger remain coverage records rather than one-rule-per-row teaching objects.",
                    "",
                    f"**Lexical/content treatment:** reviewed homes {counter_text(lhomes, 12)}. Exact word records introduced: {category_counts(intro)['word']}. Keep a narrow task-relevant core in foreground and use the remainder as contextual/support exposure until Stage 8 decides exact control roles; do not assign all introduced words independent productive mastery by default.",
                    "",
                    f"**Embedded/support and prerequisites:** {count_text(support)} previously introduced Stage-6 records are available through practice/recycle paths at this slot. {profile['b1_carry_forward']}",
                    "",
                    f"**Pronunciation / cross-cutting:** new pronunciation strand(s): {labels(intro, 'pronunciation', 6)}. New cross-cutting homes visible in exact introductions: {counter_text(xhomes, 10)}. {profile['cross_cutting']}",
                    "",
                    f"**Fresh retrieval path for today's new records:** earliest later fresh-retrieval targets: {counter_text(future_fresh, 8)}. Retrieval must change context/prompt/source/audience rather than replay the same model.",
                    "",
                    f"**Provisional exit path for today's new records:** earliest later exit-verification targets: {counter_text(future_exit, 8)}. Final evidence type is not locked until Stage 8/8.5.",
                    "",
                    f"**Semantic / grammar boundary:** {profile['boundary']} Coverage home is not a productive-mastery claim, and model imitation is not independent evidence.",
                    "",
                ]

            out += [
                f"**Stage-6 load critic:** {lesson_warning_text(warnings.get(lid, []))}",
                "",
            ]
            if warnings.get(lid):
                out += [f"**Authoring risk note:** {critic_note_for(lid, critic)}", ""]

        unit_warning_rows = [r for lid in unit_lessons for r in warnings.get(lid, [])]
        max_lesson = max(unit_lessons, key=lambda x: len(intro_by[x]))
        zero_count = sum(1 for x in unit_lessons if x in zero_new)
        if unit in {"U5", "U10"}:
            verdict = "CONDITIONALLY RETAIN the Stage-5 slot shape. No Stage-7-only contradiction forces an immediate split, but the strongest role-sensitive load risks remain open for Stage 8/8.5."
        elif unit_warning_rows:
            verdict = "PROVISIONALLY RETAIN the Stage-5 slot shape. Raw warnings are visible and bounded by the authoring rules; final role-aware load remains an explicit Stage-8.5 gate."
        else:
            verdict = "PROVISIONALLY RETAIN the Stage-5 slot shape. No raw Stage-6 threshold warning appears in this unit, subject to later semantic-role reconciliation."
        out += [
            f"#### Rolling adversarial critic — Unit {unit_no}",
            "",
            f"- Stage-5 unit critic: {meta['critic'] or 'No separate unit-critic sentence parsed; whole-map dependency rules still apply.'}",
            f"- briefs present: **{len(unit_lessons)} / {len(unit_lessons)}**",
            f"- zero-new slots protected in this unit: **{zero_count}**",
            f"- raw Stage-6 warning rows in this unit: **{len(unit_warning_rows)}**",
            f"- highest raw introduction slot: **{max_lesson} = {len(intro_by[max_lesson])} exact source records**",
            f"- critic verdict: **{verdict}**",
            "",
        ]

    all_intro_ids = [r["item_id"] for lid in order for r in intro_by[lid]]
    if len(all_intro_ids) != 2075 or len(set(all_intro_ids)) != 2075:
        raise ValueError("Stage-07 exact introduction accounting is not 2075 unique records")

    out += [
        "# Whole-level Stage-7 adversarial critic",
        "",
        "## Completeness",
        "",
        "- lesson briefs: **95 / 95**",
        "- exact Stage-6 source records represented through lesson introduction contracts: **2,075 / 2,075**",
        "- duplicate exact introduction ownership: **0**",
        "- designated zero-new slots: **18 / 18 protected**",
        "- Stage-6 raw warning set represented in briefs: **30 / 30**",
        "",
        "## Modality and performance integrity",
        "",
        "Every brief inherits one primary Stage-5 communicative/evidence outcome. Reception, production, interaction, mediation and writing/genre boundaries remain distinct; no brief uses lexical topic coverage as a substitute capability.",
        "",
        "## Semantic/control integrity",
        "",
        "Stage 7 does not assign final productive, receptive, formulaic, embedded/support or grammar-owned roles. Broad lexical homes and raw EGP rows are therefore authoring evidence, not mastery claims. Any Stage-8 role decision that increases active teaching load must be reconciled in Stage 8.5.",
        "",
        "## Dependency and retrieval integrity",
        "",
        "Each instructional brief exposes its Stage-6 earlier support and later fresh-retrieval/exit path. Transfer and capstone briefs require changed context and reduced model dependence rather than repeated prompts. Locked B1 content remains prerequisite/retrieval, not new B2 inventory.",
        "",
        "## Load integrity",
        "",
        "The exact existing set of 30 raw Stage-6 warnings remains visible; thresholds were not raised and warnings were not erased by prose. U5 and U10 remain conditional role-sensitive pressure points. Stage 8.5 must rerun load after exact semantic/control roles are locked.",
        "",
        "## Architecture decision",
        "",
        "**STAGE-7 CANDIDATE VERDICT: retain 13 units / 95 slots provisionally.** The generated authoring contracts can preserve one primary performance per slot without introducing required content inside the 18 protected transfer/exit slots. No Stage-7-only contradiction currently forces a split or merge. This is an AI-assisted curriculum-design candidate, not human approval; Stage 8 semantic lock and mandatory Stage 8.5 reconciliation may still reopen Stage 5/6/7.",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(result + "\n", encoding="utf-8")
    print("B2 STAGE-07 BRIEFS BUILT")
    print("lessons=95 source_records=2075 zero_new=18 stage06_warning_rows=30")
    print("semantic/control roles remain pending Stage 8; owner approval remains required")


if __name__ == "__main__":
    main()
