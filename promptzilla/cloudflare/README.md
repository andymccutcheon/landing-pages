# Promptzilla site on Cloudflare Workers

This project builds the static Promptzilla landing page as Worker assets using Cloudflare's `cf` CLI. `assemble.mjs` creates `dist/` from the page, its local stylesheet/script/SVG, the shared font/token/base styles, and only the two font files it references. The Vite plugin copies this public asset tree into the static-assets Worker output; `cloudflare.config.ts` supplies the Worker name, compatibility date, and Workers.dev setting.

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

```sh
npx cf workers deployments list --name promptzilla-site
```

Open `https://promptzilla-site.<your-subdomain>.workers.dev/promptzilla/` at desktop and mobile widths, including the install copy buttons. Verify the static response with:

```sh
curl -fsSI https://promptzilla-site.<your-subdomain>.workers.dev/promptzilla/
```

Set up an approved custom domain separately if required.
