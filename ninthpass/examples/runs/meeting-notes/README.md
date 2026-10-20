# A real run

This directory is one real run of the engine, captured on 2026-10-20. Nothing in it is
illustrative. It is here so that a reader can open the artifacts the landing page shows and check
them in ninety seconds.

| | |
| --- | --- |
| **Run id** | `0becaacc-fb6e-4a92-8951-5106c00edd80` |
| **Worker** | Claude Code (`claude:*` execution ids) |
| **Mode** | Full — a raw request, no existing prompt |
| **Request** | `Write a prompt for a meeting-notes summarizer that returns five bullets` |
| **Score trajectory** | 8 / CONTINUE → 8 / CONTINUE → 9 / STOP |
| **Rounds** | three Judge passes, two rewrites |
| **Fresh process per stage** | `fresh_context: true` on all six stages |

## The files, in the order they were written

| File | What it is |
| --- | --- |
| `00-request.md` | the request, verbatim |
| `01-compose.md` | the composed System Prompt and Task Prompt, 4,177 bytes |
| `02-judge-pass1.md` | the first scorecard — 12 section ratings, each with quoted evidence — 8/10, CONTINUE |
| `03-revise.md` | the first rewrite, with a checklist per recommendation |
| `03b-revise.md` | the second rewrite, after the score did not move |
| `04-judge-pass2.md` | the second scorecard — 8/10, CONTINUE again |
| `04b-judge-pass3.md` | the third scorecard — 9/10, STOP |
| `05-final.md` | the prompt the run wrote out, 4,109 bytes |

The `b` on `03b` and `04b` is the engine's round-dependent naming. It is the clearest evidence
that the run really happened: a second rewrite inside the same round, and a third scoring pass.

## What the three scorecards say

The interesting part of this run is the middle. Pass 1 scored 8 and named its gaps. Pass 2
scored 8 again — the rewrite landed most of the recommendations but the same residual problem
survived, *redundancy between the System Prompt and the Task Prompt sections*. Pass 3 scored 9
and the run stopped. And even at 9 the scorecard still lists "minor polish items", because a 9 is
a judgement, not a certificate.

> `Overall Rating: 8/10` — Strong, usable prompt with specific role definition, enforceable
> constraints, concrete examples, and comprehensive safety guidance. Most Pass-1 recommendations
> successfully incorporated (Domain Expertise specificity, prioritization rules, multi-session
> handling, numerical verification). Primary remaining gap is redundancy between system and task
> prompt sections, creating maintenance risk.

> `Overall Rating: 9/10` — Decision-ready. The prompt provides specific role definition,
> enforceable constraints, comprehensive examples, robust safety guidance, and detailed
> self-monitoring. All major gaps from earlier passes have been addressed. Remaining opportunities
> are minor polish items.

## What "approved" means here

The run recorded `approved: true` and the label *"Judge STOP; recommendations have not been
applied."* Approval in this product is a code assertion — the verdict was STOP and the score was
9, and the file was written. **No human read this prompt.** Judge is a model scoring a prompt
against a fixed rubric. It checks the structure of the prompt, not whether the prompt is true.

## Reproducing it

```sh
git clone https://github.com/andymccutcheon/ninthpass
cd ninthpass && npm install && npm run build
node dist/cli.js run \
  --request "Write a prompt for a meeting-notes summarizer that returns five bullets" \
  --worker claude --out ./prompts
```

A live run will not be byte-identical to this one — a model's output is not deterministic, and
that is the point of the scorecard. The shape will be the same: a request, a composition, scorecards
that quote their evidence, rewrites, and one file written out at the end.
