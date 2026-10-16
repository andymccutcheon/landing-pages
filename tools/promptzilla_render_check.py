"""Promptzilla responsive, interaction and resilience contract (Alien UI design system).

The page is dark-only. A register switch (industrial / science-ship) replaces the old
light/dark theme, so every width is captured and checked in both registers.
"""
import gzip
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDTHS = (360, 480, 768, 1024, 1280, 1440)
REGISTERS = ('industrial', 'science-ship')
SECTIONS = 8
RAIL_STAGES = 4
READOUT_ROWS = 7
INSTALL_COMMAND = 'claude mcp add promptzilla -- npx -y promptzilla'
REPO_URL = 'https://github.com/andymccutcheon/promptzilla'
TYPEON_TEXT = 'Validated 5 skills and 9 source assets.'
ASSETS = (
    'promptzilla/index.html',
    'promptzilla/css/pz-tokens.css',
    'promptzilla/css/promptzilla.css',
    'promptzilla/js/page.js',
    'promptzilla/assets/favicon.svg',
    'vendor/alien-ui/css/system-contract.css',
    'vendor/alien-ui/css/tokens.css',
    'vendor/alien-ui/css/system-components.css',
    'vendor/alien-ui/css/components.css',
    'vendor/alien-ui/css/crt.css',
    'vendor/alien-ui/js/typeon.js',
    'vendor/alien-ui/fonts/Michroma.ttf',
    'vendor/alien-ui/fonts/ShareTechMono.ttf',
)
# Measured total is 76,484 bytes gzipped (HTML, five vendored and two page stylesheets, two
# scripts, favicon and both TTF fonts); the budget is that total plus about 10%
# (84,132, rounded down to 84,000). The two TTF fonts are 70% of it.
GZIP_BUDGET = 84000


async def choose_register(page, register, failures, label):
    """Set the register the way a visitor does and assert the page reflects it."""
    await page.locator(f'[data-register-choice="{register}"]').click()
    state = await page.evaluate('''() => ({
      register: document.documentElement.dataset.register,
      pressed: Object.fromEntries([...document.querySelectorAll('[data-register-choice]')]
        .map(button => [button.dataset.registerChoice, button.getAttribute('aria-pressed')])),
    })''')
    expected = {name: str(name == register).lower() for name in REGISTERS}
    if state['register'] != register or state['pressed'] != expected:
        failures.append(f'{label}: register switch {state}')


