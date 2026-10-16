import { defineConfig } from 'cf/config';

export default defineConfig({
  worker: {
    name: 'promptzilla-site',
    compatibilityDate: '2026-10-01',
    workersDev: true,
  },
});
