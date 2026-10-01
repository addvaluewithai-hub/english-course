# B2 Stage 4.5 — Pronunciation, Exit Constraints, and B1 Carry-Forward

Status: **AI-ASSISTED REVIEW CANDIDATE — OWNER HUMAN APPROVAL PENDING; READY FOR STAGE-5 ARCHITECTURE WORK AFTER OWNER REVIEW**  
Level: **B2**  
Current candidate architecture: **18 capability families + cross-cutting requirements, including Stage-3 `X-REFERENCE` refinement**  
Previous locked level: **B1 — semantic/design lock reviewed; lesson design authorized; 12 units / 85 lesson slots**

This stage reconciles the B2 Stage-1–4 review candidates with the three constraints that must be explicit before any B2 unit or lesson architecture is chosen:

1. all **10 reviewed B2 pronunciation strands**;
2. the **cumulative B2 exit contract and fresh-evidence requirements**;
3. the **locked B1 exit state as prerequisite/retrieval**, never as new B2 inventory.

No B2 unit count or lesson count is selected here. No final Stage-8 productive/receptive/formulaic/support role is assigned here. This file does not authorize lesson design or delivery production.

## Pinned inputs

- B2 pronunciation: `curriculum/levels/b2/pronunciation.json` — blob `edec3acd8971b24b388a06277a12f2affe48ce2b`
- B2 exit contract: `curriculum/levels/b2/exit_contract.json` — blob `7bae6d9bd77b2e80f8f61b358e53ec6505dcc7d0`
- B2 Stage-1 ability architecture: `../01-abilities/ability-review.md`
- B2 Stage-3 architecture refinement: `../01-abilities/stage-3-architecture-refinement.md`
- B2 Stage-2 phrase review: `../02-phrases/phrase-review.md`
- B2 Stage-3 grammar review: `../03-grammar/grammar-review.md`
- B2 Stage-4 lexical review: `../04-words/word-review.md`
- locked B1 manifest: `curriculum/levels/b1/manifest.json` — blob `72a31f549b0e1bb2211b7999f097d839a6db1267`
- locked B1 exit contract: `curriculum/levels/b1/exit_contract.json` — blob `e99d14ebe8584ee14c71148ccba0886f0597aa1b`
- B1 Stage-4.5 precedent: `curriculum/levels/b1/design-review/04.5-pronunciation-exit-carry-forward/review.md`

---

# A. B2 pronunciation review — 10 / 10 strands

Global boundary: **B2 pronunciation is intelligibility-first, not accent-normalization.** The B2 source boundary is that speech is intelligible throughout, accent has little effect on understanding, and prosody generally supports the intended message. A non-native accent is not failure. The curriculum must distribute pronunciation inside real B2 reception/production/interaction, not create an isolated pronunciation chapter.

## P01 — Sound perception and word recognition
**Source:** `pronunciation.sound_perception.b2`  
**Natural homes:** C05 extended spoken input, C06 spoken argument/stance, C07 detailed spoken instructions; secondary support in C13/C14 where accurate uptake precedes response/relay.  
**Progression from B1:** move from generally understanding familiar connected speech to resolving most sound, stress and reduction variation in standard familiar and field-related input.  
**Fresh evidence:** new-speaker/new-topic listening where the learner must recover meaning without transcript dependence.  
**Boundary:** this does not require perfect phonetic discrimination or native-like perception.

## P02 — Consonant contrasts and place/manner clarity
**Source:** `pronunciation.consonant_clarity.b2`  
**Natural homes:** C08/C09/C10 spoken production; C11/C12/C13 interaction; C14 spoken mediation.  
**Progression from B1:** sustain consonant clarity across longer, more independent and less rehearsed output so breakdowns rarely interfere with understanding.  
**Fresh evidence:** extended explanation, viewpoint, problem-resolution or relay task with changed content.  
**Boundary:** accent difference is acceptable where intelligibility remains stable.

## P03 — Vowel contrasts and reduced vowels
**Source:** `pronunciation.vowel_clarity.b2`  
**Natural homes:** C08–C14, with perceptual cross-link to C05/C06.  
**Progression from B1:** stable stressed vowels plus functional reductions in longer connected speech; listener effort should not rise materially because of vowel instability.  
**Fresh evidence:** spontaneous or lightly prepared extended speech rather than isolated word repetition.

