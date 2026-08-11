const KEY = "english-course:first-ten:progress:v1";

function empty() {
  return { opened: [], practiced: [], reviewedUnits: [], feedback: {} };
}

export function readProgress() {
  try {
    const value = JSON.parse(localStorage.getItem(KEY));
    if (!value || !Array.isArray(value.opened) || !Array.isArray(value.practiced)) return empty();
    const result = { ...empty(), ...value };
    if (!result.feedback || typeof result.feedback !== "object") result.feedback = {};
    return result;
  } catch {
    return empty();
  }
}

function update(field, id) {
  const progress = readProgress();
  progress[field] = [...new Set([...progress[field], id])];
  localStorage.setItem(KEY, JSON.stringify(progress));
  return progress;
}

export const markOpened = lessonId => update("opened", lessonId);
export const markPracticed = lessonId => update("practiced", lessonId);
export const markUnitReview = unitId => update("reviewedUnits", unitId);
export function saveFeedback(lessonId, feedback) {
  const progress = readProgress();
  progress.feedback = { ...progress.feedback, [lessonId]: feedback };
  localStorage.setItem(KEY, JSON.stringify(progress));
  return progress;
}
export function resetProgress() { localStorage.removeItem(KEY); }
