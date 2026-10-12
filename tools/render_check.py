#!/usr/bin/env python3
"""Render required views and enforce the Acheron landing-page layout contract."""

import asyncio
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = Path(os.environ.get("LP_SHOTS_DIR", ROOT / ".review/shots"))
URL = os.environ.get("LP_TEST_URL", "http://127.0.0.1:8766/acheron/")
GUIDE_URL = "https://andymccutcheon.github.io/acheron/guide.html"
WIDTHS = (360, 768, 1024, 1280, 1440, 1680)


def installed_chromium() -> str:
    cache = Path.home() / "Library/Caches/ms-playwright"
    candidates = sorted(cache.glob("chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"), reverse=True)
    if not candidates:
        raise SystemExit("No installed Playwright Chromium executable found")
    return os.fspath(candidates[0])


async def warm_page_for_capture(page, width: int) -> None:
    await page.evaluate("""async () => {
      const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      const step = Math.max(240, window.innerHeight - 64);
      const maxY = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
      for (let y = 0; y <= maxY; y += step) {
        window.scrollTo(0, y);
        await delay(100);
      }
      window.scrollTo(0, maxY);
      await delay(200);
      window.scrollTo(0, 0);
      await delay(100);
    }""")
    if width < 1280:
        return
    frames = page.locator(".lp-theatre__interactive")
    for index in range(await frames.count()):
        await frames.nth(index).scroll_into_view_if_needed()
    await page.evaluate("""() => new Promise((resolve) => {
      const visible = [...document.querySelectorAll('.lp-theatre__interactive')]
        .filter((element) => getComputedStyle(element).display !== 'none');
      if (!visible.length) return resolve();
      const hasContent = (frame) => {
        try {
          return new URL(frame.src).origin !== window.location.origin
            ? frame.classList.contains('is-loaded')
            : (frame.contentDocument?.body?.childElementCount ?? 0) > 0;
        } catch (error) {
          return false;
        }
      };
      const waitForFrame = (frame) => new Promise((done) => {
        const started = performance.now();
        const tick = () => {
          if (hasContent(frame)) {
            frame.classList.add('is-loaded');
            return done();
          }
          if (performance.now() - started > 12000) return done();
          window.setTimeout(tick, 50);
        };
        frame.addEventListener('load', tick, { once: true });
        tick();
      });
      Promise.all(visible.map(waitForFrame)).then(resolve);
    })""")


async def assert_theatre_iframes(page, theme: str, width: int, failures: list[str]) -> None:
    if width < 1280:
        return
    states = await page.evaluate("""() => [...document.querySelectorAll('.lp-theatre__interactive')]
      .filter((element) => getComputedStyle(element).display !== 'none')
      .map((frame) => {
        const stage = frame.closest('.lp-theatre__stage');
        const poster = stage ? getComputedStyle(stage).getPropertyValue('--lp-theatre-stage-poster').trim() : '';
        return {
          loaded: frame.classList.contains('is-loaded'),
          posterSet: poster.length > 0,
        };
      })""")
    prefix = f"{theme} {width}"
    if not states:
        failures.append(f"{prefix}: no visible theatre iframes at desktop width")
        return
    for frame in await page.locator('.lp-theatre__interactive:visible').all():
        await frame.content_frame.locator('body > *').first.wait_for(state='attached')
        content = await frame.content_frame.locator('body').evaluate('body => body.childElementCount')
        if content == 0:
            failures.append(f"{prefix}: theatre at {await frame.get_attribute('src')} has an empty body")
    for index, state in enumerate(states, start=1):
        if not state["posterSet"]:
            failures.append(f"{prefix}: theatre {index} missing stage poster")
        if not state["loaded"]:
            failures.append(f"{prefix}: theatre {index} iframe not loaded before capture")


