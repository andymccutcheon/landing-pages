#!/usr/bin/env python3
"""Render required views and enforce the Acheron landing-page layout contract."""

import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".review/shots"
URL = "http://127.0.0.1:8766/acheron/"
GUIDE_URL = "https://andymccutcheon.github.io/acheron/guide.html"
WIDTHS = (360, 768, 1280, 1440)


def installed_chromium() -> str:
    cache = Path.home() / "Library/Caches/ms-playwright"
    candidates = sorted(cache.glob("chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"), reverse=True)
    if not candidates:
        raise SystemExit("No installed Playwright Chromium executable found")
    return os.fspath(candidates[0])


async def layout_assertions(page, theme: str, width: int, failures: list[str]) -> None:
    if width == 1280:
        await page.locator('.lp-failure-heading').scroll_into_view_if_needed()
    result = await page.evaluate(
        """({width}) => {
          const root = getComputedStyle(document.documentElement);
          const ledgerGap = parseFloat(root.getPropertyValue('--ds-space-gap-inline'));
          const textRect = (cell) => {
            const range = document.createRange();
            range.selectNodeContents(cell);
            return range.getBoundingClientRect();
          };
          const ledgerGaps = [...document.querySelectorAll('.lp-ledger tr')].flatMap(row => {
            const cells = [...row.cells];
            return cells.slice(1).map((cell, index) => textRect(cell).left - textRect(cells[index]).right);
          });
          const clippedCells = [...document.querySelectorAll('.lp-ledger th, .lp-ledger td')].filter(cell => {
            const rect = cell.getBoundingClientRect();
            let ancestor = cell.parentElement;
            while (ancestor && ancestor !== document.body) {
              const style = getComputedStyle(ancestor);
              const a = ancestor.getBoundingClientRect();
              const outside = rect.left < a.left || rect.right > a.right;
              if (outside && !['auto', 'scroll'].includes(style.overflowX)) return true;
              if (outside && ['auto', 'scroll'].includes(style.overflowX)) return false;
              ancestor = ancestor.parentElement;
            }
            return false;
          }).length;
          const result = {
            overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            ledgerGap: Math.min(...ledgerGaps),
            requiredLedgerGap: ledgerGap,
            clippedCells,
          };
          if (width === 1280) {
            const grid = document.querySelector('.lp-grid');
            const h1 = document.querySelector('h1');
            const probe = document.createElement('span');
            probe.style.fontSize = 'var(--ds-display-lg-size)';
            document.body.append(probe);
            const problems = [...document.querySelectorAll('.lp-problem')].map(el => el.getBoundingClientRect());
            const failureHeading = document.querySelector('.lp-failure-heading');
            const failure = failureHeading.getBoundingClientRect();
            const answerParagraphs = [...document.querySelectorAll('.lp-answers p')].map(el => el.getBoundingClientRect());
            const overlaps = answerParagraphs.filter(rect => !(failure.right <= rect.left || failure.left >= rect.right || failure.bottom <= rect.top || failure.top >= rect.bottom)).length;
            const cx = failure.left + failure.width / 2;
            const cy = failure.top + failure.height / 2;
            const topAtCenter = document.elementsFromPoint(cx, cy)[0];
            result.wide = {
              tracks: getComputedStyle(grid).gridTemplateColumns.split(' ').length,
              navVisible: getComputedStyle(document.querySelector('.lp-nav__anchors')).display !== 'none',
              h1Size: getComputedStyle(h1).fontSize,
              largeSize: getComputedStyle(probe).fontSize,
              problemsSideBySide: problems[0].right <= problems[1].left,
              secondProblemLower: problems[1].top > problems[0].top,
              failureOverlaps: overlaps,
              failureOwnsCenter: topAtCenter === failureHeading || failureHeading.contains(topAtCenter),
            };
            probe.remove();
          }
          return result;
        }""",
        {"width": width},
    )
    prefix = f"{theme} {width}"
    if result["overflow"]:
        failures.append(f"{prefix}: page overflow {result['scrollWidth']} > {result['clientWidth']}")
    if result["ledgerGap"] + 0.01 < result["requiredLedgerGap"]:
        failures.append(f"{prefix}: ledger text gap {result['ledgerGap']} < token gap {result['requiredLedgerGap']}")
    if result["clippedCells"]:
        failures.append(f"{prefix}: {result['clippedCells']} ledger cells clipped by non-scrolling ancestors")
    if width == 1280:
        wide = result["wide"]
        expected = {"tracks": 12, "navVisible": True, "problemsSideBySide": True, "secondProblemLower": True, "failureOverlaps": 0, "failureOwnsCenter": True}
        for key, value in expected.items():
            if wide[key] != value:
                failures.append(f"{prefix}: {key} was {wide[key]!r}, expected {value!r}")
        if wide["h1Size"] != wide["largeSize"]:
            failures.append(f"{prefix}: headline {wide['h1Size']} != large display token {wide['largeSize']}")


