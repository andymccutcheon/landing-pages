# Shipwatch implementation and sign-off ledger

Built on branch `shipwatch` in `/tmp/landing-pages-shipwatch`, isolated from the concurrent publication checkout. Starting main: `d42fe89`. No push, merge, deployment, workflow or main-branch commit. The existing publication allowlist intentionally remains untouched; adding Shipwatch is a later publication action.

## Sections as built

1. Hero: lowercase wordmark, fixed-behavior headline, install and two fictional stories.
2. In/out: staggered inputs and outputs, source kinds and archive.
3. Grounding: statement, three-column verdict scale, word-overlap limitation.
4. Scoring: weights table plus adjustments, adjustable-not-universal caveat.
5. Quickstart: three command blocks and other-command aside.
6. Modes: without model, with model, on schedule; stacked entries.
7. Limits: ruled statement and four entries, outbound requests and credential fallback.
8. Closing band: early-release status, contribution links and editorial limitation.
Footer follows. This matches the design brief's eight-section order. The copy draft's separate problem, sources, output preview and FAQ sections are merged or omitted rather than added as extra sections.

## Copy judgments for Katrina

The draft's fixed-behavior Option A is binding following Shipwatch main commit `5970c4f`. The headline is exactly **Know what AI companies actually shipped this week.** All warnings that undated entries are treated as current/included in every window are removed. The date fix does not fix semantic verification, model scores or key fallback: those caveats remain.

1. Hero lead uses the draft's shorter social copy verbatim: “Changelogs in, a cited briefing out. Each bullet links to its source and is checked for shared words with it.” The obsolete date warning is removed; the word-versus-meaning warning sits in Grounding and Limits. Status moves to Closing, per layout.
2. Specimen titles, claims, scores and source addresses are verbatim from stories six and eight of `examples/briefing.md`; these are new page fragments because the draft only specified a sample frame. Caption: “Sample output. The companies and products are invented. Two of the eight stories in the sample.” Link: “Read the full sample”. The design brief overrides the copy draft's four-story sample and coverage footer. Addresses are text, never dead links.
3. In/out heading is the draft's “How a briefing is built”, with design labels “What goes in”/“What comes out”. The pipeline list is redistributed into input/output and scoring/limits. Format labels and source-kind descriptions follow the brief. “shipwatch init writes a starter list of public sources to sources.yaml” removes the prohibited count; remaining edit-list wording comes from the draft.
4. Verdict conditions/outcomes are split into columns and reworded to match the brief's fractions: “Half or more of the claim's content words appear in the cited text.” / “Kept.”; “Between a quarter and a half.” / “Kept, and marked as flagged.”; “Less than a quarter, or no cited source.” / “Removed from the briefing.” Caption: “Content words are four characters or longer. The comparison is with the text of the cited items.” Added: “The verifier runs whether or not a model wrote the briefing.” This avoids the stale cross-reference “section 4”.
5. Scoring descriptions and numeric defaults follow the design table verbatim. Three adjustment labels split the draft's combined sentence into “Pricing changes get an added boost.”, “Deprecations get an added boost.”, “Security items get an added boost.” Added link label “Read the scoring configuration”. The keyword limits move to Limits; no accuracy/importance measurement is implied.
6. Quickstart follows the brief's Install/Set up/Run sequence; the draft combined setup and run into one block. Shell blocks preserve actual command syntax. “This run requests the public sources in your list. The briefing lands in…” replaces the draft's count and obsolete “second command”. Aside: “only updates the archive”, “briefs again from what is already stored”, “prints counts”, as specified by the brief. `shipwatch brief --since 7d` is the exact brief command.
7. Mode heading and fragments retain draft words. The claim that copied sentences “nearly always” pass is omitted to avoid an unmeasured quality implication. Model setup uses the draft's placeholder compatible endpoint rather than the brief's Freewhirr default, so the key and charging choice is explicit. Model-generated scores and failure fallback remain. “shipwatch has no billing of its own. Tokens go to the endpoint you configure and are billed, if at all, by whoever runs it.” trims “charges nothing”. The Freewhirr cross-link retains “a separate tool by the same author; its own page sets out its limits” and removes duplicated routing explanation. Added README link label “Other endpoints in the README”.
8. Schedule adds the README cron example verbatim, labelled “Cron example”, and “Weekly workflow example”. No timing promise. Nobody-reads-before-written warning is retained.
9. Limits uses brief labels “HTML extraction”, “Keyword rules”, “Near-duplicates”, “Source addresses”. HTML text becomes “Pages built in the browser extract thinly. Use a feed or GitHub Releases where a site offers one.”, removing the fixed date defect. Near-duplicate and source-address text come from the draft/brief. Outbound sentence merges the draft's two fragments: “Only if you use a model, the titles and text of fetched items go to the endpoint you configured.” Credential lookup and source failures remain verbatim (inline-code fragmentation aside). No empty-briefing or sitemap-first-run expansion is added beyond the prescribed four-item layout.
10. Closing: “shipwatch is version 0.1.0, an early release under the MIT licence. It is maintained by one person. Issues and pull requests are welcome.” replaces “the first public release” with the mandated status. “It drafts; it does not edit…” is retained. Footer non-affiliation/ownership wording retained, split into two paragraphs; links follow the design's six destinations. Accessibility labels and caption “Default scoring weights” follow the component needs.

