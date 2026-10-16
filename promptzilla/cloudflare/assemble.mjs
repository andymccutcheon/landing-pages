import { cp, mkdir, rm } from 'node:fs/promises';
import { resolve } from 'node:path';

const root = resolve(import.meta.dirname, '../..');
const output = resolve(import.meta.dirname, 'dist');
await rm(output, { recursive: true, force: true });
await mkdir(resolve(output, 'promptzilla'), { recursive: true });
for (const file of ['index.html', 'styles.css', 'page.js', 'assets']) {
  await cp(resolve(root, 'promptzilla', file), resolve(output, 'promptzilla', file), { recursive: true });
}
for (const file of ['fonts.css', 'lp-tokens.css', 'base.css']) {
  await cp(resolve(root, 'shared', file), resolve(output, 'shared', file));
}
await cp(resolve(root, 'vendor/pattern/generated/tokens.css'), resolve(output, 'vendor/pattern/generated/tokens.css'));
for (const font of ['instrument-sans', 'jetbrains-mono']) {
  await cp(resolve(root, 'vendor/pattern/fonts', font), resolve(output, 'vendor/pattern/fonts', font), { recursive: true });
}
console.log(`Assembled static assets at ${output}`);
