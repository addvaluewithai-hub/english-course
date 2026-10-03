# C1 Stage 1 — Manual Ability Review

Status: **MANUAL REVIEW CANDIDATE V1 — OWNER HUMAN APPROVAL PENDING**  
Date: 2026-10-03  
Canonical required ability inventory: **59 source records**  
Source file: `curriculum/levels/c1/abilities.json`

## Review rule

Every `include_for_spine` C1 ability was read as a learner-performance statement. The capability architecture below is a manual curriculum-design candidate; source function tags and automated groupings are evidence, not authority.

Disposition meanings:

- **KEEP** — a distinct performance/boundary is preserved inside its capability family.
- **MERGE** — the source ability is fully represented inside a broader capability without losing its modality or assessment condition.
- **SPLIT** — one source statement contains more than one independently useful design component; the source remains one source record.
- **SUPPORTING** — the required source ability is retained as a cross-cutting control/condition rather than promoted to a fake standalone top-level capability.

No disposition here assigns final productive/receptive/control roles; those remain a Stage-8 decision after the architecture and lesson evidence exist.

---

## Candidate capability architecture

### Reading reception

**C01 — Interpret complex written argument, evidence, inference, and specialised information**  
Extract and evaluate information/ideas/opinions from long or specialised written sources; follow complex argument; identify evidence supporting an interpretation; infer unstated meaning; sustain detailed comprehension efficiently.

**C02 — Interpret idiomatic, non-standard, allusive, and rhetorical written meaning**  
Understand correspondence and short/public texts whose meaning depends on idiom, non-standard language, puns, allusion, humour, or other non-literal/rhetorical choices.

### Listening reception

**C03 — Follow extended complex spoken content and argument across unfamiliar or abstract domains**  
Track coherence, detail, and argument in linguistically complex recordings, podcasts, talks, and presentations, including topics outside the learner's field.

**C04 — Interpret fast, colloquial, idiomatic, attitudinal, and implied spoken meaning**  
Follow fast fluent-speaker interaction and media; interpret slang, colloquial language, idiom, wordplay, attitude, opinion, implication, and register shift while preserving reception as reception.

### Spoken production and interaction

**C05 — Explain, describe, narrate, and answer on complex subjects with developed detail**  
Handle abstract questions, complex problem/solution relationships, detailed accounts, anecdotes, and complex domain content with clear development and conclusions where required.

**C06 — Build, justify, conclude, and persuasively develop complex positions**  
State and justify viewpoints, give reasons/explanations, close discursive arguments, and use persuasive techniques for complex purposes.

**C07 — Sustain, enter, repair, compare, and manage fast complex discussion/conversation**  
Participate naturally in fast/colloquial interaction, enter ongoing discussion, compare/contrast/summarise within interaction, reformulate, and manage participants/flow without converting interaction into solo production.

**C08 — Orally summarise, synthesise, and comment on complex source material and discussion**  
Respond orally to complex texts, discussions, broadcasts, and opinions by summarising accurately and commenting in detail. This is source-responsive spoken performance; it is **not automatically relabelled as mediation** unless later source/exit evidence explicitly requires mediation.

### Written production and interaction

**C09 — Write accurate source-based summaries, synthesis, and notes**  
Summarise complex factual/discursive sources, synthesise multiple sources, and take useful notes from complex spoken/discussion input while preserving source tone/message where required.

**C10 — Write complex argument, critical evaluation, and review**  
Argue a case precisely, justify needs/objectives, and produce critical/professional/literary/cultural reviews with developed evaluation.

**C11 — Write professional/functional correspondence and complex information using appropriate conventions**  
Produce application/correspondence and complex informational writing with the register and conventions required by the communicative context.

**C12 — Adapt written style, register, rhetoric, and revision to audience and purpose**  
Control formality, rhetorical vocabulary/emphasis, wordplay, style switching, and revision for clarity/concision/personal audience effect.

