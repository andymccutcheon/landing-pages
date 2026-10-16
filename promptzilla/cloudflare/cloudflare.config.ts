import { defineConfig } from 'cf/config';

// Assets-only Worker: there is no entrypoint module, so every request is served
// from the static assets that `scripts/build.mjs` stages into Build Output.
export default defineConfig({
  // Set CLOUDFLARE_ACCOUNT_ID in your environment, or leave it unset when your
  // cf login has access to exactly one account.
  ...(process.env.CLOUDFLARE_ACCOUNT_ID ? { accountId: process.env.CLOUDFLARE_ACCOUNT_ID } : {}),
  worker: {
    name: 'promptzilla-site',
    compatibilityDate: '2026-10-01',
    workersDev: true,
    previewUrls: false,
    assets: {
      htmlHandling: 'auto-trailing-slash',
      notFoundHandling: 'none',
    },
  },
});
