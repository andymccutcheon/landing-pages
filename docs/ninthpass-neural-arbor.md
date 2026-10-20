# Ninth Pass — the neural-arbor visualisation

**Status:** built and verified locally. Not deployed. The owner approves before anything goes live.

**Source:** `ninthpass/TASK-neural-arbor-visual.md`. The method is the `neural-arbor` skill, installed
into the Skillreef skill graph on 2026-10-19.

---

## 1. The contract

Filled from the skill's `assets/brief-template.md`:

```yaml
intent: "Show the shape of one pass of the loop: the request descends, Judge branches into
          the three recommendations it wrote, Revise gathers them, the second Judge stops."
semantic_data: "real run bc993584-d18e-4d03-94cd-762e8685d56f, worker fixture. Stage names,
                file names, the 8/10 and 9/10 scores and the three recommendations are the real
                ones. The signal timing is a schedule, and the graphic says so."
archetype: "neural-arbor (rooted cascade with one honest fork)"
root_direction: "top-to-bottom"
visual_reference: "the page's own two diagrams, and the dark chamber they live in"
visual_mood: "The Refinery: warm paper and ink, one oxblood accent, Fraunces, Geist, Geist Mono"
composition:
  root_count: 1
  total_nodes_target: 9
  maximum_depth: 6
  asymmetry: 0.30
  negative_space: "the shoulders either side of the stem, and the gap under the fork"
motion:
  initial_reveal: true
  signal_mode: "a request descends the stem, splits at the Judge, and is gathered by Revise"
  propagation: "causal: a hop never departs before its parent arrives plus the junction delay"
  ambient_motion: "none"
interaction:
  - hover-lineage
  - persistent-selection
  - step-through
  - replay
constraints:
  fps_target: 60
  reduced_motion: true
  seeded_reproducibility: true
output: "a static file in ninthpass/diagrams, embedded in the page"
```

## 2. Topology, and why

The pipeline is a directed structure with one cycle, not a tree and not a force graph. The skill's
table is explicit that a DAG must not be drawn as a tree, so the topology is a **rooted cascade with
one fork and one honest loop-back edge**.

The fork is the product's own: Judge writes a scorecard, and the scorecard's numbered
recommendations are the branches. Revise gathers all three and applies them. That is an hourglass —
a spread at the Judge, a gathering at Revise — and it is the most useful thing the picture can say,
because it is the shape of the loop's work rather than a restatement of the stage list. The loop-back
edge (Judge 2 back to Revise, labelled "BELOW 9 · REWRITE AGAIN") is drawn soft and dashed, because
it is a path the run did not take.

A **tree** would have lost the fork. A **force graph** would have turned six real stages into a
hairball and invented relationships that do not exist. A **layered DAG** would have flattened the
recommendations into another row of boxes, which is exactly what the page's existing run diagram
already does.

## 3. Art direction

- **Ground.** The diagram sits on paper (`#f3efe6`) with the house's 22px dot field at 0.55, the
  same treatment the loop diagram uses. It is embedded in the dark chamber in a light frame, so the
  page's rhythm (paper, chamber, paper) is unchanged.
- **One accent.** Oxblood (`#a84b4b`) marks the scorecard's branches and the 8/10 CONTINUE score.
  The second Judge's 9/10 STOP is the house success green (`#2e6a4b`), because that is the only
  other thing the page says is finished. Nothing else is coloured.
- **Hierarchy.** The spine is strong: filled raised-paper boxes, 176px wide, ink strokes. The
  branch tips are quiet: no fill, a hairline rule, a 9px accent number. The recommendation is a
  twig, not a peer of the stages.
- **Tangency.** Every edge leaves its source going down and arrives at its target from above, so
  the fork reads as one movement rather than three lines that happen to meet.
- **Type.** Fraunces for the title, Geist for the node names, Geist Mono for file names, scores and
  labels. All three are the page's own self-hosted faces; the diagram loads them by relative URL
  exactly as the other two do.
- **Provenance on the face.** The run identifier sits at the bottom left, and "TIMING ILLUSTRATIVE"
  at the bottom right, because the schedule is a schedule.

## 4. How the signals map to the product

The signal is a request in flight. It descends request → Compose → Judge, splits at the Judge into
the three recommendation branches, and is gathered by Revise before the second Judge and the approval.
So the split in the picture is the split the product actually makes, and the fan-in is the fan-in
Revise performs.

Each hop is scheduled from its parent's arrival plus a junction delay, and amplitude decays with
distance and generation. The engine keeps a logical clock and an arc-length table per edge, so a
pulse holds its speed around a curve instead of bunching at the ends.

The timing is a schedule, not a measurement: the run is real, the durations are illustrative, and the
graphic says so.

## 5. Placement: beside, not instead

**Beside.** The two existing diagrams are not replaced.

- `diagrams/loop.html` carries the four-pass story: a step-controlled loop, one axis, four stages.
- `diagrams/dataflow.html` carries how a run executes: fresh processes, the file that crosses each
  boundary, the directory filling up.
- `diagrams/arbor.html` carries the anatomy of a single pass, and in particular the fork that the
  other two do not show.

Replacing either would lose something real. Extending `loop.html` would have conflated two readings
of the same product in one file and put two grammars in one canvas. The new diagram sits in the dark
chamber, directly after the loop diagram, because it is a reading of the loop.