> **Architecture warning:** C01–C12 are capability families, not units and not lesson titles. Stage 5 alone may derive a C1 unit/lesson count.

---

## Cross-cutting requirements

These controls recur across capability families and must not become fake standalone topic units:

- **X-IMPLICIT-RHETORIC** — interpret/use allusion, wordplay, double meaning, rhetorical emphasis and persuasive effect where source evidence supports it.
- **X-REGISTER-AUDIENCE** — recognise and adapt formality, idiom/colloquiality, neutrality, register shift, conventions, and audience relationship.
- **X-REPAIR-PRECISION** — lexical substitution, reformulation, circumlocution and precision without conspicuous breakdown.
- **X-DISCOURSE-FOCUS** — coherence, information structure, conclusion, comparison, emphasis and logical organisation.
- **X-FLUENCY-TURN** — fast-input tolerance, natural contribution, entering ongoing talk, turn/participant management and sustained flow.
- **X-SOURCE-TRANSFORMATION** — select, preserve, combine, summarise and comment on source meaning without copying; later Stage 4.5 must reconcile this with the explicit C1 mediation exit boundary.
- **X-MONITOR-EDIT** — monitor and revise complex output for clarity, concision, precision and audience fit.

---

## Exact 59-record review

### Reading — 7 / 59

| Source record | Exact source ability | Disposition | Primary home | Review note |
| --- | --- | --- | --- | --- |
| `gse.adult.2022.c1.p13.001` | Can understand correspondence containing idiomatic or non-standard language. | KEEP | C02 | Preserve correspondence context and non-standard/idiomatic condition. |
| `gse.adult.2022.c1.p13.002` | Can understand the use of puns, allusions, jokes etc. in adverts or newspaper headlines. | KEEP | C02 | Rhetorical/non-literal written interpretation; not generic vocabulary recognition. |
| `gse.adult.2022.c1.p13.003` | Can extract information, ideas and opinions from highly specialised sources within their field. | KEEP | C01 | Specialised-source retrieval stays written reception. |
| `gse.adult.2022.c1.p13.004` | Can identify examples that support a particular interpretation of a linguistically complex text. | MERGE | C01 | Evidence-for-interpretation component inside complex reading. |
| `gse.adult.2022.c1.p13.005` | Can understand complex arguments in newspaper articles. | KEEP | C01 | Argument reception remains distinct from producing an argument. |
| `gse.adult.2022.c1.p13.006` | Can identify inferred meaning in a linguistically complex text. | KEEP | C01 | Implicit/inferred meaning is an assessment boundary. |
| `gse.adult.2022.c1.p13.007` | Can understand the details of long complex texts in their field without needing to reread. | MERGE | C01 | Adds efficiency/independence condition to detailed complex reading. |

### Listening — 12 / 59

