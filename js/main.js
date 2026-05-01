/* ============================================
   Africa Global Forum — Main JS
   ============================================ */

(function () {
  'use strict';

  // ---------- Mobile menu ----------
  const toggle = document.getElementById('menuToggle');
  const links = document.getElementById('navLinks');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('open'));
    links.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') links.classList.remove('open');
    });
  }

  // ---------- Reveal on scroll ----------
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.1 });

    document
      .querySelectorAll('.pillar, .voice-card, .init-card, .num-cell, .quote-card')
      .forEach((el, i) => {
        el.classList.add('reveal');
        el.style.transitionDelay = (i * 30) + 'ms';
        io.observe(el);
      });
  }

  // ---------- Footer year ----------
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---------- Membership form ----------
  const form = document.getElementById('joinForm');
  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      // TODO: replace with real backend (Mailchimp, Airtable, Formspree, etc.)
      const btn = form.querySelector('button');
      btn.textContent = 'Application received \u2713';
      btn.style.background = 'var(--forest)';
      form.querySelectorAll('input, select').forEach((f) => (f.disabled = true));
    });
  }
})();
