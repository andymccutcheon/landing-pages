# Freewhirr implementation report, 2026-10-12

Implementation on local `main`; starting commit `ebccc26`. No remote, push, deployment, or changes to Acheron content or vendor files. Implementation assigned to the Codex native lane (OpenAI); Grok 4.7 (xAI) is the independent reviewer, outside this implementation session.

Binding inputs read in full:

- Design Studio: `docs/pattern/landing/2026-10-11-freewhirr-landing-design-brief.md`.
- Marketing Engineering: `docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md`.

## Sections as built against the design brief

| Order | Built heading | Brief section and layout |
|---|---|---|
| Header | freewhirr | sticky shared header |
| 1 | Spend nothing until you choose to. | Hero: wide headline over split with route ladder |
| 2 | How a request is routed | What it is: statement against four triggers |
| 3 | Free models are generous. They are also flaky. | Why: staggered pair |
| 4 | Stop, or spend on purpose | Exhaustion policies: equal-weight table beside guardrails |
| 5 | Quickstart | command column with result-field aside |
| 6 | A library, a proxy, or a command line | Three surfaces: sticky heading, stacked entries |
| 7 | Settings: yours, in any format | precedence list beside four-stanza block |
| 8 | The cost of free | ruled privacy statement |
| 9 | Status | Closing: tinted band |
| Footer | freewhirr | shared footer |

The architecture table lists nine content sections despite the brief's prose saying eight. The built page follows the explicit architecture table. No theatre, media, equal-card row, tabs, automatic animation, or benchmark panel.

## Reconciled conflicts and reasons

1. **Order:** copy's problem / routing / policies / surfaces / failure / ledger / quickstart sequence becomes the brief's walk / why / policies / quickstart / surfaces / settings / privacy / closing. Settings gets its own section; failure material is distributed into walk, policies, proxy and privacy; ledger caveat is merged into privacy.
2. **Headings:** copy headings are used in the matching slots; the brief supplies the separate settings and privacy headings. Quickstart uses the already-resolved ruling, without a duration claim.
3. **Hero length:** full binding sub-headline (40 words) wins over the brief's 20-word slot. The headline and required Option B qualifier remain verbatim. Browser measurements confirm three headline lines at 360 and two at the larger required widths, with install and desktop ladder fitting the stated viewports.
4. **Hero contents and action:** omit copy's hero status/version line, since the brief permits only kicker, headline, supporting copy and install action. Install bar plus quickstart link replaces copy's PyPI/GitHub button pair. PyPI is available in the footer; GitHub in header, closing and footer. Closing retains the copy's version in its body, with no version badge or footer stamp.
5. **Proof assets:** static ordered-list ladder replaces copy's proposed terminal capture/policy panel. Four triggers replace the copy's five-box routing flow. No invented error output or blank stats dashboard. README setup tabs become visible stacked proxy evidence and plain harness names.
6. **Routing details:** copy's retry-before-failover distinction is retained in the four-trigger list and its streaming limit. The pinned/discovered-list sentence is retained. Catalog-cache detail, separate tool/quality-check steps and stealth narrative are omitted to fit the brief's chosen facts and explicit exclusions.
7. **Policy wording:** copy's narrower “calls nothing on your paid list” wins over the brief's unqualified “none, ever” spending cell. The two non-default settings warning stays directly below the example. Both columns have identical type, widths, colour and no recommended badge. Caps are expressly unset until set.
8. **Policy evidence:** brief's real `examples/paid.yaml` replaces copy's side-by-side files. Pasted verbatim from Freewhirr `494458e`; not the divergent README listing. Dollar/percentage figures appear only in that source example and the ladder's `$0.00` illustration, never as measured savings or adoption.
9. **Quickstart:** three blocks as the brief specifies; copy's fourth proxy block moves into the proxy entry. Python version prerequisite retained. Result-field aside and CLI help are source-backed labels required by the brief.
10. **Proxy command:** binding copy's `freewhirr serve --port 8787` wins over the brief's `--config examples/stop.yaml` command: that file is unavailable after `pip install`. Default `stop` policy is stated beside it. No-login/localhost warning from the copy is retained next to the command.
11. **Settings:** brief's four-format example and precedence list replace a single configuration paragraph. TOML confirmed in `tests/test_config.py:36-48` at Freewhirr `494458e`; YAML/env/Python confirmed in README/config sources. OpenRouter-only qualifier stays in this same section.
12. **Privacy:** preserve the section per the ruling. Copy's attributed README warning replaces the brief's unqualified provider statement. Remedy and consequence are equally large, primary-colour text. Local ledger and “no telemetry of its own” wording avoids implying prompts never leave the machine. Tool-identifying headers remain disclosed.
13. **Closing/footer:** name-origin sentence moves from copy's footer to brief's closing band. Footer adds README/licence destinations specified by the brief and the exact resolved “Not affiliated with OpenRouter.” sentence. Copy's broader non-affiliation paragraph remains intact.
14. **Tokens/no script:** add exactly the three requested component dimensions. `core.space.48` is not present in the vendored snapshot, so `--lp-policy-label-col` is documented as a design decision. Separate `--lp-system-*` aliases copy only needed existing Pattern dark values into the permitted primitives file; they introduce no palette choice and enable system-dark rendering with JavaScript disabled. All new selectors are Freewhirr-scoped or names absent from Acheron. Existing shared values and rules are untouched.

