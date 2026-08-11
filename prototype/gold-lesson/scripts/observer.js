const byId = id => document.querySelector(`#${id}`);
const checked = id => byId(id).checked;
const numberOrNull = id => byId(id).value === "" ? null : Number(byId(id).value);

function sectionTiming() {
  const values = byId("sectionSeconds").value.split(",").map(value => Number(value.trim()));
  if (values.some(value => !Number.isInteger(value) || value < 0)) {
    throw new Error("توقيت كل خطوة يجب أن يكون رقمًا صحيحًا موجبًا أو صفرًا.");
  }
  return values.map((seconds, index) => ({ step: index + 1, seconds }));
}

function selectedSupports() {
  const values = [...document.querySelectorAll("#supports input:checked")].map(item => item.value);
  if (!values.length) throw new Error("اختر نوع دعم واحدًا على الأقل، حتى لو كان none.");
  if (values.includes("none") && values.length > 1) throw new Error("لا تجمع none مع نوع دعم آخر.");
  return values;
}

function optionalIssue() {
  if (!byId("issueType").value) return [];
  return [{
    type: byId("issueType").value,
    severity: byId("issueSeverity").value,
    resolved: checked("issueResolved"),
    note: byId("issueNote").value.trim()
  }];
}

function buildRecord() {
  if (!byId("observerForm").reportValidity()) throw new Error("أكمل الحقول المطلوبة أولًا.");
  if (!["adult", "arabic", "voluntary", "dataBoundary", "agreed"].every(checked)) {
    throw new Error("لا تنشئ سجل جلسة من دون تأكيد الأهلية والموافقة كاملة.");
  }
  const sessionId = byId("sessionId").value.trim();
  if (!/^LT1-[0-9]{3}$/.test(sessionId)) throw new Error("رقم الجلسة يجب أن يكون مثل LT1-001.");
  const expectedCondition = Number(sessionId.slice(-3)) % 2 ? "teachback" : "omit";
  if (byId("postPerformance").value !== expectedCondition) {
    throw new Error("الجلسات الفردية teachback والجلسات الزوجية omit حسب البروتوكول.");
  }
  const ratings = {
    comprehension: numberOrNull("comprehension"),
    outcome_performance: numberOrNull("outcomePerformance"),
    context_transfer: numberOrNull("contextTransfer"),
    control_or_repair: numberOrNull("controlRepair")
  };
  const secondaryRatings = {
    comprehension: numberOrNull("secondaryComprehension"),
    outcome_performance: numberOrNull("secondaryOutcome"),
    context_transfer: numberOrNull("secondaryTransfer"),
    control_or_repair: numberOrNull("secondaryControl")
  };
  const doubleRated = checked("doubleRated");
  const secondaryDecision = byId("secondaryDecision").value || null;
  if (doubleRated && (!secondaryDecision || Object.values(secondaryRatings).some(value => value === null))) {
    throw new Error("الجلسة المزدوجة تحتاج درجات وقرار المقيم الثاني كاملة.");
  }
  if (!doubleRated && (secondaryDecision || Object.values(secondaryRatings).some(value => value !== null))) {
    throw new Error("امسح تقييم المقيم الثاني أو فعّل خيار الجلسة المزدوجة.");
  }
  if (byId("masteryDecision").value === "demonstrated") {
    if (!checked("evidenceValid") || checked("fullModelVisible") || Object.values(ratings).some(value => value !== 2)) {
      throw new Error("demonstrated يحتاج دليلًا صالحًا، نموذجًا مخفيًا، ودرجة 2 في الأبعاد الأربعة.");
    }
  }
  return {
    schema_version: 1,
    study_id: "gold_lesson_u1_l03_pilot_v1",
    session_id: sessionId,
    lesson_id: "U1-L03",
    condition: {
      post_performance: byId("postPerformance").value,
      medium: byId("medium").value,
      task_variant: byId("taskVariant").value
    },
    participant: {
      adult_confirmed: checked("adult"),
      arabic_speaking: checked("arabic"),
      entry_band: byId("entryBand").value,
      eligible_primary_sample: checked("eligible")
    },
    consent: {
      voluntary_confirmed: checked("voluntary"),
      data_boundary_confirmed: checked("dataBoundary"),
      participation_agreed: checked("agreed"),
      raw_capture: false
    },
    completion: {
      outcome: byId("completion").value,
      last_step: Number(byId("lastStep").value),
      fresh_task_attempted: checked("freshAttempt")
    },
    timing: { total_seconds: Number(byId("totalSeconds").value), section_seconds: sectionTiming() },
    supports: selectedSupports(),
    mastery: {
      evidence_valid: checked("evidenceValid"),
      full_model_visible: checked("fullModelVisible"),
      ratings,
      decision: byId("masteryDecision").value
    },
    correction: {
      important_corrections: Number(byId("corrections").value),
      successful_immediate_retries: Number(byId("retries").value)
    },
    reliability: {
      double_rated: doubleRated,
      secondary_ratings: doubleRated ? secondaryRatings : null,
      secondary_decision: doubleRated ? secondaryDecision : null,
      exact_decision_agreement: doubleRated ? secondaryDecision === byId("masteryDecision").value : null
    },
    experience: {
      arabic_clarity: numberOrNull("arabicClarity"),
      difficulty: numberOrNull("difficulty"),
      boredom: numberOrNull("boredom"),
      perceived_value: numberOrNull("perceivedValue"),
      video_helpfulness: numberOrNull("videoHelpfulness"),
      teachback_helpfulness: numberOrNull("teachbackHelpfulness"),
      teachback_fatigue: numberOrNull("teachbackFatigue")
    },
    issues: optionalIssue(),
    data_controls: {
      contains_raw_answer: false,
      contains_direct_identifier: false,
      withdrawal_route_given: checked("withdrawal")
    }
  };
}

function showRecord(record) {
  byId("formError").textContent = "";
  byId("recordPreview").textContent = JSON.stringify(record, null, 2);
  byId("recordPreview").classList.add("show");
}

function handle(action) {
  try { action(buildRecord()); }
  catch (error) { byId("formError").textContent = error.message; }
}

byId("previewRecord").onclick = () => handle(showRecord);
byId("downloadRecord").onclick = () => handle(record => {
  showRecord(record);
  const blob = new Blob([JSON.stringify(record, null, 2)], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = `${record.session_id}.json`;
  link.click();
  URL.revokeObjectURL(link.href);
});
