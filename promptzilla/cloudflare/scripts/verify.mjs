#!/usr/bin/env node
// Post-deploy reachability check. Does not deploy and needs no credentials.
//
//   npm run verify -- https://promptzilla-site.<your-subdomain>.workers.dev

const REPO_URL = 'https://github.com/andymccutcheon/promptzilla';

/** Paths that must answer 200, in the order a browser asks for them. */
const PATHS = [
  '/',
  '/css/promptzilla.css',
  '/assets/favicon.svg',
  '/shared/base.css',
  '/shared/common.css',
  '/shared/fonts.css',
  '/shared/lp-tokens.css',
  '/shared/motion.css',
  '/shared/page.js',
  '/vendor/pattern/generated/tokens.css',
  '/vendor/pattern/fonts/instrument-sans/instrument-sans-latin.woff2',
  '/vendor/pattern/fonts/fraunces/fraunces-latin.woff2',
  '/vendor/pattern/fonts/jetbrains-mono/jetbrains-mono-latin.woff2',
];

const base = process.argv[2]?.replace(/\/$/, '');
if (!base) {
  console.error('Usage: npm run verify -- <base-url>');
  process.exit(2);
}

const failures = [];
let page = '';

for (const asset of PATHS) {
  const url = base + asset;
  try {
    const response = await fetch(url, { redirect: 'follow' });
    if (response.status !== 200) {
      failures.push(`${asset}: expected 200, got ${response.status}`);
      continue;
    }
    if (asset === '/') page = await response.text();
    console.log(`200  ${asset}`);
  } catch (error) {
    failures.push(`${asset}: request failed (${error.message})`);
  }
}

if (page) {
  const ctas = [...page.matchAll(/<a class="lp-button lp-press" href="([^"]+)"/g)].map((match) => match[1]);
  if (ctas.length !== 2 || ctas.some((href) => href !== REPO_URL)) {
    failures.push(`expected two primary calls to action pointing at ${REPO_URL}, found ${JSON.stringify(ctas)}`);
  } else {
    console.log(`ok   both primary calls to action point at ${REPO_URL}`);
  }
  for (const [label, needle] of [['stylesheet', '"/css/promptzilla.css"'], ['script', '"/shared/page.js"'], ['favicon', '"/assets/favicon.svg"']]) {
    if (!page.includes(needle)) failures.push(`served page does not reference the ${label} at ${needle}`);
  }
}

if (failures.length > 0) {
  console.error(`\nVerify failed:\n- ${failures.join('\n- ')}`);
  process.exit(1);
}
console.log(`\nVerify passed: ${PATHS.length} assets answered 200 and the page's calls to action are correct.`);
