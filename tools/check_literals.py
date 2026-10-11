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


def main() -> int:
    failures = []
    for path in sorted((ROOT / "shared").glob("*.css")):
        if path == EXEMPT or path.name == "fonts.css":
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for kind, pattern in PATTERNS.items():
                if pattern.search(line):
                    failures.append(f"{path.relative_to(ROOT)}:{number}: raw {kind}: {line.strip()}")
    if failures:
        print("Literal lint failed")
        print("\n".join(failures))
        return 1
    print("Literal lint passed: no raw colour, length or duration values outside shared/lp-tokens.css")
    return 0


if __name__ == "__main__":
    sys.exit(main())

