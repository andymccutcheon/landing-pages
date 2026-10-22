# Silverquill baseline and recon record

**Author:** Layla Brower (design role-agent). **Date:** 21 October 2026.
**Directive:** `~/Downloads/Silverquill_Design_Refinement_Directive.md`, item *"Baseline screenshots at
1440×900, 1024×768, 390×844 with a written recon record"*, plus *"Mark tests at 16/24/32 px,
monochrome and reverse, light and dark"*.
**Source of truth:** `landing-pages/ninthpass/` on `main`. **Captured against:** the local preview
server, then re-checked on the deployed page.

## 1. What was captured

Three viewports, each frozen with the page-level motion toggle off so the capture is of a settled
page rather than a moving one. Per viewport: the first screen, the whole page, and the change
ledger, the process section and the install section.

| Viewport | First screen | Whole page | Page height | Evidence |
|---|---|---|---|---|
| 1440×900 | `1440-hero.png` | `1440-full.png` | 9,819 px | `.review/silverquill-baseline/` |
| 1024×768 | `1024-hero.png` | `1024-full.png` | 8,937 px | `.review/silverquill-baseline/` |
| 390×844 | `390-hero.png` | `390-full.png` | 11,975 px | `.review/silverquill-baseline/` |

Measurements are in `.review/silverquill-baseline/baseline.json`. The capture script is
`tools/capture_silverquill_baseline.py`; it fails on overflow, a missing section, a wrapped
headline, a missing diagram, an unloaded face, an undersized target, a missing scorecard or any
console error.

## 2. What the measurements say

Measured identically at all three widths:

- No horizontal overflow — the document scroll width equals the viewport width exactly.
- Eight sections, one `h1`, one headline of two lines at every width.
- Two diagrams (the feedback fan and the process flow) present and embedded.
- Two scorecards, and five blocks in the change ledger — the same five recommendations the judge
  wrote and the revision applied.
- Both primary calls to action point at the same repository, and no interactive target is under
  24 pixels.
- All three faces load: Geist, Fraunces and Geist Mono.
- No console errors and no page errors at any width.

**What I judged by eye, which no script can measure:**

- At 1024×768 the hero is a two-column composition: the promise and its qualification on the left,
  the action on the right. The gap between the columns is wide but the reading order is unbroken,
  and the primary action still sits above the fold.
- At 390×844 the header reduces to the wordmark, "Start" and the motion toggle; the eyebrow wraps
  to two lines, the headline holds at two, and the primary action sits above the fold.
- The mobile page is nearly twice the height of the desktop page (11,975 px against 9,819 px) —
  the same content, recomposed rather than cut. Nothing is missing at 390.

## 3. Mark tests

The sheet is `brand/silverquill/mark-size-tests.html`, captured by `tools/capture_mark_tests.py` into
`.review/silverquill-mark/`. Four treatments at 16, 24 and 32 pixels, plus 64 and 128 for
reference: the two-colour mark on the product ground, the one-ink mark on paper, the **one-ink
mark with the slit cut out** (`marks/nib-mono.svg`), and the **mark reversed out of a solid**
(`marks/nib-reversed.svg`).

The two forms are new. The one-ink form exists because the original drawing painted the interior
slit in the ground colour, which means it cannot be stamped in a single ink — the slit has to be a
cut, not a fill. The reversed form exists because a mark that is knocked out of a solid needs to
survive being small and filled.

**Verdict, at actual size and at 2×:**

| Treatment | 16 px | 24 px | 32 px |
|---|---|---|---|
| Two-colour on the product ground | Holds. The nib reads; the slit is a hairline. | Clean. | Clean. |
| One ink on paper | Holds. | Clean. | Clean. |
| One ink, slit cut out | Holds. The cut reads as a notch in the nib. | Clean. The slit is unmistakable. | Clean. |
| Reversed out of a solid | Holds — the contrast does the work. The stroke survives inside the knockout. | Clean. | Clean. |

Nothing needs a simplified variant below 24 pixels, which is the outcome I wanted: the earlier
"Rule" direction needed one, and that is part of why the nib was chosen. The one caution is that
the reversed form relies on the surrounding solid, so it is a mark for a tile or a printed field,
not for a bare placement on the ground.

## 4. Gates run against this build

| Gate | Command | Result |
|---|---|---|
| Cross-page aggregate render check | `tools/render_check.py` | **Passed** — 12 Acheron captures, 8 Freewhirr, 12 Shipwatch, 7 Ninth Pass widths, 16 byte-identical baseline pairs, plus the scorecard keyboard, clipboard success and refusal, local-link, no-JavaScript, live reduced-motion and focus checks |
| Contrast | `tools/ninthpass_contrast_check.py` | **Passed** — no text, state, focus or rule failure; diagram text measured separately at 280, 390 and 1440 with the real viewBox scale |
| Cloudflare build | `npm run check` | **Passed** — 42 files staged, dry run read 52 from the assets directory |

Two defects in the tooling were found and fixed during this pass, both left by the rebuild:

- `ninthpass/cloudflare/scripts/verify.mjs` still asked for the removed loop diagram and the old
  `meeting-notes` run. It now checks the two live diagrams and both retained runs — 33 files.
- `tools/ninthpass_render_check.py` read the diagram list from a variable that only existed inside
  a function, so its motion pass could not run at all. The list is now a named constant.

## 5. Deployment

Deployed to Cloudflare on 21 October 2026 as version
`ece106f4-9aa7-4c3b-b74b-1bd5bc5b3815` of the `ninthpass-site` Worker, with three custom domains
bound: `silverquill.amccutcheon.com`, `ninthpass.amccutcheon.com` and `promptzilla.amccutcheon.com`.
All three answer 200 for all 33 required files. The canonical URL and the Open Graph tags point at
the new host; the older hosts serve the same page rather than redirecting, so no bookmark breaks.

**Not deployed, and still held:** the GitHub repository rename, the npm publication, and the
installation commands that still say `ninthpass` — because changing the clone URL before the
repository is renamed would print a command that fails.

## 6. Still true

Safari and Firefox were not tested, and neither was a real assistive technology. The page is one
recorded run, not an output-quality benchmark.
