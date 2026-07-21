#!/usr/bin/env python3
"""narrative_lint.py -- deterministic narrative-structure linter for HTML story decks.

Mechanically verifies each deck against the narrative-spine contract defined in
context/storyteller-instructions.md ("## Narrative Layer"). Stdlib only (re +
basic string/regex parsing) -- no bs4/lxml -- so it stays fast and dependency-light
across a batch of ~200 decks.

Usage:
    python tools/narrative_lint.py <file.html> [<file2.html> ...]
    python tools/narrative_lint.py --json <path> <files...>
    python tools/narrative_lint.py --manifest ai_working/deck-manifest.txt --root docs --json ai_working/lint.json

Exit code 0 if all decks pass all HARD gates; 1 if any deck fails a hard gate.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from html import unescape
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Regexes
# ---------------------------------------------------------------------------

# Match any <div> whose class attribute contains `slide` as a whole class token
# (e.g. class="slide", "slide active", "slide center", "slide slide-statement").
# `slide-title`/`slide-body`/`slide-counter` are DIFFERENT single tokens and are
# correctly NOT matched, since we require `slide` as a standalone word token.
SLIDE_OPEN_RE = re.compile(r'<div\b[^>]*\bclass="([^"]*)"[^>]*>', re.IGNORECASE)


def _class_is_slide(class_value: str) -> bool:
    """True iff the class attribute has `slide` as a standalone token."""
    return "slide" in class_value.split()


def count_slide_divs(html: str) -> int:
    return sum(1 for m in SLIDE_OPEN_RE.finditer(html) if _class_is_slide(m.group(1)))


BEAT_COMMENT_RE = re.compile(r"<!--\s*beat\s+\d+\s*:\s*(\w+)\s*-->", re.IGNORECASE)
SPINE_COMMENT_RE = re.compile(r"<!--(.*?)-->", re.DOTALL)
H1_H2_RE = re.compile(r"<(h1|h2)\b[^>]*>(.*?)</\1>", re.IGNORECASE | re.DOTALL)
TAG_STRIP_RE = re.compile(r"<[^>]+>")
PUNCT_RE = re.compile(r"[^a-z0-9\s]")
CLASS_ATTR_RE = re.compile(r'class="([^"]+)"')
FONT_SIZE_DECL_RE = re.compile(r'font-size:\s*([^;"]+)')
STAT_CLASS_ELEMENT_RE = re.compile(
    r'<[^>]+class="[^"]*(?:stat-value|big-number|metric-value|stat-num|hero-number)[^"]*"[^>]*>(.*?)</\w+>',
    re.IGNORECASE | re.DOTALL,
)
NUMBER_TOKEN_RE = re.compile(r"[\d][\d,]*\+?")

# Bare topic-label denylist -- headline text that is a label, not a claim.
TOPIC_LABEL_DENYLIST = {
    "metrics",
    "overview",
    "architecture",
    "features",
    "introduction",
    "intro",
    "agenda",
    "summary",
    "background",
    "benefits",
    "use cases",
    "how it works",
    "the problem",
    "results",
    "conclusion",
    "what it does",
    "capabilities",
}

# Class-name substrings that indicate "card-like" repeated tile elements.
CARD_CLASS_SUBSTRINGS = (
    "card",
    "tile",
    "stat",
    "feature",
    "cell",
    "grid-item",
    "mode-row",
    "col-",
)

HARD_CHECKS = (
    "spine_present",
    "beat_markers",
    "title_slide",
    "beat_slide_parity",
    "frame_first",
    "proof_early",
    "payoff_present",
    "sources_slide",
)

WARN_CHECKS = (
    "title_brevity",
    "topic_label_headlines",
    "tile_grid_catalog",
    "big_number_clip_risk",
    "progressive_enhancement",
    "more_stories_link",
)

ALL_CHECKS = HARD_CHECKS + WARN_CHECKS


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------


def parse_beat_roles(html: str) -> list[str]:
    """Ordered list of beat roles from `<!-- beat N: role -->` comments."""
    return [role.lower() for role in BEAT_COMMENT_RE.findall(html)]


def find_spine_comment(html: str) -> str | None:
    """Return the content of the first HTML comment that contains 'ABT:'."""
    for match in SPINE_COMMENT_RE.finditer(html):
        content = match.group(1)
        if re.search(r"abt\s*:", content, re.IGNORECASE):
            return content
    return None


def split_slide_blocks(html: str) -> list[str]:
    """Slice the document into per-slide chunks at each `<div class="slide...">` open tag."""
    starts = [m.start() for m in SLIDE_OPEN_RE.finditer(html)]
    blocks = []
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else len(html)
        blocks.append(html[start:end])
    return blocks


def normalize_headline(raw_inner_html: str) -> str:
    """Strip tags/entities/punctuation and lowercase, for denylist comparison."""
    text = TAG_STRIP_RE.sub(" ", raw_inner_html)
    text = unescape(text).strip().lower()
    text = PUNCT_RE.sub("", text)
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------------------
# Individual checks -- each returns (status, detail)
# ---------------------------------------------------------------------------


def check_spine_present(html: str, spine: str | None) -> tuple[str, str]:
    if spine is None:
        return "fail", "missing: ABT:, Payoff, advances: (no spine comment found)"
    missing = []
    if not re.search(r"abt\s*:", spine, re.IGNORECASE):
        missing.append("ABT:")
    if not re.search(r"payoff", spine, re.IGNORECASE):
        missing.append("Payoff")
    if not re.search(r"advances\s*:", spine, re.IGNORECASE):
        missing.append("advances:")
    if missing:
        return "fail", "missing: " + ", ".join(missing)
    return "pass", "spine present (ABT/Payoff/advances found)"


def check_beat_markers(roles: list[str]) -> tuple[str, str]:
    if not roles:
        return "fail", "no beat markers found"
    return "pass", f"{len(roles)} beat markers found: {', '.join(roles)}"


def check_beat_slide_parity(
    beat_count: int, slide_count: int, has_title_slide: bool = False
) -> tuple[str, str]:
    # Non-beat slides = an optional title cover (before beat 1) + a Sources slide.
    # base = one slide per beat, plus the title cover when present.
    base = beat_count + (1 if has_title_slide else 0)
    detail = f"beats={beat_count} slides={slide_count}" + (
        " +title" if has_title_slide else ""
    )
    if slide_count == base + 1:  # + Sources slide
        return "pass", detail
    if slide_count == base:  # missing the Sources slide
        return "warn", detail + " (no separate Sources slide)"
    return "fail", detail


def _first_slide_is_title(slide_blocks: list[str]) -> bool:
    """True iff the first slide div carries the `title-slide` class token."""
    if not slide_blocks:
        return False
    classes = CLASS_ATTR_RE.findall(slide_blocks[0])
    return any("title-slide" in value.split() for value in classes)


def check_title_slide(slide_blocks: list[str]) -> tuple[str, str]:
    """The deck must open with a near-wordless title/cover slide BEFORE beat 1.

    Detected structurally: the first `<div class="slide ...">` must include the
    `title-slide` class token, must NOT carry a `<!-- beat N: role -->` comment
    (it precedes the frame beat), and must carry a heading to hold the title.
    """
    if not slide_blocks:
        return "fail", "no slides found"
    first = slide_blocks[0]
    if not _first_slide_is_title(slide_blocks):
        return (
            "fail",
            "first slide is not a title cover (class must include 'title-slide')",
        )
    if BEAT_COMMENT_RE.search(first):
        return "fail", "title slide must not carry a beat comment (it precedes beat 1)"
    if not H1_H2_RE.search(first):
        return "fail", "title slide has no <h1>/<h2> title text"
    return "pass", "title cover slide present before beat 1"


def check_title_brevity(slide_blocks: list[str]) -> tuple[str, str]:
    """The title (the title slide's <h1>) should be 5 words or fewer.

    The subtitle is not counted -- render it as a separate element (e.g. a
    `subtitle` paragraph), not inside the <h1>.
    """
    if not _first_slide_is_title(slide_blocks):
        return "na", "no title slide"
    first = slide_blocks[0]
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", first, re.IGNORECASE | re.DOTALL)
    if m is None:
        m = re.search(r"<h2\b[^>]*>(.*?)</h2>", first, re.IGNORECASE | re.DOTALL)
    if m is None:
        return "warn", "title slide has no <h1> title to measure"
    title_text = normalize_headline(m.group(1))
    words = len(title_text.split())
    if words > 5:
        return "warn", f"title is {words} words (>5): {title_text!r}"
    return "pass", f"title is {words} words: {title_text!r}"


def check_frame_first(roles: list[str], spine: str | None) -> tuple[str, str]:
    if not roles:
        return "fail", "no beats found"
    first = roles[0]
    if first in ("frame", "setup"):
        return "pass", f"first beat role = {first}"
    if spine and re.search(r"cold_open_reason", spine, re.IGNORECASE):
        return "pass", f"first beat role = {first}, but cold_open_reason present"
    return "fail", f"first beat role = {first}"


def check_proof_early(roles: list[str], spine: str | None) -> tuple[str, str]:
    if not roles:
        return "fail", "no beats found"
    first_three = roles[0:3]
    if "proof" in first_three:
        return "pass", f"proof in first 3 beats (roles: {', '.join(first_three)})"
    if spine and re.search(r"proof_deferred_reason", spine, re.IGNORECASE):
        return (
            "pass",
            f"no proof in first 3 beats (roles: {', '.join(first_three)}), "
            "but proof_deferred_reason present",
        )
    return "fail", f"no proof in first 3 beats (roles: {', '.join(first_three)})"


def check_payoff_present(roles: list[str]) -> tuple[str, str]:
    n = len(roles)
    if n == 0:
        return "fail", "no beats found"
    if "payoff" not in roles:
        return "fail", "no payoff beat"
    idx = roles.index("payoff")
    return "pass", f"payoff at beat {idx + 1} of {n}"


def check_sources_slide(html: str) -> tuple[str, str]:
    if re.search(r"sources|research methodology", html, re.IGNORECASE):
        return "pass", "Sources/Research Methodology text found"
    return "fail", "no 'Sources' or 'Research Methodology' text found"


def check_topic_label_headlines(html: str) -> tuple[str, str]:
    offenders = []
    for match in H1_H2_RE.finditer(html):
        raw_inner = match.group(2)
        if normalize_headline(raw_inner) in TOPIC_LABEL_DENYLIST:
            clean = unescape(TAG_STRIP_RE.sub("", raw_inner)).strip()
            offenders.append(clean)
    if offenders:
        return "warn", "bare topic-label headlines: " + "; ".join(offenders)
    return "pass", "no bare topic-label headlines found"


def check_tile_grid_catalog(slide_blocks: list[str]) -> tuple[str, str]:
    hits = []
    for idx, block in enumerate(slide_blocks, start=1):
        class_values = CLASS_ATTR_RE.findall(block)
        primary_tokens = [v.split()[0] for v in class_values if v.split()]
        counts = Counter(primary_tokens)
        best = None
        for cls, cnt in counts.items():
            if cnt >= 4 and any(sub in cls.lower() for sub in CARD_CLASS_SUBSTRINGS):
                if best is None or cnt > best[1]:
                    best = (cls, cnt)
        if best:
            hits.append((idx, best[0], best[1]))
    if hits:
        detail = "; ".join(f"slide {i} class={c!r} count={n}" for i, c, n in hits)
        return "warn", detail
    return "pass", "no slide with >=4 co-equal card-like tiles"


def check_big_number_clip_risk(html: str) -> tuple[str, str]:
    candidates = []
    for match in STAT_CLASS_ELEMENT_RE.finditer(html):
        inner_text = TAG_STRIP_RE.sub("", match.group(1))
        for num in NUMBER_TOKEN_RE.findall(inner_text):
            if len(num) >= 5:
                candidates.append(num)

    if not candidates:
        return "na", "no stat/big-number elements with >=5-char numbers detected"

    large_fixed = []
    for decl in FONT_SIZE_DECL_RE.findall(html):
        val = decl.strip()
        if val.lower().startswith("clamp"):
            continue
        m = re.match(r"(\d+(?:\.\d+)?)px", val)
        if m and float(m.group(1)) >= 72:
            large_fixed.append(val)

    if large_fixed:
        return (
            "warn",
            f"stat numbers {candidates[:3]} co-occur with fixed font-size(s) "
            f"{large_fixed[:3]} not wrapped in clamp()",
        )
    return "pass", "no fixed >=72px font-size found outside clamp()"


def check_progressive_enhancement(html: str) -> tuple[str, str]:
    if re.search(r"classList\.add\(\s*['\"]js['\"]\s*\)", html):
        return "pass", "progressive enhancement script found"
    return "warn", "classList.add('js') not found"


def check_more_stories_link(html: str) -> tuple[str, str]:
    if "More Amplifier Stories" in html:
        return "pass", "'More Amplifier Stories' link found"
    return "warn", "'More Amplifier Stories' text not found"


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def lint_html(html: str, filename: str = "<string>") -> dict[str, Any]:
    """Run all checks against an HTML string and return the result dict."""
    roles = parse_beat_roles(html)
    beat_count = len(roles)
    slide_count = count_slide_divs(html)
    spine = find_spine_comment(html)
    slide_blocks = split_slide_blocks(html)

    def _entry(status_detail: tuple[str, str]) -> dict[str, str]:
        status, detail = status_detail
        return {"status": status, "detail": detail}

    has_title_slide = _first_slide_is_title(slide_blocks)

    checks = {
        "spine_present": _entry(check_spine_present(html, spine)),
        "beat_markers": _entry(check_beat_markers(roles)),
        "title_slide": _entry(check_title_slide(slide_blocks)),
        "beat_slide_parity": _entry(
            check_beat_slide_parity(beat_count, slide_count, has_title_slide)
        ),
        "frame_first": _entry(check_frame_first(roles, spine)),
        "proof_early": _entry(check_proof_early(roles, spine)),
        "payoff_present": _entry(check_payoff_present(roles)),
        "sources_slide": _entry(check_sources_slide(html)),
        "title_brevity": _entry(check_title_brevity(slide_blocks)),
        "topic_label_headlines": _entry(check_topic_label_headlines(html)),
        "tile_grid_catalog": _entry(check_tile_grid_catalog(slide_blocks)),
        "big_number_clip_risk": _entry(check_big_number_clip_risk(html)),
        "progressive_enhancement": _entry(check_progressive_enhancement(html)),
        "more_stories_link": _entry(check_more_stories_link(html)),
    }

    hard_fail = any(checks[name]["status"] == "fail" for name in HARD_CHECKS)
    warn_count = sum(1 for c in checks.values() if c["status"] == "warn")

    return {
        "file": filename,
        "beats": beat_count,
        "slides": slide_count,
        "roles": roles,
        "hard_fail": hard_fail,
        "checks": checks,
        "warn_count": warn_count,
    }


def lint_file(path: str | Path) -> dict[str, Any]:
    """Read a deck HTML file and lint it."""
    p = Path(path)
    html_text = p.read_text(encoding="utf-8")
    return lint_html(html_text, filename=str(path))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _resolve_file_list(args: argparse.Namespace) -> list[str]:
    file_paths: list[str] = []
    if args.manifest_path:
        manifest = Path(args.manifest_path)
        root = Path(args.root)
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            file_paths.append(str(root / line))
    file_paths.extend(args.files)
    return file_paths


def print_summary(results: list[dict[str, Any]]) -> None:
    for r in results:
        status = "HARD-FAIL" if r["hard_fail"] else "PASS"
        checks = r["checks"]
        failed = [
            name for name in HARD_CHECKS if checks.get(name, {}).get("status") == "fail"
        ]
        warned = [name for name, c in checks.items() if c.get("status") == "warn"]
        flags = []
        if failed:
            flags.append("FAIL:" + ",".join(failed))
        if warned:
            flags.append("WARN:" + ",".join(warned))
        flag_str = " ".join(flags) if flags else "-"
        print(
            f"{r['file']:<62} beats={r['beats']:<3} slides={r['slides']:<3} {status:<10} {flag_str}"
        )

    total = len(results)
    hard_fail_count = sum(1 for r in results if r["hard_fail"])
    warn_deck_count = sum(1 for r in results if r["warn_count"] > 0)
    print(
        f"\n{total} decks, {hard_fail_count} hard-fail, {warn_deck_count} with warnings"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic narrative-structure linter for HTML story decks."
    )
    parser.add_argument("files", nargs="*", help="HTML files to lint")
    parser.add_argument(
        "--json", dest="json_path", help="Write JSON results array to this path"
    )
    parser.add_argument(
        "--manifest",
        dest="manifest_path",
        help="Read newline-separated filenames from this manifest",
    )
    parser.add_argument(
        "--root",
        dest="root",
        default=".",
        help="Root directory to prefix manifest filenames with",
    )
    args = parser.parse_args(argv)

    file_paths = _resolve_file_list(args)
    if not file_paths:
        parser.error("no input files given (pass files directly, or use --manifest)")

    results = []
    for fp in file_paths:
        try:
            results.append(lint_file(fp))
        except OSError as exc:
            results.append(
                {
                    "file": fp,
                    "beats": 0,
                    "slides": 0,
                    "roles": [],
                    "hard_fail": True,
                    "checks": {"file_read": {"status": "fail", "detail": str(exc)}},
                    "warn_count": 0,
                }
            )

    print_summary(results)

    if args.json_path:
        Path(args.json_path).write_text(json.dumps(results, indent=2), encoding="utf-8")

    return 1 if any(r["hard_fail"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
