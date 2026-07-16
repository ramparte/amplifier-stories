#!/usr/bin/env bash
# make-a-deck PHASE 3 -- deterministic router + bounded-retry counter for the two
# ISOLATED fact-check gates (research_factcheck + deck_factcheck).
#
# WHY THIS EXISTS (backend reality): in this loop-pipeline backend, LLM (box)
# nodes return PROSE -- their report_outcome/context_updates are NOT captured
# (verified: research/spine/render all land as "Plain text response",
# context_updates=None), and `$token` prompt-expansion only ever sees keys that a
# TOOL node put into context. So an LLM node canNOT reliably (a) hand a big
# artifact to a downstream node via context, nor (b) carry a routing decision.
# Only TOOL nodes (parse_json) reliably write context. Therefore each fact-check
# gate is split, exactly like the render->lint(gate) pair already in this graph:
#   * an ISOLATED LLM checker (fidelity=truncate) that READS the artifact from a
#     fixed file, re-derives the facts, WRITES its findings to files, and writes
#     its one-word verdict (pass|fail) to a verdict file; then
#   * a tiny TOOL router (this script) that READS that verdict file, applies the
#     bounded-retry counter, and emits the routing key via parse_json.
# This keeps data hand-off and routing DETERMINISTIC instead of hoping an LLM
# emits exact JSON as its final message.
#
# Routing keys are DISTINCT from the lint gate's `route`: this script emits
# `rfc_route` (research gate) / `dfc_route` (deck gate), each in {pass|fail|
# flagged}. A `pass` verdict routes on; a `fail` consumes one unit of retry
# budget and routes back to re-gather/re-render; once the budget (MAX_RETRIES) is
# spent a still-failing gate routes to `flagged` instead of spinning. The engine
# max_steps guard is the ultimate backstop.
#
# Modes (all paths ABSOLUTE; node cwd is not guaranteed to be the repo root):
#   reset      -- clear BOTH gate counters + verdict files + the per-run artifact
#                 files, so nothing (stale facts OR stale verdicts) leaks across
#                 runs. Called once per run (from lint_gate.sh reset).
#   rfc | dfc  -- read ai_working/pipeline-test/.<g>_verdict, apply the counter,
#                 print ONE line of JSON: {"<g>_route": "...", "<g>_attempt": N}.
set -u

REPO="/home/ramparte/dev/ANext/amplifier-stories"
DIR="$REPO/ai_working/pipeline-test"
MAX_RETRIES=2
MODE="${1:-}"

if [ "$MODE" = "reset" ]; then
    rm -f "$DIR/.rfc_attempts" "$DIR/.dfc_attempts" \
          "$DIR/.rfc_verdict"  "$DIR/.dfc_verdict" \
          "$DIR/research.json" "$DIR/research_verified.json" \
          "$DIR/research_flags.txt" "$DIR/spine.json" "$DIR/deck_flags.txt"
    exit 0
fi

if [ "$MODE" != "rfc" ] && [ "$MODE" != "dfc" ]; then
    printf '%s\n' '{"error": "usage: factcheck_gate.sh <reset|rfc|dfc>"}'
    exit 0
fi

mkdir -p "$DIR"
COUNTER="$DIR/.${MODE}_attempts"
VERDICT_FILE="$DIR/.${MODE}_verdict"
# The gate also carries the checker's flags forward into context so the node it
# loops back to (research on rfc, render on dfc) can read them as a $token.
if [ "$MODE" = "rfc" ]; then
    FLAGS_FILE="$DIR/research_flags.txt"; FLAGS_KEY="research_flags"
else
    FLAGS_FILE="$DIR/deck_flags.txt";     FLAGS_KEY="deck_flags"
fi

# Read the checker's verdict. Missing/garbled verdict == fail (fail-safe: an
# unproven artifact must not sail through just because the checker forgot to
# write). Decide retry vs. flagged with the bounded counter.
MODE="$MODE" COUNTER="$COUNTER" VERDICT_FILE="$VERDICT_FILE" \
FLAGS_FILE="$FLAGS_FILE" FLAGS_KEY="$FLAGS_KEY" MAX_RETRIES="$MAX_RETRIES" \
python3 <<'PY'
import json
import os

mode = os.environ["MODE"]
counter = os.environ["COUNTER"]
verdict_file = os.environ["VERDICT_FILE"]
flags_file = os.environ["FLAGS_FILE"]
flags_key = os.environ["FLAGS_KEY"]
max_retries = int(os.environ["MAX_RETRIES"])

verdict = "fail"
try:
    with open(verdict_file, encoding="utf-8") as fh:
        raw = fh.read().strip().lower()
    verdict = "pass" if "pass" in raw and "fail" not in raw else ("pass" if raw == "pass" else "fail")
except Exception:
    verdict = "fail"

try:
    with open(flags_file, encoding="utf-8") as fh:
        flags = fh.read().strip() or "(none)"
except Exception:
    flags = "(no flags file written by checker)"
# Keep the token compact so it can't blow up a downstream prompt.
flags = flags[:4000]

attempts = 0
try:
    with open(counter, encoding="utf-8") as fh:
        attempts = int(fh.read().strip() or "0")
except Exception:
    attempts = 0

if verdict == "pass":
    route = "pass"  # a pass does not consume retry budget
else:
    attempts += 1
    try:
        with open(counter, "w", encoding="utf-8") as fh:
            fh.write(str(attempts))
    except Exception:
        pass
    route = "flagged" if attempts > max_retries else "fail"

print(json.dumps({
    f"{mode}_route": route,
    f"{mode}_attempt": attempts,
    flags_key: flags,
}))
PY
