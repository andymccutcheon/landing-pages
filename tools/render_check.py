#!/usr/bin/env python3
"""Capture required review shots and fail on page-level horizontal overflow."""

import asyncio
from pathlib import Path
import os
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".review/shots"
URL = "http://127.0.0.1:8766/acheron/"
WIDTHS = (360, 768, 1280, 1440)


def installed_chromium() -> str:
    cache = Path.home() / "Library/Caches/ms-playwright"
    candidates = sorted(cache.glob("chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"), reverse=True)
    if not candidates:
        raise SystemExit("No installed Playwright Chromium executable found")
    return os.fspath(candidates[0])


async def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    failures = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True, executable_path=installed_chromium())
        for theme in ("light", "dark"):
            for width in WIDTHS:
                page = await browser.new_page(viewport={"width": width, "height": 900})
                await page.emulate_media(color_scheme=theme, reduced_motion="no-preference")
                await page.goto(URL, wait_until="networkidle")
                await page.evaluate("localStorage.removeItem('lp-theme')")
                await page.reload(wait_until="networkidle")
                await page.evaluate("document.querySelectorAll('.lp-reveal').forEach(element => element.classList.add('is-visible'))")
                overflow = await page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
                dimensions = await page.evaluate("({scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth})")
                if overflow:
                    failures.append(f"{theme} {width}: {dimensions}")
                await page.screenshot(path=OUT / f"acheron-{theme}-{width}.png", full_page=True)
                await page.close()
        await browser.close()
    if failures:
        raise SystemExit("Horizontal overflow: " + "; ".join(failures))
    print("Render check passed: light and dark at 360, 768, 1280 and 1440; no page-level horizontal overflow")


if __name__ == "__main__":
    asyncio.run(main())

