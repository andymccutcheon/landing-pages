#!/usr/bin/env python3
"""Fail when a visible HTML text line contains more than one middle dot."""

from html.parser import HTMLParser
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


class TextLines(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden = 0
        self.lines: list[tuple[int, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if self.hidden:
            return
        for line in data.splitlines():
            text = " ".join(line.split())
            if text:
                self.lines.append((self.getpos()[0], text))


def main() -> int:
    failures = []
    for name in ("acheron", "freewhirr", "shipwatch", "promptzilla"):
        parser = TextLines()
        parser.feed((ROOT / name / "index.html").read_text(encoding="utf-8"))
        failures.extend((name, line, text) for line, text in parser.lines if text.count("·") > 1)
    if failures:
        print("Middle-dot check failed")
        for name, line, text in failures:
            print(f"{name}/index.html:{line}: {text}")
        return 1
    print("Middle-dot check passed: no visible text line contains more than one middle dot")
    return 0


if __name__ == "__main__":
    sys.exit(main())
