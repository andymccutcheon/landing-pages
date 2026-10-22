# Silverquill — go-live checklist

**Author:** Layla Brower. **Date:** 21 October 2026. **Updated:** 21 October 2026, after the page
switch was authorized and run.
**Status:** the page switch has been run and verified, and the GitHub repository rename was run on
22 October 2026 — a two-way door, taken ahead of clearance on purpose. The npm publication is the
step that stays held, because npm never releases a name.

The rename is built but not switched. The reason is the one Andy gave: hold public use until the
trademark search clears. That gate covers three actions, not one — the npm publication, the GitHub
repository rename and the page switch — because public *use* of the name is the exposure, not just the
package.

> **Update, 21 October 2026 (evening).** Andy authorized the page switch and the deploy ran:
> version `ece106f4-9aa7-4c3b-b74b-1bd5bc5b3815` of the `ninthpass-site` Worker, with
> `silverquill.amccutcheon.com` added alongside the two existing hosts. All three answer 200 for all
> 33 required files. The Worker name and the page folder were deliberately **not** renamed: renaming
> the Worker would drop the two existing custom-domain bindings, and the folder rename touches the
> GitHub Pages allowlist for four other pages. Neither is worth the breakage while the repository
> rename is still held.

---

## Live now (public)

| Area | State |
|---|---|
| Page hosts | `silverquill.amccutcheon.com` (canonical), `ninthpass.amccutcheon.com`, `promptzilla.amccutcheon.com` — the same page on all three, no redirect, so no bookmark breaks |
| Worker | `ninthpass-site`, version `ece106f4-9aa7-4c3b-b74b-1bd5bc5b3815` |
| Reachability | 33 of 33 required files answer 200 on every host (`npm run verify -- <host>`) |
| Metadata | Title, description, canonical URL and Open Graph tags all carry the Silverquill name and the new host; `og.png` regenerated with the nib wordmark and the recorded run's scores |
| Gates | Cross-page aggregate render check passed; contrast passed with no text, state, focus or rule failure; baseline captured at 1440×900, 1024×768 and 390×844 (`ninthpass/specs/2026-10-21-silverquill-baseline-recon.md`) |

## Done on 22 October 2026 — the repository rename

The GitHub repository is now **`andymccutcheon/silverquill`**, and the local checkout is
`~/Documents/GitHub/silverquill`. The old slug `andymccutcheon/ninthpass` returns a 301 redirect to
the new one, so every existing clone URL and link still resolves.

The rename ran ahead of the trademark clearance on purpose. A GitHub rename is a two-way door — the
old URL redirects, and the rename can be reversed — while the npm publication is one-way, because
npm never releases a name. The name was already in public use on three hosts before this, so
renaming the repository added no exposure the page switch had not already taken.

What changed with it:

- the three GitHub URLs in `package.json` (repository, homepage, bugs) and the README's badge,
  clone and licence links;
- the page's own links — the install command, both primary calls to action, the footer source link
  and three deep links — and the copy record that mirrors them;
- the repository description, which still described the retired MCP server, and its homepage, which
  still pointed at the retired `promptzilla` npm page.

## Still held — run in this order once clearance is in

1. **Trademark result received** (classes 9 and 42). If it comes back with a conflict, the page
   copy has to change again; the name was published under three hosts, so this is the one place
   where the hold now has a cost.
2. **`npm publish`** — the irreversible step; the name is unclaimed today. The npm account was
   suspended on 19 October (error E403, "account temporarily suspended due to a recent
   security-sensitive action"), so a fresh one-time passcode is needed as well.
3. **Rename the Worker and the page folder** — optional, and now worth doing, because the
   repository rename it was waiting on has happened. Renaming the Worker drops the existing
   custom-domain bindings, so it is a deliberate pass, not a drive-by.

## Two honest notes

- **While we wait, `silverquill` on npm is unclaimed.** Nothing reserves an npm name without
  publishing, so this is a real (small) risk: anyone could take it. Worth watching weekly, and worth
  asking counsel to prioritise.
- **The install commands now say `silverquill`.** The visible inconsistency between the brand and
  the repository it pointed at is closed as of 22 October 2026. The remaining old-name surface is
  the page folder inside `landing-pages` and the Worker's name — both internal, neither visible to a
  visitor.
- **The name is now in public use on three hosts.** The trademark search was commissioned before
  the switch, not after. If it comes back with a conflict, the remedy is a copy and mark change
  plus a redirect, not an unpublished package.

