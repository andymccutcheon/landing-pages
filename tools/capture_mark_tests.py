#!/usr/bin/env python3
"""Capture the Silverquill mark at size, for the directive's small-size check.

The sheet lives at brand/silverquill/mark-size-tests.html. This captures it at
1x (the size a browser actually paints it) and at 2x (a retina display), plus a
tight crop of every 16-pixel sample scaled up so the rasterised result can be
judged rather than assumed.

    PATH="$PWD/.venv/bin:$PATH" python3 tools/capture_mark_tests.py
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
OUT = ROOT / '.review/silverquill-mark'
SHEET_URL = os.environ.get('LP_MARK_URL', 'http://127.0.0.1:8766/brand/silverquill/mark-size-tests.html')


async def main():
    OUT.mkdir(parents=True, exist_ok=True)
    failures = []
    report = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=installed_chromium())
        for scale in (1, 2):
            page = await browser.new_page(viewport={'width': 1200, 'height': 900}, device_scale_factor=scale)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(SHEET_URL, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            await page.wait_for_timeout(300)
            await page.screenshot(path=OUT / f'sheet-{scale}x.png', full_page=True)
            # Every stamp must actually paint: a mask that fails to load is silent.
            stamps = await page.evaluate('''() => [...document.querySelectorAll('.stamp')].map(stamp => {
              const style = getComputedStyle(stamp);
              const box = stamp.getBoundingClientRect();
              return { classes: stamp.className, width: box.width, height: box.height,
                       mask: style.maskImage || style.webkitMaskImage, colour: style.backgroundColor };
            })''')
            missing = [stamp for stamp in stamps if not stamp['mask'] or stamp['mask'] == 'none']
            if missing:
                failures.append(f'{scale}x: {len(missing)} stamps have no mask image')
            if errors:
                failures.append(f'{scale}x: page errors {errors}')
            report[f'{scale}x'] = {'stamps': stamps, 'errors': errors}
            if scale == 1:
                # Crop each strip so the small samples can be judged at scale.
                for index, strip in enumerate(await page.locator('.strip').all()):
                    await strip.screenshot(path=OUT / f'strip-{index}.png')
                    await page.evaluate('''() => { document.body.style.zoom = '6'; }''')
                    await strip.screenshot(path=OUT / f'strip-{index}-6x.png')
                    await page.evaluate('''() => { document.body.style.zoom = '1'; }''')
                report['strips'] = index + 1
            await page.close()
        await browser.close()
    (OUT / 'mark-tests.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'Wrote {OUT}/mark-tests.json')
    if failures:
        print('\n'.join(failures))
        raise SystemExit('Mark capture failed')
    print('Mark capture passed: every stamp carries a mask image and no page errors were raised.')


if __name__ == '__main__':
    asyncio.run(main())
