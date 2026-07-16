#!/usr/bin/env python3
"""Idempotently inject a fit-safe formatting override so slide content never
clips off the bottom. Content/narrative is never touched.

Root cause of clipping (per context/storyteller-instructions.md): slides use
`justify-content: center` but lost `overflow-y: auto`, so tall content is
centered and its top/bottom are clipped with no way to scroll. This override:
  - restores `overflow-y: auto` on every slide (scroll safety net),
  - top-aligns content slides (grows downward, scrolls instead of clipping),
  - keeps `.center` title/frame slides centered ONLY when short,
  - caps runaway hero numbers so a 160px stat can't push content off-screen.

Usage:
    python tools/fix_deck_fit.py docs/a.html docs/b.html ...
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "injected by fix_deck_fit"

FIT_CSS = """
/* --- fit-safe formatting (injected by fix_deck_fit) --- */
.slide{overflow-y:auto!important;overflow-x:hidden!important;}
/* content slides flow from the top so tall content scrolls instead of clipping */
.slide:not(.center){justify-content:flex-start!important;}
/* a centered slide that is too tall stops centering and flows from the top */
@media (max-height:820px){.slide.center{justify-content:flex-start!important;}}
/* cap runaway hero numbers so a huge stat can't shove content off-screen */
.velocity-number,.stat-value,.big-number,.metric-value,.stat-num,.hero-number,.stat-number{
  font-size:clamp(40px,8vw,96px)!important;line-height:1.05!important;}
"""


def inject_fit(html: str) -> tuple[str, bool]:
    if MARKER in html:
        return html, False
    m = re.search(r"</style>", html, re.IGNORECASE)
    if not m:
        return html, False
    idx = m.start()
    return html[:idx] + FIT_CSS + html[idx:], True


def main(argv: list[str]) -> int:
    changed = 0
    for f in argv:
        p = Path(f)
        if not p.exists():
            print(f"MISSING {p}")
            continue
        html = p.read_text(encoding="utf-8")
        html, did = inject_fit(html)
        if did:
            p.write_text(html, encoding="utf-8")
            changed += 1
            print(f"FIXED {p.name}")
        else:
            print(f"ok    {p.name}: already has fit override")
    print(f"\n{changed} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
