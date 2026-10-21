// Progressive enhancement: content is complete without this script.
(() => {
  const root = document.documentElement;
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const toggle = document.querySelector('[data-motion-toggle]');
  const frames = [...document.querySelectorAll('[data-diagram]')];
  const visible = new Map(frames.map(frame => [frame, false]));
  let paused = false;
  try { paused = localStorage.getItem('ninthpass-motion') === 'paused'; } catch { /* Storage is optional. */ }
  const send = frame => frame.contentWindow?.postMessage({ type: 'ninthpass-motion', paused: paused || preference.matches, visible: visible.get(frame) && !document.hidden }, location.origin);
  const syncMotion = () => {
    const stopped = paused || preference.matches;
    root.dataset.motion = stopped ? 'paused' : 'running';
    toggle.setAttribute('aria-pressed', String(stopped));
    toggle.textContent = preference.matches ? 'Motion reduced' : paused ? 'Resume motion' : 'Pause motion';
    toggle.disabled = preference.matches;
    frames.forEach(send);
  };
  toggle.addEventListener('click', () => {
    paused = !paused;
    try { localStorage.setItem('ninthpass-motion', paused ? 'paused' : 'running'); } catch { /* The current page still honors the setting. */ }
    syncMotion();
  });
  preference.addEventListener('change', syncMotion);
  document.addEventListener('visibilitychange', syncMotion);
  window.addEventListener('message', event => {
    if (event.origin !== location.origin || event.data?.type !== 'ninthpass-ready') return;
    const frame = frames.find(item => item.contentWindow === event.source);
    if (frame) send(frame);
  });
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => { visible.set(entry.target, entry.isIntersecting); send(entry.target); });
  }, { threshold: 0.05 });
  frames.forEach(frame => { observer.observe(frame); frame.addEventListener('load', () => send(frame)); });
  syncMotion();

  const feedback = parseFloat(getComputedStyle(root).getPropertyValue('--pz-feedback')) || 2200;
  document.querySelectorAll('[data-copy-target]').forEach(button => {
    let timer;
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copyTarget);
      const status = document.getElementById('copy-status');
      clearTimeout(timer);
      button.disabled = true;
      button.textContent = 'Copying…';
      try {
        await navigator.clipboard.writeText(target.textContent.trim());
        button.textContent = 'Copied';
        button.dataset.state = 'copied';
        status.textContent = 'Setup and first-run commands copied.';
      } catch {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        target.closest('pre').focus();
        button.textContent = 'Commands selected';
        button.dataset.state = 'error';
        status.textContent = 'Couldn’t copy. Select the commands to copy them.';
      } finally {
        button.disabled = false;
        timer = setTimeout(() => { button.textContent = 'Copy commands'; delete button.dataset.state; }, feedback);
      }
    });
  });

  const tabs = [...document.querySelectorAll('[role="tab"]')];
  function select(index, focus = false) {
    tabs.forEach((tab, i) => {
      const active = index === i;
      tab.setAttribute('aria-selected', String(active));
      tab.tabIndex = active ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
    });
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(i));
    tab.addEventListener('keydown', event => {
      const keys = { ArrowRight: (i + 1) % tabs.length, ArrowLeft: (i + tabs.length - 1) % tabs.length, Home: 0, End: tabs.length - 1 };
      if (!(event.key in keys)) return;
      event.preventDefault(); select(keys[event.key], true);
    });
  });
  if (tabs.length) select(0);
  document.querySelectorAll('pre').forEach(pre => pre.addEventListener('keydown', event => {
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key) || pre.scrollWidth <= pre.clientWidth) return;
    event.preventDefault(); pre.scrollLeft += (event.key === 'ArrowRight' ? 1 : -1) * pre.clientWidth / 3;
  }));
})();
