function detailChecks(text) {
  const value = text.toLowerCase().replace(/[’]/g, "'");
  return {
    name: /\b(i'm|i am|my name is)\b/.test(value),
    origin: /\b(i'm|i am) from\b/.test(value),
    residenceOrRole: /\b(i live in|i'm an?|i am an?|i work in|i work as)\b/.test(value),
    personal: /\b(i like|i love|i have|my hobby|my family)\b/.test(value)
  };
}

function feedbackFor(text) {
  const checks = detailChecks(text);
  if (!checks.name) return "ابدأ باسمك: Hi, I'm … ثم حاول مرة أخرى.";
  if (!checks.origin) return "أضف أصلك باستخدام: I'm from …";
  if (!checks.residenceOrRole) return "أضف مكان سكنك أو دورك: I live in … / I'm a …";
  if (!checks.personal) return "أضف اهتمامًا أو تفصيلة أسرية واحدة: I like … / I have …";
  if (text.trim().split(/\s+/).length < 9) return "المعلومات موجودة، لكن صِلها في أربع جمل قصيرة واضحة.";
  return "جميل! المعلومات الأساسية واضحة. جرّب الآن الموقف الجديد بدون النموذج.";
}

function isCompleteAttempt(text) {
  const checks = detailChecks(text);
  return Object.values(checks).every(Boolean) && text.trim().split(/\s+/).length >= 9;
}

function escapeHtml(text) {
  return text.replace(/[&<>"]/g, char => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[char]);
}