async def run(browser, failures, warm):
    out = ROOT / '.review/promptzilla'
    out.mkdir(parents=True, exist_ok=True)
    base = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
    url = base + 'promptzilla/'
    measurements = []
    for register in REGISTERS:
        for width in WIDTHS:
            page = await browser.new_page(viewport={'width': width, 'height': 900})
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            page.on('console', lambda message: errors.append(f'console {message.type}: {message.text}') if message.type == 'error' else None)
            await page.goto(url, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            label = f'Promptzilla {register} {width}'
            await choose_register(page, register, failures, label)
            state = await page.evaluate('''() => {
              const box = selector => document.querySelector(selector).getBoundingClientRect().toJSON();
              const heading = document.querySelector('h1');
              return {
                overflow: document.documentElement.scrollWidth > innerWidth,
                sections: document.querySelectorAll('main > section').length,
                h1: document.querySelectorAll('h1').length,
                lines: heading.clientHeight / parseFloat(getComputedStyle(heading).lineHeight),
                stages: document.querySelectorAll('.pz-hero .pz-rail__stage').length,
                readoutRows: document.querySelectorAll('.pz-readout dt').length,
                install: box('.pz-command--hero'),
                railTop: box('.pz-rail__stage'),
                marks: document.querySelectorAll('.pz-mark').length,
                media: document.querySelectorAll('iframe, video, img').length,
                primaryCtas: [...document.querySelectorAll('.pz-primary')].map(link => link.href),
                smallTargets: [...document.querySelectorAll('a, button')]
                  .filter(element => { const rect = element.getBoundingClientRect(); return rect.width && (rect.width < 24 || rect.height < 24); })
                  .map(element => element.textContent.trim()),
                scheme: getComputedStyle(document.documentElement).colorScheme,
              };
            }''')
            if state['overflow'] or state['sections'] != SECTIONS or state['h1'] != 1 or state['stages'] != RAIL_STAGES:
                failures.append(f'{label}: structure/overflow {state}')
            if state['marks'] != 2 or state['media'] or state['readoutRows'] != READOUT_ROWS:
                failures.append(f'{label}: wordmark/readout/media {state}')
            if state['scheme'] != 'dark' or state['lines'] > (3.1 if width < 768 else 2.1):
                failures.append(f'{label}: headline/colour scheme {state}')
            if len(state['primaryCtas']) != 2 or any(href != REPO_URL for href in state['primaryCtas']):
                failures.append(f'{label}: repeated primary call to action {state["primaryCtas"]}')
            if state['smallTargets']:
                failures.append(f'{label}: small targets {state["smallTargets"]}')
            if width == 360 and state['install']['bottom'] > 740:
                failures.append(f'{label}: install bar below the first screen {state["install"]}')
            if width == 1280 and state['railTop']['top'] > 1000:
                failures.append(f'{label}: pipeline rail starts more than one screen down {state["railTop"]}')
            failures.extend(f'{label}: {error}' for error in errors)
            await warm(page, width)
            await page.screenshot(path=out / f'promptzilla-{register}-{width}.png', full_page=True)
            measurements.append({'view': label, **state})
            await page.evaluate("""() => {
              document.querySelector('.pz-command--hero code').textContent = 'x'.repeat(140);
              document.querySelector('.pz-manifest th').textContent = 'x'.repeat(60);
              document.querySelector('.pz-readout dd').textContent = 'x'.repeat(50);
            }""")
            if await page.evaluate('document.documentElement.scrollWidth > innerWidth'):
                failures.append(f'{label}: long-string overflow')
            await page.close()

    await check_skills_table(browser, url, failures)

    context = await browser.new_context(java_script_enabled=False, viewport={'width': 360, 'height': 740})
    page = await context.new_page()
    await page.goto(url, wait_until='networkidle')
    state = await page.evaluate("""() => ({
      buttons: [...document.querySelectorAll('button')].filter(element => element.getClientRects().length > 0).length,
      scheme: getComputedStyle(document.documentElement).colorScheme,
      overflow: document.documentElement.scrollWidth > innerWidth,
      command: document.querySelector('#install-claude-code').textContent.trim(),
    })""")
    if state != {'buttons': 0, 'scheme': 'dark', 'overflow': False, 'command': INSTALL_COMMAND}:
        failures.append(f'Promptzilla no-JS: {state}')
    await page.screenshot(path=out / 'promptzilla-nojs-360.png', full_page=True)
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
    await page.locator('.pz-skip').focus()
    await page.locator('.pz-skip').press('Enter')
    if await page.evaluate('document.activeElement.id') != 'main':
        failures.append('Promptzilla skip focus')
    await page.evaluate("() => {navigator.clipboard.writeText = () => Promise.reject(new Error('fixture'));}")
    await page.locator('[data-copy-target]').first.click()
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

    await check_register_persistence(browser, url, failures)

    for register in REGISTERS:
        page = await browser.new_page(viewport={'width': 1280, 'height': 800}, reduced_motion='reduce')
        await page.goto(url, wait_until='networkidle')
        await choose_register(page, register, failures, f'Promptzilla reduced motion {register}')
        state = await page.evaluate("""() => ({
          lamps: [...document.querySelectorAll('.pz-rail .pz-lamp')].map(lamp => getComputedStyle(lamp).animationName),
          running: [...document.querySelectorAll('.pz-rail .pz-lamp')].reduce((total, lamp) => total + lamp.getAnimations().length, 0),
          typeon: document.querySelector('[data-typeon]').textContent,
          flicker: getComputedStyle(document.querySelector('.crt'), '::after').animationName,
        })""")
        if (any(name != 'none' for name in state['lamps']) or state['running'] or state['typeon'] != TYPEON_TEXT or state['flicker'] != 'none'):
            failures.append(f'Promptzilla reduced motion {register}: {state}')
        await page.close()

    sizes = {name: len(gzip.compress((ROOT / name).read_bytes())) for name in ASSETS}
    if sum(sizes.values()) > GZIP_BUDGET:
        failures.append(f'Promptzilla budget {sum(sizes.values())} > {GZIP_BUDGET}: {sizes}')
    (out / 'results.json').write_text(json.dumps({'views': measurements, 'gzip': sizes}, indent=2) + '\n', encoding='utf-8')
    print(f'Promptzilla: {len(WIDTHS) * len(REGISTERS)} captures, one no-JavaScript capture, responsive/clipboard/keyboard/register/motion/table checks; gzip {sum(sizes.values())} of {GZIP_BUDGET} bytes.')


async def check_skills_table(browser, url, failures):
    """Stacked rows on a phone, a real table on a desktop, and no overflow of the wrapper."""
    for width, stacked in ((390, True), (1280, False)):
        page = await browser.new_page(viewport={'width': width, 'height': 900})
        await page.goto(url, wait_until='networkidle')
        state = await page.evaluate('''() => {
          const table = document.querySelector('.pz-skills');
          const wrap = table.closest('.pz-table-wrap');
          return {
            row: getComputedStyle(table.querySelector('tbody tr')).display,
            table: getComputedStyle(table).display,
            tableWider: table.scrollWidth > wrap.clientWidth,
            wrapOverflow: wrap.scrollWidth > wrap.clientWidth,
          };
        }''')
        if stacked and (state['row'] != 'block' or state['tableWider'] or state['wrapOverflow']):
            failures.append(f'Promptzilla skills table {width} is not stacked: {state}')
        if not stacked and (state['row'] != 'table-row' or state['table'] != 'table'):
            failures.append(f'Promptzilla skills table {width} is not a real table: {state}')
        await page.close()


async def check_register_persistence(browser, url, failures):
    """The choice survives a reload, and the stored value drives data-register and aria-pressed."""
    context = await browser.new_context(viewport={'width': 1280, 'height': 800})
    page = await context.new_page()
    await page.goto(url, wait_until='networkidle')
    for register in ('science-ship', 'industrial'):
        await choose_register(page, register, failures, f'Promptzilla register toggle {register}')
        await page.reload(wait_until='networkidle')
        state = await page.evaluate('''() => ({
          register: document.documentElement.dataset.register,
          stored: localStorage.getItem('pz-register'),
          pressed: document.querySelector('[data-register-choice][aria-pressed="true"]').dataset.registerChoice,
        })''')
        if state != {'register': register, 'stored': register, 'pressed': register}:
            failures.append(f'Promptzilla register persistence {register}: {state}')
    await context.close()
