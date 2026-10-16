# Alien UI design system snapshot

An immutable copy of the parts of the Alien UI design system that the Promptzilla page uses.
Replace the directory as a unit; do not edit these files in place.

- Source: `andymccutcheon/alien-frame-analysis`, `design-system/`, commit `6fd26f9`
- Contract version: `0.1.0` (private preview, per the source README and ROADMAP)

| File | Source path | Role |
| --- | --- | --- |
| `css/system-contract.css` | `design-system/css/system-contract.css` | Generated primitives, shared semantic roles for the industrial and science-ship registers, component geometry |
| `css/system-components.css` | `design-system/css/system-components.css` | `ui-button`, `ui-link`, `ui-status`, `ui-alert`, `ui-panel`, `ui-data-table` and font faces |
| `css/tokens.css` | `design-system/css/tokens.css` | Generated library tokens that the CRT components read (`--bg`, `--fg`, `--fg-dim`, `--fg-hi`, `--hot`) |
| `css/components.css` | `design-system/css/components.css` | `bezel`, `crt`, `readout`, the three brightness levels and `char-new` |
| `css/crt.css` | `design-system/css/crt.css` | DOM scanlines and vignette for `.crt`; the page turns off the flicker |
| `js/typeon.js` | `design-system/js/typeon.js` | Machine-paced type-on; it renders instantly under reduced motion |
| `fonts/` | `design-system/fonts/` | Share Tech Mono and Michroma, both SIL Open Font License (licence texts included) |

The fonts are TTF as shipped by the source. No font subsetting tools are installed here, so they
are not converted to WOFF2.
