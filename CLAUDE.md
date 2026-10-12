# Landing pages agent guide

## Purpose

This private, local-only repository holds standalone marketing pages for Andy McCutcheon's open-source tools. Acheron is the approved first page; Freewhirr is the second page, pending independent review. Shipwatch is a future page. Do not create a remote, deploy, or publish anything without Andy's specific approval.

## Structure

- `acheron/index.html` — static Acheron landing page.
- `freewhirr/index.html` — static Freewhirr landing page; scoped additions in `shared/freewhirr.css`.
- `docs/freewhirr-implementation-report.md` — section reconciliation, classified copy audit and verification limits.
- `shared/` — landing-page tokens, shared styles, generated font declarations and progressive enhancement. Keep marketing-layer selectors and variables under the `lp` namespace.
- `vendor/pattern/` — read-only Design System Pattern snapshot pinned to commit `0292df0`; replace the complete snapshot rather than editing any vendored file.
- `tools/` — font generation, raw-literal lint, copy audit and optional Playwright render check.
- `.review/` — ignored local screenshot evidence.

## Commands

```sh
# Preview
python3 -m http.server 8000
# Open http://localhost:8000/acheron/

# Regenerate shared/fonts.css from the immutable snapshot
python3 tools/generate_fonts.py

# Required source checks
python3 tools/check_literals.py
python3 tools/check_copy.py /absolute/path/to/2026-10-11-acheron-landing-copy-draft1.md

# Optional visual/overflow check when Playwright and Chromium are already installed
python3 -m http.server 8766
# In another terminal:
python3 tools/render_check.py
```

Do not install dependencies or download browsers merely to run the optional render check.

## Project rules

- Keep all page styling values tokenized through `--ds-` or `--lp-` variables. Raw colour, length and duration literals belong only in `shared/lp-tokens.css` under the documented exception.
- Treat `shared/fonts.css` as generated output; change `tools/generate_fonts.py` or the snapshot source instead of hand-editing it.
- Keep the documentation-site placeholder in one source location until its real URL exists.
- Preserve no-JavaScript readability and both designed themes.
- Marketing-only pieces are promoted to the Design System Pattern only after two pages use them.

## Recent changes

- Vendored and documented the verified Design System Pattern snapshot at commit `0292df0`.
- Built the first Acheron page draft with light and dark themes, accessible semantic structure, budgeted progressive enhancement and reserved placeholder slots for the hero still and two explainers.
- Added literal lint, copy audit, font generation and optional multi-viewport screenshot/overflow checks.

- 2026-10-12: built Freewhirr; extended source gates to both pages and render gate with Freewhirr checks plus eight Acheron before/after pixel comparisons against `ebccc26`. Existing `.venv` and Chromium suffice; no new dependency. Copy audit chooses page by binding-copy filename.
