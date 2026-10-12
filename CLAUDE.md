# Landing pages agent guide

## Start here

This repository publishes three standalone static pages from `main`:

| Page | Source | Live URL |
| --- | --- | --- |
| Acheron | `acheron/index.html` | <https://andymccutcheon.github.io/landing-pages/acheron/> |
| Freewhirr | `freewhirr/index.html` | <https://andymccutcheon.github.io/landing-pages/freewhirr/> |
| Shipwatch | `shipwatch/index.html` | <https://andymccutcheon.github.io/landing-pages/shipwatch/> |

There is no root landing page, package install or build step. Preview from the repository root with
`python3 -m http.server 8000`, then open `http://localhost:8000/<page>/`.

## Shared Pattern layer

All pages load the pinned Design System Pattern tokens and the shared landing-page layer. `shared/`
contains generated font declarations, the `--lp-` landing-page token layer, base and motion rules,
`common.css`, and `page.js`. Freewhirr and Shipwatch add `freewhirr.css` and `shipwatch.css`.

The files support one repeated header, footer and copyable install-bar pattern. `page.js` supplies
progressive enhancement for theme selection, copy controls, keyboard scrolling, reveals and Acheron's
media. Keep the pages readable without JavaScript. Marketing-only variables and selectors use the
`--lp-` / `lp-` namespace; `vendor/pattern/` is an immutable snapshot and is replaced as a unit.

## Verification

Start the preview server before browser checks:

```sh
python3 -m http.server 8766
```

Run source and copy checks from another terminal:

```sh
python3 tools/check_literals.py
python3 tools/check_middle_dots.py
node --check shared/page.js
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-acheron-landing-copy-draft1.md
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-shipwatch-landing-copy-draft1.md
```

The copy audit reports differences for human classification; a non-empty report is not itself a
failure. Use the installed repository environment for the browser gates:

```sh
PATH="$PWD/.venv/bin:$PATH" python3 tools/render_check.py
PATH="$PWD/.venv/bin:$PATH" python3 tools/freewhirr_contrast_check.py
PATH="$PWD/.venv/bin:$PATH" python3 tools/shipwatch_contrast_check.py
```

`render_check.py` is the aggregate gate. It captures Acheron at 6 widths in 2 themes (12 captures),
Freewhirr at 4 widths in 2 themes (8 captures), and Shipwatch at 6 widths in 2 themes (12 captures)
plus 2 Shipwatch no-JavaScript captures. It also checks responsive layout, interaction and resilience.
Its Shipwatch regression stage requires byte-identical PNGs for Acheron and Freewhirr at 4 widths in
2 themes: 16 before/after pairs against baseline commit `d42fe89`. Evidence goes under ignored
`.review/`. Do not install dependencies or download browsers merely to run these checks.

## Deployment

`.github/workflows/pages.yml` deploys on relevant pushes to `main`. Its staging step constructs a
fresh artifact from an explicit allowlist: each page's HTML and required Acheron media, the shared
styles/script, and the required Pattern tokens, fonts and licences. It creates `.nojekyll` inside the
artifact. Tools, source documents, agent memory and review evidence are not deployed.

## Adding a page

1. Read the page's binding design brief in
   `/Users/andymccutcheon/Documents/GitHub/design-studio/docs/pattern/landing/` and binding copy in
   `/Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/`.
2. Build on a branch in an isolated Git worktree. Add page-local HTML/assets and only the shared
   Pattern changes the new page actually needs.
3. Extend source, copy, contrast, render, no-JavaScript and regression coverage as applicable.
4. Obtain an independent cross-vendor review of the finished diff and acceptance contract.
5. Merge the reviewed branch into `main`, rerun the gates, then push `origin main`.
6. Add the page and every runtime dependency to the workflow's explicit staging allowlist.

## Known backlog

These are pointers, not implementation specifications:

- **Freewhirr product:** close the two `stop`-policy escape hatches, require limits for paid fallback,
  and add inbound authentication to the proxy. Source:
  `/Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md`,
  especially “Decision 2” and its verification cases.
- **Shipwatch product:** add a direct future-dated exclusion test and address SQLite ordering of ISO
  timestamp text. Current code and adjacent coverage: `shipwatch/src/shipwatch/storage.py` and
  `shipwatch/tests/test_pipeline_e2e.py` in the sibling Shipwatch repository.
- **Freewhirr live Lab:** correct the public Lab copy described in “Decision 2” of
  `/Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md`;
  the live source is `andy-portfolio/src/data/lab.js` on `origin/main`.

## Editing rules

- Keep raw colour, length and duration literals in `shared/lp-tokens.css`, subject to the lint's
  documented exceptions. Do not hand-edit generated `shared/fonts.css`.
- Preserve both themes, no-JavaScript readability, accessible names, keyboard operation and the
  existing regression contract.
- Do not edit the vendored Pattern snapshot in place.
- Run `git diff --check` and the relevant gates before committing.