## P04 — Syllable shape, consonant clusters and word endings
**Source:** `pronunciation.syllable_shape.b2`  
**Natural homes:** C08 detailed explanation/narrative, C09 viewpoint, C10 speculation, C13 formal discussion/Q&A, C14 mediation.  
**Progression from B1:** preserve word shape reliably at natural speed, including less familiar and field-related words from the B2 lexical inventory.  
**Cross-link:** Stage-4 lexical content homes and Stage-3 morphology/grammar systems.  
**Boundary:** not a decontextualised cluster-drill syllabus.

## P05 — Audible grammatical endings
**Source:** `pronunciation.grammatical_endings.b2`  
**Natural homes:** C08/C09/C10/C11/C12/C13/C14; especially narrative time reference, comparison, passives, reported information and complex noun/reference structures.  
**Progression from B1:** integrate endings into connected speech without losing grammatical information even when clusters or reductions are present.  
**Cross-link:** Stage-3 grammar systems; pronunciation supports grammatical meaning and does not duplicate grammar ownership.

## P06 — Word stress and stress-sensitive recognition
**Source:** `pronunciation.word_stress.b2`  
**Natural homes:** distributed wherever active B2 lexis is used, strongest in C08/C09/C13/C14 plus C05/C06 recognition.  
**Progression from B1:** reliable stress over broader general and field-related vocabulary, including derived forms.  
**Cross-link:** Stage-4 active-core candidates and receptive lexical breadth.  
**Boundary:** isolated stress accuracy is not enough; evidence must occur in real meaning-focused performance.

## P07 — Sentence prominence and rhythm
**Source:** `pronunciation.prominence_rhythm.b2`  
**Natural homes:** C09 viewpoint/argument, C11 collaborative discussion, C13 formal discussion/Q&A, C14 mediation; reception support in C06.  
**Progression from B1:** use prominence/rhythm consistently to signal focus, contrast, information status and turn structure across longer stretches.  
**Cross-links:** X-DISCOURSE, X-STANCE, X-FLUENCY-TURN, X-REFERENCE.  
**Fresh evidence:** new argument, comparison or explanation where prominence must make the information hierarchy audible.

## P08 — Connected-speech perception and production
**Source:** `pronunciation.connected_speech.b2`  
**Natural homes:** C05/C06/C07 reception and C08–C14 production/interaction/mediation.  
**Progression from B1:** handle common connected-speech processes at a natural pace while remaining intelligible throughout.  
**Boundary:** reductions/linking are useful only where they support fluency and intelligibility; accent imitation is out of scope.

## P09 — Intonation, interaction and stance
**Source:** `pronunciation.intonation_stance.b2`  
**Natural homes:** C09 viewpoint/evaluation, C11 collaborative discussion, C12 negotiation/complaints, C13 formal interaction, C14 facilitation; reception cross-link to C06.  
**Progression from B1:** intonation should support viewpoint, certainty/uncertainty, politeness, turn management, contrast and social meaning consistently enough for B2 interaction.  
**Cross-links:** X-STANCE, X-PRAGMATICS, X-FLUENCY-TURN and Stage-1 prosody requirement.  
**Boundary:** no native-like contour requirement.

## P10 — Chunking, pausing, monitoring and pronunciation repair
**Source:** `pronunciation.chunking_monitoring_repair.b2`  
**Natural homes:** C08–C14, especially C11 sustained discussion, C13 Q&A/interviews and C14 relay/facilitation.  
**Progression from B1:** manage pausing and repair smoothly enough to sustain longer independent interaction at a fairly even tempo.  
**Cross-links:** X-REPAIR, X-FLUENCY-TURN, X-METACOGNITION.  
**Fresh evidence:** spontaneous contribution with changed content and no complete model.

### Pronunciation critic

- strands reviewed: **10 / 10**
- strands with natural use contexts: **10 / 10**
- standalone pronunciation units required: **0**
- accent-perfection requirements introduced: **0**
- strands requiring later fresh retrieval: **10 / 10**
- strongest B2 progression versus B1: **sustained intelligibility, wider lexical stress control, prosody for stance/focus, natural-pace connected speech, and smoother chunking/repair**

---

