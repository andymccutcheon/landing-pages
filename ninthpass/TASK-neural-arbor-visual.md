# Task directive — a neural-arbor visualization for the Ninth Pass landing page

**Status:** ready to execute. Written for a coding agent with no prior context.
**Source of truth for the design:** `ninthpass/DESIGN.md` in this repository. Read it first; it
overrides anything summarised here.
**Origin:** requested by the owner of the Skillreef project, which owns the `neural-arbor` skill
this task depends on. That skill was installed into the Skillreef skill graph on 2026-10-19.

---

## GOAL

Build a live, interactive neural-arbor visualization for the Ninth Pass landing page that shows the
product's real pipeline — Brief → Compose → Judge → Revise → Loop — as a branching structure with
causal signals travelling along real edges. Build it by following the `neural-arbor` skill's
process, not by styling a graph to look impressive. The result must read as part of The Refinery
design system, not as a widget dropped onto the page.

## SUCCESS CRITERIA

- The skill's four non-negotiable tests each pass, reported with their actual output:
  - **still-frame test** — a screenshot with motion disabled must hold up on its own;
  - **causality test** — every pulse travels along a rendered edge, with a source, trajectory and
    ending;
  - **truthfulness test** — no data semantics are falsified to make the picture prettier;
  - **replaceability test** — the demo and the real-data interface share one contract, so a real
    run can replace the sample data without touching the rendering.
- You have run the thing and looked at it. At least three iterations, each with the three worst
  visual flaws named and fixed, and each with before/after screenshots: desktop (1440 wide) and
  narrow (390 wide), motion on and motion off.
- The visualization uses the real product content: the five stage names, and the real semantics
  that every stage runs as a fresh process and the output file is the only thing that crosses the
  boundary. Any score, count or timing shown comes from a real engine run that exists, or is
  labeled as illustrative on the face of the graphic.
- The page still builds and verifies: `npm run check` in `ninthpass/cloudflare/` (build plus
  `cf deploy --dry-run --prebuilt`) and `npm run verify` both pass with the new asset in place.
- The visual respects The Refinery dials — DESIGN_VARIANCE 7, MOTION_INTENSITY 5,
  VISUAL_DENSITY 4 — and adds at most one new motivated move to the page's existing four.
  Everything else holds still.

## CONTEXT

- **Executor:** coding agent.
- **Target project:** the `ninthpass/` directory of this repository. The landing page is
  `ninthpass/index.html` plus `ninthpass/css/`, `ninthpass/js/`, `ninthpass/assets/` and
  `ninthpass/diagrams/`. `ninthpass/DESIGN.md` is the design record and the source of truth.
- **The design system, in short** — confirm against `DESIGN.md`, do not trust this summary: warm
  paper and ink, one oxblood accent, Fraunces for display, Geist for body and UI, Geist Mono for
  commands and labels.
- **What already exists.** The page carries two step-controlled diagrams:
  `ninthpass/diagrams/loop.html` (the four-pass refinement loop) and
  `ninthpass/diagrams/dataflow.html` (how a run executes), embedded in iframes in the `#loop` and
  `#output` sections. Read both before you build. Decide deliberately whether the new visual
  replaces, extends, or sits beside them, and say which and why in your write-up.
- **The page is live** at `https://ninthpass.amccutcheon.com`. It is packaged by
  `ninthpass/cloudflare/scripts/build.mjs`, which copies `css/`, `js/`, `assets/` and `diagrams/`
  and rejects any reference that is not root-relative, absolute, a fragment, or a data/mailto URL.
- **The skill.** Read `~/.agents/skills/creative/nodes/visuals/nodes/neural-arbor` — a pointer
  file whose real directory is `~/.agents/.skillreef-store/skills/neural-arbor/`. Every relative
  link inside it resolves from that real directory. It contains:
  - `SKILL.md` — the process in seven steps, and the four non-negotiable tests;
  - `references/` — topologies, art-direction, signal-propagation, engineering, interaction,
    quality-gates;
  - `assets/brief-template.md` — the visualization contract, and `assets/recipes.md` — archetype
    recipes;
  - `examples/neural-arbor/index.html` — a dependency-free example that demonstrates one preset.
    It is not a complete implementation and it is not the deliverable.

## CONSTRAINTS

- Follow the skill's process. Fill in `assets/brief-template.md` as the visualization contract
  before writing any code, choose topology deliberately rather than defaulting to a force graph,
  and read the art-direction, signal-propagation, engineering, interaction and quality-gates
  references for the parts you build.
- Read the skill and its references. Do not improvise a substitute method.
- Do not add a framework, a build step, or a runtime dependency. The page ships static files.
- Do not invent product capabilities, customer claims, testimonials, or performance numbers. Use
  what the repository and a real run actually show, and flag gaps.
- Zero emoji in any output — UI, code, copy, comments, or commit messages.
- Accessibility: `prefers-reduced-motion` must disable ambient and nonessential movement, critical
  controls need keyboard and focus access, and hit zones must exceed the visible dot radius.
- No telemetry, analytics, network calls, or external assets in the visualization.
- Do not modify or delete `ninthpass/diagrams/loop.html` or `ninthpass/diagrams/dataflow.html`
  unless your write-up says why replacing them is better.
- Publishing and deploying require the owner's confirmation. Prepare and verify the implementation,
  then ask before anything goes live.

## DELIVERABLE

- The visualization source file(s), committed in this repository, placed where the build already
  picks them up.
- Screenshots: desktop and narrow, motion off and motion on, plus the still-frame capture used for
  the still-frame test.
- A short design note: the visualization contract you filled in, the topology you chose and why,
  the art-direction decisions, how signals map to the product's real stages, the three flaws you
  fixed in each iteration, the result of each of the four tests, and whether you replaced,
  extended, or sat beside the existing diagrams.
- The actual output of `npm run check` and `npm run verify` from `ninthpass/cloudflare/`.

## STOP WHEN

All four of the skill's tests pass with their real output reported; at least three screenshot
iterations exist with the three named flaws per round; `npm run check` and `npm run verify` in
`ninthpass/cloudflare/` both pass; the new asset is referenced root-relative and the build copies
it; and nothing has been deployed. If a test fails, fix it and re-run — do not report around it.

---

## Open decisions (the owner answers these before the agent starts)

1. **Placement.** Replace the existing loop diagram, extend it, or add a new one? The owner's
   recommendation is a new one in the dark chamber: the existing loop diagram carries the
   four-pass story, and the arbor is a different reading of the same product.
2. **Data depth.** Show a real run's judge scores, or the pipeline structure only? The scores
   require a run that exists and is readable from the project; the structure does not.
