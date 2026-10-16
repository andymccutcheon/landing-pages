# Promptzilla site: Cloudflare packaging

This directory deploys `promptzilla/index.html` and the shared files it references as a
static-assets Worker named `promptzilla-site`, using the [`cf`](https://developers.cloudflare.com/cf/)
CLI. It is self-contained: nothing here changes the page, and nothing here is used by the
GitHub Pages workflow that publishes the other three pages.

There is no Wrangler configuration. `cf` is the CLI for this project, per
[Use `cf` with coding agents](https://developers.cloudflare.com/cf/agents/).

## Requirements

- Node.js 22.18 or newer. Loading `cloudflare.config.ts` requires it, and `cf` declares
  `node >= 22`. Bun is not supported.
- `npm install` in this directory. `cf` is a development dependency, so every command
  below runs through `npx` without a global install.

## What the build does

`npm run build` runs `scripts/build.mjs`, which:

1. checks that every `../`-prefixed reference in `promptzilla/index.html`, and every
   `url(...)` reference in the stylesheets it copies, appears in the script's explicit
   `SHARED_ASSETS` allowlist, and fails if one does not;
2. replaces `dist/` with the page, its `css/` and `assets/` directories, and only those
   allowlisted shared and vendored files;
3. rewrites the page's `../shared/` and `../vendor/` references to root-relative ones so
   the page can be served from `/`, and fails if any reference above the root survives;
4. writes the Cloudflare Build Output Specification tree in `.cloudflare/output/v0/` as an
   assets-only Worker: a `worker.config.json` with no bundle and no `manifest`, plus the
   staged `assets/` directory.

`dist/`, `.cloudflare/` and `node_modules/` are ignored by Git. Step 2 removes and
recreates `dist/`, which is a generated directory owned by this script.

## Check the build without deploying

```sh
cd promptzilla/cloudflare
npm install
npm run check
```

`npm run check` is `npm run build && cf deploy --dry-run --prebuilt`. `--dry-run` sends no
API requests and needs no credentials; `--prebuilt` validates the Build Output that the
build just wrote instead of rebuilding. A successful run reports the number of files read
from the assets directory and exits with `--dry-run: exiting now.`

`cf build` is **not** the command here. `cf build` delegates to a Cloudflare build tool
declared in `package.json` — the Cloudflare Vite plugin, or Wrangler — and this page has
no bundler and no Wrangler configuration. `scripts/build.mjs` is this project's build
implementation, which is what the configuration documentation means by "an assets-only
Worker can omit `entrypoint`; its build implementation must provide the asset source".
`cf deploy --dry-run --prebuilt` is therefore the closest non-deploying equivalent, and it
exercises the same Build Output that a real deploy uploads.

## Deploy

Sign in once, then deploy. Neither command has been run from this branch.

```sh
cd promptzilla/cloudflare
npx cf auth login            # add --no-browser over SSH or in a container
npx cf auth whoami           # confirms the account the deploy will use
npm install
npm run deploy               # npm run build && cf deploy --prebuilt
```

Set `CLOUDFLARE_ACCOUNT_ID` first if your login can reach more than one account;
`cloudflare.config.ts` reads it from the environment. In CI, set `CLOUDFLARE_API_TOKEN`
instead of signing in, as described in [Use `cf` in CI](https://developers.cloudflare.com/cf/ci/).

## Verify a deploy

```sh
npx cf workers list                                         # promptzilla-site is listed
npx cf workers versions list --worker-id promptzilla-site   # the version just uploaded
curl -sS -o /dev/null -w '%{http_code}\n' https://promptzilla-site.<your-subdomain>.workers.dev/
curl -sS -o /dev/null -w '%{http_code}\n' https://promptzilla-site.<your-subdomain>.workers.dev/css/promptzilla.css
curl -sS -o /dev/null -w '%{http_code}\n' https://promptzilla-site.<your-subdomain>.workers.dev/vendor/pattern/fonts/fraunces/fraunces-latin.woff2
```

Each request should answer `200`. `workersDev` is `true`, so the Worker gets a
`workers.dev` address; `previewUrls` is `false`, so per-version preview URLs are not
published. Run `npx cf workers list` or open the Cloudflare dashboard to read the
subdomain. A custom domain is not configured; see the GAPS section of the pull request.

## Roll back

List the versions, then point a new deployment at the one you want. `--versions` takes the
whole array as a single JSON value, and the percentages must total 100.

```sh
npx cf workers versions list --worker-id promptzilla-site
npx cf workers deployments create --worker promptzilla-site \
  --versions '[{"version_id":"<earlier-version-uuid>","percentage":100}]' --dry-run
```

Drop `--dry-run` to apply it. `cf` is in beta, so confirm the arguments with
`npx cf workers deployments create --help`, or find the current command with
`npx cf cli search "roll a Worker back to a previous version"`, before running it for real.
