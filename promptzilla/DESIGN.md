# Promptzilla — Dark-tech kaiju direction

## Positioning
For AI builders who want a capable prompt without writing every one by hand or learning agent engineering, Promptzilla is an MCP server that packages five prompt-engineering skills as tools, prompts and resources. The connected AI client executes the skills; Promptzilla itself does not secretly call a model. This distinction is central to trust and should appear before install instructions.

## Content plan
1. **Hero:** identify the audience and outcome, explain that Promptzilla prepares and evaluates prompts, then link to the repository and expose a copyable Claude Code install command.
2. **Pipeline story:** Metapod generates; Judge Dredd evaluates against a rubric with evidence and a STOP/CONTINUE verdict; Brian Spillner applies recommendations. The durable controller repeats the loop until STOP at ≥9, up to four scoring rounds.
3. **Choose a starting point:** full mode from a rough request, or optimize-only mode with an existing prompt preserved byte-for-byte.
4. **Trust boundary:** the connected AI client executes skills; no API key or model-provider account required. Fresh-context workers are a host obligation.
5. **Get started:** Claude Code command and generic MCP JSON config, then repeated repository CTA.

## Direction and rationale
“Dark-tech kaiju” uses a near-black technical canvas, restrained acid-lime signal color, local typography, thin measurement rules and a custom SVG creature/wordmark. The monster is a scale metaphor, not a product mascot or capability claim. A scorecard and loop diagram carry the product narrative. The install command is treated as a working terminal artifact.

## Design read and dials
Reading this as: developer-tool conversion landing page for AI builders, in a dark technical / kaiju scale language with local CSS and the repository Pattern tokens. Design variance 7, motion intensity 2, visual density 4. Low motion prioritizes accessibility and performance. No parallax, scroll pinning, external libraries, trackers, invented output, testimonials, metrics, or live endpoint.

## Claim boundary
Product statements are limited to the shared brief and `/Users/andymccutcheon/Desktop/promptzilla-mcp/README.md`. Do not describe the tool as executing agents, guaranteeing quality, or supplying isolated workers. No API key or provider account is required.

## Repo and platform decisions
Reuse vendor Pattern tokens, shared font declarations and shared base accessibility styles. Do not use shared/common.css or shared/page.js: those are coupled to existing light/dark theme controls and assume page-specific controls that this fixed dark page does not expose. Clipboard behavior is a minimal local script with selection fallback. CSS-only transitions honor `prefers-reduced-motion`. Cloudflare `cf` build config is config-driven and points at the generated dist/ asset tree; the assembly script copies only referenced local assets. No Wrangler files or commands.
