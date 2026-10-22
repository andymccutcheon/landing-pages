# Silverquill — public copy record

> **Current copy: the creation-led revision of 21 October 2026.** It supersedes the review-led hero and
> the 8 → 8 → 9 demonstration below, which are kept as history. Live copy follows. The page is
> **deployed** — the brand switch ran on 21 October and the canonical host is
> `silverquill.amccutcheon.com`. The GitHub repository was renamed to `silverquill` on 22 October;
> the old slug redirects.

## Hero (current)

**Eyebrow:** Agent instruction engineering & review

**Headline:** Give your agents better instructions.

**Description:** Describe what you want an agent to accomplish. Silverquill creates the System Prompt
and Task Prompt, independently evaluates them against a defined standard, and refines them using
evidence-backed recommendations. Every stage is inspectable. The task itself remains yours to execute
with the agent.

**Primary action:** Get Silverquill on GitHub · **Secondary:** Inspect a real run
**Prerequisites:** Node.js 22.12+ · MIT licensed. Installed, authenticated agent worker required.
**Qualification:** A score is a model's assessment of instruction quality. It is not a measurement of
what your agent does with it.

## Recorded run (current)

**Heading:** Scored 8.63. Then 9.25.
**Request:** "An agent that summarises meeting notes into five short, useful bullets for a colleague who
missed the meeting."
**Trajectory:** 8.63 → 9.25. Both scores are the mean of the section ratings, recorded by a Codex worker
on 21 October 2026.
**Scorecards:** Composed · 8.63/10 · CONTINUE — "A strong, practical prompt with clear scope, source
discipline, and output constraints. Its main weaknesses are contradictory handling of missing
information and safety refusals, plus one unsupported inference in the few-shot example." / Approved ·
9.25/10 · STOP — "A decision-ready prompt with strong source discipline, safety boundaries, output
control, and self-checking. Minor ambiguity remains around absent inputs and the scope of fact
verification."

## See what changed (current)

**Standfirst:** 5 edits, one review round. The judge scored the composed agent 8.63; after the revision
it scored the approved agent 9.25 and stopped.
**Provenance:** Recorded run · Codex worker · 21 October 2026 · full mode · 570 → 623 words.
**Ledger:** five blocks, each naming the section, the exact wording the recommendation replaced, and the
exact wording it supplied. Generated from the run; the script fails if either side does not match.

## Skills (current)

**Heading:** Three capabilities. One loop.

- **Compose · Create** — Turns what you want an agent to accomplish into a System Prompt and a Task Prompt. It never performs the task.
- **Judge · Evaluate** — Scores those instructions against the published rubric, quotes the lines that are weak, and numbers its recommendations.
- **Revise · Refine** — Applies the numbered recommendations and returns a checklist of what was applied or deferred.
- **Loop · Orchestrate** — Runs the three stages in order and keeps the record. Also available as one command: `node dist/cli.js run --request "…"`.
- **Brief · One-off task** — A separate path: turns a rough task assignment into a single execution-ready brief, without building an agent. A task-like input given to Compose still produces System and Task Prompts.

## Install (current)

**Heading:** Your next prompt. Put it through review.

**Body:** Clone and build from GitHub while the npm package is unpublished. Install and authenticate your chosen worker first; this example uses Claude Code.

**Body:** Use `--worker opencode` or `--worker codex` for another supported worker. Silverquill uses the worker’s authentication and does not store provider credentials. Worker usage follows your provider’s plan or billing.

**Actions:** Get Silverquill on GitHub · Read the setup guide · Install the five skills separately.

**From source to first run**

```sh
git clone https://github.com/andymccutcheon/silverquill
cd silverquill
npm install
npm run build
node dist/cli.js run \
  --request "An agent that summarises meeting notes into five short, useful bullets" \
  --worker claude \
  --name meeting-agent
```

**Already have a prompt?** `node dist/cli.js run --prompt ./prompt.md --worker claude`

## Shared interface (current)

- Navigation: Real run · How it works · Start.
- Page motion: Pause motion / Resume motion / Motion reduced.
- Clipboard: Copy commands / Copying… / Copied / Commands selected.
- Clipboard success announcement: Setup and first-run commands copied.
- Clipboard refusal announcement: Couldn’t copy. Select the commands to copy them.
- Footer: Open-source prompt review. MIT licensed.
- Footer links: Source · Run artifacts · License.
- Title: Silverquill — Give your agents better instructions.
- Description: An open-source toolkit that turns what you want an agent to do into a System Prompt and a Task Prompt, evaluates them against a published rubric, and refines them with evidence-backed recommendations. Every stage is inspectable.
- Social description: Create the agent instructions, evaluate them, refine them — and inspect every stage.
- Social card: Open-source prompt review, with the record attached. One recorded run. Model-assigned prompt scores.

---

# Superseded — the review-led revision (20 October 2026)

This records the flagship page's published-facing copy. `index.html` is the rendered implementation. Diagram labels and the unchanged example files are part of the same argument. Source and run links are preserved in the implementation; no customer results, testimonials or comparative superiority are claimed.

## Hero

# Put your prompts through review.

