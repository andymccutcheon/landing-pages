# Promptzilla site on Cloudflare Workers

This project builds the static Promptzilla landing page as Worker assets using Cloudflare's `cf` CLI. `assemble.mjs` creates a root `dist/index.html` plus its local stylesheet/script/SVG, the shared font/token/base styles, and only the two font files it references. The root route serves the landing page directly; its asset URLs are rewritten for that root layout. The Vite plugin copies this public asset tree into the static-assets Worker output; `cloudflare.config.ts` supplies the Worker name, compatibility date, and Workers.dev setting.

## Browser checks by layout

The repository render and contrast checks target the source page at `/promptzilla/` by default. Serve the worktree root and set `LP_PROMPTZILLA_URL=http://127.0.0.1:<port>/promptzilla/` when running `tools/render_check.py` and `tools/promptzilla_contrast_check.py`. The full repository render command also needs the corresponding `LP_TEST_URL`, `LP_FREEWHIRR_URL`, and `LP_SHIPWATCH_URL` source paths when using a non-default port.

To test the assembled Cloudflare root layout instead, build and serve `dist/`, then set `LP_PROMPTZILLA_URL=http://127.0.0.1:<port>/` explicitly. The `npm run verify -- http://127.0.0.1:<port>` script checks that assembled root and all referenced assets; against a deployment, pass its base URL instead.

## Build locally

Requires Node.js 22+ and npm. From this directory:

```sh
npm install
npm run build
```

`npm run build` assembles `dist/` and runs `cf build`. It does not authenticate, publish, or deploy.

## Deploy (maintainer action)

After reviewing the built page and configuring Cloudflare access, run from this directory:

```sh
npm install
npm run deploy
```

This invokes `cf deploy` for Worker `promptzilla-site` with Workers.dev enabled. It requires a configured Cloudflare account/login. This repository task does not run deployment or login.

## Verify deployment

Run the real reachability check with the deployed base URL (no trailing path required):

```sh
npm run verify -- https://promptzilla-site.<your-subdomain>.workers.dev
```

It GETs `/`, asserts the Promptzilla GitHub CTA is present, and checks all referenced local assets, including CSS imports and font URLs. For deployment history only, use the separate informational command:

```sh
npm run deployments
```

Set up an approved custom domain separately if required.
