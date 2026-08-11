const LABELS = {
  greeting: "👋 ابدأ بتحية",
  "wellbeing exchange": "🙂 اسأل عن الحال",
  wellbeing_question: "🙂 سؤال عن الحال",
  question: "❓ سؤال بسيط",
  reaction: "💬 رد مناسب",
  fitting_reaction: "💬 رد يناسب الخبر",
  closing: "👋 اختم المحادثة",
  name: "الاسم",
  origin: "البلد الأصلي",
  residence: "مكان السكن",
  job: "العمل",
  repair: "طلب التوضيح",
};

export function friendlyLabel(value) {
  return LABELS[value] || String(value).replaceAll("_", " ");
}

export const GUIDED_ACTIVITIES = {
  guided_exchange: {
    intro: "الشخص قال لك: Hi! اختار أجزاء المحادثة، وهنركبها معاك.",
    rows: [
      { prompt: "1. ابدأ بتحية", options: ["Hi!", "Hello!"], answers: [0, 1] },
      { prompt: "2. اسأل عن حاله", options: ["How are you?", "How's it going?"], answers: [0, 1] },
      { prompt: "3. قال: I'm tired. اختار ردًا مناسبًا", options: ["Oh, I'm sorry.", "That's good!"], answers: [0] },
      { prompt: "4. اختم الكلام", options: ["See you soon.", "Bye!"], answers: [0, 1] },
    ],
  },
};

export const MASTERY_GUIDES = {
  "U1-L01": {
    partner: "سارة قالت بعد سؤالك: I'm great today!",
    rows: [
      { prompt: "1. ابدأ", options: ["Hi!", "Good evening!"], answers: [0, 1] },
      { prompt: "2. اسأل", options: ["How are you?", "How's it going?"], answers: [0, 1] },
      { prompt: "3. رد على الخبر", options: ["That's good!", "I'm sorry."], answers: [0] },
      { prompt: "4. اختم", options: ["See you soon.", "Goodbye!"], answers: [0, 1] },
    ],
  },
};
