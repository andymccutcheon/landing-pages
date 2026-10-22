# Strategy pack — design review

**Author:** Layla Brower (design role-agent). **Date:** 21 October 2026.
**Responds to:** the incoming strategy pack (`marketing-engineering/docs/proposals/2026-10-21-ninthpass-strategy-pack/`)
and Katrina DaVita's four review documents in `marketing-engineering/docs/proposals/2026-10-21-ninthpass-strategy-review/`.

**Bottom line:** adopt the pack's rigour, reject its redesign. The page does not need rebuilding. It
needs three specific additions — a view of the artifact changing, a home for the five skills, and a
name-agnostic identity — plus one decision that is yours and not mine.

---

## 1. The lead does not change, and I will not rebuild the page

Katrina's recommendation and mine agree: **"Put your prompts through review." stays.** The pack's
transformation lead loses, for three reasons I add my own weight to:

1. **A rebuild now would be thrown away.** The pack's own sequence puts visual design after naming
   and messaging validation. Redesigning the page for a position we are not adopting, under a name we
   have not chosen, is work that has to be redone rather than refined.
2. **The page's edge is the honest failure in the middle of the run.** The second score being 8 again
   is the most credible thing on the page. Any rebuild that leads with transformation has to either
   bury that failure or explain it away, and explaining it away makes the page less trustworthy, not
   more.
3. **The art direction already meets the pack's brief.** The pack asks for restrained, editorial,
   lightly sci-fi, prioritising real examples and provenance over fake telemetry. The shipped page is
   exactly that: smoked ground, mineral-white type, one citron signal, Fraunces for editorial
   headings, real run files, and no invented metric anywhere.

**What I will not do:** re-theme, re-animate, replace the three diagrams, change the palette, or re-cut
the hero typography. The token set is semantic (ground, surface, raised, text, signal), so it already
survives a name change without touching it.

---

## 2. The gap the pack found is real, and the proof is hiding in the run files

The pack's homepage concept needs a **before → after** pair beside the rough input. Katrina found
there is no clean pair, because the run's second rewrite removed the separate Task Prompt.

I read the files. **The removal is the evidence, not the absence of it.** The chain is in the repo:

| Step | File | What it says |
|---|---|---|
| Composed | `examples/runs/meeting-notes/01-compose.md` | 98 lines. A System Prompt **and** a Task Prompt. |
| Scored | `04-judge-pass2.md` | "Task Prompt: 7/10 — Clear GOAL and RETURN FORMAT but redundant with Operating Constraints and Deliverable Structure sections." Overall 8/10, "Primary remaining gap is redundancy between system and task prompt sections, creating maintenance risk." Recommendation 1: "Eliminate Task Prompt redundancy … Remove Task Prompt section entirely or convert to cross-reference." |
| Revised | `03-revise.md` → `05-final.md` | 78 lines. **No Task Prompt.** The duplicated rules survive once. |
| Scored | `04b-judge-pass3.md` | 9/10, STOP. |

So the review named a specific flaw, the rewrite removed it, and the score moved. That is a
before-and-after pair, and it is the strongest artifact the product has — stronger than the 8 → 8 → 9
curve, because the curve is about time and this is about **the artifact changing for a stated reason**.

**What the page currently never shows:** the text of the artifact before and after. The "A review you
can take apart" section shows five recommendations fanning into one rewrite, and then the reader has
to take the word for what the rewrite actually did. The file manifest lists the files; it does not
show their content.

**The honesty constraint that comes with it:** the final artifact is twenty lines *shorter*. A naive
reader reads shorter as worse. The design has to show what was gained — the same rule stated once
instead of twice, and the reviewer's own phrase, "creating maintenance risk". The win is the removal
of duplication, and it has to be visible as a removal, not as a diff of arbitrary lines.

---

## 3. Proposal — a revision-diff view, the page's missing artifact

**What it is.** A two-column, aligned view of the composed prompt and the final prompt, showing the
Task Prompt block struck out and the two rules it duplicated collapsing to one. Not a diagram of a
process — a view of the document itself.

