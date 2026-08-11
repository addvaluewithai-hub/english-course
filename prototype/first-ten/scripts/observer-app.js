import { initialiseSelectors, renderVisit } from "./observer-view.js";
import { mergeVisit, newRecord } from "./observer-record.js";
import { validateRecord } from "./observer-validation.js";

const byId = id => document.querySelector(`#${id}`);
let importedRecord = null;

function setError(message = "") {
  byId("formError").textContent = message;
}

function build() {
  if (!byId("observerForm").reportValidity()) throw new Error("أكمل الحقول المطلوبة أولًا.");
  const base = importedRecord ? structuredClone(importedRecord) : newRecord();
  if (base.participant_code !== byId("participantCode").value.trim()) {
    throw new Error("كود الشاشة لا يطابق كود السجل المستورد.");
  }
  const record = mergeVisit(base);
  const errors = validateRecord(record);
  if (errors.length) throw new Error(errors.join("\n"));
  return record;
}

function handle(action) {
  try { setError(); action(build()); }
  catch (error) { setError(error.message); }
}

function show(record) {
  byId("recordPreview").textContent = JSON.stringify(record, null, 2);
  byId("recordPreview").classList.add("show");
}

function download(record) {
  show(record);
  const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${record.participant_code}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
}

async function importRecord(event) {
  try {
    const file = event.target.files[0];
    if (!file) return;
    const record = JSON.parse(await file.text());
    if (record.study_id !== "a1_first_10_progression_pilot_v1") throw new Error("هذا ليس سجل التجربة المطلوبة.");
    importedRecord = record;
    byId("participantCode").value = record.participant_code;
    byId("evidenceMode").value = record.evidence_mode;
    byId("renderBatch").value = record.media.render_batch_id;
    setError(`تم استيراد ${record.visits.length} زيارة. أضف الزيارة التالية ثم نزّل النسخة المحدّثة.`);
  } catch (error) { setError(error.message); }
}

initialiseSelectors();
renderVisit(1);
byId("visitNumber").onchange = event => renderVisit(Number(event.target.value));
byId("recordFile").onchange = importRecord;
byId("previewButton").onclick = () => handle(show);
byId("downloadButton").onclick = () => handle(download);
