#!/usr/bin/env node
// Build the Ninth Pass neural-arbor diagram.
//
//   node tools/build_ninthpass_arbor.mjs [--out ninthpass/diagrams/arbor.html]
//
// The data below is one real run of the engine, captured with the offline test
// worker. The structure is a rooted cascade with one honest fork: Judge writes
// a scorecard, and the scorecard's numbered recommendations are the branches
// Revise gathers and applies. The signal timing is illustrative and says so.
//
// The rendering is data-driven from PIPE, so a different run replaces the
// sample without touching the drawing code. The output is a static file: no
// build step, no dependency, and a complete frame with JavaScript switched
// off.

import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = resolve(fileURLToPath(new URL('..', import.meta.url)));
const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const i = args.indexOf(name);
  return i === -1 ? fallback : args[i + 1];
};
const OUT = resolve(REPO, flag('--out', 'ninthpass/diagrams/arbor.html'));

// ---------------------------------------------------------------- the run

const PIPE = {
  run: 'bc993584-d18e-4d03-94cd-762e8685d56f',
  request: 'Write a prompt for a meeting-notes summarizer',
  stages: [
    { id: 'request', index: '00', title: 'Request', role: 'Brief', file: '00-request.md', step: 1, x: 480, y: 74 },
    { id: 'compose', index: '01', title: 'Compose', role: 'Generate', file: '01-compose.md', step: 2, x: 454, y: 142, note: 'Two prompts' },
    { id: 'judge-1', index: '02', title: 'Judge', role: 'Score', file: '02-judge-pass1.md', step: 3, x: 478, y: 216, score: '8/10', verdict: 'CONTINUE' },
    { id: 'revise', index: '03', title: 'Revise', role: 'Rewrite', file: '03-revise.md', step: 5, x: 462, y: 392, note: 'All three applied' },
    { id: 'judge-2', index: '04', title: 'Judge', role: 'Re-score', file: '04-judge-pass2.md', step: 6, x: 482, y: 466, score: '9/10', verdict: 'STOP' },
    { id: 'final', index: '05', title: 'Approved', role: 'Prompt', file: '05-final.md', step: 6, x: 502, y: 528, path: 'prompts/meeting-notes.md', state: 'approved' },
  ],
  branches: [
    { id: 'rec-1', number: 1, text: 'Replace "notes" with "meeting notes"', x: 190, y: 306, step: 4 },
    { id: 'rec-2', number: 2, text: 'Preserve "[TBD]"', x: 470, y: 306, step: 4 },
    { id: 'rec-3', number: 3, text: 'Preserve the review gate', x: 754, y: 306, step: 4 },
  ],
  // The edges the signals travel. from -> to.
  edges: [
    { id: 'e-request-compose', from: 'request', to: 'compose', step: 2 },
    { id: 'e-compose-judge1', from: 'compose', to: 'judge-1', step: 3 },
    { id: 'e-judge1-rec1', from: 'judge-1', to: 'rec-1', step: 4 },
    { id: 'e-judge1-rec2', from: 'judge-1', to: 'rec-2', step: 4 },
    { id: 'e-judge1-rec3', from: 'judge-1', to: 'rec-3', step: 4 },
    { id: 'e-rec1-revise', from: 'rec-1', to: 'revise', step: 5 },
    { id: 'e-rec2-revise', from: 'rec-2', to: 'revise', step: 5 },
    { id: 'e-rec3-revise', from: 'rec-3', to: 'revise', step: 5 },
    { id: 'e-revise-judge2', from: 'revise', to: 'judge-2', step: 6 },
    { id: 'e-judge2-final', from: 'judge-2', to: 'final', step: 6 },
  ],
  steps: [
    { n: 1, label: 'the request is written to 00-request.md' },
    { n: 2, label: 'Compose runs in a fresh process and writes 01-compose.md' },
    { n: 3, label: 'Judge scores the two prompts: 8 out of 10, CONTINUE' },
    { n: 4, label: 'the scorecard carries three numbered recommendations' },
    { n: 5, label: 'Revise applies every recommendation and writes 03-revise.md' },
    { n: 6, label: 'the second Judge returns 9 out of 10, STOP, and the prompt is approved' },
  ],
};

