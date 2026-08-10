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
      .querySelectorAll('.pillar, .voice-card, .init-card, .num-cell, .quote-card, .footer-ball')
      .forEach((el, i) => {
        el.classList.add('reveal');
        el.style.transitionDelay = (i * 30) + 'ms';
        io.observe(el);
      });
  }

  // ---------- Reports topic filter + progressive disclosure ----------
  const filterBar = document.getElementById('reportFilter');
  const reportList = document.getElementById('reportList');
  const expandBtn = document.getElementById('reportExpandBtn');
  const collapseBtn = document.getElementById('reportCollapseBtn');
  const expandCountEl = document.getElementById('reportExpandCount');
  const items = document.querySelectorAll('.report-item');

  if (expandCountEl) expandCountEl.textContent = items.length;

  // Set the expander to the total count on the active filter
  function refreshExpandLabel() {
    if (!expandCountEl || !filterBar) return;
    const activeBtn = filterBar.querySelector('.report-filter-btn.is-active') ||
      filterBar.querySelector('.report-filter-btn[aria-pressed="true"]');
    const cat = activeBtn ? activeBtn.dataset.category : 'all';
    const visibleTotal = cat === 'all'
      ? items.length
      : Array.from(items).filter(i => i.getAttribute('data-category') === cat).length;
    expandCountEl.textContent = visibleTotal;
  }

  if (filterBar) {
    const buttons = filterBar.querySelectorAll('.report-filter-btn');
    buttons.forEach((btn) => {
      btn.addEventListener('click', () => {
        const cat = btn.dataset.category;
        buttons.forEach((b) => {
          const active = b === btn;
          b.setAttribute('aria-pressed', active ? 'true' : 'false');
          b.classList.toggle('is-active', active);
        });
        items.forEach((item) => {
          const itemCat = item.getAttribute('data-category');
          item.classList.toggle('is-hidden', cat !== 'all' && itemCat !== cat);
        });
        // When a filter is picked, uncollapse so the user sees every match
        if (reportList && cat !== 'all') {
          reportList.classList.remove('is-collapsed');
          if (expandBtn) expandBtn.hidden = true;
          if (collapseBtn) collapseBtn.hidden = true;
        } else if (reportList && cat === 'all') {
          // Back to All → re-collapse for a compact default view
          reportList.classList.add('is-collapsed');
          if (expandBtn) expandBtn.hidden = false;
          if (collapseBtn) collapseBtn.hidden = true;
        }
        refreshExpandLabel();
      });
    });
  }

  if (expandBtn && reportList) {
    expandBtn.addEventListener('click', () => {
      reportList.classList.remove('is-collapsed');
      expandBtn.hidden = true;
      if (collapseBtn) collapseBtn.hidden = false;
    });
  }
  if (collapseBtn && reportList) {
    collapseBtn.addEventListener('click', () => {
      reportList.classList.add('is-collapsed');
      collapseBtn.hidden = true;
      if (expandBtn) expandBtn.hidden = false;
      // Scroll back to reports section top so the user sees the collapsed state
      document.getElementById('reports')?.scrollIntoView({behavior: 'smooth', block: 'start'});
    });
  }

  refreshExpandLabel();

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
