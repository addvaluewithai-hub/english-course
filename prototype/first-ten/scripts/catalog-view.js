import { escapeHtml } from "./dom.js";
import { RELEASE_WARNING, UNIT_LABELS } from "./config.js";


export function renderCatalog(screen, release, progress, navigate) {
  let currentUnit = "";
  const cards = [];
  for (const lesson of release.lessons) {
    if (lesson.unit_id !== currentUnit) {
      currentUnit = lesson.unit_id;
      cards.push(`<h3 class="rail-unit">${escapeHtml(UNIT_LABELS[currentUnit] || currentUnit)}</h3>`);
    }
    const practiced = progress.practiced.includes(lesson.lesson_id);
    cards.push(`<article class="lesson-card ${practiced ? "practiced" : ""}">
      <small>${escapeHtml(lesson.lesson_id)} · الدرس ${lesson.global_sequence_position}</small>
      <h3>${escapeHtml(lesson.title.ar)}</h3>
      <p class="english">${escapeHtml(lesson.title.en)}</p>
      <p>${escapeHtml(lesson.outcome_statement)}</p>
      <button class="button ${practiced ? "secondary" : "primary"}" type="button" data-open-lesson="${lesson.lesson_id}">
        ${practiced ? "افتح مرة أخرى" : "افتح الدرس"}
      </button>
    </article>`);
  }
  cards.splice(10, 0, `<article class="unit-review-card">
    <small>UNIT 1 REVIEW</small>
    <h3>مراجعة الوحدة الأولى</h3>
    <p>ثلاث محطات جديدة تجمع التعارف والبيانات والكتابة. المحاولة لا تمنح إتقانًا آليًا.</p>
    <button class="button secondary" type="button" data-unit-review>افتح مراجعة الوحدة</button>
  </article>`);
  screen.innerHTML = `<section class="panel">
    <p class="eyebrow">CONTENT RELEASE · V1</p>
    <h2>جرّب التدرّج، مش درس منفرد</h2>
    <p class="lead">هذه أول عشرة مواقع فعلية في A1: الوحدة الأولى كاملة ثم بداية الوحدة الثانية. كل درس يضيف قدرة، ويعيد استخدام ما قبله داخل مهمة جديدة.</p>
    <p class="release-note">${escapeHtml(RELEASE_WARNING)}</p>
    <div class="lesson-grid">${cards.join("")}</div>
  </section>`;
  screen.querySelectorAll("[data-open-lesson]").forEach(button => {
    button.addEventListener("click", () => navigate({ lesson: button.dataset.openLesson }));
  });
  screen.querySelector("[data-unit-review]").addEventListener("click", () => navigate({ review: "unit1" }));
}
