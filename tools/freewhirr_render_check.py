"""Freewhirr contract and pixel regression against the pre-build Acheron commit."""
import asyncio
import functools
import gzip
import http.server
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'ebccc26'
WIDTHS = (360, 768, 1280, 1440)

async def check(browser, url, out, failures):
    measurements = []
    for theme in ('light', 'dark'):
        for width in WIDTHS:
            page = await browser.new_page(viewport={'width':width,'height':900}, color_scheme=theme)
            errors=[]
            page.on('pageerror', lambda error: errors.append(str(error)))
            await page.goto(url, wait_until='networkidle')
            await page.evaluate('document.fonts.ready')
            result = await page.evaluate('''() => {
              const boxes = [...document.querySelectorAll('pre, table, .lp-ladder, h1, h2, p')];
              const h = document.querySelector('h1');
              const style = getComputedStyle(h);
              const b = el => el.getBoundingClientRect().toJSON();
              return {overflow: document.documentElement.scrollWidth > innerWidth,
                escaped: boxes.filter(el => b(el).right > innerWidth + 1 || b(el).left < -1).map(el => el.tagName),
                lines: h.clientHeight / parseFloat(style.lineHeight),
                install: b(document.querySelector('.lp-install')),
                ladder: b(document.querySelector('.lp-ladder')),
                dark: document.documentElement.classList.contains('dark'),
                h1: document.querySelectorAll('h1').length,
                sections: document.querySelectorAll('main > section').length,
                headings: [...document.querySelectorAll('main h2')].map(el => el.textContent),
                tableRole: document.querySelector('.lp-policy').getAttribute('role')};
            }''')
            label=f'{theme} {width}'
            if result['overflow'] or result['escaped']: failures.append(f'{label}: overflow {result}')
            if result['lines'] > (3 if width==360 else 2)+0.1: failures.append(f'{label}: headline lines {result["lines"]}')
            if result['h1'] != 1 or result['sections'] != 9 or result['tableRole'] != 'table': failures.append(f'{label}: structure {result}')
            if result['dark'] != (theme=='dark'): failures.append(f'{label}: theme')
            # Actual first-screen fit, not the capture viewport.
            if width in (360,1280):
                limit=740 if width==360 else 800
                if result['install']['bottom'] > limit: failures.append(f'{label}: install outside {limit}')
                if width==1280 and result['ladder']['bottom'] > limit: failures.append(f'{label}: ladder outside {limit}')
            failures.extend(f'{label}: {error}' for error in errors)
            await page.screenshot(path=out/f'freewhirr-{theme}-{width}.png', full_page=True)
            measurements.append({'view':label, **result})
            # Long strings remain confined to evidence blocks and setting labels.
            await page.evaluate('''() => {document.querySelector('.lp-code code').textContent='x'.repeat(120); document.querySelector('.lp-guards dt').textContent='x'.repeat(40)}''')
            if await page.evaluate('document.documentElement.scrollWidth > innerWidth'): failures.append(f'{label}: long-string overflow')
            await page.close()
    for theme in ('light','dark'):
        context=await browser.new_context(java_script_enabled=False,color_scheme=theme,viewport={'width':360,'height':740})
        page=await context.new_page()
        await page.goto(url,wait_until='networkidle')
        state=await page.evaluate('''() => ({controls:[...document.querySelectorAll('button')].filter(e=>getComputedStyle(e).display!=='none').length, sections:document.querySelectorAll('main > section').length, scheme:getComputedStyle(document.documentElement).colorScheme, overflow:document.documentElement.scrollWidth>innerWidth})''')
        if state != {'controls':0,'sections':9,'scheme':theme,'overflow':False}: failures.append(f'no-JS {theme}: {state}')
        await context.close()
    context=await browser.new_context(viewport={'width':360,'height':740},permissions=['clipboard-read','clipboard-write'])
    page=await context.new_page(); await page.goto(url,wait_until='networkidle')
    for button in await page.locator('[data-copy-target]').all():
        await button.click(); await page.wait_for_timeout(50)
        target=await button.get_attribute('data-copy-target')
        expected=(await page.locator('#'+target).text_content()).strip()
        actual=await page.evaluate('navigator.clipboard.readText()')
        if await button.text_content()!='Copied' or actual!=expected: failures.append(f'copy {target}')
    await page.locator('.lp-theme').click()
    if not await page.locator('html').evaluate("el=>el.classList.contains('dark')"): failures.append('theme toggle')
    await page.locator('.lp-skip').focus(); await page.locator('.lp-skip').press('Enter')
    if await page.evaluate('document.activeElement.id')!='main': failures.append('skip focus')
    await page.evaluate("() => { navigator.clipboard.writeText=()=>Promise.reject(new Error('fixture')); }")
    button=page.locator('[data-copy-target]').first
    await button.click(); await page.wait_for_timeout(50)
    if await page.evaluate('window.getSelection().toString().trim()')!='pip install freewhirr': failures.append('clipboard fallback')
    for region in await page.locator('.lp-code').all():
        if await region.evaluate('el=>el.scrollWidth>el.clientWidth'):
            await region.focus(); await region.press('ArrowRight')
            if await region.evaluate('el=>el.scrollLeft')<=0: failures.append('keyboard code scrolling')
    await context.close()
    page=await browser.new_page(reduced_motion='reduce'); await page.goto(url,wait_until='networkidle')
    await page.locator('.lp-theme').evaluate("el=>el.classList.add('test-active')")
    # Force :active using mouse down, inspect the actual recipe.
    await page.locator('.lp-theme').hover(); await page.mouse.down()
    if await page.locator('.lp-theme').evaluate("el=>getComputedStyle(el).transform")!='none': failures.append('reduced-motion press')
    await page.mouse.up(); await page.close()
    (out.parent/'freewhirr-layout.json').write_text(json.dumps(measurements,indent=2)+'\n')

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

