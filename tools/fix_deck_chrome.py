#!/usr/bin/env python3
"""Idempotently add missing 'chrome' to decks: progressive-enhancement scaffolding
and the 'More Amplifier Stories' backlink. Content is never touched.

Progressive enhancement uses the deck-agnostic pattern from
context/storyteller-instructions.md: a `html.js` marker set immediately, a no-JS
fallback that forces all slides visible/scrollable, and JS-mode rules that hide
non-active slides. Because the injected rules are prefixed with `html:not(.js)`
(with !important) and `html.js`, they override each deck's own `.slide` rules
regardless of that deck's bespoke CSS, while preserving the existing `.active`
nav behavior for JS users.

Usage:
    python tools/fix_deck_chrome.py docs/a.html docs/b.html ...
    python tools/fix_deck_chrome.py --manifest ai_working/pe-fix.txt --root docs
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

JS_MARKER = "classList.add('js')"
JS_SNIPPET = "<script>document.documentElement.classList.add('js')</script>\n"

LINK_MARKER = "More Amplifier Stories"
LINK_SNIPPET = '<a href="index.html" class="more-stories">More Amplifier Stories</a>\n'

PE_CSS = """
/* --- progressive enhancement (no-JS fallback) — injected by fix_deck_chrome --- */
html:not(.js) .slide{display:flex!important;position:relative!important;opacity:1!important;pointer-events:auto!important;visibility:visible!important;transform:none!important;width:100%;min-height:100vh;min-height:100dvh;}
html.js{overflow:hidden;}
html.js body{overflow:hidden;overscroll-behavior:none;}
html.js .slide{display:none;}
html.js .slide.active{display:flex;}
"""


def add_js_class_script(html: str) -> tuple[str, bool]:
    if JS_MARKER in html:
        return html, False
    # Insert immediately before the first <style ...> tag.
    m = re.search(r"<style\b", html, re.IGNORECASE)
    if m:
        idx = m.start()
        return html[:idx] + JS_SNIPPET + html[idx:], True
    # Fallback: before </head>.
    m = re.search(r"</head>", html, re.IGNORECASE)
    if m:
        idx = m.start()
        return html[:idx] + JS_SNIPPET + html[idx:], True
    return html, False


def add_pe_css(html: str) -> tuple[str, bool]:
    if "injected by fix_deck_chrome" in html:
        return html, False
    # Append the fallback block before the first closing </style>.
    m = re.search(r"</style>", html, re.IGNORECASE)
    if not m:
        return html, False
    idx = m.start()
    return html[:idx] + PE_CSS + html[idx:], True


def add_backlink(html: str) -> tuple[str, bool]:
    if LINK_MARKER in html:
        return html, False
    m = re.search(r"</body>", html, re.IGNORECASE)
    if not m:
        return html, False
    idx = m.start()
    return html[:idx] + LINK_SNIPPET + html[idx:], True


def fix_file(path: Path) -> list[str]:
    html = path.read_text(encoding="utf-8")
    changes: list[str] = []

    html, did = add_js_class_script(html)
    if did:
        changes.append("js-class-script")
    html, did = add_pe_css(html)
    if did:
        changes.append("pe-css")
    html, did = add_backlink(html)
    if did:
        changes.append("backlink")

    if changes:
        path.write_text(html, encoding="utf-8")
    return changes


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--manifest")
    ap.add_argument("--root", default=".")
    args = ap.parse_args(argv)

    paths: list[Path] = [Path(f) for f in args.files]
    if args.manifest:
        root = Path(args.root)
        for line in Path(args.manifest).read_text().splitlines():
            line = line.strip()
            if line:
                paths.append(root / line)

    total_changed = 0
    for p in paths:
        if not p.exists():
            print(f"MISSING {p}")
            continue
        changes = fix_file(p)
        if changes:
            total_changed += 1
            print(f"FIXED {p.name}: {', '.join(changes)}")
        else:
            print(f"ok    {p.name}: nothing to add")
    print(f"\n{total_changed} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