## Copy audit classification

The required command audits Freewhirr when supplied a Freewhirr copy filename (formerly it always audited Acheron). Its original fragment comparison is preserved. It reports **31 additions and 40 omissions**, each classified below. This is a disclosure report, not an exact-match pass or a silent rewrite of the binding draft.

- Additions: brief-required labels/headings, repository source evidence, quote-fence normalization artifacts, the explicit footer ruling, and two reviewer-requested trigger rewrites. No additional marketing claim.
- Omissions: editorial field prefixes and paragraph splitting/reordering create false positives; actual exclusions and merges follow the brief's section and evidence contract. No unclassified difference remains.

### Every reported addition

1. **Brief-required interface label, heading or caption; no new product claim.**

   `Illustration of one request.`

2. **Brief-required interface label, heading or caption; no new product claim.**

   `When the free list is exhausted`

3. **Brief-required interface label, heading or caption; no new product claim.**

   `max_paid_per_day / max_paid_per_month`

4. **Source evidence: verbatim real `examples/paid.yaml`, required by brief section 2.6.**

   `# Escalate to paid models only after free models are exhausted, and only`

5. **Source evidence: verbatim real `examples/paid.yaml`, required by brief section 2.6.**

   `# inside explicit dollar and share guardrails.`

6. **Source evidence: verbatim real `examples/paid.yaml`, required by brief section 2.6.**

   `exhaustion_policy: paid include_discovered_free: true free_models: [] paid_models: - openai/gpt-4o-mini - google/gemini-2.0-flash-001 max_paid_per_request: 0.05 max_paid_per_day: 1.00 max_paid_per_month: 10.00`

7. **Source evidence: verbatim real `examples/paid.yaml`, required by brief section 2.6.**

   `# Fraction of successful requests that may be paid (0.1 = 10%).`

8. **Source evidence: verbatim real `examples/paid.yaml`, required by brief section 2.6.**

   `# When true, paid fallback runs only if the request is tagged high-complexity.`

9. **Source evidence: verbatim real `examples/paid.yaml`, required by brief section 2.6.**

   `paid_only_high_complexity: false deny_data_collection: false baseline_paid_model: openai/gpt-4o-mini state_backend: sqlite`

10. **Audit artifact: exact binding quickstart code; fenced Markdown retains `>` between lines while HTML does not.**

   `python -m pip install freewhirr export OPENROUTER_API_KEY=sk-or-v1-...`

