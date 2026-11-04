/* Elevate Arabia: progressive enhancement only. Every page works without JS. */
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
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
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

  const status = $('#form-status', form);
  const fields = $$('input, select, textarea', form);
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  const problem = (field) => {
    const value = field.value.trim();
    if (field.required && !value) return field.dataset.required || 'This field is required.';
    if (field.type === 'email' && value && !EMAIL.test(value)) return 'Please enter a valid email address, like name@company.com.';
    const min = Number(field.getAttribute('minlength') || 0);
    if (min && value && value.length < min) return `Please add a little more detail (at least ${min} characters, ${value.length} so far).`;
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
      setStatus('error', [`Please check ${count === 1 ? 'the highlighted field' : `the ${count} highlighted fields`}.`]);
      first.focus();
      return;
    }

    const data = new FormData(form);
    const value = (key) => String(data.get(key) || '').trim();
    const service = select ? select.options[select.selectedIndex].text : value('interest');
    const lines = [
      `Name: ${value('name')}`,
      `Email: ${value('email')}`,
      value('company') ? `Company: ${value('company')}` : null,
      value('phone') ? `Phone: ${value('phone')}` : null,
      `Interested in: ${service}`,
      '',
      value('message'),
    ].filter((line) => line !== null);
    const to = form.dataset.to;
    const href = `mailto:${to}?subject=${encodeURIComponent(`Website enquiry: ${service}`)}&body=${encodeURIComponent(lines.join('\n'))}`;

    const manual = document.createElement('a');
    manual.href = href;
    manual.textContent = 'open it manually';
    const direct = document.createElement('a');
    direct.href = `mailto:${to}`;
    direct.textContent = to;
    setStatus('ok', ['Your email app should open with the message ready to review and send. If nothing happened, ', manual, ' or write to ', direct, '.']);

    window.location.href = href;
  });
})();
