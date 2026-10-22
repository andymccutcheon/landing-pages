# Response to the Silverquill design refinement directive

**Author:** Layla Brower. **Date:** 21 October 2026.
**Directive:** `~/Downloads/Silverquill_Design_Refinement_Directive.md`.
**Baseline inspected:** `landing-pages/ninthpass/` (static HTML, no framework, Cloudflare Worker
`ninthpass-site`), `~/Documents/GitHub/silverquill` (TypeScript CLI, Node 22, Vitest).

---

## 1. The finding, which changes the diff section

The directive's suspicion is correct, and it lands on something I had already built and framed as
success. The evidence, from the code rather than from inference:

| Where | What it enforces |
|---|---|
| `src/validation.ts:validateGenerated` | Requires `=== SYSTEM PROMPT ===` **and** `=== TASK PROMPT ===`, in that order, plus eleven named System headings and four Task headings. Compose may not return a System-only prompt. |
| `skills/revise/SKILL.md:23` and `:53` | "Write the complete rewritten prompt (**System and Task when both exist**…)" — the skill's own output contract asks for both blocks when the input had both. |
| `src/validation.ts:validateRewrite` | Checks only: BODY markers present exactly once, a `Rec-application checklist` after END BODY, and one entry per recommendation. **It never checks that the rewritten body still satisfies the Compose structure.** |
| `src/pipeline-engine.ts` | Passes the rewrite through `validateRewrite` and nothing else before sending it to the next Judge. |

So a rewrite that deletes the Task Prompt passes validation, and the next Judge scores whatever it is
given. In the captured run it gave 9/10.

**What actually happened in the run, in order:**

1. `01-compose.md` contains both blocks. It passed `validateGenerated`.
2. `04-judge-pass2.md` recommendation 1 reads: "Eliminate Task Prompt redundancy… **Remove Task Prompt
   section entirely** or convert to cross-reference."
3. `05-final.md` contains only the System block — 78 lines, no Task Prompt. It passed `validateRewrite`
   because the checklist accounted for every recommendation.
4. `04b-judge-pass3.md` scored that artifact 9/10, STOP.

**The honest reading.** The removal was *authorised by the review* — the revision did what it was told.
But it produced an artifact that no longer satisfies the product's own Compose contract, and the
validator that should have noticed this checks markers, not structure. That is a **contract conflict
inside the product**, not a stray failure in the run:

- the revise skill says "return System and Task when both exist";
- the judge's recommendation said remove the Task Prompt;
- the revise skill also says "implement ALL numbered recommendations".

Both instructions cannot be satisfied at once. Whichever wins, the code currently accepts either.

**Consequence for the page.** The diff section I built said "Nothing was lost, and the score moved."
That was wrong: it presented a structural gap as an improvement, which is exactly the failure the
directive names. It has been changed — the section now states the structural change and labels it as a
known gap, and the score is described as a score of the result rather than proof that removing the
section improved it.

## 2. Decision taken (21 October 2026): **A, with mode-aware validation**

Both blocks are required **in full mode**. Optimize-only preserves the shape of its input, so a
System-only prompt can be optimised as a System-only prompt. The recommendation is subordinate to the
contract: if a Judge recommendation would delete a required block, Revise keeps the block, removes the
redundancy inside it, and marks that recommendation `DEFERRED` with the reason. The Judge is now told not
to recommend deleting a required block or section. The historical run is **not** modified or relabelled;
it passed under the validator of its time, and the defect is documented instead.

The alternatives that were considered, for the record:

**Does full mode require both blocks in the final artifact?**

| Option | Meaning | Consequence |
|---|---|---|
| **A. The Task block is required** (my recommendation) | `validateRewrite` gains the same structural check as `validateGenerated` for full-mode runs, and a rewrite that drops a required block fails and is retried. | The captured run is then a **failed** run under the current code, and must not be used as success proof. A fresh run is needed for the page. |
| **B. System-only is legitimate** | Removing the Task block is an accepted outcome when the recommendation calls for it; the contract and the skill text change to say so. | The captured run stays valid, but the revise skill's "System and Task when both exist" line must be rewritten, and the page must say the final artifact is a single prompt by design. |
| **C. A merge rule** | A removed block must be *converted*, never deleted: its rules must survive elsewhere. | Close to what happened here (the rules were promoted into Operating Constraints), but it needs a machine-checkable definition, which is hard to make reliable. |

