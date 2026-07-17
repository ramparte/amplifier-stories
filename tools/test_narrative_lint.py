"""Tests for narrative_lint.py.

Narrative contract v2: frame-first, proof-early. A deck must open with a
`frame` beat (orientation/hook), then land a `proof` beat within the first
three beats. `payoff_before_midpoint` is relaxed to `payoff_present` -- a
payoff beat must exist somewhere, since with a frame opener the payoff
legitimately lands as the climax in the back half.

All fixtures are SYNTHETIC (inline) so these tests stay fast (no subprocess,
no dependency on real decks under docs/, which may be mid-migration to v2).
"""

from narrative_lint import HARD_CHECKS, lint_html

# A v2-good deck: spine comment with ABT/Payoff/advances; beats in order
# frame, proof, tension, payoff, takeaway; matching slide divs plus a
# trailing Sources slide (beat_slide_parity: slides == beats + 1).
GOOD_DECK_HTML = """<!DOCTYPE html>
<html><head><title>Good Deck</title></head>
<body>
<!--
ABT: AND we shipped fast; BUT nobody could tell if it worked;
     THEREFORE we built a gate.
Payoff: the gate catches the regression before it ever ships.
Beats (frame-first, proof-early; each advances the ABT):
  1. frame    -- advances: orients the audience, the stakes behind the AND
  2. proof    -- advances: establishes the AND -- the leverage is real
  3. tension  -- advances: establishes the BUT
  4. payoff   -- advances: lands the THEREFORE -- the climax
  5. takeaway -- advances: what the audience keeps
-->
  <div class="slide active center">
    <!-- beat 1: frame -->
    <h1>We shipped fast, but couldn't tell if it worked</h1>
  </div>
  <div class="slide">
    <!-- beat 2: proof -->
    <h2>The gate caught 12 regressions in its first week</h2>
  </div>
  <div class="slide">
    <!-- beat 3: tension -->
    <h2>Nobody trusted the green checkmark</h2>
  </div>
  <div class="slide">
    <!-- beat 4: payoff -->
    <h2>The gate is the leverage, judgment stays human</h2>
  </div>
  <div class="slide">
    <!-- beat 5: takeaway -->
    <h2>Build the gate before you scale the team</h2>
  </div>
  <div class="slide">
    <h2>Sources &amp; Research Methodology</h2>
  </div>
</body></html>"""

# Opens with `proof`, no `frame` beat at all -- must fail frame_first only
# (proof_early and payoff_present both still pass).
NO_FRAME_DECK_HTML = """<!DOCTYPE html>
<html><body>
<!--
ABT: AND we shipped fast; BUT nobody could tell if it worked;
     THEREFORE we built a gate.
Payoff: the gate catches the regression before it ever ships.
Beats:
  1. proof   -- advances: establishes the AND
  2. tension -- advances: establishes the BUT
  3. payoff  -- advances: lands the THEREFORE
-->
  <div class="slide active center">
    <!-- beat 1: proof -->
    <h2>The gate caught 12 regressions in its first week</h2>
  </div>
  <div class="slide">
    <!-- beat 2: tension -->
    <h2>Nobody trusted the green checkmark</h2>
  </div>
  <div class="slide">
    <!-- beat 3: payoff -->
    <h2>The gate is the leverage, judgment stays human</h2>
  </div>
  <div class="slide">
    <h2>Sources &amp; Research Methodology</h2>
  </div>
</body></html>"""

# Frame first, but proof doesn't land until beat 4 -- must fail proof_early
# only (frame_first and payoff_present both still pass).
DELAYED_PROOF_DECK_HTML = """<!DOCTYPE html>
<html><body>
<!--
ABT: AND we shipped fast; BUT nobody could tell if it worked;
     THEREFORE we built a gate.
Payoff: the gate catches the regression before it ever ships.
Beats:
  1. frame     -- advances: orients the audience
  2. tension    -- advances: establishes the BUT early
  3. mechanism  -- advances: shows how the gate works
  4. proof      -- advances: establishes the AND -- the leverage is real
  5. payoff     -- advances: lands the THEREFORE
  6. takeaway   -- advances: what the audience keeps
-->
  <div class="slide active center">
    <!-- beat 1: frame -->
    <h1>We shipped fast, but couldn't tell if it worked</h1>
  </div>
  <div class="slide">
    <!-- beat 2: tension -->
    <h2>Nobody trusted the green checkmark</h2>
  </div>
  <div class="slide">
    <!-- beat 3: mechanism -->
    <h2>The gate runs on every commit</h2>
  </div>
  <div class="slide">
    <!-- beat 4: proof -->
    <h2>The gate caught 12 regressions in its first week</h2>
  </div>
  <div class="slide">
    <!-- beat 5: payoff -->
    <h2>The gate is the leverage, judgment stays human</h2>
  </div>
  <div class="slide">
    <!-- beat 6: takeaway -->
    <h2>Build the gate before you scale the team</h2>
  </div>
  <div class="slide">
    <h2>Sources &amp; Research Methodology</h2>
  </div>
</body></html>"""

