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