ASCII apostrophes are retained to minimize incidental audit differences. Scores in fictional output, default weights, verdict rules, Python/version requirements, days and technical truncation lengths are permitted configuration/example facts, never adoption, uptime, speed or quality claims. No coverage figure, source count, seconds figure, fact-checked claim, universal privacy promise or private-stack origin claim is rendered.

## Technical choices

Only `--lp-brief-max: 36rem` is a new value. Shipwatch's refusal-border alias resolves to existing secondary text, independently scoped. The common install/no-JavaScript/theme/navigation/definition-list recipes move from Freewhirr to `shared/common.css` with equivalent specificity. Freewhirr adds one stylesheet link; no prose changes. Acheron and vendor files are untouched. No framework or build step.

At 1024 pixels the large display produced three headline lines; the brief expressly permits stepping down there. Medium display applies through 1279 and large from 1280, preserving two headline lines from 768. The verdict list uses three columns from 768 pixels. At 360 the weights descriptions move under the signal/weight, using the brief's explicit narrow-column fallback; HTML table roles are restored. Caption is visually hidden. Two invented source addresses wrap safely. Theme and copy controls are hidden without JavaScript.

## Audit classification

The mechanical copy gate checks fragments and full quoted lines, not semantic equivalence. Every reported delta is reproduced below. Additions are **design-specified specimens/components/commands**, **fixed-date conditional rewrites**, **section merges/splits**, **status ruling**, or **accessibility/navigation labels**, as itemized above. Omissions are **draft metadata prefixes/whole-paragraph fragmentation**, **content relocated/trimmed to the design's eight sections**, **fixed-date obsolete warnings**, **prohibited source counts/coverage figures**, and **the four-story specimen overridden by the two-story design**. No audit delta was silently repaired by editing binding sources.

