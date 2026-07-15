"""Tests for narrative_lint.py using real fixture decks already in the repo.

Known-good decks (spine-first regenerations under docs/narrative-preview/) must
pass every hard gate. Known-bad decks (the pre-regeneration originals under
docs/) have no spine and are not proof-first, so they must hard-fail on
spine_present and proof_first specifically.
"""

from pathlib import Path

from narrative_lint import HARD_CHECKS, lint_file, lint_html

REPO_ROOT = Path(__file__).resolve().parent.parent

KNOWN_GOOD = [
    REPO_ROOT / "docs/narrative-preview/the-foundry-and-the-machine.html",
    REPO_ROOT / "docs/narrative-preview/superpowers-deck.html",
    REPO_ROOT / "docs/narrative-preview/context-rot-systems-architecture.html",
]

# Known-bad decks are SYNTHETIC (inline) so the tests stay stable even when the
# batch regenerates every real deck in docs/ in place. A "bad" deck is the old
# failure mode: topic-label title slides, no spine comment, no beat markers.
BAD_DECK_HTML = """<!DOCTYPE html>
<html><head><title>Old Catalog Deck</title></head>
<body>
  <div class="slide active center"><h1>Overview</h1></div>
  <div class="slide"><h2>Architecture</h2><div class="card">a</div></div>
  <div class="slide"><h2>Features</h2></div>
  <div class="slide"><h2>Metrics</h2></div>
</body></html>"""

# A modifier-class deck: legit slides carrying `center` / `slide-statement`
# modifier tokens. The slide counter must still count all of these.
MODIFIER_CLASS_DECK_HTML = """<!DOCTYPE html>
<html><body>
  <div class="slide active center"><h2>Claim one</h2></div>
  <div class="slide slide-statement"><h2>Claim two</h2></div>
  <div class="slide center"><h2>Claim three</h2></div>
</body></html>"""


def test_known_good_decks_pass_all_hard_gates():
    for path in KNOWN_GOOD:
        result = lint_file(path)
        assert result["hard_fail"] is False, (
            f"{path.name} should pass all hard gates, but failed: "
            f"{[n for n in HARD_CHECKS if result['checks'][n]['status'] == 'fail']}"
        )
        for name in HARD_CHECKS:
            assert result["checks"][name]["status"] in ("pass", "warn"), (
                f"{path.name}: hard gate {name} unexpectedly failed: "
                f"{result['checks'][name]}"
            )


def test_known_good_decks_have_beats_and_matching_slides():
    for path in KNOWN_GOOD:
        result = lint_file(path)
        assert result["beats"] > 0, f"{path.name} should have beat markers"
        assert result["slides"] in (result["beats"], result["beats"] + 1), (
            f"{path.name}: slides={result['slides']} beats={result['beats']}"
        )


def test_known_bad_deck_hard_fails():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["hard_fail"] is True


def test_known_bad_deck_fails_spine_present():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["checks"]["spine_present"]["status"] == "fail"


def test_known_bad_deck_fails_proof_first():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["checks"]["proof_first"]["status"] == "fail"


def test_known_bad_deck_has_zero_beats():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["beats"] == 0
    assert result["checks"]["beat_markers"]["status"] == "fail"


def test_known_bad_deck_flags_topic_label_headlines():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    # "Overview", "Architecture", "Features", "Metrics" are all bare topic labels
    assert result["checks"]["topic_label_headlines"]["status"] == "warn"


def test_slide_counter_counts_modifier_class_slides():
    """Regression: slides carrying `center`/`slide-statement` modifier tokens
    were previously undercounted (only exact class="slide"/"slide active"
    matched), causing false beat/slide parity hard-fails."""
    result = lint_html(MODIFIER_CLASS_DECK_HTML, "mods.html")
    assert result["slides"] == 3, (
        f"expected 3 modifier-class slides, counted {result['slides']}"
    )


def test_result_schema_has_expected_keys():
    result = lint_file(KNOWN_GOOD[0])
    for key in (
        "file",
        "beats",
        "slides",
        "roles",
        "hard_fail",
        "checks",
        "warn_count",
    ):
        assert key in result
    for name in HARD_CHECKS:
        assert name in result["checks"]
        assert "status" in result["checks"][name]
        assert "detail" in result["checks"][name]
