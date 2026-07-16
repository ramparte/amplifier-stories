# make-a-deck — Attractor deck pipeline

Phase 2: an Attractor pipeline that turns a topic into a narrative HTML deck and
then puts it through an **automated structural gate** (`tools/narrative_lint.py`)
with a **bounded loop-back to `render`** when the deck HARD-FAILs.

```
start → reset → research → spine → render → lint
                                              ├─ pass ───────→ done
                                              ├─ retry ──────→ render   (loop back, ≤3×)
                                              └─ flagged ────→ flagged → done  (FAIL)
```

- **reset** — (tool node) clears the bounded-retry counter and seeds a neutral
  `$lint_feedback` so the first `render` sees empty feedback. Runs **once** per
  run (it is not on the loop), so the counter can't leak between runs.
- **research** — gathers VERIFIED facts about the topic (git/gh/grep/read), emits
  context key `research_json`.
- **spine** — reads `$research_json`, writes a narrative spine per the v2 contract
  in `context/storyteller-instructions.md`, emits `spine_json`.
- **render** — reads `$research_json` + `$spine_json` (**and `$lint_feedback` on a
  retry**), writes a self-contained HTML deck to the output path. Its prompt is
  retry-aware: if `$lint_feedback` lists failing checks it rewrites the deck to
  fix exactly those.
- **lint** — (tool node) runs `pipelines/lint_gate.sh check`, which lints the deck
  with `narrative_lint.py --json` and emits **one line of JSON** (`parse_json`
  merges it into context): `route ∈ {pass|retry|flagged}`, `lint_hard_fail`,
  `lint_attempt`, and **`lint_feedback`** (the failing HARD-check names+details).
  Condition edges route on `context.route`.
- **flagged** — reached only when the deck still HARD-FAILs after **3** retries;
  it exits non-zero so the pipeline's final outcome is **FAIL** (the human-visible
  flag) rather than spinning, then routes to `done`.

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
