"""Tests for narrative_lint.py using real fixture decks already in the repo.

Known-good decks (spine-first regenerations under docs/narrative-preview/) must
pass every hard gate. Known-bad decks (the pre-regeneration originals under
docs/) have no spine and are not proof-first, so they must hard-fail on
spine_present and proof_first specifically.
"""

from pathlib import Path

from narrative_lint import HARD_CHECKS, lint_file

REPO_ROOT = Path(__file__).resolve().parent.parent

KNOWN_GOOD = [
    REPO_ROOT / "docs/narrative-preview/the-foundry-and-the-machine.html",
    REPO_ROOT / "docs/narrative-preview/superpowers-deck.html",
    REPO_ROOT / "docs/narrative-preview/context-rot-systems-architecture.html",
]

KNOWN_BAD = [
    REPO_ROOT / "docs/the-foundry-and-the-machine.html",
    REPO_ROOT / "docs/superpowers-deck.html",
]


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


def test_known_bad_decks_hard_fail():
    for path in KNOWN_BAD:
        result = lint_file(path)
        assert result["hard_fail"] is True, (
            f"{path.name} should hard-fail (no spine present)"
        )


def test_known_bad_decks_fail_spine_present():
    for path in KNOWN_BAD:
        result = lint_file(path)
        assert result["checks"]["spine_present"]["status"] == "fail", (
            f"{path.name} should fail spine_present (no ABT/Payoff/advances comment)"
        )


def test_known_bad_decks_fail_proof_first():
    for path in KNOWN_BAD:
        result = lint_file(path)
        assert result["checks"]["proof_first"]["status"] == "fail", (
            f"{path.name} should fail proof_first (no beat markers at all)"
        )


def test_known_bad_decks_have_zero_beats():
    for path in KNOWN_BAD:
        result = lint_file(path)
        assert result["beats"] == 0
        assert result["checks"]["beat_markers"]["status"] == "fail"


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
