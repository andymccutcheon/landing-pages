"""Render the page's social card using its own tokens and self-hosted typography."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from render_check import installed_chromium

CARD = """() => {
  document.body.innerHTML = `
  <main style="padding:64px;display:grid;grid-template-columns:1.45fr 1fr;gap:56px;height:630px;align-content:center;font-family:var(--pz-font)">
    <div>
      <p style="font-family:var(--pz-code);font-size:15px;letter-spacing:.16em;text-transform:uppercase;color:var(--pz-accent);margin:0 0 30px">Agent instruction engineering &amp; review</p>
      <div style="display:flex;align-items:center;gap:12px;margin:0 0 26px">
        <svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><path d="M11 4 L21 4 L16 16.5 Z" fill="#d4ed80"/><line x1="16" y1="9" x2="16" y2="16.5" stroke="#151417" stroke-width="1"/><path d="M16 18C16 23.8 12.6 27.4 6 28.6" fill="none" stroke="#d4ed80" stroke-width="1.5" stroke-linecap="round"/></svg>
        <span style="font-family:var(--pz-editorial);font-weight:600;font-size:30px;letter-spacing:-.03em">Silverquill</span>
      </div>
      <h1 style="font-family:var(--pz-font);font-size:64px;line-height:1.02;letter-spacing:-.045em;margin:0 0 24px;max-width:12ch">Give your agents better instructions.</h1>
      <p style="font-size:19px;line-height:1.5;color:var(--pz-secondary);margin:0;max-width:34ch">Creates the System Prompt and Task Prompt. Evaluates them against a published rubric. Refines them with evidence.</p>
    </div>
    <div style="align-self:center">
      <p style="font-family:var(--pz-code);font-size:14px;letter-spacing:.14em;text-transform:uppercase;color:var(--pz-muted);margin:0 0 14px">Recorded run</p>
      <p style="font-size:54px;line-height:1;letter-spacing:-.05em;margin:0;font-variant-numeric:tabular-nums">8.63</p>
      <p style="font-size:54px;line-height:1;letter-spacing:-.05em;margin:6px 0 0;color:var(--pz-accent);font-variant-numeric:tabular-nums">9.25</p>
      <p style="font-family:var(--pz-code);font-size:15px;color:var(--pz-secondary);margin:18px 0 0">Stopped at the gate · 9.00</p>
    </div>
  </main>`;
}"""

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=installed_chromium())
        page = await browser.new_page(viewport={'width': 1200, 'height': 630}, device_scale_factor=1)
        await page.goto('http://127.0.0.1:8766/ninthpass/', wait_until='networkidle')
        await page.evaluate(CARD)
        await page.evaluate('document.fonts.ready')
        await page.screenshot(path=Path(__file__).resolve().parents[1] / 'ninthpass/assets/og.png')
        await browser.close()
    print('Rendered Silverquill social card, 1200 × 630.')

if __name__ == '__main__':
    asyncio.run(main())
