(() => {
  const status = document.getElementById('copy-status');
  document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', async () => {
      const target = document.getElementById(button.dataset.copy);
      const text = target.textContent.trim();
      try {
        await navigator.clipboard.writeText(text);
        button.textContent = 'Copied';
        status.textContent = 'Copied to clipboard';
      } catch {
        const range = document.createRange();
        range.selectNodeContents(target);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        target.closest('.command').focus?.();
        button.textContent = 'Select and copy';
        status.textContent = 'Text selected. Copy it with your keyboard.';
      }
      window.setTimeout(() => { button.textContent = button.dataset.copy === 'install-command' ? 'Copy command' : 'Copy JSON'; }, 2000);
    });
  });
})();
