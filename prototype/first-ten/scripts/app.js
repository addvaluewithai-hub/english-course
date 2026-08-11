import { loadLesson, loadRelease, loadScope } from "./api.js";
import { renderCatalog } from "./catalog-view.js";
import { escapeHtml } from "./dom.js";
import { renderLesson } from "./lesson-view.js";
import { markOpened, markPracticed, markUnitReview, readProgress, resetProgress, saveFeedback } from "./state.js";
import { UNIT_LABELS } from "./config.js";
import { renderUnitReview } from "./unit-review.js";


const screen = document.querySelector("#screen");
const rail = document.querySelector("#lessonRail");
const cache = new Map();
let release;
let scope;
let progress = readProgress();

function route() {
  const params = new URLSearchParams(location.search);
  return {
    lesson: params.get("lesson"),
    step: Number(params.get("step") || 0),
    review: params.get("review"),
  };
}

function navigate(next, replace = false) {
  const url = new URL(location.href);
  url.search = "";
  Object.entries(next).forEach(([key, value]) => value && url.searchParams.set(key, value));
  history[replace ? "replaceState" : "pushState"]({}, "", url);
  renderRoute();
}

function updateRail(activeLesson) {
  let currentUnit = "";
  const html = [];
  for (const lesson of release.lessons) {
    if (lesson.unit_id !== currentUnit) {
      currentUnit = lesson.unit_id;
      html.push(`<p class="rail-unit">${escapeHtml(UNIT_LABELS[currentUnit] || currentUnit)}</p>`);
    }
    const practiced = progress.practiced.includes(lesson.lesson_id);
    html.push(`<button class="rail-link ${activeLesson === lesson.lesson_id ? "active" : ""} ${practiced ? "practiced" : ""}" type="button" data-rail-lesson="${lesson.lesson_id}"><b>${escapeHtml(lesson.lesson_id)} · ${escapeHtml(lesson.title.ar)}</b><small>${escapeHtml(lesson.title.en)}</small></button>`);
  }
  rail.innerHTML = html.join("");
  rail.querySelectorAll("[data-rail-lesson]").forEach(button => button.addEventListener("click", () => navigate({ lesson: button.dataset.railLesson })));
  const count = release.lessons.filter(lesson => progress.practiced.includes(lesson.lesson_id)).length;
  document.querySelector("#courseProgress").style.width = `${(count / 10) * 100}%`;
  document.querySelector("#courseProgressText").textContent = `${count} من 10 مكتملين`;
}

async function getLesson(contract) {
  if (!cache.has(contract.lesson_id)) cache.set(contract.lesson_id, loadLesson(contract));
  return cache.get(contract.lesson_id);
}

function adjacentCallbacks(index, lessonId) {
  return {
    previous: () => {
      if (index === 0) navigate({});
      else navigate({ lesson: release.lessons[index - 1].lesson_id });
    },
    next: () => {
      if (lessonId === "U1-L09") navigate({ review: "unit1" });
      else if (index < release.lessons.length - 1) navigate({ lesson: release.lessons[index + 1].lesson_id });
      else navigate({});
    },
  };
}

async function renderRoute() {
  const current = route();
  progress = readProgress();
  updateRail(current.lesson);
  if (current.review === "unit1") {
    scope ||= await loadScope();
    renderUnitReview(screen, scope, progress, {
      home: () => navigate({}),
      next: () => navigate({ lesson: "U2-L01" }),
      attempted: () => { progress = markUnitReview("a1.unit01.first_connections"); updateRail(); },
    });
    return;
  }
  if (!current.lesson) {
    renderCatalog(screen, release, progress, navigate);
    return;
  }
  const index = release.lessons.findIndex(row => row.lesson_id === current.lesson);
  if (index < 0) {
    navigate({}, true);
    return;
  }
  const contract = release.lessons[index];
  progress = markOpened(contract.lesson_id);
  updateRail(contract.lesson_id);
  screen.innerHTML = `<div class="loading">جارٍ تحميل ${escapeHtml(contract.title.ar)}…</div>`;
  const pkg = await getLesson(contract);
  const adjacent = adjacentCallbacks(index, contract.lesson_id);
  renderLesson(screen, pkg, current.step, {
    ...adjacent,
    step: step => navigate({ lesson: contract.lesson_id, step }),
    practiced: () => { progress = markPracticed(contract.lesson_id); updateRail(contract.lesson_id); },
    savedFeedback: progress.feedback[contract.lesson_id] || {},
    saveFeedback: feedback => { progress = saveFeedback(contract.lesson_id, feedback); updateRail(contract.lesson_id); },
  });
}

async function start() {
  try {
    release = await loadRelease();
    await renderRoute();
  } catch (error) {
    screen.innerHTML = `<section class="panel"><h2>تعذّر فتح التجربة</h2><p>${escapeHtml(error.message)}</p><p>شغّل الخادم من جذر الريبو، وليس من مجلد النموذج فقط.</p></section>`;
  }
}

document.querySelector("#homeButton").addEventListener("click", () => navigate({}));
const privacy = document.querySelector("#privacyDialog");
const reset = document.querySelector("#resetDialog");
document.querySelector("#privacyButton").addEventListener("click", () => privacy.showModal());
document.querySelector("#closePrivacy").addEventListener("click", () => privacy.close());
document.querySelector("#resetButton").addEventListener("click", () => reset.showModal());
document.querySelector("#cancelReset").addEventListener("click", () => reset.close());
document.querySelector("#confirmReset").addEventListener("click", () => { resetProgress(); reset.close(); navigate({}, true); });
window.addEventListener("popstate", renderRoute);
start();
