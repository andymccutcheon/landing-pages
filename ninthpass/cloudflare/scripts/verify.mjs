#!/usr/bin/env node
// Post-deploy reachability check. Does not deploy and needs no credentials.
//
//   npm run verify -- https://ninthpass-site.<your-subdomain>.workers.dev

const REPO_URL = 'https://github.com/andymccutcheon/silverquill';

/** Paths that must answer 200, in the order a browser asks for them. */
const PATHS = [
  '/',
  '/css/fonts.css',
  '/css/pz-tokens.css',
  '/css/ninthpass.css',
  '/css/diagrams.css',
  '/js/page.js',
  '/js/diagrams.js',
  '/diagrams/dataflow.html',
  '/diagrams/arbor.html',
  '/robots.txt',
  '/sitemap.xml',
  '/assets/favicon.svg',
  '/assets/og.png',
  '/assets/fonts/fraunces-normal.woff2',
  '/assets/fonts/fraunces-italic.woff2',
  '/assets/fonts/geist.woff2',
  '/assets/fonts/geist-mono.woff2',
  '/assets/fonts/OFL-Fraunces.txt',
  '/assets/fonts/OFL-Geist.txt',
  '/assets/fonts/OFL-GeistMono.txt',
  // The published demonstration: the full-mode meeting-agent run the page links.
  ...['00-request.md', '01-compose.md', '02-judge-pass1.md', '03-revise.md', '04-judge-pass2.md', '05-final.md', 'PROVENANCE.md']
    .map(file => '/examples/runs/meeting-agent/' + file),
  // The retained optimize-only run: the recorded example of the Brief-side path.
  ...['00-original.md', '02-judge-pass1.md', '03-revise.md', '04-judge-pass2.md', '05-final.md', 'PROVENANCE.md']
    .map(file => '/examples/runs/rough-to-reviewed/' + file),
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
  const ctas = [...page.matchAll(/<a class="[^"]*\bprimary\b[^"]*"[^>]*? href="([^"]+)"/g)].map((match) => match[1]);
  if (ctas.length !== 2 || ctas.some((href) => href !== REPO_URL)) {
    failures.push(`expected two primary calls to action pointing at ${REPO_URL}, found ${JSON.stringify(ctas)}`);
  } else {
    console.log(`ok   both primary calls to action point at ${REPO_URL}`);
  }
  for (const [label, needle] of [
    ['fonts stylesheet', '"/css/fonts.css"'],
    ['stylesheet', '"/css/ninthpass.css"'],
    ['page script', '"/js/page.js"'],
    ['favicon', '"/assets/favicon.svg"'],
  ]) {
    if (!page.includes(needle)) failures.push(`served page does not reference the ${label} at ${needle}`);
  }
}

if (failures.length > 0) {
  console.error(`\nVerify failed:\n- ${failures.join('\n- ')}`);
  process.exit(1);
}
console.log(`\nVerify passed: ${PATHS.length} assets answered 200 and the page's calls to action are correct.`);
