# Reconnaissance — Silverquill page and product

**Author:** Layla Brower. **Date:** 21 October 2026. **Purpose:** the baseline the design-refinement
directive asked for, so later changes can be checked against something real.

## Where things actually live

| Thing | Path | Notes |
|---|---|---|
| The page | `landing-pages/ninthpass/` | **Static HTML, CSS and small progressive-enhancement scripts. No framework, no build step.** Deployed by a Cloudflare assets-only Worker |
| Page records | `ninthpass/{DESIGN,COPY,VERIFICATION}.md`, `ninthpass/specs/` | Design contract, public copy, checks, and the directive response |
| The product | `~/Documents/GitHub/silverquill` | TypeScript CLI, Node 22, Vitest |
| Product entry points | `src/cli.ts`, `src/pipeline-engine.ts`, `src/validation.ts`, `src/state.ts` | Compose → Judge → Revise, staged with a fresh process per stage |
| The skills | `ninthpass/skills/{brief,compose,judge,revise,loop}/SKILL.md` | Installed into agent hosts; `loop` carries the CLI path |
| Brand work | `landing-pages/brand/silverquill/` | Marks, identity record, size tests, go-live checklist |

## Tokens in use (confirmed against `ninthpass/css/pz-tokens.css`)

`ground #151417` · `surface #1e1d21` · `raised #29272d` · `ink #f0eee9` · `secondary #c0bbc4` ·
`muted #a39da8` · `accent #d4ed80` · `rose #dfb1bc` · `olive #282e23`. Fonts: Fraunces (editorial),
Geist (interface), Geist Mono (code), all self-hosted with licences.

## Run provenance

The page's demonstration is `ninthpass/examples/runs/meeting-agent/` — run
`9f3f45e9-18c4-4ecb-a7e4-26042d392f23`, **full mode**, **Codex** worker, 21 October 2026, scores
**8.63 → 9.25 STOP (approved)**, both blocks present. Files copied unchanged; `PROVENANCE.md` records the
source. The earlier `meeting-notes` run (8 → 8 → 9) is preserved on disk but is **not** the published
example: its final artifact fails the structural contract that now exists.

`ninthpass/examples/runs/rough-to-reviewed/` is also retained: an optimize-only run that took a
two-sentence **task directive** from 5 → 9. It is not linked from the page, because the page demonstrates
the loop's job (creating an agent). It is kept as the recorded example of the Brief-side path, so the
distinction between a task brief and an agent specification has evidence behind it.

## Integration points the page depends on

- Two iframes only: `diagrams/arbor.html` (feedback fan) and `diagrams/dataflow.html` (process). The
  loop diagram was removed when the run it described was replaced.
- `tools/build_ninthpass_diagrams.mjs` regenerates the fan and the process diagram from the run's first
  scorecard; it asserts the recorded trajectory.
- `tools/build_silverquill_diff.mjs` generates the change ledger and fails unless every recommendation's
  replaced and replacement wording appear in the composed and approved prompts.
- `tools/check_silverquill_diff.py` fails if the page drifts from the generated fragment.

## Test baseline, as run today

| Check | Result |
|---|---|
| Product unit tests | **65/65 pass** |
| Product build and type tests | pass |
| Installed-package smoke | pass |
| Page render gate, seven widths (280–1440) | **PASS** — no overflow, two-line headline, fonts loaded, primary action on first screen, tab keyboard, clipboard, no-script, reduced motion, focus |
| Page contrast gate | **PASS** — minimum text 5.28:1, interactive and focus states 10.78:1; diagrams 7.8:1 and 9.7:1 |
| Diff integrity gate | **PASS** — five recommendations verified in both directions |

Two gate defects were found and fixed while establishing the baseline: the render gate assumed three
diagrams and the old scorecard tab labels, and the contrast gate treated a translucent tint as an
opaque background (it now composites alpha).

## Open questions

1. **Trademark clearance** in classes 9 and 42 — outstanding; npm, repository rename and page switch all
   wait on it.
2. **npm name reservation** — nothing is published under `silverquill`, so the name is unclaimed.
3. **The 16 px mark** reads as a distinctive glyph rather than a legible nib; accepted deliberately, and
   documented in `brand/silverquill/mark-size-tests.html`.
4. **Cross-browser and assistive-technology testing** — still not performed; all checks above are
   Chromium.
