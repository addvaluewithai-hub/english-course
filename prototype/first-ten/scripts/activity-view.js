import { escapeHtml } from "./dom.js";
import { friendlyLabel, GUIDED_ACTIVITIES } from "./learner-support.js";

const encoded = value => encodeURIComponent(JSON.stringify(value));

function choiceButtons(values, group, answer) {
  return `<div class="choice-row">${values.map((value, index) =>
    `<button class="choice" type="button" data-choice-group="${group}" data-guide-text="${escapeHtml(value)}" data-correct="${Array.isArray(answer) ? answer.includes(index) : index === answer}">${escapeHtml(value)}</button>`
  ).join("")}</div>`;
}

function choiceSet(activity) {
  if (!activity.items?.every(item => Array.isArray(item.options))) return "";
  return activity.items.map((item, index) => `<div class="question-block">
    <strong>${escapeHtml(item.prompt || item.meaning_ar || `سؤال ${index + 1}`)}</strong>
    ${choiceButtons(item.options, `${activity.id}-${index}`, item.answer)}
  </div>`).join("");
}

function multiSelect(activity) {
  return `<div class="choice-row" data-multi-answer="${encoded(activity.answer)}">${activity.options.map(value =>
    `<button class="choice" type="button" data-multi-value="${escapeHtml(value)}">${escapeHtml(value)}</button>`
  ).join("")}</div>`;
}

function orderSlots(count) {
  const labels = ["الأول", "الثاني", "الثالث", "الرابع", "الخامس", "السادس"];
  return labels.slice(0, count).map((label, index) =>
    `<div class="order-slot" data-order-slot><span>${index + 1}</span><em>${label}</em></div>`).join("");
}

function order(activity) {
  return `<div class="order-task" data-order-answer="${encoded(activity.answer)}" data-order-count="${activity.items.length}">
    <div class="order-bank">${activity.items.map(value =>
      `<button class="choice order-card" type="button" data-order-value="${escapeHtml(value)}"><b>${escapeHtml(friendlyLabel(value))}</b><small>${escapeHtml(value)}</small></button>`
    ).join("")}</div>
    <div class="order-result">${orderSlots(activity.items.length)}</div>
    <button class="text-button" type="button" data-order-reset>ابدأ الترتيب من جديد</button>
  </div>`;
}

function match(activity) {
  const right = activity.pairs.map(pair => pair[1]).reverse();
  return `<div class="match-task">${activity.pairs.map(([left, answer]) => `<label>
    <span class="english">${escapeHtml(left)}</span>
    <select data-match data-correct="${escapeHtml(answer)}"><option value="">اختر…</option>${right.map(value =>
      `<option>${escapeHtml(value)}</option>`).join("")}</select>
  </label>`).join("")}</div>`;
}

function supportItems(activity) {
  const values = activity.fields || activity.support || activity.targets || activity.classes ||
    activity.first_pass_fields || activity.minimum_detail_categories;
  if (!Array.isArray(values)) return "";
  return `<div class="chip-grid">${values.map(value => `<span class="chip">${escapeHtml(friendlyLabel(value))}</span>`).join("")}</div>`;
}

function guidedBuilder(activity, guide) {
  return `<div class="guided-builder" data-guided-builder>
    <p>${escapeHtml(guide.intro)}</p>
    ${guide.rows.map((row, index) => `<div class="guide-row"><strong>${escapeHtml(row.prompt)}</strong>${choiceButtons(row.options, `${activity.id}-guide-${index}`, row.answers)}</div>`).join("")}
    <div class="conversation-preview" data-guide-preview>اختياراتك هتظهر هنا كمحادثة قصيرة.</div>
  </div>`;
}

function freeResponse(activity) {
  const extras = supportItems(activity);
  const contrasts = activity.contrasts?.flat() || activity.items?.filter(item => typeof item !== "object");
  const hints = contrasts?.length ? `<div class="chip-grid">${contrasts.map(value =>
    `<span class="chip">${escapeHtml(String(value))}</span>`).join("")}</div>` : "";
  const answer = activity.answer ? ` data-free-answer="${encoded(activity.answer)}"` : "";
  const accept = activity.accept ? ` data-free-accept="${encoded(activity.accept)}"` : "";
  const audio = /(listening|dictation|capture)/.test(activity.type)
    ? `<button class="audio-placeholder" type="button" data-audio-placeholder>🔊 شغّل المقطع الصوتي</button>` : "";
  return `${audio}${extras}${hints}<textarea data-free-response${answer}${accept} placeholder="اكتب هنا، أو نفّذ المهمة بصوتك…"></textarea>
    <label class="oral-check"><input type="checkbox" data-oral-complete> نفّذت المهمة بصوتي</label>`;
}

function body(activity) {
  if (GUIDED_ACTIVITIES[activity.id]) return guidedBuilder(activity, GUIDED_ACTIVITIES[activity.id]);
  if (activity.type === "multi_select" && activity.options && activity.answer) return multiSelect(activity);
  if (activity.type === "order" && activity.answer) return order(activity);
  if (activity.type === "match" && activity.pairs) return match(activity);
  if (activity.options && Number.isInteger(activity.answer)) return choiceButtons(activity.options, activity.id, activity.answer);
  const set = choiceSet(activity);
  return set || freeResponse(activity);
}

