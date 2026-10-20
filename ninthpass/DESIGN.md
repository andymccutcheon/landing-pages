# Ninth Pass landing page — The Refinery

**Status:** live. The page is published as the Cloudflare Worker `ninthpass-site` and answers on
`https://ninthpass.amccutcheon.com` and, during the transition, on `https://promptzilla.amccutcheon.com`.
Source of truth is `ninthpass/` on `main` in `landing-pages`; the Worker is built from it by
`ninthpass/cloudflare/scripts/build.mjs` and is not published by the GitHub Pages workflow.

**Two states of this record.** Sections 1 to 6 describe the design. Section 7 is the measurement
record, dated. Section 8 is what is still open.

## 1. Read and dials

**Reading this as:** a developer-tool landing page for AI builders — people who already
have a model and an agent, and want the prompt craft to stop being manual.

| Dial | Value | Why |
| --- | --- | --- |
| `DESIGN_VARIANCE` | 7 | Asymmetric hero (7/5), a specimen card that overlaps the grid, and an editorial skill ledger. The page should feel composed, not templated. |
| `MOTION_INTENSITY` | 5 | Four motivated moves: the hero rise, the loop stepper, the worker tabs, and the command copy feedback. Everything else holds still. |
| `VISUAL_DENSITY` | 4 | A quiet paper surface with generous air. The dense material is the loop and the skill ledger, where the product earns attention. |

## 2. What changed from the Alien build

The page is a full redesign, not a reskin. A second pass then replaced Instrument Serif
with Fraunces and Vermilion with Oxblood, renamed the skills, and added the loop diagram. It
moves from used-future instrument panels, phosphor CRT, Michroma and Share Tech Mono to
a warm editorial refinery:

- **System.** Warm paper and ink, one oxblood accent, Fraunces for display, Geist for body
  and UI, Geist Mono for commands and labels. All faces are self-hosted, Latin-subset
  WOFF2, and used under the SIL Open Font License.
- **Content.** The page sells Ninth Pass v2 — five skills, one install command, a CLI
  that runs each stage in a fresh process, and a Markdown prompt at the end. The v1 MCP
  story (13 tools, 5 prompts, resources, Cloudflare self-hosting, the setup skill) is gone.
  The skills are **Brief, Compose, Judge, Revise, Loop**.
- **Interaction.** The register switch, CRT type-on, stage lamps and the fake-readout are
  gone. In their place: a loop stepper that starts at 08/CONTINUE and reaches 09/STOP, a
  keyboard-operable worker tab set, copy controls on every command, a step-controlled loop
  diagram, a step-controlled run/data-flow diagram, and a dark chamber that gives the loop a
  physical pause in the page.
- **Dependency.** `vendor/alien-ui/` is deleted. The page carries only its own CSS, JS,
  fonts and favicon. The Cloudflare build allowlist is now the page's own directories.

### 2a. What the finishing pass changed (2026-10-19)

1. **A second diagram, drawn from a real run.** `diagrams/dataflow.html` shows how a run
   executes: the request, four fresh processes, the file that crosses each boundary, the
   run directory as it fills, and the approved prompt. Every filename in it is the real
   name the engine writes.
2. **The run on the page is a real run.** The hero specimen, the output directory listing
   and the Judge scorecard are no longer illustrations. They are one run of the real
   engine, captured with the deterministic offline test worker, and the page says so.
3. **A scorecard was added to the output section.** The section's lead promised that
   scorecards stay on disk; now one is shown.
4. **The directory and folder names were renamed** from `promptzilla/` to `ninthpass/`,
   with the two gate scripts renamed to match.
5. **`robots.txt` and `sitemap.xml`** were added at the site root.

## 3. The system

### Colour

All values live in `css/pz-tokens.css`; `tools/check_literals.py` exempts that one file.

| Role | Value | Use |
| --- | --- | --- |
| Paper | `#f3efe6` | page ground |
| Raised paper | `#fbf8f2` | specimen, command strips, file card |
| Deep paper | `#e9e2d6` | the output section |
| Ink | `#1a1513` | text, primary button, dark chamber |
| Ink soft / faint | `#4e4641` / `#6e625b` | body and labels |
| Rule | `#d8cdbe` | hairlines |
| Accent | `#a84b4b` | display italics, rules, focus |
| Accent deep | `#7a2b2b` | small accent text on paper |
| Accent bright | `#d98a7a` | small accent text on the chamber |
| Chamber soft / faint | `#c2b6a4` / `#968a76` | body and labels on dark |
| Success / warning | `#2e6a4b` / `#855416` | status chips on paper |
| Success / warning bright | `#8fbf9f` / `#d8a45b` | status text on dark |

