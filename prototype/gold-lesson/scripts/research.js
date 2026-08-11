const lessonResearch = (() => {
  const state = {
    consented: false,
    startedAt: 0,
    currentStep: null,
    stepStartedAt: 0,
    sectionSeconds: {},
    counts: {}
  };
  let variant = "teachback";

  function elapsedSeconds(start) {
    return Math.max(0, Math.round((performance.now() - start) / 1000));
  }

  function closeCurrentStep() {
    if (!state.consented || state.currentStep === null) return;
    const prior = state.sectionSeconds[state.currentStep] || 0;
    state.sectionSeconds[state.currentStep] = prior + elapsedSeconds(state.stepStartedAt);
  }

  function stepChanged(nextStep) {
    if (!state.consented || state.currentStep === nextStep) return;
    closeCurrentStep();
    state.currentStep = nextStep;
    state.stepStartedAt = performance.now();
    state.sectionSeconds[nextStep] = state.sectionSeconds[nextStep] || 0;
  }

  function mark(eventName) {
    if (!state.consented) return;
    state.counts[eventName] = (state.counts[eventName] || 0) + 1;
  }

  function snapshot() {
    const seconds = { ...state.sectionSeconds };
    if (state.consented && state.currentStep !== null) {
      seconds[state.currentStep] = (seconds[state.currentStep] || 0) + elapsedSeconds(state.stepStartedAt);
    }
    return {
      schema_version: 1,
      lesson_id: "U1-L03",
      post_performance_condition: variant,
      total_seconds: state.consented ? elapsedSeconds(state.startedAt) : 0,
      section_seconds: Object.keys(seconds).sort((a, b) => Number(a) - Number(b)).map(step => ({
        step: Number(step), seconds: seconds[step]
      })),
      interaction_counts: { ...state.counts },
      contains_raw_answer: false,
      contains_direct_identifier: false
    };
  }

  function showTiming() {
    document.querySelector("#timingSummary").textContent = JSON.stringify(snapshot(), null, 2);
    document.querySelector("#timingDialog").showModal();
  }

  function downloadTiming() {
    const blob = new Blob([JSON.stringify(snapshot(), null, 2)], { type: "application/json" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "LT1-timing.json";
    link.click();
    URL.revokeObjectURL(link.href);
  }

  function init(options) {
    variant = options.variant;
    const consent = document.querySelector("#consentDialog");
    const check = document.querySelector("#consentCheck");
    const start = document.querySelector("#startLesson");
    check.onchange = () => { start.disabled = !check.checked; };
    start.onclick = () => {
      if (!check.checked) return;
      state.consented = true;
      state.startedAt = performance.now();
      consent.close();
      stepChanged(1);
    };
    document.querySelector("#timingButton").onclick = showTiming;
    document.querySelector("#downloadTiming").onclick = downloadTiming;
    document.querySelector("#closeTiming").onclick = () => document.querySelector("#timingDialog").close();
    consent.showModal();
  }

  return { init, mark, snapshot, stepChanged };
})();
