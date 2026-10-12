# Publication preparation — 2026-10-12

Andy authorized creation of the empty public `andymccutcheon/landing-pages` repository
and preparation of a local publication commit. Nothing may be pushed until an
independent reviewer from a different vendor clears the workflow and URL diff.

Created the empty repository, added HTTPS origin, and configured Pages with
`build_type=workflow`; no workflow was dispatched. Added `.github/workflows/pages.yml`
with a strict static-file allowlist and generated `.nojekyll`. No root index was
requested; destinations are `/landing-pages/acheron/` and `/landing-pages/freewhirr/`.

Acheron social images now use absolute landing-pages URLs. Both theatre iframes use
the live Acheron documentation-site URLs. Freewhirr has no social image or relative
cross-page links to rewrite. Shared frame loading now supports external origins.
The browser gate checks hosted frame content through Playwright, and masks iframe
pixels only in the old-local-versus-new-hosted regression comparison.

Verification: allowlist staging shell executed successfully; literal and punctuation
gates passed. The updated render gate passed: twelve Acheron captures, eight
Freewhirr captures, hosted-frame content checks, and eight surrounding-page
before/after pixel comparisons. Accessibility interaction and layout gates passed.

After independent cross-vendor clearance, run `git push -u origin main`. The new
publication commit is the sole commit after the original reviewed head `a08b9f6`.
No push, deletion, or workflow dispatch was performed during preparation.
