# make-a-deck — Attractor deck pipeline

Phase 3: an Attractor pipeline that turns a topic into a narrative HTML deck,
puts it through an **automated structural gate** (`tools/narrative_lint.py`) with
a **bounded loop-back to `render`**, AND wraps the generation in **two
independent, FULLY-ISOLATED fact-check gates** so we never build a narrative on a
hallucinated fact and never ship a deck whose claims aren't supported.

```
start → reset → research → research_factcheck → rfc_gate → spine → render → lint → deck_factcheck → dfc_gate → done
                                                  ├ pass ─→ spine                     ├ pass ─→ deck_factcheck        ├ pass ─→ done
                                                  ├ fail ─→ research (re-gather ≤2×)   ├ retry ─→ render (≤3×)          ├ fail ─→ render (fix ≤2×)
                                                  └ flagged ─→ flagged (FAIL)          └ flagged ─→ flagged (FAIL)     └ flagged ─→ flagged (FAIL)
```

## Phase 3: two isolated fact-check gates

Each `*_factcheck` node runs with **`fidelity="truncate"`** → a **fresh, isolated
session** whose preamble is *only* the graph goal + run id (see the Attractor
`fidelity.py` `_build_truncate_preamble`). It therefore has **no conversational
knowledge** of how the research/spine/render turns were produced. It re-derives
every fact from ground truth and sees **only the specific artifact file** we tell
it to read.

### Why files (not `$token`/`report_outcome`)

In this backend, **LLM (box) nodes return prose** — their `report_outcome` /
`context_updates` are **not** captured (verified: phase-2 `research`/`spine`/
`render` all log as `Plain text response`, `context_updates=None`), and `$token`
prompt-expansion only resolves keys a **tool node** put into context. So an LLM
node can neither hand a big artifact to a downstream node via context **nor**
carry a routing verdict. We therefore hand artifacts between nodes as **files at
fixed absolute paths** (under `ai_working/pipeline-test/`), and split each
fact-check gate — exactly like the existing `render → lint(gate)` pair — into:

1. an **isolated LLM checker** (`fidelity="truncate"`) that reads the artifact
   file, re-derives the facts, and writes back its findings + a **one-word verdict
   file** (`.rfc_verdict` / `.dfc_verdict`, `pass`|`fail`); and
2. a tiny **tool router** (`parallelogram`, `parse_json`) that reads the verdict
   file, applies the **bounded-retry counter** (`pipelines/factcheck_gate.sh`),
   and emits the routing key into context **deterministically**.

**Artifact files** (all cleared each run by `reset`): `research.json`
(research→checker), `research_verified.json` (checker→spine/render/deck-gate),
`research_flags.txt` + `.rfc_verdict` (checker→`rfc_gate`), `spine.json`
(spine→render), `deck.html` (render→lint/deck-gate), `deck_flags.txt` +
`.dfc_verdict` (checker→`dfc_gate`).

**Routing keys don't collide:** `lint` uses `route`; the fact-check gates use
`rfc_route` and `dfc_route` (emitted by their tool routers). The `$token`s that
actually expand are the ones a tool node populates: `$lint_feedback` (lint),
`$research_flags` (`rfc_gate`/reset seed), `$deck_flags` (`dfc_gate`/reset seed).
On a `fail` a gate consumes one unit of retry budget and loops back; once the
budget is spent a still-failing gate emits `flagged` (≤2 loop-backs) instead of
spinning. `reset` clears all three counters + artifacts once per run.

- **reset** — (tool node) clears **all three** bounded-retry counters (lint + both
  fact-check gates), the verdict files, and the per-run artifact files, and seeds
  neutral `$lint_feedback` / `$research_flags` / `$deck_flags`. Runs **once** per
  run (not on any loop), so nothing (stale fact or verdict) leaks between runs.
- **research** — gathers VERIFIED facts (git/gh/grep/read) and **writes
  `research.json`**; on a re-gather loop it reads `$research_flags` to fix exactly
  the claims the fact-checker flagged.
- **research_factcheck** — (isolated, `fidelity="truncate"`) reads `research.json`,
  re-verifies every claim against ground truth, and writes `research_verified.json`
  (bad claims removed/corrected), `research_flags.txt`, and `.rfc_verdict`.
- **rfc_gate** — (tool node) `factcheck_gate.sh rfc`: reads `.rfc_verdict` + the
  counter, emits `rfc_route ∈ {pass|fail|flagged}` and `$research_flags`
  (`pass`→spine, `fail`→research, `flagged`→flagged).
- **spine** — reads `research_verified.json`, writes a narrative spine per the v2
  contract in `context/storyteller-instructions.md` to `spine.json`.
- **render** — reads `research_verified.json` + `spine.json` (**and
  `$lint_feedback` / `$deck_flags` on a retry**), writes `deck.html`. Retry-aware:
  fixes exactly the failing lint checks and/or the unsupported deck claims.
- **lint** — (tool node) runs `pipelines/lint_gate.sh check`, which lints the deck
  with `narrative_lint.py --json` and emits **one line of JSON** (`parse_json`):
  `route ∈ {pass|retry|flagged}`, `lint_hard_fail`, `lint_attempt`, and
  **`lint_feedback`**. Condition edges route on `context.route`.
- **deck_factcheck** — (isolated, `fidelity="truncate"`) reads `deck.html` +
  `research_verified.json`, confirms every deck claim (incl. frame-slide framing)
  is supported by the verified research, and writes `deck_flags.txt` + `.dfc_verdict`.
