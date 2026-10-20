---
permalink: landing-pages-memory/sessions/2026-10-20-neural-arbor
title: 2026-10-20-neural-arbor
type: note
---

# 2026-10-20 — the Ninth Pass neural-arbor diagram

**Scope:** the Ninth Pass landing page, in this repository. The Skillreef product work that
preceded it lives in `~/Documents/GitHub/skill-graph` and is recorded there.

---

## What was built

A third diagram for the Ninth Pass page, at `ninthpass/diagrams/arbor.html` (33.5 kB, generated).
It shows the anatomy of one pass of the refinement loop: the request descends, Judge branches into
the numbered recommendations its scorecard wrote, Revise gathers them, and the second Judge stops
the loop.

- `ninthpass/diagrams/arbor.html` — the shipped diagram. A static file with inline CSS, inline SVG
  and inline JavaScript. No framework, no build step, no runtime dependency.
- `tools/build_ninthpass_arbor.mjs` — the generator. It holds the run data in one object (`PIPE`)
  and draws the geometry from it, so a different run replaces the sample without touching the
  rendering code.
- `tools/shoot_ninthpass_arbor.py` — the capture tool used for the visual review. It reuses the
  page render gate's Chromium discovery, so it adds no dependency.
- `ninthpass/index.html` — the chamber reference, root-relative, beside the existing loop diagram.
- `tools/ninthpass_render_check.py` — the gate's diagram list updated from two diagrams to three.
- `docs/ninthpass-neural-arbor.md` — the design note: contract, topology, art direction, the
  mapping from signals to the product's stages, the three iterations, the four tests, and the
  verification output.
- `.review/arbor/` — four captures: desktop and narrow, motion on and motion off.

**The data was a real run.** Run `bc993584-d18e-4d03-94cd-762e8685d56f`, worker `fixture`, request
"Write a prompt for a meeting-notes summarizer". The stage names, the file names
(`00-request.md` through `05-final.md`), the 8/10 CONTINUE and 9/10 STOP scores and the scorecard's
three numbered recommendations are the real ones, already quoted on the page.

## Key decisions — and why

- **Beside the two existing diagrams, not instead of either.** `diagrams/loop.html` carries the
  four-pass story; `diagrams/dataflow.html` carries how a run executes, with a fresh process and a
  file on every boundary. Neither shows the fork, which is the shape of the loop's actual work.
  Extending `loop.html` would have put two grammars in one canvas.
- **A rooted cascade with one honest fork and one loop-back edge.** The pipeline is a directed
  structure with a cycle, and a DAG must not be drawn as a tree. A tree would lose the fork; a force
  graph would invent relationships; a layered DAG would flatten the recommendations into another
  row of boxes, which is what the data-flow diagram already does.
- **The fork is the product's own.** Judge writes a scorecard, and the scorecard's recommendations
  are the branches. That hourglass is the most useful true thing the picture can say.
- **Real data, with the one non-measurement labelled.** The scores, files and recommendations are
  real; the *duration* of the signals is a schedule, so the graphic says "TIMING ILLUSTRATIVE" on
  its face, with the run identifier opposite it.
- **Generated from one data object, shipped as a static file.** The replaceability test asks that a
  real run can replace the sample without touching the rendering. A generator gives that; the page
  still ships static files, so the page itself gains no build step.
- **The house motion contract, not a new one.** The two existing diagrams share a contract:
  `data-motion-root`, `data-motion-item` with `data-step`, a `data-motion-controls` group, the
  `?motion=static` and `?motion=step` test hooks, items visible by default and dimmed only once the
  script takes over, and a complete frame with JavaScript switched off. The new diagram follows it
  exactly, controls hidden until the script runs. The reveal is the page's one new motivated move;
  everything else holds still.

## What didn't work

- **A first stylesheet that hid the reveal unconditionally.** The house scopes the hide rule to
  `.motion-ready`; mine was `[data-motion-item] { opacity: 0 }`. The loop-back edge and the
  provenance footer were therefore invisible in every capture, and two iterations were spent on a
  bug in my stylesheet rather than in the geometry.
- **A page script that referenced an undefined `svg`.** In the generated page `svg` is the
  generator's array of fragments, not a DOM node, so `svg.addEventListener` threw and the reveal
  never ran. The house's pattern is `root.querySelector('svg')`.
- **A narrow view that is a crop.** The house diagrams keep a 960px minimum width and scroll inside
  their frame, so at 390 the reader sees the left third. The new diagram follows the same rule
  rather than inventing a second responsive behaviour.
- **A screenshot browser pinned to 500x701**, which made the first captures a crop of the left
  third and the composition impossible to judge. The house's own Playwright setup was used instead,
  at 1440 and 390.
- **The build needs Node 22.18 or newer** (`@cloudflare/config` refuses to load the config on
  Node 18). Use `PATH="$HOME/.nvm/versions/node/v22.23.1/bin:$PATH" npm run check` in
  `ninthpass/cloudflare/`.
- **A stale server held port 8766**, so the first local load 404ed. The review server moved to 8767.

## Patterns learned

- The build rewrites `"diagrams/` to `"/diagrams/` and refuses any `href` or `src` that is not
  root-relative, absolute, a fragment, or a data or mailto URL. A new diagram only has to be
  referenced as `diagrams/name.html` from the page.
- The page render gate hard-codes the list of diagrams, so adding one means updating
  `tools/ninthpass_render_check.py` or the gate fails at all six widths.
- The Cloudflare build now stages 19 files, 18 before this diagram.
- The live reachability check runs against the deployed site, so a new asset cannot join
  `verify.mjs` until it is actually live.
- A peer session worked in this tree on the same day and left uncommitted edits to the same five
  files this work touched. Read `git log` and `git status` before assuming authorship.

## Open work / next steps

1. **Verify and commit the peer's arbor revision.** The working tree holds uncommitted changes that
   re-point the diagram at run `0becaacc` (Claude Code worker, three Judge passes, 8 then 8 then
   9/STOP) with five recommendations. They need the same treatment the first version got: the
   render gate, the capture tool and the design note brought into line, then the build and the
   dry-run deploy re-run.
2. **Update `docs/ninthpass-neural-arbor.md` to the new run.** It still quotes run `bc993584`,
   three recommendations and two Judge passes.
3. **Deploy is the owner's call.** The build is clean and staged; nothing has been deployed. Add
   `/diagrams/arbor.html` to `verify.mjs` at the deploy step, not before.