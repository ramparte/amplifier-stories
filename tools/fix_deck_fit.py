#!/usr/bin/env python3
"""Idempotently inject a fit-safe formatting override so slide content never
clips off the bottom, with vertical scroll as an escape valve. Content/narrative
is never touched. Re-running REPLACES any previously injected block (so the
override can be upgraded in place).

Root cause of clipping: in JS slide-mode the body has `overflow:hidden` and each
`.slide` uses `min-height:100vh` with no cap. When content is taller than the
viewport the slide GROWS past 100vh (min-height, not max-height) and the extra
height is clipped by the hidden body overflow -- with no way to reach it.

The fix caps each slide to the viewport (`max-height:100dvh`) and gives it
`overflow-y:auto`, so tall content scrolls INSIDE the slide (the escape valve)
instead of being clipped. Content slides also top-align so they grow downward.

Usage:
    python tools/fix_deck_fit.py docs/a.html docs/b.html ...
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BEGIN = "/* --- BEGIN fit-safe formatting (fix_deck_fit) --- */"
END = "/* --- END fit-safe formatting (fix_deck_fit) --- */"

FIT_CSS = f"""
{BEGIN}
/* every slide can scroll; content flows from the top (no center-clip) */
.slide{{overflow-y:auto!important;overflow-x:hidden!important;}}
.slide:not(.center){{justify-content:flex-start!important;}}
@media (max-height:820px){{.slide.center{{justify-content:flex-start!important;}}}}
/* JS slide-mode: cap the slide to the viewport and scroll INSIDE it (escape valve) */
html.js .slide{{max-height:100vh;max-height:100dvh;overflow-y:auto!important;-webkit-overflow-scrolling:touch;}}
/* no-JS: slides are position:relative and the page scrolls naturally */
/* cap runaway hero numbers so a huge stat can't shove content off-screen */
.velocity-number,.stat-value,.big-number,.metric-value,.stat-num,.hero-number,.stat-number{{
  font-size:clamp(40px,8vw,96px)!important;line-height:1.05!important;}}
{END}
"""

BLOCK_RE = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)


def inject_fit(html: str) -> str:
    # Remove any prior injected block so we can upgrade it in place.
    html = BLOCK_RE.sub("", html)
    m = re.search(r"</style>", html, re.IGNORECASE)
    if not m:
        return html
    idx = m.start()
    return html[:idx] + FIT_CSS + html[idx:]


def main(argv: list[str]) -> int:
    changed = 0
    for f in argv:
        p = Path(f)
        if not p.exists():
            print(f"MISSING {p}")
            continue
        original = p.read_text(encoding="utf-8")
        updated = inject_fit(original)
        if updated != original:
            p.write_text(updated, encoding="utf-8")
            changed += 1
            print(f"FIXED {p.name}")
        else:
            print(f"ok    {p.name}: no change")
    print(f"\n{changed} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
