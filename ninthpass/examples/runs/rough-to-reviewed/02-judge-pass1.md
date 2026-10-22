Section Ratings
- Task Objective & Action: 8/10 — Clear, single, verifiable verb-object target: "Summarise meeting notes"; the action and its object are unambiguous, though no purpose or reader is stated (that gap is rated separately).
- Output Format & Count Constraint: 8/10 — "into five bullet points" fixes both the container (bullets) and an exact count, which is directly checkable on output; no rules for bullet form, ordering, or the sparse-input case.
- Style & Length Constraints: 5/10 — "Keep it short and useful" is the prompt's only quality gate, and both terms are undefined: no word, line, or sentence limit for "short", no criterion for "useful", so output quality cannot be evaluated consistently across runs.
- Input Specification & Edge-Case Handling: 4/10 — "meeting notes" is named as the input but never sourced or bounded: the prompt's two sentences contain no clause stating where the notes come from, what to do when no notes are supplied, or what to do when the notes support fewer than five distinct points.
- Faithfulness / No-Invention Guard: 3/10 — No clause constrains what the summary may assert; nothing prevents inventing decisions, owners, dates, or outcomes absent from the notes, a primary failure mode for a summarisation task over meeting notes.
- Fidelity to Source User Facts: 9/10 — The prompt string is byte-identical to the fidelity source ("Summarise meeting notes into five bullet points. Keep it short and useful."), so all three user facts — meeting notes, five bullets, short and useful — are preserved with nothing added that misstates the request.

Overall Rating: 5/10 — The task and the output count are clear and enforceable, but the two gates that determine whether the output is any good — "short and useful" (undefined) and faithfulness (absent) — are exactly the ones that would break the agent's job, so a correct-looking five-bullet answer can still be wrong on both counts.

Verdict: CONTINUE

Recommendations
1. Replace the undefined style sentence with measurable limits. Old: "Keep it short and useful." → New: "Keep it short and useful: one idea per bullet, about 20 words or fewer per bullet, no preamble and no closing summary." (The 20-word figure is a suggested default to tune for your audience, not a measured threshold.)
2. Add a faithfulness clause; none exists today. Insert after "Summarise meeting notes into five bullet points." → " Use only what the notes state — never invent decisions, owners, dates, or outcomes; omit any detail the notes do not give."
3. Make bullet selection rule-based so "five bullets" is predictable. Old: "into five bullet points." → New: "into five bullet points, prioritising decisions made, action items and their owners or deadlines, and unresolved questions."
4. Bound the input and the sparse/no-input cases. Insert after the first sentence → " Use the meeting notes provided in the request; if they contain fewer than five distinct points, output only the points that exist rather than padding to five, and if no notes are provided, ask for the notes."
5. State the intended reader so "useful" becomes checkable. Append → "Write for a colleague who missed the meeting and needs to act on it without re-reading the notes."

All five replacements retain the fidelity source's three facts — meeting notes, five bullet points, and short and useful — and no existing clause is removed.