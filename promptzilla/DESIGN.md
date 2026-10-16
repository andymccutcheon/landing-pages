# Promptzilla landing page: content plan, positioning and design direction

Direction: **Editorial Engineering**. One of two competing directions built for this page;
the other lives on a separate branch. This document records the process this branch
followed, the decisions it made, and the places where a loaded skill was overruled.

Every product claim on the page is traceable to
`/Users/andymccutcheon/Desktop/promptzilla-mcp/README.md` or to the shared brief at
`landing-pages-wt/.polly/promptzilla-brief.md`. Nothing else is asserted.

---

## 1. Process

Two Symphonia formations shaped the order of work:

- **Pomelo** (positioning and go-to-market) for section 2 below: competitive frame, the
  before-and-after story, the conversion path, and the friction audit.
- **Grapefruit** (landing-page builder) for sections 3 to 5: content plan, then an
  explicitly chosen design direction, then a quality gate before shipping.

Both formations are written for an internal BlockCell host, with a `blockcell-deploy.sh`
step, a `BLOCKCELL_REGISTRY.json` and a `workspaces/<formation>/` layout. None of that
exists here. The deviations are deliberate:

| Formation step | What happened instead |
|---|---|
| `workspaces/grapefruit/outputs/<session>/site/` | The page lives at `promptzilla/`, the repository's own convention. |
| `_internal/content-plan.md`, `_internal/launch-strategy.md` | Folded into this file, so the plan ships beside the page. |
| Pomelo "social proof section with anonymized user quotes" | **Dropped.** The brief forbids testimonials, user counts and logos. Trust is carried by the limits section instead. |
| Pomelo "real UI screenshots" / "sample output" | **Dropped.** No approved sample before-and-after output exists. Flagged as a gap. |
| `skills/blockcell/design-excellence.mdc` design directions | Replaced by the repository's own Pattern layer and the direction in section 3. |
| BlockCell deploy and registry | Replaced by `promptzilla/cloudflare/`, a static-assets Worker driven by the `cf` CLI. |
| Execution-mode choice, multi-round agent critique loop | Compressed into one build and the self-critique in section 6. |

---

## 2. Positioning

**Audience.** AI builders who already run an MCP client and want high-quality prompts
without hand-writing each one, and without first learning to build an agent loop.

**Category.** A prompt-engineering MCP server with a durable optimization pipeline.

**Competitive alternatives.** Writing each prompt by hand. Pasting a "make this prompt
better" instruction into a chat. Keeping a folder of prompt templates. Building the
generate-score-rewrite loop yourself with your own orchestration.

**Unique attributes**, all from the README:

- Five named skills exposed as 13 tools, 5 prompts and `promptzilla://` resources.
- A locked 0 to 10 rubric with quoted evidence, a STOP or CONTINUE verdict and numbered
  recommendations, rather than an unexplained "improved" prompt.
- A durable controller: a run is a directory of Markdown stage files plus `run.json`, with
  restart recovery through `pipeline_status`.
- Hard loop limits: at most four scoring rounds; only a valid STOP at 9 or 10 approves.
- The connected client executes the skills, so no API key and no model-provider account.

**Value, in the buyer's terms.** You get a prompt that passed a published rubric, plus the
scorecard that approved it, without building or running the loop.

**The before-and-after.** Before: you write a prompt, it half works, you tweak it, and you
have no record of why the current version is the current version. After: you state the
request, the client walks a bounded loop, and the approved prompt arrives with its
scorecard and every intermediate stage on disk.

**Objections handled on the page.** "Is this just another wrapper that calls an LLM for
me?" (no: the client executes the skills, and the server cannot create isolated workers).
"Does it guarantee a better prompt?" (no: structure is validated, not truth). "Where does
my prompt text go?" (your disk; the server does not send it anywhere).

**Conversion path.** One primary action, repeated twice and nowhere else: the GitHub
repository. The install command and the client JSON are the secondary, zero-commitment
action, both copyable in one click.

---

## 3. Design direction

**Editorial Engineering.** A light, precise technical document. The page should read like
a datasheet written by the engineer who built the thing: ruled rows, a standing heading
beside its specification, monospace provenance in the margin, and no persuasion that the
facts do not support. This matches the README's deliberately disclaimer-honest voice, and
it is the opposite of a generic AI SaaS template.

**Materials**, all from the pinned Design System Pattern snapshot already in this
repository. No new fonts, no new palette, no external assets:

- Fraunces for display and for the stage names, Instrument Sans for prose, JetBrains Mono
  for commands, indices, provenance and figures.
- The warm-neutral surface and single teal accent from `vendor/pattern/generated/tokens.css`.
  Both themes ship; neither is an inversion of the other, because the Pattern defines both.
- Hairline rules and a single strong rule for structural separation. No cards, no drop
  shadows, no glass, no gradients.

**Signature devices**, in the order a reader meets them:

