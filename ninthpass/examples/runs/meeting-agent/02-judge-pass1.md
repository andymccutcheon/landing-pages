Section Ratings
- Primary Role: 9.3/10 — Clearly defines a “meeting-notes synthesizer” producing “five concise, decision-useful bullets.”
- High-Level Objectives: 9.0/10 — Covers outcomes, decisions, commitments, risks, next steps, and uncertainty.
- Domain Expertise & Resources: 8.5/10 — Identifies source materials, but “linked materials” lacks a clear accessibility boundary.
- Allowed Tools & APIs: 8.7/10 — Tool limits are clear, though “verify referenced facts” could be more explicitly bounded by supplied material.
- Operating Constraints: 7.4/10 — The instruction to “proceed with labelled assumptions” conflicts with the task-level prohibition on inventing facts.
- Interaction Style & Voice: 9.1/10 — “Plainly, neutrally, and efficiently” is specific and consistent with the audience.
- Memory & Context Handling: 9.2/10 — Explicitly prohibits invented background, participants, dates, decisions, and deadlines.
- Self-Monitoring & Reflection: 8.1/10 — Checks bullet count and uncertainty, but does not explicitly verify that every claim is source-supported.
- Example Exchanges (Few-Shot): 7.5/10 — The example invents a next step (“The team will confirm”) and its one-bullet refusal conflicts with the exact-five-bullets rule.
- Safety & Ethics: 9.1/10 — Provides a proportionate, audience-aware confidentiality rule.
- Deliverable Structure: 8.0/10 — The “exactly five standalone bullets” rule lacks an explicit exception for safety refusals shown in the example.
- Task Goal: 9.2/10 — Precisely restates the intended output and audience.
- Return Format: 8.5/10 — Specifies ordering and coverage well, but should align with safety-refusal handling.
- Warnings & Requirements: 9.1/10 — Strongly prohibits invention and requires clear labels for unresolved material.
- Context: 8.8/10 — Defines the audience and expected input, though source-material boundaries could be more explicit.

Overall Rating: 8.63/10 — A strong, practical prompt with clear scope, source discipline, and output constraints. Its main weaknesses are contradictory handling of missing information and safety refusals, plus one unsupported inference in the few-shot example.

Verdict: CONTINUE

Recommendations
1. In Operating Constraints, replace “For missing context, state a one-line default and proceed with labelled assumptions; ask only when the answer would materially undermine the summary.” → “For missing context, omit unsupported details; ask a concise clarifying question only when the missing information would materially undermine the summary.”
2. In the first example, replace “The team will confirm whether the tracking delay affects launch readiness.” → “Whether the possible tracking-event delay will affect the 12 May launch is not stated.”
3. In Deliverable Structure, replace “Provide exactly five standalone bullets.” → “Provide exactly five standalone bullets, except when refusing a request that would breach Safety & Ethics; in that case, provide a concise refusal instead.”
4. In Self-Monitoring & Reflection, replace “Before responding, verify that there are five bullets” → “Before responding, verify that the applicable output form is correct, every claim is supported by the supplied material, and there are five bullets unless issuing a safety refusal.”
5. In Domain Expertise & Resources, replace “Use supplied notes, transcripts, agendas, attendee lists, and linked materials as the source of truth.” → “Treat supplied meeting materials as the source of truth; use linked material only when it is explicitly supplied or accessible through an allowed tool.”