# B. B2 exit-contract constraints

B2 exit is **cumulative through A1+A2+B1+B2**. Exposure to a B2 source record cannot by itself satisfy an exit claim. Each claim below therefore constrains Stage 5 curriculum mapping, Stage 6 lifecycle evidence, Stage 7 lesson briefs and Stage 8/8.5 semantic-role reconciliation.

## E01 — Cumulative retention, not B2-only performance
**Contract principle:** completion is not mastery; retention requires later fresh evidence.  
**Architecture consequence:** B1 abilities/systems needed for B2 must be retrieved in changed contexts and cannot disappear for long spans. Stage 6 must distinguish `B1 carry-forward retrieval` from `B2 new inventory introduction`.

## E02 — Interpretation of complex input
**Assessment requirement:** `b2.assessment.01 — Interpretation of complex input`.  
**Architecture consequence:** C01–C07 need repeated new-text/new-speaker evidence across extended argument, reports, instructions, media and field-related material. A single “advanced reading/listening” lesson cannot prove this claim.

## E03 — Extended spoken reception and argument tracking
**Exit claim:** follow extended talk and complex argument and understand most standard-language news/film.  
**Architecture consequence:** C05/C06/C07 require progression in length, density, viewpoint structure and reduced dependence on repetition/transcript support.

## E04 — Complex written reception and viewpoint interpretation
**Exit claim:** understand articles/reports with viewpoints, contemporary prose and relevant technical discussion.  
**Architecture consequence:** C01–C04 need repeated source types, inference and stance work. C02 information integration and C01 viewpoint reading must remain distinct evidence paths.

## E05 — Clear detailed spoken production
**Exit claim:** give clear detailed descriptions and explain a viewpoint with advantages, disadvantages and supporting detail.  
**Architecture consequence:** C08/C09/C10 need multi-step progression from structured support to changed-topic independent performance. One rehearsed presentation is insufficient.

## E06 — Clear detailed writing and supported position
**Exit claim:** produce clear detailed texts, essays and reports that present information or support a position.  
**Architecture consequence:** C15/C16/C18 and X-DISCOURSE/X-REFERENCE/X-REGISTER need genre-distinct evidence; correspondence C17 cannot substitute for extended standalone writing.

## E07 — Useful fluency and spontaneity in oral interaction
**Exit claim:** participate actively with useful fluency/spontaneity, sustain views and manage routine disagreement.  
**Architecture consequence:** C11/C12/C13 require genuinely interactive changed-detail tasks, not solo speaking disguised as interaction. Planning is allowed, but complete scripting/model dependence cannot prove the exit claim.

## E08 — Written/online collaboration and misunderstanding repair
**Exit claim:** collaborate in multi-person tasks and handle misunderstanding when others remain reasonably cooperative.  
**Architecture consequence:** C17 plus X-REPAIR/X-PRAGMATICS must include response chains, clarification, reformulation and collaborative written exchange rather than one-way messages only.

## E09 — Mediation, relay and idea development
**Exit claim:** relay detailed information/arguments reliably, clarify complex points, and develop/connect others' ideas.  
**Architecture consequence:** C14 must include real source-to-output transformation and facilitation. Copying or answering comprehension questions is not mediation evidence.

## E10 — Broad language range and collocational appropriacy
**Exit claim:** broad general and field-related language with viewpoints, argument and some complex sentence forms; vocabulary range includes many appropriate collocations.  
**Architecture consequence:** Stage-4 lexical breadth must be distributed across performance contexts. The 1,427 words cannot become a flashcard syllabus, and `LX-GENERAL` is valid contextual breadth. Stage 6 must still ensure repeated contextual encounter and role-appropriate retrieval.

## E11 — Relatively high grammar control, not perfection
**Exit claim:** relatively high control with occasional slips and some rigid/inaccurate complex-form use.  
**Architecture consequence:** Stage-3 systems must support accurate meaning under performance pressure, but B2 is not error-free mastery. Formulaic, receptive and embedded-support roles remain legitimate where evidence warrants them.

## E12 — Pronunciation intelligible throughout
**Exit claim:** accent has little effect and prosody generally supports the intended message.  
**Architecture consequence:** all 10 pronunciation strands require distributed evidence in real performance and later fresh retrieval. Accent reduction itself is not an assessment target.