11. **Audit artifact: exact binding quickstart code; fenced Markdown retains `>` between lines while HTML does not.**

   `from freewhirr import Freewhirr with Freewhirr() as client: result = client.complete( messages=[{"role": "user", "content": "Explain vector clocks in one paragraph."}] ) print(result.model) print(result.content)`

12. **Source evidence: five lines from README library surface (543–568), required by brief section 2.8.**

   `result = client.complete(messages=[...], quality=MinLengthCheck(40)) async_result = await client.acomplete(messages=[...]) for chunk in client.stream(messages=[...]): print(chunk["choices"][0]["delta"].get("content") or "", end="") client.chat.completions.create(messages=[...])`

13. **Source evidence: verbatim README OpenAI client snippet (127–137), required by brief section 2.8.**

   `# examples/proxy_openai.py from openai import OpenAI client = OpenAI(base_url="http://127.0.0.1:8787/v1", api_key="not-used") response = client.chat.completions.create( model="freewhirr", messages=[{"role": "user", "content": "Give me a one-line haiku about buses."}], ) print(response.choices[0].message.content)`

14. **Brief-required interface label, heading or caption; no new product claim.**

   `POST /v1/chat/completions`

15. **Brief-required interface label, heading or caption; no new product claim.**

   `Setup notes in the README`

16. **Source evidence: verbatim `src/freewhirr/cli.py` subcommand help, required by brief section 2.8.**

   `Send a one-shot chat completion.`

17. **Source evidence: verbatim `src/freewhirr/cli.py` subcommand help, required by brief section 2.8.**

   `Run an OpenAI-compatible proxy.`

18. **Source evidence: verbatim `src/freewhirr/cli.py` subcommand help, required by brief section 2.8.**

   `Show free vs paid share and estimated savings.`

19. **Source evidence: verbatim `src/freewhirr/cli.py` subcommand help, required by brief section 2.8.**

   `List the free models the router would try.`

20. **Source evidence: verbatim `src/freewhirr/cli.py` subcommand help, required by brief section 2.8.**

   `Poll OpenRouter for new and stealth free models.`

21. **Source evidence: verbatim `src/freewhirr/cli.py` subcommand help, required by brief section 2.8.**

   `Print the resolved configuration (secrets redacted).`

22. **Brief-required interface label, heading or caption; no new product claim.**

   `Settings: yours, in any format`

23. **Brief-required interface label, heading or caption; no new product claim.**

   `constructor arguments: later wins`

24. **Source evidence: four-format policy illustration, required by brief section 2.9; TOML test verified.**

   `# YAML exhaustion_policy: stop`

25. **Source evidence: four-format policy illustration, required by brief section 2.9; TOML test verified.**

   `exhaustion_policy = "stop"`

26. **Source evidence: four-format policy illustration, required by brief section 2.9; TOML test verified.**

   `FREEWHIRR_EXHAUSTION_POLICY=stop`

27. **Source evidence: four-format policy illustration, required by brief section 2.9; TOML test verified.**

   `FreewhirrConfig(exhaustion_policy=ExhaustionPolicy.STOP)`

28. **Brief-required interface label, heading or caption; no new product claim.**

   `Full settings table in the README`

29. **Explicit user ruling: exact footer sentence.**

   `Not affiliated with OpenRouter.`

30. **Reviewer-requested rewrite, minor 3: distinct rate-limit explanation; binding source file unchanged.**

   `A rate limit is retried on the same model with backoff.`

31. **Reviewer-requested rewrite, minor 3: distinct timeout explanation; binding source file unchanged.**

   `A timeout is retried before moving to the next model.`

### Every reported omission

1. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Kicker: Free-first model router · independent project`

2. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Headline: Spend nothing until you choose to.`

