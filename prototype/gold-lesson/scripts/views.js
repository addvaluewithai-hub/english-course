function panel(kicker, title, body) {
  return `<article class="panel"><p class="kicker">${kicker}</p><h2>${title}</h2>${body}</article>`;
}

function lessonViews(state) {
  return [
    () => panel("VIDEO LESSON", "قدّم نفسك", `
      <p class="lead">شاهد شرح المدرّس كاملًا أولًا. الأسئلة والتطبيق يبدأان بعد الفيديو.</p>
      <div class="video-card">
        <span class="video-icon" aria-hidden="true">▶</span>
        <div><b>فيديو المدرّس الواحد</b><small>سيُضاف الفيديو النهائي بعد اعتماد تجربة الصوت.</small></div>
      </div>
      <a class="button secondary" href="../../gold/introduce-yourself/video/transcript.txt" target="_blank">عرض النص التجريبي</a>
      <p class="mini-note">ستتوفر ترجمة مرئية ومسار نصي مكافئ في النسخة النهائية.</p>`),

    () => panel("QUESTION 1", "ماذا عرفت عن Maya؟", `
      <p class="lead">اختر المجموعة التي تحتوي المعلومات المذكورة في الفيديو.</p>
      <div class="choice-list">
        ${choice("الاسم، البلد، السكن، العمل، والاهتمام", true, "quiz")}
        ${choice("العمر، رقم الهاتف، العنوان، والراتب", false, "quiz")}
        ${choice("الدراسة، السفر، الطقس، والطعام", false, "quiz")}
      </div><div id="quizFeedback" class="feedback"></div>`),

    () => panel("QUESTION 2", "from ليست live in", `
      <p class="lead"><b dir="ltr">I'm from</b> للأصل، و<b dir="ltr">I live in</b> لمكان السكن الآن.</p>
      <p>Lina من سوريا وتعيش الآن في القاهرة. اختر الجملة الصحيحة.</p>
      <div class="choice-list">
        ${choice("<span dir='ltr'>I'm from Syria. I live in Cairo.</span>", true, "quiz")}
        ${choice("<span dir='ltr'>I'm from Cairo. I live in Syria.</span>", false, "quiz")}
      </div><div id="meaningFeedback" class="feedback"></div>`),

    () => panel("APPLIED PRACTICE", "ابنِ مقدمة Omar", `
      <p class="lead">اختر الترتيب الذي يصنع مقدمة قصيرة وطبيعية.</p>
      <div class="choice-list">
        ${choice("<span dir='ltr'>I like reading. / I live in Giza. / Hi, I'm Omar.</span>", false, "order-choice")}
        ${choice("<span dir='ltr'>Hi, I'm Omar. / I'm from Egypt. / I live in Giza. / I like reading.</span>", true, "order-choice")}
      </div><div id="orderFeedback" class="feedback"></div>`),

    () => panel("MAKE IT YOURS", "خطّط بالكلمات فقط", `
      <p class="lead">اكتب كلماتك، وليس فقرة محفوظة.</p>
      <div class="field-grid">
        ${field("name", "الاسم", "Nour", state.plan.name)}
        ${field("origin", "الأصل", "Egypt", state.plan.origin)}
        ${field("role", "السكن أو الدور", "Alexandria / designer", state.plan.role)}
        ${field("detail", "اهتمام أو أسرة", "football / two brothers", state.plan.detail)}
      </div><div id="planPreview" class="preview">ستظهر مقدمتك هنا…</div>`),

    () => panel("COACHED ATTEMPT", "تدرّب ثم أَعِد المحاولة", `
      <div class="coach"><div class="bubble ai english">Hi! Tell me about yourself.</div></div>
      <textarea id="coachAnswer" aria-label="اكتب مقدمتك بالإنجليزية" placeholder="Hi, I'm …"></textarea>
      <button id="coachCheck" class="button primary" type="button">احصل على ملاحظة واحدة</button>
      <div id="coachFeedback" class="feedback"></div>
      <p class="mini-note">التدريب لا يمنح الإتقان؛ يمكنك المحاولة مرة أخرى بعد الملاحظة.</p>`),

    () => panel("FRESH MASTERY", "الآن بدون النموذج", `
      <p class="lead">هذا أول يوم لك في مجموعة دراسة عبر الإنترنت.</p>
      <div class="prompt-card english"><p>Introduce yourself in four or five short sentences.</p></div>
      <p>اذكر: الاسم، الأصل، السكن أو الدور، واهتمام أو تفصيلة أسرية.</p>
      <textarea id="masteryAnswer" aria-label="تحدي الإتقان" placeholder="Write or dictate your fresh answer…"></textarea>
      <button id="masteryCheck" class="button primary" type="button">افحص اكتمال المهمة</button>
      <div id="masteryFeedback" class="feedback"></div>`),

    () => closeView(state.variant)
  ];
}

function closeView(variant) {
  const teachBack = variant !== "omit" ? `
    <h3>شرح قصير</h3>
    <p>اشرح الفرق بين <b dir="ltr">I'm from</b> و<b dir="ltr">I live in</b>، ثم أعط مثالًا.</p>
    <textarea aria-label="شرح الفرق" placeholder="I'm from تعني…"></textarea>` : "";
  return panel("LESSON CLOSE", "أنت صنعت مقدمتك", `
    <p class="celebrate">✓</p><p class="lead">الإنجاز هنا هو أداء جديد، وليس مجرد مشاهدة الفيديو.</p>
    ${teachBack}<h3>بطاقة مراجعتك</h3>
    <p>غدًا: قدّم شخصية جديدة بأربع معلومات. بعد ثلاثة أيام: أصلح خطأ في الأصل والسكن ثم قدّم نفسك.</p>`);
}

function choice(content, correct, className) {
  return `<button class="choice ${className}" data-correct="${correct}" type="button"><span>${content}</span><b aria-hidden="true">○</b></button>`;
}

function field(name, label, placeholder, value = "") {
  return `<label>${label}<input data-field="${name}" value="${escapeHtml(value || "")}" placeholder="${placeholder}"></label>`;
}
