Section Ratings
- Primary Role: 9/10 — "You are a professional meeting summarizer who distills lengthy discussions into actionable, executive-ready bullet points" is specific, enforceable, and clearly scoped
- High-Level Objectives: 8/10 — Four clear objectives present ("Extract the most critical information", "Identify decisions, action items"), though success criteria could be more explicit
- Domain Expertise & Resources: 7/10 — Lists relevant domains ("Corporate communication best practices", "Meeting facilitation") but remains outline-level without when-to-apply guidance
- Allowed Tools & APIs: 7/10 — States "Text processing and summarization. No external tools required" clearly but minimally
- Operating Constraints: 9/10 — Hard rule "Output must be exactly five bullet points" is specific and enforceable; includes edge case handling ("When input lacks five distinct points, state assumptions")
- Interaction Style & Voice: 8/10 — Multiple specific directives ("Use active voice and strong verbs", "Write for busy executives who scan") provide clear guidance
- Memory & Context Handling: 7/10 — Present ("Retain context about ongoing meetings") but outline-only; lacks specifics on how to handle multi-session contexts
- Self-Monitoring & Reflection: 8/10 — Three concrete checks listed ("Verify all five bullets represent distinct information"), could include verification of factual accuracy
- Example Exchanges (Few-Shot): 9/10 — Three examples covering standard case, edge case (empty meeting), and draft request scenario with realistic detail
- Safety & Ethics: 8/10 — Four clear directives including "Never fabricate information not present in source material" and confidentiality guidance
- Deliverable Structure: 9/10 — Exact format specified with bullet structure requirements ("Beginning with a strong action verb", "Containing one primary idea")
- Task Prompt: 8/10 — Clear GOAL and RETURN FORMAT sections, though redundant with system prompt Operating Constraints and Deliverable Structure

Overall Rating: 8/10 — Usable and mostly complete. The prompt provides clear role definition, enforceable constraints, strong few-shot examples, and safety guidance. Remaining gaps are non-blocking: some sections remain outline-level (Domain Expertise, Memory & Context), and redundancy exists between system and task prompt sections.

Verdict: CONTINUE

Recommendations
1. Eliminate redundancy between system and task prompts: "Task Prompt" section repeats "Output must be exactly five bullet points" (Operating Constraints) and bullet format requirements (Deliverable Structure). Merge or cross-reference to prevent drift.
2. Add when-to-apply guidance to Domain Expertise: "Corporate communication best practices" → "Corporate communication best practices: use active voice for decisions, passive for group discussions; prioritize outcomes over process; lead with impact"
3. Extend prioritization rules for >5 points: Current "Prioritize actionable items and decisions over general discussion" → "When >5 distinct points exist, select in order: (1) Decisions with clear outcomes, (2) Action items with named owners and dates, (3) Action items without owners, (4) Discussion points revealing blockers/risks, (5) General themes"
4. Specify multi-session context handling: "Retain context about ongoing meetings or project threads when provided" → "For multi-part meetings, maintain cumulative decisions and open action items; flag contradictions with earlier sessions; cross-reference recurring themes by date"
5. Strengthen Self-Monitoring verification: Add "verify all numerical data (dates, amounts, counts) matches source exactly; confirm no bullets contain overlapping information" to existing checks
