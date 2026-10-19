"""Promptzilla responsive, interaction and resilience contract.

The page is light-only. It is captured at six widths, then checked for the
structure, the install command above the fold, the loop interaction, the worker
tabs, copy and keyboard behaviour, no-JavaScript readability and reduced motion.
"""

import gzip
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (360, 480, 768, 1024, 1280, 1440)
HEIGHT = 900
SECTIONS = 7
STAGES = 4
SKILLS = 5
TABS = 3
REPO_URL = 'https://github.com/andymccutcheon/promptzilla'
INSTALL_COMMAND = 'npx promptzilla install'
ASSETS = (
    'promptzilla/index.html',
    'promptzilla/css/fonts.css',
    'promptzilla/css/pz-tokens.css',
    'promptzilla/css/promptzilla.css',
    'promptzilla/js/page.js',
    'promptzilla/assets/favicon.svg',
    'promptzilla/assets/fonts/instrument-serif-regular.woff2',
    'promptzilla/assets/fonts/instrument-serif-italic.woff2',
    'promptzilla/assets/fonts/geist.woff2',
    'promptzilla/assets/fonts/geist-mono.woff2',
)
# The page is small: HTML, three stylesheets, one script, the favicon and four
# Latin-subset WOFF2 files. The budget leaves room for copy edits, not a redesign.
GZIP_BUDGET = 150000


