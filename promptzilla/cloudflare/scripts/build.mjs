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

/**
 * Files copied from the repository root, published at the same path under dist/. The Alien UI
 * snapshot is allowlisted file by file; vendor/alien-ui/SNAPSHOT.md is deliberately left out.
 */
const SHARED_ASSETS = [
  'vendor/alien-ui/css/system-contract.css',
  'vendor/alien-ui/css/tokens.css',
  'vendor/alien-ui/css/system-components.css',
  'vendor/alien-ui/css/components.css',
  'vendor/alien-ui/css/crt.css',
  'vendor/alien-ui/js/typeon.js',
  'vendor/alien-ui/fonts/Michroma.ttf',
  'vendor/alien-ui/fonts/Michroma-OFL.txt',
  'vendor/alien-ui/fonts/ShareTechMono.ttf',
  'vendor/alien-ui/fonts/ShareTechMono-OFL.txt',
];

/** Page-local directories copied verbatim, published relative to dist/. */
const PAGE_DIRECTORIES = ['css', 'js', 'assets'];

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

/**
 * Move the page to the Worker root. Every local reference becomes root-relative, so
 * the page resolves the same way whatever path serves it: `../vendor/x` and `css/x`
 * both become `/vendor/x` and `/css/x`.
 */
const ROOT_RELATIVE_REWRITES = [
  ['"../vendor/', '"/vendor/'],
  ['"css/', '"/css/'],
  ['"js/', '"/js/'],
  ['"assets/', '"/assets/'],
];

function rootRelative(html) {
  let staged = html;
  for (const [from, to] of ROOT_RELATIVE_REWRITES) {
    if (!staged.includes(from)) throw new Error(`The page no longer references ${from}; update ROOT_RELATIVE_REWRITES.`);
    staged = staged.replaceAll(from, to);
  }
  return staged;
}

/** Every href/src must now be root-relative, absolute, or a fragment. */
function assertEveryReferenceIsRootRelative(html) {
  const offenders = references(html, /(?:href|src)="([^"]+)"/g)
    .filter((reference) => !/^(?:\/|#|https?:|data:|mailto:)/.test(reference));
  if (offenders.length > 0) {
    throw new Error(`The staged page keeps non-root-relative references: ${offenders.join(', ')}`);
  }
}

async function stageDist(html) {
  await rm(DIST, { recursive: true, force: true });
  await mkdir(DIST, { recursive: true });
  const staged = rootRelative(html);
  assertEveryReferenceIsRootRelative(staged);
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
