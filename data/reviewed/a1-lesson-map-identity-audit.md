# A1 Lesson Map: Identity Partition Audit

Status: reviewed draft partition for `LESSON-002`; the task and global map remain in
progress. Candidate-unit names and the working sequence are provisional.

## Partition outcome

All 24 reviewed records assigned to `identity_personal_information` are reconciled:

- 22 records appear as non-context candidate evidence;
- 2 identity-assigned CEFR competence records are part of the passed concurrent
  `basic_language_control` support definition; and
- 3 compound CEFR records use named partial coverage so unclaimed clauses remain
  visible for later cluster partitions.

The support definitions also retain five passed `CUR-006` records outside the identity
assignment: grammatical and phonological control plus overall interaction and two
clarification descriptors. In total, the partition cites 29 unique included records.

## Candidate review

| Candidate | Primary performance | Evidence | Scope |
| --- | --- | ---: | --- |
| `locate_written_personal_details` | Locate details in a short text | 1 | focused |
| `understand_spoken_personal_introductions` | Identify details in an introduction | 2 | focused |
| `understand_spoken_contact_details` | Record a caller name and number | 2 | focused |
| `give_short_self_introduction` | Give a bounded spoken introduction | 6 | standard |
| `exchange_personal_details_orally` | Ask and answer direct questions | 4 | standard |
| `complete_personal_details_form` | Fill an unfamiliar simple form | 2 | standard |
| `write_short_personal_profile` | Write a few profile sentences | 3 | standard |
| `exchange_personal_details_in_writing` | Request or pass details in a message | 1 | focused |
| `relay_personal_details_in_english` | Mediate another person's details | 1 | focused |

Each candidate passes the six contract coherence tests in its authored draft. The
separations are purpose-based: reception, monologic output, form completion, written
interaction, oral interaction, and mediation need different fresh tasks and mastery
judgments. Shared personal-information vocabulary alone was not used as a merge reason.

## Source-fidelity review

The deterministic builder copies dataset, source, raw-file, exact PDF location, and
source-text hash fields from the accepted reviewed collections. Source text remains
unchanged in those collections and is not copied into interpretation fields.

Named partial records:

- `cefr.cv2020.p067.creative_writing.01`: self/residence/role coverage only; broader
  imaginary-person coverage remains for an adjacent partition.
- `cefr.cv2020.p079.information_exchange.03`: personal questions and residence only;
  people-known and possession examples remain visible for adjacent work.
- `cefr.cv2020.p116.acting_as_an_intermediary_in_informal_situations.01`: relaying
  personal details only; other predictable information remains unmapped here.

No candidate uses context-only evidence. No language target or Arabic-speaker error was
invented: those arrays stay empty until grammar, vocabulary, pronunciation, and error
evidence is deliberately reviewed in a later `LESSON-002` partition.

## Balance and support review

The nine candidates collectively represent listening, reading, speaking, and writing,
plus reception, production, interaction, and mediation. This is presence evidence, not
a claim of equal instructional weight.

All candidates cite `basic_language_control`. The two interaction candidates also cite
`interaction_repair`. No hard prerequisite, successor, unit boundary, or final global
order is claimed. The JSON sequence is only a deterministic partition-local working
order required by the map envelope.

## Open review items

- Independent curriculum review is still required before candidate approval.
- Partial clauses and multi-cluster records must be reconciled as adjacent partitions
  are authored; repeated full anchors remain prohibited.
- Global duplicate, orphan, prerequisite, balance, and final sequence audits cannot
  pass until all included source records are normalized.
- Language targets, Arabic-speaker error hypotheses, and time estimates remain open and
  must not be filled without evidence.
