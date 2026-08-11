export const STUDY_ID = "a1_first_10_progression_pilot_v1";
export const RELEASE_ID = "a1_first_10_lessons_pilot_v1";
export const LESSON_IDS = [
  "U1-L01", "U1-L02", "U1-L03", "U1-L04", "U1-L05",
  "U1-L06", "U1-L07", "U1-L08", "U1-L09", "U2-L01"
];
export const VISIT_PLAN = {
  1: ["U1-L01", "U1-L02"],
  2: ["U1-L03", "U1-L04"],
  3: ["U1-L05", "U1-L06"],
  4: ["U1-L07"],
  5: ["U1-L08", "U1-L09"],
  6: ["U2-L01"]
};
export const STATIONS = ["UNIT1-STATION-01", "UNIT1-STATION-02", "UNIT1-STATION-03"];
export const DECISIONS = ["not_rated", "demonstrated", "practiced", "needs_review"];
export const ISSUES = [
  "none", "instruction_confusion", "arabic_clarity", "level_fit", "video_value",
  "navigation", "fatigue", "mastery_construct", "accessibility", "privacy", "safety"
];

export function optionList(values, selected = "") {
  return values.map(value => `<option${value === selected ? " selected" : ""}>${value}</option>`).join("");
}
