# Landing pages

Private, standalone landing pages for Acheron, Freewhirr and Shipwatch. Acheron is the first implementation. This repository has no remote; nothing is deployed or made public without Andy McCutcheon's specific approval.

The Acheron draft is a static, progressively enhanced page with light and dark themes. Its hero still and two dark explainer frames are deliberately accessible placeholders until approved assets are ready. The page remains readable when JavaScript is unavailable; JavaScript adds remembered theme selection, command copying and in-view reveals.

The dark theme is applied by the `.dark` class on the root `<html>` element. External audit scripts should toggle that class rather than looking for a data attribute.

## Structure

- `acheron/` contains the Acheron page and product-local assets.
- `shared/` contains the landing-page tokens, shared styles, generated browser font declarations and small progressive-enhancement script. Marketing-layer names use the `lp` namespace.
- `tools/` contains dependency-free generation and audit scripts, plus the optional Playwright render check.
- `vendor/pattern/` contains the immutable Design System Pattern snapshot pinned to source commit `0292df0`. Its provenance and hashes are recorded in `vendor/pattern/SNAPSHOT.md`.
- `freewhirr/` and `shipwatch/` are the planned future page locations; neither directory has been created yet.

## Preview

From the repository root, run:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000/acheron/`.

There is no package install or build step. When the pinned Pattern font declarations change, regenerate the browser-safe relative URLs from the repository root:

```sh
python3 tools/generate_fonts.py
```

Do not hand-edit `shared/fonts.css`; the script generates it from the immutable vendored source.

## Checks

Run the dependency-free checks from the repository root:

```sh
python3 tools/check_literals.py
python3 tools/check_copy.py /absolute/path/to/2026-10-11-acheron-landing-copy-draft1.md
```

The copy audit reports visible prose fragments that are not verbatim in the binding copy; its output requires human classification because accessibility and placeholder labels may be intentional additions.

Run the visible-text punctuation check separately:

```sh
python3 tools/check_middle_dots.py
```

The optional render check requires an already-installed Python Playwright package and Chromium. Start a second terminal with `python3 -m http.server 8766`, then run:

```sh
python3 tools/render_check.py
```

It captures light and dark screenshots at 360, 768, 1280 and 1440 CSS pixels under `.review/shots/` and fails on page-level horizontal overflow. The review directory is intentionally ignored by Git.

## Pattern snapshot

`vendor/pattern/` is replaced as a complete unit, never edited in place. Before accepting a replacement, verify every copied file against the hashes recorded in `vendor/pattern/SNAPSHOT.md` and update that record with the new source commit and date.

The page loads `generated/tokens.css` directly. It does not load `generated/theme.css`, because that file targets Tailwind's theme layer rather than a plain browser stylesheet. It also does not load the vendored `generated/fonts.css`; `tools/generate_fonts.py` derives `shared/fonts.css` with relative URLs so previewing works from a sub-path while preserving declared font-weight ranges.

The canonical Acheron guide destination is defined directly on the guide anchors in `acheron/index.html`, the sole configuration file for page destinations. Because the page must work without JavaScript, each guide anchor carries that destination directly; there is no runtime URL rewrite. The two explainer links remain absent until their live addresses exist.

## House rules

- `vendor/pattern/` is a read-only, pinned snapshot. Replace the whole snapshot to update it; never edit files in place.
- Marketing-only pieces live under the `--lp-` namespace in `shared/`.
- A marketing piece is promoted into the Design System Pattern only after two landing pages use it.
- The pages are static HTML and CSS. Small progressive-enhancement scripts are allowed within the documented budget.
- Nothing is deployed or made public without Andy's specific approval.
- Do not add a remote, deploy a page or publish repository content without that approval.
- Run the relevant checks above before committing page changes.