```text
Auditing shipwatch/index.html
Page-to-copy differences (visible page fragments absent from the binding copy):
- Northwind Agents: northwind 1.2.0
- Northwind Agents 1.2.0 adds a stable tool-calling interface and removes the deprecated DeskRetrievalChain.
- https://github.com/example/northwind/releases/tag/v1.2.0
- Acme AI News: New fine-tuning recipes for structured outputs
- The API now ships official fine-tuning recipes for structured outputs so teams can keep JSON schemas stable across model upgrades.
- https://acme.example/index/structured-outputs-recipes
- Sample output. The companies and products are invented. Two of the eight stories in the sample.
- writes a starter list of public sources to
- Half or more of the claim's content words appear in the cited text.
- Between a quarter and a half.
- Kept, and marked as flagged.
- Less than a quarter, or no cited source.
- Removed from the briefing.
- Content words are four characters or longer. The comparison is with the text of the cited items.
- The verifier runs whether or not a model wrote the briefing.
- how distinct the title is from other items in the window
- the kind of item, plus keyword cues
- whether it reaches the API, enterprise or all customers
- newer items score higher; the default half-life is 7 days
- Read the scoring configuration
- Pricing changes get an added boost.
- Deprecations get an added boost.
- Security items get an added boost.
- python -m venv .venv && source .venv/bin/activate pip install shipwatch
- shipwatch init shipwatch sources check
- This run requests the public sources in your list. The briefing lands in
- only updates the archive
- shipwatch brief --since 7d
- briefs again from what is already stored
- export SHIPWATCH_BASE_URL=https://your-endpoint.example/v1 export SHIPWATCH_MODEL=your-model export SHIPWATCH_API_KEY=... shipwatch run --since 7d
- shipwatch has no billing of its own. Tokens go to the endpoint you configure and are billed, if at all, by whoever runs it.
- , a separate tool by the same author; its own page sets out its limits.
- Other endpoints in the README
- 0 9 * * 1 cd /path/to/project && .venv/bin/shipwatch --no-llm run --since 7d --out briefs
- Pages built in the browser extract thinly. Use a feed or GitHub Releases where a site offers one.
- Only if you use a model, the titles and text of fetched items go to the endpoint you configured.
- shipwatch is version 0.1.0, an early release under the MIT licence. It is maintained by one person. Issues and pull requests are welcome.
Copy-to-page differences (binding quoted lines absent from visible page text):
- Kicker: Changelog briefing tool · independent project
- Headline: Know what AI companies actually shipped this week.
- Sub-headline: shipwatch reads the changelogs and release notes you list, scores each item with a rubric you can tune, and writes a briefing where every bullet links to the item it came from. Each bullet is checked for shared words with its source. That is not a fact-check, and an entry with no date on its page is treated as current.
- Status line (small, directly under the sub-headline): An independent open-source tool that runs on your machine. It is a local pipeline, with no hosted service and no human editor. MIT licensed, version 0.1.0.
- Install command (copyable, beside the buttons): pip install shipwatch
- Primary call to action: Install from PyPI
- Secondary call to action: Read the source on GitHub
- Heading: Release notes are a firehose. Summaries drift.
- Keeping up with what shipped means reading a few dozen changelogs by hand, or pasting them into a chat model and trusting the summary. The first is slow. The second gives you sentences with no link back to where they came from, so you cannot tell a release from a paraphrase that wandered.
- shipwatch does the reading and keeps the link. It fetches the pages, sorts and scores what it finds, and drafts a briefing you can check bullet by bullet.
- Heading: How a briefing is built
- 1. Fetch. RSS and Atom feeds, HTML changelog pages, GitHub Releases, and docs sitemaps. Everything is stored in one SQLite file.
- 2. Sort. Each item is tagged as a launch, model release, pricing change, deprecation, API change, availability change, security item, non-shipment, or other. Without a model this is keyword matching.
- 3. Collapse repeats. Items with the same link, or mostly the same words, are merged. Related items are grouped into topics.
- 4. Score. A weighted rubric gives each item and each topic a number from 0 to 1.
- 5. Draft. The top topics become sections, twelve by default, with up to three bullets each when no model is used.
- 6. Check. Each bullet is compared with the item it cites, by shared words, and marked supported, flagged or dropped.
- Heading: What the check does, and what it cannot tell you
- Every bullet has a source. A claim that cites no known item is thrown out before the briefing is written.
- Every bullet is compared with that source. The verifier takes the claim's content words, four characters or longer, and counts how many appear in the item it cites. Half or more and the claim is marked supported. Between a quarter and a half, it is kept and marked flagged. Below that it is dropped. The footer of each briefing reports the counts.
- "Coverage" counts what was kept. It is supported and flagged claims together, as a share of all claims. It is not an accuracy score. Nobody has measured the verifier's accuracy against a labelled set, and this page publishes no such number.
- The link is to the item, which is not always the page that was read. For HTML changelogs the link is the first one found inside the entry. Sometimes that is a docs page the entry points to.
- Heading: A rubric you can tune
- Each item gets a number from 0 to 1 from four signals: how different its title is from the others in the window, what kind of item it is, how wide an audience it mentions, and how recent it is. Pricing changes, deprecations and security items get an added boost. Case studies, webinars, hiring posts and opinion pieces are tagged as non-shipments and take a penalty.
- Every weight is a line in shipwatch.yaml. Change them to suit what you cover.
- The signals are keyword rules. They will tag some posts wrongly, and a post the rules do not recognise is scored as "other". The number tells you how an item did against your rubric. It is not a general measure of importance.
- Heading: With a model, or without one
- Without a model (--no-llm). No key and no account. Each bullet is a sentence copied from the item: the first usable one, cut at 220 characters. Copied sentences nearly always pass the check, because they are being compared with the text they came from. Some will read as fragments.
- With a model. Point shipwatch at any OpenAI-compatible endpoint. It asks the model to classify each item, to pull facts from each item, and then to write the briefing. That is two calls for every item in the window, plus one. Count your items before you point it at an endpoint that charges.
- In this mode the model writes the headings, and the score printed beside a section is the model's own number when it supplies one. The check in section 4 still runs on every bullet.
- Who pays. shipwatch charges nothing and has no billing of its own. Tokens go to the endpoint you configure and are billed, if at all, by whoever runs it. The sample configuration points at freewhirr, a separate tool by the same author that tries OpenRouter's $0 models first; its own page sets out its limits.
- Heading: Sources, and how shipwatch fetches them
- shipwatch init writes a starter list of 27 public sources to sources.yaml: changelog pages, release feeds, news feeds and GitHub repositories from companies such as OpenAI, Anthropic, Google, Mistral, Cursor and Vercel. Edit it freely. A source is a few lines of YAML.
- Prefer feeds and GitHub Releases. They carry dates and clean entries. HTML pages are a fallback. A page that builds its content in the browser will extract thinly, and a page with no machine-readable date gives shipwatch nothing to place the entry in time.
- Sitemaps are watched for new addresses only. shipwatch records that a page appeared; it does not read the page. On the first run it has no history, so pages that already existed are listed as new.
- Fetch manners. Every request identifies itself as shipwatch. It reads each site's robots.txt and obeys it unless you turn that off, waits between requests to the same host, and asks for a page again only if it has changed.
- Heading: When it goes wrong, and what leaves your machine
- An entry with no date. shipwatch cannot tell when it was published, so it is included in every briefing window and can sit beside this week's releases. Changelog pages that head each month with plain text are the usual cause. Check the date on anything from an HTML source before you repeat it.
- A source fails. A blocked, unreachable or unparseable source is reported by name in the run output. The other sources still run.
- Nothing passes the check. The briefing says so and lists no claims.
- A scheduled run. The repository includes a cron example and a GitHub Actions workflow that commits each briefing. Nobody reads a scheduled briefing before it is written. Read it before you forward it.
- Requests to the sources. Each source receives an ordinary page request with a user-agent header naming shipwatch and linking its GitHub repository. If you set a GitHub token, it is sent to GitHub's API and nowhere else.
- Requests to a model. Only if you use one. The titles and text of fetched items go to the endpoint you configured.
- Which key is sent. shipwatch looks for the key variable you configured, then OPENROUTER_API_KEY, then OPENAI_API_KEY, and sends the first one it finds to your endpoint. Keep only the key for the endpoint you are using in that shell.
- Everything else stays local. The archive is one SQLite file in .shipwatch/. shipwatch has no telemetry of its own.
- Heading: What a briefing looks like
- Label (inside the sample frame, not below it): Sample. The companies and products are invented. The pipeline ran on test fixtures with no model, and computed the scores and the footer. This is not news about any real company.
- [The first four sections of examples/briefing.md, rendered as the tool writes them, with the grounding footer left in place inside the frame.]
- Caption: The footer reads "coverage 100%" because every bullet here was copied from its source. It reports what was kept, not how accurate the briefing is.
- Check the source list, then run a briefing
- The second command requests each of the 27 starter sources once. The briefing lands in out/ as briefing.md, briefing.json, briefings.xml and index.html.
- Later, if you want a model to write it
- Call to action: Install from PyPI
- Has the verifier been measured for accuracy?
- No. No accuracy figure has been measured against a labelled set, and none is published. The verifier compares words. A flagged claim is not necessarily wrong, and a supported claim is not necessarily right.
- Will HTML changelogs extract cleanly?
- Often not. Pages built in the browser extract thinly, and pages without machine-readable dates produce undated entries that appear in every window. Use a feed or GitHub Releases where a site offers one.
- Does shipwatch bill me for tokens?
- No. Tokens go to the endpoint you configured and are billed by whoever runs it. Without a model there is nothing to bill.
- What does the sample briefing represent?
- Unedited output of the pipeline, run with no model on invented companies. Regenerate it with python examples/generate_sample_briefing.py from a clone of the repository.
- Can I add my own sources?
- Yes. shipwatch init writes the list to sources.yaml. A source is rss, html, github or sitemap. shipwatch sources check validates the file.
- shipwatch is version 0.1.0, the first public release, under the MIT licence. It is maintained by one person. Issues and pull requests are welcome.
- Footer links: PyPI · GitHub repository · Changelog · Open an issue
- Footer small print: shipwatch is an independent open-source project by Andy McCutcheon. It reads public pages. It is not affiliated with, or endorsed by, any company whose changelog, feed or repository it can read, or any model provider it can call. Product names belong to their owners. The sample briefing on this page uses invented companies.
Copy diff result: 37 page addition(s), 66 copy omission(s) require explanation
```

