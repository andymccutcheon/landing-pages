---
permalink: landing-pages-memory/sessions/2026-10-21-silverquill-page-switch
title: 2026-10-21-silverquill-page-switch
type: note
---

# 2026-10-21 — the Silverquill page switch, deployed and verified

**Scope:** the Ninth Pass / Silverquill landing page, in this repository. The product rename lives in
`~/Documents/GitHub/ninthpass`; the brand and go-live record live in `brand/silverquill/`.

---

## What was done

The session before this one was interrupted mid-flight with six files modified and uncommitted. The
page has since been finished, gated, deployed and committed.

**The switch.** `silverquill.amccutcheon.com` is now the canonical host. The Worker `ninthpass-site`
was left under its old name and both old hosts (`ninthpass.amccutcheon.com`,
`promptzilla.amccutcheon.com`) keep serving the same build rather than redirecting, so no bookmark
breaks and no custom-domain binding is lost. The page folder was also left alone: renaming it
touches the GitHub Pages allowlist for four other pages, and it buys nothing while the repository
rename is still held.

**Deployed:** Worker version `ece106f4-9aa7-4c3b-b74b-1bd5bc5b3815`, three custom domains bound.
All 33 required files answer 200 on every host, and the page was opened live in a browser with no
console errors.

**Gates, all passing:**

- `tools/render_check.py` — the cross-page aggregate: Acheron's twelve captures, Freewhirr's eight,
  Shipwatch's twelve plus two no-script views, the sixteen byte-identical baseline pairs, and the
  seven Silverquill widths with the scorecard keyboard, clipboard success and refusal, local-link,
  no-JavaScript, live reduced-motion and focus checks.
- `tools/ninthpass_contrast_check.py` — no text, state, focus or rule failure; diagram text measured
  separately at 280, 390 and 1440 with the real viewBox scale.
- `npm run check` in `ninthpass/cloudflare/` — 42 files staged, dry run reads 52 from the assets
  directory.

**Baseline.** Captured at 1440×900, 1024×768 and 390×844 by the new
`tools/capture_silverquill_baseline.py`, with the written record at
`ninthpass/specs/2026-10-21-silverquill-baseline-recon.md`.

**Mark.** Two new forms, because the original drawing painted the interior slit in the ground colour
and so could not be stamped in one ink: `brand/silverquill/marks/nib-mono.svg` (slit cut out) and
`brand/silverquill/marks/nib-reversed.svg` (knocked out of a solid). Tested at 16, 24 and 32 pixels
in four treatments by `tools/capture_mark_tests.py`. The nib holds at every size, which is why the
earlier "Rule" direction, which needed a simplified variant, was not chosen.

## Two defects in the tooling, both left by the rebuild

- `ninthpass/cloudflare/scripts/verify.mjs` still asked for the removed loop diagram and the old
  `meeting-notes` run. It now checks the two live diagrams and both retained runs — 33 files.
- `tools/ninthpass_render_check.py` read the diagram list from a variable scoped to another
  function, so its motion pass could not run at all. The list is now a named constant.

## Still held, and where it bites

The GitHub repository rename and the npm publication remain behind trademark clearance, so the
page's install commands still clone `andymccutcheon/ninthpass` and the primary calls to action
still point at it. That is visible to anyone who visits the page now. The name is also in public
use on three hosts before the search has reported; if it conflicts, the remedy is a copy-and-mark
change plus a redirect.