async def interactive_assertions(browser, failures: list[str]) -> None:
    context = await browser.new_context(viewport={"width": 360, "height": 740}, permissions=["clipboard-read", "clipboard-write"])
    page = await context.new_page()
    await page.goto(URL, wait_until="networkidle")
    for index, button in enumerate(await page.locator('[data-copy-target]').all()):
        await button.scroll_into_view_if_needed()
        try:
            await button.click(timeout=3000)
        except Exception as error:
            failures.append(f"copy button {index + 1}: pointer click intercepted: {error}")
            continue
        await page.wait_for_timeout(50)
        if await button.text_content() != "Copied":
            failures.append(f"copy button {index + 1}: success state was not Copied")
    for index, region in enumerate(await page.locator('.lp-scroll-region, .lp-code').all()):
        dimensions = await region.evaluate("el => ({scroll: el.scrollWidth, client: el.clientWidth})")
        if dimensions["scroll"] <= dimensions["client"]:
            continue
        await region.focus()
        before = await region.evaluate("el => el.scrollLeft")
        await region.press("ArrowRight")
        after = await region.evaluate("el => el.scrollLeft")
        if after <= before:
            failures.append(f"scroll region {index + 1}: ArrowRight did not move scrollLeft")
    await context.close()

    for width, height in ((360, 740), (1280, 800)):
        page = await browser.new_page(viewport={"width": width, "height": height})
        await page.goto(URL, wait_until="networkidle")
        cta = await page.locator('.lp-cta').bounding_box()
        if not cta or cta["y"] + cta["height"] > height:
            failures.append(f"hero CTA is outside first screen at {width}x{height}")
        await page.close()


async def resilience_assertions(browser, failures: list[str]) -> None:
    nojs = await browser.new_context(java_script_enabled=False, viewport={"width": 360, "height": 740})
    page = await nojs.new_page()
    await page.goto(URL, wait_until="domcontentloaded")
    visible = await page.locator('.lp-reveal:visible').count()
    total = await page.locator('.lp-reveal').count()
    if visible != total:
        failures.append(f"no-JS: {visible} of {total} reveal elements visible")
    hrefs = await page.locator('a', has_text="guide").evaluate_all("links => links.map(link => link.href)")
    if not hrefs or any(href != GUIDE_URL for href in hrefs):
        failures.append(f"no-JS: guide hrefs were {hrefs}")
    await nojs.close()

    fallback = await browser.new_page(viewport={"width": 360, "height": 740})
    await fallback.goto(URL, wait_until="networkidle")
    await fallback.evaluate("""() => {
      Object.defineProperty(navigator.clipboard, 'writeText', {
        configurable: true,
        value: () => Promise.reject(new Error('fixture')),
      });
    }""")
    fallback_button = fallback.locator('[data-copy-target]').first
    await fallback_button.scroll_into_view_if_needed()
    await fallback_button.click()
    await fallback.wait_for_timeout(50)
    fallback_state = await fallback.evaluate("""() => ({
      label: document.querySelector('[data-copy-target]').textContent,
      status: document.querySelector('#copy-status').textContent,
      selected: window.getSelection().toString().trim(),
      expected: document.querySelector('#benchmark-command').textContent.trim(),
    })""")
    if fallback_state["label"] != "Select command" or fallback_state["status"] != "Command selected for manual copy" or fallback_state["selected"] != fallback_state["expected"]:
        failures.append(f"clipboard fallback mismatch: {fallback_state}")
    await fallback.close()

    skip = await browser.new_page(viewport={"width": 360, "height": 740})
    await skip.goto(URL, wait_until="domcontentloaded")
    await skip.locator('.lp-skip').focus()
    await skip.locator('.lp-skip').press('Enter')
    if await skip.evaluate("document.activeElement.id") != "main":
        failures.append("skip link did not move focus to main")
    await skip.close()

    reduced = await browser.new_page(viewport={"width": 1280, "height": 800}, reduced_motion="reduce")
    await reduced.goto(URL, wait_until="networkidle")
    motion = await reduced.evaluate("""() => ({
      hidden: [...document.querySelectorAll('.lp-reveal')].some(el => getComputedStyle(el).opacity === '0'),
      revealDuration: getComputedStyle(document.querySelector('.lp-reveal')).transitionDuration,
      pressProperties: getComputedStyle(document.querySelector('.lp-press')).transitionProperty,
      pressTransform: getComputedStyle(document.querySelector('.lp-press')).transform,
    })""")
    if motion["hidden"] or motion["revealDuration"] != "0s" or "transform" in motion["pressProperties"] or motion["pressTransform"] != "none":
        failures.append(f"reduced motion mismatch: {motion}")
    await reduced.close()


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, executable_path=installed_chromium())
        for theme in ("light", "dark"):
            for width in WIDTHS:
                page = await browser.new_page(viewport={"width": width, "height": 900}, color_scheme=theme, reduced_motion="no-preference")
                await page.goto(URL, wait_until="networkidle")
                await page.evaluate("document.querySelectorAll('.lp-reveal').forEach(element => element.classList.add('is-visible'))")
                await layout_assertions(page, theme, width, failures)
                await page.screenshot(path=OUT / f"acheron-{theme}-{width}.png", full_page=True)
                await page.close()
        await interactive_assertions(browser, failures)
        await resilience_assertions(browser, failures)
        await browser.close()
    if failures:
        raise SystemExit("Render check failed:\n- " + "\n- ".join(failures))
    print("Render check passed: 8 screenshots, responsive contract, ledger gaps, copy controls, keyboard scrolling, no-JS and reduced motion")


if __name__ == "__main__":
    asyncio.run(main())