| Source record | Exact source ability | Disposition | Primary home | Review note |
| --- | --- | --- | --- | --- |
| `gse.adult.2022.c1.p20.001` | Can follow a fast-paced conversation between fluent speakers well enough to be able to contribute. | KEEP | C04 | Source mode remains reception; contribution is the downstream purpose, not permission to assess only speaking. |
| `gse.adult.2022.c1.p20.002` | Can recognise coherence devices and follow complex arguments on unfamiliar topics. | KEEP | C03 | Coherence + unfamiliar-topic argument tracking. |
| `gse.adult.2022.c1.p20.003` | Can understand the intended double meaning of a word used in a joke. | MERGE | C04 | Spoken wordplay/implicit meaning; cross-link X-IMPLICIT-RHETORIC. |
| `gse.adult.2022.c1.p20.004` | Can understand most of a linguistically complex podcast. | MERGE | C03 | Extended complex media reception. |
| `gse.adult.2022.c1.p20.005` | Can follow presentations on abstract and complex topics outside their field of interest. | KEEP | C03 | Outside-field/abstract transfer is a strong boundary. |
| `gse.adult.2022.c1.p20.006` | Can understand stories being told by a fluent speaker using colloquial language. | MERGE | C04 | Colloquial narrative reception. |
| `gse.adult.2022.c1.p20.007` | Can follow films employing a considerable degree of slang and idiomatic usage. | KEEP | C04 | Slang/idiom in authentic media remains explicit. |
| `gse.adult.2022.c1.p20.008` | Can recognise a speaker’s feelings or attitude in linguistically complex speech. | KEEP | C04 | Attitude interpretation remains explicit. |
| `gse.adult.2022.c1.p20.009` | Can infer meaning, opinion, attitude, etc. in fast-paced conversations between fluent speakers. | MERGE | C04 | Combines pace + inference; both conditions retained. |
| `gse.adult.2022.c1.p20.010` | Can understand the details in a linguistically complex audio recording. | MERGE | C03 | Detailed complex recording reception. |
| `gse.adult.2022.c1.p20.011` | Can understand the details of extended and linguistically complex talks on a range of political, environmental, and social issues. | KEEP | C03 | Topic examples are contexts, not three topic capabilities. |
| `gse.adult.2022.c1.p20.012` | Can recognise a wide range of idiomatic expressions and colloquialisms, appreciating register shifts. | KEEP | C04 | Register-shift recognition cross-links X-REGISTER-AUDIENCE. |

### Speaking / oral interaction — 24 / 59

| Source record | Exact source ability | Disposition | Primary home | Review note |
| --- | --- | --- | --- | --- |
| `gse.adult.2022.c1.p36.001` | Can answer questions about abstract topics clearly and in detail. | KEEP | C05 | Abstract Q&A with developed detail. |
| `gse.adult.2022.c1.p36.002` | Can substitute an equivalent term for a word they can’t recall so smoothly that it isn’t noticeable. | SUPPORTING | X-REPAIR-PRECISION | Required cross-cutting lexical repair; supports C05–C08, not a standalone capability. |
| `gse.adult.2022.c1.p36.003` | Can describe the details of problem-solution relationships using a range of linguistic devices. | KEEP | C05 | Complex relational explanation/description. |
| `gse.adult.2022.c1.p36.004` | Can contribute to group discussions even when speech is fast and colloquial. | KEEP | C07 | Genuine group interaction under pace/colloquial pressure. |
| `gse.adult.2022.c1.p36.005` | Can justify a point of view using linguistically complex language. | KEEP | C06 | Core complex-position performance. |
| `gse.adult.2022.c1.p36.006` | Can rephrase controversial statements into more neutral language. | SUPPORTING | X-REGISTER-AUDIENCE | Required pragmatic/register transformation; supports C06/C07. |
| `gse.adult.2022.c1.p36.007` | Can comment on and discuss a linguistically complex text. | KEEP | C08 | Source-responsive interaction; source text remains the input anchor. |
| `gse.adult.2022.c1.p36.008` | Can conclude a discursive argument using a range of linguistic devices. | MERGE | C06 | Argument closure/discourse control, cross-link X-DISCOURSE-FOCUS. |
| `gse.adult.2022.c1.p36.009` | Can give reasons and explanations for their opinions using linguistically complex language. | MERGE | C06 | Support/justification component of complex position. |
| `gse.adult.2022.c1.p36.010` | Can give a detailed account of a complex subject, ending with a clear conclusion. | KEEP | C05 | Extended complex account + conclusion. |
| `gse.adult.2022.c1.p36.011` | Can summarise clearly and precisely the arguments and event descriptions from a complex text. | KEEP | C08 | Oral source summary with precision. |
| `gse.adult.2022.c1.p36.012` | Can participate in linguistically complex discussions about attitudes and opinions. | MERGE | C07 | Interaction/stance context retained. |
| `gse.adult.2022.c1.p36.013` | Can contribute fluently and naturally to a conversation about a complex or abstract topic. | KEEP | C07 | Fluency/naturalness + complex/abstract interaction. |
| `gse.adult.2022.c1.p36.014` | Can summarise and comment on the content of a linguistically complex text. | MERGE | C08 | Combined source summary/commentary. |
| `gse.adult.2022.c1.p36.015` | Can participate in a fast-paced conversation with fluent speakers. | MERGE | C07 | Pace/partner condition stays explicit. |
| `gse.adult.2022.c1.p36.016` | Can participate in discussions using linguistically complex language to compare, contrast and summarise information. | KEEP | C07 | Integrated comparison/summary inside interaction; not split into solo subskills. |
| `gse.adult.2022.c1.p36.017` | Can reformulate what they want to say during a conversation or discussion using linguistically complex language. | SUPPORTING | X-REPAIR-PRECISION | Interaction repair/control; secondary home C07. |
| `gse.adult.2022.c1.p36.018` | Can use a wide range of persuasive techniques in presentations and discussions to encourage others to take a course of action. | KEEP | C06 | Persuasion crosses presentation/discussion but shares one rhetorical outcome. |
| `gse.adult.2022.c1.p36.019` | Can join a conversation already in progress between fluent speakers on complex topics. | KEEP | C07 | Turn entry is a distinct interaction condition. |
| `gse.adult.2022.c1.p36.020` | Can manage the participants in a fast-moving discussion to keep it on course. | KEEP | C07 | Interaction management/facilitation boundary preserved. |
| `gse.adult.2022.c1.p36.021` | Can tell a detailed anecdote using linguistically complex language. | MERGE | C05 | Complex narrative instance, not a separate anecdote unit. |
| `gse.adult.2022.c1.p36.022` | Can summarise group discussions on a wide range of linguistically complex topics. | KEEP | C08 | Source is live/group discourse; cross-link C07 but summary performance remains visible. |
| `gse.adult.2022.c1.p36.023` | Can comment in detail on the content of a linguistically complex radio programme or podcast in which people describe reactions or opinions. | KEEP | C08 | Detailed oral response to audio source. |
| `gse.adult.2022.c1.p36.024` | Can talk about complex financial problems in detail. | MERGE | C05 | Finance is a transfer context, not a top-level topic capability. |

