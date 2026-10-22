# Silverquill — go-live checklist

**Author:** Layla Brower. **Date:** 21 October 2026.
**Status:** everything below the line is prepared and tested. Nothing below "Held" has been run.

The rename is built but not switched. The reason is the one Andy gave: hold public use until the
trademark search clears. That gate covers three actions, not one — the npm publication, the GitHub
repository rename and the page switch — because public *use* of the name is the exposure, not just the
package.

---

## Prepared and verified (nothing public)

| Area | State |
|---|---|
| Product code | `package.json` name and binary are `silverquill`; CLI help, error prefix and user-facing messages renamed; env vars are `SILVERQUILL_*` with `NINTHPASS_*` still accepted |
| Legacy runs | `~/.silverquill/runs` is the new default; if it does not exist and `~/.ninthpass/runs` does, the old directory is used, so existing history is never orphaned |
| Product tests | `npm run build` clean, **59/59 tests pass**, type tests pass, installed-package smoke passes |
| Product defects | README release statement corrected; the npm badge that pointed at a 404 removed; the `revise` skill no longer says "Toast-specific" and no longer claims an effect on downstream agent performance |
| Page | Copy, metadata, wordmark, favicon, hero qualification, revision-diff section and skills block all in place |
| Diff integrity | `tools/check_silverquill_diff.py` — 10 quotations and 2 line counts verified against the run files |
| Not changed | palette, type pair, motion system, the three diagram documents, section order apart from the one added section |

## Held — run in this order once clearance is in

1. **Trademark result received** (classes 9 and 42). If it comes back with a conflict, stop here and
   reopen the name; nothing has been published.
2. **`gh repo rename silverquill`** on `andymccutcheon/ninthpass`, then update the three GitHub URLs in
   `package.json` and the links in `README.md` (they are deliberately still pointing at the old slug).
3. **Update the page's links** that reference the old repository path and the run-artifacts path.
4. **`npm publish`** — this is the irreversible step; the name is unclaimed today.
5. **Switch the page**: rename the page folder and worker, add `silverquill.amccutcheon.com`, deploy,
   and keep a redirect from the old host.
6. **Regenerate** `og.png` with the new name and mark (`tools/render_ninthpass_social.py`), and move
   the two brand files out of `brand/silverquill/` into the renamed page folder.
7. **Re-run** the render check, the contrast check and the cross-page aggregate, then announce.

## Two honest notes

- **While we wait, `silverquill` on npm is unclaimed.** Nothing reserves an npm name without
  publishing, so this is a real (small) risk: anyone could take it. Worth watching weekly, and worth
  asking counsel to prioritise.
- **The install commands still say `ninthpass`.** That is correct until step 2 — changing them now
  would produce a command that fails. The page therefore shows a Silverquill brand above a `git clone`
  of the old repository, which will look odd if anyone sees it before the switch. That is the cost of
  preparing ahead of the gate, and it is why the page is not published yet.