- **dfc_gate** — (tool node) `factcheck_gate.sh dfc`: reads `.dfc_verdict` + the
  counter, emits `dfc_route ∈ {pass|fail|flagged}` and `$deck_flags`
  (`pass`→done, `fail`→render, `flagged`→flagged).
- **flagged** — reached when the deck still HARD-FAILs after **3** lint retries, or
  when either fact-check gate exhausts its **2** loop-backs; it exits non-zero so
  the pipeline's final outcome is **FAIL** (the human-visible flag) rather than
  spinning, then routes to `done`.

## Phase 2: the structural gate

The gate wrapper `pipelines/lint_gate.sh` (modes `reset` / `check`) exists so the
gate can do two things a bare tool node can't do at once:

1. **Carry the pass/fail verdict in a parsed context key (`route`)** instead of
   the node outcome. The lint tool node *always exits 0*; a tool node that
   returned `FAIL` would discard its stdout, and we'd lose the `lint_feedback`
   that `render` needs on loop-back. So routing is `condition="context.route=…"`,
   not `outcome=fail`.
2. **Feed the failing checks back to `render` via context** — the parsed
   **`lint_feedback`** key (a plain, dot-free token) is what `render` reads as
   `$lint_feedback` to fix exactly the checks that failed.

Bound: 1 initial lint + **3** re-renders. On the 4th still-failing lint the gate
emits `route=flagged` → the `flagged` node → `done` (FAIL). The engine's
`max_steps` guard (`nodes × 50`) is the backstop.

## Files

| File | Purpose |
|------|---------|
| `make-a-deck.dot` | The pipeline graph. The **topic is `graph[goal=...]`**; the output path is a literal absolute path in the `render` node prompt (also mirrored as `graph[output_path=...]`). |
| `lint_gate.sh` | Structural-gate wrapper (`reset`/`check`) for the `lint` node; also clears the two fact-check counters on `reset`. |
| `factcheck_gate.sh` | Bounded-retry counter for the two isolated fact-check gates (`reset`/`rfc`/`dfc`): turns each checker's semantic `pass`/`fail` verdict into a counter-bounded `rfc_route`/`dfc_route` (`pass`/`fail`/`flagged`) so a failing checker routes to `flagged` (≤2 loop-backs) instead of spinning. |
| `make-a-deck.bundle.yaml` | Overlay bundle. Includes `attractor:bundles/attractor-pipeline`, points `session.orchestrator.config.dot_file` at the `.dot`, and redeclares the `attractor-agent-anthropic` child **with an inline `loop-agent` orchestrator** (required by the recursion guard). |

## One-time setup (register bundles)

```bash
# The Attractor bundle (skip if already registered — see `amplifier bundle list`)
amplifier bundle add "file:///home/ramparte/dev/ANext/amplifier-resolve/amplifier-bundle-attractor/bundle.md"

# This pipeline's overlay bundle
amplifier bundle add "file:///home/ramparte/dev/ANext/amplifier-stories/pipelines/make-a-deck.bundle.yaml"
```

## Run

```bash
cd /home/ramparte/dev/ANext/amplifier-stories
amplifier run -B make-a-deck -v "Run the pipeline"
```

There is **no `--dot-file` / `--goal` CLI flag** in this core. The DOT is passed
via the overlay's `session.orchestrator.config.dot_file`; the goal is passed via
`graph[goal=...]` inside the DOT.

A scratch `.amplifier/settings.yaml` in this repo sets `bundle: {app: []}` so
global app bundles / superpowers / modes don't override the loop-pipeline
orchestrator. (`.amplifier/` and `ai_working/` are git-ignored.)

## Set the topic / output path

- **Topic:** edit `graph[goal="…"]` in `make-a-deck.dot`.
- **Output path:** edit the literal path in the `render` node prompt (and the
  `graph[output_path=…]` attr). Default:
  `/home/ramparte/dev/ANext/amplifier-stories/ai_working/pipeline-test/deck.html`
  (create `ai_working/pipeline-test/` first). **Never** write test decks into `docs/`.

## Verify the output

```bash
python3 tools/narrative_lint.py ai_working/pipeline-test/deck.html
# expect: ... PASS ...   (exit 0, no HARD-FAIL)
```

## Attractor gotchas locked in phase 1

1. **Recursion guard.** Each child agent the pipeline routes to MUST have an
   INLINE `session.orchestrator` (a non-pipeline one, `loop-agent`) in the
   overlay's `agents:` map. A `bundle:`-ref-only child resolves to
   `orchestrator.module=None` and trips the guard
   (`loop-pipeline recursion guard: … module=None`). See `make-a-deck.bundle.yaml`.
2. **DOT-only entrypoints.** No CLI `--dot-file`/`--goal`; pass DOT via
   `orchestrator.config.dot_file` and goal via `graph[goal=…]`.
3. **Data-flow = `report_outcome`.** Each node's child agent calls the
   `report_outcome` tool with `context_updates`; the engine merges those into
   shared context, and later node prompts read them as `$key` (plain keys, no
   dots — e.g. `$research_json`, `$spine_json`). `$goal` expands from the graph
   goal. Graph attrs land in context as `graph.<key>` (dotted → NOT expanded as
   a bare `$token`), which is why the output path is passed as a literal in the
   render prompt rather than as `$output_path`.
4. **App isolation.** Run-dir `.amplifier/settings.yaml` → `bundle: {app: []}`.
