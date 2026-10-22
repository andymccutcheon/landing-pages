#!/usr/bin/env python3
"""Capture the Silverquill baseline at the three widths the directive names.

The directive asks for baseline screenshots at 1440x900, 1024x768 and 390x844
with a written recon record. This captures, per width: the first screen, the
change ledger, and the whole page, and writes a machine-readable summary so
the written record can quote measurements rather than impressions.

    PATH="$PWD/.venv/bin:$PATH" python3 tools/capture_silverquill_baseline.py
"""
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_check import installed_chromium
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.review/silverquill-baseline'
PAGE_URL = os.environ.get('LP_NINTHPASS_URL', 'http://127.0.0.1:8766/ninthpass/')
# The three widths the directive names, with their exact viewports.
VIEWPORTS = ((1440, 900), (1024, 768), (390, 844))
SECTIONS = ('hero', 'the-diff', 'how-it-works', 'start')


async def capture(browser, width, height):
    page = await browser.new_page(viewport={'width': width, 'height': height})
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
    await page.goto(PAGE_URL, wait_until='networkidle')
    await page.evaluate('document.fonts.ready')
    # Freeze motion so the capture is of a settled page, not a moving one.
    await page.locator('[data-motion-toggle]').click()
    await page.evaluate('window.scrollTo(0,0)')
    await page.wait_for_timeout(400)

    measured = await page.evaluate('''() => ({
      width: innerWidth,
      height: innerHeight,
      scrollWidth: document.documentElement.scrollWidth,
      scrollHeight: document.documentElement.scrollHeight,
      sections: document.querySelectorAll('main > section').length,
      h1: document.querySelectorAll('h1').length,
      headlineLines: Number((document.querySelector('h1').clientHeight / parseFloat(getComputedStyle(document.querySelector('h1')).lineHeight)).toFixed(2)),
      heroLines: [...document.querySelectorAll('.hero-line')].length,
      iframes: document.querySelectorAll('iframe').length,
      primaryActions: [...document.querySelectorAll('.primary')].map(a => a.getAttribute('href')),
      fontsLoaded: ['Geist', 'Fraunces', 'Geist Mono'].every(f => document.fonts.check(`16px "${f}"`)),
      undersizedTargets: [...document.querySelectorAll('a,button')].filter(e => {
        const r = e.getBoundingClientRect();
        return r.width && (r.width < 24 || r.height < 24);
      }).map(e => e.textContent.trim().slice(0, 40)),
      scorecards: document.querySelectorAll('.score-panel').length,
      ledgerBlocks: document.querySelectorAll('#the-diff .change').length,
    })''')

    failures = []
    if measured['scrollWidth'] > width:
        failures.append(f'{width}: horizontal overflow {measured["scrollWidth"]}')
    if measured['sections'] != 8:
        failures.append(f'{width}: expected 8 sections, found {measured["sections"]}')
    if measured['h1'] != 1:
        failures.append(f'{width}: expected one h1, found {measured["h1"]}')
    if measured['headlineLines'] > 2.1:
        failures.append(f'{width}: headline wraps to {measured["headlineLines"]} lines')
    if measured['iframes'] != 2:
        failures.append(f'{width}: expected 2 diagrams, found {measured["iframes"]}')
    if not measured['fontsLoaded']:
        failures.append(f'{width}: a loaded face is missing')
    if measured['undersizedTargets']:
        failures.append(f'{width}: undersized targets {measured["undersizedTargets"]}')
    if measured['scorecards'] != 2:
        failures.append(f'{width}: expected 2 scorecards, found {measured["scorecards"]}')
    if errors:
        failures.append(f'{width}: console errors {errors}')

    await page.screenshot(path=OUT / f'{width}-hero.png')
    await page.screenshot(path=OUT / f'{width}-full.png', full_page=True)
    for name in SECTIONS:
        element = page.locator(f'#{name}') if name != 'hero' else page.locator('.site-header')
        if name == 'hero':
            continue
        if await element.count() == 0:
            failures.append(f'{width}: section #{name} is missing')
            continue
        await element.scroll_into_view_if_needed()
        await page.wait_for_timeout(200)
        await element.screenshot(path=OUT / f'{width}-{name}.png')
    await page.close()
    return {'viewport': f'{width}x{height}', 'measured': measured, 'errors': errors, 'failures': failures}


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    failures = []
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=installed_chromium())
        for width, height in VIEWPORTS:
            result = await capture(browser, width, height)
            results.append(result)
            failures.extend(result['failures'])
            print(f'captured {width}x{height}')
        await browser.close()
    (OUT / 'baseline.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'Wrote {OUT}/baseline.json')
    if failures:
        print('\n'.join(failures))
        raise SystemExit('Baseline capture failed')
    print('Baseline capture passed')


if __name__ == '__main__':
    asyncio.run(main())
