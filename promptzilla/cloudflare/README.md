# Promptzilla site on Cloudflare Workers

This project builds the static Promptzilla landing page as Worker assets using Cloudflare's `cf` CLI. `assemble.mjs` creates a root `dist/index.html` plus its local stylesheet/script/SVG, the shared font/token/base styles, and only the two font files it references. The root route serves the landing page directly; its asset URLs are rewritten for that root layout. The Vite plugin copies this public asset tree into the static-assets Worker output; `cloudflare.config.ts` supplies the Worker name, compatibility date, and Workers.dev setting.

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