## E13 — Cohesive, logically organised discourse
**Exit claim:** varied linking expressions, cohesive devices, supporting detail and clear logical paragraphs.  
**Architecture consequence:** X-DISCOURSE + X-REFERENCE + genre/layout requirements are exit-critical across C08/C09/C14/C15/C16/C17/C18. They must develop throughout the level rather than be postponed to a final writing unit.

## E14 — Fairly even tempo over longer stretches
**Exit claim:** sustain longer stretches at a fairly even tempo with few conspicuously long pauses.  
**Architecture consequence:** X-FLUENCY-TURN and P10 require progressive reduction of model dependence, longer turns and fresh interaction while allowing normal monitoring/repair.

## E15 — Spontaneous contribution
**Assessment requirement:** `b2.assessment.02 — Spontaneous contribution`.  
**Architecture consequence:** at least one cumulative evidence path must require the learner to contribute relevantly without a full script/model in a genuinely changing interaction. C11/C13 are primary homes; C12/C14 can provide additional evidence.

## E16 — Supported viewpoint for a new audience and topic
**Assessment requirement:** `b2.assessment.03 — A supported viewpoint for a new audience and topic`.  
**Architecture consequence:** C09/C16 must build argument resources that transfer beyond practised content. The final evidence must change both **topic and audience/context** enough that memorised content cannot satisfy the claim; supporting reasons/evidence, discourse organisation, register and language control must all remain visible.

### Exit-evidence critic

- B2 exit/assessment claims reviewed: **all contract claims plus 3 explicit assessment requirements**
- claims with architecture consequence: **all**
- claims satisfiable by one isolated source-row exposure: **0**
- claims requiring multiple evidence events: complex reception, detailed production, interaction/spontaneity, mediation, discourse, fluency, pronunciation, range and supported viewpoint
- final exit verification remains a Stage-6/7/8.5 lifecycle obligation; Stage 4.5 only establishes required evidence paths

---

# C. Locked B1 carry-forward map

B1 is locked and immutable here. Its semantic inventory and authorized 12-unit / 85-slot architecture are **not copied into B2**. B2 retrieves B1 capabilities/systems when they are prerequisites and then extends them to the B2 performance boundary.

## CF01 — B1 familiar factual/media reception → B2 extended complex reception
**B1 basis:** C01/C02/C05 practical/factual media, main points, viewpoints and logical relationships.  
**B2 extension:** C01–C07 handle longer input, denser argument, technical/field-related detail, inference, stance and standard-language media.  
**Treatment:** retrieve scanning/main-point/viewpoint routines early inside harder input; do not reteach them as new B2 skills.

## CF02 — B1 unprepared familiar conversation → B2 sustained collaborative discussion
**B1 basis:** C06 + X05 familiar unprepared conversation and turn-taking.  
**B2 extension:** C11 sustain, redirect and develop collaborative discussion with useful spontaneity.  
**Treatment:** assume routine conversation management; retrieve through changed prompts, then extend turn length, contribution quality and viewpoint development.

## CF03 — B1 reasoned opinion/advice/problem talk → B2 sustained viewpoint and evaluation
**B1 basis:** C07 reasoned response across familiar contexts.  
**B2 extension:** C09/C11/C12/C16 compare/evaluate alternatives, support claims, negotiate disagreement and develop arguments in more demanding contexts.  
**Treatment:** simple reason/advice/comparison is prerequisite; B2 evidence adds depth, counter-position handling and transfer to new audience/topic.

## CF04 — B1 repair/circumlocution → B2 smoother repair under extended interaction
**B1 basis:** C08 clarification, paraphrase, confirmation and lexical-gap workarounds.  
**B2 extension:** X-REPAIR across C11/C12/C13/C14 plus P10 monitoring/repair.  
**Treatment:** do not reteach basic clarification formulas as new inventory; require faster, less disruptive reformulation and maintenance of the task.

## CF05 — B1 connected narrative → B2 detailed narrative/explanation with richer viewpoint
**B1 basis:** C09/C18 connected experience/story production.  
**B2 extension:** C08/C15 detailed narratives, explanations and process accounts using richer background, evaluation, reference and discourse control.  
**Treatment:** simple connected chronology is prerequisite and should reappear in fresh B2 narrative/explanatory contexts.

