# Promptzilla landing page: Alien UI redesign

This page restyles the editorial Promptzilla page (branch `polly/pz-editorial`, commit `94ee878`,
live as of 2026-10-16) on the Alien UI design system. It is an overhaul in the `design-taste-frontend`
sense: new visual language, same content, information architecture, section IDs and conversion path.

## 1. Design read and dials

**Reading this as:** a developer-tool landing page for AI builders, rendered in the Alien UI
industrial register: used-future instrument panels, a phosphor CRT, Michroma display type and Share
Tech Mono interface type, on the system's shared semantic roles.

| Dial | Value | Why |
| --- | --- | --- |
| `DESIGN_VARIANCE` | 6 | Asymmetric hero (copy left, instrument right), but the rest is ruled and orderly, as instrument panels are. |
| `MOTION_INTENSITY` | 4 | Two motivated moves only: the CRT's last line types on at the system's machine pace (50 ms per character), and the four stage lamps light once in pipeline order. Both are static under reduced motion. The CRT flicker is turned off. |
| `VISUAL_DENSITY` | 5 | A datasheet audience. The page shows facts, not atmosphere. |

## 2. The system and how it is consumed

`vendor/alien-ui/` is an immutable snapshot of `alien-frame-analysis/design-system` at `6fd26f9`
(see `vendor/alien-ui/SNAPSHOT.md`). The page imports the system's generated contract, components,
CRT layer, type-on engine and fonts unchanged. It does not use this repository's Pattern layer
(`shared/`, `vendor/pattern/`), so the three published pages are unaffected.

- **Colour** resolves through the contract's semantic roles (`--alien-semantic-color-*`). The page
  defines no colour of its own.
- **Raw lengths** live in `css/pz-tokens.css`, which `tools/check_literals.py` now treats as a
  token file alongside `shared/lp-tokens.css`.
- **Theme.** The system is dark by construction. The page is dark-locked (`color-scheme: dark`),
  and its theme control is the system's register choice: Industrial (default) or Science ship. A
  pair of buttons uses truthful `aria-pressed`, as `COMPONENTS.md` specifies, and the choice is
  stored in `localStorage` under `pz-register`. The CRT phosphor follows the register's accent so
  the science-ship screen is not a green island.

## 3. Component mapping

| Section | Alien UI component | What it carries |
| --- | --- | --- |
| Hero instrument | `bezel` + `crt` + `readout` + `selected` + `t-hot` | The seven README facts that used to sit in the "At a glance" stamp. The last line is the real output of `npx -y promptzilla --validate` (`src/cli.ts:26`), labelled as such in the caption. It is a real-content preview, not a mock terminal. |
| Pipeline rail | Annunciator-style lamps (page CSS on contract roles) + a warning-toned gate | Four stages, with the loop stage drawn as an open lamp. The gate uses the warning role because it is the rule that can refuse approval. |
| What each stage is allowed to do | `ui-data-table` | Skill, job and boundary for each of the five skills. On phones the rows stack. Explicit `table`/`row`/`rowheader`/`cell` roles keep the semantics through the display change. |
| How a run ends | `ui-status` with real states | positive Approved, warning Provisional, neutral Paused, danger Blocked. Each status uses colour and a word, never colour alone. |
| Modes | `ui-panel` (two) + aside | `full` and `optimize-only`, plus what the server exposes. |
| Install | Terminal command surfaces + `ui-button` copy controls | Copy uses the Clipboard API with a manual-selection fallback. |
| Every run is a directory | `ui-data-table` with a caption | The run's stage files. |
| What Promptzilla does not do | `ui-alert` (static, no live role) | One warning-toned lead ("It does not run an agent for you"), then four neutral boundaries. |
| Status | `.pz-action` links | "Get it on GitHub" and "Open an issue". |

`COMPONENTS.md` reserves `ui-button` for native `<button>` actions (here, the copy controls). The
GitHub calls to action are navigation, so they are real links with a page-local `.pz-action` style
built on the same contract roles and control geometry, as the system's own home page does for its
actions.

**CRT readout contrast.** The system's dim phosphor level (`--fg-dim`) measures 4.12:1 on the
industrial screen, under the 4.5:1 text floor. The readout therefore uses two levels, `--fg` for
labels and `--fg-hi` for values. A third, hot level is reserved for the typed line. The register
contrast is unchanged.

## 4. Copy changes from the editorial build

The copy is carried over verbatim. The editorial `DESIGN.md` at `94ee878` records its claim-by-claim
provenance against the README, the source skills and the package. A cross-check on 2026-10-16
against the public repository and npm `promptzilla@1.0.0` found no wrong claims. Deltas:

- The rail's loop stage reads "Judge again" instead of "Back to 02", because stage numbers are gone.
- Each skill's boundary ("Never performs the task.", "Evaluates only." and so on) moved into its
  own table column. Brian Spillner's boundary is "Cuts nothing that was not asked for", from
  `README.md:215-216`.
- The outcomes rows lead with a status word (Approved, Provisional, Paused, Blocked) that names the
  run state from `README.md:191-197`. Blocked rows are labelled "Rejected twice" (`README.md:188-190`).
- The meta description now says "until a 9 or 10 approves it", matching the gate rule
  (`README.md:203-204`).
- The footer credit states that the interface style is an original, film-inspired system, and
  that both fonts are used under the OFL. It also states that the skill names imply no
  affiliation. "Judge Dredd" is the product's real skill name and is kept. Whether to rename the
  skill is the product owner's decision, not the page's.

## 5. Where a skill or rule was overruled

| Rule | Decision |
| --- | --- |
| Taste: "design for both light and dark modes" | **Overruled by the chosen system.** Alien UI ships two dark registers and no light mode. The register switch is the theme control. |
| Taste: no div-based fake terminals | **Not triggered.** The CRT shows real facts and real CLI output, and is labelled. |
| Taste: no neon glows | **Scoped exception.** Phosphor bloom is the system's CRT treatment and stays inside the bezel. The stage lamps carry a small glow because they show lit state. Nothing else glows. |
| Alien UI `crt.css` flicker (0.15 s infinite) | **Turned off.** It is atmospheric motion with no message, and a persistent flicker is a photosensitivity risk. |
| Alien UI `COMPONENTS.md`: tables keep their semantics on small screens | **Kept** through explicit ARIA roles while the skill rows stack visually. |
| Repository `CLAUDE.md`: keep raw literals in `shared/lp-tokens.css` | **Extended.** This page does not load the Pattern layer, so its literals live in its own token file, and the lint covers it. |
| Fonts as WOFF2 | **Deferred.** The system ships TTF and no subsetting tool is installed. This costs about 100 KB uncompressed. |

## 6. Open items

Inherited and still open:
- A share image (OG image)
- A custom domain
- Social proof
- A real before and after prompt example

New:
- Subset the two fonts to WOFF2
- Decide whether the Science-ship register earns its place on a marketing page, or should be
  removed for focus
