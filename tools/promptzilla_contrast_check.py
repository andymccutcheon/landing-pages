"""Measure Ninth Pass text, interactive state and focus contrast in Chromium.

Text needs 4.5:1 (3:1 at 24px, or 18.66px bold and larger). Focus indicators and
the gate rule need 3:1. The page is light-only, so one pass covers it.
"""

import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_check import installed_chromium
from playwright.async_api import async_playwright

BASE = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
PAGE_URL = os.environ.get('LP_PROMPTZILLA_URL', BASE + 'promptzilla/')
RULES = ('.pz-loop__gate',)


async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=installed_chromium())
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto(PAGE_URL, wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        await page.evaluate('''() => {
          window.ratio = (a, b) => {
            const canvas = document.createElement('canvas');
            canvas.width = canvas.height = 1;
            const ctx = canvas.getContext('2d', { willReadFrequently: true });
            const luminance = (color) => {
              ctx.clearRect(0, 0, 1, 1);
              ctx.fillStyle = color;
              ctx.fillRect(0, 0, 1, 1);
              const rgb = [...ctx.getImageData(0, 0, 1, 1).data].slice(0, 3).map((value) => {
                value /= 255;
                return value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4;
              });
              return rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722;
            };
            const x = luminance(a);
            const y = luminance(b);
            return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
          };
          window.background = (element) => {
            while (element) {
              const color = getComputedStyle(element).backgroundColor;
              if (color !== 'rgba(0, 0, 0, 0)' && color !== 'transparent') return color;
              element = element.parentElement;
            }
            return 'rgb(245, 240, 230)';
          };
        }''')

        text = await page.evaluate('''() => [...document.querySelectorAll('body *')]
          .filter((element) => element.getBoundingClientRect().width
            && getComputedStyle(element).visibility !== 'hidden'
            && !element.closest('script, style, [aria-hidden="true"]')
            && [...element.childNodes].some((node) => node.nodeType === 3 && node.textContent.trim()))
          .map((element) => {
            const style = getComputedStyle(element);
            const size = parseFloat(style.fontSize);
            const weight = parseInt(style.fontWeight, 10) || 400;
            const large = size >= 24 || (size >= 18.66 && weight >= 700);
            const bg = window.background(element);
            return {
              tag: element.tagName.toLowerCase(),
              className: typeof element.className === 'string' ? element.className : '',
              text: element.textContent.trim().slice(0, 60),
              color: style.color,
              background: bg,
              size,
              weight,
              threshold: large ? 3 : 4.5,
              ratio: ratio(style.color, window.background(element)),
            };
          })''')
        failures = [entry for entry in text if entry['ratio'] < entry['threshold']]

        states = []
        await page.keyboard.press('Tab')
        await page.evaluate('document.activeElement.blur()')
        for element in await page.locator('a, button, summary').all():
            if not await element.is_visible():
                continue
            if await element.get_attribute('class') == 'pz-skip':
                continue
            await element.hover()
            await page.wait_for_timeout(420)
            states.append(await element.evaluate('''element => {
              const style = getComputedStyle(element);
              return { state: 'hover', text: element.textContent.trim().slice(0, 40), color: style.color, background: window.background(element), ratio: ratio(style.color, window.background(element)) };
            }'''))
            await element.focus()
            await page.wait_for_timeout(420)
            states.append(await element.evaluate('''element => {
              const style = getComputedStyle(element);
              return {
                state: 'focus',
                text: element.textContent.trim().slice(0, 40),
                color: style.color,
                background: window.background(element),
                ratio: ratio(style.color, window.background(element)),
                outline: style.outlineColor,
                focusRatio: ratio(style.outlineColor, window.background(element.parentElement)),
              };
            }'''))
        stateFailures = [entry for entry in states if entry['ratio'] < 4.5]
        focusFailures = [entry for entry in states if 'focusRatio' in entry and entry['focusRatio'] < 3]

        rules = await page.evaluate('''(selectors) => selectors.map((selector) => {
          const element = document.querySelector(selector);
          const color = getComputedStyle(element).borderInlineStartColor;
          return { selector, color, ratio: ratio(color, window.background(element.parentElement)) };
        })''', list(RULES))
        ruleFailures = [entry for entry in rules if entry['ratio'] < 3]

        results.append({
            'minText': min(entry['ratio'] for entry in text),
            'minState': min(entry['ratio'] for entry in states),
            'minFocus': min(entry['focusRatio'] for entry in states if 'focusRatio' in entry),
            'textFailures': failures,
            'stateFailures': stateFailures,
            'focusFailures': focusFailures,
            'rules': rules,
            'ruleFailures': ruleFailures,
        })
        await page.close()
        await browser.close()

    Path('.review/promptzilla').mkdir(parents=True, exist_ok=True)
    Path('.review/promptzilla/contrast.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))
    if any(result['textFailures'] or result['stateFailures'] or result['focusFailures'] or result['ruleFailures'] for result in results):
        raise SystemExit('Contrast check failed')


if __name__ == '__main__':
    asyncio.run(main())
