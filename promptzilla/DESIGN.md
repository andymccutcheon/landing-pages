# Promptzilla landing page — The Refinery

**Status:** redesign branch `redesign/promptzilla`, 2026-10-19. Verified locally and
packaged with a Cloudflare dry run; **not deployed**. The live page is still the Alien UI
build. Deploy only after `promptzilla@2.0.0` is on npm, because the page's install command
is the v2 command.

## 1. Read and dials

**Reading this as:** a developer-tool landing page for AI builders — people who already
have a model and an agent, and want the prompt craft to stop being manual.

| Dial | Value | Why |
| --- | --- | --- |
| `DESIGN_VARIANCE` | 7 | Asymmetric hero (7/5), a specimen card that overlaps the grid, and an editorial skill ledger. The page should feel composed, not templated. |
| `MOTION_INTENSITY` | 5 | Four motivated moves: the hero rise, the loop stepper, the worker tabs, and the command copy feedback. Everything else holds still. |
| `VISUAL_DENSITY` | 4 | A quiet paper surface with generous air. The dense material is the loop and the skill ledger, where the product earns attention. |

## 2. What changed from the Alien build

The page is a full redesign, not a reskin. It moves from used-future instrument panels,
phosphor CRT, Michroma and Share Tech Mono to a warm editorial refinery:

- **System.** Paper and ink, one vermilion accent, Instrument Serif for display, Geist for
  body and UI, Geist Mono for commands and labels. All faces are self-hosted, Latin-subset
  WOFF2, and used under the SIL Open Font License.
- **Content.** The page now sells Promptzilla v2 — five skills, one install command, a CLI
  that runs each stage in a fresh process, and a Markdown prompt at the end. The v1 MCP
  story (13 tools, 5 prompts, resources, Cloudflare self-hosting, the setup skill) is gone.
- **Interaction.** The register switch, CRT type-on, stage lamps and the fake-readout are
  gone. In their place: a loop stepper that starts at 08/CONTINUE and reaches 09/STOP, a
  keyboard-operable worker tab set, copy controls on every command, and a dark chamber
  that gives the loop a physical pause in the page.
- **Dependency.** `vendor/alien-ui/` is deleted. The page carries only its own CSS, JS,
  fonts and favicon. The Cloudflare build allowlist is now the page's own directories.

## 3. The system

### Colour

All values live in `css/pz-tokens.css`; `tools/check_literals.py` exempts that one file.

| Role | Value | Use |
| --- | --- | --- |
| Paper | `#f5f0e6` | page ground |
| Raised paper | `#fbf8f1` | specimen, command strips, file card |
| Deep paper | `#ece4d4` | the output section |
| Ink | `#171410` | text, primary button, dark chamber |
| Ink soft / faint | `#4f493f` / `#6f6557` | body and labels |
| Rule | `#d9cfbd` | hairlines |
| Accent | `#b8401f` | display italics, rules, focus |
| Accent deep | `#8f2c18` | small accent text on paper |
| Accent bright | `#e58a6c` | small accent text on the chamber |
| Chamber soft / faint | `#bcb19d` / `#8d8270` | body and labels on dark |
| Success / warning | `#2e6a4b` / `#855416` | status chips on paper |
| Success / warning bright | `#7fbf9a` / `#d8a45b` | status text on dark |

### Type

| Role | Face | Size and behaviour |
| --- | --- | --- |
| Display | Instrument Serif | `h1` `clamp(3.9rem, 10vw, 8rem)`, line-height 0.88; `h2` up to 5rem |
| Body | Geist | `clamp(1rem, 0.96rem + 0.18vw, 1.125rem)`, line-height 1.6, 64ch measure |
| Command and label | Geist Mono | 0.7–0.82rem, uppercase labels with 0.16em tracking |

The italic display phrase is the page's recurring accent: “your prompts”, “One gate”,
“each with a narrow job”, “not a chat log”, “you already trust”, “does not do”,
“Read the prompt”.

### Layout

- 12-column shell, 82rem max width, fluid gutter.
- Hero: copy on columns 1–7, specimen on 8–12. Below 48rem the two stack; the specimen
  loses its offset.
- The loop is a full-bleed dark chamber. On wide screens the readout is a left rail and
  the four stages share the right side; below 64rem they stack, and below 48rem the
  stages become a 2×2 grid.
- Skills are an ordered ledger, not a card grid: index, job, boundary. Hover adds a
  vermilion inset rule.
- Output is a split between a dark file card and three end states.
- Install is a split between the worker tabs and the install aside.
- Boundaries are a short, heavy dark band. Start is the one centred moment.