## Verification

Literal lint, middle-dot gate, copy audit and `git diff --check`: pass. Copy audit: 37 additions and 66 omissions, classified above. Sample fidelity: the two title/claim/score/address groups match the repository's example (source names retained).

Full `tools/render_check.py`: pass, including twelve Acheron captures, eight Freewhirr captures, eight initial Shipwatch captures and two no-JavaScript captures. Expanded Shipwatch gate: pass, twelve theme/width captures at 360/480/768/1024/1280/1440, plus two no-JavaScript captures. All interactive assertions and all sixteen regression pairs passed again against the final styles. Interactive checks cover exact clipboard output, manual-copy fallback, keyboard code scrolling, theme toggle, skip-link focus, long strings, minimum targets and reduced motion. No page-level overflow.

Both approved pages: eight before/after PNG pairs each at 360/768/1280/1440, light and dark, byte-identical against `d42fe89`. Acheron's external iframe contents are masked in both phases, as in the existing approved gate; the full render gate separately verifies those hosted frames are loaded and nonempty. Acheron HTML/assets and Pattern snapshot are also unchanged in Git. Freewhirr prose is unchanged; the only HTML delta is the common stylesheet link.

Shipwatch gzip assets: 156,018 bytes (including all three fonts), shared script 1,552 bytes plus 172 bytes gzip for the inline theme initializer; well inside the 350 KB/15 KB budgets.

