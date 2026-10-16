// Promptzilla page behaviour on the Alien UI system. Progressive enhancement only: with
// JavaScript off, every command and readout line is already in the markup.
(() => {
  const COPY_FEEDBACK_DURATION_MS = 2000;
  const REGISTERS = ['industrial', 'science-ship'];
  const root = document.documentElement;
  const status = document.getElementById('copy-status');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Visual register: the contract's two registers share roles and behaviour, so switching
  // re-skins the page without changing content. One choice is pressed at a time.
  const choices = [...document.querySelectorAll('[data-register-choice]')];
  const showRegister = (register) => {
    root.dataset.register = register;
    choices.forEach((choice) => choice.setAttribute('aria-pressed', String(choice.dataset.registerChoice === register)));
  };
  showRegister(REGISTERS.includes(root.dataset.register) ? root.dataset.register : 'industrial');
  choices.forEach((choice) => choice.addEventListener('click', () => {
    showRegister(choice.dataset.registerChoice);
    try { localStorage.setItem('pz-register', choice.dataset.registerChoice); } catch (error) {}
  }));

  // Copy controls with a manual-selection fallback when the Clipboard API is refused.
  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    const defaultAccessibleName = button.getAttribute('aria-label');
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        button.textContent = 'Copied';
        button.dataset.state = 'copied';
        button.setAttribute('aria-label', 'Copied');
        status.textContent = 'Copied';
        window.setTimeout(() => {
          button.textContent = 'Copy';
          delete button.dataset.state;
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
        status.textContent = 'Command selected for manual copy';
      }
    });
  });

  // Arrow keys scroll focused code and table regions that overflow.
  document.querySelectorAll('.pz-code, .pz-table-wrap').forEach((region) => {
    region.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      if (region.scrollWidth <= region.clientWidth) return;
      event.preventDefault();
      region.scrollLeft += (event.key === 'ArrowRight' ? 1 : -1) * Math.max(1, region.clientWidth / 4);
    });
  });

  // The CRT's last line types on at the system's machine pace. Assistive technology reads
  // the complete line from a hidden copy instead of the partial characters.
  const line = document.querySelector('[data-typeon]');
  if (line && window.TypeOn && !reducedMotion) {
    const text = line.textContent;
    const spoken = document.createElement('span');
    spoken.className = 'pz-visually-hidden';
    spoken.textContent = text;
    line.after(spoken);
    line.setAttribute('aria-hidden', 'true');
    window.TypeOn.typeOn(line, text);
  }

  // Pipeline lamps light in stage order the first time the rail is on screen.
  const rail = document.querySelector('.pz-rail');
  if (rail && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries.some((entry) => entry.isIntersecting)) {
        rail.classList.add('is-live');
        observer.disconnect();
      }
    }, { threshold: 0.4 });
    observer.observe(rail);
  } else if (rail) {
    rail.classList.add('is-live');
  }
})();