## 4. The argument

1. **Claim: prompts should not be hand-written.** Proof: the headline, the specimen card
   (a request, four stages, 09/STOP, the output path) and the install command.
2. **Claim: the loop is the product.** Proof: the interactive four-stage loop, the gate
   rule, the 08 → 09 score change, and the cap/plateau note.
3. **Claim: each skill has a narrow job.** Proof: the five-row ledger with explicit
   refusals.
4. **Claim: the output is a readable artifact.** Proof: the file card, the stage manifest,
   and the approved/provisional/paused rows.
5. **Claim: bring your own model.** Proof: the OpenCode, Claude Code and Codex tabs, each
   with a real command and a fresh-process note.
6. **Claim: the limits are honest.** Proof: the four boundary statements — no model call,
   no agent runtime, structure not truth, explicit fixes.
7. **Claim: start now.** Proof: the final install command and two GitHub calls to action.

## 5. Preserve list and cut list

**Preserve**

- The primary conversion path: the GitHub repository, reached twice (hero and final CTA).
- The real product vocabulary: Metapod, Judge Dredd, Brian Spillner, Tasker, Prompt
  Pipeline; `STOP`, `CONTINUE`, `full`, `optimize-only`, `approved`, `provisional`.
- No fabricated claims: no customers, counts, benchmarks, testimonials or “try it live”.
- No-JavaScript readability, keyboard operation, reduced motion, visible focus.
- The page's own Cloudflare packaging and reachability check.

**Cut**

- MCP, stdio, prompts/resources, 13 tools, Cloudflare self-hosting and the setup skill.
- The industrial register switch and its two dark palettes.
- The CRT bezel, phosphor, type-on engine and stage-lamp animation.
- The vendor Alien UI snapshot.
- The six-section datasheet rhythm; the new page has seven sections with a different
  rhythm: paper, chamber, paper, deep paper, paper, chamber, paper.

## 6. Motion and interaction thesis

- **Hero:** a 900ms staggered rise, copy first, specimen last. No parallax.
- **Loop:** the button steps four stages at 650ms each. The score changes at the second
  Judge pass; the track fills; the stage borders and dots move from pending to active to
  done. “Run again” is always available. Under reduced motion the page loads at 09/STOP
  and the button completes instantly.
- **Tabs:** `role="tablist"` with arrow, Home and End support. Only one panel is open.
- **Copy:** 2s “Copied” feedback with an `aria-live` announcement and a manual-selection
  fallback when the Clipboard API refuses.
- **Header:** a scrolled surface change and a scrollspy underline on the section links.

## 7. Verification

Run from the worktree root with the repository's Playwright environment:

```sh
python3 tools/check_literals.py
LP_PROMPTZILLA_URL=http://127.0.0.1:8777/promptzilla/ \
  ~/Documents/GitHub/landing-pages/.venv/bin/python tools/promptzilla_render_check.py
LP_PROMPTZILLA_URL=http://127.0.0.1:8777/promptzilla/ \
  ~/Documents/GitHub/landing-pages/.venv/bin/python tools/promptzilla_contrast_check.py
```

Measured on 2026-10-19:

- Six captures at 360, 480, 768, 1024, 1280 and 1440; no horizontal overflow, no small
  targets, one `h1`, seven sections, four stages, five skills, three tabs, two primary
  CTAs to the repository.
- Loop: 08/CONTINUE → 09/STOP; all four stages done; track at 1.
- No-JavaScript: all three worker panels visible; no visible buttons; 09/STOP; install
  command present.
- Reduced motion: no hero or stage animations; loop at 09/STOP.
- Contrast: no text failures; minimum large-display ratio 3.38:1; minimum interactive
  state 4.83:1; minimum focus ratio 3.31:1; gate rule 3.38:1.
- Gzip: 96,808 bytes of the 150,000-byte budget.
- Cloudflare: `npm run check` stages 14 files and `cf deploy --dry-run --prebuilt` passes.
- Built output: `verify.mjs` passes 14 reachability checks against a local `dist/` server;
  all three fonts load with no console or network errors.

## 8. Open items

- **Deploy after npm 2.0.0.** The page's install command is `npx promptzilla install`.
  Until the v2 package is published, that command installs the v1 MCP package. Publish
  first, then deploy.
- **OG image.** `assets/og.png` is a 1200×630 paper/ink/vermilion card, wired into
  the Open Graph and Twitter metadata.
- **Social proof and a before/after prompt.** Still absent, deliberately. Add only with
  real material.
- **Custom domain.** Already live on `promptzilla.amccutcheon.com`; keep it.