### Writing / written interaction — 16 / 59

| Source record | Exact source ability | Disposition | Primary home | Review note |
| --- | --- | --- | --- | --- |
| `gse.adult.2022.c1.p43.001` | Can write a clear summary of a complex factual text, maintaining its original tone and message. | KEEP | C09 | Preserve source-record interaction mode metadata; curriculum home reflects the source-summary performance without silently rewriting inventory mode. |
| `gse.adult.2022.c1.p43.002` | Can make jokes in writing using words with similar spelling but different meanings. | KEEP | C12 | Written wordplay/rhetorical control, cross-link X-IMPLICIT-RHETORIC. |
| `gse.adult.2022.c1.p43.003` | Can write essays and reports synthesising information from a number of sources. | KEEP | C09 | Multi-source synthesis is a major C1 exit path. |
| `gse.adult.2022.c1.p43.004` | Can write a letter of application using appropriate conventions and a range of linguistically complex language. | KEEP | C11 | Functional correspondence + conventions/register. |
| `gse.adult.2022.c1.p44.001` | Can write an accurate summary of a complex, discursive text. | MERGE | C09 | Accuracy + discursive-source summary. |
| `gse.adult.2022.c1.p44.002` | Can write a detailed critical review of cultural events or literary works. | KEEP | C10 | Critical evaluation/review performance; examples do not create topic units. |
| `gse.adult.2022.c1.p44.003` | Can express themselves fluently in writing, adapting the level of formality to the context. | KEEP | C12 | Register/formality adaptation is explicit. |
| `gse.adult.2022.c1.p44.004` | Can use linguistic devices such as fronting to emphasise key information in a sentence. | SUPPORTING | X-DISCOURSE-FOCUS | Required information-structure control; secondary home C12, not an isolated fronting capability. |
| `gse.adult.2022.c1.p44.005` | Can precisely select vocabulary for rhetorical purposes. | SUPPORTING | X-IMPLICIT-RHETORIC | Required rhetorical lexical precision; secondary home C12. |
| `gse.adult.2022.c1.p44.006` | Can write summaries and reviews of professional or literary works. | SPLIT | C09 + C10 | Two design components (summary / review); remains **one source record**. |
| `gse.adult.2022.c1.p44.007` | Can take effective notes while listening to a linguistically complex audio recording. | MERGE | C09 | Cross-modal note-taking from complex audio. |
| `gse.adult.2022.c1.p44.008` | Can confidently argue a case in writing, specifying needs and objectives precisely and justifying them as necessary. | KEEP | C10 | Complex written argument + precision/justification. |
| `gse.adult.2022.c1.p44.009` | Can edit and add to a linguistically complex text to make it clearer or more concise. | KEEP | C12 | Revision/editing is an explicit C1 performance, not proofreading decoration. |
| `gse.adult.2022.c1.p44.010` | Can smoothly switch between a range of writing styles to address specific audiences and topics in a personal way. | KEEP | C12 | Audience/style transfer strongly supports C1 exit assessment. |
| `gse.adult.2022.c1.p44.011` | Can take notes to summarise the key points made during a technical or linguistically complex discussion. | MERGE | C09 | Preserve source-record interaction mode; source selection/summarisation remains central. |
| `gse.adult.2022.c1.p44.012` | Can give complex information using appropriate register and conventions. | KEEP | C11 | Complex informational writing + register/conventions. |