export function renderActivity(activity, index, total) {
  const prompt = activity.prompt_ar || activity.prompt_en || "نفّذ المهمة بالمعلومات الجديدة.";
  return `<article class="activity-focus" data-activity-root>
    <p class="step-kicker">تطبيق ${index + 1} من ${total}</p>
    <h3>${escapeHtml(prompt)}</h3>
    ${body(activity)}
    <div class="activity-feedback" data-activity-feedback role="status"></div>
    <button class="button primary" type="button" data-check-activity>تحقق وكمل</button>
  </article>`;
}

function bindChoices(host) {
  host.querySelectorAll("[data-choice-group]").forEach(button => button.onclick = () => {
    host.querySelectorAll(`[data-choice-group="${CSS.escape(button.dataset.choiceGroup)}"]`)
      .forEach(item => item.classList.remove("selected"));
    button.classList.add("selected");
    const preview = host.querySelector("[data-guide-preview]");
    if (preview) {
      const lines = [...host.querySelectorAll("[data-guided-builder] .choice.selected")].map(item => item.dataset.guideText);
      preview.innerHTML = lines.length ? lines.map(line => `<span>${escapeHtml(line)}</span>`).join("") : "اختياراتك هتظهر هنا كمحادثة قصيرة.";
    }
  });
  host.querySelectorAll("[data-multi-value]").forEach(button => button.onclick = () => button.classList.toggle("selected"));
}

function bindOrder(host) {
  const task = host.querySelector("[data-order-answer]");
  if (!task) return;
  const result = task.querySelector(".order-result");
  task.querySelectorAll("[data-order-value]").forEach(button => button.onclick = () => {
    if (button.disabled) return;
    const slot = result.querySelector("[data-order-slot]:not(.filled)");
    if (!slot) return;
    button.disabled = true;
    slot.classList.add("filled");
    slot.dataset.picked = button.dataset.orderValue;
    slot.insertAdjacentHTML("beforeend", `<b>${escapeHtml(friendlyLabel(button.dataset.orderValue))}</b>`);
  });
  task.querySelector("[data-order-reset]").onclick = () => {
    result.innerHTML = orderSlots(Number(task.dataset.orderCount));
    task.querySelectorAll("[data-order-value]").forEach(button => { button.disabled = false; });
  };
}

function result(host) {
  const groups = [...new Set([...host.querySelectorAll("[data-choice-group]")].map(item => item.dataset.choiceGroup))];
  if (groups.length) return groups.every(group => host.querySelector(`[data-choice-group="${CSS.escape(group)}"].selected`)?.dataset.correct === "true");
  const multi = host.querySelector("[data-multi-answer]");
  if (multi) {
    const expected = JSON.parse(decodeURIComponent(multi.dataset.multiAnswer)).sort();
    const actual = [...multi.querySelectorAll(".selected")].map(item => item.dataset.multiValue).sort();
    return JSON.stringify(expected) === JSON.stringify(actual);
  }
  const orderTask = host.querySelector("[data-order-answer]");
  if (orderTask) {
    const expected = JSON.parse(decodeURIComponent(orderTask.dataset.orderAnswer));
    const actual = [...orderTask.querySelectorAll("[data-order-slot][data-picked]")].map(item => item.dataset.picked);
    return JSON.stringify(expected) === JSON.stringify(actual);
  }
  const matches = [...host.querySelectorAll("[data-match]")];
  if (matches.length) return matches.every(item => item.value && item.value === item.dataset.correct);
  const input = host.querySelector("[data-free-response]");
  if (!input) return false;
  if (input.dataset.freeAnswer) {
    const expected = String(JSON.parse(decodeURIComponent(input.dataset.freeAnswer))).toLowerCase();
    const actual = input.value.trim().toLowerCase();
    const accepts = input.dataset.freeAccept ? JSON.parse(decodeURIComponent(input.dataset.freeAccept)) : [];
    return actual === expected || (accepts.length && accepts.every(value => actual.includes(value.toLowerCase())));
  }
  return input.value.trim().length > 0 || host.querySelector("[data-oral-complete]")?.checked;
}

export function bindActivity(host, onComplete) {
  bindChoices(host);
  bindOrder(host);
  host.querySelector("[data-audio-placeholder]")?.addEventListener("click", event => {
    event.currentTarget.textContent = "🔊 Audio Placeholder — ضع المقطع هنا";
    event.currentTarget.classList.add("played");
  });
  host.querySelector("[data-check-activity]").onclick = () => {
    const feedback = host.querySelector("[data-activity-feedback]");
    if (result(host)) {
      feedback.textContent = "تمام! كمل للخطوة التالية.";
      feedback.className = "activity-feedback correct";
      onComplete();
    } else {
      feedback.textContent = "لسه محتاجة محاولة. راجع اختيارك أو نفّذ المهمة الأول.";
      feedback.className = "activity-feedback retry";
    }
  };
}
