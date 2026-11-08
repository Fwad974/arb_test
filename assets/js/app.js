/* Elevate Arabia: progressive enhancement only. Every page works without JS.
   All visible text comes from the page (data attributes), so the same script
   serves the English and Arabic sites. */
(() => {
  'use strict';
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* ---------- mobile navigation ---------- */
  const toggle = $('.nav-toggle');
  const nav = $('#site-nav');
  if (toggle && nav) {
    const isOpen = () => toggle.getAttribute('aria-expanded') === 'true';
    const setOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? toggle.dataset.labelClose : toggle.dataset.labelOpen);
      document.documentElement.classList.toggle('menu-open', open);
    };
    toggle.addEventListener('click', () => setOpen(!isOpen()));
    $$('a', nav).forEach((a) => a.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && isOpen()) { setOpen(false); toggle.focus(); }
    });
    document.addEventListener('click', (e) => {
      if (isOpen() && !e.target.closest('.site-header')) setOpen(false);
    });
    window.matchMedia('(min-width: 761px)').addEventListener('change', (e) => { if (e.matches) setOpen(false); });
  }

  /* ---------- language menu (a <details> element; JS only adds closing behaviour) ---------- */
  const langMenu = $('.lang-menu');
  if (langMenu) {
    document.addEventListener('click', (e) => { if (langMenu.open && !langMenu.contains(e.target)) langMenu.open = false; });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && langMenu.open) { langMenu.open = false; $('summary', langMenu).focus(); }
    });
    langMenu.addEventListener('toggle', () => {
      // Only one menu open at a time on phones: close the navigation menu directly.
      if (langMenu.open && toggle && toggle.getAttribute('aria-expanded') === 'true') {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', toggle.dataset.labelOpen);
        document.documentElement.classList.remove('menu-open');
      }
    });
    if (toggle) toggle.addEventListener('click', () => { langMenu.open = false; });
  }

  /* ---------- copy buttons (WeChat ID) ---------- */
  $$('[data-copy]').forEach((button) => {
    const label = button.textContent;
    button.hidden = false;
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(button.dataset.copy);
      } catch (err) {
        // No clipboard access: select the ID so it can be copied by hand.
        const code = button.parentElement.querySelector('code');
        if (code) { const range = document.createRange(); range.selectNodeContents(code); getSelection().removeAllRanges(); getSelection().addRange(range); }
        return;
      }
      button.textContent = button.dataset.copied;
      button.setAttribute('aria-live', 'polite');
      setTimeout(() => { button.textContent = label; }, 2000);
    });
  });

  /* ---------- header: a soft shadow once the page has scrolled ---------- */
  const header = $('.site-header');
  if (header) {
    let queued = false;
    const update = () => { header.classList.toggle('is-scrolled', window.scrollY > 8); queued = false; };
    window.addEventListener('scroll', () => { if (!queued) { queued = true; requestAnimationFrame(update); } }, { passive: true });
    update();
  }

  /* ---------- motion: blocks rise in as they scroll into view, figures count up ----------
     Only when the head script set .motion (IntersectionObserver available, no reduced-motion
     request). Blocks already on screen are left alone, so nothing visible ever disappears. */
  if (document.documentElement.classList.contains('motion')) {
    // Lists reveal item by item; every other block reveals as a whole.
    const LISTS = '.rows, .logos, .people, .grid-values, .steps, .list, .contact-list';
    const targets = $$('main .split__head, main .wide__head, main .cta__inner');
    $$('main .split__body > *, main .section > .wrap:not(.split) > :not(.wide__head)').forEach((el) => {
      if (el.matches(LISTS)) targets.push(...el.children); else targets.push(el);
    });
    targets.sort((a, b) => (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1));
    const reveal = new IntersectionObserver((entries) => {
      let k = 0;  // stagger the blocks that arrive together
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.style.setProperty('--i', Math.min(k++, 8));
        entry.target.classList.add('is-in');
        reveal.unobserve(entry.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    // A block holding a link target (#finance) must not rise after the browser has scrolled to
    // it, or it ends up under the sticky header: show it at once instead.
    const show = (id) => {
      const target = id && document.getElementById(id);
      if (!target) return;
      targets.forEach((el) => {
        if (el.contains(target) && el.classList.contains('reveal')) {
          el.style.transition = 'none';
          el.classList.add('is-in');
          reveal.unobserve(el);
        }
      });
    };
    const fold = window.innerHeight;
    const linked = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    targets.forEach((el) => {
      if (el.getBoundingClientRect().top >= fold && !(linked && el.contains(linked))) { el.classList.add('reveal'); reveal.observe(el); }
    });
    // In-page links: show the target's block before the browser scrolls to it.
    document.addEventListener('click', (e) => {
      const a = e.target.closest('a[href*="#"]');
      if (a && a.pathname === location.pathname) show(decodeURIComponent(a.hash.slice(1)));
    });
    window.addEventListener('hashchange', () => show(decodeURIComponent(location.hash.slice(1))));

    // Figures (8, 7, 26) count up from zero when they come into view, ending on the page's own text.
    const count = (el) => {
      const text = el.textContent;
      const m = text.match(/^(\D*)(\d+)(\D*)$/);
      if (!m) return;
      const end = Number(m[2]);
      const start = performance.now();
      const step = (now) => {
        const t = Math.min(1, (now - start) / 1200);
        el.textContent = t < 1 ? m[1] + Math.round(end * (1 - (1 - t) ** 3)) + m[3] : text;
        if (t < 1) requestAnimationFrame(step);
      };
      el.textContent = m[1] + '0' + m[3];
      requestAnimationFrame(step);
    };
    const counter = new IntersectionObserver((entries) => entries.forEach((entry) => {
      if (entry.isIntersecting) { counter.unobserve(entry.target); count(entry.target); }
    }));
    $$('.stat dt').forEach((el) => counter.observe(el));

    // Trust strip: the two rows of logos drift in opposite directions. Each row is repeated
    // until one set covers the screen, then doubled for a seamless loop; the copies are hidden
    // from screen readers and the keyboard. Hover, focus or the pause button stop it.
    $$('.marquee').forEach((marquee) => {
      const viewport = $('.marquee__viewport', marquee);
      marquee.classList.add('is-moving');
      $$('.marquee__row', marquee).forEach((row, r) => {
        const items = Array.from(row.children);
        const set = row.scrollWidth || 1;
        const copies = 2 * Math.max(1, Math.ceil(viewport.clientWidth / set));
        for (let k = 1; k < copies; k++) {
          items.forEach((li) => {
            const copy = li.cloneNode(true);
            copy.setAttribute('aria-hidden', 'true');
            $$('a', copy).forEach((a) => a.setAttribute('tabindex', '-1'));
            row.appendChild(copy);
          });
        }
        row.style.setProperty('--dur', `${Math.round(row.scrollWidth / 2 / (r ? 22 : 26))}s`);  // px per second
      });
      const toggle = $('.marquee__toggle', marquee);
      if (toggle) {
        toggle.hidden = false;
        toggle.addEventListener('click', () => {
          const paused = marquee.classList.toggle('is-paused');
          toggle.setAttribute('aria-label', paused ? toggle.dataset.labelPlay : toggle.dataset.labelPause);
        });
      }
    });
  }

  /* ---------- enquiry form → pre-filled email ---------- */
  const form = $('#enquiry-form');
  if (!form) return;

  const select = $('#f-interest', form);
  const preset = new URLSearchParams(window.location.search).get('interest');
  if (select && preset && $$('option', select).some((o) => o.value === preset)) select.value = preset;

  const T = JSON.parse(form.dataset.i18n || '{}');
  const fill = (text, values) => text.replace(/\{(\w+)\}/g, (m, key) => (key in values ? values[key] : m));
  const status = $('#form-status', form);
  const fields = $$('input, select, textarea', form);
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  const problem = (field) => {
    const value = field.value.trim();
    if (field.required && !value) return field.dataset.required || T.required;
    if (field.type === 'email' && value && !EMAIL.test(value)) return T.email;
    const min = Number(field.getAttribute('minlength') || 0);
    if (min && value && value.length < min) return fill(T.min, { min, count: value.length });
    return '';
  };

  const show = (field, message) => {
    const error = document.getElementById(`${field.id}-error`);
    if (message) field.setAttribute('aria-invalid', 'true');
    else field.removeAttribute('aria-invalid');
    if (error) error.textContent = message;
  };

  const setStatus = (kind, nodes) => {
    status.className = `form-status is-${kind}`;
    status.replaceChildren(...nodes);
  };

  fields.forEach((field) => {
    // Re-check while typing only once a field has been flagged; check on blur once it has content.
    field.addEventListener('input', () => { if (field.getAttribute('aria-invalid') === 'true') show(field, problem(field)); });
    field.addEventListener('change', () => { if (field.getAttribute('aria-invalid') === 'true') show(field, problem(field)); });
    field.addEventListener('blur', () => { if (field.value.trim()) show(field, problem(field)); });
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    let first = null;
    let count = 0;
    fields.forEach((field) => {
      const message = problem(field);
      show(field, message);
      if (message) { count += 1; first = first || field; }
    });
    if (first) {
      setStatus('error', [count === 1 ? T.fixOne : fill(T.fixMany, { count })]);
      first.focus();
      return;
    }

    const data = new FormData(form);
    const value = (key) => String(data.get(key) || '').trim();
    const service = select ? select.options[select.selectedIndex].text : value('interest');
    const L = T.labels;
    const lines = [
      `${L.name}: ${value('name')}`,
      `${L.email}: ${value('email')}`,
      value('company') ? `${L.company}: ${value('company')}` : null,
      value('phone') ? `${L.phone}: ${value('phone')}` : null,
      `${L.interest}: ${service}`,
      '',
      value('message'),
    ].filter((line) => line !== null);
    const to = form.dataset.to;
    const href = `mailto:${to}?subject=${encodeURIComponent(`${T.subject}: ${service}`)}&body=${encodeURIComponent(lines.join('\n'))}`;

    // The success message has two links in it: {manual} (the prepared email) and {email} (plain address).
    const manual = document.createElement('a');
    manual.href = href;
    manual.textContent = T.okManual;
    const direct = document.createElement('a');
    direct.href = `mailto:${to}`;
    direct.dir = 'ltr';
    direct.textContent = to;
    const parts = T.ok.split(/(\{manual\}|\{email\})/).map((part) => (part === '{manual}' ? manual : part === '{email}' ? direct : part));
    setStatus('ok', parts);

    window.location.href = href;
  });
})();
