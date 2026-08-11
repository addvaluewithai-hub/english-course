import { SECTION_LABELS, RELEASE_WARNING } from "./config.js";
import { bindActivities, renderActivities } from "./activity-view.js";
import { cleanTranscript, collectStrings, escapeHtml, list, speak } from "./dom.js";


function overview(pkg) {
  const intro = pkg.packet.exact_introductions.map(row => row.label);
  const recycle = pkg.packet.exact_recycles.map(row => row.label);
  return `<div class="content-stack">
    <p class="lead">${escapeHtml(pkg.manifest.goal.ar)}</p>
    <p class="release-note">${escapeHtml(RELEASE_WARNING)}</p>
    <div class="info-card"><strong>النتيجة القابلة للملاحظة</strong><span class="english">${escapeHtml(pkg.contract.outcome_statement)}</span></div>
    <div class="info-card"><strong>الجديد في مكانه</strong>${intro.length ? list(intro) : "لا يوجد عنصر نظام جديد؛ هذا درس دمج وتطبيق."}</div>
    <div class="info-card"><strong>إعادة استخدام مقصودة</strong>${recycle.length ? list(recycle) : "المهمة تعتمد على القدرة نفسها أو تمهّد لتكرار لاحق."}</div>
  </div>`;
}

function video(pkg) {
  return `<div class="content-stack">
    <div class="video-placeholder"><b>مصدر الفيديو جاهز · الرندر النهائي غير موجود</b><p>نص مدرس واحد كامل، وكل إنجليزي منطوق له لغة ونطق محددان. استمع للرندر النهائي لاحقًا قبل اختبار البشر.</p></div>
    <details><summary>Scene</summary><pre class="context-source">${escapeHtml(pkg.scene)}</pre></details>
    <details><summary>Sample Context</summary><pre class="context-source">${escapeHtml(pkg.context)}</pre></details>
    <details open><summary>نص الفيديو المقروء</summary><div class="transcript">${escapeHtml(cleanTranscript(pkg.transcript))}</div></details>
  </div>`;
}

function contentMap(pkg) {
  const content = pkg.content;
  const situation = content.situation || {};
  const modelLines = collectStrings(content.model).filter(value => /[A-Za-z]/.test(value)).slice(0, 14);
  const notices = (content.notice || []).map(row =>
    `<div class="info-card">${Object.values(row).filter(value => typeof value === "string").map(escapeHtml).join(" · ")}</div>`
  ).join("");
  const toolkit = collectStrings(content.toolkit).slice(0, 40);
  return `<div class="content-stack">
    <div class="info-card"><strong>${escapeHtml(situation.title_ar || "موقف اليوم")}</strong>${escapeHtml(situation.prompt_ar || "")}</div>
    <div class="model-box">${modelLines.map((line, index) => `<button class="choice english" type="button" data-speak="${index}">${escapeHtml(line)} 🔊</button>`).join("")}</div>
    <h3>لاحظ المعنى والشكل</h3>${notices}
    <h3>الشرح المختصر</h3>${list(content.explanation_ar || [])}
    <h3>صندوق الأدوات</h3><div class="chip-grid">${toolkit.map(item => `<span class="chip">${escapeHtml(item)}</span>`).join("")}</div>
  </div>`;
}

function mastery(pkg) {
  const task = pkg.assessment.mastery_task;
  return `<div class="content-stack">
    <div class="mastery-card">
      <strong>${escapeHtml(task.scenario_ar)}</strong>
      <p class="english">${escapeHtml(task.prompt_en)}</p>
      <p>${escapeHtml(task.support)}</p>
      ${list(task.required.map(item => item.replaceAll("_", " ")), "required-list")}
    </div>
    <label class="privacy-inline">محاولة مستقلة بمعلومات خيالية — لا تُحفظ
      <textarea id="masteryDraft" placeholder="خطّط أو اكتب هنا…"></textarea>
    </label>
    <button class="button primary" id="attemptButton" type="button">سجل أنني جرّبت المهمة</button>
    <div class="status-message" id="attemptStatus">تم تسجيل التجربة على هذا الجهاز فقط. هذا لا يعني إتقانًا؛ التقييم الحقيقي يحتاج ملاحظًا ومهمة جديدة.</div>
  </div>`;
}

function review(pkg) {
  return `<div class="content-stack">
    <p class="lead">المراجعة تغيّر المحتوى ولا تعيد نفس الإجابة.</p>
    ${pkg.assessment.delayed_review.map(row => `<div class="info-card"><strong>${escapeHtml(row.when)}</strong>${escapeHtml(row.task)}</div>`).join("")}
    <div class="info-card"><strong>محاولة بديلة</strong>${escapeHtml(pkg.assessment.replacement_mastery_task.scenario_ar)}<p class="english">${escapeHtml(pkg.assessment.replacement_mastery_task.prompt_en)}</p></div>
  </div>`;
}

function sectionBody(pkg, section) {
  if (section === "video") return video(pkg);
  if (section === "content") return contentMap(pkg);
  if (section === "practice") return `<div class="content-stack">${renderActivities(pkg.activities.activities)}<p class="privacy-inline">الإجابات في المساحات النصية لا تُحفظ.</p></div>`;
  if (section === "mastery") return mastery(pkg);
  if (section === "review") return review(pkg);
  return overview(pkg);
}

export function renderLesson(screen, pkg, section, callbacks) {
  const sections = Object.keys(SECTION_LABELS);
  screen.innerHTML = `<article class="panel">
    <div class="lesson-meta"><span>${escapeHtml(pkg.contract.lesson_id)}</span><span>الموقع ${pkg.contract.global_sequence_position} من 10</span></div>
    <h2>${escapeHtml(pkg.contract.title.ar)}</h2>
    <p class="english lead">${escapeHtml(pkg.contract.title.en)}</p>
    <nav class="section-tabs" aria-label="أجزاء الدرس">${sections.map(key => `<button class="tab ${key === section ? "active" : ""}" type="button" data-section="${key}">${SECTION_LABELS[key]}</button>`).join("")}</nav>
    <section>${sectionBody(pkg, section)}</section>
    <div class="lesson-actions"><button class="button secondary" type="button" data-prev>الدرس السابق</button><button class="button primary" type="button" data-next>الدرس التالي</button></div>
  </article>`;
  screen.querySelectorAll("[data-section]").forEach(button => button.addEventListener("click", () => callbacks.section(button.dataset.section)));
  screen.querySelector("[data-prev]").addEventListener("click", callbacks.previous);
  screen.querySelector("[data-next]").addEventListener("click", callbacks.next);
  const modelLines = collectStrings(pkg.content.model).filter(value => /[A-Za-z]/.test(value)).slice(0, 14);
  screen.querySelectorAll("[data-speak]").forEach(button => button.addEventListener("click", () => speak(modelLines[Number(button.dataset.speak)])));
  bindActivities(screen);
  screen.querySelector("#attemptButton")?.addEventListener("click", () => {
    callbacks.practiced();
    screen.querySelector("#attemptStatus").classList.add("show");
  });
}
