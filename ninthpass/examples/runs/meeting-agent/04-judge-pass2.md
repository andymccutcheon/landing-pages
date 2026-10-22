Section Ratings

- Primary Role: 9.6/10 — Defines a “meeting-notes synthesizer” producing “five concise, decision-useful bullets.”
- High-Level Objectives: 9.5/10 — Explicitly covers “outcomes, decisions, commitments, risks, and next steps” while preserving uncertainty.
- Domain Expertise & Resources: 9.2/10 — Establishes supplied material as “the source of truth” and bounds linked-material use.
- Allowed Tools & APIs: 8.6/10 — Restricts tools and prohibits external actions, but “verify referenced facts” does not explicitly limit verification to supplied material.
- Operating Constraints: 8.7/10 — Strong rules on uncertainty and ownership, but the sparse-source fallback does not clearly handle completely absent meeting material.
- Interaction Style & Voice: 9.5/10 — “Plainly, neutrally, and efficiently” with outcome-first guidance is specific and usable.
- Memory & Context Handling: 9.5/10 — Explicitly prohibits invented “background, participants, dates, decisions, or deadlines.”
- Self-Monitoring & Reflection: 9.5/10 — Requires source support, useful bullets, correct form, ownership labeling, and uncertainty checks.
- Example Exchanges (Few-Shot): 8.7/10 — The examples correctly demonstrate supported summaries and a safety refusal, but do not demonstrate the sparse-material rule.
- Safety & Ethics: 9.5/10 — Provides proportionate confidentiality protection and an audience-sensitive disclosure rule.
- Deliverable Structure: 9.4/10 — Clearly specifies five standalone bullets, one-sentence preference, and a safety-refusal exception.
- Task Goal: 9.5/10 — Precisely states the intended summary, length, and audience.
- Return Format: 9.3/10 — Requires importance ordering and relevant coverage, though it relies on system-level handling when no material is supplied.
- Warnings & Requirements: 9.5/10 — Clearly prohibits invented facts and requires explicit labeling of unresolved material.
- Context: 8.8/10 — Identifies the expected material and audience, but states material “will be supplied” without an explicit absent-input path.

Overall Rating: 9.25/10 — A decision-ready prompt with strong source discipline, safety boundaries, output control, and self-checking. Minor ambiguity remains around absent inputs and the scope of fact verification.

Verdict: STOP

Recommendations

1. In Allowed Tools & APIs: “verify referenced facts” → “verify referenced facts only against supplied meeting material or explicitly supplied context.”
2. In Operating Constraints: “Return exactly five short bullets unless the source contains too little information; then state the limitation in one bullet and use the remaining bullets for supported takeaways.” → “When meeting material is supplied, return exactly five short bullets. If no meeting material is supplied, ask one concise clarifying question; if material is sparse, state the limitation in one bullet and use the remaining bullets only for supported takeaways.”
3. Add a sparse-material few-shot example that demonstrates a stated limitation and avoids padding the five bullets with unsupported content.
