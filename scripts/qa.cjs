#!/usr/bin/env node
/*
 * Browser QA for the built site in ./dist. Run `python3 build.py` first.
 *
 *   npm install --no-save playwright && npx playwright install chromium   (once)
 *   node scripts/qa.cjs              checks only
 *   node scripts/qa.cjs --shots      checks + screenshots in ./qa-output
 *
 * Checks: horizontal overflow at 7 widths (320-2560px), JS errors, AA text
 * contrast, headline on the first screen, mobile menu, anchors clearing the
 * sticky header, contact form behaviour, redirects from old addresses, no
 * cookies, no leftover research notes in the legal text, and for the Arabic
 * site (/ar/): lang/dir, untranslated text, language switch and the Arabic form.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const DIST = path.resolve(__dirname, '..', 'dist');
const OUT = path.resolve(__dirname, '..', 'qa-output');
const SHOTS = process.argv.includes('--shots');
const TYPES = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.txt': 'text/plain', '.xml': 'application/xml' };

function serve() {
  const server = http.createServer((req, res) => {
    const url = decodeURIComponent(new URL(req.url, 'http://x').pathname);
    let file = path.join(DIST, url.endsWith('/') ? url + 'index.html' : url);
    if (!file.startsWith(DIST) || !fs.existsSync(file)) { res.writeHead(404, { 'content-type': 'text/html' }); return res.end(fs.readFileSync(path.join(DIST, '404.html'))); }
    res.writeHead(200, { 'content-type': TYPES[path.extname(file)] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  });
  return new Promise((ok) => server.listen(0, '127.0.0.1', () => ok(server)));
}

(async () => {
  if (!fs.existsSync(DIST)) { console.error('dist/ not found. Run `python3 build.py` first.'); process.exit(1); }
  const server = await serve();
  const base = `http://127.0.0.1:${server.address().port}/`;
  const redirectStubs = ['home-1', 'blank', 'blank-1', 'blank-2', 'blank-3', 'blank-4', 'blank-5', 'terms-and-coniditions', 'privacy-policy'].map((n) => n + '.html');
  const pages = fs.readdirSync(DIST).filter((f) => f.endsWith('.html') && !redirectStubs.includes(f))
    .concat(fs.readdirSync(path.join(DIST, 'ar')).filter((f) => f.endsWith('.html')).map((f) => 'ar/' + f));
  const browser = await chromium.launch();
  const failures = [];
  const fail = (msg) => failures.push(msg);
  if (SHOTS) fs.mkdirSync(OUT, { recursive: true });

  // 1. Layout + errors + contrast across widths
  for (const width of [320, 375, 768, 1024, 1280, 1440, 2560]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    page.on('pageerror', (err) => fail(`JS error @${width}: ${err.message}`));
    page.on('console', (msg) => { if (msg.type() === 'error') fail(`console error @${width}: ${msg.text()}`); });
    for (const name of pages) {
      await page.goto(base + name);
      const scroll = await page.evaluate(() => document.documentElement.scrollWidth);
      if (scroll > width) fail(`${name} @${width}px: horizontal overflow (${scroll}px)`);
      if (width === 1280) {
        const text = await page.evaluate(() => document.body.innerText);
        for (const note of ['Saudi official website', 'SDAIA states', 'The PDPL is the principal']) if (text.includes(note)) fail(`${name}: leftover research note "${note}"`);
        if (await page.evaluate(() => document.cookie !== '')) fail(`${name}: sets a cookie`);
        if (name.startsWith('ar/')) {
          const [lang, dir] = await page.evaluate(() => [document.documentElement.lang, document.documentElement.dir]);
          if (lang !== 'ar' || dir !== 'rtl') fail(`${name}: expected lang="ar" dir="rtl", got ${lang}/${dir}`);
          // Latin-only text on an Arabic page should be a name, address, number or brand, marked lang="en" or dir="ltr".
          const untranslated = await page.evaluate(() => {
            const out = [];
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            for (let n = walker.nextNode(); n; n = walker.nextNode()) {
              const text = n.textContent.trim();
              const el = n.parentElement;
              if (!text || !/[A-Za-z]{3,}/.test(text) || /[\u0600-\u06FF]/.test(text)) continue;
              if (el.closest('[lang="en"], [dir="ltr"], script, style, .visually-hidden')) continue;
              if (/^(©\s*\d{4}\s*)?Elevate Arabia$/.test(text)) continue;
              out.push(text.slice(0, 40));
            }
            return out;
          });
          untranslated.forEach((x) => fail(`${name}: untranslated text "${x}"`));
        }
      }
      if (width === 375 || width === 1280) {
        const low = await page.evaluate(() => {
          const rgb = (c) => (c.match(/[\d.]+/g) || []).map(Number);
          const lum = ([r, g, b]) => [r, g, b].map((v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; })
            .reduce((s, v, i) => s + v * [0.2126, 0.7152, 0.0722][i], 0);
          const bg = (el) => { for (; el; el = el.parentElement) { const c = rgb(getComputedStyle(el).backgroundColor); if (c.length === 3 || c[3] > 0.5) return c; } return [255, 255, 255]; };
          const bad = [];
          for (const el of document.querySelectorAll('body *')) {
            const text = [...el.childNodes].filter((n) => n.nodeType === 3).map((n) => n.textContent).join('').trim();
            if (!text || !el.getClientRects().length || el.closest('.visually-hidden')) continue;
            const cs = getComputedStyle(el);
            const a = lum(rgb(cs.color)), b = lum(bg(el));
            const ratio = (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
            const size = parseFloat(cs.fontSize), large = size >= 24 || (size >= 18.66 && Number(cs.fontWeight) >= 700);
            if (ratio < (large ? 3 : 4.5)) bad.push(`"${text.slice(0, 30)}" ${ratio.toFixed(2)}:1`);
          }
          return bad;
        });
        low.forEach((b) => fail(`${name} @${width}px: low contrast ${b}`));
      }
    }
    if (SHOTS && (width === 375 || width === 1440)) {
      for (const name of ['index.html', 'services.html', 'advisory.html', 'about.html', 'contact.html', 'ar/index.html', 'ar/about.html', 'ar/contact.html']) {
        await page.goto(base + name);
        await page.screenshot({ path: path.join(OUT, `${name.replace('.html', '').replace('/', '-')}-${width}.png`), fullPage: true });
      }
    }
    await page.close();
  }

  // 2. Headline, intro and main button on the first screen (laptop) / headline (phone)
  for (const [w, h, sel, home] of [[1280, 720, '.hero .button', 'index.html'], [1366, 768, '.hero .button', 'index.html'],
    [375, 667, '.hero h1', 'index.html'], [1280, 720, '.hero .button', 'ar/index.html'], [375, 667, '.hero h1', 'ar/index.html']]) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    await p.goto(base + home);
    await p.evaluate(() => document.fonts.ready);
    const bottom = await p.evaluate((s) => document.querySelector(s).getBoundingClientRect().bottom, sel);
    if (bottom > h) fail(`${home} @${w}x${h}: "${sel}" below the first screen (${Math.round(bottom)}px)`);
    await p.close();
  }

  const page = await browser.newPage({ viewport: { width: 375, height: 800 } });
  // 3. Mobile menu
  await page.goto(base + 'index.html');
  const toggle = page.locator('.nav-toggle');
  if (await page.locator('#site-nav').isVisible()) fail('mobile nav visible before opening');
  await toggle.click();
  if (!(await page.locator('#site-nav').isVisible())) fail('mobile nav did not open');
  if ((await toggle.getAttribute('aria-expanded')) !== 'true') fail('aria-expanded not true when open');
  await page.keyboard.press('Escape');
  if (await page.locator('#site-nav').isVisible()) fail('Escape did not close mobile nav');
  await toggle.click(); await page.locator('#site-nav a[href="about.html"]').click(); await page.waitForURL(/about/);
  if (await page.locator('#site-nav').isVisible()) fail('mobile nav stayed open after navigation');

  // 4. Anchors clear the sticky header
  await page.setViewportSize({ width: 1280, height: 800 });
  for (const target of ['advisory.html#finance', 'about.html#partnership', 'sectors.html#education', 'ar/advisory.html#finance']) {
    await page.goto(base + target); await page.waitForTimeout(400);
    const [top, header] = await page.evaluate((id) => [document.getElementById(id).getBoundingClientRect().top, document.querySelector('.site-header').getBoundingClientRect().bottom], target.split('#')[1]);
    if (top < header) fail(`${target}: target hidden under sticky header (${Math.round(top)} < ${Math.round(header)})`);
  }

  // 5. Contact form
  await page.goto(base + 'contact.html?interest=capital');
  if ((await page.inputValue('#f-interest')) !== 'capital') fail('?interest= did not preselect the service');
  await page.selectOption('#f-interest', '');
  await page.click('#enquiry-form button[type=submit]');
  const invalid = await page.locator('[aria-invalid="true"]').count();
  if (invalid !== 4) fail(`empty submit: expected 4 invalid fields, got ${invalid}`);
  if (!(await page.evaluate(() => document.activeElement.id === 'f-name'))) fail('focus did not move to first invalid field');
  for (const id of ['f-name', 'f-email', 'f-interest', 'f-message']) {
    const text = await page.textContent(`#${id}-error`);
    const described = await page.getAttribute(`#${id}`, 'aria-describedby');
    if (!text.trim()) fail(`${id}: no error message`);
    if (!described || !described.includes(`${id}-error`)) fail(`${id}: error not linked via aria-describedby`);
  }
  await page.fill('#f-name', 'Test Person');
  if ((await page.getAttribute('#f-name', 'aria-invalid')) !== null) fail('error did not clear after fixing field');
  await page.fill('#f-email', 'not-an-email'); await page.locator('#f-email').blur();
  if (!(await page.textContent('#f-email-error')).includes('valid email')) fail('invalid email not explained');
  await page.fill('#f-email', 'test@example.com');
  await page.selectOption('#f-interest', 'market-entry');
  await page.fill('#f-message', 'Too short');
  await page.click('#enquiry-form button[type=submit]');
  if (!(await page.textContent('#f-message-error')).includes('at least 20')) fail('minlength error not explained');
  await page.fill('#f-message', 'We are planning to enter the Saudi market next year.');
  await page.click('#enquiry-form button[type=submit]');
  const cls = await page.getAttribute('#form-status', 'class');
  const href = await page.getAttribute('#form-status a', 'href');
  if (!cls.includes('is-ok')) fail(`valid submit: status not success (${cls})`);
  if (!href || !href.startsWith('mailto:ceo@elevatearabia.com?subject=Website%20enquiry%3A%20Market%20Entry')) fail(`mailto link wrong: ${href}`);
  if (href && decodeURIComponent(href).includes('Company:')) fail('empty optional field leaked into email body');

  // 6. Arabic site: language switch both ways, menu labels, Arabic form messages and email
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto(base + 'services.html');
  await page.click('.site-nav .lang-switch');
  if (!page.url().endsWith('/ar/services.html')) fail(`language switch went to ${page.url()}, expected ar/services.html`);
  await page.click('.site-nav .lang-switch');
  if (!page.url().endsWith('/services.html') || page.url().includes('/ar/')) fail(`switch back went to ${page.url()}`);
  await page.setViewportSize({ width: 375, height: 800 });
  await page.goto(base + 'ar/index.html');
  await page.click('.nav-toggle');
  if (!(await page.locator('#site-nav').isVisible())) fail('Arabic mobile menu did not open');
  if (!/[\u0600-\u06FF]/.test(await page.getAttribute('.nav-toggle', 'aria-label'))) fail('Arabic menu button label is not Arabic');
  await page.goto(base + 'ar/contact.html?interest=capital');
  await page.selectOption('#f-interest', '');
  await page.click('#enquiry-form button[type=submit]');
  for (const id of ['f-name', 'f-email', 'f-interest', 'f-message', 'form-status']) {
    const text = await page.textContent(id === 'form-status' ? '#form-status' : `#${id}-error`);
    if (!/[\u0600-\u06FF]/.test(text)) fail(`Arabic form: ${id} message is not Arabic ("${text}")`);
  }
  await page.fill('#f-name', 'سارة'); await page.fill('#f-email', 'test@example.com');
  await page.selectOption('#f-interest', 'capital'); await page.fill('#f-message', 'نخطط لجولة تمويل خلال العام القادم.');
  await page.click('#enquiry-form button[type=submit]');
  const arHref = await page.getAttribute('#form-status a', 'href');
  if (!arHref || !decodeURIComponent(arHref).includes('subject=استفسار من الموقع: رأس المال')) fail(`Arabic mailto wrong: ${arHref && decodeURIComponent(arHref).slice(0, 90)}`);

  // 7. Old Wix addresses redirect to the new pages
  for (const [old, now] of [['home-1.html', 'services.html'], ['blank-3.html', 'advisory.html'], ['terms-and-coniditions.html', 'terms.html']]) {
    await page.goto(base + old);
    await page.waitForURL((u) => u.pathname.endsWith(now), { timeout: 5000 }).catch(() => fail(`${old} did not redirect to ${now}`));
  }
  const cookies = await page.context().cookies();
  if (cookies.length) fail(`cookies set: ${cookies.map((c) => c.name).join(', ')}`);

  // 8. 404 page is served for unknown URLs
  const res = await page.goto(base + 'nope/deeper.html');
  if (res.status() !== 404 || !(await page.textContent('h1')).includes('not found')) fail('404 page not served');

  await browser.close();
  server.close();
  if (failures.length) { console.error(`QA FAILED (${failures.length})\n  ` + failures.join('\n  ')); process.exit(1); }
  console.log(`QA passed: ${pages.length} pages (English + Arabic) x 7 widths, contrast, first screen, menu, anchors, forms, language switch, redirects, cookies, 404.${SHOTS ? ' Screenshots in qa-output/.' : ''}`);
})();
