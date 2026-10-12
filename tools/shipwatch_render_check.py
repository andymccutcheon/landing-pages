"""Shipwatch responsive contract and both approved-page PNG regressions."""
import functools
import gzip
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import threading
import http.server
from freewhirr_render_check import QuietHandler, WIDTHS
ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'd42fe89'
SHIPWATCH_WIDTHS = (360, 480, 768, 1024, 1280, 1440)

async def run(browser, failures, warm):
    out = ROOT / '.review/shipwatch'
    out.mkdir(parents=True, exist_ok=True)
    base = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
    url = base + 'shipwatch/'
    measurements = []
    for theme in ('light', 'dark'):
        for width in SHIPWATCH_WIDTHS:
            page = await browser.new_page(viewport={'width': width, 'height': 900}, color_scheme=theme)
            errors = []
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(url, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            state = await page.evaluate('''() => {
              const h=document.querySelector('h1');const b=s=>document.querySelector(s).getBoundingClientRect().toJSON();
              return {overflow:document.documentElement.scrollWidth>innerWidth,sections:document.querySelectorAll('main>section').length,
              h1:document.querySelectorAll('h1').length,lines:h.clientHeight/parseFloat(getComputedStyle(h).lineHeight),
              install:b('.lp-install'),specimen:b('.lp-brief'),stories:document.querySelectorAll('.lp-brief article').length,
              smallTargets:[...document.querySelectorAll('a,button')].filter(e=>{const r=e.getBoundingClientRect();return r.width && (r.width<24||r.height<24)}).map(e=>e.textContent),dark:document.documentElement.classList.contains('dark'),iframes:document.querySelectorAll('iframe,video').length,
              description:b('.lp-weights tbody td:last-child')};}''')
            label = f'Shipwatch {theme} {width}'
            if state['smallTargets']: failures.append(f'{label}: small targets {state["smallTargets"]}')
            if state['overflow'] or state['sections'] != 8 or state['h1'] != 1 or state['stories'] != 2 or state['iframes']:
                failures.append(f'{label}: structure/overflow {state}')
            if state['dark'] != (theme == 'dark') or state['lines'] > (3.1 if width < 768 else 2.1):
                failures.append(f'{label}: headline/theme {state}')
            if width == 360 and (state['install']['bottom'] > 740 or state['description']['width'] < 240):
                failures.append(f'{label}: mobile install/table {state}')
            if width == 1280 and max(state['install']['bottom'], state['specimen']['bottom']) > 800:
                failures.append(f'{label}: desktop first screen {state}')
            if await page.get_by_role('table', name='Default scoring weights').count() != 1:
                failures.append(f'{label}: accessible weights table')
            failures.extend(f'{label}: {e}' for e in errors)
            await page.screenshot(path=out/f'shipwatch-{theme}-{width}.png', full_page=True)
            measurements.append({'view':label, **state})
            await page.evaluate("() => {document.querySelector('.lp-code code').textContent='x'.repeat(120);document.querySelector('.lp-brief-source span').textContent='x'.repeat(80)}")
            if await page.evaluate('document.documentElement.scrollWidth>innerWidth'):
                failures.append(f'{label}: long-string overflow')
            await page.close()
    for theme in ('light','dark'):
        context=await browser.new_context(java_script_enabled=False,color_scheme=theme,viewport={'width':360,'height':740})
        page=await context.new_page();await page.goto(url,wait_until='networkidle')
        state=await page.evaluate("() => ({buttons:[...document.querySelectorAll('button')].filter(e=>getComputedStyle(e).display!=='none').length,scheme:getComputedStyle(document.documentElement).colorScheme,overflow:document.documentElement.scrollWidth>innerWidth})")
        if state != {'buttons':0,'scheme':theme,'overflow':False}: failures.append(f'Shipwatch no-JS {theme}: {state}')
        await page.screenshot(path=out/f'shipwatch-nojs-{theme}-360.png',full_page=True)
        await context.close()
    context=await browser.new_context(viewport={'width':360,'height':740},permissions=['clipboard-read','clipboard-write'])
    page=await context.new_page();await page.goto(url,wait_until='networkidle')
    for button in await page.locator('[data-copy-target]').all():
        await button.click();await page.wait_for_timeout(50)
        target=await button.get_attribute('data-copy-target')
        if await button.text_content() != 'Copied' or await page.evaluate('navigator.clipboard.readText()') != (await page.locator('#'+target).text_content()).strip():
            failures.append(f'Shipwatch clipboard {target}')
    await page.locator('.lp-theme').click()
    if not await page.locator('html').evaluate("e=>e.classList.contains('dark')"): failures.append('Shipwatch theme toggle')
    await page.locator('.lp-skip').focus();await page.locator('.lp-skip').press('Enter')
    if await page.evaluate('document.activeElement.id') != 'main': failures.append('Shipwatch skip focus')
    await page.evaluate("() => {navigator.clipboard.writeText=()=>Promise.reject(new Error('fixture'));}")
    await page.locator('[data-copy-target]').first.click();await page.wait_for_timeout(50)
    if await page.evaluate('window.getSelection().toString().trim()') != 'pip install shipwatch': failures.append('Shipwatch manual-copy fallback')
    for region in await page.locator('.lp-code').all():
        if await region.evaluate('e=>e.scrollWidth>e.clientWidth'):
            await region.focus();await region.press('ArrowRight')
            if await region.evaluate('e=>e.scrollLeft') <= 0: failures.append('Shipwatch keyboard code scrolling')
    await context.close()
    page=await browser.new_page(reduced_motion='reduce');await page.goto(url,wait_until='networkidle')
    await page.locator('.lp-theme').hover();await page.mouse.down()
    if await page.locator('.lp-theme').evaluate('e=>getComputedStyle(e).transform') != 'none': failures.append('Shipwatch reduced-motion press')
    await page.mouse.up();await page.close()
    with tempfile.TemporaryDirectory(prefix='shipwatch-regression-') as directory:
        archive=Path(directory)/'baseline.tar'
        subprocess.run(['git','archive','--format=tar','-o',str(archive),BASELINE],cwd=ROOT,check=True)
        with tarfile.open(archive) as tar:tar.extractall(directory,filter='data')
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=directory))
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            for product in ('acheron','freewhirr'):
                for theme in ('light','dark'):
                    for width in WIDTHS:
                        shots=[]
                        for phase,address in [('before',f'http://127.0.0.1:{server.server_port}/{product}/'),('after',base+product+'/')]:
                            page=await browser.new_page(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce')
                            await page.goto(address,wait_until='networkidle');await page.evaluate('document.fonts.ready')
                            if product=='acheron':await warm(page,width)
                            await page.evaluate('window.scrollTo(0,0)')
                            shots.append(await page.screenshot(path=out/f'{product}-{phase}-{theme}-{width}.png',full_page=True,animations='disabled',mask=[page.locator('.lp-theatre__interactive')]))
                            await page.close()
                        if shots[0]!=shots[1]:failures.append(f'{product} byte regression {theme} {width}')
        finally:server.shutdown();server.server_close()
    assets=['shipwatch/index.html','vendor/pattern/generated/tokens.css','shared/fonts.css','shared/lp-tokens.css','shared/base.css','shared/motion.css','shared/common.css','shared/shipwatch.css','shared/page.js']
    assets += [str(p.relative_to(ROOT)) for p in (ROOT/'vendor/pattern/fonts').rglob('*.woff2')]
    sizes={name:len(gzip.compress((ROOT/name).read_bytes())) for name in assets}
    if sum(sizes.values())>350000 or sizes['shared/page.js']>15000:failures.append(f'Shipwatch budget {sizes}')
    (out/'results.json').write_text(json.dumps({'views':measurements,'gzip':sizes,'baseline':BASELINE,'regressionPairs':16},indent=2)+'\n')
    print(f'Shipwatch: twelve captures, two no-JS captures, responsive/clipboard/keyboard/theme/motion checks; gzip {sum(sizes.values())} bytes. Acheron + Freewhirr: 16 byte-identical PNG pairs required against {BASELINE}.')
