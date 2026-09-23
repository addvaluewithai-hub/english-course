# A1 Manual Ability Review Log

Status: **IN PROGRESS**  
Input: `curriculum/levels/a1/abilities.json`  
Total required source abilities: **119**

This is a manual curriculum review. The decisions below are not produced by clustering code or inherited lesson structure. Provisional capability IDs may be renamed or regrouped after later abilities are read; source abilities remain traceable.

## Decision vocabulary

- **KEEP** — the source ability expresses a meaningful learner performance that must remain visible in the final capability map.
- **MERGE** — preserve the source evidence, but represent it as a component of a broader final capability.
- **SUPPORTING** — a general processing/language condition rather than a useful standalone curriculum capability.
- **SPLIT** — the source statement contains more than one materially distinct learner performance.

## Batch 1 — Reading, GSE A1 page 9

| # | Source ID | Source ability | Decision | Provisional home | Manual rationale |
|---|---|---|---|---|---|
| 1 | `gse.adult.2022.a1.p09.001` | Recognise cardinal numbers 11–100. | MERGE | `CAP-NUMBERS-BASIC` | Numeral recognition matters, but it is a component of functional number handling rather than a standalone communicative capability. Keep the reading/reception evidence visible. |
| 2 | `gse.adult.2022.a1.p09.002` | Understand basic sentences describing everyday objects (colour/size), with visual support. | MERGE | `CAP-UNDERSTAND-DESCRIPTIONS` | Same core receptive act as other simple-description objectives; object description is a context/sub-domain, not a separate top-level capability. |
| 3 | `gse.adult.2022.a1.p09.003` | Understand short simple descriptions of objects, people and animals, with visual support. | MERGE | `CAP-UNDERSTAND-DESCRIPTIONS` | Broadly subsumes the descriptive-reading performance in #2 while adding people/animals. Preserve the visual-support condition as evidence, not as a new capability. |
| 4 | `gse.adult.2022.a1.p09.004` | Follow short simple written directions from X to Y. | MERGE | `CAP-FOLLOW-WRITTEN-INSTRUCTIONS` | A real task, but best treated as the navigation branch of a broader A1 ability to follow short written instructions/directions. Navigation must remain testable separately inside the capability. |
| 5 | `gse.adult.2022.a1.p09.005` | Understand short written notices, signs and instructions with visual support. | KEEP | `CAP-UNDERSTAND-SIGNS-NOTICES` | Public notices/signs are a distinct functional-literacy task. Although related to instructions, recognising/understanding a sign is not the same performance as following a procedure or route. |
| 6 | `gse.adult.2022.a1.p09.006` | Understand simple descriptions of places. | MERGE | `CAP-UNDERSTAND-DESCRIPTIONS` | Same receptive description capability as #2–3, with place as another required content domain. |
| 7 | `gse.adult.2022.a1.p09.007` | Understand basic phrases in short simple texts. | SUPPORTING | `SUPPORT-READ-BASIC-PHRASES` | This describes general reading processing, not a meaningful real-world task. It should be evidenced through more specific reading capabilities rather than become its own final capability. |
| 8 | `gse.adult.2022.a1.p09.008` | Follow basic instructions for making something simple. | MERGE | `CAP-FOLLOW-WRITTEN-INSTRUCTIONS` | Same core performance as #4—following written instructions—but procedural rather than navigational. Both contexts should survive as assessment branches. |
| 9 | `gse.adult.2022.a1.p09.009` | Extract personal details in a limited way. | KEEP | `CAP-LOCATE-PERSONAL-DETAILS` | Clear, observable information-location task with a distinct success condition; should stay visible in the final capability structure. |
| 10 | `gse.adult.2022.a1.p09.010` | Understand short simple messages about when and where to meet. | KEEP | `CAP-UNDERSTAND-SIMPLE-ARRANGEMENTS` | Functional message-reading task combining time/place information; sufficiently distinct to remain visible. |
| 11 | `gse.adult.2022.a1.p09.011` | Understand familiar phrases in a simple text. | SUPPORTING | `SUPPORT-READ-FAMILIAR-PHRASES` | General processing statement, largely overlapping #7; should support specific reading tasks, not generate a separate curriculum endpoint. |
| 12 | `gse.adult.2022.a1.p09.012` | Understand simple phrases related to familiar everyday activities. | SUPPORTING | `SUPPORT-READ-EVERYDAY-PHRASES` | Again a broad language-processing condition. Useful evidence for difficulty/load, but too unspecific to be a standalone final capability. |

## Provisional capability families after Batch 1

1. `CAP-NUMBERS-BASIC` — understand/use basic numbers in functional contexts; currently only reading recognition evidence reviewed.
2. `CAP-UNDERSTAND-DESCRIPTIONS` — understand short simple descriptions of familiar people, places, objects and animals; visual support may be allowed at A1 where source-evidenced.
3. `CAP-FOLLOW-WRITTEN-INSTRUCTIONS` — follow short simple written instructions, including route directions and basic procedures; sub-contexts must remain separately testable.
4. `CAP-UNDERSTAND-SIGNS-NOTICES` — understand short public notices/signs/simple instruction messages, often with visual support.
5. `CAP-LOCATE-PERSONAL-DETAILS` — locate requested personal information in a simple written source.
6. `CAP-UNDERSTAND-SIMPLE-ARRANGEMENTS` — understand basic written meeting arrangements such as when and where to meet.

## Critic flags opened by Batch 1

- Decide later whether `CAP-UNDERSTAND-SIGNS-NOTICES` should remain independent or become a branch of a broader functional-reading capability after all reading objectives are seen.
- `CAP-NUMBERS-BASIC` must not be locked until listening/speaking/writing number objectives are reviewed; number handling may become a cross-modal capability.
- `CAP-UNDERSTAND-DESCRIPTIONS` currently combines multiple semantic domains. This is acceptable only if later assessment design keeps people/place/object/animal coverage visible rather than testing one domain and implying all are covered.