**Why a diff and not a fourth diagram.** The page has three diagrams and each explains something
different: the loop explains time, the arbor explains feedback anatomy, the dataflow explains process
handoff. A fourth loop would repeat. Nothing on the page shows the artifact, and the artifact is the
product.

**Anatomy.**

- **Left column:** "Composed — `01-compose.md`, 98 lines." The System Prompt with the Task Prompt
  block present. The block is marked *removed*, not merely dimmed.
- **Right column:** "Final — `05-final.md`, 78 lines." The same prompt without the block, and with the
  two Operating Constraints lines the reviewer asked for.
- **The join:** one line that appears in both columns — "Output must be exactly five bullet points" —
  shown once in the left column and once in the right, with the left instance marked as the duplicate
  the reviewer named.
- **Three callouts, all quoted from the run:** the reviewer's Task Prompt rating; the recommendation
  wording; and the score move, 8 → 9.
- **Caption:** "The review found the same rule twice. The rewrite removed one copy. The next scorecard
  read 9." Every clause is checkable against the files.

**Construction.** Built by a script from the two real files, the way
`tools/build_ninthpass_diagrams.mjs` builds the existing three — never hand-transcribed. The script
asserts that the Task Prompt block is present in the composed file and absent in the final file, and
fails the build if it is not. No synthetic lines, no ellipses, no invented content.

**Motion.** One pass, under eight seconds, then a complete still composition. A single highlight
sweep crosses the removed block, and the duplicated rule lines converge to the one that survived. It
must not loop: this is a document, and a document that keeps moving is a document you cannot read.
It sits under the page's existing persistent **Pause motion** setting, and the reduced-motion and
offscreen rules apply unchanged.

**Accessibility.** The diff must be readable as text. "Removed" is stated in words, not signalled by
strike-through colour alone; added and removed text both meet 4.5:1 against their own backgrounds; the
SVG title and description carry the whole comparison in prose; the phone layout is recomposed, not a
shrunken desktop version.

**Where it sits.** At the end of "A review you can take apart" — after the reader has met the five
recommendations, so the diff reads as their consequence. It does not replace the arbor; the arbor
explains what the feedback was, the diff shows what it did.

---

## 4. The second gap — composability has no home on the page

The page names the five skills in six places and every one of them is inside the install panel. Nowhere
does the page tell a reader that **Brief, Compose, Judge, Revise and Loop can each be run on their
own**. That is the product truth behind the pack's "use the parts you need" pillar, and it is the
cheapest thing we have that a single-call prompt tool cannot also say.

**Proposal.** One compact strip inside the "Start" section: five rows, each with the skill name, one
line on what it does, the exact command, and one line that says whether that skill alone is a complete
answer. No icons, no cards, no animation, no new tokens — five rows of type in the existing system.

**Why this is an addition and not a rebuild:** one section in an existing page, no new visual system,
no new palette, no new motion. It can also be written before the name is chosen, because it never
mentions the brand.

---

## 5. Rename readiness — what a rename actually costs

The page is rename-safe by copy. Here is the whole surface, counted rather than asserted:

| Surface | Count | What it takes |
|---|---|---|
| Copy strings in `index.html` | 14 visible + title, meta description, canonical, four Open Graph fields, four Twitter fields | A copy pass. Nothing structural. |
| Header and footer wordmarks | 2 | The visible label and its `aria-label`. The mark is a separate inline SVG. |
| **Identity assets** | **3** | The mark in the wordmark is a literal **9** (a circle and a descender hook). `assets/favicon.svg` is the same 9. `assets/og.png` has the name rendered into the 1200 × 630 card by `tools/render_ninthpass_social.py`. These need new artwork — this is the only real design work in a rename. |
| Diagram documents | 3 `<title>` elements | Visible diagram labels are already name-agnostic: they say Compose, Judge, Revise and the scores. The name appears only in the browser tab title. |
| JavaScript | 8 occurrences of `ninthpass-motion` | A local-storage key and a post-message type. Mechanical. **Keep the key stable** — changing it would reset the saved pause preference for returning visitors. |
| CSS | 0 occurrences | Nothing to do. `css/pz-tokens.css` is named after the old Promptzilla brand and is worth renaming for hygiene at the same time, on its own. |
| External identifiers | domain, GitHub repository, npm package, output path | `ninthpass.amccutcheon.com` and `promptzilla.amccutcheon.com` are two domains on one Cloudflare Worker, so a new name is a domain change rather than a redeploy. The npm package name `ninthpass` **does not exist** — the registry returns 404, and the old release is `promptzilla@1.0.0`. Nothing needs un-publishing. |

