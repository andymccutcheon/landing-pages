# Design System Pattern snapshot

- Source repository: `/Users/andymccutcheon/Documents/GitHub/design-studio`
- Source commit: `0292df0`
- Snapshot date: 2026-10-11
- Policy: `vendor/pattern/` is read-only and is replaced only by a new complete snapshot.
- Font verification: Fraunces was verified against upstream Fraunces 1.000 on 2026-10-11 by two independent checks; all 245 glyphs matched.

## Files and SHA-256

| File | SHA-256 |
|---|---|
| `RULES.md` | `91cd406d1d0793e0066e6cc7a7ed19407cf6ae87b57349813fbb42f3a3b9440e` |
| `fonts/fonts.json` | `44cd26590797885be395c7f8c9566dc7182a7e424904536cf6b6de352408fbd9` |
| `fonts/fraunces/OFL.txt` | `bdf4c22802eaf804f998195871c6b8938aac2ac14b2d78a8bd66a6f1eced833b` |
| `fonts/fraunces/fraunces-latin.woff2` | `48282a415ec22e31beaf0a0666e6fae0c8cbddcd0b1f6e729f27c3ade8a64e43` |
| `fonts/instrument-sans/OFL.txt` | `9e27a72ed30eb49a08678f6a5d6ed98ec7ba5368f541637ee0683ec9134ef966` |
| `fonts/instrument-sans/instrument-sans-latin.woff2` | `faa47d64961313a084b47cf95d373c27f9259898774fc258e2e72ec22175952d` |
| `fonts/jetbrains-mono/OFL.txt` | `b2fe5e8987594e9ffd1d2ca52a2f5d73eb8335243893c5d6254b5ad69269591d` |
| `fonts/jetbrains-mono/jetbrains-mono-latin.woff2` | `2c32b9b3ee358c119e210f6f5195f9bd34894d78a785ff2e95d60e718e400af4` |
| `generated/fonts.css` | `fff18b59eb3077a9e21bcad0e2770c0031cca7a759fd0c3642d068445c8ea4bc` |
| `generated/theme.css` | `0a840e94b4a49f61a25869a1e5777ad2261a394acbe32dc3e6fac2c35880313c` |
| `generated/tokens.css` | `a314e94c1e232a02a4449c1cf421ae9b6bb065a2d58c8a55641026e46c490b67` |
| `generated/tokens.json` | `1d990151e5e332fa2c34f17c978ee91394d3060e0e4096da98fb854b6fc2330c` |

## Browser stylesheet use

`generated/tokens.css` is loaded directly because it is plain CSS custom properties with the `--ds-` prefix. `generated/theme.css` is preserved unchanged for provenance but is not loaded: it targets Tailwind's theme layer and is not a reliable plain-browser stylesheet. `generated/fonts.css` is preserved unchanged; `tools/generate_fonts.py` creates `shared/fonts.css` with relative URLs and removes the unused italic face while keeping all declared weight ranges exactly.