// ---------------------------------------------------------------- geometry

const NODE = new Map();
for (const stage of PIPE.stages) NODE.set(stage.id, stage);
for (const branch of PIPE.branches) NODE.set(branch.id, branch);

// A cubic that leaves the source going down and arrives at the target from
// above, so the fork and the gathering read as one hourglass.
function edgePath(from, to) {
  const a = NODE.get(from);
  const b = NODE.get(to);
  const drop = Math.max(18, (b.y - a.y) * 0.45);
  return `M${a.x},${a.y} C${a.x},${a.y + drop} ${b.x},${b.y - drop} ${b.x},${b.y}`;
}

const W = 960;
const H = 600;
const esc = (text) =>
  String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

// ---------------------------------------------------------------- svg

const svg = [];
svg.push(`<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="pz-arbor-title pz-arbor-desc">`);
svg.push(`  <title id="pz-arbor-title">The anatomy of one pass of the Ninth Pass loop</title>`);
svg.push(`  <desc id="pz-arbor-desc">A top-down branching diagram of one real run. The request is composed, judged at 8 out of 10 with a continue verdict, and the judge writes three numbered recommendations that branch out and are gathered again by Revise. The second Judge scores 9 out of 10 and stops the loop, and the prompt is approved.</desc>`);
svg.push(`  <defs>`);
svg.push(`    <pattern id="pz-arbor-dots" width="22" height="22" patternUnits="userSpaceOnUse">`);
svg.push(`      <circle cx="11" cy="11" r="0.8" fill="#1a1513" opacity="0.08"/>`);
svg.push(`    </pattern>`);
svg.push(`    <marker id="pz-arbor-arrow" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#6e625b"/></marker>`);
svg.push(`    <marker id="pz-arbor-arrow-accent" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#a84b4b"/></marker>`);
svg.push(`    <marker id="pz-arbor-arrow-soft" markerWidth="8" markerHeight="6" refX="7" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="#b6a793"/></marker>`);
svg.push(`  </defs>`);
svg.push(`  <rect width="${W}" height="${H}" fill="#f3efe6"/>`);
svg.push(`  <rect width="${W}" height="${H}" fill="url(#pz-arbor-dots)" opacity="0.55"/>`);

// The loop back: a real semantic, drawn softly and labelled.
svg.push(`  <g data-motion-item data-step="6" aria-label="Below 9, the loop returns to Revise">`);
svg.push(`    <path d="M570,466 C690,466 690,392 550,392" fill="none" stroke="#6e625b" stroke-width="1.1" stroke-dasharray="5,4" marker-end="url(#pz-arbor-arrow-soft)"/>`);
svg.push(`    <rect x="586" y="418" width="152" height="16" fill="#f3efe6"/>`);
svg.push(`    <text x="662" y="430" text-anchor="middle" fill="#6e625b" font-family="'Geist Mono', monospace" font-size="9" letter-spacing="0.08em">BELOW 9 · REWRITE AGAIN</text>`);
svg.push(`  </g>`);

// The edges.
svg.push(`  <g id="pz-arbor-edges">`);
for (const edge of PIPE.edges) {
  const d = edgePath(edge.from, edge.to);
  const branch = edge.from === 'judge-1' || edge.to === 'revise';
  const stroke = branch ? '#a84b4b' : '#6e625b';
  const width = branch ? '1.1' : '1';
  const marker = branch ? 'pz-arbor-arrow-accent' : 'pz-arbor-arrow';
  const dash = edge.from === 'judge-1' ? '' : '';
  svg.push(`    <path data-edge="${edge.id}" data-from="${edge.from}" data-to="${edge.to}" data-step="${edge.step}" d="${d}" fill="none" stroke="${stroke}" stroke-width="${width}"${dash} marker-end="url(#${marker})" opacity="0.55"/>`);
}
svg.push(`  </g>`);