## 6. Iterations

Three iterations after the first working render, each with the three worst flaws named and fixed.
Captures at 1440 and 390, motion on and off, in `.review/arbor/`.

**Iteration 1 — the first render.** Flaws: (1) text overflowed every box, the file names sat on the
bottom borders, and the final box printed two labels on top of each other; (2) the loop-back edge
was invisible because its path started and ended inside the Revise and Judge boxes and the nodes
painted over it; (3) the spine was dead straight, a diagrammatic list rather than an arbor.
Fixes: file names moved under their boxes on a paper mask, one line only; the loop-back re-routed
onto the box edges; the spine given a gentle, seeded asymmetry.

**Iteration 2.** Flaws: (1) the bottom of the canvas was clipped, `prompts/meeting-notes.md` ran off
the edge and the provenance footer was invisible; (2) the loop-back was still unreadable at 1px
dashed `#b6a793`; (3) the composition was unbalanced, the spine drifting right into an empty left
half. Fixes: a compact vertical rhythm that clears the canvas, the final node reduced to one line
(the path, which is the fact that matters); the loop-back taken to the ink tone and 1.1px; the stem
brought back to the centre.

**Iteration 3.** Flaws: (1) no hierarchy — the branch tips were as heavy as the spine, so the eye
could not tell the scorecard's branches from the pipeline; (2) the score crowded the role line in
both Judge boxes; (3) nothing explained the two edge weights. Fixes: the tips went quiet (no fill, a
hairline, a 9px accent number); the score moved onto the name's line and the verdict beneath it; a
legend added that names the stages, the scorecard's recommendations and the loop's return.

A fourth fix fell out of the screenshot review and is worth recording: the reveal never ran, because
the page script referenced an undefined `svg`. The items were hidden by a rule that did not match
the house's own pattern, so the loop-back edge and the footer were invisible in every capture until
it was fixed. The diagram now follows the house contract exactly: items visible by default, dimmed
only once the script takes over, controls hidden until then.

## 7. The four tests

- **Still-frame test.** `motion=static` at 1440 and 390: `.review/arbor/desktop-motion-off.png`,
  `.review/arbor/narrow-motion-off.png`. The composition holds on its own — a stem, a fork, a
  gathering, an approval — with no motion and no pulse.
- **Causality test.** Every pulse travels along a rendered edge. The engine samples each edge's
  arc length and places the head and the tail on that curve, and a hop is scheduled only after its
  parent's arrival plus the junction delay. The fork is the check: three pulses leave the Judge
  along the three drawn branches and are gathered by the three drawn edges into Revise.
- **Truthfulness test.** Stage names, file names, the 8/10 CONTINUE and 9/10 STOP scores and the
  three recommendations are the real ones from run `bc993584-d18e-4d03-94cd-762e8685d56f`, which the
  page already quotes. Nothing was invented. The one thing that is not a measurement — the duration
  of the signals — is labelled "TIMING ILLUSTRATIVE" on the face of the graphic.
- **Replaceability test.** The drawing is generated from one data object, `PIPE`, in
  `tools/build_ninthpass_arbor.mjs`. A different run replaces the data; the rendering code does not
  change. The output is a static file, so the page still ships with no build step and no dependency.

## 8. Verification

- `npm run check` in `ninthpass/cloudflare/` (Node 22.23.1): build stages **19 files** — 18 before,
  the new diagram is the nineteenth — and `cf deploy --dry-run --prebuilt` passes. **Nothing was
  deployed.**
- `npm run verify -- https://ninthpass.amccutcheon.com`: 18 assets answered 200 and the calls to
  action are correct. The new diagram is not on that list because it is not live; it belongs in
  `verify.mjs` at the deploy step, not before.
- `tools/ninthpass_render_check.py`: six captures at 360, 480, 768, 1024, 1280 and 1440, plus the
  no-JavaScript, loop, tabs, clipboard, keyboard, reduced-motion and boundary checks. Gzip 228,783
  of the 240,000-byte budget. The gate's diagram list was updated to the three diagrams the page now
  carries.
- `tools/ninthpass_contrast_check.py`: no text, state, focus or rule failures.
- `tools/check_literals.py` and `tools/check_middle_dots.py`: pass.

## 9. Known limits

- The narrow view is a horizontal crop, because the house diagrams keep a 960px minimum width and
  scroll inside their frame. The new diagram follows the same rule rather than inventing a second
  responsive behaviour; at 390 the reader sees the left third and scrolls.
- Touch was not tested. The hit targets are the boxes themselves, which are large, but no touch
  device was available.
- The diagram is one run. A run that plateaued, or was provisional, would draw a different ending;
  that case is not in the data yet.
- The signals are scheduled, not simulated. They show the order of operations, not their duration.

## 10. Files

- `ninthpass/diagrams/arbor.html` — the shipped diagram, generated.
- `tools/build_ninthpass_arbor.mjs` — the generator and the run data.
- `tools/shoot_ninthpass_arbor.py` — the capture tool used for the review.
- `ninthpass/index.html` — the chamber reference, root-relative.
- `tools/ninthpass_render_check.py` — the diagram list updated to three.
