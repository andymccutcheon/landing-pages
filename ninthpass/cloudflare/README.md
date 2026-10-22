# Ninth Pass site: Cloudflare packaging

This directory deploys `ninthpass/index.html` and its page-local `css/`, `js/`,
`assets/`, `diagrams/` and unchanged `examples/` proof artifacts as a static-assets Worker named `ninthpass-site`, using the
[`cf`](https://developers.cloudflare.com/cf/) CLI. It is self-contained: nothing here
changes the page, and nothing here is used by the GitHub Pages workflow that publishes
the other pages.

There is no Wrangler configuration. `cf` is the CLI for this project, per
[Use `cf` with coding agents](https://developers.cloudflare.com/cf/agents/).

## Requirements

- Node.js 22.18 or newer. Loading `cloudflare.config.ts` requires it, and `cf` declares
  `node >= 22`. Bun is not supported.
- `npm install` in this directory. `cf` is a development dependency, so every command
  below runs through `npx` without a global install.

## What the build does

`npm run build` runs `scripts/build.mjs`, which:

1. checks that every `css/`, `js/`, `diagrams/`, `examples/` and `assets/` reference in `ninthpass/index.html`
   resolves to a real file, and that every non-data `url(...)` in the page stylesheets
   resolves to a real asset;
2. replaces `dist/` with the page and its five runtime/proof directories, then rewrites
   every local reference to a root-relative one (`css/x` becomes `/css/x`, and so on);
   it re-reads the staged page and fails unless every `href` and `src` is root-relative,
   absolute, a fragment, or a data/mailto URL;
3. writes the Cloudflare Build Output Specification tree in `.cloudflare/output/v0/` as an
   assets-only Worker: a `worker.config.json` with no bundle and no `manifest`, plus the
   staged `assets/` directory.

`dist/`, `.cloudflare/` and `node_modules/` are ignored by Git. Step 2 removes and
recreates `dist/`, which is a generated directory owned by this script.

## Check the build without deploying

```sh
cd ninthpass/cloudflare
npm install
npm run check
```

`npm run check` is `npm run build && cf deploy --dry-run --prebuilt`. `--dry-run` sends no
API requests and needs no credentials; `--prebuilt` validates the Build Output that the
build just wrote instead of rebuilding. A successful run reports the number of files read
from the assets directory and exits with `--dry-run: exiting now.`

## Deploy

Sign in once, then deploy only after the public deployment is authorized. The page uses the
working clone-and-build setup path while the npm package is unpublished; publication is not a
prerequisite for this page revision. Repository source changes and a public deployment are separate actions.

```sh
cd ninthpass/cloudflare
npx cf auth login            # add --no-browser over SSH or in a container
npx cf auth whoami           # confirms the account the deploy will use
npm install
npm run deploy               # npm run build && cf deploy --prebuilt
```

Set `CLOUDFLARE_ACCOUNT_ID` first if your login can reach more than one account;
`cloudflare.config.ts` reads it from the environment. In CI, set `CLOUDFLARE_API_TOKEN`
instead of signing in, as described in [Use `cf` in CI](https://developers.cloudflare.com/cf/ci/).

## Verify a deploy

Reachability is one command. It requests all thirty-three required page/runtime/proof files,
requires `200` from each, and asserts that the served HTML still carries two primary calls
to action pointing at the Ninth Pass repository and references its stylesheet, page
script and favicon.

```sh
npm run verify -- https://silverquill.amccutcheon.com
```

The page answers on three hosts — `silverquill.amccutcheon.com` (canonical),
`ninthpass.amccutcheon.com` and `promptzilla.amccutcheon.com` — and the verify command passes
against each of them.
