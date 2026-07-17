#!/usr/bin/env bash
# make-a-deck PHASE 2 -- structural gate wrapper for the Attractor `lint` node.
#
# Runs tools/narrative_lint.py on the rendered deck and turns its verdict into a
# machine-readable ROUTING decision for the pipeline. Both modes print EXACTLY
# ONE line of JSON on stdout; the `lint`/`reset` tool nodes ingest it via
# parse_json="true", so every key lands in shared pipeline context as a plain
# $token that later prompts (notably `render`) can read.
#
# Modes:
#   reset  -- clear the bounded-retry counter and seed neutral feedback context.
#             Runs ONCE per pipeline run (start -> reset -> research -> ...), so
#             the counter can't carry over from a previous run.
#   check  -- lint the deck, maintain a bounded retry counter, and emit:
#               route=pass     deck clean (no HARD-FAIL)        -> done
#               route=retry    HARD-FAIL, retries remain        -> render (loop back)
#               route=flagged  HARD-FAIL, retries exhausted     -> flagged -> done
#             plus lint_feedback = the failing HARD-check names + details, so the
#             render node can fix EXACTLY those issues on loop-back.
#
# Bound: MAX_RETRIES loop-backs (1 initial lint + MAX_RETRIES re-renders). After
# that the gate emits route=flagged instead of spinning.
#
# All paths are ABSOLUTE: the tool node's cwd is not guaranteed to be the repo
# root, so we mirror the literal deck path baked into the render prompt.
set -u

REPO="/home/ramparte/dev/ANext/amplifier-stories"
DECK="$REPO/ai_working/pipeline-test/deck.html"
COUNTER="$REPO/ai_working/pipeline-test/.lint_attempts"
LINT_OUT="$REPO/ai_working/pipeline-test/.lint_result.json"
MAX_RETRIES=3
MODE="${1:-check}"

if [ "$MODE" = "reset" ]; then
    rm -f "$COUNTER" "$LINT_OUT"
    # PHASE 3: also clear BOTH fact-check gate counters, verdict files, AND the
    # per-run artifact files (research.json, research_verified.json, spine.json,
    # deck_flags.txt, ...) so neither a stale FACT nor a stale VERDICT can leak in
    # from a previous run. reset runs ONCE per run (start -> reset -> ...).
    bash "$REPO/pipelines/factcheck_gate.sh" reset
    printf '%s\n' '{"route": "start", "lint_hard_fail": "", "lint_attempt": 0, "lint_feedback": "(first attempt: no prior lint feedback)", "research_flags": "(first pass: no prior fact-check flags)", "deck_flags": "(first pass: no prior deck fact-check flags)"}'
    exit 0
fi

# check mode: lint the deck (write machine-readable JSON; never let the linter's
# non-zero HARD-FAIL exit code abort this gate -- routing is decided below).
python3 "$REPO/tools/narrative_lint.py" --json "$LINT_OUT" "$DECK" >/dev/null 2>&1 || true

MAX_RETRIES="$MAX_RETRIES" COUNTER="$COUNTER" LINT_OUT="$LINT_OUT" python3 <<'PY'
import json
import os

lint_out = os.environ["LINT_OUT"]
counter = os.environ["COUNTER"]
max_retries = int(os.environ["MAX_RETRIES"])

HARD_CHECKS = (
    "spine_present",
    "beat_markers",
    "beat_slide_parity",
    "frame_first",
    "proof_early",
    "payoff_present",
    "sources_slide",
)

hard_fail = True
feedback = "linter produced no result"
try:
    with open(lint_out, encoding="utf-8") as fh:
        results = json.load(fh)
    r = results[0] if isinstance(results, list) and results else {}
    hard_fail = bool(r.get("hard_fail", True))
    checks = r.get("checks", {})
    failed = [
        f"{name}: {checks[name].get('detail', '').strip()}"
        for name in HARD_CHECKS
        if checks.get(name, {}).get("status") == "fail"
    ]
    feedback = " | ".join(failed) if failed else "(no failing HARD checks)"
except Exception as exc:  # noqa: BLE001
    feedback = f"could not read lint result: {exc}"

# Bounded retry counter: number of lint runs so far this pipeline run.
attempts = 0
try:
    with open(counter, encoding="utf-8") as fh:
        attempts = int(fh.read().strip() or "0")
except Exception:
    attempts = 0
attempts += 1
try:
    with open(counter, "w", encoding="utf-8") as fh:
        fh.write(str(attempts))
except Exception:
    pass

if not hard_fail:
    route = "pass"
elif attempts > max_retries:
    route = "flagged"
else:
    route = "retry"

print(
    json.dumps(
        {
            "route": route,
            "lint_hard_fail": "true" if hard_fail else "false",
            "lint_attempt": attempts,
            "lint_feedback": feedback,
        }
    )
)
PY
