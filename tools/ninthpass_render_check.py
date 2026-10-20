"""Ninth Pass responsive, interaction and resilience contract.

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
SECTIONS = 8
STAGES = 6
SKILLS = 0
TABS = 3
# The page embeds three diagrams: the run/data-flow view, the neural-arbor view of
# one pass, and the refinement loop.
DIAGRAMS = ['diagrams/arbor.html', 'diagrams/dataflow.html', 'diagrams/loop.html']
REPO_URL = 'https://github.com/andymccutcheon/ninthpass'
INSTALL_COMMAND = 'git clone https://github.com/andymccutcheon/ninthpass\ncd ninthpass && npm install && npm run build'
ASSETS = (
    'ninthpass/index.html',
    'ninthpass/css/fonts.css',
    'ninthpass/css/pz-tokens.css',
    'ninthpass/css/ninthpass.css',
    'ninthpass/js/page.js',
    'ninthpass/diagrams/loop.html',
    'ninthpass/diagrams/dataflow.html',
    'ninthpass/assets/favicon.svg',
    'ninthpass/assets/fonts/fraunces-normal.woff2',
    'ninthpass/assets/fonts/fraunces-italic.woff2',
    'ninthpass/assets/fonts/geist.woff2',
    'ninthpass/assets/fonts/geist-mono.woff2',
)
# The page is small: HTML, three stylesheets, one script, the favicon and four
# Latin-subset WOFF2 files. The budget leaves room for copy edits, not a redesign.
GZIP_BUDGET = 240000
# The rubric has twelve sections; the standard section renders one row each.
RUBRIC_SECTIONS = 12


async def run(browser, failures, warm):
    out = ROOT / '.review/ninthpass'
    out.mkdir(parents=True, exist_ok=True)
    base = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
    url = os.environ.get('LP_NINTHPASS_URL', base + 'ninthpass/')
    measurements = []

    for width in WIDTHS:
        page = await browser.new_page(viewport={'width': width, 'height': HEIGHT})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(f'console {message.type}: {message.text}') if message.type == 'error' else None)
        await page.goto(url, wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        await page.wait_for_timeout(1200)
        label = f'Ninth Pass {width}'
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
            media: document.querySelectorAll('video, img').length,
            iframes: [...document.querySelectorAll('iframe')].map(frame => frame.getAttribute('src')),
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
            files: document.querySelectorAll('.pz-file').length,
            rubric: document.querySelectorAll('.pz-standard__row').length,
            standard: [...document.querySelectorAll('.pz-standard__row')].map(row => row.querySelector('.pz-standard__name').textContent + ' ' + row.querySelector('.pz-standard__score').textContent),
            scorecard: [...document.querySelectorAll('.pz-file code')].map(code => code.textContent).join(String.fromCharCode(10)),
            runId: (document.body.textContent.match(new RegExp('runs/[0-9a-f-]{36}/')) || [''])[0],
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
        if state['marks'] != 2 or state['media'] or sorted(state['iframes']) != DIAGRAMS:
            failures.append(f'{label}: wordmark/media {state}')
        if state['scheme'] != 'light':
            failures.append(f'{label}: colour scheme {state["scheme"]}')
        if len(state['primaryCtas']) != 2 or any(href != REPO_URL for href in state['primaryCtas']):
            failures.append(f'{label}: primary calls to action {state["primaryCtas"]}')
        if state['smallTargets']:
            failures.append(f'{label}: small targets {state["smallTargets"]}')
        if state['files'] != 2:
            failures.append(f'{label}: artifact cards {state["files"]}')
        if state['rubric'] != RUBRIC_SECTIONS:
            failures.append(f'{label}: the standard shows {state["rubric"]} sections, not {RUBRIC_SECTIONS}')
        if not state['standard'] or not state['standard'][0].startswith('Primary Role'):
            failures.append(f'{label}: the standard does not start at Primary Role')
        if not state['runId']:
            failures.append(f'{label}: no run identifier in the output directory listing')
        if state['loopScore'] != '08' or 'CONTINUE' not in state['loopStatus']:
            failures.append(f'{label}: loop did not start at 08/CONTINUE {state["loopScore"]} {state["loopStatus"]}')
        if state['loopStates'] != ['done', 'active'] + ['pending'] * (STAGES - 2):
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
        await page.screenshot(path=out / f'ninthpass-{width}.png', full_page=True)
        await page.evaluate("document.querySelector('.pz-header').style.removeProperty('position')")
        measurements.append({'view': label, **state})

        await page.evaluate("""() => {
          document.querySelector('#install-hero').textContent = 'x'.repeat(140);
          document.querySelector('.pz-standard__name').textContent = 'x'.repeat(60);
        }""")
        if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
            failures.append(f'{label}: long-string overflow')
        await page.close()

    await check_diagrams(browser, url, failures)
    await check_loop_and_tabs(browser, url, failures)
    await check_no_javascript(browser, url, failures)
    await check_copy_and_keyboard(browser, url, failures)
    await check_reduced_motion(browser, url, failures)

    sizes = {name: len(gzip.compress((ROOT / name).read_bytes())) for name in ASSETS}
    if sum(sizes.values()) > GZIP_BUDGET:
        failures.append(f'Ninth Pass budget {sum(sizes.values())} > {GZIP_BUDGET}: {sizes}')
    (out / 'results.json').write_text(json.dumps({'views': measurements, 'gzip': sizes}, indent=2) + '\n', encoding='utf-8')
    print(f'Ninth Pass: {len(WIDTHS)} captures, no-JavaScript, loop, tabs, clipboard, keyboard, reduced-motion and boundary checks; gzip {sum(sizes.values())} of {GZIP_BUDGET} bytes.')


async def check_diagrams(browser, url, failures):
    """Both standalone diagrams must show a complete frame with no motion, step on demand,
    reach the end on their own, and log nothing."""
    base = url.rstrip('/') + '/diagrams/'
    for name in ('loop.html', 'dataflow.html'):
        target = base + name
        page = await browser.new_page(viewport={'width': 1280, 'height': 900})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(f'console {message.type}: {message.text}') if message.type == 'error' else None)

        # The static frame is complete and the controls are hidden.
        await page.goto(target + '?motion=static', wait_until='networkidle')
        hidden = await page.eval_on_selector_all('[data-motion-item]', "els => els.filter(e => getComputedStyle(e).opacity !== '1').length")
        if hidden:
            failures.append(f'Ninth Pass diagram {name}: {hidden} items hidden in the static frame')
        controls = await page.eval_on_selector('[data-motion-controls]', "e => getComputedStyle(e).display")
        if controls != 'none':
            failures.append(f'Ninth Pass diagram {name}: the static frame shows the controls')

        # A single step reveals part of the diagram, not all of it.
        await page.goto(target + '?motion=step&step=1', wait_until='networkidle')
        visible = await page.eval_on_selector_all('[data-motion-item]', "els => els.filter(e => e.classList.contains('is-visible')).length")
        total = await page.eval_on_selector_all('[data-motion-item]', "els => els.length")
        if not 0 < visible < total:
            failures.append(f'Ninth Pass diagram {name}: step 1 shows {visible} of {total} items')

        # Reduced motion lands on the complete static frame with no controls.
        quiet = await browser.new_page(viewport={'width': 1280, 'height': 900}, reduced_motion='reduce')
        await quiet.goto(target, wait_until='networkidle')
        await quiet.wait_for_timeout(600)
        hidden = await quiet.eval_on_selector_all('[data-motion-item]', "els => els.filter(e => getComputedStyle(e).opacity !== '1').length")
        if hidden:
            failures.append(f'Ninth Pass diagram {name}: reduced motion hides {hidden} items')
        controls = await quiet.eval_on_selector('[data-motion-controls]', "e => getComputedStyle(e).display")
        if controls != 'none':
            failures.append(f'Ninth Pass diagram {name}: reduced motion shows the controls')
        await quiet.close()

        # The autoplay reaches the end on its own.
        await page.goto(target, wait_until='networkidle')
        await page.wait_for_timeout(5400)
        frame = await page.eval_on_selector('[data-motion-root]', "e => e.dataset.frame")
        if frame != 'end':
            failures.append(f'Ninth Pass diagram {name}: the autoplay ended in frame {frame}')

        failures.extend(f'Ninth Pass diagram {name}: {error}' for error in errors)
        await page.close()


async def check_loop_and_tabs(browser, url, failures):
    page = await browser.new_page(viewport={'width': 1280, 'height': 900})
    await page.goto(url, wait_until='networkidle')
    await page.locator('#loop').scroll_into_view_if_needed()
    await page.locator('[data-loop-run]').click()
    await page.wait_for_timeout(5200)
    state = await page.evaluate('''() => ({
      score: document.querySelector('[data-loop-score]').textContent,
      status: document.querySelector('[data-loop-status]').textContent,
      states: [...document.querySelectorAll('[data-loop-stage]')].map(stage => stage.dataset.state),
      progress: getComputedStyle(document.querySelector('[data-loop-track]')).getPropertyValue('--progress').trim(),
      button: document.querySelector('[data-loop-run]').textContent,
    })''')
    if state['score'] != '09' or state['status'] != 'STOP / gate passed' or state['states'] != ['done'] * STAGES or state['progress'] != '1':
        failures.append(f'Ninth Pass loop interaction {state}')
    if state['button'] != 'Replay again':
        failures.append(f'Ninth Pass loop button {state["button"]}')

    for tab, panel in (('#tab-claude', '#panel-claude'), ('#tab-codex', '#panel-codex'), ('#tab-opencode', '#panel-opencode')):
        await page.locator(tab).click()
        if not await page.locator(panel).is_visible():
            failures.append(f'Ninth Pass tab {tab} did not open')
    await page.locator('#tab-opencode').focus()
    await page.keyboard.press('ArrowRight')
    if await page.evaluate('document.activeElement.id') != 'tab-claude':
        failures.append('Ninth Pass tab keyboard arrow')
    await page.keyboard.press('End')
    if await page.evaluate('document.activeElement.id') != 'tab-codex':
        failures.append('Ninth Pass tab keyboard End')
    await page.keyboard.press('Home')
    if await page.evaluate('document.activeElement.id') != 'tab-opencode':
        failures.append('Ninth Pass tab keyboard Home')
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
    expected = {'buttons': 0, 'panels': 3, 'scheme': 'light', 'overflow': False, 'command': INSTALL_COMMAND, 'score': '09', 'status': 'STOP / gate passed', 'states': ['done'] * STAGES}
    if state != expected:
        failures.append(f'Ninth Pass no-JS: {state}')
    await page.screenshot(path=ROOT / '.review/ninthpass/ninthpass-nojs-360.png', full_page=True)
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
            failures.append(f'Ninth Pass clipboard {target}')
    await page.locator('.pz-skip').focus()
    await page.locator('.pz-skip').press('Enter')
    if await page.evaluate('document.activeElement.id') != 'main':
        failures.append('Ninth Pass skip focus')
    await page.evaluate("() => {navigator.clipboard.writeText = () => Promise.reject(new Error('fixture'));}")
    await page.locator('[data-copy-target]:visible').first.click()
    await page.wait_for_timeout(50)
    if await page.evaluate('window.getSelection().toString().trim()') != INSTALL_COMMAND:
        failures.append('Ninth Pass manual-copy fallback')
    for region in await page.locator('.pz-code').all():
        if await region.evaluate('element => element.scrollWidth > element.clientWidth'):
            await region.focus()
            await region.press('ArrowRight')
            if await region.evaluate('element => element.scrollLeft') <= 0:
                failures.append('Ninth Pass keyboard code scrolling')
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
    if state['score'] != '09' or state['status'] != 'STOP / gate passed' or state['states'] != ['done'] * STAGES:
        failures.append(f'Ninth Pass reduced-motion loop {state}')
    if state['heroAnimations'] or state['stageAnimations']:
        failures.append(f'Ninth Pass reduced-motion animations {state}')
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
