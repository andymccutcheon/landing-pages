#!/usr/bin/env python3
"""Capture the Ninth Pass arbor diagram at desktop and narrow widths.

Used for the neural-arbor visual review: motion on, motion off, and the
still-frame capture the still-frame test needs. Mirrors the page render gate's
Chromium discovery so no extra dependency is introduced.

    python3 tools/shoot_ninthpass_arbor.py [--url URL] [--out DIR]
"""

import argparse
import asyncio
import os
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_URL = os.environ.get("LP_ARBOR_URL", "http://127.0.0.1:8767/ninthpass/diagrams/arbor.html")
VIEWS = (
    ("desktop", 1440, 900, ""),
    ("desktop-motion-off", 1440, 900, "?motion=static"),
    ("narrow", 390, 844, ""),
    ("narrow-motion-off", 390, 844, "?motion=static"),
)


def installed_chromium() -> str:
    cache = Path.home() / "Library/Caches/ms-playwright"
    candidates = sorted(
        cache.glob("chromium_headless_shell-*/chrome-headless-shell-mac-arm64/chrome-headless-shell"),
        reverse=True,
    )
    if not candidates:
        raise SystemExit("No installed Playwright Chromium executable found")
    return os.fspath(candidates[0])


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--out", default=str(ROOT / ".review" / "arbor"))
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=installed_chromium())
        for name, width, height, query in VIEWS:
            page = await browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
            await page.goto(args.url + query, wait_until="networkidle")
            await page.wait_for_timeout(2200 if not query else 600)
            path = out / f"{name}.png"
            await page.screenshot(path=str(path))
            print(f"wrote {path}")
            await page.close()
        await browser.close()


asyncio.run(main())