3. **Audit artifact: full sub-headline present verbatim, editorial `Sub-headline:` prefix excluded.**

   `Sub-headline: freewhirr tries OpenRouter's $0 models in order and fails over when one rate-limits, errors or times out. Free models are not guaranteed to answer. When they all fail, you get an error unless you have opted in to paid fallback.`

4. **Intentional omission: hero status line violates brief four-element limit; independence in kicker/footer, OpenRouter dependency in settings/status, licence and version in closing.**

   `Status line (small, directly under the sub-headline): An independent open-source tool that sits on top of OpenRouter. It hosts no models and works with no other provider. MIT licensed, version 0.1.0.`

5. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Install command (copyable, beside the buttons): pip install freewhirr`

6. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Primary call to action: Install from PyPI`

7. **Intentional replacement: GitHub header/closing/footer links replace hero source action per brief.**

   `Secondary call to action: Read the source on GitHub`

8. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Heading: Free models are generous. They are also flaky.`

9. **Intentional trim: workaround sentence retained in Why; preceding catalog prose omitted for brief paragraph budget.**

   `OpenRouter lists models that cost $0 to call. They rate-limit, go down, and some have small context windows. The common workaround is to hard-code one cheap paid model, and then pay for work a free model would have done.`

10. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Heading: How a request is routed`

11. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `1. Build the free list. Models come from your own pinned list, from OpenRouter's catalog where the price is zero, or both. The catalog is cached for an hour by default.`

12. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `2. Try each model in order. A rate limit, server error or timeout is retried on the same model with backoff. A context-length error or most other client errors move straight to the next model.`

13. **Intentional omission: separate tool/quality-check steps excluded by brief section 10 and four-trigger layout.**

   `3. Skip models that cannot do the job. If the request includes tools, models that do not advertise tool calling are skipped. A malformed tool call counts as a failure and moves on.`

14. **Intentional omission: separate tool/quality-check steps excluded by brief section 10 and four-trigger layout.**

   `4. Check the answer, if you asked for a check. A minimum length, a JSON Schema or your own function can reject a response and trigger the next model. These checks do not run on streamed responses.`

15. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `5. Apply your policy when the list runs out. Stop with an error, or go to your paid list.`

16. **Audit artifact: heading present; editorial `Heading:` prefix excluded.**

   `Heading: Stop, or spend on purpose`

17. **Merged/split content: default and paid-list behaviour present in separate table cells; original paragraph continuity differs.**

   `stop is the default. When every free model has failed, freewhirr raises an error and calls nothing on your paid list.`

18. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `paid is opt-in. You list the paid models you accept, in order. freewhirr tries them only after the free list is exhausted, and only if every cap you set allows it:`

19. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `- a ceiling per request, checked against an estimate of the call's cost`

20. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `- a ceiling per day and per month, checked against a ledger on your machine`

21. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `- a maximum share of successful requests that may be paid`

22. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `- an option to allow paid only for requests you tag as high complexity`

23. **Audit artifact: full caps warning retained; inline-code fragment joining differs.**

   `Set the caps before you switch to paid. Every cap is off until you set it. With paid and no caps, the only limit is the list of models.`

24. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Heading: A library, a proxy, or a command line`

25. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `Agent harnesses. The README has setup notes for Claude Code, Codex, OpenCode, Cursor, Pi, Goose, Omnigent and Hermes. Most agent work needs a model that can call tools, which narrows the free list.`

26. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `Configuration comes from a YAML or TOML file, environment variables, or arguments in code, in that order of precedence. The one required setting is your OpenRouter key.`

27. **Intentional heading replacement: failure material distributed across walk, policies, proxy and “The cost of free”.**

   `Heading: When it goes wrong, and what leaves your machine`

28. **Intentional merge: paid-list exhaustion behaviour retained in table; named exception, proxy HTTP 402 and separate failure paragraph omitted for the brief layout.**

   `Every free model fails. Under stop, the library raises an error that lists each attempt, and the proxy returns HTTP 402 with the same list. Nothing on your paid list is called. Plan for this; it is the normal cost of running on free endpoints.`

29. **Intentional merge: streaming limit retained verbatim in walk; duplicate mid-stream paragraph omitted.**

   `A stream breaks part-way. The error reaches your client. freewhirr does not switch models once tokens have been sent.`

30. **Reordered/split: prompt egress, README warning, setting and consequence retained in privacy, split into the brief’s ruled layout.**

   `Your prompts. freewhirr sends your prompt to OpenRouter and to whichever model provider answers. The project's README warns that most free endpoints may train on prompts. Set deny_data_collection: true and freewhirr asks OpenRouter to route only to providers that do not collect prompts. That shrinks the free list, sometimes to nothing, and then stop fails closed.`

