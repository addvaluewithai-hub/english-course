#!/usr/bin/env python3
"""Apply explicit B2 Stage-8.5 lifecycle moves and audit role-aware evidence.

This script is non-semantic automation. Exact review-row moves and hotspot dispositions
live in the Stage-8.5 decision artifact. The script may validate/apply/recount only; it
must not invent additional semantic roles or lesson moves.
"""
from __future__ import annotations

import argparse
import copy
import json
from collections import Counter, defaultdict
from pathlib import Path

import build_b2_coverage_ledger as base

ROOT = Path(__file__).resolve().parents[1]
B2 = ROOT / "curriculum/levels/b2"
REVIEW = B2 / "design-review"
DECISIONS = REVIEW / "08.5-role-reconciliation/reconciliation-decisions.json"
BASE_LEDGER = REVIEW / "08-semantic-lock/generated/semantic-role-ledger.json"
MAP_PATH = REVIEW / "05-curriculum-map/curriculum-map.md"
PLAN_PATH = REVIEW / "06-coverage-ledger/lifecycle-plan.json"
TOTAL = 2075
EXPECTED = {"ability":270,"phrase":125,"grammar":243,"word":1427,"pronunciation":10}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def render(c: Counter) -> str:
    return ", ".join(f"{k}: {v}" for k, v in sorted(c.items())) if c else "—"


