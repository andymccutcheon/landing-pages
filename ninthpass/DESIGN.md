# Ninth Pass — The Review Room

**Revision:** flagship overhaul, October 2026. **Implementation:** complete local revision; not publicly deployed. The public site still serves the preceding design until an authorized deployment. `index.html` is the implementation, `COPY.md` the public copy record, and `specs/flagship-design-spec.md` the executable design contract.

## Positioning and argument

An open-source command-line prompt-review loop for terminal-capable agent builders who already have an authenticated worker. The alternative is drafting and critiquing in the same conversation. The distinction is an explicit staged process, checked return contracts and a retained review history—not a claim of objectively superior model answers.

The page leads with **“Put your prompts through review.”** It supports that statement with an unchanged recorded Claude Code run: three model-assigned prompt scores of **8, 8, 9**, two rewrites and two remaining suggestions after STOP. The final artifact is an inspectable example, not a certified summarizer. The runtime validator does not establish semantic evidence accuracy, actual application of claimed edits, twelve complete ratings, or guaranteed prompt improvement.

Reading this as a flagship developer-tool page with nocturnal scientific-editorial language. Dials: design variance 8, motion intensity 7, visual density 5. These are direction settings, not quality scores.

## Art direction

Large, tightly set typography leads. The first viewport is composed from a two-line statement, a concrete product description and a GitHub action. The explanatory imagery arrives after the first screen. Full serif editorial headings change the rhythm; no isolated decorative italic words. Diagram routes derive from the actual run and feedback relationships.

| Role | Token value | Intent |
| --- | --- | --- |
| Ground | `#151417` | smoked near-black |
| Surface | `#1e1d21` | slightly lifted graphite/plum |
| Raised | `#29272d` | controls, recommendation labels, process chambers |
| Primary text | `#f0eee9` | mineral white |
| Secondary / muted | `#c0bbc4` / `#a39da8` | supporting evidence and metadata |
| Action / active path | `#d4ed80` | restrained citron signal |
| Continuing score | `#dfb1bc` | desaturated rose, not an error state |
| Standard section | `#282e23` | deep dry olive, a quiet whole-field change |

All color, length and timing tokens live in `css/pz-tokens.css`. The existing static CSS architecture is retained; no new framework or token compiler. `css/diagrams.css` and all three diagram documents consume that same source.

Geist supplies display and body; Fraunces supplies complete editorial headings and scorecard quotations; Geist Mono is restricted to literal code. All are self-hosted with their existing licences. The hero is 126.7 CSS pixels at a 1440-pixel viewport; it remains two lines down to 280 pixels. Phone diagrams are recomposed vertically, not shrunk desktop screenshots. Final diagram label sizing is measured separately from CSS font size because the SVG viewBox scales it.

## Narrative architecture

1. **Hero:** category, value, audience, working GitHub action and worker prerequisite.
2. **A real run:** the first rewrite remains at 8. The six-stage trajectory, original request, run attribution, model-score qualification and selectable actual scorecard excerpts.
3. **Feedback:** five actual first-pass recommendations flow into one rewrite. Its APPLIED checklist does not prove fixes; the next Judge still scores 8.
4. **Process boundaries:** separate worker processes exchange explicit packets. Judge receives the prompt and relevant history; separate processes need not use different models and are not a security sandbox.
5. **Score and limits:** the published bands, what code validates, what it does not establish and the absence of demonstrated task-performance testing in the artifacts.
6. **Record:** the actual eight example files and completed/provisional/paused distinctions.
7. **Start:** source-first setup, a complete first-run command, supported workers, authentication/billing qualifications and the existing-prompt path.

Cut from the preceding page: unsupported “best-in-class,” “never saw the draft,” unconditional “until it reaches 9,” a twelve-enforced-sections claim, duplicated loop widgets, playback chrome, the light paper palette and the unqualified “no API key” promise.

## Diagram and motion contracts

The build command is `node tools/build_ninthpass_diagrams.mjs`. It reads scores from the unchanged example scorecards and asserts 8/8/9. Source-mapped recommendation labels are editorial summaries; the original files remain linked. The older `build_ninthpass_arbor.mjs` generator is historical and must not be used to overwrite this revision.

| Document | What it explains | Sequence |
| --- | --- | --- |
| `diagrams/loop.html` | time and the lack of guaranteed improvement | Compose → Judge 8 → Revise → Judge 8 → Revise → Judge 9 |
| `diagrams/arbor.html` | one scorecard's feedback anatomy | five feedback branches fan out, rest for reading, then gather into one rewrite; next Judge is still 8 |
| `diagrams/dataflow.html` | explicit handoff, retained artifacts and a fresh review process | prompt transfer, scorecard transfer, then rewritten-prompt return to a fresh Judge; records stay on disk |