Contrast: light minimum text/interaction 5.65:1; dark minimum text 5.31:1. Refusal rule/table-header rule: 6.27:1 light, 7.71:1 dark. All measured text/state pairs clear 4.5:1 and focus/borders clear their thresholds.

At 360, install bottom approximately 479 pixels (740-pixel target); at 1280, install approximately 548 and specimen approximately 775 (800-pixel target). All specimen addresses wrap without becoming links. Screenshots visually inspected at 360 light, 1280 light and 768 dark.

No new axe verdict is claimed: inherited Chrome/ChromeDriver mismatch is logged, not repaired. Raw evidence lives under ignored `.review/shipwatch/`; the source audits under `.review/shipwatch-copy.txt`. Existing installed Playwright and Chromium used; no dependencies installed or browsers downloaded. Independent cross-vendor sign-off remains pending; these are implementer checks, not an independent verdict.

Logged only: inherited axe Chrome/ChromeDriver mismatch. Accepted Freewhirr 1.5px strong-border rendering and existing dark `--lp-system-*` token drift remain unchanged; revisit at a Pattern snapshot update. No new canonical agent-memory changes are mixed into this product commit. This report is the Shipwatch branch handoff.

Routing: user-assigned implementation, Codex native/OpenAI, existing fixed-plan lane; no model/harness selection or delegation performed. Different-vendor review remains external.
