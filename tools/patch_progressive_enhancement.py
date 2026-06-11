#!/usr/bin/env python3
"""Patch HTML decks for progressive enhancement (no-JS fallback).

Without JavaScript, decks become scrollable single-page documents.
With JavaScript, slide navigation works as before.

Changes per file:
1. Adds <script>document.documentElement.classList.add("js")</script> before <style>
2. Changes .slide { display: none } to .slide { display: flex } (no-JS: all visible)
3. Removes overflow: hidden from body / html,body rules
4. Removes overscroll-behavior: none from body
5. Handles .deck wrapper (removes overflow/height for no-JS)
6. Adds html.js scoped rules to restore JS-mode behavior
"""

import re
from pathlib import Path


def patch_deck(filepath: Path) -> tuple[str, list[str]]:
    """Apply progressive enhancement to a single HTML deck.

    Returns (status, list_of_changes).
    """
    text = filepath.read_text(encoding="utf-8")

    # Skip if already patched
    if "document.documentElement.classList.add" in text:
        return "already_patched", []

    # Skip non-deck pages (index.html, etc.)
    if ".slide" not in text:
        return "not_a_deck", []

    original = text
    changes: list[str] = []

    # --- 1. Inject <script> before <style> ---
    new = re.sub(
        r"(\s*)(<style\b)",
        r"\1<script>document.documentElement.classList.add('js')</script>\n\1\2",
        text,
        count=1,
    )
    if new != text:
        changes.append("script_tag")
        text = new

    # --- 2. .slide { display: none → flex } ---
    # Matches .slide { ... display: none; ... }  but NOT .slide.active or .slide-xxx
    new = re.sub(
        r"(\.slide\s*\{[^}]*?)display:\s*none\s*;",
        r"\1display: flex;",
        text,
        count=1,
        flags=re.DOTALL,
    )
    if new != text:
        changes.append("slide_visible")
        text = new

    # --- 3. Remove overflow: hidden from body rules ---
    def _strip_overflow(m: re.Match) -> str:
        return re.sub(r"\s*overflow:\s*hidden\s*;", "", m.group(0))

    new = re.sub(
        r"(?:html\s*,\s*)?body\s*\{[^}]*?\}",
        _strip_overflow,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if new != text:
        changes.append("body_overflow")
        text = new

    # --- 4. Remove overscroll-behavior: none from body ---
    def _strip_overscroll(m: re.Match) -> str:
        return re.sub(r"\s*overscroll-behavior:\s*none\s*;", "", m.group(0))

    new = re.sub(
        r"(?:html\s*,\s*)?body\s*\{[^}]*?\}",
        _strip_overscroll,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if new != text:
        changes.append("body_overscroll")
        text = new

    # --- 5. Handle .deck wrapper ---
    has_deck = bool(re.search(r"\.deck\s*\{", text))
    if has_deck:

        def _strip_deck_props(m: re.Match) -> str:
            rule = m.group(0)
            rule = re.sub(r"\s*overflow:\s*hidden\s*;", "", rule)
            rule = re.sub(r"\s*height:\s*100dvh\s*;", "", rule)
            rule = re.sub(r"\s*height:\s*100vh\s*;", "", rule)
            return rule

        new = re.sub(
            r"\.deck\s*\{[^}]*?\}",
            _strip_deck_props,
            text,
            count=1,
            flags=re.DOTALL,
        )
        if new != text:
            changes.append("deck_wrapper")
            text = new

    # --- 6. Add html.js scoped rules ---
    js_block = "\n        /* Progressive enhancement: JS-only slide mode */\n"
    js_block += "        html.js { overflow: hidden; }\n"
    js_block += (
        "        html.js body { overflow: hidden; overscroll-behavior: none; }\n"
    )
    if has_deck:
        js_block += "        html.js .deck { height: 100vh; height: 100dvh; overflow: hidden; }\n"
    js_block += "        html.js .slide { display: none; }\n"
    js_block += "        html.js .slide.active { display: flex; }\n"

    new = text.replace("</style>", js_block + "    </style>", 1)
    if new != text:
        changes.append("js_scoped_rules")
        text = new

    if text == original:
        return "no_changes", changes

    filepath.write_text(text, encoding="utf-8")
    return "patched", changes


def main() -> None:
    docs = Path("/home/samschillace/dev/ANext/amplifier-stories/docs")
    buckets: dict[str, list] = {
        "patched": [],
        "already_patched": [],
        "not_a_deck": [],
        "no_changes": [],
        "error": [],
    }

    for f in sorted(docs.glob("*.html")):
        try:
            status, changes = patch_deck(f)
            buckets[status].append((f.name, changes))
        except Exception as exc:
            buckets["error"].append((f.name, str(exc)))

    # Report
    print(f"Patched:          {len(buckets['patched'])}")
    for name, ch in buckets["patched"]:
        print(f"  {name}: {', '.join(ch)}")

    print(f"Already patched:  {len(buckets['already_patched'])}")
    print(f"Skipped (non-deck): {len(buckets['not_a_deck'])}")
    for name, _ in buckets["not_a_deck"]:
        print(f"  {name}")
    print(f"No changes:       {len(buckets['no_changes'])}")
    for name, _ in buckets["no_changes"]:
        print(f"  {name}")
    print(f"Errors:           {len(buckets['error'])}")
    for name, err in buckets["error"]:
        print(f"  {name}: {err}")


if __name__ == "__main__":
    main()