Small traveling signals and short route segments animate over a stable complete composition. Each timeline repeats every 18 seconds, with opacity gone before the reset and a quiet rest between sequences. No changing text layout, flashing reset, per-frame JavaScript, simulated latency, live-generation claim or growing animation-instance collection. Each document has a fixed animation set; the inactive responsive SVG, offscreen iframe and background document are paused.

All embedded diagrams start automatically when visible and repeat without interaction. They have **no visible local playback controls, scrubber or play requirement**. SVG titles and descriptions carry complete text explanations; all labels and paths remain present with scripts disabled.

### Accessibility resolution for autonomous motion

The persistent header **Pause motion** setting stops all automatic diagram timelines. It becomes **Resume motion**, persists across reloads when storage is available and works without storage. Operating-system reduced motion takes precedence, disables the running preference and presents the complete still composition. Preference changes apply live. Standalone diagram documents provide their own page-level stop setting because no containing-page header is present.

This deliberately resolves the control-free presentation against [Web Content Accessibility Guidelines criterion 2.2.2, Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html): automatically starting movement beyond five seconds in parallel with other content needs a stop mechanism. Reduced-motion support alone is not claimed to satisfy it. No claim of complete assistive-technology certification is made from automated checks.

## Verification receipts

Evidence is local under the ignored `.review/ninthpass-flagship/` directory.

- **Ninth Pass render gate:** seven widths, 280/320/390/414/768/1024/1440 CSS pixels. No document overflow; two-line hero; loaded faces; primary action on the first screen; no undersized targets. Scorecard arrow/Home/End behavior, copy success/refusal, keyboard focus, local links, no-script reading, OS preference changes and motion preference persistence pass.
- **Motion gate:** each actual embedded diagram observed for more than two 18-second cycles on desktop and mobile. Six videos: `motion-video/loop-two-cycles.webm`, `arbor-two-cycles.webm`, `dataflow-two-cycles.webm` and their `-mobile-two-cycles.webm` counterparts; changing signal coordinates and timeline samples in `motion-results.json`. Zero visible embedded controls. Stable fixed instance counts; stopped time under pause/offscreen/reduced-motion conditions.
- **Contrast:** real-browser text, hover, focus and SVG fill/background measurements. Main text minimum **6.94:1**; interactive text and focus minimum **10.78:1**. Diagram text minima: loop **8.90:1**, arbor **9.74:1**, dataflow **7.84:1**. Minimum rendered phone diagram type at a 280-pixel viewport: **13.64 pixels**. No failures in the measured set. Receipt: `.review/ninthpass/contrast.json`.
- **Observed motion performance:** local Chromium, four seconds per active diagram, 241 frame intervals each. Median **16.7 milliseconds**, 95th percentile at most **16.8 milliseconds**, no observed long tasks. This is local evidence, not a device-wide frame-rate guarantee. Receipt: `performance.json`.
- **Source checks:** literal tokens, middle-dot style, JavaScript syntax and `git diff --check` pass. Installed taste source lint: **0 failures, 0 warnings**.
- **Installed taste browser inspector:** **0 failures, 3 warnings** with three declared scope exceptions. No stock-image quota for a command-line product explained by real data; iframe SVG motion is checked by the dedicated motion gate rather than the parent-only movement counter; actual score numerals were falsely detected as headings with an eyebrow. Warnings retained with reasons: mineral-white *text* was classified as a cream background; code legitimately uses a third font; live vector animation replaces video footage. The report is `.review/ninthpass-taste-final/report.json`.
- **Tooling boundary:** the installed design-doctrine package contains no `accuracy_report.mjs` or related generic gate scripts. They were not run or claimed. Existing project gates, the installed taste inspector and explicit browser checks supply the actual receipts.
- **Messaging owner:** rendered desktop/mobile review accepted; all scorecard states, diagram semantics, setup prerequisites and claim boundaries inspected. Visual implementation review inspected desktop, tablet and phone captures and the active diagram state; the final narrow-screen refinement increased diagram type rather than merely passing overflow tests.
- **Cloudflare packaging:** build and dry-run validation pass. All **30 required page/runtime/proof files** returned HTTP 200 from the locally served staged build; both primary actions point to the product repository. The package now includes shared diagram runtime files and unchanged proof artifacts. No public deployment has been performed.

**Cross-page aggregate:** `tools/render_check.py` passes on the final revision: Acheron's twelve theme/width captures, Freewhirr's eight, Shipwatch's twelve plus two no-script views, the unchanged sixteen byte-identical Acheron/Freewhirr baseline pairs and the seven Ninth Pass views. An earlier attempt exceeded a four-minute tool timeout; the subsequent full run completed successfully. No unrelated page runtime files changed.

## Remaining boundaries

No known blocking Ninth Pass defect in the checked Chromium views. Firefox, Safari and real assistive-technology testing have not been performed. The npm package remains unpublished at the availability check, so source setup remains primary. The rubric is the project's own, not a validated industry benchmark. This revision is uncommitted and undeployed until separately authorized.
