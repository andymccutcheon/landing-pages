"""The Review Room contract: rendered behavior and actual autonomous SVG timelines.

Imported by the existing aggregate gate, or run directly with --motion for two
full cycles of all three embedded diagrams, with browser video evidence.
"""
import asyncio
import gzip
import json
import os
from pathlib import Path
from playwright.async_api import async_playwright
from render_check import installed_chromium, warm_page_for_capture

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.review/ninthpass-flagship'
WIDTHS = (280, 320, 390, 414, 768, 1024, 1440)
BASE = os.environ.get('LP_TEST_URL', 'http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
URL = os.environ.get('LP_NINTHPASS_URL', BASE + 'ninthpass/')
REPO = 'https://github.com/andymccutcheon/ninthpass'

async def read_motion(frame):
    return await frame.evaluate('''() => {
      const svg = [...document.querySelectorAll('svg')].find(s => getComputedStyle(s.parentElement).display !== 'none');
      return {
        mode: document.documentElement.dataset.mode,
        running: document.documentElement.dataset.running,
        time: svg.getCurrentTime(), paused: svg.animationsPaused(),
        instances: document.querySelectorAll('animateMotion, animate').length,
        signals: [...svg.querySelectorAll('.signal')].map(s => {
          const p = s.getBoundingClientRect(); return {x:p.x,y:p.y,opacity:getComputedStyle(s).opacity,visibility:getComputedStyle(s).visibility};
        }),
        controls: [...document.querySelectorAll('button')].filter(b => b.getBoundingClientRect().width).length
      };
    }''')

async def run(browser, failures, warm):
    OUT.mkdir(parents=True, exist_ok=True)
    views = []
    errors = []
    for width in WIDTHS:
        page = await browser.new_page(viewport={'width': width, 'height': 900})
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        await page.goto(URL, wait_until='networkidle')
        await page.evaluate('document.fonts.ready')
        await warm(page, width)
        await page.locator('[data-motion-toggle]').click()
        await page.evaluate('window.scrollTo(0,0)')
        state = await page.evaluate('''() => ({
          width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
          sections: document.querySelectorAll('main > section').length,
          h1: document.querySelectorAll('h1').length,
          headlineLines: document.querySelector('h1').clientHeight / parseFloat(getComputedStyle(document.querySelector('h1')).lineHeight),
          scheme: getComputedStyle(document.documentElement).colorScheme,
          primary: [...document.querySelectorAll('.primary')].map(a=>a.href),
          fonts: ['Geist','Fraunces','Geist Mono'].map(f=>({name:f,loaded:document.fonts.check(`16px "${f}"`)})),
          targets: [...document.querySelectorAll('a,button')].filter(e=>{
            const r=e.getBoundingClientRect(); return r.width && (r.width<24 || r.height<24);
          }).map(e=>e.textContent.trim()),
          firstActionBottom: document.querySelector('.primary').getBoundingClientRect().bottom,
          iframes: [...document.querySelectorAll('iframe')].map(f=>f.getAttribute('src'))
        })''')
        if state['scrollWidth'] > width: failures.append(f'{width}: horizontal overflow {state["scrollWidth"]}')
        if state['sections'] != 8 or state['h1'] != 1: failures.append(f'{width}: structure {state}')
        if state['headlineLines'] > 2.1: failures.append(f'{width}: headline {state["headlineLines"]} lines')
        if state['scheme'] != 'dark': failures.append(f'{width}: wrong scheme')
        if state['primary'] != [REPO, REPO]: failures.append(f'{width}: primary actions')
        if not all(f['loaded'] for f in state['fonts']): failures.append(f'{width}: unloaded font')
        if state['targets']: failures.append(f'{width}: small targets {state["targets"]}')
        if state['firstActionBottom'] > 900: failures.append(f'{width}: primary action below first screen')
        if len(state['iframes']) != 2: failures.append(f'{width}: missing diagrams')
        # Capture the full static-readable composition with loaded embedded documents.
        await page.locator('.site-header').evaluate("e=>e.style.position='static'")
        await page.screenshot(path=OUT / f'page-{width}.png', full_page=True)
        await page.locator('.site-header').evaluate("e=>e.style.position='sticky'")
        if width in (390, 1440):
            await page.screenshot(path=OUT / f'fold-{width}.png')
            for name in await page.eval_on_selector_all('[data-diagram]', 'els => els.map(e => e.dataset.diagram)'):
                frame_el = page.locator(f'[data-diagram="{name}"]')
                await frame_el.scroll_into_view_if_needed()
                await frame_el.screenshot(path=OUT / f'{name}-{width}.png')
                frame = await frame_el.element_handle()
                frame = await frame.content_frame()
                frame_errors = await frame.evaluate('''() => [...document.querySelectorAll('svg')].filter(s=>getComputedStyle(s.parentElement).display!=='none').flatMap(s=>[...s.querySelectorAll('text')].filter(t=>{
                  const b=t.getBBox(), v=s.viewBox.baseVal;return b.x<0||b.y<0||b.x+b.width>v.width||b.y+b.height>v.height;
                }).map(t=>t.textContent))''')
                if frame_errors: failures.append(f'{width} {name}: clipped SVG labels {frame_errors}')
        # Meaningful resilience probe: unusually long code must stay inside its scroll region.
        await page.locator('#start-command').evaluate("e=>e.textContent='x'.repeat(300)")
        if await page.evaluate('document.documentElement.scrollWidth > innerWidth'): failures.append(f'{width}: long code overflow')
        views.append(state)
        await page.close()

    page = await browser.new_page(viewport={'width':1440,'height':900})
    await page.goto(URL, wait_until='networkidle')
    # Full keyboard tab pattern, not merely clicking the tabs.
    await page.get_by_role('tab', name='Composed', exact=True).focus()
    await page.keyboard.press('ArrowRight')
    if await page.get_by_role('tab', name='Approved', exact=True).get_attribute('aria-selected') != 'true': failures.append('ArrowRight did not select scorecard')
    await page.keyboard.press('End')
    if not await page.locator('#pass2').is_visible(): failures.append('End did not select final scorecard')
    await page.keyboard.press('Home')
    if not await page.locator('#pass1').is_visible(): failures.append('Home did not select first scorecard')
    # Every public local link/asset resolves, including unchanged proof artifacts.
    local = await page.evaluate("[...document.querySelectorAll('[href],[src]')].map(e=>e.href||e.src).filter(u=>u.startsWith(location.origin)&&!u.includes('#'))")
    for link in set(local):
        response = await page.request.get(link)
        if response.status != 200: failures.append(f'Broken local URL {response.status}: {link}')
    await page.context.grant_permissions(['clipboard-read','clipboard-write'])
    await page.get_by_role('button', name='Copy setup and first-run commands').click()
    copied = await page.evaluate('navigator.clipboard.readText()')
    if 'git clone '+REPO not in copied or '--worker claude' not in copied: failures.append('Clipboard content incomplete')
    await page.evaluate("() => { navigator.clipboard.writeText=async()=>{throw new Error('Denied for verification')}; }")
    await page.get_by_role('button', name='Copy setup and first-run commands').click()
    if not await page.evaluate("getSelection().toString().includes('git clone')"): failures.append('Clipboard refusal did not select commands')
    # Keyboard-focus visibility and no sticky-header obstruction.
    focus = []
    await page.keyboard.press('Tab')
    for target in await page.locator('a,button,[role="tabpanel"],pre').all():
        if not await target.is_visible() or await target.is_disabled(): continue
        await target.focus()
        result = await target.evaluate('''e=>({name:e.textContent.trim().slice(0,40),outline:getComputedStyle(e).outlineStyle,width:parseFloat(getComputedStyle(e).outlineWidth),top:e.getBoundingClientRect().top})''')
        if result['outline'] == 'none' or result['width'] < 3: failures.append(f'No focus indicator: {result}')
        focus.append(result)
    await page.close()

    context = await browser.new_context(java_script_enabled=False, viewport={'width':390,'height':900})
    plain = await context.new_page()
    await plain.goto(URL, wait_until='networkidle')
    if await plain.locator('.score-panel:visible').count() != 2: failures.append('No-script scorecards missing')
    if await plain.locator('button:visible').count(): failures.append('No-script dead buttons visible')
    if not await plain.locator('#start-command').is_visible(): failures.append('No-script setup missing')
    for name in await plain.eval_on_selector_all('[data-diagram]', 'els => els.map(e => e.dataset.diagram)'):
        el = plain.locator(f'[data-diagram="{name}"]')
        await el.scroll_into_view_if_needed()
        frame = await (await el.element_handle()).content_frame()
        if await frame.locator('svg text').count() < 5: failures.append(f'No-script {name} incomplete')
    await plain.screenshot(path=OUT/'no-javascript-390.png', full_page=True)
    await context.close()

    page = await browser.new_page(viewport={'width':1440,'height':900}, reduced_motion='reduce')
    await page.goto(URL, wait_until='networkidle')
    if await page.locator('[data-motion-toggle]').text_content() != 'Motion reduced': failures.append('OS preference not communicated')
    for name in await page.eval_on_selector_all('[data-diagram]', 'els => els.map(e => e.dataset.diagram)'):
        el = page.locator(f'[data-diagram="{name}"]')
        await el.scroll_into_view_if_needed()
        frame = await (await el.element_handle()).content_frame()
        first = await read_motion(frame)
        await page.wait_for_timeout(250)
        last = await read_motion(frame)
        if first['time'] != last['time'] or last['running'] != 'false': failures.append(f'Reduced-motion {name} still runs')
    await page.screenshot(path=OUT/'reduced-motion.png')
    await page.emulate_media(reduced_motion='no-preference')
    await page.wait_for_timeout(150)
    if await page.locator('[data-motion-toggle]').is_disabled(): failures.append('Live OS preference did not restore toggle')
    await page.close()
    assets = [p for directory in ('css','js','diagrams','assets') for p in (ROOT/'ninthpass'/directory).rglob('*') if p.is_file() and p.suffix in ('.css','.js','.html','.woff2','.svg','.png')]
    sizes = {str(p.relative_to(ROOT)): len(gzip.compress(p.read_bytes())) for p in assets}
    if sum(sizes.values()) > 400000: failures.append(f'Runtime gzip exceeds 400000 bytes: {sum(sizes.values())}')
    failures.extend(errors)
    (OUT/'results.json').write_text(json.dumps({'views':views,'focus':focus,'runtimeGzipBytes':sum(sizes.values()),'assets':sizes,'errors':errors,'failures':failures},indent=2)+'\n')
    print(f'Silverquill: {len(WIDTHS)} responsive views; scorecard keyboard, clipboard success/refusal, local links, no-script, live reduced-motion and focus checked. Runtime gzip: {sum(sizes.values())} bytes.')

async def motion_case(browser, name, width=1440):
    """Real embedded page, two cycles, then stop/resume/offscreen/OS preference."""
    label=name if width==1440 else name+'-mobile'
    context = await browser.new_context(viewport={'width':width,'height':900},record_video_dir=OUT/'motion-video',record_video_size={'width':width,'height':900})
    page = await context.new_page()
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    await page.goto(URL,wait_until='networkidle')
    target=page.locator(f'[data-diagram="{name}"]')
    await target.scroll_into_view_if_needed()
    frame=await (await target.element_handle()).content_frame()
    await page.wait_for_timeout(300)
    samples=[]
    for wait in (0,3000,6000,8000,4000,18000):
        await page.wait_for_timeout(wait)
        samples.append(await read_motion(frame))
    if samples[-1]['time'] < 36: errors.append('Did not witness two autonomous cycles')
    if len({s['instances'] for s in samples}) != 1: errors.append('Animation instances accumulated')
    if not any(s['signals'] != samples[0]['signals'] for s in samples[1:]): errors.append('Signal did not move')
    await target.screenshot(path=OUT/f'{label}-autonomous.png')
    # Toggle without scrolling the target away (fixed header button is visible).
    await page.locator('[data-motion-toggle]').click()
    await page.wait_for_timeout(150)
    stopped=await read_motion(frame)
    await page.wait_for_timeout(400)
    stopped_after=await read_motion(frame)
    if stopped['time'] != stopped_after['time'] or stopped_after['running']!='false': errors.append('Page motion setting did not stop timeline')
    if stopped_after['controls']: errors.append('Embedded diagram exposes playback controls')
    await page.reload(wait_until='networkidle')
    if await page.locator('[data-motion-toggle]').text_content() != 'Resume motion': errors.append('Pause preference not persistent')
    await target.scroll_into_view_if_needed()
    frame=await (await target.element_handle()).content_frame()
    await page.locator('[data-motion-toggle]').click()
    await page.wait_for_timeout(350)
    resumed=await read_motion(frame)
    await page.locator('#hero-title').scroll_into_view_if_needed()
    await page.wait_for_timeout(250)
    off=await read_motion(frame)
    await page.wait_for_timeout(500)
    off_after=await read_motion(frame)
    if off['time'] != off_after['time'] or not off_after['paused']: errors.append('Offscreen diagram kept running')
    await target.scroll_into_view_if_needed()
    await page.emulate_media(reduced_motion='reduce')
    await page.wait_for_timeout(150)
    reduced=await read_motion(frame)
    if reduced['running']!='false': errors.append('Live reduced-motion change did not stop diagram')
    video=page.video
    await context.close()
    video_path=OUT/'motion-video'/f'{label}-two-cycles.webm'
    await video.save_as(video_path)
    return {'name':name,'width':width,'samples':samples,'stopped':stopped_after,'resumed':resumed,'offscreen':off_after,'reduced':reduced,'video':str(video_path),'errors':errors}

async def main():
    OUT.mkdir(parents=True,exist_ok=True)
    failures=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=installed_chromium())
        await run(browser,failures,warm_page_for_capture)
        if '--motion' in __import__('sys').argv:
            motion=await asyncio.gather(*(motion_case(browser,n,w) for w in (1440,390) for n in await page.eval_on_selector_all('[data-diagram]', 'els => els.map(e => e.dataset.diagram)')))
            (OUT/'motion-results.json').write_text(json.dumps(motion,indent=2)+'\n')
            for item in motion: failures.extend(f'{item["name"]}: {e}' for e in item['errors'])
        await browser.close()
    print('Silverquill PASS' if not failures else '\n'.join(failures))
    raise SystemExit(bool(failures))

if __name__=='__main__': asyncio.run(main())
