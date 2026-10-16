/* Alien UI design system — type-on engine (zero dependencies).
 *
 * Machine-paced text reveal per the library §3.5 timings: one character per
 * 50 ms tick, the newest character renders "hot" (white) then decays to the
 * screen hue over 450 ms. A cursor block leads the text (P03).
 *
 * Reduced motion: text appears instantly, no animation.
 */
(function () {
  "use strict";

  var REDUCED = window.matchMedia
    && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function cursorBlock() {
    var c = document.createElement("span");
    c.className = "t-hot typeon-cursor";
    c.textContent = "\u2588";
    return c;
  }

  /* Reveal `text` inside `el`, one char per tick. Returns a promise. */
  function typeOn(el, text, opts) {
    opts = opts || {};
    var charMs = opts.charMs || 50;
    var hotMs = opts.hotMs || 450;
    el.textContent = "";
    var cursor = cursorBlock();
    el.appendChild(cursor);

    if (REDUCED) {
      el.textContent = text;
      return Promise.resolve();
    }

    return new Promise(function (resolve) {
      var i = 0;
      (function tick() {
        if (i >= text.length) {
          el.removeChild(cursor);
          resolve();
          return;
        }
        var span = document.createElement("span");
        span.className = "char-new";
        span.textContent = text[i];
        el.insertBefore(span, cursor);
        window.setTimeout(function () { span.classList.remove("char-new"); }, hotMs);
        i += 1;
        window.setTimeout(tick, charMs);
      })();
    });
  }

  /* Line-by-line boot: each line types on, with a beat between lines. */
  function bootLines(el, lines, opts) {
    opts = opts || {};
    var lineMs = opts.lineMs || 160;
    el.textContent = "";
    if (REDUCED) {
      lines.forEach(function (line) {
        var row = document.createElement("div");
        row.textContent = line;
        el.appendChild(row);
      });
      return Promise.resolve();
    }
    var queue = Promise.resolve();
    lines.forEach(function (line) {
      queue = queue.then(function () {
        var row = document.createElement("div");
        el.appendChild(row);
        return typeOn(row, line, opts).then(function () {
          return new Promise(function (r) { window.setTimeout(r, lineMs); });
        });
      });
    });
    return queue;
  }

  window.TypeOn = { typeOn: typeOn, bootLines: bootLines, REDUCED: REDUCED };
})();
