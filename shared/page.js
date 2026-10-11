(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('.lp-theme');
  const setThemeButton = () => {
    const dark = root.classList.contains('dark');
    themeButton.textContent = dark ? 'Light' : 'Dark';
    themeButton.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    themeButton.setAttribute('aria-pressed', String(dark));
  };
  setThemeButton();
  const docsUrl = document.body.dataset.docsUrl;
  document.querySelectorAll('[data-docs-link]').forEach((link) => { link.href = docsUrl; });
  themeButton.addEventListener('click', () => {
    root.classList.toggle('dark');
    try { localStorage.setItem('lp-theme', root.classList.contains('dark') ? 'dark' : 'light'); } catch (error) {}
    setThemeButton();
  });

  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        button.textContent = 'Copied';
        button.setAttribute('aria-label', 'Benchmark replay command copied');
        document.getElementById('copy-status').textContent = 'Benchmark command copied';
        window.setTimeout(() => {
          button.textContent = 'Copy';
          button.setAttribute('aria-label', 'Copy benchmark replay command');
        }, 2000);
      } catch (error) {
        button.textContent = 'Select command';
        button.setAttribute('aria-label', 'Select benchmark replay command to copy manually');
        target.focus();
      }
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

