# Pattern rules

These are the rules every surface built from the Design System Pattern obeys. Each rule has
three parts: the rule, the reason it exists, and the named gate or named review step that
checks it. A rule nobody can check is not a rule, so none is listed here without a checker.

How to read "Checked by":

- **Gate 1 to Gate 7** are the seven gates behind `npm run gates` (run inside `pattern/`):
  Gate 1 token and source lint (checks 1a token graph and output equivalence, 1b source
  literal lint, 1c contracts, 1d rendered intent), Gate 2 accessibility, Gate 3 measured
  contrast, Gate 4 performance budget, Gate 5 AI-tell scan, Gate 6 motion, Gate 7 layout
  integrity.
- **Design review** is the required review layer: five dimensions (philosophy, visual
  hierarchy, detail, functionality, innovation), scored 1 to 10 by a critic from a different
  vendor than the builder, recorded in `docs/pattern/reviews/`.
- **Acceptance review** is the check by the reviewer named for the task in the task manifest,
  against that task's acceptance text.

When two rules pull apart, decide in this order: the person's need, then accessibility, then
consistency, then aesthetics, then developer convenience. A higher tier is never traded for a
lower one.

## Verification

**R01. Never state a number you did not measure. A contrast ratio, a pass, or a count is pasted from gate output, or it is written as "not verified yet".**
Reason: a claimed number that nobody measured is the commonest way a broken surface ships.
Checked by: Acceptance review. The reviewer re-runs `npm run gates` and compares the report with every number claimed.

**R02. A check that cannot run is a failure, not a skip.**
Reason: a gate that prints "skipped" and exits 0 reports success while proving nothing.
Checked by: every gate, Gate 1 to Gate 7, through the gate runner; `npm run test:gates` asserts it against fixtures.

**R03. Nothing measured is nothing passed. A gate that counts zero routes, cells, nodes or animations where the contracts say there are some has failed.**
Reason: an empty page is silent, and silence must not read as green.
Checked by: every gate, Gate 1 to Gate 7; Gate 6 specifically through each variant's `minAnimations`.

**R04. Gates prove correctness, never taste. Every component group and the demo also pass a design review: overall at least 7, no dimension under 6, no open must-fix finding.**
Reason: a surface can pass every measurement and still look generated.
Checked by: Design review, with the record filed in `docs/pattern/reviews/`.

**R05. A model never grades work from its own family. The critic is a different vendor than the builder.**
Reason: a reviewer shares its builder's blind spots when they are the same model.
Checked by: Design review. The record names builder and critic; Acceptance review rejects a same-vendor record.

**R06. A stub never ships. A contract with `"status": "stub"` may pass a single gate with `--allow-stubs` while it is being written, and never passes the full run.**
Reason: stubs let an author iterate; left in, they are untested surface that looks finished.
Checked by: Gate 1 check 1c in the full `npm run gates` run, which fails on any stub and names it.

**R07. Every allow-list entry carries its reason.**
Reason: an exception without a reason is a failure someone hid.
Checked by: the gate that consumes the allow file: Gate 2 for `a11y.allow.json`, Gate 3 for `contrast.allow.json`, Gate 5 for `tells.allow.json`, and Gate 6 for `motion-exceptions.json`.

## Tokens

**R08. No literal values in authored source except Gate 1 check 1b's closed, reasoned allow-list: no authored colour literal, unapproved length or time literal, Tailwind default-palette class, or unapproved arbitrary-value class.**
Reason: a literal is a decision made outside the system, and it will not follow the theme.
Checked by: Gate 1 check 1b.

**R09. Scripts obtain design-system values through `src/lib/tokens.ts`; only the closed literal set allowed by Gate 1 check 1b may be typed directly.**
Reason: a number typed in a script drifts from the token it copied the day the token changes.
Checked by: Gate 1 check 1b.

**R10. One theme, one source of truth. Every emitted style value comes from the token files through the single variable layer; there is no per-page palette.**
Reason: two sources of truth disagree, and the disagreement shows up as a page that looks like another product.
Checked by: Gate 1 check 1a.

**R11. Token by intent. Choose the token whose meaning matches the action. Anything named delete, remove, revoke, discard or destroy wears `color.action.destructive` everywhere it appears.**
Reason: colour is a promise about consequence; a destructive action in the primary colour misleads.
Checked by: Gate 1 check 1d.

**R12. Two type ramps, a text ramp and a display ramp, and both are tokens. No type size exists outside them.**
Reason: one ramp stretched to cover both jobs gives weak headlines or oversized body text.
Checked by: Gate 1 check 1a for emitted token equivalence and check 1b for source literals; Acceptance review checks the authored token inventory against the closed ramps in spec section 2.7.

**R13. No emoji, anywhere: interface, code, data, copy, comments, commit messages.**
Reason: emoji are the strongest single sign of machine-generated work, and they render differently on every platform.
Checked by: Gate 1 check 1d on rendered text; Acceptance review for documents and commit messages.

## Components

**R14. Every component addresses all eight states: default, hover, focus, active, disabled, loading, error, selected. A state that does not apply is written `n/a` with its reason, never left out.**
Reason: the missing state is the one a person meets first in real use.
Checked by: Gate 1 check 1c (the contract declares all eight) and Gate 2 state coverage (the declared cells exist).

**R15. Hover, focus and active are produced by real input in the harness, never by a class that fakes the state.**
Reason: what the gates measure must be what a person gets.
Checked by: Gate 3, which reaches focus by keyboard and drives hover and active with a real pointer.

**R16. Hover never lifts. Hover changes tint only, on pointer devices only; press scales down.**
Reason: hover lift is the heaviest tell of generated interface work, and movement under the pointer makes a target harder to hit.
Checked by: Gate 5 for no lift; Gate 6 for the declared `hover-tint` and `press` recipe behavior; Acceptance review checks pointer scoping.

