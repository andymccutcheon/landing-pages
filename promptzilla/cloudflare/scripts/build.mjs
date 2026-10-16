#!/usr/bin/env node
// Assemble dist/ from an explicit allowlist, then write the Cloudflare Build
// Output Specification tree that `cf deploy --prebuilt` reads.
//
// The landing page itself has no build step. This script only copies files and
// rewrites the page's `../` repository-relative references so the page can sit
// at the Worker's root.

import { cleanBuildOutputDir, writeAssets, writeRootConfig, writeWorkerConfig } from '@cloudflare/build-output-utils';
import { loadAndParseConfig } from '@cloudflare/config';
import { cp, mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PROJECT = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const REPO = path.resolve(PROJECT, '../..');
const DIST = path.join(PROJECT, 'dist');
const PAGE = path.join(REPO, 'promptzilla/index.html');

/** Files copied from the repository root, published at the same path under dist/. */
const SHARED_ASSETS = [
  'shared/fonts.css',
  'shared/lp-tokens.css',
  'shared/base.css',
  'shared/motion.css',
  'shared/common.css',
  'shared/page.js',
  'vendor/pattern/generated/tokens.css',
  'vendor/pattern/fonts/instrument-sans/instrument-sans-latin.woff2',
  'vendor/pattern/fonts/instrument-sans/OFL.txt',
  'vendor/pattern/fonts/fraunces/fraunces-latin.woff2',
  'vendor/pattern/fonts/fraunces/OFL.txt',
  'vendor/pattern/fonts/jetbrains-mono/jetbrains-mono-latin.woff2',
  'vendor/pattern/fonts/jetbrains-mono/OFL.txt',
];

/** Page-local directories copied verbatim, published relative to dist/. */
const PAGE_DIRECTORIES = ['css', 'assets'];

const references = (source, pattern) => [...source.matchAll(pattern)].map((match) => match[1]);

/** Every `../`-prefixed reference the page makes, normalised to a repository path. */
function pageReferences(html) {
  const attributes = references(html, /(?:href|src)="(\.\.\/[^"]+)"/g);
  return [...new Set(attributes.map((reference) => path.posix.normalize(path.posix.join('promptzilla', reference))))];
}

/** Every `url(...)` reference a copied stylesheet makes, normalised the same way. */
async function stylesheetReferences(repoPath) {
  const css = await readFile(path.join(REPO, repoPath), 'utf8');
  const urls = references(css, /url\(['"]?([^'")]+)['"]?\)/g).filter((url) => !/^(?:data|https?):/.test(url));
  return urls.map((url) => path.posix.normalize(path.posix.join(path.posix.dirname(repoPath), url)));
}

async function assertAllowlistIsComplete(html) {
  const allowed = new Set(SHARED_ASSETS);
  const required = new Set(pageReferences(html));
  for (const stylesheet of SHARED_ASSETS.filter((asset) => asset.endsWith('.css'))) {
    for (const reference of await stylesheetReferences(stylesheet)) required.add(reference);
  }
  const missing = [...required].filter((reference) => !allowed.has(reference));
  if (missing.length > 0) {
    throw new Error(`Referenced files are missing from SHARED_ASSETS: ${missing.join(', ')}`);
  }
}

/** Move the page to the Worker root: `../shared/x` becomes `shared/x`. */
const rootRelative = (html) => html.replaceAll('"../shared/', '"shared/').replaceAll('"../vendor/', '"vendor/');

async function assertNoEscapingReferences(html) {
  if (html.includes('"../')) {
    throw new Error('The staged page still contains a reference above its own root.');
  }
}

async function stageDist(html) {
  await rm(DIST, { recursive: true, force: true });
  await mkdir(DIST, { recursive: true });
  const staged = rootRelative(html);
  await assertNoEscapingReferences(staged);
  await writeFile(path.join(DIST, 'index.html'), staged, 'utf8');
  for (const directory of PAGE_DIRECTORIES) {
    await cp(path.join(REPO, 'promptzilla', directory), path.join(DIST, directory), { recursive: true });
  }
  for (const asset of SHARED_ASSETS) {
    await mkdir(path.join(DIST, path.dirname(asset)), { recursive: true });
    await cp(path.join(REPO, asset), path.join(DIST, asset));
  }
}

async function countFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true, recursive: true });
  return entries.filter((entry) => entry.isFile()).length;
}

async function writeBuildOutput() {
  const context = { isPreview: false, mode: undefined };
  const { result } = await loadAndParseConfig(path.join(PROJECT, 'cloudflare.config.ts'), context);
  if (!result.success) {
    throw new Error(`cloudflare.config.ts did not parse: ${JSON.stringify(result.error ?? result, null, 2)}`);
  }
  await cleanBuildOutputDir(PROJECT);
  await writeRootConfig(PROJECT, result.data.settings, context);
  await writeAssets({ root: PROJECT, sourceDirectory: DIST });
  // No `manifest` and no bundle/: this is an assets-only Worker.
  await writeWorkerConfig({ root: PROJECT, config: result.data.worker });
  return result.data.worker.name;
}

const html = await readFile(PAGE, 'utf8');
await assertAllowlistIsComplete(html);
await stageDist(html);
const name = await writeBuildOutput();
console.log(`Staged ${await countFiles(DIST)} files into dist/ and wrote Build Output for Worker "${name}".`);
