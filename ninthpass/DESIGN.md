# Ninth Pass landing page — The Refinery

**Status:** live, and repositioned. The page is published as the Cloudflare Worker `ninthpass-site`
and answers on `https://ninthpass.amccutcheon.com` and, during the transition, on
`https://promptzilla.amccutcheon.com`. Source of truth is `ninthpass/` on `main` in
`landing-pages`; the Worker is built from it by `ninthpass/cloudflare/scripts/build.mjs` and is not
published by the GitHub Pages workflow.

**Two states of this record.** Sections 1 to 6 describe the design. Section 7 is the measurement
record, dated. Section 8 is what is still open.

## 1. Read and dials

**Reading this as:** a developer-tool landing page for AI builders — people who already have a
model and an agent, and want the prompt craft to stop being manual.

| Dial | Value | Why |
| --- | --- | --- |
| `DESIGN_VARIANCE` | 7 | Asymmetric hero (7/5), a specimen card that overlaps the grid, and an editorial ledger. The page should feel composed, not templated. |
| `MOTION_INTENSITY` | 5 | Four motivated moves: the hero rise, the loop stepper, the worker tabs, and the command copy feedback. Everything else holds still. |
| `VISUAL_DENSITY` | 4 | A quiet paper surface with generous air. The dense material is the standard and the loop, where the product earns attention. |

## 2. The positioning

**The frame is review, not authoring.** The product's own history was a prompt-writing tool; the
page now sells the part that cannot be faked. A model can write your prompt, and it can also grade
its own homework. This product's Judge runs in a fresh process, never saw the draft, refuses to
rewrite what it grades, and its scorecard is *rejected by the code* unless every section rating
quotes the line that cost the points.

**The headline is the owner's decision:** "Give your agents best-in-class prompts." It obliges the
page to show what best-in-class means, and that is discharged by section 03, which prints the
rubric's twelve sections with the real rating and the real quoted evidence from a real run. The
adjective is never left as an assertion.

**The audience is the operator** — someone who commissions work from an agent and cannot tell
whether a bad result came from the model or from their own instructions. Installing through the
command line or the repository is expected. The non-technical user is the beneficiary of the
promise in the copy, not the addressee.

### 2.1 What the repositioning pass changed (2026-10-20)

1. **The hero shows a real run.** The previous hero used the deterministic test worker, whose score
   is a call counter (`src/workers/fixture.ts:64`) and whose "rewrite" never changes a word of the
   prompt while stamping each recommendation APPLIED. The hero now shows run
   `0becaacc-fb6e-4a92-8951-5106c00edd80`, worker Claude Code, three Judge passes, 8 → 8 → 9.
2. **"Approved" is gone.** It implies a human signed off. In the code it is a boolean set when
   Judge's verdict is STOP and the score is 9. The page says "no human signs off", and the run's
   9 still carries open notes.
3. **The install command resolves.** `npx ninthpass install` appeared three times and 404'd three
   times. The page leads with a clone-and-build path, and names the npm form as the thing that
   will replace it.
4. **A new section, "The shortcut",** names the competitive alternative — ask the model to write
   the prompt and critique it in the same conversation — and says what is missing from it: no
   record, no teeth, no separation.
5. **The five-skills ledger is cut.** It was the product's org chart and it recast the tool as a
   skills collection. The rubric's **twelve sections** take its place, which is what makes the
   headline true.
6. **The honest-limits band moved to second.** It is the strongest asset on the page and it was
   sixth.
7. **The loop widget replays the real run.** Six stages, 8 → 8 → 9, and the button says "Replay
   the run" rather than pretending to be the product.
8. **The real run is committed to the repository** at `examples/runs/meeting-notes/`, so the hero
   artifact is a link a reader can open in ninety seconds.
