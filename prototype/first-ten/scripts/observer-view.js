import { DECISIONS, ISSUES, LESSON_IDS, STATIONS, VISIT_PLAN, optionList } from "./observer-config.js";

const ratingOptions = `<option value="">—</option><option>0</option><option>1</option><option>2</option>`;
const experienceOptions = `<option value="">—</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option>`;

function selectField(label, name, options) {
  return `<label>${label}<select data-field="${name}">${options}</select></label>`;
}

function attemptBlock(kind, title) {
  return `<div class="attempt-block" data-attempt="${kind}">
    <h4>${title}</h4>
    <div class="check-grid">
      <label><input data-field="attempted" type="checkbox"> تمت المحاولة</label>
      <label><input data-field="modelVisible" type="checkbox"> ظهر نموذج الإجابة</label>
    </div>
    <div class="attempt-grid">
      ${selectField("فهم المهمة", "comprehension", ratingOptions)}
      ${selectField("تحقيق النتيجة", "outcome", ratingOptions)}
      ${selectField("النقل لموقف جديد", "transfer", ratingOptions)}
      ${selectField("التحكم أو الإصلاح", "control", ratingOptions)}
      ${selectField("القرار", "decision", optionList(DECISIONS))}
      ${selectField("قرار المقيم الثاني", "secondaryDecision", `<option value="">—</option>${optionList(DECISIONS)}`)}
    </div>
  </div>`;
}

function lessonCard(lessonId) {
  return `<article class="lesson-observation" data-lesson="${lessonId}">
    <h3>${lessonId}</h3>
    <div class="check-grid">
      <label><input data-field="completed" type="checkbox"> اكتمل الدرس</label>
    </div>
    <div class="form-grid">
      <label>المدة بالثواني<input data-field="seconds" type="number" min="0" max="3600" value="0"></label>
      <label>مساعدة لا تكشف الإجابة<input data-field="safeHelp" type="number" min="0" max="20" value="0"></label>
      <label>مساعدة تكشف الإجابة<input data-field="revealingHelp" type="number" min="0" max="20" value="0"></label>
      ${selectField("مشكلة مضبوطة", "issue", optionList(ISSUES))}
      ${selectField("الصعوبة 1–5", "difficulty", experienceOptions)}
      ${selectField("الإرهاق 1–5", "fatigue", experienceOptions)}
      ${selectField("الملل 1–5", "boredom", experienceOptions)}
      ${selectField("القيمة 1–5", "value", experienceOptions)}
    </div>
    ${attemptBlock("primary", "المهمة الجديدة الأساسية")}
    ${attemptBlock("replacement", "المهمة البديلة — فقط عند الحاجة")}
  </article>`;
}

export function initialiseSelectors() {
  document.querySelector("#visitNumber").innerHTML = [1, 2, 3, 4, 5, 6]
    .map(value => `<option>${value}</option>`).join("");
  document.querySelector("#probeLesson").innerHTML += LESSON_IDS
    .map(value => `<option>${value}</option>`).join("");
}

export function renderVisit(visitNumber) {
  const lessons = VISIT_PLAN[visitNumber];
  document.querySelector("#visitPlan").textContent = `خطة الزيارة ${visitNumber}: ${lessons.join("، ")}${visitNumber === 6 ? " + محطات الوحدة الأولى" : ""}`;
  document.querySelector("#lessonRecords").innerHTML = lessons.map(lessonCard).join("");
  const stationSection = document.querySelector("#stationSection");
  stationSection.hidden = visitNumber !== 6;
  document.querySelector("#stationRecords").innerHTML = STATIONS.map(id =>
    selectField(id, id, optionList(DECISIONS))).join("");
}
