// Promptzilla page behaviour. Progressive enhancement only: every command and
// every section is present and readable with JavaScript off.
(() => {
  const COPY_FEEDBACK_MS = 2000;
  const STEP_MS = 650;
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const copyStatus = document.getElementById('copy-status');

  // Header gains a quieter surface after the first scroll.
  const header = document.querySelector('[data-header]');
  const syncHeader = () => {
    if (header) header.dataset.scrolled = String(window.scrollY > 8);
  };
  syncHeader();
  window.addEventListener('scroll', syncHeader, { passive: true });

  // The three section links mark the section in view.
  const navLinks = [...document.querySelectorAll('[data-nav]')];
  const navSections = navLinks
    .map(link => document.querySelector(link.getAttribute('href')))
    .filter(Boolean);
  if ('IntersectionObserver' in window && navSections.length) {
    const spy = new IntersectionObserver((entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        const id = `#${entry.target.id}`;
        navLinks.forEach(link => {
          link.dataset.active = String(link.getAttribute('href') === id);
        });
      }
    }, { rootMargin: '-40% 0px -55% 0px' });
    navSections.forEach(section => spy.observe(section));
  }

  // Copy controls, with a manual-selection fallback when the Clipboard API refuses.
  document.querySelectorAll('[data-copy-target]').forEach((button) => {
    const defaultLabel = button.getAttribute('aria-label');
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      if (!target) return;
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        button.textContent = 'Copied';
        button.dataset.state = 'copied';
        button.setAttribute('aria-label', 'Copied');
        if (copyStatus) copyStatus.textContent = 'Copied';
        window.setTimeout(() => {
          button.textContent = 'Copy';
          delete button.dataset.state;
          if (defaultLabel) button.setAttribute('aria-label', defaultLabel);
        }, COPY_FEEDBACK_MS);
      } catch (error) {
        button.textContent = 'Select command';
        button.setAttribute('aria-label', 'Command selected for manual copy');
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(target);
        selection.removeAllRanges();
        selection.addRange(range);
        target.closest('pre')?.focus();
        if (copyStatus) copyStatus.textContent = 'Command selected for manual copy';
      }
    });
  });

  // Arrow keys scroll a focused command that overflows.
  document.querySelectorAll('.pz-code').forEach((region) => {
    region.addEventListener('keydown', (event) => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      if (region.scrollWidth <= region.clientWidth) return;
      event.preventDefault();
      const amount = Math.max(1, region.clientWidth / 4);
      region.scrollLeft += (event.key === 'ArrowRight' ? 1 : -1) * amount;
    });
  });

  // Worker tabs. Panels are already in the document; the first is the default.
  const tabRoot = document.querySelector('[data-tabs]');
  if (tabRoot) {
    const tabs = [...tabRoot.querySelectorAll('[role="tab"]')];
    const panels = tabs.map(tab => document.getElementById(tab.getAttribute('aria-controls')));
    const select = (index, moveFocus) => {
      tabs.forEach((tab, tabIndex) => {
        const selected = tabIndex === index;
        tab.setAttribute('aria-selected', String(selected));
        tab.tabIndex = selected ? 0 : -1;
        if (panels[tabIndex]) panels[tabIndex].hidden = !selected;
      });
      if (moveFocus) tabs[index].focus();
    };
    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(index, false));
      tab.addEventListener('keydown', (event) => {
        const last = tabs.length - 1;
        let next;
        if (event.key === 'ArrowRight') next = index === last ? 0 : index + 1;
        else if (event.key === 'ArrowLeft') next = index === 0 ? last : index - 1;
        else if (event.key === 'Home') next = 0;
        else if (event.key === 'End') next = last;
        else return;
        event.preventDefault();
        select(next, true);
      });
    });
    select(0, false);
  }

  // The loop: four stages, one score, and a gate that only Judge can open.
  const loop = document.querySelector('[data-loop]');
  if (loop) {
    const score = loop.querySelector('[data-loop-score]');
    const status = loop.querySelector('[data-loop-status]');
    const run = loop.querySelector('[data-loop-run]');
    const track = loop.querySelector('[data-loop-track]');
    const stages = [...loop.querySelectorAll('[data-loop-stage]')];
    let timer;
    let running = false;

    const render = (step) => {
      const judged = step >= 3;
      const complete = step >= stages.length;
      score.textContent = judged ? '09' : '08';
      status.textContent = judged ? 'STOP / approved' : 'CONTINUE / pass 1';
      status.classList.toggle('is-stop', judged);
      if (track) track.style.setProperty('--progress', String(step / stages.length));
      stages.forEach((stage, index) => {
        if (complete || index < step) stage.dataset.state = 'done';
        else if (index === step) stage.dataset.state = 'active';
        else stage.dataset.state = 'pending';
      });
    };

    const finish = () => {
      running = false;
      if (run) {
        run.disabled = false;
        run.textContent = 'Run again';
      }
      render(stages.length);
    };

    const start = () => {
      if (running) return;
      running = true;
      if (run) {
        run.disabled = true;
        run.textContent = 'Running';
      }
      if (reducedMotion.matches) {
        finish();
        return;
      }
      let step = 0;
      render(step);
      const tick = () => {
        step += 1;
        render(step);
        if (step >= stages.length) {
          finish();
          return;
        }
        timer = window.setTimeout(tick, STEP_MS);
      };
      timer = window.setTimeout(tick, STEP_MS);
    };

    if (reducedMotion.matches) {
      finish();
    } else {
      render(0);
    }
    run?.addEventListener('click', start);
    window.addEventListener('pagehide', () => window.clearTimeout(timer), { once: true });
  }
})();