Open-source command-line prompt review for agent builders. Start with a rough request or an existing prompt. Ninth Pass runs a scored review-and-rewrite loop and saves the prompt with the scorecards behind it.

**Get Ninth Pass on GitHub** · **Inspect a real run**

Node.js 22.12+ · MIT licensed. Installed, authenticated agent worker required.

## The first rewrite still scored 8.

You can ask a model to critique a prompt in the same chat. Ninth Pass makes review a sequence you can inspect: score the prompt, revise from numbered feedback, then score the rewritten text.

The actual request: “Write a prompt for a meeting-notes summarizer that returns five bullets”

One captured run · Claude Code. 20 October 2026.

Compose / Draft prompt → Judge / 8 / CONTINUE → Revise / First rewrite → Judge / 8 / CONTINUE → Revise / Second rewrite → Judge / 9 / STOP.

Three scorecards. Two rewrites. The first rewrite did not improve the score. This is a recorded example, not a live model run. **Open the unchanged run files.**

**8 → 8 → 9**

These are model-assigned prompt scores, not measurements of task performance. The run stopped at 9 with two polish recommendations still open.

Scorecard selector: **First score · After rewrite · Final score**

- **8/10 · CONTINUE:** “Usable and mostly complete.” **Read the first scorecard.**
- **8/10 · CONTINUE:** “Primary remaining gap is redundancy between system and task prompt sections, creating maintenance risk.” **Read the second scorecard.**
- **9/10 · STOP:** “Remaining opportunities are minor polish items.” **Read the final scorecard.**

## A review you can take apart.

The first scorecard named five recommendations. Revise returned one rewritten prompt and a numbered checklist accounting for each one.

**First scorecard / 8 / CONTINUE** branches to:

1. Remove repeated instructions
2. Apply domain guidance
3. Rank more than five points
4. Carry context across meetings
5. Check numbers against source

Gathered into **One rewrite → Next Judge / Still 8/10**.

Five pieces of feedback, not five parallel workers. Every checklist entry said APPLIED; the next scorecard still found repeated instructions.

The branches summarize the actual first-pass recommendations. Open the scorecard for the exact wording.

**Read the five recommendations. Inspect the first rewrite.**

## Separate the process. Keep the evidence.

The built-in OpenCode, Claude Code and Codex workers start a new process for each stage. Ninth Pass forwards the stage packet rather than the conversation that produced the draft.

Diagram: Compose / Draft the prompt → Prompt → Judge / Prompt + original request / Earlier scorecards → Scorecard → Revise / Rewrite from feedback → Rewritten prompt → fresh Judge. Each is a separate worker process. Run record on disk: input, stage outputs, scorecards and retries. Phone annotations abbreviate Judge's input as “Current prompt + history” and Revise's artifact as “Rewritten prompt.”

Judge must see the prompt it grades. Its packet includes the original request and earlier scorecards. Ninth Pass does not forward the authoring conversation or the rewrite’s APPLIED checklist; deferred notes can travel with it.

Separate processes can use the same model and provider. In manual mode, your host must provide fresh contexts. Process separation is not a security sandbox.

**Read the worker implementation.**

## A score. Not a certificate.

Know what a 9 means—and what it doesn’t. **Read the published rubric.**

| Score | Rubric summary |
| --- | --- |
| 0–3 | Missing, contradictory or unsafe |
| 4–6 | Present but thin |
| 7–8 | Usable, with gaps |
| 9–10 | Stop-loop caliber |

Judge is instructed to cite prompt text or structural facts. An overall score of at least 9 means STOP under this rubric. A lower score means CONTINUE.

The model judges the prompt. The code checks return formats, score/verdict agreement and recommendation accounting. It does not establish that cited evidence is sound or that a claimed edit was made.

This run’s final prompt still has limitations. These artifacts do not demonstrate its performance on a meeting transcript. STOP requires no human sign-off and does not certify that an agent’s answer will be right.

## The prompt. And its paper trail.

Run files stay on disk: the input, stage outputs, scorecards, retries and run state. The exported Markdown contains the prompt text.

**Files from the captured example**

```text
00-request.md
01-compose.md
02-judge-pass1.md
03-revise.md
04-judge-pass2.md
03b-revise.md
04b-judge-pass3.md
05-final.md
```

**Read the unchanged final prompt.**

**Judge STOP:** Export the scored prompt to `./prompts/<slug>.md`.

**Cap, validation block or plateau:** Preserve the best scored candidate as `<slug>.provisional.md`, when one exists. A run that fails before any score may have no prompt to export.

**Paused:** Resume with your explicit decision. The run waits until a decision is supplied.

## Your next prompt. Put it through review.

Clone and build from GitHub while the npm package is unpublished. Install and authenticate your chosen worker first; this example uses Claude Code.

Use `--worker opencode` or `--worker codex` for another supported worker. Ninth Pass uses the worker’s authentication and does not store provider credentials. Worker usage follows your provider’s plan or billing.

**Get Ninth Pass on GitHub. Read the setup guide. Install the five skills separately.**

**From source to first run**

