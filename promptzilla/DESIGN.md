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

- Instrument Sans for display, stage names and prose (the page reassigns the shared display
  token; see section 8), JetBrains Mono for commands, indices, provenance and figures.
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
| 3 | How a run ends | Ruled label-and-value rows (four end states) |
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
| How a run ends | Set the expectation that a run can end unapproved | Brief "Outcomes" |
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

## 5. Claim ledger

Every product claim the page makes, with the line in `promptzilla/index.html` that carries
it and the source that supports it. Sources are paths inside the Promptzilla repository at
`/Users/andymccutcheon/Desktop/promptzilla-mcp`. `README.md` is the published contract;
`src/` and `skills/` are cited where they are the stronger evidence, or where the README
summarises what the code enforces.

Line numbers were read at commit time. If a claim on the page cannot be found in this
table, it should not be on the page.

### Hero and specification stamp

| Page | Claim | Source |
|---|---|---|
| 38 | "MCP server", five prompt-engineering skills | `README.md:7-10`; `skills/` has 5 directories |
| 39, 41 | Generates, scores on a locked rubric, rewrites against the numbered recommendations | `README.md:7-10`, `199-204` |
| 41 | "stops only when the rubric scores it 9 or 10" | `README.md:203-204`; `src/validation.ts:40` enforces `(score >= 9) !== (verdict === 'STOP')` |
| 42 | "The connected AI client executes the skills, so there is no API key and no model-provider account" | `README.md:12-15` |
| 44, 158 | `claude mcp add promptzilla -- npx -y promptzilla` | `README.md:38` (client table) |
| 51 | Transport: "stdio, or self-hosted HTTP" | `README.md:9-10`, `96-97` |
| 53 | Skills: 5 | `README.md:49`; `skills/` directory listing |
| 55, 144, 174 | Tools: 13 | `README.md:43`; tools table `README.md:111-125` has 13 rows |
| 57, 146, 174 | Prompts: 5 | `README.md:43`, `135` |
| 59, 155 | Runtime: Node.js 22.12+ | `README.md:19` |
| 61, 229, 236 | Licence: MIT | `package.json:38`; `README.md:310` |
| 63, 155 | API key: not required | `README.md:15` |

### Pipeline rail

| Page | Claim | Source |
|---|---|---|
| 69-71 | Metapod generates a System Prompt and a Task Prompt from one raw request | `README.md:208-209`; `skills/metapod/SKILL.md:40-60` |
| 74-76 | Judge Dredd: locked 0 to 10 rubric, quoted evidence, STOP or CONTINUE verdict, numbered recommendations | `skills/judge-dredd/SKILL.md:3`, `55-57`; `README.md:210-214` |
| 79-81 | Brian Spillner applies every numbered recommendation and cuts nothing that was not asked for | `skills/brian-spillner/SKILL.md:3`, `58` |
| 84-86 | Judge re-scores the exact rewritten body; at most four scoring rounds | `README.md:200-202` |
| 87 | "Only a valid STOP at an overall rating of 9 or 10 approves the prompt. The server never invents a score and never changes a verdict." | `README.md:203-204`; `src/validation.ts:40` |
| 88 | "The Prompt Pipeline orchestrates these stages. It does not execute them." | `skills/prompt-pipeline/SKILL.md:8` |

### Stage specifications