**My recommendation is A**, because a contract that silently accepts a structurally incomplete artifact
is the kind of thing that only gets worse, and because the promotion of the two rules into Operating
Constraints shows the rewrite *could* have kept both blocks. The cost of A: the current page example
has to be replaced, and the next public run needs a fresh execution.

## 3. What I changed before writing this

**Page** (`landing-pages/ninthpass/`):

- The diff standfirst no longer claims nothing was lost or that the score moved because of the edit.
- The caption now discloses: this artifact carries only the System block, the full-mode contract expects
  both, and it is recorded as a known gap rather than proof of improvement.
- Added the **Rule** device: a 0–10 score track with the gate marked at 9, three markers in run order,
  the repeated 8 shown twice.
- The skills block now states the true invocation (installs into the agent's skill directory, invoked
  there by name) and shows the CLI equivalent **only** for the loop, which is verified. It does not
  invent `silverquill brief` or any per-skill subcommand.
- `tools/check_silverquill_diff.py` still passes: 10 quotations and 2 line counts match the run files.

**Product** (`~/Documents/GitHub/silverquill`):

- **Legacy runs are now read-only.** My earlier change would have written new runs into
  `~/.ninthpass/runs` when that directory existed, which the directive forbids. Writes now always go to
  `~/.silverquill/runs`; `status` falls back to a plain, lock-free, write-free read of
  `~/.ninthpass/runs/<id>/run.json` and prints a line saying the run is legacy and read-only. Resuming or
  updating a legacy run is explicitly not supported.
- Build clean, 59/59 tests pass after the change.

## 4. What is not done, and is not blocked

| Item | Status |
|---|---|
| `validateRewrite` structural check and the regression fixtures the directive lists | **Blocked on the decision above** — the semantics are the owner's call |
| A clean example run for the page's success proof | **Done.** `examples/runs/rough-to-reviewed/`: optimize-only, OpenCode, 5/10 → 9/10 STOP, contract-valid, published provenance note |
| Mark tests at 16/24/32 px, monochrome and reverse, light and dark | Not done. Next. |
| Baseline screenshots at 1440×900, 1024×768, 390×844 with a written recon record | Partly done (screenshots exist at 1440 and 390); the 1024 pass and the written record are not |
| Read-only legacy run test (no files created) | Not done; the behaviour is implemented and observed, not yet pinned by a test |
| npm badge restoration, publish, repo rename, route switch | Held behind trademark clearance, as decided |
| The deferred Arbor/visualisation family | Not started, correctly |

## 5. One judgement on the page

**I would pull the diff section until a clean example exists.** It is truthful now, but a landing page
whose headline proof is "here is a structural gap we found" spends its best asset explaining a weakness
to a visitor who has not yet been convinced the product works. The finding is valuable — as a product
note, a changelog entry and an internal exhibit — and the *technique* (a generated diff of a real
revision) belongs on the page with a legitimate example. That is a product call, not a design one.


---

## Update — the clean run and the rebuilt section

Full mode was attempted first and plateaued at 8.5 three times, pausing for a human decision. That run is
a valid, honest artifact but not a success proof, so the page uses the optimize-only path instead:
`38d87300-e913-4c98-9356-4075448d4e62`, OpenCode worker, 21 October 2026.

| | |
|---|---|
| Input | "Summarise meeting notes into five bullet points. Keep it short and useful." (12 words) |
| First scorecard | 5/10 CONTINUE, five numbered recommendations with exact replacement wording |
| Revision | all five APPLIED, with a CUT note for each of the two replaced sentences |
| Second scorecard | 9/10 STOP — every gate previously scored 3–5/10 now closed |
| Structure | valid under the repaired contract; optimize-only preserved its input's shape |

`tools/build_silverquill_diff.mjs` generates the section and fails unless every recommendation's
replacement text is present verbatim in the final prompt and every struck phrase is present in the
original. `tools/check_silverquill_diff.py` fails if the page stops matching the generated fragment.
The Claude Code worker was out of weekly quota (resets 23 October), which is why this run used OpenCode;
the provenance line says so.
