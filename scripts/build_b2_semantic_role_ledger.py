#!/usr/bin/env python3
"""Expand explicit B2 Stage-08 candidate decisions into exact role evidence.

Automation here is intentionally non-semantic: it joins already-explicit Stage-08
candidate policy to the exact Stage-06 ledger, validates completeness, counts roles,
and renders review evidence. It must fail rather than invent a missing semantic role.
Owner human approval remains required.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B2 = ROOT / "curriculum/levels/b2"
REVIEW = B2 / "design-review"
SEM = REVIEW / "08-semantic-lock"
DECISIONS = SEM / "semantic-decisions.json"
COVERAGE = REVIEW / "06-coverage-ledger/generated/coverage-ledger.json"

EXPECTED = {"ability":270,"phrase":125,"grammar":243,"word":1427,"pronunciation":10}
TOTAL = 2075
VALID_MASTERY = {"productive","receptive","interactive","integrated_support"}
VALID_SCOPE = {"generative","bounded_pattern","formulaic","contextual","quality_constraint"}
VALID_EXIT = {"independent_possible","integrated_required","support_condition"}
ZERO_NEW = {
    "U1-L07","U2-L07","U3-L07","U4-L08","U5-L08","U6-L07",
    "U7-L07","U8-L07","U9-L08","U10-L07","U11-L08","U12-L08",
    "U13-L01","U13-L02","U13-L03","U13-L04","U13-L05","U13-L06",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_role(role: dict, where: str) -> dict:
    required = {"mastery_mode","control_scope","exit_evidence"}
    if set(role) != required:
        raise ValueError(f"{where}: role keys must be exactly {sorted(required)}")
    if role["mastery_mode"] not in VALID_MASTERY:
        raise ValueError(f"{where}: invalid mastery_mode {role['mastery_mode']}")
    if role["control_scope"] not in VALID_SCOPE:
        raise ValueError(f"{where}: invalid control_scope {role['control_scope']}")
    if role["exit_evidence"] not in VALID_EXIT:
        raise ValueError(f"{where}: invalid exit_evidence {role['exit_evidence']}")
    return dict(role)


def grouped_owner(groups: dict[str,list[str]], label: str) -> dict[str,str]:
    out = {}
    for group, vals in groups.items():
        for val in vals:
            if val in out:
                raise ValueError(f"{label} {val} appears in both {out[val]} and {group}")
            out[val] = group
    return out


def add_role(rec: dict, role: dict, basis: str) -> dict:
    out = dict(rec)
    out["semantic_role"] = validate_role(role, basis)
    out["semantic_decision_basis"] = basis
    out["semantic_decision_source"] = "explicit_ai_assisted_stage08_candidate_owner_approval_pending"
    return out


def render(c: Counter) -> str:
    return ", ".join(f"{k}: {v}" for k,v in sorted(c.items())) if c else "—"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--report", type=Path, required=True)
    ap.add_argument("--lesson-attribution", type=Path, required=True)
    ap.add_argument("--active-load", type=Path, required=True)
    args = ap.parse_args()

    decisions = load(DECISIONS)
    coverage = load(COVERAGE)
    base = coverage.get("records", [])
    counts = Counter(r["category"] for r in base)
    if len(base) != TOTAL or dict(counts) != EXPECTED:
        raise ValueError(f"B2 coverage drift: total={len(base)} counts={dict(counts)}")

    mode_policy = decisions["abilities"]["capability_source_mode_policy"]
    cross_policy = decisions["abilities"]["cross_cutting_home_policy"]
    expected_cross = {
        "X-REFERENCE","X-DISCOURSE","X-REGISTER","X-PRAGMATICS","X-LEXICAL-STRATEGY",
        "X-REPAIR","X-METACOGNITION","X-STANCE","X-PLANNING-AUDIENCE","X-FLUENCY-TURN",
        "X-PRON-STANCE","X-EDITING","X-SOURCE-USE","X-GENRE","X-ACCURACY",
    }
    if set(cross_policy) != expected_cross:
        raise ValueError(f"cross-cutting decision drift: missing={sorted(expected_cross-set(cross_policy))} extra={sorted(set(cross_policy)-expected_cross)}")

    pd = decisions["phrases"]
    phrase_owner = grouped_owner({
        "productive_formulaic": pd["productive_formulaic_homes"],
        "receptive_contextual": pd["receptive_contextual_homes"],
    }, "phrase home")
    gd = decisions["grammar"]
    grammar_owner = grouped_owner({
        "productive_bounded": gd["productive_bounded_systems"],
        "integrated_support": gd["integrated_support_systems"],
    }, "grammar system")
    expected_systems = {f"G{i:02d}" for i in range(1,48)}
    if set(grammar_owner) != expected_systems:
        raise ValueError(f"grammar decisions must cover G01..G47 exactly; missing={sorted(expected_systems-set(grammar_owner))} extra={sorted(set(grammar_owner)-expected_systems)}")
    row_overrides = {int(k):v for k,v in gd.get("review_row_overrides",{}).items()}

    wd = decisions["words"]
    word_owner = grouped_owner({
        "productive_contextual": wd["productive_contextual_homes"],
        "integrated_support": wd["integrated_support_homes"],
        "receptive_contextual": wd["receptive_contextual_homes"],
    }, "word home")
    expected_word_homes = {f"L{i:02d}" for i in range(1,29)} | {"LX-GENERAL"}
    if set(word_owner) != expected_word_homes:
        raise ValueError(f"word decisions must cover L01..L28 + LX-GENERAL exactly; missing={sorted(expected_word_homes-set(word_owner))} extra={sorted(set(word_owner)-expected_word_homes)}")

    pronunciation = decisions["pronunciation"]
    if len(pronunciation) != 10:
        raise ValueError(f"pronunciation decisions must cover 10 exact items, got {len(pronunciation)}")

    records = []
    seen = set()
    seen_phrase_homes, seen_word_homes, seen_systems, seen_cross = set(), set(), set(), set()
    lesson_intro: dict[str,list[dict]] = defaultdict(list)

    for rec in base:
        iid = rec["item_id"]
        if iid in seen:
            raise ValueError(f"duplicate item_id {iid}")
        seen.add(iid)
        cat = rec["category"]

        if cat == "ability":
            modes = rec.get("stage_07_intro_routing",{}).get("source_mode_codes",[])
            if len(modes) != 1:
                raise ValueError(f"ability {iid} lacks exactly one preserved source mode: {modes}")
            mode = modes[0]
            if mode not in mode_policy:
                raise ValueError(f"ability {iid} unsupported source mode {mode}")
            homes = rec.get("homes",[])
            if not homes:
                raise ValueError(f"ability {iid} has no reviewed home")
            if all(h.startswith("C") for h in homes):
                role = dict(mode_policy[mode])
                basis = f"ability.capability_home:{'+'.join(homes)};source_mode:{mode}"
            elif len(homes) == 1 and homes[0].startswith("X-"):
                home = homes[0]
                seen_cross.add(home)
                if home not in cross_policy:
                    raise ValueError(f"ability {iid} cross home lacks decision: {home}")
                role = dict(cross_policy[home])
                if role["mastery_mode"] == "source_mode":
                    role["mastery_mode"] = mode_policy[mode]["mastery_mode"]
                basis = f"ability.cross_cutting_home:{home};source_mode:{mode}"
            else:
                raise ValueError(f"ability {iid} has unsupported mixed homes {homes}")
            out = add_role(rec, role, basis)
            out["source_mode"] = mode

        elif cat == "phrase":
            home = rec["homes"][0]
            seen_phrase_homes.add(home)
            group = phrase_owner.get(home)
            if not group:
                raise ValueError(f"phrase {iid} home lacks explicit role: {home}")
            out = add_role(rec, pd["role_templates"][group], f"phrase.home:{home};group:{group}")

        elif cat == "grammar":
            system = rec.get("grammar_system")
            seen_systems.add(system)
            group = grammar_owner.get(system)
            if not group:
                raise ValueError(f"grammar {iid} system lacks explicit role: {system}")
            row = int(rec["review_row"])
            if row in row_overrides:
                role_name = row_overrides[row]["role"]
                role = gd["role_templates"][role_name]
                basis = f"grammar.review_row_override:{row};system:{system};role:{role_name}"
            else:
                role = gd["role_templates"][group]
                basis = f"grammar.system:{system};group:{group}"
            out = add_role(rec, role, basis)

        elif cat == "word":
            home = rec["homes"][0]
            seen_word_homes.add(home)
            group = word_owner.get(home)
            if not group:
                raise ValueError(f"word {iid} home lacks explicit role: {home}")
            out = add_role(rec, wd["role_templates"][group], f"word.reviewed_home:{home};group:{group}")

        elif cat == "pronunciation":
            if iid not in pronunciation:
                raise ValueError(f"pronunciation {iid} lacks exact Stage-08 decision")
            out = add_role(rec, pronunciation[iid], f"pronunciation.item:{iid}")

        else:
            raise ValueError(f"unknown category {cat}")

        intro = out["lifecycle"]["introduce"]
        if len(intro) != 1:
            raise ValueError(f"{iid} must retain exactly one introduction, got {intro}")
        lesson_intro[intro[0]].append(out)
        records.append(out)

    if len(records) != TOTAL or len(seen) != TOTAL:
        raise ValueError("semantic expansion did not preserve 2075 unique records")
    if seen_systems != expected_systems:
        raise ValueError(f"coverage does not exercise exact G01..G47 set: missing={sorted(expected_systems-seen_systems)}")
    if seen_word_homes != expected_word_homes:
        raise ValueError(f"coverage does not exercise all word homes: missing={sorted(expected_word_homes-seen_word_homes)}")
    if not seen_phrase_homes <= set(phrase_owner):
        raise ValueError(f"unowned phrase homes: {sorted(seen_phrase_homes-set(phrase_owner))}")
    if not seen_cross <= expected_cross:
        raise ValueError(f"unowned cross homes: {sorted(seen_cross-expected_cross)}")

    all_lessons = [f"U{u}-L{l:02d}" for u,n in [(1,7),(2,7),(3,7),(4,8),(5,8),(6,7),(7,7),(8,7),(9,8),(10,7),(11,8),(12,8),(13,6)] for l in range(1,n+1)]
    if len(all_lessons) != 95:
        raise ValueError("internal lesson map is not 95")
    actual_zero = {lid for lid in all_lessons if not lesson_intro.get(lid)}
    if actual_zero != ZERO_NEW:
        raise ValueError(f"semantic expansion changed zero-new set: {sorted(actual_zero ^ ZERO_NEW)}")

    mastery = Counter(r["semantic_role"]["mastery_mode"] for r in records)
    scope = Counter(r["semantic_role"]["control_scope"] for r in records)
    exit_roles = Counter(r["semantic_role"]["exit_evidence"] for r in records)
    by_cat_mastery = defaultdict(Counter)
    by_cat_scope = defaultdict(Counter)
    for r in records:
        by_cat_mastery[r["category"]][r["semantic_role"]["mastery_mode"]] += 1
        by_cat_scope[r["category"]][r["semantic_role"]["control_scope"]] += 1

    ledger = {
        "schema_version":1,
        "level":"B2",
        "status":"expanded_from_explicit_ai_assisted_stage08_candidate_owner_approval_pending",
        "record_count":TOTAL,
        "record_counts":EXPECTED,
        "automation_inferred_semantic_roles":0,
        "candidate_semantic_orphans":0,
        "owner_human_approval_pending":True,
        "mastery_counts":dict(sorted(mastery.items())),
        "control_scope_counts":dict(sorted(scope.items())),
        "exit_evidence_counts":dict(sorted(exit_roles.items())),
        "records":records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

    report = [
        "# B2 Stage 8 Semantic Role Expansion Audit","",
        "Status: **GENERATED FROM EXPLICIT AI-ASSISTED STAGE-08 CANDIDATE DECISIONS — OWNER HUMAN APPROVAL PENDING**","",
        f"- exact records assigned a candidate role: **{len(records)} / {TOTAL}**",
        "- candidate semantic orphans: **0**",
        "- automation-inferred semantic roles: **0**",
        "- lesson-design authorization changed: **no**","",
        "## Category accounting","",
        "| Category | Records | Mastery modes | Control scopes |","|---|---:|---|---|",
    ]
    for cat in ("ability","phrase","grammar","word","pronunciation"):
        report.append(f"| {cat} | {counts[cat]} | {render(by_cat_mastery[cat])} | {render(by_cat_scope[cat])} |")
    report += ["","## Whole-level candidate role counts","",f"- mastery: **{render(mastery)}**",f"- control scope: **{render(scope)}**",f"- exit evidence: **{render(exit_roles)}**","",
        "## Guardrails","",
        "- Reception remains receptive even when a later task asks for a response.",
        "- Interaction retains exchange/response evidence; solo production cannot substitute.",
        "- Mediation keeps its source-mode trace and is assessed through relay/transformation/facilitation.",
        "- Phrase control is source-sense/formula bounded and never licenses a broader grammar system.",
        "- Integrated-support grammar is not an independent productive exit target by default.",
        "- Broad topic and LX-GENERAL vocabulary is not forced into isolated productive recall.",
        "- Pronunciation remains an intelligibility/prosody quality condition, not accent imitation.",
        "- These candidate roles require owner human approval and mandatory Stage 8.5 role-aware lifecycle/load reconciliation before authorization.",
    ]
    args.report.write_text("\n".join(report)+"\n",encoding="utf-8")

    attrib = ["# B2 Stage 8 Lesson Semantic Attribution Aid","","Status: **GENERATED REVIEW AID — OWNER HUMAN APPROVAL PENDING**","",
              "Counts below are introductions after candidate semantic/control roles; they do not change Stage-6 lifecycle ownership.",""]
    active_lines = ["# B2 Stage 8 Active-Load Aid","","Status: **GENERATED ROLE-AWARE LOAD AID FOR STAGE 8.5 — NOT AN AUTHORIZATION**","",
                    "Independent = source abilities with independent evidence. Controlled = productive/interactive/formulaic/contextual resources requiring integrated evidence. Support = receptive/integrated-support records.","",
                    "| Lesson | Independent | Controlled | Support | Productive words | Productive grammar | Formulaic phrases | Total new |","|---|---:|---:|---:|---:|---:|---:|---:|"]
    maxima = Counter()
    for lid in all_lessons:
        rs = lesson_intro.get(lid,[])
        mc = Counter(r["semantic_role"]["mastery_mode"] for r in rs)
        sc = Counter(r["semantic_role"]["control_scope"] for r in rs)
        independent = sum(1 for r in rs if r["semantic_role"]["exit_evidence"] == "independent_possible")
        controlled = sum(1 for r in rs if r["semantic_role"]["exit_evidence"] == "integrated_required" and r["semantic_role"]["mastery_mode"] in {"productive","interactive"})
        support = len(rs)-independent-controlled
        pwords = sum(1 for r in rs if r["category"]=="word" and r["semantic_role"]["mastery_mode"]=="productive")
        pgram = sum(1 for r in rs if r["category"]=="grammar" and r["semantic_role"]["mastery_mode"]=="productive")
        pphr = sum(1 for r in rs if r["category"]=="phrase" and r["semantic_role"]["control_scope"]=="formulaic" and r["semantic_role"]["mastery_mode"]=="productive")
        attrib += [f"## {lid}","",f"- new records: **{len(rs)}**",f"- mastery modes: **{render(mc)}**",f"- control scopes: **{render(sc)}**",f"- independent evidence obligations introduced: **{independent}**",""]
        active_lines.append(f"| {lid} | {independent} | {controlled} | {support} | {pwords} | {pgram} | {pphr} | {len(rs)} |")
        maxima["independent"] = max(maxima["independent"],independent)
        maxima["controlled"] = max(maxima["controlled"],controlled)
        maxima["productive_words"] = max(maxima["productive_words"],pwords)
        maxima["productive_grammar"] = max(maxima["productive_grammar"],pgram)
        maxima["formulaic_phrases"] = max(maxima["formulaic_phrases"],pphr)
    attrib += ["# Whole-level attribution checks","",f"- lesson slots: **{len(all_lessons)} / 95**",f"- exact records: **{sum(len(lesson_intro.get(x,[])) for x in all_lessons)} / 2,075**",f"- zero-new slots unchanged: **{len(actual_zero)} / 18**",""]
    active_lines += ["","## Maxima for Stage 8.5 critic","",f"- max independent obligations introduced in one lesson: **{maxima['independent']}**",f"- max controlled resources introduced in one lesson: **{maxima['controlled']}**",f"- max productive words introduced in one lesson: **{maxima['productive_words']}**",f"- max productive grammar rows introduced in one lesson: **{maxima['productive_grammar']}**",f"- max productive formulaic phrases introduced in one lesson: **{maxima['formulaic_phrases']}**","","Stage 8.5 must interpret these role-aware counts against lesson coherence and may reopen Stage 5/6/7. No threshold is silently raised here."]
    args.lesson_attribution.write_text("\n".join(attrib)+"\n",encoding="utf-8")
    args.active_load.write_text("\n".join(active_lines)+"\n",encoding="utf-8")

    print("B2 STAGE-08 CANDIDATE ROLE EXPANSION PASS")
    print(f"records={TOTAL} zero_new={len(actual_zero)} automation_inferred_roles=0 owner_approval_pending=true")
    print(f"mastery={dict(sorted(mastery.items()))}")


if __name__ == "__main__":
    main()
