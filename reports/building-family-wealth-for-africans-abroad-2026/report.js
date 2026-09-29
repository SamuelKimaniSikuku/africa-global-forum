(() => {
  if (!('IntersectionObserver' in window)) return;
  const links = document.querySelectorAll('.report-toc a');
  const observer = new IntersectionObserver(entries => entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    links.forEach(link => {
      const active = link.getAttribute('href') === '#' + entry.target.id;
      link.classList.toggle('active', active);
      if (active) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }), {rootMargin: '-20% 0px -60% 0px'});
  document.querySelectorAll('.report-body-content section').forEach(section => observer.observe(section));
})();