// The pulse layer: drawn by the script, empty in the static frame.
svg.push(`  <g id="pz-arbor-pulse" data-motion-decorative></g>`);

// The stage nodes.
svg.push(`  <g id="pz-arbor-nodes">`);
for (const stage of PIPE.stages) {
  const isJudge = stage.role === 'Score' || stage.role === 'Re-score';
  const stop = stage.verdict === 'STOP';
  const width = stage.id === 'request' ? 268 : 176;
  const height = 50;
  const x = stage.x - width / 2;
  const y = stage.y - height / 2;
  svg.push(`    <g data-node="${stage.id}" data-step="${stage.step}" data-kind="stage" tabindex="-1" aria-label="${esc(stage.title)}, ${esc(stage.role)}, file ${esc(stage.file)}">`);
  svg.push(`      <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="4" fill="#fbf8f2" stroke="${stop ? '#2e6a4b' : isJudge ? '#a84b4b' : '#1a1513'}" stroke-width="${stop || isJudge ? '1.2' : '1'}" opacity="0.95"/>`);
  svg.push(`      <text x="${stage.x}" y="${y + 22}" text-anchor="middle" fill="#1a1513" font-family="'Geist', sans-serif" font-size="12" font-weight="600">${esc(stage.title)}</text>`);
  const sub = stage.role + (stage.note ? ' · ' + stage.note : '');
  svg.push(`      <text x="${stage.x}" y="${y + 38}" text-anchor="middle" fill="#6e625b" font-family="'Geist Mono', monospace" font-size="9" letter-spacing="0.06em">${esc(sub.toUpperCase())}</text>`);
  if (stage.score) {
    svg.push(`      <text x="${x + width - 10}" y="${y + 22}" text-anchor="end" fill="${stop ? '#2e6a4b' : '#a84b4b'}" font-family="'Geist Mono', monospace" font-size="12">${esc(stage.score)}</text>`);
    svg.push(`      <text x="${x + width - 10}" y="${y + 38}" text-anchor="end" fill="${stop ? '#2e6a4b' : '#a84b4b'}" font-family="'Geist Mono', monospace" font-size="8" letter-spacing="0.08em">${esc(stage.verdict)}</text>`);
  }
  // The file the stage writes, set under the box on a paper mask.
  const file = stage.path ? stage.path : stage.file;
  const fileWidth = file.length * 5.4 + 8;
  svg.push(`      <rect x="${stage.x - fileWidth / 2}" y="${y + height + 2}" width="${fileWidth}" height="12" fill="#f3efe6"/>`);
  svg.push(`      <text x="${stage.x}" y="${y + height + 11}" text-anchor="middle" fill="#6e625b" font-family="'Geist Mono', monospace" font-size="9">${esc(file)}</text>`);
  svg.push(`    </g>`);
}

// The branch tips: the three recommendations.
for (const branch of PIPE.branches) {
  const width = 222;
  const height = 38;
  const x = branch.x - width / 2;
  const y = branch.y - height / 2;
  svg.push(`    <g data-node="${branch.id}" data-step="${branch.step}" data-kind="branch" tabindex="-1" aria-label="Recommendation ${branch.number}: ${esc(branch.text)}">`);
  svg.push(`      <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="3" fill="#f3efe6" stroke="#d8cdbe" stroke-width="1"/>`);
  svg.push(`      <text x="${x + 12}" y="${y + 17}" fill="#a84b4b" font-family="'Geist Mono', monospace" font-size="9" letter-spacing="0.08em">${branch.number}</text>`);
  svg.push(`      <text x="${x + 26}" y="${y + 17}" fill="#1a1513" font-family="'Geist', sans-serif" font-size="11">${esc(branch.text)}</text>`);
  svg.push(`      <text x="${x + 26}" y="${y + 30}" fill="#6e625b" font-family="'Geist Mono', monospace" font-size="8" letter-spacing="0.08em">RECOMMENDATION</text>`);
  svg.push(`    </g>`);
}
svg.push(`  </g>`);

