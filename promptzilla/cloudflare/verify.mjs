const base = process.argv[2];
if (!base) {
  console.error('Usage: npm run verify -- <deployed-base-url>');
  process.exit(2);
}

const origin = new URL(base);
origin.pathname = origin.pathname.endsWith('/') ? origin.pathname : `${origin.pathname}/`;
origin.search = '';
origin.hash = '';
const checked = new Set();
const failures = [];

async function get(url) {
  const response = await fetch(url);
  checked.add(url);
  console.log(`${response.status} ${url}`);
  if (response.status !== 200) failures.push(`${url} returned ${response.status}; expected 200`);
  return response;
}

const rootUrl = new URL('/', origin);
const rootResponse = await get(rootUrl);
const html = await rootResponse.text();
const expectedCta = 'https://github.com/andymccutcheon/promptzilla';
const ctaRegions = [
  ['.hero-actions', html.match(/<div class="hero-actions">([\s\S]*?)<\/div>/i)?.[1] ?? ''],
  ['.end-cta', html.match(/<div class="end-cta">([\s\S]*?)<\/section>/i)?.[1] ?? ''],
];
for (const [name, region] of ctaRegions) {
  const hasCtaAnchor = [...region.matchAll(/<a\b[^>]*>/gi)].some(([tag]) => {
    const href = tag.match(/\bhref=["']([^"']+)["']/i)?.[1];
    return href === expectedCta;
  });
  if (!hasCtaAnchor) failures.push(`Root response is missing the Promptzilla CTA anchor in ${name}`);
}

const references = new Set();
for (const match of html.matchAll(/(?:href|src)=["']([^"']+)["']/gi)) {
  const raw = match[1];
  if (!raw || raw.startsWith('#') || raw.startsWith('data:') || raw.startsWith('https:') || raw.startsWith('http:') || raw.startsWith('mailto:')) continue;
  references.add(new URL(raw, rootUrl).href);
}

const visitedCss = new Set();
async function checkCss(url) {
  if (visitedCss.has(url)) return;
  visitedCss.add(url);
  const response = await get(url);
  const css = await response.text();
  for (const match of css.matchAll(/@import\s+(?:url\()?\s*["']?([^\s"')]+)["']?\s*\)?[^;]*;|url\(\s*["']?([^\s"')]+)["']?\s*\)/gi)) {
    const raw = match[1] || match[2];
    if (!raw || raw.startsWith('data:') || raw.startsWith('https:') || raw.startsWith('http:')) continue;
    references.add(new URL(raw, url).href);
  }
}

while (references.size) {
  const url = references.values().next().value;
  references.delete(url);
  if (checked.has(url)) continue;
  if (url.split('?')[0].endsWith('.css')) {
    await checkCss(url);
  } else {
    await get(url);
  }
}
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`Verified root page and ${checked.size - 1} referenced assets.`);
