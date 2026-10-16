import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const output = resolve(import.meta.dirname, 'dist');
await rm(output, { recursive: true, force: true });
await mkdir(output, { recursive: true });

const page = await readFile(resolve(root, 'promptzilla/index.html'), 'utf8');
await writeFile(resolve(output, 'index.html'), page.replaceAll('../shared/', 'shared/').replaceAll('../vendor/', 'vendor/'));
for (const file of ['styles.css', 'page.js', 'assets']) {
  await cp(resolve(root, 'promptzilla', file), resolve(output, file), { recursive: true });
}
await mkdir(resolve(output, 'shared'), { recursive: true });
const fontCss = await readFile(resolve(root, 'shared/fonts.css'), 'utf8');
const usedFonts = [...fontCss.matchAll(/@font-face\s*\{[^}]+\}/g)]
  .map(([rule]) => rule)
  .filter((rule) => /font-family:\s*['\"]?(?:Instrument Sans|JetBrains Mono)(?: Fallback)?['\"]?;/.test(rule));
await writeFile(resolve(output, 'shared/fonts.css'), `${usedFonts.join('\n\n')}\n`);
for (const file of ['lp-tokens.css', 'base.css']) {
  await cp(resolve(root, 'shared', file), resolve(output, 'shared', file));
}
await cp(resolve(root, 'vendor/pattern/generated/tokens.css'), resolve(output, 'vendor/pattern/generated/tokens.css'));
for (const [font, file] of [
  ['instrument-sans', 'instrument-sans-latin.woff2'],
  ['jetbrains-mono', 'jetbrains-mono-latin.woff2'],
]) {
  await mkdir(resolve(output, 'vendor/pattern/fonts', font), { recursive: true });
  await cp(resolve(root, 'vendor/pattern/fonts', font, file), resolve(output, 'vendor/pattern/fonts', font, file));
}
console.log(`Assembled root landing page and referenced static assets at ${output}`);