The page is light-only by choice, not by omission: the two dark palettes of the earlier
Alien build were cut deliberately, and the dark ground now appears only as two bands inside a
paper page — the loop chamber and the boundaries band. The rhythm is paper, chamber, paper,
deep paper, paper, chamber, paper.

One colour rule is section-specific. The bright accent is the focus colour on the dark
chamber; on the deep paper of the output section it sits at 4.32:1, too close to the ground
to read as a ring, so the focus ring there uses the deep accent at 7.39:1.

### Type

| Role | Face | Size and behaviour |
| --- | --- | --- |
| Display | Fraunces | `h1` `clamp(3.4rem, 10vw, 8rem)`, line-height 0.88; `h2` up to 5rem |
| Body | Geist | `clamp(1rem, 0.96rem + 0.18vw, 1.125rem)`, line-height 1.6, 64ch measure |
| Command and label | Geist Mono | 0.7–0.82rem, uppercase labels with 0.16em tracking |

The italic display phrase is the page's recurring accent: "your prompts", "One gate",
"each with a narrow job", "not a chat log", "you already trust", "does not do",
"Read the prompt".

### Layout

- 12-column shell, 82rem max width, fluid gutter.
- Hero: copy on columns 1–7, specimen on 8–12. Below 48rem the two stack; the specimen
  loses its offset.
- The loop is a full-bleed dark chamber. On wide screens the readout is a left rail and
  the four stages share the right side; below 64rem they stack, and below 48rem the
  stages become a 2×2 grid.
- Skills are an ordered ledger, not a card grid: index, job, boundary. Hover adds a
  oxblood inset rule.
- Output is a split between the run directory, the Judge scorecard and the three end states.
- Install is a split between the worker tabs and the install aside.
- Boundaries are a short, heavy dark band. Start is the one centred moment.

## 4. The argument

1. **Claim: prompts should not be hand-written.** Proof: the headline, the specimen card
   (a request, four stages, 09/STOP, the output path) and the install command.
2. **Claim: the loop is the product.** Proof: the interactive four-stage loop, the
   step-controlled diagram, the gate rule, the 08 → 09 score change, and the cap/plateau
   note.
3. **Claim: each skill has a narrow job.** Proof: the five-row ledger with explicit
   refusals.
4. **Claim: the output is a readable artifact.** Proof: the run directory listing, the
   Judge scorecard in full, the approved prompt file, and the approved/provisional/paused
   rows. The scorecard is quoted, not described: section ratings, one overall rating, a
   verdict, and numbered recommendations.
5. **Claim: what crosses a stage boundary is a file.** Proof: the run/data-flow diagram.
   Four dashed process boundaries, one file on each arrow, and a run directory that fills
   as the stages run.
6. **Claim: bring your own model.** Proof: the OpenCode, Claude Code and Codex tabs, each
   with a real command and a fresh-process note.
7. **Claim: the limits are honest.** Proof: the four boundary statements — no model call,
   no agent runtime, structure not truth, explicit fixes.
8. **Claim: start now.** Proof: the final install command and two GitHub calls to action.

## 5. Preserve list and cut list

**Preserve**

- The primary conversion path: the GitHub repository, reached twice (hero and final CTA).
- The real product vocabulary: Brief, Compose, Judge, Revise, Loop; `STOP`, `CONTINUE`,
  `full`, `optimize-only`, `approved`, `provisional`.
- No fabricated claims: no customers, counts, benchmarks, testimonials or "try it live".
- The specimen, the directory listing and the scorecard are a real run, and the page says
  which worker produced it.
- No-JavaScript readability, keyboard operation, reduced motion, visible focus.
- The page's own Cloudflare packaging and reachability check.

**Cut**

