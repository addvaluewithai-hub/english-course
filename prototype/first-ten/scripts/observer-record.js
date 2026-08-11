import { RELEASE_ID, STATIONS, STUDY_ID } from "./observer-config.js";

const byId = id => document.querySelector(`#${id}`);
const checked = id => byId(id).checked;
const value = (root, field) => root.querySelector(`[data-field="${field}"]`).value;
const number = (root, field) => Number(value(root, field));
const nullableNumber = (root, field) => value(root, field) === "" ? null : number(root, field);

function readAttempt(card, kind) {
  const root = card.querySelector(`[data-attempt="${kind}"]`);
  const decision = value(root, "decision");
  const secondary = value(root, "secondaryDecision") || null;
  return {
    attempted: root.querySelector('[data-field="attempted"]').checked,
    answer_model_visible: root.querySelector('[data-field="modelVisible"]').checked,
    ratings: {
      comprehension: nullableNumber(root, "comprehension"),
      outcome: nullableNumber(root, "outcome"),
      transfer: nullableNumber(root, "transfer"),
      control_or_repair: nullableNumber(root, "control")
    },
    decision,
    secondary_decision: secondary,
    exact_agreement: secondary === null ? null : secondary === decision
  };
}

function readLesson(card) {
  const issue = value(card, "issue");
  return {
    lesson_id: card.dataset.lesson,
    completed: card.querySelector('[data-field="completed"]').checked,
    duration_seconds: number(card, "seconds"),
    help: {
      non_answer_revealing_count: number(card, "safeHelp"),
      answer_revealing_count: number(card, "revealingHelp")
    },
    primary: readAttempt(card, "primary"),
    replacement: readAttempt(card, "replacement"),
    experience: {
      difficulty: nullableNumber(card, "difficulty"),
      fatigue: nullableNumber(card, "fatigue"),
      boredom: nullableNumber(card, "boredom"),
      perceived_value: nullableNumber(card, "value")
    },
    issue_codes: [issue]
  };
}

function readProbe() {
  if (!byId("probeLesson").value) return [];
  if (!byId("probeDays").value) throw new Error("اكتب عدد الأيام للاختبار المؤجل.");
  return [{
    probe_id: `P10-PROBE-${String(byId("visitNumber").value).padStart(2, "0")}`,
    source_lesson_id: byId("probeLesson").value,
    days_since_lesson: Number(byId("probeDays").value),
    decision: byId("probeDecision").value
  }];
}

function readStations(visitNumber) {
  if (visitNumber !== 6) return [];
  return STATIONS.map(id => ({
    station_id: id,
    decision: document.querySelector(`[data-field="${id}"]`).value
  }));
}

function visitRecord() {
  const visitNumber = Number(byId("visitNumber").value);
  return {
    visit_number: visitNumber,
    day_number: Number(byId("dayNumber").value),
    consent_reaffirmed: checked("reconsent"),
    completion: byId("visitCompletion").value,
    duration_seconds: Number(byId("visitSeconds").value),
    lesson_records: [...document.querySelectorAll("[data-lesson]")].map(readLesson),
    unit1_stations: readStations(visitNumber),
    delayed_probes: readProbe()
  };
}

export function newRecord() {
  return {
    schema_version: 1,
    study_id: STUDY_ID,
    participant_code: byId("participantCode").value.trim(),
    evidence_mode: byId("evidenceMode").value,
    eligibility: {
      adult: checked("adult"), arabic_dominant: checked("arabicDominant"),
      beginner_boundary: checked("beginner"), no_answer_material_exposure: checked("noExposure"),
      not_owner_or_author: checked("notAuthor")
    },
    initial_consent: {
      voluntary: checked("voluntary"), data_boundary_understood: checked("dataBoundary"),
      withdrawal_route_understood: checked("withdrawalRoute"), agreed: checked("agreed")
    },
    media: {
      release_id: RELEASE_ID, render_batch_id: byId("renderBatch").value.trim(),
      all_transcript_matched: checked("transcriptMatched"), all_listened: checked("allListened")
    },
    visits: [],
    withdrawal: { status: "active", after_visit: null, reason_code: null },
    privacy: {
      contains_direct_identifier: false, contains_raw_answer: false,
      contains_audio: false, contains_video: false, stored_outside_repository: true
    }
  };
}

export function mergeVisit(base) {
  const current = visitRecord();
  const visits = (base.visits || []).filter(row => row.visit_number !== current.visit_number);
  visits.push(current);
  base.visits = visits.sort((a, b) => a.visit_number - b.visit_number);
  base.withdrawal.status = byId("journeyStatus").value;
  base.withdrawal.after_visit = base.withdrawal.status === "active" ? null : current.visit_number;
  base.withdrawal.reason_code = byId("withdrawalReason").value || null;
  return base;
}
