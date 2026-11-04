(()=>{
  'use strict';
  const $=(q,root=document)=>root.querySelector(q);
  const $$=(q,root=document)=>Array.from(root.querySelectorAll(q));
  const menuButton=$('.menu-button');const mobileMenu=$('#mobile-menu');
  function closeMobile(){if(!menuButton||!mobileMenu)return;mobileMenu.hidden=true;menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','Open mobile menu')}
  if(menuButton&&mobileMenu){menuButton.addEventListener('click',()=>{const open=mobileMenu.hidden;mobileMenu.hidden=!open;menuButton.setAttribute('aria-expanded',String(open));menuButton.setAttribute('aria-label',open?'Close mobile menu':'Open mobile menu')});$$('a',mobileMenu).forEach(a=>a.addEventListener('click',closeMobile));}
  const dropdowns=$$('[data-dropdown]');
  function closeDropdowns(except=null){dropdowns.forEach(drop=>{if(drop===except)return;const btn=$('button',drop),panel=$('.mega-menu',drop);if(btn&&panel){panel.hidden=true;btn.setAttribute('aria-expanded','false')}})}
  dropdowns.forEach(drop=>{const btn=$('button',drop),panel=$('.mega-menu',drop);if(!btn||!panel)return;btn.addEventListener('click',()=>{const willOpen=panel.hidden;closeDropdowns(drop);panel.hidden=!willOpen;btn.setAttribute('aria-expanded',String(willOpen))});drop.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDropdowns();btn.focus()}})});
  document.addEventListener('click',e=>{if(!e.target.closest('[data-dropdown]'))closeDropdowns();if(mobileMenu&&!mobileMenu.hidden&&!e.target.closest('.nav-actions')&&!e.target.closest('.mobile-menu'))closeMobile()});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDropdowns();closeMobile()}});

  const filterButtons=$$('[data-filter]');
  if(filterButtons.length){filterButtons.forEach(btn=>btn.addEventListener('click',()=>{const category=btn.dataset.filter;filterButtons.forEach(b=>{b.classList.toggle('is-selected',b===btn);b.setAttribute('aria-pressed',String(b===btn))});let total=0;$$('[data-industry-card]').forEach(card=>{const visible=category==='All'||category===card.dataset.category;card.hidden=!visible;if(visible)total++});const empty=$('#filter-empty');if(empty)empty.hidden=total!==0;}))}

  const form=$('#enquiry-form');
  if(form){const preset=new URLSearchParams(location.search).get('interest');const select=$('#contact-interest');if(preset&&select&&$$('option',select).some(o=>o.value===preset))select.value=preset;
    const validate=(field)=>{if(field.type==='checkbox')return field.checked;const text=field.value.trim();if(field.required&&!text)return false;if(field.type==='email'&&!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(text))return false;if(field.hasAttribute('minlength')&&text.length<Number(field.getAttribute('minlength')))return false;return true};
    $$('input,select,textarea',form).forEach(field=>{const event=field.tagName==='SELECT'||field.type==='checkbox'?'change':'input';field.addEventListener(event,()=>{if(field.getAttribute('aria-invalid')==='true'&&validate(field)){field.removeAttribute('aria-invalid');const error=$('.field-error',field.closest('.field')||form);if(error)error.textContent='';}})});
    form.addEventListener('submit',e=>{e.preventDefault();let firstInvalid=null;const feedback=$('#form-feedback');$$('input[required],select[required],textarea[required]',form).forEach(field=>{const ok=validate(field);field.setAttribute('aria-invalid',String(!ok));const wrap=field.closest('.field');const error=wrap?$('.field-error',wrap):null;if(error)error.textContent=ok?'':(field.value.trim()?'Please enter a valid value.':'This field is required.');if(!ok&&!firstInvalid)firstInvalid=field});if(firstInvalid){if(feedback)feedback.textContent='Please review the highlighted fields before continuing.';firstInvalid.focus();return;}if(feedback)feedback.textContent='Your email application will open. Review the message there before sending.';
      const data=new FormData(form);const subject=encodeURIComponent('Elevate Arabia website enquiry — '+String(data.get('interest')||'General'));
      const parts=['Elevate Arabia website enquiry','','Name: '+String(data.get('name')||''),'Email: '+String(data.get('email')||''),'Company: '+String(data.get('company')||''),'Phone: '+String(data.get('phone')||''),'Service: '+String(data.get('interest')||''),'','Project details:',String(data.get('message')||'')];
      const mail='mailto:ceo@elevatearabia.com?subject='+subject+'&body='+encodeURIComponent(parts.join('\n'));
      window.location.href=mail;
    });
  }
})();
