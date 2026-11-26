/* Shared navigation; one accessible menu on all AGF pages. */
(function () {
  'use strict';
  const toggle = document.getElementById('menuToggle');
  const links = document.getElementById('navLinks');
  const year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
  if (!toggle || !links) return;
  document.documentElement.classList.add('agf-menu-ready');
  const mobile = window.matchMedia('(max-width: 1300px)');
  function setOpen(open) {
    links.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  toggle.addEventListener('click', function () { setOpen(!links.classList.contains('open')); });
  links.addEventListener('click', function (event) { if (event.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && links.classList.contains('open')) { setOpen(false); toggle.focus(); }
  });
  document.addEventListener('click', function (event) { if (!event.target.closest('.agf-nav')) setOpen(false); });
  links.closest('nav').addEventListener('focusout', function (event) {
    if (event.relatedTarget && !this.contains(event.relatedTarget)) setOpen(false);
  });
  mobile.addEventListener('change', function () { setOpen(false); });
  setOpen(false);
})();
