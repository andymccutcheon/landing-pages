#!/usr/bin/env node
// Assemble dist/ from the page and its page-local css, js and assets, then write
// the Cloudflare Build Output Specification tree that `cf deploy --prebuilt` reads.
//
// The landing page has no bundler. This script copies files, rewrites the page's
// css/js/assets references to root-relative URLs, and checks that every local
// reference exists before anything is staged.

import { cleanBuildOutputDir, writeAssets, writeRootConfig, writeWorkerConfig } from '@cloudflare/build-output-utils';
import { loadAndParseConfig } from '@cloudflare/config';
import { cp, mkdir, readFile, readdir, rm, stat, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const PROJECT = path.resolve(fileURLToPath(new URL('..', import.meta.url)));
const REPO = path.resolve(PROJECT, '../..');
const PAGE_DIR = path.join(REPO, 'ninthpass');
const PAGE = path.join(PAGE_DIR, 'index.html');
const DIST = path.join(PROJECT, 'dist');
const PAGE_DIRECTORIES = ['css', 'js', 'assets', 'diagrams'];
// Root-level files served from the site root rather than from a directory.
const PAGE_ROOT_FILES = ['robots.txt', 'sitemap.xml'];

const references = (source, pattern) => [...source.matchAll(pattern)].map((match) => match[1]);

async function exists(target) {
  try {
    await stat(target);
    return true;
  } catch {
    return false;
  }
}

function localPageReferences(html) {
  return [...new Set(references(html, /(?:href|src)="((?:css|js|assets|diagrams)\/[^"]+)"/g))];
}

async function assertPageReferencesExist(html) {
  for (const reference of localPageReferences(html)) {
    if (!(await exists(path.join(PAGE_DIR, reference)))) {
      throw new Error(`Referenced page asset is missing: ${reference}`);
    }
  }
}

async function assertCssReferencesExist() {
  const directory = path.join(PAGE_DIR, 'css');
  for (const file of (await readdir(directory)).filter((entry) => entry.endsWith('.css'))) {
    const css = await readFile(path.join(directory, file), 'utf8');
    for (const url of references(css, /url\(['"]?([^'")]+)['"]?\)/g)) {
      if (/^(?:data|https?):/.test(url)) continue;
      const target = path.posix.normalize(path.posix.join('ninthpass/css', url));
      if (!(await exists(path.join(REPO, target)))) {
        throw new Error(`Referenced stylesheet asset is missing: ${url} (from css/${file})`);
      }
    }
  }
}

const ROOT_RELATIVE_REWRITES = [
  ['"css/', '"/css/'],
  ['"js/', '"/js/'],
  ['"assets/', '"/assets/'],
  ['"diagrams/', '"/diagrams/'],
];

function rootRelative(html) {
  let staged = html;
  for (const [from, to] of ROOT_RELATIVE_REWRITES) staged = staged.replaceAll(from, to);
  return staged;
}

/** Every href/src must be root-relative, absolute, a fragment, or a data/mailto URL. */
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
  for (const file of PAGE_ROOT_FILES) {
    await cp(path.join(PAGE_DIR, file), path.join(DIST, file));
  }
  for (const directory of PAGE_DIRECTORIES) {
    await cp(path.join(PAGE_DIR, directory), path.join(DIST, directory), { recursive: true });
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
await assertPageReferencesExist(html);
await assertCssReferencesExist();
await stageDist(html);
const name = await writeBuildOutput();
console.log(`Staged ${await countFiles(DIST)} files into dist/ and wrote Build Output for Worker "${name}".`);
