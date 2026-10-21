"""Observe frame intervals and long tasks during the actual embedded diagrams.

This is a local Chromium observation, not a promise about device performance.
"""
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright
from render_check import installed_chromium

async def main():
    results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path=installed_chromium())
        page=await browser.new_page(viewport={'width':1440,'height':900})
        await page.goto('http://127.0.0.1:8899/ninthpass/',wait_until='networkidle')
        for name in ('loop','arbor','dataflow'):
            target=page.locator(f'[data-diagram="{name}"]')
            await target.scroll_into_view_if_needed()
            frame=await (await target.element_handle()).content_frame()
            await page.wait_for_timeout(1000)
            sample=await frame.evaluate('''() => new Promise(resolve=>{
              const intervals=[],tasks=[]; let first,last;
              const observer=new PerformanceObserver(list=>tasks.push(...list.getEntries().map(e=>e.duration)));
              observer.observe({type:'longtask',buffered:false});
              const tick=t=>{
                first??=t;
                if(last!==undefined) intervals.push(t-last);
                last=t;
                if(t-first<4000) return requestAnimationFrame(tick);
                observer.disconnect(); intervals.sort((a,b)=>a-b);
                resolve({frames:intervals.length,durationMs:t-first,medianIntervalMs:intervals[Math.floor(intervals.length/2)],p95IntervalMs:intervals[Math.floor(intervals.length*.95)],maxIntervalMs:Math.max(...intervals),longTasksMs:tasks,animationInstances:document.querySelectorAll('animateMotion,animate').length});
              };requestAnimationFrame(tick);
            })''')
            results.append({'name':name,**sample})
        await browser.close()
    out=Path(__file__).resolve().parents[1]/'.review/ninthpass-flagship/performance.json'
    out.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__': asyncio.run(main())
