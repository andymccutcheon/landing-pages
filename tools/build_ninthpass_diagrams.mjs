// Build three complete, responsive explanations from the captured meeting-notes run.
// The real artifacts are inputs, never generated or edited by this build.
import { readFileSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const output = resolve(root, 'ninthpass/diagrams');
const run = resolve(root, 'ninthpass/examples/runs/meeting-agent');
const cycle = readFileSync(resolve(root,'ninthpass/css/pz-tokens.css'),'utf8').match(/--pz-cycle:\s*([^;]+);/)[1].trim();
const files = ['02-judge-pass1.md', '04-judge-pass2.md'];
const scores = files.map(file => Number(readFileSync(resolve(run, file), 'utf8').match(/Overall Rating:\s*(\d+(?:\.\d+)?)/)[1]));
if (scores.join() !== '8.63,9.25') throw new Error('Captured trajectory changed: re-review the diagrams.');
const recs = ['Omit unsupported details', 'Label unstated facts', 'Five bullets, except refusals', 'Check form and source support', 'Only supplied material'];
const mobileRecs = [['Omit unsupported','details'], ['Label unstated','facts'], ['Five bullets,','except refusals'], ['Check form and','source support'], ['Only supplied','material']];
const esc = value => value.replaceAll('&', '&amp;').replaceAll('<', '&lt;');
const text = (x, y, content, cls = '', anchor = 'middle') => `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${esc(content)}</text>`;
const path = (d, cls = '') => `<path d="${d}" class="route ${cls}"/>`;
const fade = (start=.04,end=.74) => `<animate data-clock attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;${start-.01};${start+.02};${end};${Math.min(.98,end+.06)};1" dur="${cycle}" begin="indefinite" repeatCount="indefinite"/>`;
const dot = (d, start=.04, end=.74) => `<circle r="5" class="signal"><animateMotion data-clock path="${d}" dur="${cycle}" begin="indefinite" repeatCount="indefinite" keyPoints="0;0;1;1" keyTimes="0;${start};${end};1" calcMode="linear"/>${fade(start,end)}</circle>`;
const trail = (d,start=.04,end=.74) => `<path d="${d}" pathLength="1" stroke-dasharray=".08 .92" class="trail"><animate data-clock attributeName="stroke-dashoffset" values="1;1;0;0" keyTimes="0;${start};${end};1" dur="${cycle}" begin="indefinite" repeatCount="indefinite"/>${fade(start,end)}</path>`;
const ribbon = (d, feedback = false) => `<path d="${d}" class="ribbon ${feedback?'feedback-ribbon':''}"/>`;
const svg = (id, w, h, title, desc, content) => `<svg viewBox="0 0 ${w} ${h}" role="img" aria-labelledby="${id}-title ${id}-desc"><title id="${id}-title">${title}</title><desc id="${id}-desc">${desc}</desc>${content}</svg>`;
const wrap = (kind, title, desc, desktop, mobile) => `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="dark"><title>${title} — Ninth Pass</title><link rel="stylesheet" href="../css/fonts.css"><link rel="stylesheet" href="../css/pz-tokens.css"><link rel="stylesheet" href="../css/diagrams.css"><script src="../js/diagrams.js" defer></script></head><body data-kind="${kind}"><main class="scene"><div class="desktop">${desktop}</div><div class="mobile">${mobile}</div><p class="screen-reader-only">${desc}</p></main><button hidden data-standalone-motion aria-pressed="false" type="button">Pause motion</button></body></html>\n`;

function loop(mobile) {
  const points = mobile ? [[68,58],[265,146],[110,252],[265,352],[110,458],[265,558]] : [[75,250],[295,180],[490,300],[685,180],[875,300],[1115,150]];
  const d = points.map(([x,y],i) => i ? `C${points[i-1][0]+(mobile ? 80 : 100)},${points[i-1][1]} ${x-(mobile ? 80 : 100)},${y} ${x},${y}` : `M${x},${y}`).join(' ');
  let body = ribbon(d) + path(d) + trail(d);
  const labels = ['Compose', 'Judge', 'Revise', 'Judge', 'Revise', 'Judge'];
  points.forEach(([x,y],i) => {
    const scored = [1,3,5].includes(i);
    if (scored) {
      body += `<circle cx="${x}" cy="${y}" r="${mobile ? 43 : 68}" class="${i === 5 ? 'accent' : 'warm'}"/>`;
      body += text(x-2,y+(mobile?22:32),String(scores[(i-1)/2]), mobile?'score':'score giant-score');
      body += text(x,y+(mobile?66:89),i===5?'Judge · STOP':'Judge · CONTINUE','small');
    } else {
      body += `<circle cx="${x}" cy="${y}" r="${mobile?9:12}" class="endpoint"/>`;
      body += text(x, y-(mobile?23:32), labels[i], 'stage-label');
      body += text(x, y+(mobile?28:40),i===0?'Draft prompt':i===2?'First rewrite':'Second rewrite','small');
    }
  });
  body += dot(d);
  const desc = 'One captured Claude Code run. Compose drafts the prompt. Judge scores 8 and continues. Revise rewrites. Judge still scores 8 and continues. Revise rewrites again. Judge scores 9 and stops. These are prompt rubric scores, not measurements of task performance.';
  return svg(`loop-${mobile?'m':'d'}`,mobile?400:1200,mobile?650:440,'The first rewrite still scored 8',desc,body);
}

function arbor(mobile) {
  let body = '';
  const from = mobile ? [50,76] : [110,220];
  const to = mobile ? [220,530] : [1080,220];
  const rows = mobile ? [170,235,300,365,430] : [60,140,220,300,380];
  rows.forEach((y,i) => {
    const x = mobile ? 75 : 480;
    const end = mobile ? 340 : 820;
    const inbound = mobile ? `M${from[0]},${from[1]+12} C35,${y-30} 35,${y} ${x},${y}` : `M${from[0]+45},${from[1]} C260,220 280,${y} ${x-22},${y}`;
    const outbound = mobile ? `M${end},${y} C375,${y} 375,530 ${to[0]},530` : `M${end},${y} C930,${y} 935,220 ${to[0]-20},220`;
    body += ribbon(inbound,true) + ribbon(outbound,true) + path(inbound) + path(outbound);
    body += `<rect x="${x-12}" y="${y-24}" width="${mobile?286:366}" height="48" rx="4" class="feedback-row"/>`;
    body += mobile ? text(x,y-4,mobileRecs[i][0],'recommendation','start') + text(x,y+18,mobileRecs[i][1],'recommendation','start') : text(x,y+6,recs[i],'', 'start');
    const entry=.04+i*.025, arrived=.28+i*.025, gather=.47+i*.025, gathered=.74+i*.015;
    body += trail(inbound,entry,arrived) + trail(outbound,gather,gathered) + dot(inbound,entry,arrived) + dot(outbound,gather,gathered);
  });
  if (mobile) {
    body += text(56,80,'8.63','score score-dec score-ink') + text(102,48,'First scorecard','stage-label','start') + text(102,77,'Five recommendations','small','start');
    body += `<circle cx="${to[0]}" cy="${to[1]}" r="10" class="accent"/>`;
    body += text(200,568,'One rewrite','stage-label') + text(200,603,'Next Judge: 9.25/10','small');
  } else {
    body += text(102,212,'8','score score-ink') + text(110,265,'First scorecard','stage-label') + text(110,294,'CONTINUE','small');
    body += `<circle cx="${to[0]}" cy="${to[1]}" r="12" class="accent"/>`;
    body += text(1080,179,'One rewrite','stage-label') + text(1080,269,'Next Judge','small') + text(1080,302,'9.25 / STOP','stage-label');
  }
  const desc = 'Five recommendations from the first scorecard: omit unsupported details; label unstated facts; allow a safety refusal instead of five bullets; check form and source support; use only supplied material. They gather into one rewrite, not five parallel workers. The next Judge scored 9.25 and stopped.';
  return svg(`arbor-${mobile?'m':'d'}`,mobile?400:1200,mobile?650:440,'Five recommendations, one rewrite',desc,body);
}

function dataflow(mobile) {
  let body = '';
  if (!mobile) {
    const chambers = [[40,'Compose','Draft the prompt'],[435,'Judge','Review the current prompt'],[830,'Revise','Rewrite from feedback']];
    chambers.forEach(([x,name,action]) => {
      body += `<rect x="${x}" y="70" width="330" height="170" rx="4" class="chamber"/>`;
      body += text(x+24,113,name,'chamber-title','start') + text(x+24,145,name==='Judge'?'Prompt + original request':action,'small','start');
      if(name==='Judge') body += text(x+24,176,'Earlier scorecards','small','start');
      body += text(x+24,211,'Separate worker process','small','start');
      body += path(`M${x+165},240 L${x+165},353`);
    });
    const a='M205,178 C300,178 365,35 490,35 C585,35 600,60 600,70';
    const b='M600,178 C730,178 765,35 885,35 C980,35 995,60 995,70';
    body += ribbon(a) + ribbon(b) + path(a) + path(b) + trail(a,.04,.24) + trail(b,.34,.54) + dot(a,.04,.24) + dot(b,.34,.54);
    body += text(411,27,'Prompt','packet-label')+text(795,27,'Scorecard','packet-label');
    body += `<rect x="40" y="353" width="1120" height="60" rx="4" class="ground"/>`;
    body += text(66,390,'Run record on disk','stage-label','start') + text(1135,389,'Input, stage outputs, scorecards and retries','small','end');
    const back='M995,240 C995,320 600,320 600,240';
    body += ribbon(back,true) + path(back) + trail(back,.64,.84) + dot(back,.64,.84);
    body += text(800,335,'Rewritten prompt → fresh Judge','small');
  } else {
    const chambers=[[30,'Compose','Draft prompt'],[205,'Judge','Current prompt + history'],[380,'Revise','Rewritten prompt']];
    chambers.forEach(([y,name,action])=> {
      body += `<rect x="30" y="${y}" width="285" height="126" rx="4" class="chamber"/>`;
      body += text(50,y+37,name,'chamber-title','start')+text(50,y+70,action,'','start')+text(50,y+101,'Separate worker process','small','start');
      body += path(`M315,${y+63} L355,${y+63}`);
    });
    const a='M170,156 L170,205',b='M170,331 L170,380';
    body += path(a)+path(b)+dot(a,.04,.24)+dot(b,.34,.54);
    const back='M315,443 C342,443 342,268 315,268';
    body += path(back) + dot(back,.64,.84);
    body += path('M355,93 L355,560 L200,560');
    body += `<rect x="30" y="535" width="285" height="62" rx="4" class="ground"/>`;
    body += text(172,574,'Run record on disk','stage-label');
    body += text(200,628,'Artifacts persist between stages','small');
  }
  const desc='Compose, Judge and Revise run in separate worker processes. The prompt passes to Judge, the scorecard passes to Revise, and the rewritten prompt goes to a fresh Judge process. Judge receives the current prompt, original request and earlier scorecards, not the forwarded authoring conversation or APPLIED checklist. Run artifacts persist on disk. Separate processes may use the same model and provider.';
  return svg(`flow-${mobile?'m':'d'}`,mobile?400:1200,mobile?650:440,'Separate processes, explicit packets',desc,body);
}

for (const [name, build, title] of [['arbor',arbor,'Five recommendations, one rewrite'],['dataflow',dataflow,'Separate processes, explicit packets']]) {
  const desc='Recorded meeting-agent example, Codex worker, 21 October 2026. This explanation is not a live execution.';
  writeFileSync(resolve(output,`${name}.html`),wrap(name,title,desc,build(false),build(true)));
}
console.log('Built the feedback fan and process diagram from the recorded run (8.63 → 9.25).');