31. **Intentional omission: stealth narrative excluded by brief section 10; prescribed CLI watch help retained as source evidence.**

   `Stealth models. OpenRouter sometimes lists anonymous preview models at $0. freewhirr scores catalog entries that look like one and can alert you when a new one appears. On default settings a detected stealth model stays in the free list in its usual position. It is removed only when deny_data_collection is on. Do not send secrets or code you cannot leak through one.`

32. **Audit artifact: local ledger sentence retained in privacy; editorial topic label omitted.**

   `The ledger. Request logs and spend totals are written to a file on your machine. freewhirr has no telemetry of its own.`

33. **Audit artifact: tool-identifying-header sentence retained in privacy; editorial topic label omitted.**

   `What OpenRouter sees about the tool. Each request carries an app name and a link identifying freewhirr. You can change both.`

34. **Intentional omission: standalone savings heading replaced by merged privacy caveat.**

   `Heading: What it cost, and what it would have cost`

35. **Intentional omission: standalone ledger detail/heading replaced by privacy estimate caveat; no sample stats panel per brief.**

   `Every request is logged with the models tried, the outcome, the latency, the token counts and the cost. freewhirr stats adds that up and compares it with what the same tokens would have cost on one paid model you name as a baseline.`

36. **Audit artifact: proxy URL/policy sentence present, but parser separates inline code without retaining spaces at fragment joins.**

   `Then point an OpenAI-compatible client at http://127.0.0.1:8787/v1. With no configuration file the policy is stop.`

37. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Call to action: Install from PyPI`

38. **Merged/split content: retained relevant sentences or facts across the designated brief slots; metadata, ordinal, label or paragraph continuity differs.**

   `Footer links: PyPI · GitHub repository · Changelog · Open an issue`

39. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Footer line on the name: Named after Whir of Invention.`

40. **Audit artifact: editorial field label is absent; its visible content is present (name line moved into closing; PyPI label in footer).**

   `Footer small print: freewhirr is an independent open-source project by Andy McCutcheon. It is not affiliated with, or endorsed by, OpenRouter, OpenAI, Anthropic, or the makers of the tools and models it can work with. Product names belong to their owners.`

## Verification and limits

- `python3 tools/check_literals.py`: passed, now covers both pages and new shared stylesheet.
- `python3 tools/check_middle_dots.py`: passed, now covers both pages.
- Required copy-audit command: ran; classifications above. Complete raw output in ignored `.review/freewhirr-copy-audit.txt`.
- `python3 tools/render_check.py`, using already installed `.venv/bin/python3` and Chromium: passed. Existing Acheron checks retained; Freewhirr checks added for eight width/theme views, structural table roles, headline line/fit limits, long strings, no page overflow, no-script light/dark, clipboard exact content and fallback, theme switch, skip focus, keyboard code scrolling, reduced-motion press.
- Acheron pixel regression: **8/8 byte-identical PNG pairs** against clean `git archive ebccc26` at 360/768/1280/1440 in light/dark. Reduced-motion captures and the existing theatre warm-up make comparison deterministic. Screenshot evidence under ignored `.review/freewhirr/`. Source/content under `acheron/` and all `vendor/pattern/` files unchanged.
- Visual inspection: actual desktop light and mobile light captures reviewed. Eight theme/width captures available for independent review.
- `tools/freewhirr_contrast_check.py`: computed colours converted by canvas to sRGB and measured in installed Chromium at 1280 in both themes. Minimum text ratios: light 5.65:1; dark 5.31:1. Hover/focus text, focus outlines and gate rules pass their 4.5:1 / 3:1 bars. This is sampled state/viewport evidence, not a full axe audit.
- Conservative gzip asset sum approximately **156 KB**, including all three font files; shared script **1,518 bytes**, plus the small inline theme initializer. Fonts **138,144 bytes** gzip. No image, video, framework or browser/dependency install. Local Python preview serves uncompressed; the size sum measures prospective gzip payload, not a production network waterfall.
- `git diff --check`: passed.

