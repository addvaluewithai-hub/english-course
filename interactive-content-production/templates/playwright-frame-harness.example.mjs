/**
 * PORTABLE TEMPLATE, NOT CONFIGURED IN english-course.
 * Copy this file into the PRODUCT repo where Playwright is installed, and
 * implement a real read-only deterministic lesson QA route exposing:
 *   [data-qa-ready="true"] [data-lesson-id] [data-scene-id]
 *   [data-beat-id] [data-lesson-state] [data-lesson-board]
 *
 * Usage in product repo (after running a local fixture server):
 *   BASE_URL=http://127.0.0.1:5173 node scripts/lesson-frame-sheets.mjs qa/cases.json
 * Example cases.json (also needs canonicalBeats, quizScenes,
 * requiresFinalSpeaking — see fixture-cases.example.json):
 *   {"cases":[
 *     {"id":"S01-teach","scene":"S01","beat":"reaction","state":"teaching",
 *      "path":"/qa/lessons/b1-u1-l02?scene=S01&beat=reaction&state=teaching"},
 *     {"id":"S01-wrong","scene":"S01","beat":"question","state":"wrong-feedback",
 *      "path":"/qa/lessons/b1-u1-l02?scene=S01&beat=question&state=wrong-feedback"}
 *   ]}
 * The fixture path and selectors above are a CONTRACT TO IMPLEMENT, not an
 * assertion that EnglishLive already supports them.
 */
import assert from 'node:assert/strict';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { chromium } from 'playwright';

const matrix = {
  'phone-compact': {width:320,height:640},
  'phone': {width:400,height:860},
  'desktop': {width:1280,height:900},
};
const base = process.env.BASE_URL;
const file = process.argv[2];
const out = resolve(process.env.FRAME_OUTPUT || 'test-results/lesson-frames');
if (!base || !file) throw Error('Set BASE_URL and pass a cases.json manifest.');
const manifest = JSON.parse(await readFile(file, 'utf8'));
assert.ok(Array.isArray(manifest.cases) && manifest.cases.length,
  'Need at least one explicit fixture state.');
// The fixture must declare the canonical inventory derived from the lesson
// package, not merely the screenshots an agent happened to choose to take.
assert.ok(Array.isArray(manifest.canonicalBeats) && manifest.canonicalBeats.length,
  'Missing canonical beat inventory.');
assert.ok(Array.isArray(manifest.quizScenes), 'Missing quiz-scene inventory.');
assert.equal(manifest.requiresFinalSpeaking, true,
  'The current EnglishLive teaching contract requires final Speaking.');
for(const item of manifest.canonicalBeats) {
  const match = manifest.cases.some(c=>c.scene===item.scene && c.beat===item.beat);
  assert.ok(match, 'Missing screenshot fixture for authored beat '+item.scene+'/'+item.beat);
}
for(const scene of manifest.quizScenes) {
  for(const state of ['question','correct-feedback','wrong-feedback'])
    assert.ok(manifest.cases.some(c=>c.scene===scene && c.state===state),
      'Missing '+state+' screenshot fixture in '+scene);
}
for(const state of ['speaking-listening','speaking-otti','complete'])
  assert.ok(manifest.cases.some(c=>c.state===state), 'Missing '+state+' fixture');