## CF06 — B1 familiar-topic explanation/presentation → B2 detailed presentation and formal Q&A
**B1 basis:** C10 familiar-topic explanation and C11 short presentation with straightforward questions.  
**B2 extension:** C08/C09/C13 longer structured explanation/viewpoint, presentation Q&A, formal discussion/interview/survey.  
**Treatment:** basic structure and prepared delivery are retrieval; B2 adds audience adaptation, supporting detail, spontaneous follow-up and prosodic information structure.

## CF07 — B1 travel/service problem handling → B2 less-routine negotiation and resolution
**B1 basis:** C12/C13 travel, service, complaint and product/equipment problem resolution.  
**B2 extension:** C12 describes problems precisely, requests/demands action, negotiates perspectives and resolves disputes.  
**Treatment:** routine transaction language is assumed; B2 focuses on changed conditions, competing needs, justification and resolution.

## CF08 — B1 interview skill → B2 formal interview/survey/Q&A participation
**B1 basis:** C15 simple interviews with follow-up/checking.  
**B2 extension:** C13 detailed/formal questioning, survey/interview follow-up and presentation Q&A.  
**Treatment:** question formation/checking is prerequisite; B2 extends initiative, depth, register and spontaneous follow-up.

## CF09 — B1 source summarising/reporting → B2 mediation and facilitation
**B1 basis:** C16 compare/collate/summarise/report clear sources and relay useful information.  
**B2 extension:** C14 relay detailed arguments, paraphrase, clarify complex points and connect others' ideas.  
**Treatment:** simple source transformation is retrieval; B2 requires selection, synthesis, reliable relay and facilitation without copying.

## CF10 — B1 correspondence/online interaction → B2 audience-sensitive written interaction
**B1 basis:** C17 personal/formal correspondence and response chains.  
**B2 extension:** C17 more detailed correspondence, complaints/applications/invitations and collaborative written interaction with register control.  
**Treatment:** basic openings/closings/message organisation are assumed; B2 adds nuance, audience relationship, misunderstanding repair and sustained exchange.

## CF11 — B1 connected writing → B2 clear detailed genres and supported argument
**B1 basis:** C18/C19 straightforward narratives, descriptions, reviews, simple essays and practical informational texts.  
**B2 extension:** C15/C16/C18 detailed explanatory/narrative writing, argument/evaluation/synthesis and reports/reviews.  
**Treatment:** paragraphing and linear organisation are prerequisites; B2 adds denser reference, supporting detail, source use, genre control and argument structure.

## CF12 — B1 connected linear discourse → B2 cohesive extended discourse
**B1 basis:** X02/X03 plus B1 reference-building infrastructure.  
**B2 extension:** X-DISCOURSE + Stage-3 `X-REFERENCE`, supporting-detail hierarchy and varied linking across longer spoken/written output.  
**Treatment:** B1 basic chronology/paragraph/linking repertoire is retrieved; B2 expands information density and logical relation without a standalone connector unit.

## CF13 — B1 pragmatic/register control → B2 stance, tact and audience calibration
**B1 basis:** X04/X05 politeness, register, turn-taking and active listening.  
**B2 extension:** X-PRAGMATICS/X-STANCE/X-REGISTER across C09/C11/C12/C13/C17.  
**Treatment:** routine politeness/turn-taking is assumed; B2 adds hedging, concession, stronger/softer stance, disagreement management and audience-sensitive choices.

## CF14 — B1 grammar control → B2 Stage-3 grammar systems
**B1 basis:** locked B1 grammar roles and integrated support.  
**B2 extension:** 47 Stage-3 B2 grammar systems, many of which depend on B1 tense/aspect, modality, clause, reference and discourse prerequisites.  
**Treatment:** B1 forms are not reclassified as B2 new records. Retrieve prerequisite form/function briefly where needed, then teach the new B2 contrast/function/control boundary.

## CF15 — B1 lexical range → B2 broader general/field-related range
**B1 basis:** locked B1 productive/receptive/integrated lexical roles.  
**B2 extension:** Stage-4 B2 lexical homes and `LX-GENERAL`, with broader argument, institutional, technical, cultural and field-related content.  
**Treatment:** previously mastered B1 words are contextual resources, not B2 introductions; same-form/new-sense cases require exact source-record discipline.

