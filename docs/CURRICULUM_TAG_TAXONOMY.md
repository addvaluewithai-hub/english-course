# A1 Curriculum Tag Taxonomy v1.0.0

## Purpose and evidence boundary

These controlled codes normalize the reviewed GSE A1 objectives and CEFR A1
descriptors for comparison in Phase 2. They are project interpretations, not wording or
labels published by Pearson or the Council of Europe. Verbatim text, source facts,
locations, hashes, inclusion decisions, and source-specific warnings remain unchanged.

Tags describe what the evidence record supports; they do not create a unit, cluster,
lesson, prerequisite, or final learner outcome. Multiple tags are allowed where one
source record explicitly spans purposes or channels.

## Skill and domain codes

| Code | Meaning |
| --- | --- |
| `listening` | Meaning is received through spoken language. |
| `reading` | Meaning is received through written language. |
| `speaking` | Meaning is produced through spoken language. |
| `writing` | Meaning is produced through written language. |
| `viewing` | Visual context or signed/visual content is part of reception. |
| `non_verbal` | Gesture or another non-verbal signal is explicit in performance. |
| `language_system` | A channel-neutral linguistic, sociolinguistic, or pragmatic competence. |

`language_system` prevents a channel-neutral competence descriptor from being falsely
claimed as speaking-only or writing-only. It is a comparison domain, not a fifth
language skill.

## Communication-mode codes

| Code | Meaning |
| --- | --- |
| `reception` | Receiving and constructing meaning. |
| `production` | Producing a spoken or written contribution without required turn exchange. |
| `interaction` | Co-constructing an exchange with another participant. |
| `online_interaction` | Interacting through an online written or multimodal channel. |
| `mediation` | Relaying, translating, processing, or facilitating meaning for others. |
| `communicative_competence` | Language-system control supporting communication. |

CEFR mode labels map directly to these codes. Pearson labels only Reading, Listening,
Speaking, and Writing, so GSE modes are inferred from the objective action: Reading and
Listening map to reception; Writing maps to production except correspondence; and
Speaking maps to interaction only when an exchange, request, social response, or
transaction is required. This inference remains in `interpretation.mode_codes`.

## Communicative-function codes

| Code | Controlled meaning |
| --- | --- |
| `comprehend_information` | Understand stated meaning or factual content. |
| `follow_instructions` | Understand and act on directions, commands, or instructions. |
| `locate_information` | Find, identify, recognise, or extract a target detail. |
| `describe` | Describe a person, object, place, situation, or routine. |
| `give_information` | State or present information without a required exchange. |
| `ask_for_information` | Request a specific fact or explanation. |
| `exchange_information` | Ask, answer, or reciprocally share information. |
| `introduce` | Introduce oneself or another person. |
| `socialize` | Establish or maintain basic social contact and politeness. |
| `express_preference` | State or exchange likes, dislikes, or preferences. |
| `express_feeling` | State a feeling or personal emotional response. |
| `express_ability` | State ability or lack of ability. |
| `request` | Ask for an action, item, help, attention, food, or directions. |
| `respond_to_request_or_offer` | Accept, agree to, or otherwise answer an offer/request. |
| `transact` | Obtain goods/services or complete a practical transaction. |
| `correspond` | Compose or exchange a note, message, email, postcard, or posting. |
| `complete_form` | Supply information in a form or application. |
| `clarify_or_repair` | Signal non-understanding, compensate, clarify, or repair communication. |
| `infer_meaning` | Infer an unfamiliar item from form or context. |
| `mediate_information` | Relay or process information across people, texts, or languages. |
| `translate` | Give a rough oral or written translation between languages. |
| `facilitate_interaction` | Invite, support, or sustain others' collaborative contribution. |
| `reproduce_language` | Copy, spell, repeat, or read supplied language aloud. |
| `control_language_form` | Control grammar, vocabulary, sound, spelling, punctuation, or cohesion. |

## Deterministic assignment and ambiguity

`scripts/tag_gse.py` assigns GSE tags from its source skill and action wording.
`scripts/tag_cefr.py` assigns CEFR tags from its source mode, skill hierarchy, scale,
and descriptor action. `scripts/curriculum_tagging.py` applies those decisions without
changing evidence fields, and `scripts/normalize_curriculum_tags.py` updates the four
derived/reviewed collections reproducibly.

The CEFR personal-response descriptor does not fix whether the learner responds orally
or in writing. Both supported productive channels are tagged and the uncertainty is
retained in `interpretation.ambiguities`. Multi-tag records are not automatically
ambiguous: explicit compound source actions retain all supported purposes. Unknown
source labels or an empty tag group are validation failures rather than silent guesses.

Candidate clusters are now governed separately by `docs/CANDIDATE_UNIT_MAP.md`. These
codes remain broad audit aids and must not be treated as a final unit structure or
lesson-sized ability taxonomy.
The source-record schema rejects any skill, mode, or function code outside these lists.
