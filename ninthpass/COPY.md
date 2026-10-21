# Ninth Pass — final public copy record

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
git clone https://github.com/andymccutcheon/ninthpass
cd ninthpass
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