**Remaining validation:** full axe serious/critical audit, Lighthouse mobile performance/Largest Contentful Paint/Cumulative Layout Shift/Total Blocking Time, exhaustive assistive-technology and transition-intermediate-state checks, and the independent different-vendor design review are not claimed as passed. No axe or Lighthouse dependency was installed to manufacture a gate. The brief's full gate set is not yet signed off.

**Open product questions:** none requiring implementation to pause; the listed user rulings resolve the binding decisions. Whether to accept the classified copy/layout reconciliations and remaining review gates belongs to the upcoming Grok review. Underlying priced-model/ledger caveats remain visible, not fixed in the product by this page.

## Reproduce

Use the existing virtual environment; no installation needed:

```sh
python3 -m http.server 8769 --bind 127.0.0.1
PATH="$PWD/.venv/bin:$PATH" LP_TEST_URL=http://127.0.0.1:8769/acheron/ python3 tools/render_check.py
LP_FREEWHIRR_URL=http://127.0.0.1:8769/freewhirr/ .venv/bin/python3 tools/freewhirr_contrast_check.py
python3 tools/check_copy.py /Users/andymccutcheon/Documents/GitHub/marketing-engineering/docs/proposals/2026-10-11-freewhirr-landing-copy-draft1.md
```

## Independent review fixes

Verdict on original commit `50dea7668918ea3e6456b1ef056c1496a8afc708`: ACCEPT WITH FIXES.

- Major 1: rewrite the original local commit into a product commit containing only `freewhirr/`, `shared/`, `docs/`, `tools/` and the README listing the Freewhirr page; retain `.agent/` and `CLAUDE.md` changes in a separate chore commit. No changes discarded.
- Major 2: both `.lp-ladder__gate` and `.lp-policy thead` use the new Freewhirr-scoped `--lp-route-gate-color` alias to Pattern secondary text. No Acheron-consumed token changes. Strengthen the sampler to enforce 4.5:1 on these two rules, while keeping 3:1 for the other non-text control checks. Light before: 4.1018:1 for both; light after: 6.2683:1 for both. Dark remains 7.7132:1 for both before and after. The updated threshold supersedes the initial 3:1 rule check reported above.
- Minor 3: rate-limit body is “A rate limit is retried on the same model with backoff.” Timeout body is “A timeout is retried before moving to the next model.” Retain all four brief-required triggers. Only these two copy-audit additions are new; the binding copy file is unchanged.
- Minor 4: Why fact label becomes `rate-limit` in place of bare `429`. This short label is below the copy auditor’s 24-character reporting threshold.
- Minor 5, log only: reviewer reported an axe-CI Chrome/ChromeDriver version mismatch. Recorded without changing either version or installing anything; axe validation remains unclaimed.

Review-fix checks: literal lint, middle-dot check, copy audit (31 additions, 40 omissions, fully classified), contrast sampling and complete render/regression gate rerun. Acheron remains byte-identical at all eight width/theme pairs against `ebccc26`.
