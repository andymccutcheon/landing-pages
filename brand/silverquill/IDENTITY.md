# Silverquill — identity

**Author:** Layla Brower (design role-agent). **Date:** 21 October 2026.
**Status:** the name is chosen by the founder; the mark is not yet. This is the first pass.

**Reading this as:** an identity for an open-source command-line prompt-review tool — an instrument,
not a mascot — in a letterpress-and-ink register, leaning scientific-editorial.
**Dials:** design variance 6, motion intensity 1 (an identity has no motion; the page keeps its own),
visual density 3.

**Palette** is the page's existing token set, unchanged: ground `#151417`, ink `#f0eee9`, signal
`#d4ed80`, secondary `#c0bbc4`, muted `#a39da8`, raised `#29272d`.
**Type** is the page's existing pair: Fraunces for the wordmark, Geist for utility surfaces, Geist Mono
for code. Nothing is drawn as a raster except the social card.

---

## 1. Why the mark is being redrawn

The old mark was a literal nine — a circle with a descender hook — in the wordmark and the favicon.
That mark *was* the name. With the name changing, there is nothing to preserve, so the mark is a free
choice rather than a constraint. That freedom is worth spending once, properly.

## 2. Three directions

Full comparison with small-scale tests: `mark-directions.html`. Source files: `marks/`.

### Direction one — The Rule

A hairline rule divided into ten, with the ninth division marked tall. A rubric is a ruled line with
marks, and the run stops at the ninth; the old name's number survives as a mark on a rule instead of a
letter in a wordmark.

*Where it wins:* it is the only direction that explains where the product came from.
*Where it loses:* at sixteen pixels a tenth of a rubric is not legible, so the favicon needs a
simplified six-mark variant. And it asks the reader to know what a rubric is before they know the
product.

### Direction two — The Quoted

Two hairline hooks, drawn as closing quotes. The product's signature act is quoting: it names the
exact line that is wrong, with a quote, and then fixes it.

*Where it wins:* the best behaviour-match, and it holds at every size without simplification.
*Where it loses:* a pair of quote marks is a general typographic symbol. At full size it reads closer to
brackets than to language, and it does not carry the word "quill" at all.

### Direction three — The Nib

A nib and the stroke it has just written. Silver and ink, one stroke, no ornament.

*Where it wins:* the most handsome of the three and the most obviously the name. It holds at sixteen
pixels and needs no variant.
*Where it loses:* a fountain pen is the oldest mark in the book. It reads as heritage, and this product
argues for the opposite. It also leans a little costume — the one register the page has avoided.

## 3. My recommendation: one logo, two devices

The three ideas do not have to compete for the same job. Use each where it is actually best:

- **The Nib is the mark.** It is the name, it is the best-looking thing here, and it is the only one
  that survives a favicon without a second drawing.
- **The Rule becomes the rubric device.** A ruled line with the ninth marked is exactly what a
  scorecard wants: it turns the score track into a measure instead of a number. It belongs in the
  interface, in the score display, and in the page's diagram — not in the logo.
- **The Quoted becomes the evidence device.** Quoted evidence is the product's substance. A hairline
  quote mark as a section device, at the size of punctuation rather than a logo, tells the reader
  "this line is being quoted" before any label has to.

This gives the brand one mark, and gives the product two graphic tools it did not have.

## 4. Wordmark

- **Editorial surfaces** (the page header, the footer, the social card, print): the mark, then
  **Silverquill** in Fraunces at weight 600, tracked at `-0.03em`. The serif carries the register of a
  written word.
- **Utility surfaces** (the terminal banner, the npm page header, the CLI help text, the repository
  description): the mark, then **Silverquill** in Geist at weight 550, tracked at `-0.02em`. The
  grotesque carries the register of a tool.

Two lockups, one identity: the brand is editorial, the tool is technical, and the difference between
those two faces is the argument the product is making.

## 5. Not decided yet

- Which mark direction (mine: The Nib).
- Whether the wordmark is one word or two — "Silverquill" reads as one word, which is right, but the
  page's display type may prefer "Silver Quill" at large sizes. That is a typographic call to make on
  the rendered lockup, not on paper.
- The favicon and the social card need their own drawings once the mark is chosen.

## 6. What is not changing

The page's palette, its type pair, its motion system, its three diagrams and its seven-section
structure all stay as they are. The mark is new; the design system is not being reopened.