async def run(browser, failures, warm):
    out = ROOT / '.review/promptzilla'
    out.mkdir(parents=True, exist_ok=True)
    base = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
    url = os.environ.get('LP_PROMPTZILLA_URL', base + 'promptzilla/')
    measurements = []

    for width in WIDTHS:
        page = await browser.new_page(viewport={'width': width, 'height': HEIGHT})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(f'console {message.type}: {message.text}') if message.type == 'error' else None)
        await page.goto(url, wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        await page.wait_for_timeout(1200)
        label = f'Promptzilla {width}'
        state = await page.evaluate('''() => {
          const box = selector => document.querySelector(selector).getBoundingClientRect().toJSON();
          const heading = document.querySelector('h1');
          const panels = [...document.querySelectorAll('.pz-tab-panel')].map(panel => getComputedStyle(panel).display);
          return {
            overflow: document.documentElement.scrollWidth > innerWidth,
            sections: document.querySelectorAll('main > section').length,
            h1: document.querySelectorAll('h1').length,
            lines: heading.clientHeight / parseFloat(getComputedStyle(heading).lineHeight),
            stages: document.querySelectorAll('[data-loop-stage]').length,
            skills: document.querySelectorAll('.pz-skill').length,
            tabs: document.querySelectorAll('[role="tab"]').length,
            panels,
            marks: document.querySelectorAll('.pz-mark').length,
            media: document.querySelectorAll('iframe, video, img').length,
            primaryCtas: [...document.querySelectorAll('.pz-primary')].map(link => link.href),
            smallTargets: [...document.querySelectorAll('a, button, summary')]
              .filter(element => { const rect = element.getBoundingClientRect(); return rect.width && (rect.width < 24 || rect.height < 24); })
              .map(element => element.textContent.trim().slice(0, 40)),
            scheme: getComputedStyle(document.documentElement).colorScheme,
            loopScore: document.querySelector('[data-loop-score]').textContent,
            loopStatus: document.querySelector('[data-loop-status]').textContent,
            loopStates: [...document.querySelectorAll('[data-loop-stage]')].map(stage => stage.dataset.state),
            install: box('#install-hero'),
            boundaries: getComputedStyle(document.querySelector('.pz-boundaries__list')).gridTemplateColumns,
          };
        }''')
        if state['overflow'] or state['sections'] != SECTIONS or state['h1'] != 1:
            failures.append(f'{label}: structure/overflow {state}')
        if state['lines'] > 3.25:
            failures.append(f'{label}: headline wraps to {state["lines"]:.2f} lines')
        if state['stages'] != STAGES or state['skills'] != SKILLS or state['tabs'] != TABS:
            failures.append(f'{label}: component counts {state}')
        if state['panels'] != ['grid', 'none', 'none']:
            failures.append(f'{label}: worker tabs start open {state["panels"]}')
        if state['marks'] != 2 or state['media']:
            failures.append(f'{label}: wordmark/media {state}')
        if state['scheme'] != 'light':
            failures.append(f'{label}: colour scheme {state["scheme"]}')
        if len(state['primaryCtas']) != 2 or any(href != REPO_URL for href in state['primaryCtas']):
            failures.append(f'{label}: primary calls to action {state["primaryCtas"]}')
        if state['smallTargets']:
            failures.append(f'{label}: small targets {state["smallTargets"]}')
        if state['loopScore'] != '08' or 'CONTINUE' not in state['loopStatus']:
            failures.append(f'{label}: loop did not start at 08/CONTINUE {state["loopScore"]} {state["loopStatus"]}')
        if state['loopStates'] != ['active', 'pending', 'pending', 'pending']:
            failures.append(f'{label}: loop stage start state {state["loopStates"]}')
        if width == 360 and state['install']['bottom'] > HEIGHT:
            failures.append(f'{label}: install bar below the first screen {state["install"]}')
        if width < 768 and state['boundaries'].count(' ') > 0:
            failures.append(f'{label}: boundaries did not stack {state["boundaries"]}')
        if width >= 1024 and state['boundaries'].count(' ') != 1:
            failures.append(f'{label}: boundaries did not use two columns {state["boundaries"]}')
        failures.extend(f'{label}: {error}' for error in errors)

        await warm(page, width)
        # A sticky header appears at the scroll position in a stitched full-page capture;
        # pin it to the top for the screenshot, then restore it.
        await page.evaluate("document.querySelector('.pz-header').style.position = 'static'")
        await page.screenshot(path=out / f'promptzilla-{width}.png', full_page=True)
        await page.evaluate("document.querySelector('.pz-header').style.removeProperty('position')")
        measurements.append({'view': label, **state})

        await page.evaluate("""() => {
          document.querySelector('#install-hero').textContent = 'x'.repeat(140);
          document.querySelector('.pz-skill h3').textContent = 'x'.repeat(60);
        }""")
        if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
            failures.append(f'{label}: long-string overflow')
        await page.close()

    await check_loop_and_tabs(browser, url, failures)
    await check_no_javascript(browser, url, failures)
    await check_copy_and_keyboard(browser, url, failures)
    await check_reduced_motion(browser, url, failures)

    sizes = {name: len(gzip.compress((ROOT / name).read_bytes())) for name in ASSETS}
    if sum(sizes.values()) > GZIP_BUDGET:
        failures.append(f'Promptzilla budget {sum(sizes.values())} > {GZIP_BUDGET}: {sizes}')
    (out / 'results.json').write_text(json.dumps({'views': measurements, 'gzip': sizes}, indent=2) + '\n', encoding='utf-8')
    print(f'Promptzilla: {len(WIDTHS)} captures, no-JavaScript, loop, tabs, clipboard, keyboard, reduced-motion and boundary checks; gzip {sum(sizes.values())} of {GZIP_BUDGET} bytes.')


async def check_loop_and_tabs(browser, url, failures):
    page = await browser.new_page(viewport={'width': 1280, 'height': 900})
    await page.goto(url, wait_until='networkidle')
    await page.locator('#loop').scroll_into_view_if_needed()
    await page.locator('[data-loop-run]').click()
    await page.wait_for_timeout(3200)
    state = await page.evaluate('''() => ({
      score: document.querySelector('[data-loop-score]').textContent,
      status: document.querySelector('[data-loop-status]').textContent,
      states: [...document.querySelectorAll('[data-loop-stage]')].map(stage => stage.dataset.state),
      progress: getComputedStyle(document.querySelector('[data-loop-track]')).getPropertyValue('--progress').trim(),
      button: document.querySelector('[data-loop-run]').textContent,
    })''')
    if state['score'] != '09' or state['status'] != 'STOP / approved' or state['states'] != ['done'] * STAGES or state['progress'] != '1':
        failures.append(f'Promptzilla loop interaction {state}')
    if state['button'] != 'Run again':
        failures.append(f'Promptzilla loop button {state["button"]}')

    for tab, panel in (('#tab-claude', '#panel-claude'), ('#tab-codex', '#panel-codex'), ('#tab-opencode', '#panel-opencode')):
        await page.locator(tab).click()
        if not await page.locator(panel).is_visible():
            failures.append(f'Promptzilla tab {tab} did not open')
    await page.locator('#tab-opencode').focus()
    await page.keyboard.press('ArrowRight')
    if await page.evaluate('document.activeElement.id') != 'tab-claude':
        failures.append('Promptzilla tab keyboard arrow')
    await page.keyboard.press('End')
    if await page.evaluate('document.activeElement.id') != 'tab-codex':
        failures.append('Promptzilla tab keyboard End')
    await page.keyboard.press('Home')
    if await page.evaluate('document.activeElement.id') != 'tab-opencode':
        failures.append('Promptzilla tab keyboard Home')
    await page.close()


async def check_no_javascript(browser, url, failures):
    context = await browser.new_context(java_script_enabled=False, viewport={'width': 360, 'height': HEIGHT})
    page = await context.new_page()
    await page.goto(url, wait_until='networkidle')
    state = await page.evaluate('''() => ({
      buttons: [...document.querySelectorAll('button')].filter(element => element.getClientRects().length > 0).length,
      panels: [...document.querySelectorAll('.pz-tab-panel')].filter(panel => getComputedStyle(panel).display !== 'none').length,
      scheme: getComputedStyle(document.documentElement).colorScheme,
      overflow: document.documentElement.scrollWidth > innerWidth,
      command: document.querySelector('#install-hero').textContent.trim(),
      score: document.querySelector('[data-loop-score]').textContent,
      status: document.querySelector('[data-loop-status]').textContent,
      states: [...document.querySelectorAll('[data-loop-stage]')].map(stage => stage.dataset.state),
    })''')
    expected = {'buttons': 0, 'panels': 3, 'scheme': 'light', 'overflow': False, 'command': INSTALL_COMMAND, 'score': '09', 'status': 'STOP / approved', 'states': ['done'] * STAGES}
    if state != expected:
        failures.append(f'Promptzilla no-JS: {state}')
    await page.screenshot(path=ROOT / '.review/promptzilla/promptzilla-nojs-360.png', full_page=True)
    await context.close()


async def check_copy_and_keyboard(browser, url, failures):
    context = await browser.new_context(viewport={'width': 1280, 'height': 900}, permissions=['clipboard-read', 'clipboard-write'])
    page = await context.new_page()
    await page.goto(url, wait_until='networkidle')
    for button in await page.locator('[data-copy-target]:visible').all():
        target = await button.get_attribute('data-copy-target')
        expected = (await page.locator('#' + target).text_content()).strip()
        await button.scroll_into_view_if_needed()
        await button.click()
        await page.wait_for_timeout(50)
        if await button.text_content() != 'Copied' or await page.evaluate('navigator.clipboard.readText()') != expected:
            failures.append(f'Promptzilla clipboard {target}')
    await page.locator('.pz-skip').focus()
    await page.locator('.pz-skip').press('Enter')
    if await page.evaluate('document.activeElement.id') != 'main':
        failures.append('Promptzilla skip focus')
    await page.evaluate("() => {navigator.clipboard.writeText = () => Promise.reject(new Error('fixture'));}")
    await page.locator('[data-copy-target]:visible').first.click()
    await page.wait_for_timeout(50)
    if await page.evaluate('window.getSelection().toString().trim()') != INSTALL_COMMAND:
        failures.append('Promptzilla manual-copy fallback')
    for region in await page.locator('.pz-code').all():
        if await region.evaluate('element => element.scrollWidth > element.clientWidth'):
            await region.focus()
            await region.press('ArrowRight')
            if await region.evaluate('element => element.scrollLeft') <= 0:
                failures.append('Promptzilla keyboard code scrolling')
    await context.close()


async def check_reduced_motion(browser, url, failures):
    page = await browser.new_page(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
    await page.goto(url, wait_until='networkidle')
    state = await page.evaluate('''() => ({
      score: document.querySelector('[data-loop-score]').textContent,
      status: document.querySelector('[data-loop-status]').textContent,
      states: [...document.querySelectorAll('[data-loop-stage]')].map(stage => stage.dataset.state),
      heroAnimations: document.querySelector('.pz-hero__copy').getAnimations().length,
      stageAnimations: [...document.querySelectorAll('[data-loop-stage]')].reduce((total, stage) => total + stage.getAnimations().length, 0),
    })''')
    if state['score'] != '09' or state['status'] != 'STOP / approved' or state['states'] != ['done'] * STAGES:
        failures.append(f'Promptzilla reduced-motion loop {state}')
    if state['heroAnimations'] or state['stageAnimations']:
        failures.append(f'Promptzilla reduced-motion animations {state}')
    await page.close()


if __name__ == '__main__':
    import asyncio
    from render_check import installed_chromium, warm_page_for_capture
    from playwright.async_api import async_playwright

    async def main():
        failures = []
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(executable_path=installed_chromium())
            await run(browser, failures, warm_page_for_capture)
            await browser.close()
        if failures:
            raise SystemExit('Render check failed:\n- ' + '\n- '.join(failures))

    asyncio.run(main())