// The run's own identifiers, so the graphic carries its provenance.
svg.push(`  <g data-motion-item data-step="1" aria-label="The run identifier">`);
svg.push(`    <text x="30" y="${H - 8}" fill="#6e625b" font-family="'Geist Mono', monospace" font-size="9" letter-spacing="0.08em">RUN ${esc(PIPE.run)}</text>`);
svg.push(`    <text x="${W - 30}" y="${H - 20}" text-anchor="end" fill="#6e625b" font-family="'Geist Mono', monospace" font-size="9" letter-spacing="0.08em">TIMING ILLUSTRATIVE</text>`);
svg.push(`  </g>`);
svg.push(`</svg>`);

// ---------------------------------------------------------------- page

const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>The Ninth Pass loop, as a branching tree</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; }
    @font-face {
      font-family: "Fraunces";
      src: url("../assets/fonts/fraunces-normal.woff2") format("woff2");
      font-style: normal;
      font-weight: 300 700;
      font-display: swap;
    }
    @font-face {
      font-family: "Fraunces";
      src: url("../assets/fonts/fraunces-italic.woff2") format("woff2");
      font-style: italic;
      font-weight: 300 700;
      font-display: swap;
    }
    @font-face {
      font-family: "Geist";
      src: url("../assets/fonts/geist.woff2") format("woff2");
      font-style: normal;
      font-weight: 300 700;
      font-display: swap;
    }
    @font-face {
      font-family: "Geist Mono";
      src: url("../assets/fonts/geist-mono.woff2") format("woff2");
      font-style: normal;
      font-weight: 400 600;
      font-display: swap;
    }
    :root {
      --color-paper: #f3efe6;
      --color-paper-2: #fbf8f2;
      --color-ink: #1a1513;
      --color-muted: #4e4641;
      --color-soft: #6e625b;
      --color-accent: #a84b4b;
      --color-accent-tint: rgba(168,75,75,0.08);
      --color-rule: #d8cdbe;
      --color-success: #2e6a4b;
      --font-sans: 'Geist', system-ui, sans-serif;
      --font-serif: 'Fraunces', Georgia, serif;
      --font-mono: 'Geist Mono', ui-monospace, monospace;
      --motion-fast: 160ms;
      --motion-step: 480ms;
      --motion-hold: 720ms;
      --motion-total: 3600ms;
      --motion-ease: cubic-bezier(.2,.8,.2,1);
    }
    body {
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: var(--color-paper);
      color: var(--color-ink);
      font-family: var(--font-sans);
    }
    main { width: min(96vw, 1180px); padding: 2.5rem 1rem; }
    .eyebrow {
      font: 500 0.68rem/1 var(--font-mono);
      letter-spacing: 0.18em;
      text-transform: uppercase;
      color: var(--color-soft);
      margin: 0 0 0.5rem;
    }
    h1 {
      font: 400 clamp(1.4rem, 2.2vw, 2rem)/1.1 var(--font-serif);
      letter-spacing: -0.01em;
      margin: 0 0 1.5rem;
    }
    .diagram-container { overflow-x: auto; }
    svg { width: 100%; min-width: 960px; display: block; }
    .motion-ready [data-motion-item] {
      opacity: .12;
      transform: translateY(8px);
      transform-box: fill-box;
      transform-origin: center;
      transition: opacity var(--motion-step) var(--motion-ease),
                  transform var(--motion-step) var(--motion-ease);
    }
    .motion-ready [data-motion-item].is-visible,
    .motion-ready[data-frame="end"] [data-motion-item],
    .motion-ready[data-frame="static"] [data-motion-item] {
      opacity: 1;
      transform: none;
    }
    #pz-arbor-nodes g { cursor: pointer; }
    #pz-arbor-nodes g:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 3px; }
    #pz-arbor-nodes g.is-dim { opacity: 0.32; }
    #pz-arbor-nodes g.is-lit rect { stroke-width: 1.6; }
    #pz-arbor-edges path { transition: opacity var(--motion-step) var(--motion-ease), stroke var(--motion-step) var(--motion-ease); }
    #pz-arbor-edges path.is-dim { opacity: 0.14; }
    #pz-arbor-edges path.is-lit { opacity: 1; stroke: var(--color-accent); }
    .pulse { fill: var(--color-accent); }
    .pulse-trail { fill: none; stroke: var(--color-accent); stroke-linecap: round; }
    html[data-motion="static"] [data-motion-controls],
    html[data-motion="static"] [data-motion-decorative] { display: none !important; }
    html[data-motion="static"] [data-motion-item] {
      opacity: 1 !important;
      transform: none !important;
      animation: none !important;
      transition: none !important;
    }
    html[data-motion="step"] [data-motion-controls],
    html[data-motion="step"] [data-motion-decorative] { display: none !important; }
    html[data-motion="step"] [data-motion-item] {
      animation: none !important;
      transition: none !important;
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: .001ms !important;
        animation-iteration-count: 1 !important;
        scroll-behavior: auto !important;
        transition-duration: .001ms !important;
      }
      [data-motion-item] { opacity: 1 !important; transform: none !important; }
      [data-motion-decorative] { display: none !important; }
      [data-motion-controls] { display: none !important; }
    }
    @media print {
      .diagram-container { overflow-x: visible; }
      svg { min-width: 0; }
      [data-motion-controls], [data-motion-decorative] { display: none !important; }
      [data-motion-item] { opacity: 1 !important; transform: none !important; }
    }
    .legend {
      display: flex; flex-wrap: wrap; gap: 1.25rem; margin: 0 0 0.25rem;
      font: 400 0.7rem/1 var(--font-mono); letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--color-soft);
    }
    .legend span { display: inline-flex; align-items: center; gap: 0.5rem; }
    .legend__line { width: 1.75rem; height: 0; border-top: 1px solid var(--color-soft); }
    .legend__line--branch { border-top-color: var(--color-accent); }
    .legend__line--loop { border-top-style: dashed; }
    [data-motion-controls] {
      display: none;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
      margin-block-start: 1.25rem;
    }
    [data-motion-controls] button {
      font: 500 0.72rem/1 var(--font-mono);
      letter-spacing: 0.1em;
      text-transform: uppercase;
      color: var(--color-muted);
      background: var(--color-paper-2);
      border: 1px solid var(--color-rule);
      border-radius: 3px;
      padding: 0.55rem 0.8rem;
      cursor: pointer;
      min-block-size: 2.4rem;
    }
    .motion-ready [data-motion-controls] { display: flex; }
    [data-motion-controls] button:hover { color: var(--color-ink); border-color: var(--color-soft); }
    [data-motion-controls] button:focus-visible { outline: 2px solid var(--color-accent); outline-offset: 2px; }
    [data-motion-controls] button:disabled { opacity: 0.4; cursor: default; }
    .keyboard-help { font: 400 0.7rem/1 var(--font-mono); color: var(--color-soft); }
    [data-motion-status-visible] { font: 400 0.7rem/1 var(--font-mono); color: var(--color-soft); }
    .sr-only {
      position: absolute; width: 1px; height: 1px; margin: -1px; padding: 0;
      overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0;
    }
    noscript p { margin: 0.75rem 0 0; color: var(--color-muted); font: 500 0.72rem/1.4 var(--font-mono); }
  </style>