1. **An original wordmark.** A hairline square stamp containing a Z whose top bar carries
   three dorsal ticks: an engineering stamp that reads as a crest without becoming a
   mascot. Inline SVG using `currentColor`, so it themes for free, costs no request, and
   scales. The same mark is the favicon, with its own `prefers-color-scheme` block.
2. **The datasheet stamp.** The hero's top right is a ruled specification block: transport,
   skills, tools, prompts, runtime, licence, API key. It states what the thing is before
   any argument about why it is good.
3. **The pipeline rail.** The central story, as the brief requires: four numbered stations
   (Metapod, Judge Dredd, Brian Spillner, back to 02) under a strong rule, closed by a
   full-width **gate** row carrying the one condition that matters, the valid STOP at 9 or
   10. It is a semantic ordered list styled with CSS, not an image, so it is readable,
   selectable, translatable, themeable and weighs nothing.
4. **Margin provenance.** Specification rows carry a monospace source note in the margin
   (`skills/judge-dredd`, and so on). The page cites itself, which is both the honest-
   engineer voice and a visible answer to "where did this claim come from".

**Layout rhythm.** No two adjacent sections share a composition:

| # | Section | Archetype |
|---|---|---|
| 1 | Hero | Asymmetric copy and stamp, then a full-width rail |
| 2 | What each stage is allowed to do | Standing sticky heading, ruled index rows |
| 3 | Three ways a run ends | Full-width three-up ledger band |
| 4 | Modes | Content left, aside right |
| 5 | Install | Mirrored: commands left, aside right, heading in flow |
| 6 | Every run is a directory | Editorial stack over a full-width two-column index |
| 7 | What Promptzilla does not do | Ruled full-width heading, two columns |
| 8 | Status | Tinted band, repeated primary call to action |

The rail (four-up) and the outcomes band (three-up) rhyme on purpose: both are state
ledgers, and the system should look like one system.

**Motion.** The shared `motion.css` press and reveal behaviour only. No scroll-driven
choreography, no pinning. Under `prefers-reduced-motion: reduce` the press transform and
every transition are removed, which the aggregate render gate asserts.

---

## 4. Content plan

| Section | Job | Source |
|---|---|---|
| Hero | Name the thing, state the loop, give the two actions, show the specification | README lines 7 to 15, 17 to 51 |
| Pipeline rail | The loop as the central story, ending at the rubric gate | README "Execute a pipeline end to end" |
| Stage specifications | What each of the five skills is allowed to do, and what it refuses | Brief "Five skills"; README "Tools" |
| Three ways a run ends | Set the expectation that a run can end unapproved | Brief "Outcomes" |
| Modes | `full` and `optimize-only`, including the byte-for-byte guarantee | README protocol flow |
| Install | The one-line command, the client JSON, the offline check, the agent skill | README lines 17 to 51 |
| Runs | The durable artifacts, by filename | README "Persistence and recovery" |
| Limits | The five honest refusals, including the attestation caveat | README lines 12 to 15, "Stage output contracts", "Persistence" |
| Status | Version, licence, CI, optional self-hosting; repeat the primary action | README; brief |

Copy rules applied: no exclamation points, no superlatives, no "seamless" or "powerful",
no invented numbers, no em dashes in interface text, no "SECTION 01" filler labels, and no
emoji anywhere. Every number on the page (5, 13, 9, 4, 0 to 10, 22.12, 1.0.0, 22/24/26) is
copied from the README.

**Explicitly not on the page**, per the brief: testimonials, user or star counts,
benchmarks, quality guarantees, a live demo, the private `workers.dev` endpoint, and any
claim that Promptzilla runs or sandboxes agents for you.

---

## 5. Where a loaded skill was overruled

The taste skills disagree with each other and with this repository. Where they conflict,
repository conventions, accessibility and performance win. Each override is deliberate:

