"""Render the page's social card using its own tokens and self-hosted typography."""
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from render_check import installed_chromium

async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=installed_chromium())
        page=await browser.new_page(viewport={'width':1200,'height':630},device_scale_factor=1)
        await page.goto('http://127.0.0.1:8899/ninthpass/',wait_until='networkidle')
        await page.evaluate('''() => { document.body.innerHTML = `<main style="padding:60px;display:grid;grid-template-columns:1.5fr 1fr;gap:48px;height:630px;align-content:center"><div><p style="font-size:24px;margin-bottom:60px">Ninth Pass</p><h1 style="font-size:78px;line-height:.98;letter-spacing:-.055em">Put your prompts<br>through review.</h1><p style="font-size:22px;margin-top:32px">Open-source prompt review,<br>with the record attached.</p></div><div style="align-self:center;font-size:96px;letter-spacing:-.07em">8 → 8<br><span style="color:var(--pz-accent)">→ 9</span><p style="font-size:18px;letter-spacing:0;margin-top:24px;color:var(--pz-secondary)">One recorded run.<br>Model-assigned prompt scores.</p></div></main>`; }''')
        await page.evaluate('document.fonts.ready')
        await page.screenshot(path=Path(__file__).resolve().parents[1]/'ninthpass/assets/og.png')
        await browser.close()
    print('Rendered Ninth Pass social card, 1200 × 630.')

if __name__=='__main__': asyncio.run(main())