const ids = new Set();
for(const test of manifest.cases) {
  for(const prop of ['id','scene','beat','state','path'])
    assert.equal(typeof test[prop], 'string', 'Missing ' + prop);
  assert.ok(!ids.has(test.id), 'Duplicate fixture ID: ' + test.id);
  ids.add(test.id);
  assert.ok(test.path.startsWith('/') && !test.path.startsWith('//'), 'Local fixture URL only');
}
await mkdir(out, {recursive:true});
const browser = await chromium.launch();
const findings = [];
const tiles = new Map();
const escape = s => String(s).replace(/[&<>"']/g, c => (
  {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const safe = s => s.replace(/[^a-z0-9_-]/gi,'_');
try {
  for (const [viewport, size] of Object.entries(matrix)) {
    const context = await browser.newContext({
      viewport: size, reducedMotion: 'reduce', serviceWorkers:'block'
    });
    const page = await context.newPage();
    const pageErrors = [];
    page.on('pageerror', e => pageErrors.push('JS: '+e.message));
    page.on('response', r => {
      if(r.status() >= 400 && !r.url().endsWith('/favicon.ico'))
        pageErrors.push(r.status()+' '+r.url());
    });
    for(const test of manifest.cases) {
      const issues = [];
      pageErrors.length = 0;
      await page.goto(new URL(test.path, base).href, {waitUntil:'networkidle'});
      await page.locator('[data-qa-ready="true"]').waitFor({timeout:15000});
      await page.evaluate(() => document.fonts.ready);
      const root = page.locator('[data-lesson-board]');
      if(await root.count() === 0 && test.state !== 'speaking-listening'
        && test.state !== 'speaking-otti' && test.state !== 'complete')
        issues.push('Missing lesson board');
      const actual = await page.evaluate(() => {
        const host = document.querySelector('[data-qa-ready="true"]');
        const board = document.querySelector('[data-lesson-board]');
        const rect = board?.getBoundingClientRect();
        const outside = rect ? [...board.querySelectorAll('*')]
          .filter(n => !n.children.length && n.textContent?.trim() &&
            getComputedStyle(n).visibility !== 'hidden' &&
            getComputedStyle(n).display !== 'none')
          .filter(n => {
            const b = n.getBoundingClientRect();
            return b.width && b.height &&
              (b.left < rect.left-2 || b.right > rect.right+2 ||
               b.top < rect.top-2 || b.bottom > rect.bottom+2);
          }).slice(0,4).map(n => n.textContent?.trim().slice(0,30)) : [];
        return {
          lesson:host?.getAttribute('data-lesson-id'),
          scene:host?.getAttribute('data-scene-id'),
          beat:host?.getAttribute('data-beat-id'),
          state:host?.getAttribute('data-lesson-state'),
          sideways:document.documentElement.scrollWidth > innerWidth+1,
          boardScroll:Boolean(board && board.scrollHeight>board.clientHeight+2),
          textOutside:outside
        };
      });
      if(actual.scene !== test.scene || actual.beat !== test.beat ||
        actual.state !== test.state) issues.push('Fixture state mismatch');
      if(actual.sideways) issues.push('Horizontal page overflow');
      if(actual.boardScroll) issues.push('Board internally scrolls');
      if(actual.textOutside.length) issues.push('Text outside board: '+actual.textOutside.join(', '));
      issues.push(...pageErrors);
      const png = join(out, safe(test.id)+'-'+viewport+'.png');
      await page.screenshot({path:png,fullPage:true});
      findings.push({id:test.id,viewport,file:png,actual,issues});
      const key = test.scene+'-'+viewport;
      tiles.set(key, [...(tiles.get(key)||[]),
        {label:test.id+' · '+test.beat+' · '+test.state, png, issues}]);
    }
    await context.close();
  }
  // Contact sheet per scene/view; same frames and labels, not visual certification.
  for(const [key, items] of tiles) {
    const parts = await Promise.all(items.map(async item => {
      const png = (await readFile(item.png)).toString('base64');
      return '<figure><img src="data:image/png;base64,'+png+'"><figcaption>'+
        escape(item.label)+(item.issues.length?'<p>'+escape(item.issues.join('; '))+'</p>':'')+
        '</figcaption></figure>';
    }));
    const page = await browser.newPage({
      viewport:{width:1100,height:850},reducedMotion:'reduce'
    });
    await page.setContent('<!doctype html><meta charset="utf-8"><style>'+
      'body{background:#edf3ef;font:14px system-ui;color:#234;padding:16px}'+
      'main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px}'+
      'figure{margin:0;background:white;padding:8px;border-radius:8px}'+
      'img{display:block;width:100%}figcaption{overflow-wrap:anywhere}p{color:#b33}'+
      '</style><h2>'+escape(key)+'</h2><main>'+parts.join('')+'</main>');
    await page.screenshot({path:join(out,safe(key)+'-CONTACT.png'),fullPage:true});
    await page.close();
  }
  await writeFile(join(out,'REPORT.json'), JSON.stringify(findings,null,2)+'\n');
  const lines = ['# Frame report','','WARNING: automatic hints only. Open every contact sheet.','',
    ...findings.map(row=>'- '+row.id+' / '+row.viewport+' → '+
      (row.issues.length?row.issues.join('; '):'no automatic warning')),''];
  await writeFile(join(out,'REPORT.md'),lines.join('\n'));
  // Missing states, real app errors, and overflow are technical failures.
  if(findings.some(r=>r.issues.length)) process.exitCode = 1;
} finally { await browser.close(); }