async def regression(browser, out, failures, warm):
    with tempfile.TemporaryDirectory(prefix='freewhirr-baseline-') as directory:
        archive=Path(directory)/'baseline.tar'
        subprocess.run(['git','archive','--format=tar','-o',str(archive),BASELINE],cwd=ROOT,check=True)
        with tarfile.open(archive) as tar: tar.extractall(directory,filter='data')
        server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(QuietHandler,directory=directory))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        current=os.environ.get('LP_TEST_URL','http://127.0.0.1:8766/acheron/')
        try:
            for theme in ('light','dark'):
                for width in WIDTHS:
                    shots=[]
                    for phase,url in [('before',f'http://127.0.0.1:{server.server_port}/acheron/'),('after',current)]:
                        page=await browser.new_page(viewport={'width':width,'height':900},color_scheme=theme,reduced_motion='reduce')
                        await page.goto(url,wait_until='networkidle');await page.evaluate('document.fonts.ready')
                        await warm(page,width)
                        await page.evaluate('window.scrollTo(0,0)')
                        shots.append(await page.screenshot(path=out/f'acheron-{phase}-{theme}-{width}.png',full_page=True,animations='disabled'))
                        await page.close()
                    if shots[0]!=shots[1]: failures.append(f'Acheron pixel regression: {theme} {width}')
        finally: server.shutdown();server.server_close()
    print(f'Acheron regression: eight before/after PNG pairs compared against {BASELINE}')

async def run(browser, failures, warm):
    out=ROOT/'.review/freewhirr';out.mkdir(parents=True,exist_ok=True)
    url=os.environ.get('LP_TEST_URL','http://127.0.0.1:8766/acheron/').replace('/acheron/','/freewhirr/')
    await check(browser,url,out,failures)
    await regression(browser,out,failures,warm)
    assets=['freewhirr/index.html','vendor/pattern/generated/tokens.css','shared/fonts.css','shared/lp-tokens.css','shared/base.css','shared/motion.css','shared/freewhirr.css','shared/page.js']
    assets += [str(p.relative_to(ROOT)) for p in (ROOT/'vendor/pattern/fonts').rglob('*.woff2')]
    sizes={name:len(gzip.compress((ROOT/name).read_bytes())) for name in assets}
    total=sum(sizes.values());script=sizes['shared/page.js']
    if total>350_000 or script>15_000: failures.append(f'Budget: {total} total, {script} script')
    (out.parent/'freewhirr-budget.json').write_text(json.dumps(sizes,indent=2)+'\n')
    print(f'Freewhirr: eight theme/width captures; no-JS, long strings, copy, theme, skip, keyboard scrolling, reduced motion. gzip assets {total} bytes; script {script} bytes plus inline theme initializer.')
