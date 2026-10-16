"""Responsive screenshot and behavior checks for Promptzilla."""
import os
from pathlib import Path

async def run(browser, failures):
    root=Path(__file__).resolve().parents[1]
    out=root/'.review/promptzilla'
    out.mkdir(parents=True,exist_ok=True)
    url=os.environ.get('LP_PROMPTZILLA_URL','http://127.0.0.1:8766/promptzilla/')
    for width in (360,390,768,1024,1280,1440):
        page=await browser.new_page(viewport={'width':width,'height':900},color_scheme='dark',reduced_motion='reduce')
        errors=[]
        page.on('pageerror',lambda error: errors.append(str(error)))
        page.on('console',lambda message: errors.append(message.text) if message.type == 'error' else None)
        await page.goto(url,wait_until='networkidle')
        overflow=await page.evaluate('document.documentElement.scrollWidth > innerWidth')
        if overflow: failures.append(f'Promptzilla {width}: horizontal overflow')
        if await page.title() != 'Promptzilla — prompts worth running': failures.append(f'Promptzilla {width}: missing or incorrect document title')
        if await page.locator('.hero-actions .primary').get_attribute('href') != 'https://github.com/andymccutcheon/promptzilla': failures.append(f'Promptzilla {width}: primary CTA destination changed')
        if errors: failures.append(f'Promptzilla {width}: browser errors {errors}')
        if width in (390,1280): await page.screenshot(path=out/f'promptzilla-{width}.png',full_page=True)
        if width==390:
            await page.locator('button[data-copy="install-command"]').focus()
            button=page.locator('button[data-copy="install-command"]')
            if not await button.evaluate('e=>e===document.activeElement'):
                failures.append('Promptzilla: install copy button is not keyboard focusable')
            await page.context.grant_permissions(['clipboard-read', 'clipboard-write'])
            await button.click()
            if await button.text_content() != 'Copied': failures.append('Promptzilla: install copy feedback did not appear')
            copied=await page.evaluate('navigator.clipboard.readText()')
            if copied != 'claude mcp add promptzilla -- npx -y promptzilla': failures.append('Promptzilla: copied install command mismatch')
        await page.close()
    page=await browser.new_page(viewport={'width':1280,'height':900},color_scheme='dark')
    await page.goto(url,wait_until='networkidle')
    contrasts=await page.evaluate("""() => {
      const lum=c=>{const x=document.createElement('canvas').getContext('2d');x.fillStyle=c;x.fillRect(0,0,1,1);return [...x.getImageData(0,0,1,1).data].slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0)};
      const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
      const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent')return c;e=e.parentElement}return '#0c0e0d'};
      return [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().width&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())).map(e=>({text:e.textContent.trim().slice(0,50),ratio:ratio(getComputedStyle(e).color,bg(e))}));
    }""")
    low=[item for item in contrasts if item['ratio'] < 4.5]
    if low: failures.append(f'Promptzilla contrast below 4.5:1: {low}')
    (out/'contrast.json').write_text(__import__('json').dumps(contrasts,indent=2)+'\n')
    await page.close()
