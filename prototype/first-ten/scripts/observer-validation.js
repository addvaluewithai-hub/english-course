const requiredChecks = [
  "adult", "arabicDominant", "beginner", "noExposure", "notAuthor",
  "voluntary", "dataBoundary", "withdrawalRoute", "agreed", "reconsent"
];
const byId = id => document.querySelector(`#${id}`);

function attemptErrors(attempt, label) {
  const errors = [];
  const ratings = Object.values(attempt.ratings);
  if (attempt.attempted && ratings.some(value => value === null)) errors.push(`${label}: أكمل الدرجات الأربع.`);
  if (!attempt.attempted && (attempt.decision !== "not_rated" || ratings.some(value => value !== null))) {
    errors.push(`${label}: محاولة غير منفذة يجب أن تبقى غير مقيّمة.`);
  }
  if (attempt.decision === "demonstrated" && (attempt.answer_model_visible || ratings.some(value => value !== 2))) {
    errors.push(`${label}: demonstrated يتطلب 2 في كل الأبعاد من غير ظهور نموذج الإجابة.`);
  }
  return errors;
}

export function validateRecord(record) {
  const errors = [];
  if (!/^P10-[A-Z0-9]{4,8}$/.test(record.participant_code)) errors.push("كود المشارك غير صحيح.");
  if (requiredChecks.some(id => !byId(id).checked)) errors.push("أكمل الأهلية والموافقة وإعادة التأكيد.");
  if (record.evidence_mode === "real_observation" &&
      (!record.media.all_transcript_matched || !record.media.all_listened)) {
    errors.push("لا تبدأ سجلًا حقيقيًا قبل مطابقة كل الفيديوهات والاستماع إليها.");
  }
  const currentNumber = Number(byId("visitNumber").value);
  const visit = record.visits.find(row => row.visit_number === currentNumber);
  for (const lesson of visit.lesson_records) {
    errors.push(...attemptErrors(lesson.primary, `${lesson.lesson_id} الأساسية`));
    errors.push(...attemptErrors(lesson.replacement, `${lesson.lesson_id} البديلة`));
    if (lesson.replacement.attempted && !lesson.primary.attempted) errors.push(`${lesson.lesson_id}: البديلة لا تسبق الأساسية.`);
    if (lesson.issue_codes.includes("none") && lesson.issue_codes.length > 1) errors.push(`${lesson.lesson_id}: none لا يجتمع مع مشكلة.`);
  }
  if (record.withdrawal.status === "withdrew" && !record.withdrawal.reason_code) errors.push("اختر سبب الانسحاب المنضبط.");
  if (record.withdrawal.status !== "withdrew" && record.withdrawal.reason_code) errors.push("سبب الانسحاب يستخدم فقط مع withdrew.");
  return errors;
}