async def layout_assertions(page, theme: str, width: int, failures: list[str], grid_audit: dict) -> None:
    if width == 1280:
        await page.locator('.lp-failure-heading').scroll_into_view_if_needed()
    result = await page.evaluate(
        """({width}) => {
          const root = getComputedStyle(document.documentElement);
          const ledgerGap = parseFloat(root.getPropertyValue('--ds-space-gap-inline'));
          // --lp-hero-still-small is 15rem (~240 CSS px): ~three content columns at 360.
          const readableProbe = document.createElement('div');
          readableProbe.style.inlineSize = root.getPropertyValue('--lp-hero-still-small');
          readableProbe.style.position = 'absolute';
          readableProbe.style.visibility = 'hidden';
          document.body.append(readableProbe);
          const readableMin = readableProbe.getBoundingClientRect().width;
          readableProbe.remove();
          const blockDisplays = new Set(['block', 'flex', 'grid', 'list-item']);
          const readableAllowlist = [
            { selector: '.lp-header__inner nav, .lp-header__inner nav *', reason: 'intrinsic navigation controls' },
            { selector: '.lp-skip, .lp-wordmark, .lp-theme, .lp-copy', reason: 'header chrome and copy controls' },
            { selector: '.lp-cta a, .lp-cta .lp-button', reason: 'hero call-to-action cluster' },
            { selector: '.lp-tools li', reason: 'brief-specified multi-column tool roster' },
            { selector: '.lp-footer__links li', reason: 'brief-specified two-column footer list' },
            { selector: '.lp-write-side, .lp-write-side *', reason: 'brief-specified three-column write-side aside' },
          ];
          const allowReason = element => readableAllowlist.find(entry => element.matches(entry.selector))?.reason || null;
          const readableTextSelectors = 'p, h1, h2, h3, .lp-lead, article, figcaption, summary, .lp-placeholder, .lp-evidence';
          const descriptor = element => {
            const section = element.closest('section, footer, header');
            const context = section?.id || section?.getAttribute('aria-labelledby') || section?.tagName.toLowerCase() || 'page';
            const name = element.id ? `#${element.id}` : `${element.tagName.toLowerCase()}${[...element.classList].map(value => `.${value}`).join('')}`;
            return `${context} ${name}`;
          };
          const narrowBlocks = [...document.querySelectorAll(readableTextSelectors)].flatMap(element => {
            if (element.closest('pre, code, button')) return [];
            const style = getComputedStyle(element);
            const rect = element.getBoundingClientRect();
            if (!blockDisplays.has(style.display) || style.visibility === 'hidden' || !element.innerText.trim() || rect.width >= readableMin - 0.01) return [];
            const reason = allowReason(element);
            return reason ? [] : [{ element: descriptor(element), width: rect.width }];
          });
          const narrowCode = [...document.querySelectorAll('pre.lp-code')].flatMap(element => {
            const width = element.getBoundingClientRect().width;
            return width < readableMin - 0.01 ? [{ element: descriptor(element), width }] : [];
          });
          const grids = [...document.querySelectorAll('body *')].filter(element => ['grid', 'inline-grid'].includes(getComputedStyle(element).display)).map((grid, index) => ({
            grid: `${index + 1}: ${descriptor(grid)}`,
            columns: getComputedStyle(grid).gridTemplateColumns.split(' ').length,
            children: [...grid.children].map(child => ({
              child: descriptor(child),
              start: getComputedStyle(child).gridColumnStart,
              end: getComputedStyle(child).gridColumnEnd,
              width: child.getBoundingClientRect().width,
              allow: allowReason(child),
            })),
          }));
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
            readableMin,
            narrowBlocks,
            narrowCode,
            grids,
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
    for item in result["narrowBlocks"]:
        failures.append(f"{prefix}: text block {item['element']} is {item['width']:.2f}px wide, below token threshold {result['readableMin']:.2f}px")
    for item in result["narrowCode"]:
        failures.append(f"{prefix}: code block {item['element']} is {item['width']:.2f}px wide, below token threshold {result['readableMin']:.2f}px")
    if theme == "light":
        grid_audit[str(width)] = result["grids"]
    if width in (1280, 1440, 1680):
        hero_right = await page.locator('.lp-hero__still').evaluate("element => element.getBoundingClientRect().right")
        if abs(hero_right - width) > 1:
            failures.append(f"{prefix}: hero still right edge {hero_right:.2f}px != viewport edge {width}px")
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

    for width in (360, 1280):
        page = await browser.new_page(viewport={"width": width, "height": 900})
        await page.goto(URL, wait_until="networkidle")
        overlaps = await page.evaluate("""() => [...document.querySelectorAll('.lp-terminal')].flatMap((terminal, index) => {
          const button = terminal.querySelector('.lp-copy').getBoundingClientRect();
          const pre = terminal.querySelector('pre');
          pre.scrollLeft = 0;
          const range = document.createRange();
          range.selectNodeContents(pre.querySelector('code'));
          const intersects = [...range.getClientRects()].some(rect =>
            rect.left < button.right && rect.right > button.left && rect.top < button.bottom && rect.bottom > button.top
          );
          return intersects ? [index + 1] : [];
        })""")
        if overlaps:
            failures.append(f"{width}: copy buttons overlap command glyphs in terminals {overlaps}")
        await page.close()

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
    grid_audit: dict = {}
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, executable_path=installed_chromium())
        for theme in ("light", "dark"):
            for width in WIDTHS:
                page = await browser.new_page(viewport={"width": width, "height": 900}, color_scheme=theme, reduced_motion="no-preference")
                await page.goto(URL, wait_until="networkidle")
                await page.evaluate("document.querySelectorAll('.lp-reveal').forEach(element => element.classList.add('is-visible'))")
                await warm_page_for_capture(page, width)
                await layout_assertions(page, theme, width, failures, grid_audit)
                await assert_theatre_iframes(page, theme, width, failures)
                await page.screenshot(path=OUT / f"acheron-{theme}-{width}.png", full_page=True)
                await page.close()
        await interactive_assertions(browser, failures)
        await resilience_assertions(browser, failures)
        if (ROOT / "freewhirr/index.html").exists():
            from freewhirr_render_check import run
            await run(browser, failures, warm_page_for_capture)
        if (ROOT / 'shipwatch/index.html').exists():
            from shipwatch_render_check import run as shipwatch_run
            await shipwatch_run(browser, failures, warm_page_for_capture)
        await browser.close()
    audit_path = OUT.parent / "grid-audit.json"
    audit_path.write_text(json.dumps(grid_audit, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit("Render check failed:\n- " + "\n- ".join(failures))
    print(f"Render check passed: {len(WIDTHS) * 2} screenshots, readable-width and grid audits, edge alignment, command clearance, responsive contract, ledger gaps, copy controls, keyboard scrolling, no-JS and reduced motion")
    print(f"Grid audit: {audit_path}")


if __name__ == "__main__":
    asyncio.run(main())
