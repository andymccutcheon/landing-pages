"""Promptzilla responsive, interaction and resilience contract."""
import gzip
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (360, 480, 768, 1024, 1280, 1440)
SECTIONS = 8
RAIL_STAGES = 4
INSTALL_COMMAND = 'claude mcp add promptzilla -- npx -y promptzilla'
REPO_URL = 'https://github.com/andymccutcheon/promptzilla'
ASSETS = (
    'promptzilla/index.html',
    'promptzilla/css/promptzilla.css',
    'promptzilla/assets/favicon.svg',
    'vendor/pattern/generated/tokens.css',
    'shared/fonts.css',
    'shared/lp-tokens.css',
    'shared/base.css',
    'shared/motion.css',
    'shared/common.css',
    'shared/page.js',
)
GZIP_BUDGET = 350000


async def run(browser, failures, warm):
    out = ROOT / '.review/promptzilla'
    out.mkdir(parents=True, exist_ok=True)
    base = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
    url = base + 'promptzilla/'
    measurements = []
    for theme in ('light', 'dark'):
        for width in WIDTHS:
            page = await browser.new_page(viewport={'width': width, 'height': 900}, color_scheme=theme)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('console', lambda message: errors.append(f'console {message.type}: {message.text}') if message.type == 'error' else None)
            await page.goto(url, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            state = await page.evaluate('''() => {
              const box = selector => document.querySelector(selector).getBoundingClientRect().toJSON();
              const heading = document.querySelector('h1');
              return {
                overflow: document.documentElement.scrollWidth > innerWidth,
                sections: document.querySelectorAll('main > section').length,
                h1: document.querySelectorAll('h1').length,
                lines: heading.clientHeight / parseFloat(getComputedStyle(heading).lineHeight),
                stages: document.querySelectorAll('.lp-rail__stage').length,
                stamps: document.querySelectorAll('.lp-stamp__list > div').length,
                install: box('.lp-hero__install'),
                railTop: box('.lp-rail__stage'),
                railInHero: Boolean(document.querySelector('.lp-hero .lp-rail')),
                marks: document.querySelectorAll('.lp-mark').length,
                media: document.querySelectorAll('iframe, video, img').length,
                primaryCtas: [...document.querySelectorAll('.lp-cta .lp-button')].map(link => link.href),
                smallTargets: [...document.querySelectorAll('a, button')]
                  .filter(element => { const rect = element.getBoundingClientRect(); return rect.width && (rect.width < 24 || rect.height < 24); })
                  .map(element => element.textContent.trim()),
                dark: document.documentElement.classList.contains('dark'),
              };
            }''')
            label = f'Promptzilla {theme} {width}'
            if state['overflow'] or state['sections'] != SECTIONS or state['h1'] != 1 or state['stages'] != RAIL_STAGES:
                failures.append(f'{label}: structure/overflow {state}')
            if state['marks'] != 2 or state['media'] or state['stamps'] != 7:
                failures.append(f'{label}: wordmark/stamp {state}')
            if state['dark'] != (theme == 'dark') or state['lines'] > (3.1 if width < 768 else 2.1):
                failures.append(f'{label}: headline/theme {state}')
            if len(state['primaryCtas']) != 2 or any(href != REPO_URL for href in state['primaryCtas']):
                failures.append(f'{label}: repeated primary call to action {state["primaryCtas"]}')
            if state['smallTargets']:
                failures.append(f'{label}: small targets {state["smallTargets"]}')
            if width == 360 and state['install']['bottom'] > 740:
                failures.append(f'{label}: install bar below the first screen {state["install"]}')
            if not state['railInHero']:
                failures.append(f'{label}: the pipeline rail left the hero')
            if width == 1280 and state['railTop']['top'] > 1000:
                failures.append(f'{label}: pipeline rail starts more than one screen down {state["railTop"]}')
            failures.extend(f'{label}: {error}' for error in errors)
            await page.screenshot(path=out / f'promptzilla-{theme}-{width}.png', full_page=True)
            measurements.append({'view': label, **state})
            await page.evaluate("""() => {
              document.querySelector('.lp-hero__install code').textContent = 'x'.repeat(140);
              document.querySelector('.lp-manifest-list dt').textContent = 'x'.repeat(60);
              document.querySelector('.lp-stamp__list dd').textContent = 'x'.repeat(50);
            }""")
            if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
                failures.append(f'{label}: long-string overflow')
            await page.close()

    for theme in ('light', 'dark'):
        context = await browser.new_context(java_script_enabled=False, color_scheme=theme, viewport={'width': 360, 'height': 740})
        page = await context.new_page()
        await page.goto(url, wait_until='networkidle')
        state = await page.evaluate("""() => ({
          buttons: [...document.querySelectorAll('button')].filter(element => getComputedStyle(element).display !== 'none').length,
          scheme: getComputedStyle(document.documentElement).colorScheme,
          overflow: document.documentElement.scrollWidth > innerWidth,
          command: document.querySelector('#install-claude-code').textContent.trim(),
        })""")
        if state != {'buttons': 0, 'scheme': theme, 'overflow': False, 'command': INSTALL_COMMAND}:
            failures.append(f'Promptzilla no-JS {theme}: {state}')
        await page.screenshot(path=out / f'promptzilla-nojs-{theme}-360.png', full_page=True)
        await context.close()

    context = await browser.new_context(viewport={'width': 360, 'height': 740}, permissions=['clipboard-read', 'clipboard-write'])
    page = await context.new_page()
    await page.goto(url, wait_until='networkidle')
    for button in await page.locator('[data-copy-target]').all():
        await button.scroll_into_view_if_needed()
        await button.click()
        await page.wait_for_timeout(50)
        target = await button.get_attribute('data-copy-target')
        expected = (await page.locator('#' + target).text_content()).strip()
        if await button.text_content() != 'Copied' or await page.evaluate('navigator.clipboard.readText()') != expected:
            failures.append(f'Promptzilla clipboard {target}')
    await page.locator('.lp-theme').click()
    if not await page.locator('html').evaluate("element => element.classList.contains('dark')"):
        failures.append('Promptzilla theme toggle')
    await page.locator('.lp-skip').focus()
    await page.locator('.lp-skip').press('Enter')
    if await page.evaluate('document.activeElement.id') != 'main':
        failures.append('Promptzilla skip focus')
    await page.evaluate("() => {navigator.clipboard.writeText = () => Promise.reject(new Error('fixture'));}")
    await page.locator('[data-copy-target]').first.click()
    await page.wait_for_timeout(50)
    if await page.evaluate('window.getSelection().toString().trim()') != INSTALL_COMMAND:
        failures.append('Promptzilla manual-copy fallback')
    for region in await page.locator('.lp-code').all():
        if await region.evaluate('element => element.scrollWidth > element.clientWidth'):
            await region.focus()
            await region.press('ArrowRight')
            if await region.evaluate('element => element.scrollLeft') <= 0:
                failures.append('Promptzilla keyboard code scrolling')
    await context.close()

    page = await browser.new_page(viewport={'width': 1280, 'height': 800}, reduced_motion='reduce')
    await page.goto(url, wait_until='networkidle')
    await page.locator('.lp-theme').hover()
    await page.mouse.down()
    if await page.locator('.lp-theme').evaluate('element => getComputedStyle(element).transform') != 'none':
        failures.append('Promptzilla reduced-motion press')
    await page.mouse.up()
    await page.close()

    sizes = {name: len(gzip.compress((ROOT / name).read_bytes())) for name in ASSETS}
    sizes.update({str(path.relative_to(ROOT)): len(gzip.compress(path.read_bytes())) for path in (ROOT / 'vendor/pattern/fonts').rglob('*.woff2')})
    if sum(sizes.values()) > GZIP_BUDGET:
        failures.append(f'Promptzilla budget {sizes}')
    (out / 'results.json').write_text(json.dumps({'views': measurements, 'gzip': sizes}, indent=2) + '\n', encoding='utf-8')
    print(f'Promptzilla: {len(WIDTHS) * 2} captures, two no-JavaScript captures, responsive/clipboard/keyboard/theme/motion checks; gzip {sum(sizes.values())} bytes.')
