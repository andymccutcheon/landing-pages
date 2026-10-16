"""Measure Promptzilla text, control and rule contrast in the installed Chromium.

Run with the existing repository virtual environment and local preview server.
"""
import asyncio,json,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from render_check import installed_chromium
from playwright.async_api import async_playwright
RULES=('.lp-rail__stage','.lp-rail__gate','.lp-limits-heading','.lp-stamp__list > div:first-child')
# Same resolution order as render_check.py: LP_PROMPTZILLA_URL wins, otherwise the
# page is derived from the one preview server LP_TEST_URL names.
BASE=os.environ.get('LP_TEST_URL','http://127.0.0.1:8766/acheron/').removesuffix('acheron/')
PAGE_URL=os.environ.get('LP_PROMPTZILLA_URL',BASE+'promptzilla/')
async def main():
 results=[]
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path=installed_chromium())
  for theme in ('light','dark'):
   page=await b.new_page(color_scheme=theme,viewport={'width':1280,'height':800})
   await page.goto(PAGE_URL,wait_until='networkidle')
   await page.evaluate('''() => {window.ratio = (a,b) => {
    const canvas=document.createElement('canvas'); canvas.width=canvas.height=1; const ctx=canvas.getContext('2d',{willReadFrequently:true});
    const luminance=color=>{ctx.clearRect(0,0,1,1);ctx.fillStyle=color;ctx.fillRect(0,0,1,1);const rgb=[...ctx.getImageData(0,0,1,1).data].slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return rgb[0]*.2126+rgb[1]*.7152+rgb[2]*.0722;};
    const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05);
   };window.background=e=>{while(e){let c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent')return c;e=e.parentElement;}return 'white';};}''')
   measurements=await page.evaluate('''() => [...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().width&&getComputedStyle(e).visibility!=='hidden'&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())&&!e.closest('script,style')).map(e=>({text:e.textContent.trim().slice(0,60),ratio:ratio(getComputedStyle(e).color,background(e))}))''')
   states=[]
   for element in await page.locator('a,button').all():
    if not await element.is_visible():continue
    if await element.get_attribute('class')=='lp-skip':continue
    await element.hover(); await page.wait_for_timeout(250)
    states.append(await element.evaluate('e=>({state:"hover",text:e.textContent.trim().slice(0,40),ratio:ratio(getComputedStyle(e).color,background(e))})'))
    await element.focus(); await page.wait_for_timeout(250)
    states.append(await element.evaluate('e=>({state:"focus",text:e.textContent.trim().slice(0,40),ratio:ratio(getComputedStyle(e).color,background(e)),focusRatio:ratio(getComputedStyle(e).outlineColor,background(e.parentElement))})'))
   rules=await page.evaluate('''selectors => selectors.map(s=>{const e=document.querySelector(s);return {selector:s,ratio:ratio(getComputedStyle(e).borderTopColor,background(e.parentElement))}})''',list(RULES))
   results.append({'theme':theme,'minText':min(x['ratio'] for x in measurements),'minState':min(x['ratio'] for x in states),'minFocus':min(x['focusRatio'] for x in states if 'focusRatio' in x),'rules':rules,'failures':[x for x in measurements+states if x['ratio']<4.5]})
   await page.close()
  await b.close()
 Path('.review/promptzilla').mkdir(parents=True,exist_ok=True)
 Path('.review/promptzilla/contrast.json').write_text(json.dumps(results,indent=2)+'\n')
 print(json.dumps(results,indent=2))
 if any(result['failures'] or result['minFocus']<3 or any(rule['ratio']<3 for rule in result['rules']) for result in results):
  raise SystemExit('Contrast check failed')
asyncio.run(main())