def lesson_metrics(records: list[dict], lessons: list[str]) -> dict[str, dict]:
    intro: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        lid = r["lifecycle"]["introduce"][0]
        intro[lid].append(r)
    out = {}
    for lid in lessons:
        rs = intro.get(lid, [])
        independent = sum(1 for r in rs if r["semantic_role"]["exit_evidence"] == "independent_possible")
        controlled = sum(1 for r in rs if r["semantic_role"]["exit_evidence"] == "integrated_required" and r["semantic_role"]["mastery_mode"] in {"productive","interactive"})
        support = len(rs) - independent - controlled
        pwords = sum(1 for r in rs if r["category"] == "word" and r["semantic_role"]["mastery_mode"] == "productive")
        pgram_rows = [r for r in rs if r["category"] == "grammar" and r["semantic_role"]["mastery_mode"] == "productive"]
        pgram_systems = sorted({r.get("grammar_system") for r in pgram_rows})
        pphr = sum(1 for r in rs if r["category"] == "phrase" and r["semantic_role"]["mastery_mode"] == "productive" and r["semantic_role"]["control_scope"] == "formulaic")
        out[lid] = {
            "total": len(rs), "independent": independent, "controlled": controlled, "support": support,
            "productive_words": pwords, "productive_grammar_rows": len(pgram_rows),
            "productive_grammar_systems": pgram_systems, "formulaic_phrases": pphr,
        }
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--brief-amendments", type=Path, required=True)
    ap.add_argument("--active-load", type=Path, required=True)
    args = ap.parse_args()

    decisions = load(DECISIONS)
    baseline = load(BASE_LEDGER)
    records = copy.deepcopy(baseline["records"])
    if len(records) != TOTAL or Counter(r["category"] for r in records) != Counter(EXPECTED):
        raise ValueError("Stage-8 baseline ledger drift")

    lessons = base.lesson_ids(MAP_PATH.read_text(encoding="utf-8"))
    if len(lessons) != 95:
        raise ValueError(f"expected 95 lesson slots, got {len(lessons)}")
    order = {lid:i for i,lid in enumerate(lessons)}
    raw_plan = load(PLAN_PATH)
    plan = base.expand_plan(raw_plan, lessons)
    zero_new = set(plan["zero_new_lessons"])

    baseline_roles = {r["item_id"]: copy.deepcopy(r["semantic_role"]) for r in records}
    baseline_homes = {r["item_id"]: tuple(r.get("homes", [])) for r in records}
    baseline_metrics = lesson_metrics(records, lessons)

    grammar_by_row = {int(r["review_row"]): r for r in records if r["category"] == "grammar"}
    overrides = {int(k):v for k,v in decisions["grammar_review_row_intro_overrides"].items()}
    if len(overrides) != len(decisions["grammar_review_row_intro_overrides"]):
        raise ValueError("duplicate numeric grammar override row")

    applied = []
    for row, move in sorted(overrides.items()):
        rec = grammar_by_row.get(row)
        if rec is None:
            raise ValueError(f"Stage-8.5 override row {row} missing from exact grammar ledger")
        old = rec["lifecycle"]["introduce"]
        if old != [move["from"]]:
            raise ValueError(f"row {row} baseline intro drift: {old} != {[move['from']]}")
        target = move["to"]
        if target not in order:
            raise ValueError(f"row {row} target lesson does not exist: {target}")
        if target in zero_new:
            raise ValueError(f"row {row} would violate zero-new slot {target}")
        if not move.get("reason"):
            raise ValueError(f"row {row} lacks explicit reconciliation reason")

        rec["lifecycle"]["introduce"] = [target]
        homes = rec.get("homes", [])
        rec["lifecycle"]["practice"] = base.later(plan, homes, "practice", order, target, False)
        rec["lifecycle"]["fresh_retrieval"] = base.later(plan, homes, "fresh_retrieval", order, target, True)
        rec["lifecycle"]["recycle"] = base.later(plan, homes, "recycle", order, target, True)
        rec["lifecycle"]["consolidate"] = base.later(plan, homes, "consolidate", order, target, True)
        rec["lifecycle"]["exit_verify"] = base.later(plan, homes, "exit_verify", order, target, True)
        rec["stage_08_5_reconciliation"] = {
            "from": move["from"], "to": target, "reason": move["reason"],
            "decision_source": "explicit_stage08_5_reconciliation_candidate_owner_approval_pending"
        }
        applied.append((row, rec["item_id"], move["from"], target, move["reason"]))

    if len(records) != TOTAL or len({r["item_id"] for r in records}) != TOTAL:
        raise ValueError("Stage-8.5 exact record accounting drift")
    if Counter(r["category"] for r in records) != Counter(EXPECTED):
        raise ValueError("Stage-8.5 category accounting drift")

    for r in records:
        iid = r["item_id"]
        if r["semantic_role"] != baseline_roles[iid]:
            raise ValueError(f"Stage-8.5 changed semantic role for {iid}")
        if tuple(r.get("homes", [])) != baseline_homes[iid]:
            raise ValueError(f"Stage-8.5 changed semantic homes for {iid}")
        intro = r["lifecycle"]["introduce"]
        if len(intro) != 1:
            raise ValueError(f"{iid} no longer has exactly one introduction")
        ii = order[intro[0]]
        if not r["lifecycle"].get("practice"):
            raise ValueError(f"{iid} has no practice path after reconciliation")
        if not r["lifecycle"].get("fresh_retrieval"):
            raise ValueError(f"{iid} has no later fresh retrieval after reconciliation")
        if not r["lifecycle"].get("exit_verify"):
            raise ValueError(f"{iid} has no role-appropriate exit path after reconciliation")
        if any(order[x] <= ii for x in r["lifecycle"]["fresh_retrieval"]):
            raise ValueError(f"{iid} fresh retrieval is not later than introduction")
        if any(order[x] <= ii for x in r["lifecycle"]["exit_verify"]):
            raise ValueError(f"{iid} exit verification is not later than introduction")

    actual_zero = {lid for lid in lessons if not any(r["lifecycle"]["introduce"] == [lid] for r in records)}
    if actual_zero != zero_new or len(actual_zero) != 18:
        raise ValueError(f"Stage-8.5 zero-new drift: {sorted(actual_zero ^ zero_new)}")

    mastery = Counter(r["semantic_role"]["mastery_mode"] for r in records)
    if dict(sorted(mastery.items())) != baseline["mastery_counts"]:
        raise ValueError("Stage-8.5 changed Stage-8 mastery-role counts")

    reconciled_metrics = lesson_metrics(records, lessons)
    hotspots = decisions["manual_hotspot_dispositions"]
    for lid in hotspots:
        if lid not in reconciled_metrics:
            raise ValueError(f"hotspot disposition references unknown lesson {lid}")

    out = copy.deepcopy(baseline)
    out["status"] = "stage08_5_lifecycle_reconciled_from_explicit_candidate_moves_owner_approval_pending"
    out["stage_08_5"] = {
        "applied_exact_grammar_row_moves": len(applied),
        "semantic_roles_changed": 0,
        "semantic_homes_changed": 0,
        "zero_new_slots": len(actual_zero),
        "owner_human_approval_pending": True,
    }
    out["records"] = records
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    args.ledger.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = [
        "# B2 Stage 8.5 — Role-aware Lifecycle and Load Reconciliation", "",
        "Status: **AI-ASSISTED RECONCILIATION CANDIDATE — OWNER HUMAN APPROVAL PENDING**", "",
        f"- exact semantic-role records preserved: **{len(records)} / 2,075**",
        f"- explicit exact grammar review-row moves applied: **{len(applied)}**",
        "- semantic/control roles changed in Stage 8.5: **0**",
        "- Stage-1 semantic homes changed: **0**",
        "- lifecycle records lacking later fresh retrieval: **0**",
        "- lifecycle records lacking later exit verification: **0**",
        f"- zero-new transfer/exit slots preserved: **{len(actual_zero)} / 18**",
        "- lesson-design authorization changed: **no**", "",
        "## Exact reconciliation moves", "",
        "| Grammar review row | From | To | Reason |", "|---:|---|---|---|",
    ]
    for row, _, src, dst, reason in applied:
        report.append(f"| {row} | {src} | {dst} | {reason} |")
    report += ["", "## Manual role-aware hotspot dispositions", ""]
    for lid, disposition in hotspots.items():
        b = baseline_metrics[lid]; a = reconciled_metrics[lid]
        report += [
            f"### {lid}", "",
            f"- before: independent {b['independent']}; controlled {b['controlled']}; productive words {b['productive_words']}; productive grammar rows {b['productive_grammar_rows']} ({', '.join(b['productive_grammar_systems']) or 'none'}); formulaic phrases {b['formulaic_phrases']}",
            f"- after: independent {a['independent']}; controlled {a['controlled']}; productive words {a['productive_words']}; productive grammar rows {a['productive_grammar_rows']} ({', '.join(a['productive_grammar_systems']) or 'none'}); formulaic phrases {a['formulaic_phrases']}",
            f"- critic decision: **{disposition}**", "",
        ]
    report += [
        "## Reconciliation verdict", "",
        "**CANDIDATE PASS — Stage-8 roles can be reconciled with the 13-unit / 95-slot architecture after the exact grammar reroutes above.**",
        "The pass does not mean every source row is a separate teaching object and does not authorize lesson design. High row counts that remain are accepted only where the records collapse into a small coherent set of bounded systems or contextual lexical resources serving one communicative performance.",
        "Owner human approval remains required before Stage 9 authorization.",
    ]
    args.report.write_text("\n".join(report) + "\n", encoding="utf-8")

    amend = [
        "# B2 Stage 8.5 — Lesson Brief Reconciliation Amendments", "",
        "Status: **AUTHORITATIVE CANDIDATE OVERLAY FOR STAGE-7 BRIEFS — OWNER HUMAN APPROVAL PENDING**", "",
        "Only the exact grammar introductions listed below change. All other Stage-7 brief outcomes, zero-new slots, source IDs, semantic homes, and Stage-8 roles remain unchanged. Stage 9 should fold this overlay into the final controlled-authoring contract rather than treating the older pre-reconciliation grammar placement as authoritative.", "",
    ]
    by_lesson = defaultdict(lambda: {"in":[], "out":[]})
    for row, iid, src, dst, reason in applied:
        by_lesson[src]["out"].append((row, iid, dst, reason))
        by_lesson[dst]["in"].append((row, iid, src, reason))
    for lid in lessons:
        changes = by_lesson.get(lid)
        if not changes:
            continue
        amend += [f"## {lid}", ""]
        for row, iid, other, reason in changes["out"]:
            amend.append(f"- MOVE OUT grammar review row **{row}** (`{iid}`) → **{other}**. {reason}")
        for row, iid, other, reason in changes["in"]:
            amend.append(f"- MOVE IN grammar review row **{row}** (`{iid}`) ← **{other}**. {reason}")
        a = reconciled_metrics[lid]
        amend.append(f"- reconciled active signature: independent **{a['independent']}**, controlled **{a['controlled']}**, productive words **{a['productive_words']}**, productive grammar rows **{a['productive_grammar_rows']}** across **{len(a['productive_grammar_systems'])}** productive systems, formulaic phrases **{a['formulaic_phrases']}**.")
        amend.append("")
    args.brief_amendments.write_text("\n".join(amend) + "\n", encoding="utf-8")

    active = [
        "# B2 Stage 8.5 — Reconciled Active-load Audit", "",
        "Status: **GENERATED FROM EXPLICIT STAGE-8.5 MOVES — NOT AN AUTHORIZATION**", "",
        "| Lesson | Independent | Controlled | Support | Productive words | Productive grammar rows | Productive grammar systems | Formulaic phrases | Total new |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    maxima = Counter()
    for lid in lessons:
        m = reconciled_metrics[lid]
        active.append(f"| {lid} | {m['independent']} | {m['controlled']} | {m['support']} | {m['productive_words']} | {m['productive_grammar_rows']} | {len(m['productive_grammar_systems'])} | {m['formulaic_phrases']} | {m['total']} |")
        for key in ("independent","controlled","productive_words","productive_grammar_rows","formulaic_phrases"):
            maxima[key] = max(maxima[key], m[key])
        maxima["productive_grammar_systems"] = max(maxima["productive_grammar_systems"], len(m["productive_grammar_systems"]))
    active += ["", "## Reconciled maxima — critic signals only", "",
               f"- independent source abilities in one lesson: **{maxima['independent']}**",
               f"- controlled resources in one lesson: **{maxima['controlled']}**",
               f"- productive words in one lesson: **{maxima['productive_words']}**",
               f"- productive grammar rows in one lesson: **{maxima['productive_grammar_rows']}**",
               f"- productive grammar systems in one lesson: **{maxima['productive_grammar_systems']}**",
               f"- formulaic productive phrases in one lesson: **{maxima['formulaic_phrases']}**",
               "", "These are inspection signals, not silently raised or newly invented authorization thresholds."]
    args.active_load.write_text("\n".join(active) + "\n", encoding="utf-8")

    print("B2 STAGE-08.5 RECONCILIATION CANDIDATE PASS")
    print(f"records={TOTAL} exact_moves={len(applied)} zero_new={len(actual_zero)} semantic_roles_changed=0 owner_approval_pending=true")
    print(f"U6-L04 productive_grammar_rows {baseline_metrics['U6-L04']['productive_grammar_rows']} -> {reconciled_metrics['U6-L04']['productive_grammar_rows']}")


if __name__ == "__main__":
    main()