# Frame first, proof early, but no payoff beat anywhere -- must fail
# payoff_present only (frame_first and proof_early both still pass).
NO_PAYOFF_DECK_HTML = """<!DOCTYPE html>
<html><body>
<!--
ABT: AND we shipped fast; BUT nobody could tell if it worked;
     THEREFORE we built a gate.
Payoff: the gate catches the regression before it ever ships.
Beats:
  1. frame    -- advances: orients the audience
  2. proof    -- advances: establishes the AND
  3. tension  -- advances: establishes the BUT
  4. takeaway -- advances: what the audience keeps
-->
  <div class="slide active center">
    <!-- beat 1: frame -->
    <h1>We shipped fast, but couldn't tell if it worked</h1>
  </div>
  <div class="slide">
    <!-- beat 2: proof -->
    <h2>The gate caught 12 regressions in its first week</h2>
  </div>
  <div class="slide">
    <!-- beat 3: tension -->
    <h2>Nobody trusted the green checkmark</h2>
  </div>
  <div class="slide">
    <!-- beat 4: takeaway -->
    <h2>Build the gate before you scale the team</h2>
  </div>
  <div class="slide">
    <h2>Sources &amp; Research Methodology</h2>
  </div>
</body></html>"""

# A "bad" deck is the old failure mode: topic-label title slides, no spine
# comment, no beat markers at all.
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


def test_good_deck_passes_all_hard_gates():
    result = lint_html(GOOD_DECK_HTML, "good.html")
    assert result["hard_fail"] is False, [
        n for n in HARD_CHECKS if result["checks"][n]["status"] == "fail"
    ]
    for name in HARD_CHECKS:
        assert result["checks"][name]["status"] in ("pass", "warn"), (
            f"hard gate {name} unexpectedly failed: {result['checks'][name]}"
        )


def test_good_deck_passes_frame_first():
    result = lint_html(GOOD_DECK_HTML, "good.html")
    assert result["checks"]["frame_first"]["status"] == "pass"


def test_good_deck_passes_proof_early():
    result = lint_html(GOOD_DECK_HTML, "good.html")
    assert result["checks"]["proof_early"]["status"] == "pass"


def test_good_deck_passes_payoff_present():
    result = lint_html(GOOD_DECK_HTML, "good.html")
    assert result["checks"]["payoff_present"]["status"] == "pass"


def test_good_deck_has_matching_beats_and_slides():
    result = lint_html(GOOD_DECK_HTML, "good.html")
    assert result["beats"] == 5
    assert result["slides"] == 6  # 5 beats + Sources slide


def test_deck_opening_with_proof_fails_frame_first_only():
    result = lint_html(NO_FRAME_DECK_HTML, "no_frame.html")
    assert result["checks"]["frame_first"]["status"] == "fail"
    assert result["checks"]["frame_first"]["detail"] == "first beat role = proof"
    assert result["checks"]["proof_early"]["status"] == "pass"
    assert result["checks"]["payoff_present"]["status"] == "pass"
    assert result["hard_fail"] is True


def test_deck_with_delayed_proof_fails_proof_early_only():
    result = lint_html(DELAYED_PROOF_DECK_HTML, "delayed_proof.html")
    assert result["checks"]["frame_first"]["status"] == "pass"
    assert result["checks"]["proof_early"]["status"] == "fail"
    assert "frame, tension, mechanism" in result["checks"]["proof_early"]["detail"]
    assert result["checks"]["payoff_present"]["status"] == "pass"
    assert result["hard_fail"] is True


def test_deck_with_no_payoff_fails_payoff_present_only():
    result = lint_html(NO_PAYOFF_DECK_HTML, "no_payoff.html")
    assert result["checks"]["frame_first"]["status"] == "pass"
    assert result["checks"]["proof_early"]["status"] == "pass"
    assert result["checks"]["payoff_present"]["status"] == "fail"
    assert result["checks"]["payoff_present"]["detail"] == "no payoff beat"
    assert result["hard_fail"] is True


def test_known_bad_deck_hard_fails():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["hard_fail"] is True


def test_known_bad_deck_fails_spine_present():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["checks"]["spine_present"]["status"] == "fail"


def test_known_bad_deck_fails_frame_first():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["checks"]["frame_first"]["status"] == "fail"


def test_known_bad_deck_fails_proof_early():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["checks"]["proof_early"]["status"] == "fail"


def test_known_bad_deck_fails_payoff_present():
    result = lint_html(BAD_DECK_HTML, "bad.html")
    assert result["checks"]["payoff_present"]["status"] == "fail"


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
    result = lint_html(GOOD_DECK_HTML, "good.html")
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
