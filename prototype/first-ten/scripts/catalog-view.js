import { escapeHtml } from "./dom.js";
import { UNIT_LABELS } from "./config.js";

function feedbackSummary(release, feedback) {
  const rows = release.lessons.filter(lesson => feedback[lesson.lesson_id]).map(lesson => {
    const value = feedback[lesson.lesson_id];
    return `${lesson.lesson_id} | الشرح: ${value.clarity} | التجربة: ${value.enjoyment} | المدة: ${value.pace} | النتيجة: ${value.confidence}`;
  });
  return [`انطباعي عن تجربة أول 10 دروس`, `الدروس التي قيّمتها: ${rows.length}/10`, ...rows].join("\n");
}

async function copyFeedback(release, progress, status) {
  try {
    await navigator.clipboard.writeText(feedbackSummary(release, progress.feedback));
    status.textContent = "تم نسخ انطباعك. ابعته لصاحب التجربة في رسالة عادية.";
  } catch {
    status.textContent = "تعذر النسخ التلقائي. افتح التجربة من localhost وحاول مرة أخرى.";
  }
  status.classList.add("show");
}

export function renderCatalog(screen, release, progress, navigate) {
  let currentUnit = "";
  const cards = [];
  for (const lesson of release.lessons) {
    if (lesson.unit_id !== currentUnit) {
      currentUnit = lesson.unit_id;
      cards.push(`<h3 class="rail-unit">${escapeHtml(UNIT_LABELS[currentUnit] || currentUnit)}</h3>`);
    }
    const completed = progress.practiced.includes(lesson.lesson_id);
    cards.push(`<article class="lesson-card ${completed ? "practiced" : ""}">
      <small>${escapeHtml(lesson.lesson_id)} · الدرس ${lesson.global_sequence_position}</small>
      <h3>${escapeHtml(lesson.title.ar)}</h3>
      <p class="english">${escapeHtml(lesson.title.en)}</p>
      <button class="button ${completed ? "secondary" : "primary"}" type="button" data-open-lesson="${lesson.lesson_id}">
        ${completed ? "جرّبه مرة أخرى" : "ابدأ الدرس"}
      </button>
    </article>`);
  }
  cards.splice(10, 0, `<article class="unit-review-card">
    <small>UNIT 1 REVIEW</small><h3>تحدّي الوحدة الأولى</h3>
    <p>بعد أول 9 دروس، جرّب ثلاث مواقف جديدة قبل بداية الوحدة الثانية.</p>
    <button class="button secondary" type="button" data-unit-review>ابدأ التحدّي</button>
  </article>`);
  const nextLesson = release.lessons.find(lesson => !progress.practiced.includes(lesson.lesson_id)) || release.lessons[0];
  const feedbackCount = Object.keys(progress.feedback).length;
  screen.innerHTML = `<section class="panel student-home">
    <p class="eyebrow">10 REAL LESSONS · ONE SIMPLE JOURNEY</p>
    <h2>جرّب الإنجليزي كطالب، مش كمراجع محتوى</h2>
    <p class="lead">في كل درس: فيديو، تطبيق خطوة بخطوة، تحدّي أخير، ثم انطباع سريع.</p>
    <div class="hero-actions">
      <button class="button primary" type="button" data-continue>ابدأ أو كمّل التجربة</button>
      <button class="button secondary" type="button" data-copy-feedback ${feedbackCount ? "" : "disabled"}>انسخ انطباعي (${feedbackCount}/10)</button>
    </div>
    <div class="status-message" data-copy-status></div>
    <div class="lesson-grid">${cards.join("")}</div>
  </section>`;
  screen.querySelector("[data-continue]").onclick = () => navigate({ lesson: nextLesson.lesson_id });
  screen.querySelectorAll("[data-open-lesson]").forEach(button => {
    button.onclick = () => navigate({ lesson: button.dataset.openLesson });
  });
  screen.querySelector("[data-unit-review]").onclick = () => navigate({ review: "unit1" });
  screen.querySelector("[data-copy-feedback]").onclick = () => copyFeedback(release, progress, screen.querySelector("[data-copy-status]"));
}
