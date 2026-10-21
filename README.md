# Landing pages

Four standalone, progressively enhanced product pages. Three publish through GitHub Pages; the
fourth, Ninth Pass, publishes through its own Cloudflare Worker so it can answer on a custom
domain. There is no root landing page and no build step.

| Product | Source | Published page |
| --- | --- | --- |
| Acheron | [`acheron/index.html`](acheron/index.html) | <https://andymccutcheon.github.io/landing-pages/acheron/> |
| Freewhirr | [`freewhirr/index.html`](freewhirr/index.html) | <https://andymccutcheon.github.io/landing-pages/freewhirr/> |
| Shipwatch | [`shipwatch/index.html`](shipwatch/index.html) | <https://andymccutcheon.github.io/landing-pages/shipwatch/> |
| Ninth Pass | [`ninthpass/index.html`](ninthpass/index.html) | <https://ninthpass.amccutcheon.com/> |

## Repository map

- `acheron/`, `freewhirr/`, `shipwatch/` — page HTML and product-local assets.
- `ninthpass/` — the Ninth Pass page: HTML, its own token and layout CSS, its own script and fonts,
  and its three standalone diagrams. It is a standalone design and does not use the shared Pattern
  layer; its design record is `ninthpass/DESIGN.md`.
- `shared/` — the shared Pattern layer: generated fonts, `--lp-` tokens, base and motion rules,
  `common.css`, page-specific `freewhirr.css` and `shipwatch.css`, and `page.js`.
- `vendor/pattern/` — immutable Design System Pattern snapshot pinned in `SNAPSHOT.md`.
- `tools/` — dependency-free source/copy audits and Playwright browser gates.
- `docs/` — implementation reports; these are source documentation, not deployed site content.

Acheron, Freewhirr and Shipwatch use the same header, footer and copyable install-bar pattern. The
shared script adds remembered theme selection, clipboard behavior, keyboard scrolling and
reveal/media enhancement. The underlying content remains readable without JavaScript. Landing-page
additions use the `lp-` selector namespace and `--lp-` custom-property namespace. Ninth Pass has its
own script and its own dark palette. Its three responsive diagrams loop autonomously with a
persistent page-level motion setting; reduced motion and no-script views retain complete explanations.
See `ninthpass/DESIGN.md` and `ninthpass/COPY.md` for the flagship revision's maintained records.

## Preview

From the repository root:

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000/acheron/`, `/freewhirr/`, `/shipwatch/` or `/ninthpass/`.

There is no dependency installation or compilation step. `shared/fonts.css` is generated from the
pinned Pattern snapshot; regenerate it with `python3 tools/generate_fonts.py` instead of editing it.

## Verification pipeline

Source checks:

```sh
python3 tools/check_literals.py
python3 tools/check_middle_dots.py
node --check shared/page.js
```

Copy audit, once per page, using the binding Marketing Engineering draft:

```sh
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-acheron-landing-copy-draft1.md
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-shipwatch-landing-copy-draft1.md
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-20-ninthpass-landing-copy-draft3.md
```

The audit lists visible page/copy differences for human classification; it does not require verbatim
pages. Start a preview server for browser checks:

```sh
python3 -m http.server 8766
```

Then, in another terminal:

```sh
PATH="$PWD/.venv/bin:$PATH" python3 tools/render_check.py
PATH="$PWD/.venv/bin:$PATH" python3 tools/freewhirr_contrast_check.py
PATH="$PWD/.venv/bin:$PATH" python3 tools/shipwatch_contrast_check.py
PATH="$PWD/.venv/bin:$PATH" python3 tools/ninthpass_contrast_check.py
```

The aggregate render gate produces:

- Acheron: 6 widths × 2 themes = 12 captures.
- Freewhirr: 4 widths × 2 themes = 8 captures.
- Shipwatch: 6 widths × 2 themes = 12 captures, plus 2 no-JavaScript captures.
- Ninth Pass: 7 widths (280 through 1440 pixels), plus no-JavaScript, scorecard tabs, clipboard,
  keyboard, local links, reduced-motion and persistent motion-setting checks. For autonomous motion
  and video evidence run `.venv/bin/python tools/ninthpass_render_check.py --motion` with
  `LP_NINTHPASS_URL` set to the local preview URL.

It also exercises responsive layout, clipboard and fallback behavior, keyboard scrolling, theme and
skip controls, reduced motion, long strings and asset budgets. The final regression gate compares
Acheron and Freewhirr at 4 widths × 2 themes and requires all 16 before/after PNG pairs to be
byte-identical to baseline commit `d42fe89`. Acheron's external iframe pixels are masked during the
byte comparison and validated separately by the render gate. Browser evidence is written under
the ignored `.review/` directory.

The three contrast scripts are the explicit contrast gates for Freewhirr, Shipwatch and Ninth Pass.
Do not install packages or download browsers just to run optional local browser checks; use the
existing `.venv` and Chromium installation.

## Deployment

**GitHub Pages.** [`.github/workflows/pages.yml`](.github/workflows/pages.yml) deploys relevant
changes from `main`. It stages a fresh artifact from an explicit file allowlist containing:

- the three page entry points and required Acheron media;
- shared tokens, styles, fonts and `page.js`;
- required Pattern token CSS, font files and font licences; and
- a generated `.nojekyll` marker.

The workflow does not publish tools, implementation reports, agent memory or review evidence. When a
page gains a runtime asset, that file must also be added to the staging allowlist. Ninth Pass is not
in this allowlist.

**Cloudflare Worker.** Ninth Pass publishes from [`ninthpass/cloudflare/`](ninthpass/cloudflare/),
which stages the page and its directories into an assets-only Worker named `ninthpass-site` and
attaches the custom domains. See [`ninthpass/cloudflare/README.md`](ninthpass/cloudflare/README.md)
for the build, the deploy and the reachability check.

## New-page workflow

1. Use the binding design brief from
   `/Users/andymccutcheon/Documents/GitHub/design-studio/docs/pattern/landing/`.
2. Use the binding copy source from
   `/Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/`.
3. Create a branch in an isolated Git worktree and build the page there.
4. Extend the relevant audits and browser/regression gates.
5. Obtain independent cross-vendor review of the completed diff.
6. Merge the reviewed branch to `main`, rerun the gates, and push `origin main`.
7. Confirm the Pages workflow stages the page and every runtime dependency.

## Known backlog

- **Freewhirr product fixes:** make `stop` a true never-spend policy with no configuration escape
  hatches, require guardrails for paid fallback instead of allowing it uncapped, and add proxy
  authentication. Source of truth:
  `/Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md`,
  especially “Decision 2” and the five verification cases.
- **Shipwatch follow-ups:** add a direct future-dated exclusion test and correct the risk from
  lexically ordering ISO timestamp text in SQLite. Current implementation and adjacent test are
  `/Users/andymccutcheon/Documents/GitHub/shipwatch/src/shipwatch/storage.py` and
  `/Users/andymccutcheon/Documents/GitHub/shipwatch/tests/test_pipeline_e2e.py`.
- **Freewhirr live-Lab fix:** update `andy-portfolio/src/data/lab.js` on that repository's
  `origin/main` using “Decision 2” in the Freewhirr copy draft above as the issue record.

These entries are discovery pointers, not implementation specifications; inspect the current product
repositories before changing product behavior.
