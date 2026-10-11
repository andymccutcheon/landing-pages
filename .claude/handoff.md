# Agent Handoff — landing-pages

**Date:** 2026-10-11, America/Boise  
**Branch:** `main`  
**Last implementation commit:** `32c9537 test(acheron): add copy audit`

## Session Summary

This session created the private, local-only `landing-pages` repository and built the first Acheron landing-page draft from Layla's binding design brief and Katrina's binding copy. The Pattern snapshot is pinned and intact, the static page works in both themes without a framework, and the required local checks pass. The three explainer assets remain explicit placeholders because their approved synthetic content does not exist yet.

## Accomplished This Session

- Vendored the Design System Pattern snapshot at commit `0292df0`, including verified generated outputs, fonts and licences.
- Built `acheron/index.html`, shared token-driven styles, provisional motion recipes and progressive-enhancement JavaScript.
- Added theme persistence, copy-button state, reveal-in-view behavior and a fully readable no-JavaScript path.
- Added tools for relative font CSS generation, literal linting, copy diffing and Playwright screenshots/overflow checks.
- Captured light and dark screenshots at 360, 768, 1280 and 1440 pixels in ignored `.review/shots/`.
- Verified no page-level horizontal overflow at all eight theme/width combinations.
- Proved the literal linter fails on a temporary planted `13px` fixture, restored the file, and reran it successfully.
- Measured 152,018 gzip bytes for the first-load file set and 2,245 raw bytes for the external script.

## In Progress / Incomplete

- The hero still, search-path explainer and storage-path explainer are deliberately labelled placeholders. Do not use Acheron's current explainers because they contain real vault content.
- An independent non-GPT review and Layla's designer review have not run.
- Lighthouse, axe, measured contrast and the unavailable Pattern gate runner have not run.
- The documentation-site destination remains `[DOCS-SITE-URL]` in one `body` data attribute.

## Known Issues and Gotchas

- The pinned snapshot does not contain the `--ds-navigation-*` variables named by the brief. The page uses corresponding existing Pattern semantic tokens. Ask Layla whether the brief or snapshot should be corrected.
- `theme.css` is vendored but not loaded because its Tailwind theme-layer syntax is not a reliable plain-browser stylesheet.
- The copy audit reports 19 fragments; several are false positives caused by Markdown formatting or code-block normalization. Actual additions are accessibility labels, required placeholder explanations, the illustrative response note, the not-live docs-site fallback, and Basic Memory credit lines. No new product claim or benchmark number was added.
- The benchmark command retains `--delay 3.2`; Andy must decide whether a command-line pacing value violates the rule against seconds figures.
- The benchmark has three columns from the copy even though the design component says two; at 360 pixels it scrolls inside a focusable table to prevent page overflow.
- The brief asks for eleven search-path steps, but Katrina's binding copy supplies five. The draft prints the five supplied steps without inventing six more.

## Recommended Next Steps

1. Send the committed diff and acceptance contract to a non-GPT reviewer, then to Layla.
2. Resolve the navigation-token, five-versus-eleven-step and `--delay 3.2` questions.
3. Replace each explicit visual slot when the approved synthetic explainer assets arrive, then remeasure performance and theatre ratio.
4. Run axe, contrast and Lighthouse gates when the Pattern runner is available.

## Architecture and Decisions

- Plain HTML, CSS and JavaScript; no client framework, dependency install or build step.
- `tokens.css` loads directly; `tools/generate_fonts.py` derives relative font URLs from the immutable vendored CSS and retains the `400 700` Fraunces range.
- All page colors and lengths use `--ds-` or `--lp-` tokens. Breakpoint-bound compositions live in `lp-tokens.css` because CSS custom properties cannot be used in media-query conditions.
- Reduced motion keeps hover tint but removes press and reveal transitions, leaving content visible.

## How to Run

```sh
python3 -m http.server 8000
python3 tools/check_literals.py
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-acheron-landing-copy-draft1.md
~/.cache/visual-explainer/venv/bin/python tools/render_check.py
```

The render check expects the page at `http://127.0.0.1:8766/acheron/`; start a static server on port 8766 first.

## Environment Notes

No environment variables, credentials, package installation or network access are required. The repository has no Git remote and must remain private and undeployed until Andy explicitly approves otherwise.

