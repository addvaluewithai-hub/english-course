import { escapeHtml } from "./dom.js";

function options(values, group) {
  return `<div class="choice-row">${values.map((value, index) =>
    `<button class="choice" type="button" data-choice-group="${group}" data-choice="${index}">${escapeHtml(value)}</button>`
  ).join("")}</div>`;
}

function objectItems(activity) {
  if (!Array.isArray(activity.items)) return "";
  if (activity.items.every(item => typeof item === "string")) {
    return `<div class="chip-grid">${activity.items.map(item => `<span class="chip">${escapeHtml(item)}</span>`).join("")}</div>`;
  }
  return activity.items.map((item, index) => {
    const prompt = item.prompt || item.meaning_ar || item.meaning || `جزء ${index + 1}`;
    return `<div class="info-card"><strong>${escapeHtml(prompt)}</strong>${
      Array.isArray(item.options) ? options(item.options, `${activity.id}-${index}`) : ""
    }</div>`;
  }).join("");
}

export function renderActivities(activities) {
  return activities.map((activity, index) => {
    const prompt = activity.prompt_ar || activity.prompt_en || "نفّذ المهمة بالمعلومات الجديدة.";
    const topOptions = Array.isArray(activity.options) ? options(activity.options, activity.id) : "";
    return `<article class="activity-card">
      <small>تطبيق ${index + 1} · ${escapeHtml(activity.type)}</small>
      <h4>${escapeHtml(prompt)}</h4>
      ${topOptions}${objectItems(activity)}
      <label class="privacy-inline">مساحة تجريبية — لا تُحفظ
        <textarea aria-label="إجابة تجريبية للنشاط ${index + 1}" placeholder="اكتب أو خطط هنا بمعلومات خيالية…"></textarea>
      </label>
    </article>`;
  }).join("");
}

export function bindActivities(host) {
  host.querySelectorAll("[data-choice-group]").forEach(button => {
    button.addEventListener("click", () => {
      const group = button.dataset.choiceGroup;
      host.querySelectorAll(`[data-choice-group="${CSS.escape(group)}"]`).forEach(item => item.classList.remove("selected"));
      button.classList.add("selected");
    });
  });
}