- MCP, stdio, prompts/resources, 13 tools, Cloudflare self-hosting and the setup skill.
- The industrial register switch and its two dark palettes.
- The CRT bezel, phosphor, type-on engine and stage-lamp animation.
- The vendor Alien UI snapshot.
- The six-section datasheet rhythm; the new page has seven sections with a different
  rhythm: paper, chamber, paper, deep paper, paper, chamber, paper.

## 6. Motion and interaction thesis

- **Hero:** a 900ms staggered rise, copy first, specimen last. No parallax.
- **Loop:** the button steps four stages at 650ms each. The score changes at the second
  Judge pass; the track fills; the stage borders and dots move from pending to active to
  done. "Run again" is always available. Under reduced motion the page loads at 09/STOP
  and the button completes instantly.
- **Loop diagram:** the embedded loop diagram autoplays a five-step reveal once on load,
  ends complete, and offers Play, Pause, Replay, Previous and Next. It has a complete no-JS
  frame and a complete reduced-motion frame.
- **Data-flow diagram:** the embedded run diagram reveals in five steps — the request and
  Compose, Judge, Revise, the second Judge, then the approved prompt and the end states.
  The run directory's rows arrive one per stage, so the directory visibly fills. It has
  the same controls, the same `?motion=static` and `?motion=step` test hooks, the same
  complete no-JS frame and the same complete reduced-motion frame.
- **Tabs:** `role="tablist"` with arrow, Home and End support. Only one panel is open.
- **Copy:** 2s "Copied" feedback with an `aria-live` announcement and a manual-selection
  fallback when the Clipboard API refuses.
- **Header:** a scrolled surface change and a scrollspy underline on the section links.

## 7. Verification

Measured on 2026-10-19, after the finishing pass.

- **Aggregate gate:** `tools/render_check.py` passes across all four pages, including the
  16 byte-identical before/after PNG pairs for Acheron and Freewhirr against baseline
  commit `d42fe89`.
- **Ninth Pass render gate:** six captures at 360, 480, 768, 1024, 1280 and 1440; no
  horizontal overflow, no small targets, one `h1`, seven sections, four stages, five
  skills, three tabs, two primary CTAs to the repository, two diagrams, two artifact cards.
- **Loop:** 08/CONTINUE → 09/STOP; all four stages done; track at 1.
- **No-JavaScript:** all three worker panels visible; no visible buttons; 09/STOP; install
  command present.
- **Reduced motion:** no hero or stage animations; loop at 09/STOP.
- **Contrast:** no text failures; minimum large-display ratio 3.32:1; minimum interactive
  state 4.85:1; minimum focus ratio 3.25:1; gate rule 3.32:1.
- **Gzip:** 228,658 bytes of the 240,000-byte budget.
- **Cloudflare:** `npm run check` stages 18 files and `cf deploy --dry-run --prebuilt`
  passes.
- **The real run behind the page:** run `bc993584-d18e-4d03-94cd-762e8685d56f`, request
  "Write a prompt for a meeting-notes summarizer", worker `fixture`, scores 8/CONTINUE
  then 9/STOP, files `00-request.md`, `01-compose.md`, `02-judge-pass1.md`, `03-revise.md`,
  `04-judge-pass2.md`, `05-final.md`, exported to `prompts/meeting-notes.md` and marked
  approved. The render gate asserts that the page carries a run identifier in that shape
  and that the scorecard still reads `Verdict: CONTINUE`.

## 8. Open items

- **The install command does not resolve yet.** The page's install command is
  `npx ninthpass install`. Until the v2 package is published, that command installs nothing:
  the name `ninthpass` is unclaimed on npm, and the v1 MCP server is published separately as
  `promptzilla@1.0.0`. `ninthpass@2.0.0` is not on npm; the npm account is in a 72-hour security
  hold triggered by signing in with a recovery code. The durable fix is an authenticator
  app, which does not trigger the hold. The GitHub calls to action work today.
- **Domain.** `ninthpass.amccutcheon.com` is the interim site and is attached. `ninthpass.com`
  is free to register; the apex would be the permanent address. This is a purchase and
  waits on Andy. The old `promptzilla.amccutcheon.com` is kept attached during the
  transition.
- **Social proof and a before/after prompt.** The scorecard is now real, but there is still no
  before/after of a prompt's own text and no evidence of use by other people. Add only with
  real material.
- **A third diagram.** The run/data-flow view was the second; nothing is planned beyond it.
