(() => {
  // Feedback duration is project-local until the Pattern defines copy-button timing.
  const COPY_FEEDBACK_DURATION_MS = 2000;
  const root = document.documentElement;
  const themeButton = document.querySelector('.lp-theme');
  const setThemeButton = () => {
    const dark = root.classList.contains('dark');
    themeButton.textContent = dark ? 'Light' : 'Dark';
    themeButton.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    themeButton.setAttribute('aria-pressed', String(dark));
  };
  setThemeButton();
  themeButton.addEventListener('click', () => {
    root.classList.toggle('dark');
    try { localStorage.setItem('lp-theme', root.classList.contains('dark') ? 'dark' : 'light'); } catch (error) {}
    setThemeButton();
  });

  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    const defaultAccessibleName = button.getAttribute('aria-label');
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        button.textContent = 'Copied';
        button.setAttribute('aria-label', 'Copied');
        document.getElementById('copy-status').textContent = 'Copied';
        window.setTimeout(() => {
          button.textContent = 'Copy';
          button.setAttribute('aria-label', defaultAccessibleName);
        }, COPY_FEEDBACK_DURATION_MS);
      } catch (error) {
        button.textContent = 'Select command';
        button.setAttribute('aria-label', 'Command selected for manual copy');
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(target);
        selection.removeAllRanges();
        selection.addRange(range);
        target.closest('pre').focus();
        document.getElementById('copy-status').textContent = 'Command selected for manual copy';
      }
    });
  });

  document.querySelectorAll('.lp-scroll-region, .lp-code').forEach((region) => {
    region.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      if (region.scrollWidth <= region.clientWidth) return;
      event.preventDefault();
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      region.scrollLeft += direction * Math.max(1, region.clientWidth / 4);
    });
  });

  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    });
    document.querySelectorAll('.lp-reveal').forEach((element) => observer.observe(element));
  } else {
    document.querySelectorAll('.lp-reveal').forEach((element) => element.classList.add('is-visible'));
  }
})();