9. **The neural-arbor diagram was rebound to the real run.** It was built against the fixture run,
   which the page no longer shows. Its generator takes the run as a data object, so it was pointed
   at run `0becaacc`: eight stages, five recommendations, eight steps. The shape improved — the
   real run's second pass also scored 8, so the diagram's "below 9, rewrite again" return is a path
   the run actually took, twice.

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

The page is light-only by choice, not by omission: the two dark palettes of the earlier Alien
build were cut deliberately, and the dark ground now appears only as two bands inside a paper
page — the boundaries band and the loop chamber.

One colour rule is section-specific. The bright accent is the focus colour on the dark chamber; on
the deep paper of the output section it sits at 4.32:1, too close to the ground to read as a ring,
so the focus ring there uses the deep accent at 7.39:1.

### Type

| Role | Face | Size and behaviour |
| --- | --- | --- |
| Display | Fraunces | `h1` `clamp(3rem, 8.2vw, 6.9rem)`, line-height 0.92; `h2` up to 5rem |
| Body | Geist | `clamp(1rem, 0.96rem + 0.18vw, 1.125rem)`, line-height 1.6, 64ch measure |
| Command and label | Geist Mono | 0.7–0.82rem, uppercase labels with 0.16em tracking |

The display size and leading were eased down from `clamp(3.4rem, 10vw, 8rem)` at 0.88 when the
headline grew: at the old size a Fraunces descender landed on the line beneath it.

The italic display phrase is the page's recurring accent: "best-in-class prompts", "to grade its own
homework", "does not", "twelve sections", "not a chat log", "you already trust", "Read the prompt".

### Layout

- 12-column shell, 82rem max width, fluid gutter.
- Hero: copy on columns 1–7, specimen on 8–12. Below 48rem the two stack.
- The standard is a two-column ledger of twelve rows, each a name, a score and the quoted evidence
  that cost the points. Below 48rem it is one column.
- The loop is a full-bleed dark chamber with a readout rail and six stages.
- Output is a split between the run directory, the prompt file itself, and the three end states.

## 4. The argument

1. **Claim: your agent deserves better than a prompt you guessed at.** Proof: the headline and the
   real run beside it.
2. **Claim: the model can grade its own homework; that is not a grade.** Proof: the shortcut
   section — no record, no teeth, no separation.
3. **Claim: the promise is scoped.** Proof: the boundaries band, second, including "no human signs
   off".
4. **Claim: best-in-class is a fixed standard, not an adjective.** Proof: the twelve sections,
   each with its real rating and its real quoted evidence.
5. **Claim: what leaves is a file you can read.** Proof: the run directory, the prompt file
   itself, the approved / provisional / paused rows.
6. **Claim: the loop is real and it does not invent a score.** Proof: the six stages replaying a
   captured run whose middle pass did not improve.
7. **Claim: bring your own model.** Proof: the three worker tabs, each a real command.
8. **Claim: start now.** Proof: the clone-and-build command and two calls to action.

## 5. Preserve list and cut list

**Preserve**

- The primary conversion path: the GitHub repository, reached three times.
- The real product vocabulary: Brief, Compose, Judge, Revise, Loop; `STOP`, `CONTINUE`, `full`,
  `optimize-only`, `provisional`, `paused`.
- No fabricated claims: no customers, counts, benchmarks, testimonials or "try it live".
- Every artifact the page shows is a file in `examples/runs/meeting-notes/`.
- No-JavaScript readability, keyboard operation, reduced motion, visible focus.
- The page's own Cloudflare packaging and reachability check.

**Cut**

- The fixture run and its caption.
- "Approved" in every form.
- The five-skills ledger.
- The npm install command as the primary path, and the footer link to an unpublished package.
- "Prompt-engineering" and "AI builders" as self-description.

## 6. Motion and interaction thesis

- **Hero:** a 900ms staggered rise, copy first, specimen last. No parallax.
- **Loop:** six steps replaying the captured run — Compose, Judge 8, Revise, Judge 8, Revise,
  Judge 9. The score does not move on the second pass, which is why the loop kept going. Under
  reduced motion the page loads at 09/STOP and the button completes instantly.
