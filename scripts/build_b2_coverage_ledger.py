#!/usr/bin/env python3
"""Build the exact B2 Stage-06 provisional coverage/lifecycle ledger.

This is NON-SEMANTIC automation. It expands reviewed Stage 1-5 candidate decisions,
joins exact source IDs, balances records only inside declared introduction windows,
and fails closed on missing coverage, lifecycle gaps, zero-new violations, or drift.
"""
from __future__ import annotations
import argparse, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
B2=ROOT/"curriculum/levels/b2"; REVIEW=B2/"design-review"
PLAN_PATH=REVIEW/"06-coverage-ledger/lifecycle-plan.json"
WORD_POLICY_PATH=REVIEW/"04-words/word-home-decisions.json"
STAGES={"i":"introduce","p":"practice","f":"fresh_retrieval","r":"recycle","c":"consolidate","e":"exit_verify"}

def load_json(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def text(p): return Path(p).read_text(encoding="utf-8")
def csv(s): return [x for x in str(s).split(",") if x]

def lesson_ids(md):
    out=[]
    for x in re.findall(r"^###\s+(U\d+-L\d+)\b",md,flags=re.M):
        if x not in out: out.append(x)
    return out

def expand_number_spec(v):
    v=v.replace("–","-").replace("—","-"); out=[]
    for part in re.split(r"[,;]",v):
        part=part.strip().strip(".")
        if not part: continue
        m=re.search(r"(\d+)\s*-\s*(\d+)",part)
        if m: out.extend(range(int(m.group(1)),int(m.group(2))+1)); continue
        m=re.search(r"\d+",part)
        if m: out.append(int(m.group()))
    return out

def parse_aid_ids(md):
    out={}
    for line in md.splitlines():
        m=re.match(r"^\|\s*(\d+)\s*\|\s*`([^`]+)`\s*\|",line)
        if m: out[int(m.group(1))]=m.group(2)
    return out

def parse_ability_homes(md):
    out={}
    for m in re.finditer(r"\b(\d+)=(K|M|S):([A-Z][A-Z0-9-]*)",md):
        out[int(m.group(1))]=[m.group(3)]
    for m in re.finditer(r"\b(\d+)=P:([A-Z][A-Z0-9-]*)\+([A-Z][A-Z0-9-]*)",md):
        out[int(m.group(1))]=[m.group(2),m.group(3)]
    return out

def parse_phrase_rows(md):
    out={}
    for line in md.splitlines():
        if not re.match(r"^\|\s*\d+\s*\|",line): continue
        cols=[x.strip() for x in line.strip().strip("|").split("|")]
        if len(cols)<6: continue
        try: row=int(cols[0])
        except ValueError: continue
        iid=cols[1].strip("`")
        if iid.startswith("oxford.phrase."):
            out[row]={"item_id":iid,"primary_home":cols[3].strip("`")}
    return out

def parse_grammar_aid(md):
    out={}
    for line in md.splitlines():
        m=re.match(r"^\|\s*(\d+)\s*\|\s*(\d+)\s*\|",line)
        if m: out[int(m.group(1))]=int(m.group(2))
    return out

def parse_grammar_systems(md):
    row_system={}; system_homes={}; current=None
    for line in md.splitlines():
        h=re.match(r"##\s+(G\d{2})\b",line)
        if h: current=h.group(1); continue
        if line.startswith("#") and not line.startswith("##"): current=None; continue
        if not current: continue
        if line.startswith("**Review row"):
            for row in expand_number_spec((line.split(":",1)[1] if ":" in line else line).replace("**","")):
                if row in row_system and row_system[row]!=current: raise ValueError(f"grammar row {row} has multiple systems")
                row_system[row]=current
        elif line.startswith("**Homes:**"):
            system_homes[current]=list(dict.fromkeys(re.findall(r"\b(?:C\d{2}|X-[A-Z0-9-]+)\b",line)))
    return row_system,system_homes

def union_cap_lifecycle(plan,cap_codes,order):
    result={stage:[] for stage in STAGES.values()}
    for cap in cap_codes:
        raw=plan["capabilities"][cap]
        for short,stage in STAGES.items(): result[stage].extend(csv(raw[short]))
    for stage in result: result[stage]=sorted(set(result[stage]),key=order.__getitem__)
    return result

def expand_plan(raw,lessons):
    order={x:i for i,x in enumerate(lessons)}; plan=dict(raw)
    plan["zero_new_lessons"]=csv(raw["zero_new_lessons"])
    caps={}
    for code,v in raw["capabilities"].items(): caps[code]={stage:csv(v[short]) for short,stage in STAGES.items()}
    plan["capabilities"]=caps
    cross={}
    for code,cap_csv in raw["cross_cutting_capability_homes"].items(): cross[code]=union_cap_lifecycle(plan,csv(cap_csv),order)
    plan["cross_cutting"]=cross
    lexical={}
    for code,cap_csv in raw["lexical_set_capability_homes"].items(): lexical[code]=union_cap_lifecycle(plan,csv(cap_csv),order)
    instruction=[x for x in lessons if x not in set(plan["zero_new_lessons"])]
    gp=raw["lexical_general_policy"]
    lexical["LX-GENERAL"]={"introduce":instruction if gp["i"]=="ALL_INSTRUCTIONAL" else csv(gp["i"]),"practice":instruction if gp["p"]=="ALL_INSTRUCTIONAL" else csv(gp["p"]),"fresh_retrieval":plan["zero_new_lessons"] if gp["f"]=="ALL_ZERO_NEW" else csv(gp["f"]),"recycle":csv(gp["r"]),"consolidate":csv(gp["c"]),"exit_verify":csv(gp["e"])}
    plan["lexical_sets"]=lexical
    plan["grammar_system_intro"]={k:csv(v) for k,v in raw["grammar_system_intro"].items()}
    pron={}
    for iid,intro in raw["pronunciation_intro"].items():
        base=union_cap_lifecycle(plan,csv(raw["pronunciation_capability_homes"][iid]),order); base["introduce"]=[intro]; pron[iid]=base
    plan["pronunciation"]=pron
    return plan

def family_plan(plan,home):
    if home.startswith("C"): return plan["capabilities"][home]
    if home.startswith("X"): return plan["cross_cutting"][home]
    return plan["lexical_sets"][home]

def validate_refs(plan,lessons):
    allowed=set(lessons); bad=[]
    for group in ("capabilities","cross_cutting","lexical_sets","pronunciation"):
        for home,life in plan[group].items():
            for stage,vals in life.items():
                for lid in vals:
                    if lid not in allowed: bad.append((group,home,stage,lid))
    for g,vals in plan["grammar_system_intro"].items():
        for lid in vals:
            if lid not in allowed: bad.append(("grammar",g,"introduce",lid))
    if bad: raise ValueError(f"unknown lesson refs: {bad[:30]}")

def stable_offset(key,size): return 0 if size<=1 else sum((i+1)*ord(ch) for i,ch in enumerate(key))%size

def approved_windows(plan,homes,order):
    vals=[]
    for h in homes: vals.extend(family_plan(plan,h)["introduce"])
    return sorted(set(vals),key=order.__getitem__)

def balanced(records,key_fn,windows_fn,salt):
    groups=defaultdict(list); assigned={}
    for r in records: groups[key_fn(r)].append(r)
    for key,vals in groups.items():
        wins=windows_fn(key)
        if not wins: raise ValueError(f"no introduction window for {key}")
        off=stable_offset(f"{salt}:{key}",len(wins))
        for i,r in enumerate(vals): assigned[r["item_id"]]=wins[(i+off)%len(wins)]
    return assigned

def later(plan,homes,stage,order,intro,strict):
    i=order[intro]; vals=set()
    for h in homes: vals.update(family_plan(plan,h)[stage])
    vals={x for x in vals if order[x]>(i if strict else i-1)}
    return sorted(vals,key=order.__getitem__)

def build_record(category,item,label,homes,intro,plan,order,extra=None):
    rec={"category":category,"item_id":item["item_id"],"label":label,"homes":homes,"provisional_semantic_role":"pending_stage_8_reconciliation","lifecycle":{"introduce":[intro],"practice":later(plan,homes,"practice",order,intro,False),"fresh_retrieval":later(plan,homes,"fresh_retrieval",order,intro,True),"recycle":later(plan,homes,"recycle",order,intro,True),"consolidate":later(plan,homes,"consolidate",order,intro,True),"exit_verify":later(plan,homes,"exit_verify",order,intro,True)}}
    if extra: rec.update(extra)
    return rec

def exact_word_homes(words,policy):
    explicit={}
    for home,heads in policy["explicit_headword_homes"].items():
        for h in heads:
            if h in explicit and explicit[h]!=home: raise ValueError(f"headword {h} has multiple homes")
            explicit[h]=home
    counts=Counter(x["headword"] for x in words); overrides=policy.get("exact_item_overrides",{}); out={}
    for item in words:
        iid=item["item_id"]; head=item["headword"]
        if iid in overrides: out[iid]=overrides[iid]["home"]
        elif head in explicit:
            if counts[head]!=1: raise ValueError(f"non-unique headword {head} needs exact-ID override")
            out[iid]=explicit[head]
        else: out[iid]="LX-GENERAL"
    return out

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",type=Path); ap.add_argument("--report",type=Path); ap.add_argument("--source-home-index",type=Path); args=ap.parse_args()
    curriculum=text(REVIEW/"05-curriculum-map/curriculum-map.md"); lessons=lesson_ids(curriculum); raw=load_json(PLAN_PATH)
    if len(lessons)!=raw["lesson_count_baseline"]: raise ValueError(f"lesson map={len(lessons)} plan={raw['lesson_count_baseline']}")
    plan=expand_plan(raw,lessons); order={x:i for i,x in enumerate(lessons)}; validate_refs(plan,lessons)
    abilities=load_json(B2/"abilities.json")["items"]; phrases=load_json(B2/"phrases.json")["items"]; grammar=load_json(B2/"grammar.json")["items"]; words=load_json(B2/"words.json")["items"]; pron=load_json(B2/"pronunciation.json")["items"]
    expected={"ability":270,"phrase":125,"grammar":243,"word":1427,"pronunciation":10}; actual={"ability":len(abilities),"phrase":len(phrases),"grammar":len(grammar),"word":len(words),"pronunciation":len(pron)}
    if actual!=expected: raise ValueError(f"source count drift {actual} != {expected}")
    row_source=parse_aid_ids(text(REVIEW/"01-abilities/generated/ability-review-aid.md")); row_homes=parse_ability_homes(text(REVIEW/"01-abilities/ability-review.md")); rows=set(range(1,271))
    if set(row_source)!=rows or set(row_homes)!=rows: raise ValueError(f"ability rows incomplete source={len(row_source)} homes={len(row_homes)}")
    by_source={x["source_record_id"]:x for x in abilities}; arecs=[]
    for row in range(1,271):
        sid=row_source[row]
        if sid not in by_source: raise ValueError(f"missing ability source {sid}")
        homes=row_homes[row]
        for h in homes: family_plan(plan,h)
        arecs.append({**by_source[sid],"review_row":row,"manual_homes":homes})
    aintro=balanced(arecs,lambda x:"+".join(x["manual_homes"]),lambda k:approved_windows(plan,k.split("+"),order),"ability")
    prows=parse_phrase_rows(text(REVIEW/"02-phrases/phrase-review.md"))
    if set(prows)!=set(range(1,126)): raise ValueError(f"phrase rows incomplete: {len(prows)}")
    pby={x["item_id"]:x for x in phrases}; precs=[]
    for row in range(1,126):
        m=prows[row]; iid=m["item_id"]
        if iid not in pby: raise ValueError(f"missing canonical phrase {iid}")
        family_plan(plan,m["primary_home"]); precs.append({**pby[iid],"review_row":row,"primary_home":m["primary_home"]})
    pintro=balanced(precs,lambda x:x["primary_home"],lambda h:family_plan(plan,h)["introduce"],"phrase")
    row_src=parse_grammar_aid(text(REVIEW/"03-grammar/generated/grammar-review-aid.md")); row_sys,sys_homes=parse_grammar_systems(text(REVIEW/"03-grammar/grammar-review.md")); grows=set(range(1,244))
    if set(row_src)!=grows or set(row_sys)!=grows: raise ValueError(f"grammar rows incomplete aid={len(row_src)} system={len(row_sys)}")
    gby={int(x["source_ref"]["spreadsheet_row"]):x for x in grammar}; grecs=[]; groups=defaultdict(list)
    for row in range(1,244):
        src=row_src[row]
        if src not in gby: raise ValueError(f"EGP source row missing {src}")
        system=row_sys[row]; homes=sys_homes.get(system,[])
        if not homes: raise ValueError(f"{system} has no homes")
        for h in homes: family_plan(plan,h)
        rec={**gby[src],"review_row":row,"grammar_system":system,"manual_homes":homes}; grecs.append(rec); groups[system].append(rec)
    if set(groups)!=set(plan["grammar_system_intro"]): raise ValueError("grammar intro plan must cover G01-G47 exactly")
    gintro={}
    for system,vals in groups.items():
        wins=plan["grammar_system_intro"][system]; off=stable_offset("grammar:"+system,len(wins))
        for i,r in enumerate(vals): gintro[r["item_id"]]=wins[(i+off)%len(wins)]
    wh=exact_word_homes(words,load_json(WORD_POLICY_PATH)); wrecs=[]
    for item in words:
        home=wh[item["item_id"]]; family_plan(plan,home); wrecs.append({**item,"primary_home":home})
    wintro=balanced(wrecs,lambda x:x["primary_home"],lambda h:family_plan(plan,h)["introduce"],"word")
    records=[]
    for x in arecs: records.append(build_record("ability",x,x.get("source_text") or x["item_id"],x["manual_homes"],aintro[x["item_id"]],plan,order,{"review_row":x["review_row"],"source_record_id":x["source_record_id"]}))
    for x in precs: records.append(build_record("phrase",x,x.get("phrase") or x["item_id"],[x["primary_home"]],pintro[x["item_id"]],plan,order,{"review_row":x["review_row"]}))
    for x in grecs: records.append(build_record("grammar",x,x.get("guideword") or x["item_id"],x["manual_homes"],gintro[x["item_id"]],plan,order,{"review_row":x["review_row"],"egp_spreadsheet_row":int(x["source_ref"]["spreadsheet_row"]),"grammar_system":x["grammar_system"]}))
    for x in wrecs: records.append(build_record("word",x,x.get("headword_source") or x.get("headword") or x["item_id"],[x["primary_home"]],wintro[x["item_id"]],plan,order))
    pron_by={x["item_id"]:x for x in pron}
    if set(pron_by)!=set(plan["pronunciation"]): raise ValueError("pronunciation plan mismatch")
    for iid,life in plan["pronunciation"].items(): records.append(build_record("pronunciation",pron_by[iid],pron_by[iid]["title"],csv(raw["pronunciation_capability_homes"][iid]),life["introduce"][0],plan,order))
    counts=Counter(x["category"] for x in records)
    if dict(counts)!=expected: raise ValueError(f"ledger count mismatch {dict(counts)} != {expected}")
    ids=[x["item_id"] for x in records]
    if len(ids)!=len(set(ids)): raise ValueError("duplicate primary item IDs")
    required=raw["policy"]["required_stages"]; gaps={s:[x["item_id"] for x in records if not x["lifecycle"][s]] for s in required}
    intro_counts={lid:Counter() for lid in lessons}; intro_items={lid:defaultdict(list) for lid in lessons}
    for rec in records:
        lid=rec["lifecycle"]["introduce"][0]; intro_counts[lid][rec["category"]]+=1; intro_counts[lid]["total"]+=1; intro_items[lid][rec["category"]].append(rec["label"])
    tkey={"ability":"abilities_introduced","phrase":"phrases_introduced","grammar":"grammar_introduced","word":"words_introduced","pronunciation":"pronunciation_introduced","total":"total_source_introductions"}; overloads=[]
    for lid,c in intro_counts.items():
        for cat in ("ability","phrase","grammar","word","pronunciation","total"):
            lim=raw["load_thresholds"][tkey[cat]]
            if c[cat]>lim: overloads.append((lid,cat,c[cat],lim))
    transfer_new={lid:intro_counts[lid]["total"] for lid in plan["zero_new_lessons"] if intro_counts[lid]["total"]}
    report=["# B2 Coverage Ledger Audit","","Status: **PROVISIONAL PRE-SEMANTIC-LOCK LIFECYCLE AUDIT**","",f"Source records expanded: **{len(records)} / 2075**","","- abilities: 270","- phrases: 125","- grammar: 243","- words: 1427","- pronunciation: 10","- duplicate primary item IDs: **0**","","Exact source coverage is not a mastery claim; final role-aware evidence remains for Stage 8/8.5.","","## Lifecycle completeness",""]
    for s in required: report.append(f"- records missing `{s}`: **{len(gaps[s])}**")
    report += ["","## Introduction load by lesson","","| Lesson | Abilities | Phrases | Grammar | Words | Pron. | Total |","|---|---:|---:|---:|---:|---:|---:|"]
    for lid in lessons:
        c=intro_counts[lid]; report.append(f"| {lid} | {c['ability']} | {c['phrase']} | {c['grammar']} | {c['word']} | {c['pronunciation']} | {c['total']} |")
    report += ["","## Mechanical load result",""]
    if overloads:
        report.append("**OVERLOAD WARNINGS FOUND — Stage-06 load critic required; thresholds were not raised to force a pass.**")
        for lid,cat,n,lim in overloads: report.append(f"- {lid}: {cat} = {n} > {lim}")
    else: report.append("**PASS — no mechanical introduction warning threshold exceeded.**")
    report += ["","## Zero-new transfer / exit slots",""]
    if transfer_new:
        report.append("**FAIL — designated zero-new slots received new source introductions.**")
        for lid,n in transfer_new.items(): report.append(f"- {lid}: **{n}** new source records")
    else: report.append(f"**PASS — all {len(plan['zero_new_lessons'])} designated zero-new slots are zero-new.**")
    if overloads:
        report += ["","## Overload attribution",""]
        for lid in sorted({x[0] for x in overloads},key=order.__getitem__):
            report.append("### "+lid)
            for cat in ("ability","phrase","grammar","word","pronunciation"):
                vals=intro_items[lid][cat]
                if vals: report.append(f"- **{cat} ({len(vals)})**: "+"; ".join(vals))
            report.append("")
    gap_count=sum(len(v) for v in gaps.values()); report += ["","## Audit verdict",""]
    if gap_count: report.append(f"**FAIL — {gap_count} lifecycle-stage gaps require revision.**")
    elif transfer_new: report.append("**FAIL — zero-new protection was violated.**")
    elif overloads: report.append(f"**REVIEW REQUIRED — lifecycle complete, but {len(overloads)} mechanical load warnings require critic review.**")
    else: report.append("**PASS — exact B2 source coverage and provisional lifecycle are complete with no mechanical load warnings. Owner review remains required.**")
    ledger={"schema_version":1,"level":"B2","status":"expanded_from_review_candidates_and_provisional_lifecycle_plan","lesson_count":len(lessons),"record_counts":expected,"records":records}; index={"schema_version":1,"level":"B2","record_count":len(records),"records":[{"category":r["category"],"item_id":r["item_id"],"homes":r["homes"],"introduce":r["lifecycle"]["introduce"]} for r in records]}
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if args.report: args.report.parent.mkdir(parents=True,exist_ok=True); args.report.write_text("\n".join(report)+"\n",encoding="utf-8")
    if args.source_home_index: args.source_home_index.parent.mkdir(parents=True,exist_ok=True); args.source_home_index.write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("\n".join(report))
    if gap_count or transfer_new: raise SystemExit(3)
    if overloads: raise SystemExit(2)

if __name__=="__main__": main()
