#!/usr/bin/env node
/*
 * Browser QA for the built site in ./dist. Run `python3 build.py` first.
 *
 *   npm install --no-save playwright && npx playwright install chromium   (once)
 *   node scripts/qa.cjs              checks only
 *   node scripts/qa.cjs --shots      checks + screenshots in ./qa-output
 *
 * Every layout, error and contrast check runs in light AND dark mode, and the
 * page must look identical with the browser's forced dark mode switched on.
 * Checks: horizontal overflow at 8 widths (320-2560px), JS errors, AA text
 * contrast, headline on the first screen, large screens using their width, the logo, motion,
 * the moving logo strip and its pause button, the landing animation, mobile menu, anchors clearing the
 * sticky header, contact form behaviour, redirects from old addresses, no
 * cookies, no leftover research notes in the legal text, and for the translated
 * sites (/ar/, /zh/, /ja/): lang/dir, untranslated text, the language menu and the forms.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const DIST = path.resolve(__dirname, '..', 'dist');
const OUT = path.resolve(__dirname, '..', 'qa-output');
const SHOTS = process.argv.includes('--shots');
// Translated sites: folder -> expected <html lang/dir> and the script their text is written in.
const LANGS = {
  ar: { code: 'ar', dir: 'rtl', script: '[\\u0600-\\u06FF]' },
  zh: { code: 'zh-Hans', dir: 'ltr', script: '[\\u3400-\\u9FFF]' },
  ja: { code: 'ja', dir: 'ltr', script: '[\\u3040-\\u30FF\\u3400-\\u9FFF]' },
};
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
    .concat(...Object.keys(LANGS).map((d) => fs.readdirSync(path.join(DIST, d)).filter((f) => f.endsWith('.html')).map((f) => `${d}/${f}`)));
  const browser = await chromium.launch();
  const failures = [];
  const fail = (msg) => failures.push(msg);
  // Wait for page-load and reveal animations to end before measuring positions. Looping
  // animations (the moving logo strip) never end, so they are skipped, and 5 s is the limit.
  const settle = (p) => p.evaluate(() => Promise.race([
    Promise.all(document.getAnimations()
      .filter((a) => a.timeline === document.timeline && a.effect && a.effect.getComputedTiming().endTime !== Infinity)
      .map((a) => a.finished.catch(() => {}))),
    new Promise((done) => setTimeout(done, 5000)),
  ]));
  if (SHOTS) fs.mkdirSync(OUT, { recursive: true });

  // 1. Layout + errors + contrast across widths, in both colour schemes
  for (const scheme of ['light', 'dark']) for (const width of [320, 375, 768, 1024, 1280, 1440, 1920, 2560]) {
    const page = await browser.newPage({ viewport: { width, height: 900 }, colorScheme: scheme });
    page.on('pageerror', (err) => fail(`JS error @${width}: ${err.message}`));
    page.on('console', (msg) => { if (msg.type() === 'error') fail(`console error @${width}: ${msg.text()}`); });
    for (const name of pages) {
      await page.goto(base + name);
      const scroll = await page.evaluate(() => document.documentElement.scrollWidth);
      if (scroll > width) fail(`${name} @${width}px ${scheme}: horizontal overflow (${scroll}px)`);
      if (width === 1280) {
        const text = await page.evaluate(() => document.body.innerText);
        for (const note of ['Saudi official website', 'SDAIA states', 'The PDPL is the principal']) if (text.includes(note)) fail(`${name}: leftover research note "${note}"`);
        if (await page.evaluate(() => document.cookie !== '')) fail(`${name}: sets a cookie`);
        const L = LANGS[name.split('/')[0]];
        if (L) {
          const [lang, dir] = await page.evaluate(() => [document.documentElement.lang, document.documentElement.dir]);
          if (lang !== L.code || dir !== L.dir) fail(`${name}: expected lang="${L.code}" dir="${L.dir}", got ${lang}/${dir}`);
          // Latin-only text on a translated page should be a name, address, number or brand, marked lang or dir.
          const untranslated = await page.evaluate((script) => {
            const own = new RegExp(script);
            const out = [];
            const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
            for (let n = walker.nextNode(); n; n = walker.nextNode()) {
              const text = n.textContent.trim();
              const el = n.parentElement;
              if (!text || !/[A-Za-z]{3,}/.test(text) || own.test(text)) continue;
              if (el.closest('[lang]:not(html), [dir="ltr"]:not(html), script, style, .visually-hidden')) continue;
              if (/^(©\s*\d{4}\s*)?Elevate Arabia$|^(WhatsApp|WeChat|LINE)$/.test(text)) continue;
              out.push(text.slice(0, 40));
            }
            return out;
          }, L.script);
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
        low.forEach((b) => fail(`${name} @${width}px ${scheme}: low contrast ${b}`));
      }
    }
    if (SHOTS && scheme === 'light' && (width === 375 || width === 1440)) {
      await page.emulateMedia({ reducedMotion: 'reduce' });  // full-page shots: no reveal, all content
      for (const name of ['index.html', 'services.html', 'advisory.html', 'about.html', 'contact.html', 'ar/index.html', 'ar/about.html', 'ar/contact.html', 'zh/index.html', 'zh/contact.html', 'ja/index.html', 'ja/contact.html']) {
        await page.goto(base + name);
        await page.screenshot({ path: path.join(OUT, `${name.replace('.html', '').replace('/', '-')}-${width}.png`), fullPage: true });
      }
    }
    await page.close();
  }

  // 1b. Forced dark mode (Chrome/Samsung "darken websites") must not repaint the page:
  //     with color-scheme declared, it should render exactly like our own dark theme.
  const forced = await chromium.launch({ args: ['--blink-settings=forceDarkModeEnabled=true'] });
  for (const name of ['index.html', 'ar/index.html', 'zh/index.html', 'ja/index.html', 'about.html', 'contact.html']) {
    const shots = [];
    for (const b of [browser, forced]) {
      const p = await b.newPage({ viewport: { width: 390, height: 844 }, colorScheme: 'dark', reducedMotion: 'reduce' });
      await p.goto(base + name);
      // Finish the logo intro first, so both screenshots show the same frame. Wait, too, for the
      // images on screen to decode: the home photo decodes asynchronously, and a screenshot taken
      // before then shows an empty box in one browser and the photo in the other.
      await p.evaluate(async () => {
        await document.fonts.ready;
        await Promise.all([...document.images].filter((i) => { const r = i.getBoundingClientRect(); return r.bottom > 0 && r.top < innerHeight; })
          .map((i) => i.decode().catch(() => {})));
        document.getAnimations().filter((a) => a.effect && a.effect.getComputedTiming().endTime !== Infinity).forEach((a) => a.finish());
      });
      shots.push(await p.screenshot({ animations: 'disabled' }));
      await p.close();
    }
    if (!shots[0].equals(shots[1])) fail(`${name}: forced dark mode changes the page (browser is repainting it)`);
  }
  await forced.close();

  // 2. Headline, intro and main button on the first screen (laptop) / headline (phone)
  for (const [w, h, sel, home] of [[1280, 720, '.hero .button', 'index.html'], [1366, 768, '.hero .button', 'index.html'],
    [375, 667, '.hero h1', 'index.html'], [1280, 720, '.hero .button', 'ar/index.html'], [375, 667, '.hero h1', 'ar/index.html'],
    [1280, 720, '.hero .button', 'zh/index.html'], [375, 667, '.hero h1', 'zh/index.html'],
    [1280, 720, '.hero .button', 'ja/index.html'], [375, 667, '.hero h1', 'ja/index.html']]) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    await p.goto(base + home);
    await p.evaluate(() => document.fonts.ready);
    await settle(p);
    const bottom = await p.evaluate((s) => document.querySelector(s).getBoundingClientRect().bottom, sel);
    if (bottom > h) fail(`${home} @${w}x${h}: "${sel}" below the first screen (${Math.round(bottom)}px)`);
    await p.close();
  }

  // 2b. Large screens use their width: the type scale grows, the content fills most of the
  //     screen, and the hero puts its intro (or the home page's stats) beside the headline.
  for (const [w, h] of [[1920, 1080], [2560, 1440]]) {
    const p = await browser.newPage({ viewport: { width: w, height: h } });
    for (const dir of ['', 'ar/', 'zh/', 'ja/']) for (const file of ['index.html', 'about.html', 'advisory.html', 'contact.html']) {
      const name = dir + file;
      await p.goto(base + name);
      await p.evaluate(() => document.fonts.ready);
      await settle(p);
      const m = await p.evaluate(() => {
        const box = (s) => { const el = document.querySelector(s); return el && el.getBoundingClientRect(); };
        const h1 = box('.hero h1'), beside = box('.hero--home .hero__photo') || box('.hero__side');
        return { root: parseFloat(getComputedStyle(document.documentElement).fontSize), content: box('main .section .wrap').width,
          beside: !!beside && beside.top < h1.bottom };
      });
      if (m.root <= 16) fail(`${name} @${w}px: text does not scale up (root ${m.root}px)`);
      if (m.content < w * 0.55) fail(`${name} @${w}px: content only ${Math.round(m.content / w * 100)}% of the screen`);
      if (!m.beside) fail(`${name} @${w}px: hero intro is not beside the headline`);
    }
    await p.close();
  }

  // 2c. Home header photo: on wide screens a panel the full height of the header, running to the
  //     screen edge (the left edge in Arabic) and clear of the text; on smaller screens a band the
  //     full width of the screen above the headline. Its caption names the place.
  for (const dir of ['', 'ar/']) for (const [w, h] of [[1280, 720], [1440, 900], [1920, 1080], [2560, 1440], [1024, 768], [390, 844]]) {
    const p = await browser.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    await p.goto(base + dir + 'index.html');
    await p.evaluate(() => document.fonts.ready);
    const m = await p.evaluate(() => {
      const r = (el) => el.getBoundingClientRect();
      return { hero: r(document.querySelector('.hero--home')), photo: r(document.querySelector('.hero__photo')), h1: r(document.querySelector('.hero h1')),
        text: [...document.querySelectorAll('.hero--home .wrap > *')].map(r), vw: document.documentElement.clientWidth,
        rtl: document.dir === 'rtl', place: (document.querySelector('.hero__place') || {}).textContent || '' };
    });
    const name = `${dir}index.html @${w}px`;
    if (w >= 1200) {
      const short = m.rtl ? m.photo.left : m.vw - m.photo.right;
      if (Math.abs(short) > 1) fail(`${name}: header photo stops ${Math.round(short)}px short of the screen edge`);
      if (Math.abs(m.photo.top - m.hero.top) > 1 || Math.abs(m.photo.bottom - m.hero.bottom) > 1) fail(`${name}: header photo is not the full height of the header`);
      if (m.text.some((t) => (m.rtl ? t.left < m.photo.right : t.right > m.photo.left))) fail(`${name}: header text runs under the photo`);
    } else {
      if (m.photo.left > 0.5 || m.photo.width < m.vw - 1) fail(`${name}: header photo band is not the full width of the screen`);
      if (m.photo.bottom > m.h1.top) fail(`${name}: header photo band is not above the headline`);
    }
    if (!m.place.trim()) fail(`${name}: header photo caption does not name the place`);
    await p.close();
  }

  // 2d. Layout: no large empty space beside a heading. In every side-by-side block (a two-column
  //     section, a service on the Services page, a full-width heading with a block beside it) the
  //     content may run at most 300px past the heading column; longer content belongs in an aside
  //     under the heading or in a full-width section (see "Layout" in the README).
  for (const [w, h] of [[1440, 900], [1920, 1080]]) {
    const p = await browser.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
    for (const name of pages) {
      await p.goto(base + name);
      await p.evaluate(() => document.fonts.ready);
      const gaps = await p.evaluate(() => {
        const out = [];
        const check = (el, head, body) => {
          if (!head || !body) return;
          const a = head.getBoundingClientRect(), b = body.getBoundingClientRect();
          if (b.left < a.right - 1 && a.left < b.right - 1) return;  // stacked, not side by side
          if (b.height - a.height > 300) out.push(`${((el.querySelector('h2') || {}).textContent || '').trim().slice(0, 40)} (${Math.round(b.height - a.height)}px)`);
        };
        document.querySelectorAll('.split').forEach((s) => check(s, s.querySelector(':scope > .split__head'), s.querySelector(':scope > .split__body')));
        document.querySelectorAll('.service').forEach((s) => check(s, s.querySelector('.service__head'), s.querySelector('.service__body')));
        document.querySelectorAll('.wide__head--side').forEach((s) => check(s, s.querySelector(':scope > .wide__title'), s.querySelector(':scope > :not(.wide__title)')));
        return out;
      });
      for (const g of gaps) fail(`${name} @${w}px: large empty space beside the heading: ${g}`);
    }
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
  for (const target of ['advisory.html#finance', 'about.html#partnership', 'sectors.html#education', 'ar/advisory.html#finance', 'ja/advisory.html#finance']) {
    await page.goto(base + target); await page.waitForTimeout(400); await settle(page);
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

  // 6. Language menu: the same page in every language, round trip, on desktop and phone
  for (const vp of [{ width: 1280, height: 800 }, { width: 375, height: 800 }]) {
    await page.setViewportSize(vp);
    await page.goto(base + 'services.html');
    for (const [label, expected] of [['中文', '/zh/services.html'], ['日本語', '/ja/services.html'], ['العربية', '/ar/services.html'], ['English', '/services.html']]) {
      await page.click('.lang-menu summary');
      await page.click(`.lang-menu a:text-is("${label}")`);
      const url = new URL(page.url()).pathname;
      if (!url.endsWith(expected) || (expected === '/services.html' && /\/(ar|zh|ja)\//.test(url))) fail(`language menu (${vp.width}px): ${label} went to ${url}, expected ${expected}`);
    }
  }
  await page.goto(base + 'index.html');
  await page.click('.lang-menu summary');
  await page.keyboard.press('Escape');
  if (await page.locator('.lang-menu ul').isVisible()) fail('Escape did not close the language menu');
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
  // Chinese and Japanese forms: messages in their own script, email subject localised.
  for (const [dir, subject] of [['zh', '网站咨询: 资本'], ['ja', 'ウェブサイトからのお問い合わせ: 資本']]) {
    const own = new RegExp(LANGS[dir].script);
    await page.goto(base + `${dir}/contact.html`);
    await page.click('#enquiry-form button[type=submit]');
    for (const id of ['f-name-error', 'f-email-error', 'form-status']) {
      const text = await page.textContent(`#${id}`);
      if (!own.test(text)) fail(`${dir} form: ${id} is not in ${dir} ("${text}")`);
    }
    await page.fill('#f-name', 'Test'); await page.fill('#f-email', 'test@example.com');
    await page.selectOption('#f-interest', 'capital'); await page.fill('#f-message', '我们计划明年在沙特阿拉伯开展融资计划，希望了解更多。');
    await page.click('#enquiry-form button[type=submit]');
    const href = await page.getAttribute('#form-status a', 'href');
    if (!href || !decodeURIComponent(href).includes(`subject=${subject}`)) fail(`${dir} mailto wrong: ${href && decodeURIComponent(href).slice(0, 80)}`);
  }

  // 6b. Messaging apps from site.env: contact page links, footer row, WeChat copy button
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, permissions: ['clipboard-read', 'clipboard-write'] });
  const cp = await ctx.newPage();
  for (const name of ['contact.html', 'ar/contact.html', 'zh/contact.html', 'ja/contact.html']) {
    await cp.goto(base + name);
    const wa = await cp.getAttribute('.contact-list a[href^="https://wa.me/"]', 'href').catch(() => null);
    if (!wa || !/^https:\/\/wa\.me\/\d{8,15}\?text=/.test(wa)) fail(`${name}: WhatsApp link missing or malformed (${wa})`);
    if (!(await cp.locator('.contact-list a[href^="https://line.me/R/ti/p/"]').count())) fail(`${name}: LINE link missing`);
    if ((await cp.locator('.footer-apps li').count()) !== 3) fail(`${name}: footer should list 3 messaging apps`);
    if (!(await cp.locator('.hero a[href^="https://wa.me/"]').count())) fail(`${name}: WhatsApp link missing from the first screen`);
  }
  // Linked partner logos (third value in CLIENTS_NETWORK) open the partner's site in a new tab.
  for (const name of ['index.html', 'ar/index.html', 'zh/index.html', 'ja/index.html']) {
    await cp.goto(base + name);
    const link = cp.locator('#clients li:not([aria-hidden]) a[href="https://www.flopexa.com/"]');
    if ((await link.count()) !== 1 || (await link.getAttribute('target')) !== '_blank') fail(`${name}: Flopexa logo link missing`);
  }
  await cp.goto(base + 'contact.html');
  const wechatId = (await cp.textContent('#wechat code')).trim();
  await cp.click('#wechat .copy-button');
  if ((await cp.evaluate(() => navigator.clipboard.readText())) !== wechatId) fail('WeChat copy button did not copy the ID');
  if ((await cp.textContent('#wechat .copy-button')).trim() !== 'Copied') fail('WeChat copy button gave no feedback');
  await ctx.close();

  // 6c. Logo: inline SVG whose letters follow the theme. On arrival the landing animation forms
  //     the wordmark (letters one by one, the red line drawing up, the kanji fading in); back on
  //     the home page from inside the site, the header logo plays the same intro; other pages
  //     inside the site play neither. The bar lifts on hover, nothing moves with reduced motion,
  //     and the footer's beige copy loads.
  const logoAnims = (p) => p.evaluate(() => document.getAnimations().map((a) => a.animationName).filter(Boolean));
  for (const scheme of ['light', 'dark']) {
    const lp = await browser.newPage({ viewport: { width: 1280, height: 800 }, colorScheme: scheme });
    await lp.goto(base + 'index.html');
    const fill = await lp.evaluate(() => getComputedStyle(document.querySelector('.site-header .logo path')).fill);
    const want = scheme === 'light' ? 'rgb(15, 33, 55)' : 'rgb(180, 162, 152)';
    if (fill !== want) fail(`logo letters in ${scheme} mode are ${fill}, expected ${want}`);
    if (scheme === 'light') {
      if (!(await lp.evaluate(() => document.documentElement.classList.contains('splash-active')))) fail('landing animation did not play on arrival');
      const arrival = await lp.evaluate(() => [...document.querySelectorAll('.splash__logo *')].flatMap((el) => el.getAnimations()).map((a) => a.animationName));
      for (const name of ['logo-letter', 'logo-draw', 'logo-fade']) if (!arrival.includes(name)) fail(`logo: ${name} missing on arrival`);
      await lp.waitForSelector('.splash', { state: 'detached', timeout: 5000 }).catch(() => fail('landing animation did not end'));
      await settle(lp);
      await lp.hover('.site-header .brand');
      await lp.waitForTimeout(800);
      if ((await lp.evaluate(() => getComputedStyle(document.querySelector('.site-header .logo__bar')).transform)) === 'none') fail('logo bar does not lift on hover');
      await Promise.all([lp.waitForNavigation(), lp.click('.site-nav a[href="about.html"]')]);
      if (await lp.evaluate(() => document.documentElement.classList.contains('logo-intro'))) fail('logo intro replays on pages inside the site');
      const inside = (await logoAnims(lp)).filter((n) => n.startsWith('logo-'));
      if (inside.length) fail(`logo moves on pages inside the site: ${inside.join(', ')}`);
      const foot = lp.locator('.site-footer .brand img');
      await foot.scrollIntoViewIfNeeded();
      if (!(await foot.evaluate((i) => i.decode().then(() => i.naturalWidth > 0, () => false)))) fail('footer logo did not load');
      // Back to the home page from inside the site: the intro plays again, for presenting.
      await Promise.all([lp.waitForNavigation(), lp.click('.site-header .brand')]);
      if (!(await logoAnims(lp)).includes('logo-letter')) fail('logo intro does not play on the home page');
    }
    await lp.close();
  }
  for (const [dir, label] of [['ar/', /[\u0600-\u06FF]/], ['zh/', /首页/], ['ja/', /ホーム/]]) {
    const lp = await browser.newPage();
    await lp.goto(base + dir + 'index.html');
    if (!label.test(await lp.getAttribute('.site-header .brand', 'aria-label'))) fail(`${dir}: logo link label is not translated`);
    await lp.close();
  }
  const rm = await browser.newPage({ reducedMotion: 'reduce' });
  await rm.goto(base + 'index.html');
  if ((await logoAnims(rm)).some((n) => n.startsWith('logo-'))) fail('logo animates with reduced motion requested');
  await rm.close();

  // 6d. Motion: the page header rises in, blocks below the first screen start hidden and are all
  //     revealed by scrolling, nothing on the first screen is ever hidden, the figures count up
  //     to the page's own numbers, and the header gains its shadow. With reduced motion or
  //     without JavaScript, nothing is hidden and nothing animates.
  for (const name of ['index.html', 'about.html', 'ar/index.html', 'zh/services.html', 'ja/sectors.html']) {
    const mp = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await mp.goto(base + name);
    const start = await mp.evaluate(() => ({
      motion: document.documentElement.classList.contains('motion'),
      rise: getComputedStyle(document.querySelector('.hero h1')).animationName,
      hidden: document.querySelectorAll('.reveal').length,
      onScreen: [...document.querySelectorAll('.reveal')].filter((el) => el.getBoundingClientRect().top < innerHeight).length,
    }));
    if (!start.motion || start.rise !== 'rise') fail(`${name}: page header does not rise in (${JSON.stringify(start)})`);
    if (!start.hidden) fail(`${name}: no blocks reveal on scroll`);
    if (start.onScreen) fail(`${name}: ${start.onScreen} block(s) on the first screen start hidden`);
    for (let y = 0; y < 15000; y += 350) { await mp.evaluate((y) => scrollTo(0, y), y); await mp.waitForTimeout(50); }
    await mp.waitForTimeout(1500);
    await settle(mp);
    const end = await mp.evaluate(() => ({
      left: document.querySelectorAll('.reveal:not(.is-in)').length,
      faint: [...document.querySelectorAll('.reveal')].filter((el) => getComputedStyle(el).opacity !== '1').length,
      shadow: document.querySelector('.site-header').classList.contains('is-scrolled'),
      stats: [...document.querySelectorAll('.stat dt')].map((d) => d.textContent).join(','),
    }));
    if (end.left || end.faint) fail(`${name}: ${end.left + end.faint} block(s) still hidden after scrolling to the end`);
    if (!end.shadow) fail(`${name}: header shadow missing after scrolling`);
    if (name.endsWith('index.html') && end.stats !== '8,7,26') fail(`${name}: figures ended as ${end.stats}, expected 8,7,26`);
    await mp.close();
  }
  for (const opts of [{ reducedMotion: 'reduce' }, { javaScriptEnabled: false }]) {
    const ctx = await browser.newContext({ viewport: { width: 1280, height: 800 }, ...opts });
    const sp = await ctx.newPage();
    await sp.goto(base + 'index.html');
    const still = await sp.evaluate(() => ({
      curtain: getComputedStyle(document.querySelector('.splash')).display,
      motion: document.documentElement.classList.contains('motion'),
      hidden: document.querySelectorAll('.reveal').length,
      rise: getComputedStyle(document.querySelector('.hero h1')).animationName,
      stats: [...document.querySelectorAll('.stat dt')].map((d) => d.textContent).join(','),
    }));
    if (still.curtain !== 'none' || still.motion || still.hidden || still.rise !== 'none' || still.stats !== '8,7,26') fail(`${JSON.stringify(opts)}: expected a still page with everything visible, got ${JSON.stringify(still)}`);
    await ctx.close();
  }

  // 6e. Trust strip on the home page, right under the page header: the two rows of client logos
  //     move, the copies that make the loop seamless are hidden from screen readers and the
  //     keyboard, the pause button stops and restarts them with a label in the page's language,
  //     and with reduced motion the logos are a still grid with no button.
  {
    const tp = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await tp.goto(base + 'index.html');
    const strip = await tp.evaluate(() => {
      const m = document.querySelector('.marquee');
      return {
        afterHero: !!document.querySelector('main .hero + .trust'),
        moving: m.classList.contains('is-moving'),
        anims: [...m.querySelectorAll('.marquee__row')].map((r) => getComputedStyle(r).animationName),
        real: m.querySelectorAll('li:not([aria-hidden])').length,
        focusableCopies: m.querySelectorAll('li[aria-hidden] a:not([tabindex="-1"])').length,
        button: !m.querySelector('.marquee__toggle').hidden,
      };
    });
    if (!strip.afterHero) fail('trust strip is not right under the home page header');
    if (!strip.moving || strip.anims.join() !== 'marquee,marquee') fail(`trust strip does not move (${JSON.stringify(strip)})`);
    if (strip.real !== 14) fail(`trust strip shows ${strip.real} logos, expected 14`);
    if (strip.focusableCopies) fail('trust strip: hidden logo copies can take keyboard focus');
    if (!strip.button) fail('trust strip: pause button missing');
    const toggle = tp.locator('.marquee__toggle');
    const pauseLabel = await toggle.getAttribute('aria-label');
    await toggle.click();
    const paused = await tp.evaluate(() => getComputedStyle(document.querySelector('.marquee__row')).animationPlayState);
    if (paused !== 'paused' || (await toggle.getAttribute('aria-label')) === pauseLabel) fail('trust strip: pause button does not pause or relabel');
    await toggle.click();
    await tp.mouse.move(5, 5);
    if ((await tp.evaluate(() => getComputedStyle(document.querySelector('.marquee__row')).animationPlayState)) !== 'running') fail('trust strip: does not restart');
    for (const [dir, own] of [['ar/', /[\u0600-\u06FF]/], ['zh/', /[\u3400-\u9FFF]/], ['ja/', /[\u3040-\u30FF]/]]) {
      await tp.goto(base + dir + 'index.html');
      if (!own.test(await tp.getAttribute('.marquee__toggle', 'aria-label'))) fail(`${dir}: pause button label is not translated`);
    }
    await tp.close();
    const still = await browser.newPage({ viewport: { width: 1280, height: 800 }, reducedMotion: 'reduce' });
    await still.goto(base + 'index.html');
    const s2 = await still.evaluate(() => ({ moving: document.querySelector('.marquee').classList.contains('is-moving'),
      button: !document.querySelector('.marquee__toggle').hidden, logos: document.querySelectorAll('.marquee li').length }));
    if (s2.moving || s2.button || s2.logos !== 14) fail(`trust strip with reduced motion: expected 14 still logos and no button, got ${JSON.stringify(s2)}`);
    await still.close();
  }

  // 6f. Landing animation: on arrival (no referrer) a curtain covers the page while the wordmark
  //     forms and the header logo waits; the wordmark then glides into the header as the curtain
  //     lifts, and within 3.5 s everything is gone and the header logo shows. A key press skips
  //     it; it does not play when moving between pages or with reduced motion; a reload always
  //     replays it.
  for (const [name, vp] of [['index.html', { width: 1280, height: 800 }], ['ar/index.html', { width: 1280, height: 800 }],
    ['ja/services.html', { width: 375, height: 740 }]]) {
    const sp = await browser.newPage({ viewport: vp });
    await sp.goto(base + name);
    const first = await sp.evaluate(() => {
      const curtain = document.querySelector('.splash');
      const r = curtain.getBoundingClientRect();
      return { active: document.documentElement.classList.contains('splash-active'),
        covers: getComputedStyle(curtain).display !== 'none' && r.width >= innerWidth && r.height >= innerHeight,
        headerLogo: getComputedStyle(document.querySelector('.site-header .logo')).visibility };
    });
    if (!first.active || !first.covers || first.headerLogo !== 'hidden') fail(`${name}: landing animation did not start (${JSON.stringify(first)})`);
    const glide = await sp.waitForFunction(() => {
      const mark = document.querySelector('.splash__logo');
      if (!mark) return 'gone';
      return mark.getAnimations().some((a) => !(a instanceof CSSAnimation)) ? 'glide' : false;
    }, null, { timeout: 3000, polling: 50 }).then((h) => h.jsonValue(), () => 'timeout');
    if (glide !== 'glide') fail(`${name}: the wordmark did not glide into the header (${glide})`);
    const ended = await sp.waitForSelector('.splash', { state: 'detached', timeout: 3500 }).then(() => true, () => false);
    const after = await sp.evaluate(() => ({ active: document.documentElement.classList.contains('splash-active'),
      headerLogo: getComputedStyle(document.querySelector('.site-header .logo')).visibility }));
    if (!ended || after.active || after.headerLogo !== 'visible') fail(`${name}: landing animation did not end cleanly (${JSON.stringify(after)})`);
    await sp.close();
  }
  {
    const kp = await browser.newPage({ viewport: { width: 1280, height: 800 } });
    await kp.goto(base + 'about.html');
    await kp.waitForTimeout(300);
    await kp.keyboard.press('Shift');
    if (!(await kp.waitForSelector('.splash', { state: 'detached', timeout: 1000 }).then(() => true, () => false))) fail('landing animation: a key press does not skip it');
    await kp.goto(base + 'services.html', { referer: base + 'about.html' });
    if (await kp.evaluate(() => document.documentElement.classList.contains('splash-active'))) fail('landing animation plays on pages inside the site');
    // A reload always replays it, even on a page reached from inside the site (for presenting).
    await kp.reload();
    if (!(await kp.evaluate(() => document.documentElement.classList.contains('splash-active')))) fail('landing animation does not replay on reload');
    // Stylesheet and script URLs carry a content hash, so a new deploy never runs on stale CSS or JS.
    const versioned = await kp.evaluate(() => [document.querySelector('link[rel="stylesheet"]').href, document.querySelector('script[src*="app.js"]').src]
      .every((u) => /[?]v=[0-9a-f]{10}$/.test(u)));
    if (!versioned) fail('stylesheet or script URL has no ?v= content hash');
    await kp.close();
    const rp = await browser.newPage({ reducedMotion: 'reduce' });
    await rp.goto(base + 'index.html');
    if (await rp.evaluate(() => document.documentElement.classList.contains('splash-active') || getComputedStyle(document.querySelector('.splash')).display !== 'none')) fail('landing animation plays with reduced motion requested');
    await rp.close();
  }

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
  console.log(`QA passed: ${pages.length} pages (English, Arabic, Chinese, Japanese) x 8 widths x light/dark, contrast, forced dark, first screen, large screens, logo, landing animation, motion, logo strip, menus, anchors, forms, language menu, messaging, redirects, cookies, 404.${SHOTS ? ' Screenshots in qa-output/.' : ''}`);
})();
