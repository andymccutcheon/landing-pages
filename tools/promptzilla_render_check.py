"""Responsive screenshots and behavior checks for Promptzilla."""
import json
import os
from pathlib import Path


async def run(browser, failures):
    root = Path(__file__).resolve().parents[1]
    out = root / '.review/promptzilla'
    out.mkdir(parents=True, exist_ok=True)
    url = os.environ.get('LP_PROMPTZILLA_URL', 'http://127.0.0.1:8766/')
    for width in (360, 390, 768, 1024, 1280, 1440):
        page = await browser.new_page(viewport={'width': width, 'height': 900}, color_scheme='dark', reduced_motion='reduce')
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda message: errors.append(message.text) if message.type == 'error' else None)
        await page.goto(url, wait_until='networkidle')
        overflow = await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        if overflow:
            failures.append(f'Promptzilla {width}: horizontal overflow')
        if await page.title() != 'Promptzilla — prompts worth running':
            failures.append(f'Promptzilla {width}: missing or incorrect document title')
        for selector in ('.hero-actions .primary', '.end-cta .primary'):
            if await page.locator(selector).get_attribute('href') != 'https://github.com/andymccutcheon/promptzilla':
                failures.append(f'Promptzilla {width}: CTA destination changed for {selector}')
        motion = await page.evaluate("""() => ({
          scroll: getComputedStyle(document.documentElement).scrollBehavior,
          durations: getComputedStyle(document.querySelector('.button')).transitionDuration.split(',').map(x => parseFloat(x))
        })""")
        if motion['scroll'] != 'auto' or max(motion['durations']) > 0.00002:
            failures.append(f'Promptzilla {width}: reduced-motion styles not applied: {motion}')
        if errors:
            failures.append(f'Promptzilla {width}: browser errors {errors}')
        if width in (390, 1280):
            await page.screenshot(path=out / f'promptzilla-{width}.png', full_page=True)
        if width == 390:
            await page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
            install_button = page.locator('button[data-copy="install-command"]')
            await install_button.click()
            await page.wait_for_function("document.querySelector('button[data-copy=\"install-command\"]').textContent === 'Copied'")
            if await install_button.text_content() != 'Copied':
                failures.append('Promptzilla: install copy feedback did not appear')
            copied = await page.evaluate('navigator.clipboard.readText()')
            if copied != 'claude mcp add promptzilla -- npx -y promptzilla':
                failures.append('Promptzilla: copied install command mismatch')
            await page.locator('.config summary').click()
            config_button = page.locator('button[data-copy="mcp-config"]')
            await config_button.click()
            await page.wait_for_function("document.querySelector('button[data-copy=\"mcp-config\"]').textContent === 'Copied'")
            if await config_button.text_content() != 'Copied':
                failures.append('Promptzilla: JSON copy feedback did not appear')
            copied_json = await page.evaluate('navigator.clipboard.readText()')
            if '"mcpServers"' not in copied_json or '"promptzilla"' not in copied_json:
                failures.append('Promptzilla: copied MCP JSON mismatch')
        await page.close()

    keyboard = await browser.new_page(viewport={'width': 1280, 'height': 900}, color_scheme='dark')
    await keyboard.goto(url, wait_until='networkidle')
    await keyboard.locator('.config').evaluate('(e) => e.open = true')
    targets = {
        '.hero-actions .primary': False,
        'button[data-copy="install-command"]': False,
        'button[data-copy="mcp-config"]': False,
        '.end-cta .primary': False,
    }
    for _ in range(30):
        await keyboard.keyboard.press('Tab')
        for selector, found in targets.items():
            if found or not await keyboard.locator(selector).evaluate('(e) => e === document.activeElement'):
                continue
            targets[selector] = True
            visible_focus = await keyboard.locator(selector).evaluate("""e => {
              const s = getComputedStyle(e);
              return (s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0) || s.boxShadow !== 'none';
            }""")
            if not visible_focus:
                failures.append(f'Promptzilla: no visible keyboard focus indicator on {selector}')
        if all(targets.values()):
            break
    for selector, found in targets.items():
        if not found:
            failures.append(f'Promptzilla: keyboard Tab did not reach {selector}')
    await keyboard.close()

    denied = await browser.new_page(viewport={'width': 390, 'height': 900}, color_scheme='dark')
    await denied.add_init_script("Object.defineProperty(navigator, 'clipboard', { configurable: true, value: { writeText: async () => { throw new DOMException('denied', 'NotAllowedError'); } } })")
    await denied.goto(url, wait_until='networkidle')
    denied_button = denied.locator('button[data-copy="install-command"]')
    await denied_button.click()
    await denied.wait_for_function("document.querySelector('button[data-copy=\"install-command\"]').textContent === 'Select and copy'")
    if await denied_button.text_content() != 'Select and copy':
        failures.append('Promptzilla: denied clipboard did not select command fallback')
    selected = await denied.evaluate('window.getSelection().toString().trim()')
    if selected != 'claude mcp add promptzilla -- npx -y promptzilla':
        failures.append('Promptzilla: denied clipboard fallback selection mismatch')
    await denied.close()

    page = await browser.new_page(viewport={'width': 1280, 'height': 900}, color_scheme='dark')
    await page.goto(url, wait_until='networkidle')
    await page.locator('.config').evaluate('(e) => e.open = true')
    contrasts = await page.evaluate("""() => {
      const lum = c => { const x=document.createElement('canvas').getContext('2d'); x.fillStyle=c; x.fillRect(0,0,1,1); return [...x.getImageData(0,0,1,1).data].slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0) };
      const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
      const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent')return c;e=e.parentElement}return '#0c0e0d'};
      return [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().width&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>({text:e.textContent.trim().slice(0,50),ratio:ratio(getComputedStyle(e).color,bg(e))}));
    }""")
    low = [item for item in contrasts if item['ratio'] < 4.5]
    if low:
        failures.append(f'Promptzilla contrast below 4.5:1: {low}')
    (out / 'contrast.json').write_text(json.dumps(contrasts, indent=2) + '\n')
    await page.close()