---

## Disposition accounting

- **KEEP:** 36
- **MERGE:** 17
- **SUPPORTING:** 5
- **SPLIT:** 1
- **Total source records:** 59

The single SPLIT creates two design mappings but **does not** increase the required source-record count. All five SUPPORTING rows remain required and must receive lifecycle/evidence later; they are not exclusions.

## Source and modality safeguards

1. Reading and listening remain receptive capabilities; later tasks cannot replace them with speaking/writing evidence.
2. Fast-conversation listening (`p20.001`) remains reception even though comprehension enables later contribution.
3. Interaction rows remain exchange/participant-management requirements rather than solo production.
4. `p43.001` and `p44.011` retain their source-record mode metadata; the curriculum does not silently rewrite canonical assignments.
5. C08/C09 source transformation is not automatically called mediation. The C1 exit contract's mediation boundary must be reconciled explicitly during later exit/carry-forward review.
6. `p36.024` does not create a finance unit; domain/topic content is a transfer context serving C05.
7. Wordplay, fronting, rhetorical vocabulary, repair, and register controls are not inflated into topic units simply because they are salient C1 features.

## Stage-1 critic

- Required source abilities reviewed: **59 / 59**.
- Orphan required abilities: **0**.
- Silent exclusions: **0**.
- Source-record inflation from SPLIT: **0**.
- Receptive modalities silently converted to production: **0**.
- Interaction requirements converted to solo tasks: **0**.
- Topic-only fake capabilities: **0**.
- Cross-cutting requirements promoted to fake standalone capabilities: **0**.
- Unit count selected: **0**.
- Lesson count selected: **0**.
- Final semantic/control roles assigned: **0** (deferred to Stage 8).

## Architecture decision

Stage 1 proposes **12 top-level C1 capability families plus seven cross-cutting requirement groups**. This is a manual review candidate and remains owner-approval pending. Later phrase, grammar, lexical, pronunciation, exit, and B2 carry-forward evidence may reopen/refine the architecture before Stage 5.

### Handoff to Stage 2

Phrase review should test especially:

- register/formality and audience adaptation;
- idiomatic/non-literal/wordplay meaning;
- argument, concession, persuasion and stance;
- source summary/synthesis language;
- discussion management, reformulation and repair;
- discourse focus/emphasis and logical organisation;
- whether any phrase evidence exposes a missing performance boundary rather than merely a lexical theme.