## CF16 — B1 pronunciation intelligibility → B2 sustained intelligibility/prosody
**B1 basis:** generally intelligible familiar-topic speech despite regular mispronunciation/L1 influence.  
**B2 extension:** all 10 B2 strands, with intelligibility throughout, less listener impact from accent, stronger prosodic support and smoother natural-pace connected speech.  
**Treatment:** recycle lower-level sound/stress/chunking work inside B2 performances; never restart pronunciation as isolated sound training.

## CF17 — B1 assessment performances → B2 transfer performances
**B1 basis:** unscripted familiar problem, connected narrative, reasoned response in more than one context.  
**B2 extension:** complex-input interpretation, spontaneous contribution, and supported viewpoint for a new audience/topic.  
**Treatment:** B1 assessment capabilities must remain retrievable but are not repeated as B2 capstones. B2 evidence raises complexity, transfer and independence.

### Carry-forward critic

- B1 prerequisite families/systems deliberately mapped: **17 carry-forward bundles**
- B1 units copied into B2: **0**
- B1 lesson slots copied into B2: **0**
- B1 records reclassified as B2 new inventory: **0**
- B1 assessment tasks treated as sufficient B2 exit evidence: **0**
- required Stage-5 behavior: schedule early/periodic retrieval where a B2 dependency needs B1 control, and ensure no essential carry-forward disappears for an excessive span

---

# D. Stage-4.5 whole-architecture critic

## D1 — Pronunciation has use contexts
All 10 strands are attached to real reception, production, interaction or mediation contexts. No pronunciation strand is left as a free-floating accent target.

## D2 — Exit claims have candidate evidence paths
Every B2 exit/assessment claim maps to one or more capability/cross-cutting homes. Claims that inherently require breadth or transfer are explicitly marked as multi-event obligations for Stage 6/7/8.5 rather than falsely “completed” here.

## D3 — B1 remains prerequisite, not new B2 inventory
The carry-forward map retrieves and extends B1 performance. It does not reopen B1, change B1 semantic roles, copy B1 unit architecture, or count B1 records as new B2 introductions.

## D4 — Dependencies are visible before Stage 5
B2 grammar, discourse, interaction, mediation, pronunciation and lexical breadth all have explicit B1 prerequisites. Stage 5 must sequence new B2 demands after or alongside appropriate retrieval rather than assuming prerequisite control silently.

## D5 — Modalities remain distinct
Complex reception cannot be replaced by production; mediation cannot be replaced by comprehension; interaction cannot be assessed as solo production; written-online collaboration cannot be reduced to one-way correspondence.

## D6 — Transfer/retrieval cannot hide new B2 inventory
Any Stage-5 transfer, consolidation or carry-forward slot must have **zero hidden new required B2 source records**. New B2 records require explicit introduction homes in Stage 6.

## D7 — Completion is not mastery
Stage 5 may place a source/system once for introduction, but Stage 6 must show later changed-context retrieval and role-appropriate exit evidence. This applies especially to pronunciation, discourse, fluency, argument, mediation and broad lexical sets.

## D8 — No premature architecture sizing
The evidence does not justify a B2 unit count or lesson count yet. Counts must emerge in Stage 5 from capability boundaries, prerequisite order, introduction load, retrieval spacing, transfer/consolidation, cumulative assessment and independence requirements.

---

# Stage-4.5 decision

**Candidate Stage 4.5 is complete and does not require a new top-level B2 capability family.**

The current architecture remains:

- **18 capability families** from Stage 1;
- Stage-1 cross-cutting requirements, including the Stage-3 `X-REFERENCE` refinement;
- **47 grammar systems/infrastructure families** from Stage 3;
- **28 lexical/content homes + `LX-GENERAL`** from Stage 4;
- **10 pronunciation strands** with distributed use contexts;
- **16 B2 exit/evidence constraints** recorded above;
- **17 B1 carry-forward bundles** recorded above.

The next design step is **Stage 5 — curriculum map**. Only there should unit and lesson-slot architecture be proposed, and the count must emerge from this evidence rather than from a preset template.

Owner human review remains required before these candidates are treated as authoritative human curriculum decisions or used to set `lesson_design_authorized: true`.