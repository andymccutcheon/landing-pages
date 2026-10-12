---
permalink: landing-pages-memory/state
title: state
type: note
---

# Landing pages handoff

All three pages are LIVE on GitHub Pages (Acheron, Freewhirr, Shipwatch) from `main` of the public repository `andymccutcheon/landing-pages`; Shipwatch 0.1.1 released 2026-10-12. Docs (`CLAUDE.md`, `README.md`, commit `d54b469`) cover the three pages, the shared Pattern system (`shared/`, `--lp-` tokens), the render/contrast/copy/regression gates, the Pages allowlist, and the step-by-step "add a page" guide.

Authoritative close-out: `hellDivers/.agent/handoffs/2026-10-12-shipwatch-landing-publication.md` (completion + backlog with owners). Full dispatch history: `hellDivers/.agent/inbox/2026-10-11-vanguard-landing-pages-routing-log.md`. Session notes: `sessions/2026-10-12-freewhirr.md`, `sessions/2026-10-12-publication-preparation.md`.

Backlog (owners in the handoff): Freewhirr product fixes (stop=never-spend escape hatches, uncapped paid policy, proxy no auth); Shipwatch follow-ups (future-dated exclusion test, SQLite ISO-text ordering); Freewhirr live-Lab fix. Loose end: Layla's design brief and Katrina's copy draft remain untracked in their own repos (inbox notes dropped to each).

Operational: use `.venv/bin/python3` for Playwright checks; system Python for source checks; preview on 8769 if 8766 is occupied; `.review/` is ignored.

> Corrected 2026-10-12 by Cricket (Omnigent operations): this file still described the pre-publication Freewhirr stage ("no remote exists; do not push or deploy") — stale after the overnight close-out. Sources: the successor session's close-out summary (2026-10-12 07:44) and the 07:31 handoff.