</head>
<body>
  <main data-motion-root data-motion-mode="reveal" data-step-count="${PIPE.steps.length}" data-step-current="${PIPE.steps.length}" data-frame="static" data-static-frame="complete">
    <p class="eyebrow">Anatomy of one pass</p>
    <h1>Judge branches. Revise gathers.</h1>

    <div class="diagram-container">
${svg.join('\n')}
    </div>

    <p class="legend">
      <span><span class="legend__line legend__line--spine"></span>the stages</span>
      <span><span class="legend__line legend__line--branch"></span>the scorecard's recommendations</span>
      <span><span class="legend__line legend__line--loop"></span>the loop returns</span>
    </p>

    <div data-motion-controls role="group" aria-label="Diagram playback controls">
      <button type="button" data-motion-action="prev">Previous</button>
      <button type="button" data-motion-action="play" aria-pressed="false">Play</button>
      <button type="button" data-motion-action="pause" aria-pressed="true">Pause</button>
      <button type="button" data-motion-action="next">Next</button>
      <button type="button" data-motion-action="replay">Replay</button>
      <span class="keyboard-help">←/→ step, Space play/pause, R replay</span>
      <span data-motion-status-visible aria-hidden="true">Step <span data-motion-step-label>${PIPE.steps.length}</span> of ${PIPE.steps.length}</span>
    </div>
    <p class="sr-only" data-motion-status role="status" aria-live="polite" aria-atomic="true"></p>
    <noscript><p>Animation controls require JavaScript. The complete final diagram is shown above.</p></noscript>
  </main>

  <script data-diagram-controls>
    (() => {
      const params = new URLSearchParams(location.search);
      const reduce = matchMedia('(prefers-reduced-motion: reduce)');
      document.fonts.ready.then(() => { document.documentElement.dataset.fontsReady = 'true'; });

      const EDGES = ${JSON.stringify(PIPE.edges)};
      const STEPS = ${JSON.stringify(PIPE.steps)};

      document.querySelectorAll('[data-motion-root]').forEach((root) => {
        const count = Number(root.dataset.stepCount);
        const items = [...root.querySelectorAll('[data-motion-item]')];
        const nodes = [...root.querySelectorAll('#pz-arbor-nodes g[data-node]')];
        const edges = [...root.querySelectorAll('#pz-arbor-edges path[data-edge]')];
        const pulseLayer = root.querySelector('#pz-arbor-pulse');
        const controls = root.querySelector('[data-motion-controls]');
        const status = root.querySelector('[data-motion-status]');
        const visibleStep = root.querySelector('[data-motion-step-label]');
        const requestedStep = params.get('step');
        const exactStep = params.get('motion') === 'step' && /^\d+$/.test(requestedStep || '') ? Number(requestedStep) : null;
        const buttons = (action) => controls.querySelector('[data-motion-action="' + action + '"]');
        let step = count;
        let timer = 0;
        let playing = false;

        // Arc-length tables, so a pulse holds its speed around a curve.
        const geometry = new Map();
        for (const path of edges) {
          const total = path.getTotalLength();
          const samples = [];
          let length = 0;
          let previous = path.getPointAtLength(0);
          samples.push({ at: 0, x: previous.x, y: previous.y });
          for (let i = 1; i <= 24; i++) {
            const at = (total * i) / 24;
            const point = path.getPointAtLength(at);
            length += Math.hypot(point.x - previous.x, point.y - previous.y);
            samples.push({ at: length, x: point.x, y: point.y });
            previous = point;
          }
          geometry.set(path.getAttribute('data-edge'), { path, total, length, samples });
        }

        function pointAt(edge, distance) {
          const samples = edge.samples;
          if (distance <= 0) return samples[0];
          if (distance >= edge.length) return samples[samples.length - 1];
          let lo = 0;
          let hi = samples.length - 1;
          while (hi - lo > 1) {
            const mid = (lo + hi) >> 1;
            if (samples[mid].at <= distance) lo = mid; else hi = mid;
          }
          const a = samples[lo];
          const b = samples[hi];
          const span = b.at - a.at || 1;
          const t = (distance - a.at) / span;
          return { x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t };
        }

        // The signals for one step: the edges that step lights, in order.
        function signalsFor(stepNumber) {
          return EDGES.filter((edge) => edge.step === stepNumber).map((edge) => ({
            id: edge.id,
            geometry: geometry.get(edge.id),
            delay: 0,
          }));
        }

        let raf = 0;
        function runPulses(stepNumber) {
          cancelAnimationFrame(raf);
          pulseLayer.replaceChildren();
          if (reduce.matches || document.documentElement.dataset.motion === 'static') return;
          const signals = signalsFor(stepNumber).filter((signal) => signal.geometry);
          if (!signals.length) return;
          const speed = 320; // design units per second
          const started = performance.now();
          const trail = 26;
          function frame(now) {
            const elapsed = (now - started) / 1000;
            pulseLayer.replaceChildren();
            let alive = false;
            for (const signal of signals) {
              const distance = elapsed * speed;
              if (distance > signal.geometry.length + 0.35) continue;
              alive = true;
              const head = pointAt(signal.geometry, Math.min(distance, signal.geometry.length));
              const back = pointAt(signal.geometry, Math.max(0, distance - trail));
              const trailPath = document.createElementNS('http://www.w3.org/2000/svg', 'path');
              trailPath.setAttribute('class', 'pulse-trail');
              trailPath.setAttribute('d', 'M' + back.x.toFixed(1) + ',' + back.y.toFixed(1) + ' L' + head.x.toFixed(1) + ',' + head.y.toFixed(1));
              trailPath.setAttribute('stroke-width', '2');
              trailPath.setAttribute('opacity', '0.55');
              const dot = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
              dot.setAttribute('class', 'pulse');
              dot.setAttribute('cx', head.x.toFixed(1));
              dot.setAttribute('cy', head.y.toFixed(1));
              dot.setAttribute('r', '3.4');
              pulseLayer.appendChild(trailPath);
              pulseLayer.appendChild(dot);
            }
            if (alive) raf = requestAnimationFrame(frame);
          }
          raf = requestAnimationFrame(frame);
        }

        function announce() {
          const entry = STEPS.find((s) => s.n === step);
          status.textContent = 'Step ' + step + ' of ' + count + ': ' + (entry ? entry.label : 'Complete');
        }

        function render(next, userInitiated = false) {
          step = Math.max(0, Math.min(count, next));
          root.dataset.stepCurrent = String(step);
          root.dataset.frame = step === count ? 'end' : step === 0 ? 'start' : 'step';
          items.forEach((item) => {
            const itemStep = Number(item.dataset.step);
            item.classList.toggle('is-visible', itemStep <= step);
          });
          nodes.forEach((node) => {
            const nodeStep = Number(node.dataset.step);
            node.classList.toggle('is-visible', nodeStep <= step);
            node.setAttribute('opacity', nodeStep <= step ? '1' : '0.12');
          });
          edges.forEach((path) => {
            const edgeStep = Number(path.dataset.step);
            path.setAttribute('opacity', edgeStep <= step ? (path.getAttribute('stroke') === '#a84b4b' ? '0.85' : '0.55') : '0.1');
          });
          if (visibleStep) visibleStep.textContent = String(step);
          buttons('prev').disabled = step === 0;
          buttons('next').disabled = step === count;
          if (userInitiated) announce();
          runPulses(step);
        }

        function pause(userInitiated = false) {
          clearTimeout(timer);
          playing = false;
          root.classList.remove('is-playing');
          buttons('play').setAttribute('aria-pressed', 'false');
          buttons('pause').setAttribute('aria-pressed', 'true');
          if (userInitiated) status.textContent = 'Paused at step ' + step + ' of ' + count;
        }

        function tick() {
          if (!playing) return;
          if (step >= count) { pause(false); status.textContent = 'Complete · step ' + count + ' of ' + count; return; }
          render(step + 1, false);
          if (step >= count) { pause(false); return; }
          timer = window.setTimeout(tick, 760);
        }

        function play(fromStart = false, userInitiated = false) {
          clearTimeout(timer);
          if (fromStart || step >= count) render(0, userInitiated);
          playing = true;
          root.classList.add('is-playing');
          buttons('play').setAttribute('aria-pressed', 'true');
          buttons('pause').setAttribute('aria-pressed', 'false');
          timer = window.setTimeout(tick, 760);
        }

        controls.addEventListener('click', (event) => {
          const button = event.target.closest('[data-motion-action]');
          if (!button) return;
          const action = button.dataset.motionAction;
          if (action === 'play') play(false, true);
          if (action === 'pause') pause(true);
          if (action === 'replay') play(true, true);
          if (action === 'prev') { pause(false); render(step - 1, true); }
          if (action === 'next') { pause(false); render(step + 1, true); }
        });

        window.addEventListener('keydown', (event) => {
          if (event.target.matches('input, textarea, select')) return;
          if (event.key === 'ArrowRight') { pause(false); render(step + 1, true); }
          if (event.key === 'ArrowLeft') { pause(false); render(step - 1, true); }
          if (event.key === ' ') { event.preventDefault(); playing ? pause(true) : play(false, true); }
          if (event.key === 'r' || event.key === 'R') play(true, true);
          if (event.key === 'Home') { pause(false); render(0, true); }
          if (event.key === 'End') { pause(false); render(count, true); }
        });

        // Hover and selection light a lineage: the path down to the node and
        // everything that node feeds.
        const parents = new Map();
        for (const edge of EDGES) {
          if (!parents.has(edge.to)) parents.set(edge.to, []);
          parents.get(edge.to).push(edge.from);
        }
        function lineageOf(id) {
          const chain = new Set();
          const walk = (nodeId) => {
            if (chain.has(nodeId)) return;
            chain.add(nodeId);
            for (const parent of parents.get(nodeId) || []) walk(parent);
          };
          walk(id);
          return chain;
        }
        function descendantsOf(id) {
          const out = new Set();
          const walk = (nodeId) => {
            for (const edge of EDGES) {
              if (edge.from !== nodeId || out.has(edge.to)) continue;
              out.add(edge.to);
              walk(edge.to);
            }
          };
          walk(id);
          return out;
        }
        let pinned = null;
        function light(id) {
          const active = id || pinned;
          if (!active) {
            nodes.forEach((node) => node.classList.remove('is-dim', 'is-lit'));
            edges.forEach((path) => path.classList.remove('is-dim', 'is-lit'));
            return;
          }
          const up = lineageOf(active);
          const down = descendantsOf(active);
          nodes.forEach((node) => {
            const nodeId = node.getAttribute('data-node');
            const on = up.has(nodeId) || down.has(nodeId);
            node.classList.toggle('is-lit', on);
            node.classList.toggle('is-dim', !on);
          });
          edges.forEach((path) => {
            const from = path.getAttribute('data-from');
            const to = path.getAttribute('data-to');
            const on = (up.has(from) && up.has(to)) || (up.has(from) && down.has(to)) || (up.has(to) && down.has(to));
            path.classList.toggle('is-lit', on);
            path.classList.toggle('is-dim', !on);
          });
        }
        for (const node of nodes) {
          node.addEventListener('pointerenter', () => { if (!pinned) light(node.getAttribute('data-node')); });
          node.addEventListener('pointerleave', () => { if (!pinned) light(null); });
          node.addEventListener('click', (event) => {
            event.stopPropagation();
            const id = node.getAttribute('data-node');
            pinned = pinned === id ? null : id;
            light(pinned);
          });
        }
        root.querySelector('svg').addEventListener('click', () => { pinned = null; light(null); });

        const staticOverride = params.get('motion') === 'static' || document.documentElement.dataset.motion === 'static';
        if (staticOverride) {
          document.documentElement.dataset.motion = 'static';
          root.dataset.frame = 'static';
          root.dataset.motionState = 'static';
          render(count, false);
          status.textContent = 'Static frame \u00b7 step ' + count + ' of ' + count;
        } else if (exactStep !== null) {
          document.documentElement.dataset.motion = 'step';
          pause(false);
          render(exactStep, false);
          root.dataset.frame = 'step';
          root.dataset.motionState = 'test';
          status.textContent = 'Test frame \u00b7 step ' + exactStep + ' of ' + count;
        } else {
          render(0, false);
          if (!reduce.matches) {
            play(true, false);
          }
        }
        root.classList.add('motion-ready');
      });
    })();
  </script>
</body>
</html>
`;

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(OUT, html);
console.log(`wrote ${OUT}`);
console.log(`${PIPE.stages.length} stages, ${PIPE.branches.length} branches, ${PIPE.edges.length} edges, ${PIPE.steps.length} steps`);