| Skill | Instruction | Decision |
|---|---|---|
| `gpt-taste`, `high-end-visual-design`, the GSAP skills | Mandatory GSAP ScrollTrigger pinning, card stacking, scrubbed text reveals | **Rejected.** This repository ships no build step and no third-party runtime; the pages must stay readable without JavaScript and respect reduced motion. Scroll pinning also fights the sticky section headings. |
| `gpt-taste` | Tailwind utility classes, `py-32 md:py-48` | **Rejected.** Styling goes through the `--lp-` and `--ds-` token layers; `tools/check_literals.py` rejects raw lengths outside `shared/lp-tokens.css`. |
| `gpt-taste` | `picsum.photos` imagery with CSS filters | **Rejected.** No external requests and no trackers. The page ships zero raster images; the only graphic is an inline SVG. |
| `gpt-taste` | Fonts must be Satoshi, Cabinet Grotesk, Outfit or Geist | **Rejected.** The pinned Pattern snapshot supplies Fraunces, Instrument Sans and JetBrains Mono, self-hosted with their licences. Consistency across the four pages outranks a font preference. |
| `high-end-visual-design` | Double-bezel nested cards, `backdrop-blur`, glass surfaces, floating pill navigation | **Rejected.** Wrong register for a spec sheet, and `impeccable-frontend-design` bans decorative glass outright. Depth here comes from hairline rules and one strong rule. |
| `impeccable-frontend-design` | "Do not use monospace as lazy shorthand for technical vibes" | **Partly accepted.** Monospace is used only where it carries meaning: shell commands, JSON, filenames, stage indices, provenance and the specification values. Prose is never monospace. |
| `design-taste-frontend`, `design-taste.md` | Never repeat a layout archetype | **Accepted**, with one deliberate rhyme: the rail and the outcomes band are both ledgers, which is system coherence rather than monotony. |
| `ux-writing` | Error and empty-state formulas | **Not applicable.** The page has no forms and no stateful UI. Its button and copy-feedback copy comes from the shared `page.js`. |
| `cro` | Add social proof and trust badges above the fold | **Rejected.** The brief forbids social proof. The hero's specification stamp and the limits section do the trust work instead. |
| Repository `CLAUDE.md` | "Add the page and every runtime dependency to the workflow's staging allowlist" | **Deferred.** The acceptance contract forbids touching `.github/workflows/pages.yml`, and this page deploys to Cloudflare, not GitHub Pages. If it is ever published alongside the other three, the workflow needs `promptzilla/index.html`, `promptzilla/css/promptzilla.css` and `promptzilla/assets/favicon.svg` added. |
| Repository precedent (`shared/freewhirr.css`, `shared/shipwatch.css`) | Page stylesheets live in `shared/` | **Overruled** by the acceptance contract, which specifies `promptzilla/` with `css/`. Keeping this page's CSS out of `shared/` also guarantees it cannot affect the three published pages, and it keeps the Cloudflare staging allowlist smaller. `tools/check_literals.py` was extended to lint `promptzilla/css/*.css`, so the gate still covers it. |
| Acceptance contract item 1 ("index.html + css/js/assets") | A page-local JavaScript file | **Not created.** Theme switching, clipboard copy with a manual-selection fallback and keyboard scrolling all come from `shared/page.js`. A page-local script with no job would be dead weight. The one page-specific interaction that was considered, a stepper walking a worked example of the loop, was dropped because it would have required inventing scores, which the brief forbids. |

---

## 6. Self-critique against the taste checklists

Checked against the pre-flight list in `ux-ui-agent-skills/taste/design-taste.md` and the
DON'T list in `impeccable-frontend-design`:

- Headline wraps to 2 lines at every width from 360 to 1680, asserted by the render gate.
- No two adjacent sections share a column structure. See the table in section 3.
- Body measure is capped at the Pattern's 68ch; the lead is capped at 44ch.
- One accent, the Pattern teal, used for links, the primary button, the focus ring and the
  stage role labels. Neutrals carry everything else.
- No pure black or pure white: every surface and text colour is a warm-neutral OKLCH token.
- Spacing hierarchy runs outer to inner: section, then group, then row.
- Depth is hairline rules and one strong rule. No shadow anywhere on the page.
- No dead cells: the rail is `auto-fit` with a minimum station width, giving four columns
  at 1024 and wider, two at tablet widths and one on a phone.
- Hover, focus and press states on every control, inherited from the shared layer.
- No emoji, no "SECTION 01" labels, no gradient text, no sparklines, no icon-above-heading
  cards, no modal, no invisible button text.
- Reduced motion removes the press transform and every transition.
- Every value traces to a token; the literal lint proves it.

Known soft spots, left as they are:

- The install bar scrolls horizontally on a phone without a visible fade affordance. A
  gradient mask would need a raw colour literal, and the Copy button is the primary action
  there anyway. This matches the existing Shipwatch behaviour.
- The stage specification rows are dense. That is the point of a datasheet, and the measure
  and rule weights keep them scannable, but it is a deliberate density choice rather than
  an accident.

---

## 7. Verification

Source and copy gates, from the repository root:

```sh
python3 tools/check_literals.py
python3 tools/check_middle_dots.py
node --check shared/page.js
node --check promptzilla/cloudflare/scripts/build.mjs
```

Browser gates, with a preview server on the repository root:

```sh
python3 -m http.server 8766
PATH="$PWD/.venv/bin:$PATH" python3 tools/render_check.py
PATH="$PWD/.venv/bin:$PATH" python3 tools/promptzilla_contrast_check.py
```

`tools/promptzilla_render_check.py` is hooked into the aggregate `render_check.py` the same
way Freewhirr and Shipwatch are. It captures 6 widths in 2 themes plus 2 no-JavaScript
captures, and asserts structure, overflow, headline lines, target sizes, long-string
resilience, that the repeated primary call to action points at the repository, clipboard
behaviour with its manual-selection fallback, the theme toggle, skip-link focus, keyboard
scrolling, reduced motion and the gzip asset budget. The aggregate gate's existing
regression stage still requires byte-identical Acheron and Freewhirr captures, which is
what proves the `shared/common.css` change is inert for the published pages.

Deployment packaging is documented in `promptzilla/cloudflare/README.md`.
