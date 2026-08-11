import { escapeHtml, list } from "./dom.js";


export function renderUnitReview(screen, scope, progress, callbacks) {
  const unit = scope.units.find(row => row.unit_id === "a1.unit01.first_connections");
  const stations = unit.unit_review.mastery_stations;
  const readyCount = unit.lessons.filter(row => progress.practiced.includes(row.lesson_id)).length;
  screen.innerHTML = `<section class="panel">
    <p class="eyebrow">UNIT 1 · FRESH REVIEW</p>
    <h2>مراجعة التعارف الأول</h2>
    <p class="lead">ثلاث محطات جديدة تجمع الاستماع والكلام والقراءة والكتابة. أنهيت تجربة ${readyCount} من 9 دروس الوحدة.</p>
    ${readyCount < 9 ? `<p class="release-note">يفضل تجربة الدروس التسعة أولًا، لكن يمكنك معاينة شكل المراجعة الآن.</p>` : ""}
    <div class="content-stack">${stations.map(station => `<article class="mastery-card">
      <strong>${escapeHtml(station.title)}</strong>
      <p class="english">${escapeHtml(station.fresh_task)}</p>
      <p>الفشل الحاسم: ${escapeHtml(station.critical_failure)}</p>
      ${list(station.dimension_codes)}
      <textarea aria-label="محاولة غير محفوظة لمحطة ${escapeHtml(station.title)}" placeholder="خطّط أو اكتب هنا بمعلومات خيالية…"></textarea>
    </article>`).join("")}</div>
    <p class="privacy-inline">لا تُحفظ الإجابات، والمحاولة هنا لا تمنح إتقانًا.</p>
    <div class="lesson-actions"><button class="button secondary" id="reviewHome" type="button">العودة للدروس</button><button class="button secondary" id="reviewAttempted" type="button">سجل أنني عاينت المراجعة</button><button class="button primary" id="reviewNext" type="button">ابدأ الوحدة الثانية</button></div>
    <div class="status-message" id="reviewStatus">تم حفظ حالة المعاينة على هذا الجهاز فقط.</div>
  </section>`;
  screen.querySelector("#reviewHome").addEventListener("click", callbacks.home);
  screen.querySelector("#reviewAttempted").addEventListener("click", () => {
    callbacks.attempted();
    screen.querySelector("#reviewStatus").classList.add("show");
  });
  screen.querySelector("#reviewNext").addEventListener("click", callbacks.next);
}