**Total cost of a rename:** one new mark, one new favicon, one regenerated social card, one copy
pass, one worker domain change, and redirects on GitHub and npm. **Not a rebuild.** Design time is
under a day and most of it is the mark.

**Two rules I want applied now, before any name is chosen**, so that the eventual swap is a copy change
rather than a project:

1. **No identity may be baked into a raster except the social card.** The mark stays an inline SVG in
   the document so it can be swapped without a build step.
2. **No product name inside any diagram's visible content.** Already true; worth keeping true.

**On the name itself.** "Ninth Pass" implies a count. The product has no nine anywhere: the loop caps
at four scoring rounds, the rubric rates whatever sections a prompt happens to have, and the old
"twelve sections" claim was cut from the page. The rename commit records no rationale, and no
document explains the name. **It can only be replaced or tolerated — it cannot be explained.** If it is
tolerated, the cheapest honest treatment is to never lean on it as a number and to accept that every
visitor will read it as one.

---

## 6. What I am not taking from the pack

- **No brand-neutral hero metaphor work.** The pack asks to postpone hero metaphors and motion until
  naming is settled. There is nothing to postpone: the hero is a statement, a description and a real
  run, with no metaphor in it.
- **No motion system change.** The three diagrams share one runtime and one pause setting. It is the
  part of the page that most needs to survive a rename untouched.
- **No new colour or type work.** The palette is already semantic and name-agnostic.
- **No social-card redesign beyond the name swap.**

---

## 7. Pre-flight on the pack's language, against the live page

| Pack wording | Verdict | Why |
|---|---|---|
| "Transform rough intent into explicit agent directives" | Cannot lead | No artifact shows a clean transformation; the composition is one stage inside a review loop. |
| "Evidence-backed review" | Cannot be used | The evidence is quoted, not verified. The validator does not check that a quoted critique is true. |
| "9/10 proves quality" | Already handled | Section 5, "A score. Not a certificate." |
| "Your intent shouldn't need a 5,000-token detour" | **Usable** | It promises nothing about outcome, and it is the best line in the pack. Worth offering to Katrina as an alternate subhead. |
| "Think out loud. Give your agents better instructions." | Cannot lead | "Better instructions" is an outcome claim the page later retracts. |

---

## 8. Acceptance criteria, if these two additions are approved

**Revision-diff view**

- Built by script from the two real run files; the build fails if either file changes shape.
- No new colour beyond the seven existing token roles.
- Passes the existing render check at all seven widths down to 280 pixels, with no overflow and no
  clipped text.
- Removed and added text each measure at least 4.5:1, and neither is signalled by colour alone.
- One motion pass under eight seconds, then still; honours the page's pause setting and reduced
  motion; no embedded playback control.
- The caption's claims are each checkable against a line in the run files.

**Skills strip**

- Five rows, no icons, no cards, no new tokens.
- Every command verified against the product README before it is written.
- No claim that any single skill is better than a chat model.
- The cross-page render check stays green.

---

## 9. The one decision that is yours, not mine

Everything above is a two-way door and I will walk it. One is not: **whether the page's lead changes**
(and, with it, whether the page is rebuilt). My recommendation is no rebuild, no lead change, and two
additions instead — because the page's proof is a review and its credibility comes from the honest
failure inside the run. If you want the transformation lead, the page is rebuilt, the second 8 has to
go somewhere less prominent, and a future rename will land on a page that was designed for a position
we have since abandoned.
