"""Check visible Promptzilla copy and control contrast in installed Chromium."""
import asyncio, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_check import installed_chromium
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=installed_chromium())
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto(os.environ.get("LP_PROMPTZILLA_URL", "http://127.0.0.1:8766/promptzilla/"), wait_until="networkidle")
        await page.locator('.config').evaluate('(e) => e.open = true')
        values = await page.evaluate("""() => {
          const lum = c => { const x=document.createElement('canvas').getContext('2d');x.fillStyle=c;x.fillRect(0,0,1,1);return [...x.getImageData(0,0,1,1).data].slice(0,3).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0) };
          const ratio=(a,b)=>{const x=lum(a),y=lum(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
          const bg=e=>{while(e){const c=getComputedStyle(e).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent')return c;e=e.parentElement}return '#0c0e0d'};
          const nodes=[...document.querySelectorAll('body *')].filter(e=>e.getBoundingClientRect().width&&[...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()));
          return nodes.map(e=>({text:e.textContent.trim().slice(0,50),ratio:ratio(getComputedStyle(e).color,bg(e))}));
        }""")
        await browser.close()
    Path('.review').mkdir(exist_ok=True)
    Path('.review/promptzilla-contrast.json').write_text(json.dumps(values, indent=2)+'\n')
    failures=[x for x in values if x['ratio']<4.5]
    print(f"Promptzilla contrast: {len(values)} text nodes, minimum {min(x['ratio'] for x in values):.2f}:1, failures {len(failures)}")
    if failures: raise SystemExit(json.dumps(failures, indent=2))
asyncio.run(main())