```sh
git clone https://github.com/andymccutcheon/silverquill
cd silverquill
npm install
npm run build
node dist/cli.js run \
  --request "Write a prompt for a meeting-notes summarizer that returns five bullets" \
  --worker claude \
  --name meeting-notes
```

**Already have a prompt?**

```sh
node dist/cli.js run --prompt ./prompt.md --worker claude
```

## Shared interface

- Navigation: Real run · How it works · Start.
- Page motion: Pause motion / Resume motion / Motion reduced.
- Clipboard: Copy commands / Copying… / Copied / Commands selected.
- Clipboard success announcement: Setup and first-run commands copied.
- Clipboard refusal announcement: Couldn’t copy. Select the commands to copy them.
- Footer: Open-source prompt review. MIT licensed.
- Footer links: Source · Run artifacts · License.
- Title: Ninth Pass — Put your prompts through review.
- Description: An open-source review-and-rewrite loop for agent prompts. Separate worker processes, inspectable scorecards, and a real 8 → 8 → 9 run. Build Ninth Pass from GitHub.
- Social description: Prompt review, with the record attached. Inspect a real run, then review your next agent prompt.
- Social card: Open-source prompt review, with the record attached. One recorded run. Model-assigned prompt scores.


---

## Added 21 October 2026 — the Silverquill revision (prepared, not yet published)

> **The revision-diff block below was pulled on 21 October 2026** — its artefact is not contract-valid
> (the rewrite removed the required Task Prompt block). It is kept as the engineering exhibit
> `specs/diff-exhibit-2026-10-21.html`. **The live section is the block further down, built from the
> later `rough-to-reviewed` run.**

**Hero qualification, under the prerequisite line**

A score is a model-assigned rating of prompt structure. It is not a measurement of what your agent
does with it.

**Revision diff — "The review changed the artifact."**

Standfirst: The reviewer found the same rule stated twice. The rewrite left it once. Nothing was lost,
and the score moved.

Left column, `01-compose.md`, 98 lines: the Operating Constraints line "Output must be exactly five
bullet points"; then the removed Task Prompt — "Summarize the provided meeting notes into exactly five
bullet points that capture the most important decisions, action items, and discussion points." and
"Do not exceed five bullets".

Right column, `05-final.md`, 78 lines: "Output must be exactly five bullet points", "Each bullet should
be self-contained and meaningful", and the promoted rule "When >5 distinct points exist, select in
order: (1) Decisions with clear outcomes, (2) Action items with named owners and dates, (3) Action items
without owners, (4) Discussion points revealing blockers/risks, (5) General themes".

Scores: "Second scorecard · 8/10 · CONTINUE" with "Primary remaining gap is redundancy between system
and task prompt sections, creating maintenance risk." / "Third scorecard · 9/10 · STOP" with
"Decision-ready… Remaining opportunities are minor polish items."

Caption: The reviewer's instruction was "Remove Task Prompt section entirely or convert to
cross-reference". The rewrite removed it and promoted the two rules it had been carrying. Every line
above is copied from the two run files.

**Skills — "Use the parts you need."**

Five skills. Each one installs into the agent host you already use and can be called on its own.

- **Brief** — Shape a loose assignment into a clear task with its objective, boundaries and expected return.
- **Compose** — Write the system prompt and the task prompt for an agent, from a rough request.
- **Judge** — Score the prompt against the published rubric, and quote the lines that are wrong.
- **Revise** — Apply the numbered recommendations and return a checklist of what was applied or deferred.
- **Loop** — Run the stages in order, and keep the record. The same loop is one CLI command.


**Score track — "A score. Not a certificate."**

A 0–10 track with the gate marked at 9 and three markers in run order: 8, 8, 9. Legend: "Three scores
from one run, in order. The second rewrite scored 8 again; the third scored 9. The gate is the score,
not a count of passes."


## The revision diff now on the page — built from `examples/runs/rough-to-reviewed/`

**Heading:** See what changed.

**Standfirst:** A two-sentence prompt scored 5 out of 10. The review named 5 gaps with exact wording;
the rewrite applied all 5; the next scorecard scored 9 and stopped.

**Provenance line:** Second recorded run · OpenCode worker · 21 October 2026 · optimize-only

**Left column — `00-original.md`, 12 words:** "Summarise meeting notes into five bullet points. Keep it
short and useful." Two phrases struck, each numbered to the recommendation that replaced it.

**Right column — `05-final.md`, 146 words, after one round:** the System Prompt and Task Prompt, with
each recommended clause marked and numbered.

**Scores:** First scorecard · 5/10 · CONTINUE — "The task and the output count are clear and
enforceable, but the two gates that determine whether the output is any good — 'short and useful'
(undefined) and faithfulness (absent) — are exactly the ones that would break the agent's job…" /
Second scorecard · 9/10 · STOP — "Every gate the earlier pass scored 3–5/10 is now closed with
enforceable text…"

**Caption:** The numbers mark the recommendations from the first scorecard. Every one is applied
verbatim — this script fails if a recommendation's wording is missing from the final text, or if a
struck phrase is missing from the original. Following the rewrite, the judge scored the result 9/10.
That is a score of the result, not proof that any single edit caused it.
