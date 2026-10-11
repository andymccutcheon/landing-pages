#!/usr/bin/env python3
"""List visible prose fragments that do not appear verbatim in the binding copy."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hidden = 0
        self.fragments: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            text = " ".join(data.split())
            if text:
                self.fragments.append(text)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: check_copy.py PATH_TO_BINDING_COPY")
    source = normalize(Path(sys.argv[1]).read_text(encoding="utf-8"))
    parser = VisibleText()
    parser.feed((ROOT / "acheron/index.html").read_text(encoding="utf-8"))
    additions = []
    for fragment in parser.fragments:
        if len(fragment) >= 24 and normalize(fragment) not in source and fragment not in additions:
            additions.append(fragment)
    print("Visible prose fragments absent from the binding copy:")
    for fragment in additions:
        print(f"- {fragment}")
    print(f"Copy diff result: {len(additions)} fragment(s) require explanation")
    return 0


if __name__ == "__main__":
    sys.exit(main())

