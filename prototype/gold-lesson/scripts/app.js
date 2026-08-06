const host = document.querySelector("#stepHost");
const nextButton = document.querySelector("#nextButton");
const backButton = document.querySelector("#backButton");
const variant = new URLSearchParams(location.search).get("variant") || "teachback";
let step = 0;
let plan = {};

function render() {
  const views = lessonViews({ plan, variant });
  host.innerHTML = views[step]();
  const percent = ((step + 1) / views.length) * 100;
  document.querySelector("#progressBar").style.width = `${percent}%`;
  document.querySelector("#progressText").textContent = `الخطوة ${step + 1} من ${views.length}`;
  document.querySelector("#stepList").innerHTML = lessonData.steps.map((item, index) => `<li class="${index === step ? "active" : ""} ${index < step ? "done" : ""}">${item.title}</li>`).join("");
  backButton.disabled = step === 0 || step === 6;
  nextButton.textContent = step === views.length - 1 ? "ابدأ من جديد" : "التالي";
  bindStep();
}

function bindStep() {
  host.querySelectorAll("[data-speech]").forEach(button => button.onclick = () => speak(button.dataset.speech));
  host.querySelectorAll(".quiz, .order-choice").forEach(button => button.onclick = () => checkChoice(button));
  host.querySelectorAll("[data-field]").forEach(input => input.oninput = updatePlan);
  document.querySelector("#coachCheck")?.addEventListener("click", checkCoach);
  document.querySelector("#masteryCheck")?.addEventListener("click", checkMastery);
  if (step === 4) updatePlan();
}

function checkChoice(button) {
  button.parentElement.querySelectorAll(".choice").forEach(item => item.classList.remove("correct", "wrong"));
  const correct = button.dataset.correct === "true";
  button.classList.add(correct ? "correct" : "wrong");
  const feedback = button.parentElement.nextElementSibling;
  feedback.className = `feedback show ${correct ? "good" : "try"}`;
  feedback.textContent = correct ? "صحيح — المعنى والترتيب واضحان." : "حاول مرة أخرى. ابدأ بالاسم، وتذكّر: from للأصل.";
}

function updatePlan() {
  host.querySelectorAll("[data-field]").forEach(input => plan[input.dataset.field] = input.value.trim());
  const lines = [`Hi, I'm ${plan.name || "…"}.`, `I'm from ${plan.origin || "…"}.`, plan.role ? (/city|cairo|giza|alex|jeddah|riyadh/i.test(plan.role) ? `I live in ${plan.role}.` : `I'm a ${plan.role}.`) : "I live in ….", `I like ${plan.detail || "…"}.`];
  document.querySelector("#planPreview").textContent = lines.join(" ");
}

function checkCoach() {
  const text = document.querySelector("#coachAnswer").value;
  showFeedback("coachFeedback", feedbackFor(text), isCompleteAttempt(text));
}

function checkMastery() {
  const text = document.querySelector("#masteryAnswer").value;
  const ok = isCompleteAttempt(text);
  showFeedback("masteryFeedback", ok ? "عناصر المهمة موجودة. في الاختبار الحقيقي سنقيّم الوضوح والإصلاح بصوت جديد." : feedbackFor(text), ok);
}

function showFeedback(id, text, good) {
  const box = document.querySelector(`#${id}`);
  box.className = `feedback show ${good ? "good" : "try"}`;
  box.textContent = text;
}

function speak(text) {
  speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US"; utterance.rate = .82;
  speechSynthesis.speak(utterance);
}

nextButton.onclick = () => {
  step = step === lessonData.steps.length - 1 ? 0 : step + 1;
  render();
};
backButton.onclick = () => { if (step > 0 && step !== 6) step -= 1; render(); };
document.querySelector("#privacyButton").onclick = () => document.querySelector("#privacyDialog").showModal();
document.querySelector("#closePrivacy").onclick = () => document.querySelector("#privacyDialog").close();
render();