- **Diagrams:** all three embedded diagrams autoplay their reveal once on load, end complete, and
  offer Play, Pause, Replay, Previous and Next. Each has a complete no-JavaScript frame and a
  complete reduced-motion frame. The browser gate checks this rather than a person.
- **Tabs:** `role="tablist"` with arrow, Home and End support. Only one panel is open.
- **Copy:** 2s "Copied" feedback with an `aria-live` announcement and a manual-selection fallback
  when the Clipboard API refuses.
- **Header:** a scrolled surface change and a scrollspy underline on the section links.

## 7. Verification

Measured on 2026-10-20, after the repositioning pass.

- **Aggregate gate:** `tools/render_check.py` passes across all four pages, including the 16
  byte-identical before/after PNG pairs for Acheron and Freewhirr against baseline commit `d42fe89`.
- **Ninth Pass render gate:** six captures at 360, 480, 768, 1024, 1280 and 1440; no horizontal
  overflow, no small targets, one `h1`, **eight sections**, **six stages**, **twelve rubric rows**,
  three tabs, two primary CTAs to the repository, two diagrams, two artifact cards, and a run
  identifier in the output listing.
- **Loop:** the replay reaches 09 / "STOP / gate passed" with all six stages done and the track at 1.
- **No-JavaScript:** all three worker panels visible; no visible buttons; 09/STOP; the command
  present.
- **Reduced motion:** no hero or stage animations; loop at 09/STOP.
- **Contrast:** no text failures; minimum large-display ratio 3.32:1; minimum interactive state
  4.85:1; minimum focus ratio 3.25:1; gate rule 3.32:1.
- **Gzip:** 230,857 bytes of the 240,000-byte budget.
- **Cloudflare:** `npm run check` stages 19 files and `cf deploy --dry-run --prebuilt` passes.
- **The real run behind the page:** `0becaacc-fb6e-4a92-8951-5106c00edd80`, request "Write a
  prompt for a meeting-notes summarizer that returns five bullets", worker Claude Code, scores
  8/CONTINUE then 8/CONTINUE then 9/STOP, files `00-request.md`, `01-compose.md`,
  `02-judge-pass1.md`, `03-revise.md`, `04-judge-pass2.md`, `03b-revise.md`, `04b-judge-pass3.md`,
  `05-final.md`. The render gate asserts that the page carries a run identifier in that shape and
  that the standard section shows exactly twelve rated sections.

## 8. Open items

- **The install command is a clone-and-build path, not an npm path.** `ninthpass@2.0.0` is not on
  npm; the npm account is in a 72-hour security hold triggered by signing in with a recovery code.
  The durable fix is an authenticator app, which does not trigger the hold. When the package
  publishes, the page should lead with `npx ninthpass install` again.
- **Domain.** `ninthpass.amccutcheon.com` is the interim site and is attached. `ninthpass.com` is
  free to register; the apex would be the permanent address. This is a purchase and waits on Andy.
  The old `promptzilla.amccutcheon.com` is kept attached during the transition.
- **No customer language.** Nobody has ever said what they call this. Every line of copy is the
  company's voice, and it is a hypothesis until five operator interviews say otherwise.
- **No output measurement.** The page claims a standard for the prompt, not a better answer. A
  blinded comparison is the only route to the second claim.
- **The rubric is the project's own.** It is fixed and published, but not validated against human
  raters, and the page does not pretend otherwise.
- **Diagrams.** Three are shipped: the run/data-flow view, the neural-arbor view of one pass, and
  the refinement loop. A panel of nine experts was split on how many the page needs. The arbor
  stays because it shows something the other two cannot — the anatomy of a single pass, with the
  scorecard's recommendations as real branches. The loop diagram is the one that could still go:
  the page now shows the real trajectory in the loop chamber, so the diagram beside it repeats
  what the widget beside it already says.
