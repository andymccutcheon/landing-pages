#!/usr/bin/env python3
"""Reject raw colour, length and duration literals outside lp-tokens.css."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXEMPT = ROOT / "shared/lp-tokens.css"
PATTERNS = {
    "colour": re.compile(r"(?<![\w-])(?:#[0-9a-fA-F]{3,8}|(?:rgb|hsl|oklch|lab|lch)\s*\()"),
    "length": re.compile(r"(?<![\w.-])-?(?:\d*\.\d+|\d+)(?:px|rem|em|ch|vw|vh|dvw|dvh)\b"),
    "duration": re.compile(r"(?<![\w.-])-?(?:\d*\.\d+|\d+)(?:ms|s)\b"),
}
LAYOUT_BREAKPOINTS = {"30rem", "48rem", "64rem", "80rem", "90rem"}


def permitted_media_query(line: str, match: re.Match[str]) -> bool:
    """Allow only the five brief-defined query boundaries in base.css."""
    return line.lstrip().startswith("@media") and match.group(0) in LAYOUT_BREAKPOINTS


def main() -> int:
    failures = []
    paths = sorted((ROOT / "shared").glob("*.css")) + sorted((ROOT / "promptzilla/css").glob("*.css")) + [
        ROOT / "acheron/index.html",
        ROOT / "freewhirr/index.html",
        ROOT / "shipwatch/index.html",
        ROOT / "promptzilla/index.html",
    ]
    for path in paths:
        if path == EXEMPT or path.name == "fonts.css":
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for kind, pattern in PATTERNS.items():
                matches = list(pattern.finditer(line))
                if kind == "length" and path.name in {"base.css", "freewhirr.css", "shipwatch.css", "common.css", "promptzilla.css"}:
                    matches = [match for match in matches if not permitted_media_query(line, match)]
                if matches:
                    values = ", ".join(match.group(0) for match in matches)
                    failures.append(f"{path.relative_to(ROOT)}:{number}: raw {kind} ({values}): {line.strip()}")
    if failures:
        print("Literal lint failed")
        print("\n".join(failures))
        return 1
    print("Literal lint passed: no raw colour, length or duration values outside shared/lp-tokens.css or the five reviewed base.css media-query boundaries")
    return 0


if __name__ == "__main__":
    sys.exit(main())

