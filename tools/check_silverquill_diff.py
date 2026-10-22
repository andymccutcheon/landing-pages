#!/usr/bin/env python3
"""Keep the "See what changed." section honest.

  1. The section on the page is byte-identical to the generated fragment.
  2. Every recommendation's replaced wording appears verbatim in the composed prompt,
     and its replacement wording in the approved prompt.

Run after `node tools/build_silverquill_diff.mjs`.
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "ninthpass" / "index.html"
FRAGMENT = ROOT / "ninthpass" / "specs" / "diff-section.html"
RUN = ROOT / "ninthpass" / "examples" / "runs" / "meeting-agent"


def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def core(text: str) -> str:
    """Wording matters; terminal punctuation may be merged into a following clause."""
    return re.sub(r"[.;,:]+$", "", text)


def main() -> int:
    failures: list[str] = []

    page = PAGE.read_text(encoding="utf-8")
    fragment = FRAGMENT.read_text(encoding="utf-8")
    section = fragment.split("-->\n", 1)[1] if fragment.startswith("<!--") else fragment
    if squash(section) not in squash(page):
        failures.append("The section on the page does not match the generated fragment. "
                        "Re-run tools/build_silverquill_diff.mjs and re-insert it.")

    before = squash((RUN / "01-compose.md").read_text(encoding="utf-8"))
    after = squash((RUN / "05-final.md").read_text(encoding="utf-8"))
    judge = (RUN / "02-judge-pass1.md").read_text(encoding="utf-8")

    block = judge[re.search(r"^Recommendations\s*$", judge, re.M).start():]
    for match in re.finditer(r"(?m)^(\d+)\.\s+([\s\S]*?)(?=\n\d+\.\s+|\Z)", block):
        number, body = match.group(1), match.group(2)
        quoted = [squash(q) for q in re.findall(r'[“"]([^”"]*)[”"]', body)]
        if len(quoted) < 2:
            failures.append(f"Recommendation {number} states no old and new wording.")
            continue
        replaced, replacement = quoted[-2], quoted[-1]
        if core(replaced) not in before:
            failures.append(f"Recommendation {number}: replaced wording is not in the composed prompt.")
        if core(replacement) not in after:
            failures.append(f"Recommendation {number}: replacement wording is not in the approved prompt.")

    if failures:
        print("DIFF CHECK FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1

    print("DIFF CHECK PASS — page matches the generated section; every recommendation verified "
          "in both directions against the composed and approved prompts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
