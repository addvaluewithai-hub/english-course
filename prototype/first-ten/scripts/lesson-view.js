import { bindActivity, renderActivity } from "./activity-view.js";
import { cleanTranscript, escapeHtml, list } from "./dom.js";

function videoStep(pkg) {
  const player = pkg.videoUrl
    ? `<video class="lesson-video" controls preload="metadata"><source src="${pkg.videoUrl}" type="video/mp4">متصفحك لا يدعم الفيديو.</video>`
    : `<div class="video-placeholder student-video">
        <span class="play-mark">▶</span>
        <b>فيديو ${escapeHtml(pkg.contract.lesson_id)}</b>
        <p>Video Placeholder — اعتبر الفيديو موجودًا وكمل التجربة.</p>
      </div>`;
  return `<div class="flow-step video-step">
    ${player}
    <details><summary>اقرأ Transcript الفيديو بدل المشاهدة</summary><div class="transcript">${escapeHtml(cleanTranscript(pkg.transcript))}</div></details>
    <button class="button primary large-action" type="button" data-video-done>شاهدت الفيديو — ابدأ التطبيق</button>
  </div>`;
}

function masteryStep(pkg) {
  const task = pkg.assessment.mastery_task;
  return `<div class="flow-step challenge-step">
    <p class="step-kicker">التحدي الأخير</p>
    <h3>${escapeHtml(task.scenario_ar)}</h3>
    <p class="english challenge-prompt">${escapeHtml(task.prompt_en)}</p>
    ${list(task.required.map(item => item.replaceAll("_", " ")), "required-list")}
    <p class="privacy-inline">استخدم معلومات خيالية. الإجابة لا تُحفظ.</p>
    <textarea data-mastery-response placeholder="اكتب هنا أو نفّذ المهمة بصوتك…"></textarea>
    <label class="oral-check"><input type="checkbox" data-mastery-oral> نفّذت التحدي بصوتي</label>
    <div class="activity-feedback" data-mastery-feedback role="status"></div>
    <button class="button primary large-action" type="button" data-mastery-done>أنهيت التحدي</button>
  </div>`;
}

const FEEDBACK = {
  clarity: ["واضح", "واضح جزئيًا", "محتاج تبسيط"],
  enjoyment: ["ممتع", "عادي", "ممل"],
  pace: ["قصير", "مناسب", "طويل"],
  confidence: ["أقدر أستخدمه", "محتاج تدريب", "مش فاهمه بعد"],
};

function feedbackStep(pkg, saved = {}) {
  const rows = Object.entries(FEEDBACK).map(([key, values]) => `<div class="feedback-row" data-feedback-group="${key}">
    <strong>${{ clarity: "الشرح", enjoyment: "التجربة", pace: "مدة الدرس", confidence: "بعد الدرس" }[key]}</strong>
    <div class="choice-row">${values.map(value => `<button class="choice ${saved[key] === value ? "selected" : ""}" type="button" data-feedback-value="${escapeHtml(value)}">${escapeHtml(value)}</button>`).join("")}</div>
  </div>`).join("");
  return `<div class="flow-step feedback-step">
    <div class="success-mark">✓</div>
    <h3>خلصت ${escapeHtml(pkg.contract.title.ar)}</h3>
    <p>قول لنا انطباعك السريع. لا يوجد تسجيل دخول ولا بيانات شخصية.</p>
    ${rows}
    <div class="activity-feedback" data-feedback-message role="status"></div>
    <button class="button primary large-action" type="button" data-save-feedback>احفظ الانطباع وانتقل</button>
  </div>`;
}

function stepName(step, activityCount) {
  if (step === 0) return "فيديو الدرس";
  if (step <= activityCount) return `تطبيق ${step} من ${activityCount}`;
  if (step === activityCount + 1) return "التحدي الأخير";
  return "انطباعك";
}

function bindFeedback(screen, callbacks) {
  screen.querySelectorAll("[data-feedback-value]").forEach(button => button.onclick = () => {
    button.closest("[data-feedback-group]").querySelectorAll(".choice").forEach(item => item.classList.remove("selected"));
    button.classList.add("selected");
  });
  screen.querySelector("[data-save-feedback]").onclick = () => {
    const result = {};
    screen.querySelectorAll("[data-feedback-group]").forEach(group => {
      result[group.dataset.feedbackGroup] = group.querySelector(".selected")?.dataset.feedbackValue;
    });
    if (Object.values(result).some(value => !value)) {
      screen.querySelector("[data-feedback-message]").textContent = "اختار إجابة واحدة في كل سطر.";
      screen.querySelector("[data-feedback-message]").className = "activity-feedback retry";
      return;
    }
    callbacks.saveFeedback(result);
    callbacks.next();
  };
}

function bindStep(screen, pkg, step, callbacks) {
  const count = pkg.activities.activities.length;
  screen.querySelector("[data-back]").onclick = () => step > 0 ? callbacks.step(step - 1) : callbacks.previous();
  if (step === 0) {
    screen.querySelector("[data-video-done]").onclick = () => callbacks.step(1);
    return;
  }
  if (step <= count) {
    const next = screen.querySelector("[data-flow-next]");
    bindActivity(screen, () => { next.disabled = false; });
    next.onclick = () => callbacks.step(step + 1);
    return;
  }
  if (step === count + 1) {
    screen.querySelector("[data-mastery-done]").onclick = () => {
      const written = screen.querySelector("[data-mastery-response]").value.trim();
      const oral = screen.querySelector("[data-mastery-oral]").checked;
      if (!written && !oral) {
        screen.querySelector("[data-mastery-feedback]").textContent = "نفّذ التحدي كتابة أو بصوتك الأول.";
        screen.querySelector("[data-mastery-feedback]").className = "activity-feedback retry";
        return;
      }
      callbacks.practiced();
      callbacks.step(step + 1);
    };
    return;
  }
  bindFeedback(screen, callbacks);
}

export function renderLesson(screen, pkg, requestedStep, callbacks) {
  const activities = pkg.activities.activities;
  const lastStep = activities.length + 2;
  const step = Math.max(0, Math.min(Number(requestedStep) || 0, lastStep));
  let body = videoStep(pkg);
  if (step > 0 && step <= activities.length) body = renderActivity(activities[step - 1], step - 1, activities.length);
  if (step === activities.length + 1) body = masteryStep(pkg);
  if (step === lastStep) body = feedbackStep(pkg, callbacks.savedFeedback);
  const nextButton = step > 0 && step <= activities.length
    ? `<button class="button primary" type="button" data-flow-next disabled>الخطوة التالية</button>` : "";
  screen.innerHTML = `<article class="panel lesson-flow">
    <div class="lesson-meta"><span>${escapeHtml(pkg.contract.lesson_id)}</span><span>الدرس ${pkg.contract.global_sequence_position} من 10</span></div>
    <h2>${escapeHtml(pkg.contract.title.ar)}</h2>
    <p class="english lead">${escapeHtml(pkg.contract.title.en)}</p>
    <div class="flow-progress"><span style="width:${((step + 1) / (lastStep + 1)) * 100}%"></span></div>
    <p class="flow-label">${stepName(step, activities.length)}</p>
    ${body}
    <div class="lesson-actions"><button class="button secondary" type="button" data-back>رجوع</button>${nextButton}</div>
  </article>`;
  bindStep(screen, pkg, step, callbacks);
}