**R17. Focus is always visible: a `border.width.focus` ring in `color.focus.ring` at the 2px offset declared in spec section 3.1, appearing instantly, at least 3:1 against every surface it can sit on.**
Reason: a keyboard user who cannot see focus cannot use the page, and an animated ring arrives late.
Checked by: Gate 3 for focus-ring contrast and Gate 2 for Tab reachability; Acceptance review checks the width token, section 3.1 offset and instant appearance.

**R18. Error and selected never rely on colour alone. Error carries an icon and a linked message; selected carries a non-colour mark and the right ARIA state.**
Reason: colour alone fails people who cannot distinguish it and fails every screen reader.
Checked by: Gate 2 for declared accessibility behavior; Acceptance review checks the error icon and linked message and the selected mark and ARIA state.

**R19. A contract lists every widget in a family separately, and each widget's keyboard behaviour is exactly its own APG pattern.**
Reason: a radio group, a select and a text input share no role, Tab-stop rule or key set.
Checked by: Gate 1 check 1c for the per-widget schema and Gate 2 for declared key behavior; Acceptance review compares the declared key list with the linked APG pattern.

**R20. Only modal widgets trap focus. A popover, menu, tooltip or select that traps Tab is a failure.**
Reason: a trap where none is expected strands a keyboard user.
Checked by: Gate 2, from `focus.modal` in the contract.

**R21. Every pointer target measures at least 24 by 24 CSS pixels.**
Reason: smaller targets are missed by touch and by anyone with a tremor.
Checked by: Gate 2, the target size check.

**R22. Text meets its contrast requirement in every state and both themes, measured on the real render.**
Reason: a control that passes at rest can fail on hover or in dark mode.
Checked by: Gate 3.

**R23. One system. Components are built on the shadcn or Radix primitive when one exists. No second component library enters the tree.**
Reason: two systems in one tree disagree about spacing, focus and motion, and the seams show.
Checked by: Acceptance review of spec section 10, implementation imports, `package.json` and the lockfile against the contract's `shadcn` and `implementation` fields.

**R24. One thing leads. Every screen has a first place for the eye, and display type is at least 2.5 times the body size except where the token spec names a concession.**
Reason: equal weight everywhere means the eye lands nowhere and the screen reads as generated.
Checked by: Design review, visual hierarchy dimension; Acceptance review compares the display and body tokens and the concession in spec section 2.7.

**R25. Content must survive: a long label, a long paragraph, an empty list, a single row and many rows, at 320, 360, 414, 768 and 1440 pixels, with no horizontal overflow and no clipped text.**
Reason: a layout designed around ideal content breaks on the first real record.
Checked by: Gate 7.

**R26. The page stays inside Gate 4's performance budgets.**
Reason: a slow or shifting page costs trust before anyone reads a word.
Checked by: Gate 4.

## Motion

**R27. Every recipe declares exactly one reduced-motion tier: `remove`, `soften`, `keep` or `substitute`. `keep` needs a written reason.**
Reason: reduced motion is a medical need for some people, and each kind of motion needs a different answer.
Checked by: Gate 1 check 1c (a recipe without a declared treatment fails) and Gate 6 (the treatment is measured under `reduce`).

**R28. Reduced motion is tiered, never a kill switch. A global rule that sets animation and transition to none is not an implementation.**
Reason: with everything removed, a dialog that should cross-fade simply appears, which reads as a page change.
Checked by: Gate 6, the reduced treatment check (a `soften` recipe has no fade to find).

**R29. Durations, easings and distances are tokens: four transition durations and two loading cycles. A transition slower than the slowest states its reason in the recipe contract.**
Reason: a fixed small set keeps motion feeling like one hand made it.
Checked by: Gate 1 check 1c for structured token references; Acceptance review rejects a finite transition slower than `motion.duration.slower` whose `slowDurationReason` is null or empty. Gate 6 measures the duration against the contract.

**R30. The contract is written before the recipe is built, and no expected number is derived from what a gate observes.**
Reason: an expectation copied from the output can only ever agree with it.
Checked by: Gate 6, whose every comparison value comes from the contract or a token it names; Acceptance review of commit order.

**R31. A recipe that can leave has an `exit` phase. A looping recipe has exactly one `cycle` phase.**
Reason: an entrance without an exit leaves the interface snapping shut.
Checked by: Gate 1 check 1c for phase shape and Gate 6 for declared exit completion; Acceptance review uses the closed recipe table in spec section 4.3 to identify recipes that can leave and require an exit.

**R32. CSS first. A Motion or GSAP variant exists only when it does something the CSS variant cannot, with that reason written in the recipe spec.**
Reason: every engine is weight on the page and one more thing to keep consistent.
Checked by: Acceptance review against spec section 4.3: each non-null Motion or GSAP slot matches an enumerated earned case and carries its written reason. Gate 4 separately checks the resulting weight and GSAP initial-chunk exclusion.

**R33. Skill examples are never pasted. A recipe is rewritten against the tokens.**
Reason: pasted examples bring foreign values and, in several cases, licence terms that forbid copying.
Checked by: Gate 1 check 1b (foreign literals fail) and Acceptance review for provenance.

## Growth

**R34. Something new starts project-local, is promoted into the Pattern after two real uses, and arrives complete: spec, active contract, tokens, implementation, harness route, index row, changelog entry and review record.**
Reason: promoting on first use fills the Pattern with one-off shapes; arriving incomplete leaves untested surface.
Checked by: `npm run gates` on the addition, then Acceptance review against the checklist in `specs/README.md`.