| Page | Claim | Source |
|---|---|---|
| 96 | Tasker: execution-ready instruction for another agent; unknowns become bracketed placeholders; never performs the task | `skills/tasker/SKILL.md:3`, `8`, `12`, `41-42` |
| 100 | Metapod: "all 11 System headings and all 4 Task headings"; never executes the task | `README.md:209`; `src/validation.ts:26` lists exactly 11 System headings and `:29` exactly 4 Task headings; `skills/metapod/SKILL.md:8` |
| 104 | Judge Dredd: section ratings, one overall rating, a STOP or CONTINUE verdict, numbered recommendations; evaluates only | `README.md:210-214`; `src/validation.ts:41` requires `^Section Ratings$`, `:37` exactly one `Overall Rating`, `:48` sequential recs; `skills/judge-dredd/SKILL.md:3`, `91` |
| 108 | Brian Spillner: full rewrite plus a line for every recommendation marked applied or deferred | `README.md:215-216`; `src/validation.ts:60-63` |
| 108 | "Interior whitespace, Unicode, trailing spaces and line endings are preserved" | `README.md:217` (Brian's output contract) |
| 112 | Prompt Pipeline: Metapod, Judge Dredd, Brian Spillner until STOP at 9 or above, at most four scoring rounds; orchestrates only | `README.md:202-204`; `skills/prompt-pipeline/SKILL.md:8` |

### How a run ends

| Page | Claim | Source |
|---|---|---|
| 122 | STOP at 9 or above: approved, written as the final artifact | `README.md:203-204`, `240`; `src/pipeline-engine.ts:129-130` writes `05-final.md` with `approved: true` |
| 124 | Four-round cap: best scored candidate exported as provisional, `approved: false` | `README.md:196-197`; `src/pipeline-engine.ts:68-74` |
| 126 | No improvement after two rewrites: the run pauses for your decision | `README.md:202-203`, `192` |
| 128 | Blocked: a stage output rejected twice blocks the run; a best scored candidate, if any, may be exported as provisional | `README.md:188-190`, `196-197` |
| 127 | "Pass 1 counts toward the four-round maximum" | `README.md:201-202` |

### Modes and server surface

| Page | Claim | Source |
|---|---|---|
| 136 | `full`: starts at Metapod from a raw request, saved as the run's first file | `README.md:199`; `src/pipeline-engine.ts:50` writes `00-request.md` |
| 139 | `optimize-only`: saves your prompt to `00-original.md` byte for byte, unchanged, and starts at Judge | `README.md:199-200`; `skills/prompt-pipeline/SKILL.md:31`; `src/pipeline-engine.ts:49` |
| 144 | 13 tools: skill packets and the durable pipeline controller | `README.md:111-125` |
| 146 | 5 prompts, one per skill, using the source skill names | `README.md:135-136` |
| 148 | `promptzilla://` resources: the catalog, the exact original skill files, each run's artifacts | `README.md:143-147` |

### Install

| Page | Claim | Source |
|---|---|---|
| 155 | Node.js 22.12 or newer; no API key and no account | `README.md:19`, `15` |
| 162 | The `mcpServers` JSON block, verbatim | `README.md:26-35` |
| 172-173 | `npx -y promptzilla --validate` prints "Validated 5 skills and 9 source assets." | `README.md:49` |
| 174 | A connected client lists 13 tools, 5 prompts and the `promptzilla://` resources | `README.md:43` |
| 177 | Setup skill at `agent-skills/promptzilla-setup`; walks the Node check, client configuration and optional Cloudflare self-hosting | `README.md:60-65` |

### Durable runs

| Page | Claim | Source |
|---|---|---|
| 184 | A folder of Markdown stage files plus `run.json` | `README.md:247-257` |
| 184 | "written with private permissions" | `README.md:248`; `src/file-run-store.ts:14` creates directories `0o700`, `:21` and `:33` create files `0o600` |
| 185 | "Artifacts are immutable" | `README.md:147`, `240`; `src/file-run-store.ts:19-26` writes each artifact with `'wx'` and refuses to overwrite |
| 185 | "Changed stage files are detected" | `src/file-run-store.ts:25` throws `Artifact was modified outside the pipeline`; `README.md:259-261` |
| 185 | "missing derived files are reconstructed from `run.json`" | `README.md:260-261`; `src/file-run-store.ts:58` re-materializes artifacts from parsed state on every read |
| 185 | `pipeline_status` resumes a run after a server restart | `README.md:259`; `README.md:121` |
| 186 | "Runs are stored under your home directory by default" | `README.md:53`, `71`, `247` |
| 191 | `00-request.md`, or `00-original.md` for optimize-only | `README.md:252`; `src/pipeline-engine.ts:49-50` |
| 193 | `01-metapod.md` | `README.md:253`; `src/pipeline-engine.ts:61` |
| 195 | `02-judge-pass1.md` | `README.md:253`; `src/pipeline-engine.ts:64` (round 0) |
| 197 | `03-brian-rewrite.md` | `README.md:253`; `src/pipeline-engine.ts:63` (round 1) |
| 199 | `04-judge-pass2.md` | `README.md:254`; `src/pipeline-engine.ts:64` (round 1) |
| 201 | `05-final.md`, or `05-provisional.md` at a cap | `README.md:256-257`; `src/pipeline-engine.ts:129`, `:72` |

### What Promptzilla does not do

| Page | Claim | Source |
|---|---|---|
| 208-209 | Standalone tools return instructions and input packets; they do not secretly call an LLM; the server cannot create isolated AI workers itself | `README.md:12-14`, `160` |
| 213 | Fresh worker per stage is the host's obligation; the server records attestations, validates returned output, enforces loop limits | `README.md:13-15` |
| 213 | "rejects reused execution identifiers" | `README.md:190` ("Stale dispatches and reused worker IDs are rejected") |
| 214 | Unique identifier and fresh-context flag are recorded attestations, not a sandbox or proof of separate model execution | `README.md:162-163` |
| 214 | "A host without fresh-context workers has to pause the run with a blocker" | `README.md:160-161` |
| 217 | Scorecards validated for structure and consistency, not semantic truth, completeness of evidence or model quality | `README.md:130-131` |
| 217 | Structural acceptance does not verify a rewrite preserved every fact or implemented its recommendations; those remain worker and Judge duties | `README.md:221-223` |
| 220 | Exact fixes are never inferred from a scorecard | `README.md:228`, `237-238` |
| 220 | Each pair must match a quoted replacement in a Judge recommendation | `README.md:238-239`; `src/validation.ts:52-55` (`isAuthorizedFix`); `src/pipeline-engine.ts:179-181` |
| 220 | Each old string must occur exactly once | `README.md:239`; `src/validation.ts:69` |
| 220 | "All of them succeed or none are written" | `README.md:240`; `src/validation.ts:67-73` replaces into a local copy and throws before anything is persisted |
| 220 | "stays unapproved until a fresh Judge confirms the diff" | `README.md:241`; `src/pipeline-engine.ts:185` sets `approved: false, label: 'Pending fresh Judge diff-only confirmation.'` and `:120-124` only approves after a passing confirm stage |
| 223 | Run data stays on disk until you remove it and can contain your prompt text; the server does not send prompt data to external services | `README.md:271-273` |
| 223 | "a single-user service over standard input and output, with filesystem permissions as its access boundary" | `README.md:270-271` |

### Status and footer

| Page | Claim | Source |
|---|---|---|
| 229 | Version 1.0.0 on npm under the MIT licence | `package.json:3`, `:38`; `README.md:308` |
| 229 | Continuous integration runs on Node 22, 24 and 26 | `README.md:291` |
| 230 | Optional private, authenticated HTTP server on your own Cloudflare account, Workers and Durable Objects, no database and no model API | `README.md:96-98` |
| 240 | "Install from npm" links to the npm package | `README.md:308` |
| 243 | "Self-hosting guide" links to `CLOUDFLARE.md` | `README.md:99` |

### Corrections this ledger forced

Building the ledger caught one misattribution and one loose number, both now fixed:

- **Rewritten.** The `optimize-only` row carried "Interior whitespace, Unicode, trailing
  spaces and line endings are preserved". That sentence is `README.md:217`, which is
  **Brian's output contract** for the rewritten body, not a statement about how an
  optimize-only run stores your input. The mode row now says only what
  `README.md:199-200` and `skills/prompt-pipeline/SKILL.md:31` support, and the
  preservation guarantee moved to the Brian Spillner specification row where it belongs.
- **Tightened.** The hero said the pipeline "stops when the score reaches 9". The enforced
  condition is a STOP verdict at an overall rating of 9 or 10
  (`src/validation.ts:40`), so the hero now says "stops only when the rubric scores it
  9 or 10", matching the gate row.

Nothing was removed: every other claim audited is literally supported by the cited source.

---

## 6. Where a loaded skill was overruled

The taste skills disagree with each other and with this repository. Where they conflict,
repository conventions, accessibility and performance win. Each override is deliberate:

| Skill | Instruction | Decision |
|---|---|---|
| `gpt-taste`, `high-end-visual-design`, the GSAP skills | Mandatory GSAP ScrollTrigger pinning, card stacking, scrubbed text reveals | **Rejected.** This repository ships no build step and no third-party runtime; the pages must stay readable without JavaScript and respect reduced motion. Scroll pinning also fights the sticky section headings. |
| `gpt-taste` | Tailwind utility classes, `py-32 md:py-48` | **Rejected.** Styling goes through the `--lp-` and `--ds-` token layers; `tools/check_literals.py` rejects raw lengths outside `shared/lp-tokens.css`. |
| `gpt-taste` | `picsum.photos` imagery with CSS filters | **Rejected.** No external requests and no trackers. The page ships zero raster images; the only graphic is an inline SVG. |
| `gpt-taste` | Fonts must be Satoshi, Cabinet Grotesk, Outfit or Geist | **Partly accepted.** No new font is added: the pinned Pattern snapshot's Instrument Sans and JetBrains Mono stay. Fraunces was dropped from this page in the section 8 revision (`design-taste-frontend` bans it as a default display serif). |
| `high-end-visual-design` | Double-bezel nested cards, `backdrop-blur`, glass surfaces, floating pill navigation | **Rejected.** Wrong register for a spec sheet, and `impeccable-frontend-design` bans decorative glass outright. Depth here comes from hairline rules and one strong rule. |
| `impeccable-frontend-design` | "Do not use monospace as lazy shorthand for technical vibes" | **Partly accepted.** Monospace is used only where it carries meaning: shell commands, JSON, filenames, stage indices, provenance and the specification values. Prose is never monospace. |
| `design-taste-frontend`, `design-taste.md` | Never repeat a layout archetype | **Accepted**, with one deliberate rhyme: the rail and the outcomes band are both ledgers, which is system coherence rather than monotony. |
| `ux-writing` | Error and empty-state formulas | **Not applicable.** The page has no forms and no stateful UI. Its button and copy-feedback copy comes from the shared `page.js`. |
| `cro` | Add social proof and trust badges above the fold | **Rejected.** The brief forbids social proof. The hero's specification stamp and the limits section do the trust work instead. |
| Repository `CLAUDE.md` | "Add the page and every runtime dependency to the workflow's staging allowlist" | **Deferred.** The acceptance contract forbids touching `.github/workflows/pages.yml`, and this page deploys to Cloudflare, not GitHub Pages. If it is ever published alongside the other three, the workflow needs `promptzilla/index.html`, `promptzilla/css/promptzilla.css` and `promptzilla/assets/favicon.svg` added. |
| Repository precedent (`shared/freewhirr.css`, `shared/shipwatch.css`) | Page stylesheets live in `shared/` | **Overruled** by the acceptance contract, which specifies `promptzilla/` with `css/`. Keeping this page's CSS out of `shared/` also guarantees it cannot affect the three published pages, and it keeps the Cloudflare staging allowlist smaller. `tools/check_literals.py` was extended to lint `promptzilla/css/*.css`, so the gate still covers it. |
| Acceptance contract item 1 ("index.html + css/js/assets") | A page-local JavaScript file | **Not created.** Theme switching, clipboard copy with a manual-selection fallback and keyboard scrolling all come from `shared/page.js`. A page-local script with no job would be dead weight. The one page-specific interaction that was considered, a stepper walking a worked example of the loop, was dropped because it would have required inventing scores, which the brief forbids. |

---

## 7. Self-critique against the taste checklists

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

## 8. Verification

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

Every gate resolves its URL the same way: `LP_TEST_URL` names the one preview server
(default `http://127.0.0.1:8766/acheron/`), and each page gate derives its own page from
that, or takes an explicit `LP_PROMPTZILLA_URL`, `LP_FREEWHIRR_URL` or `LP_SHIPWATCH_URL`.
If port 8766 is taken, serve on another port and point every gate at it with one variable:

```sh
python3 -m http.server 8790 --bind 127.0.0.1
LP_TEST_URL=http://127.0.0.1:8790/acheron/ PATH="$PWD/.venv/bin:$PATH" python3 tools/render_check.py
LP_TEST_URL=http://127.0.0.1:8790/acheron/ PATH="$PWD/.venv/bin:$PATH" python3 tools/promptzilla_contrast_check.py
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

---

## 8. Revision after the Taste pre-flight audit (2026-10-16)

An independent `design-taste-frontend` audit scored the first build 7/10 for taste and 6/10 for
conversion clarity. A separate claims audit against the public repository found no wrong claims.
Changes:

- **Hero leads with the outcome.** The H1 is now "Stop hand-writing your prompts." The lead is cut
  from two paragraphs (56 words) to 20 words: "Your AI client drafts the prompt, scores it on a
  locked rubric and rewrites it. Only a 9 or 10 passes." The client still does the work (README
  lines 12 to 15), and "no API key" stays in the stamp.
- **One label per intent.** Both primary CTAs read "Get it on GitHub". The hero's redundant
  "Install" text link is gone, because the install bar sits directly beneath. Footer labels are
  shortened to GitHub, README, npm package, Issues, License and Self-hosting guide.
- **CTA label alignment.** `.lp-promptzilla a` set `display: inline-block` and overrode
  `.lp-button`'s `inline-flex`, so the label sat high in the button. The rule now excludes
  `.lp-button`.
- **Hero install command on phones.** Below 48rem it wraps instead of clipping, so the whole
  command is visible before copying.
- **Single sans family.** The page reassigns `--ds-font-family-display` to the text face, and
  headings use the semibold weight. The Fraunces preload is removed, so the page downloads one
  font fewer. Other pages are unaffected, because the override is scoped to `.lp-promptzilla`.
- **Outcomes are complete and no longer a three-up row.** The section is now "How a run ends",
  with four ruled rows that include `blocked`, which was missing. This also removes the
  three-equal-columns pattern.
- **Copy.** "Asks you the actual question" becomes "pauses for your decision". Spelling is now
  American throughout (License).
- **Wordmark lockup gap.** The same `a` rule also turned the header lockup into `inline-block`,
  so the mark touched the name. The rule now excludes `.lp-lockup`, and the lockup link keeps its
  44px minimum target height.
- **Wrap point.** On phones the command breaks only at the space before `--`. It used to split the
  `--` flag separator across two lines. The copied text is unchanged.
