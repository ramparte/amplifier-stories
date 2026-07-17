# make-a-deck Pipeline — Findings & Handoff

**Status:** Built through Phase 3, **NOT yet verified end-to-end.** The session
building it was terminated (cause unknown) during the Phase 3 end-to-end test.
All code is committed (`f74c70b`). This document is the honest state of things so
you can finish it.

**Last verified-good point:** Phase 1 & 2 each reported passing when built, BUT
see the **Critical Open Question** below — those "passes" may not be as solid as
reported, and need genuine re-verification, not trust.

---

## What this pipeline is

An [Attractor](../../amplifier-resolve/amplifier-bundle-attractor) DOT-graph
pipeline that turns `"make a deck about X"` into a narrative HTML deck with
automated quality + fact-check gates — hands-off and batchable.

**Target topology:**

```
start → reset → research → research_factcheck → spine → render → lint → deck_factcheck → done
                                │ pass→spine                  │pass→dfc   │pass→done
                                │ fail→research (retry ≤2)     │fail→render (retry≤3)   │fail→render (retry≤2)
                                │ flagged→flagged              │flagged→flagged         │flagged→flagged
```

Two **independent, isolated** fact-check gates (the whole reason for this build):

1. **`research_factcheck`** — verifies the *research evidence* against ground
   truth (git/gh/grep on the real repos) BEFORE the spine is built, so we never
   build a narrative on a hallucinated fact. Loops back to `research`.
2. **`deck_factcheck`** — verifies the *finished deck's* claims (including the
   frame-slide framing) against the verified research, catching render-time
   drift/embellishment. Loops back to `render`.

Both run with `fidelity="truncate"` (fresh isolated session — no knowledge of the
generation conversation), so they can't rationalize claims they didn't make.
Plus the structural `lint` gate (`narrative_lint.py`) between them.

---

## Files (all committed at `f74c70b`)

| File | Role |
|------|------|
| `pipelines/make-a-deck.dot` | The pipeline graph: nodes, prompts, edges, routing conditions. Fully wired through Phase 3. |
| `pipelines/make-a-deck.bundle.yaml` | Attractor overlay bundle: points orchestrator at the `.dot`, defines the inline-orchestrator `attractor-agent-anthropic` child (required — see gotcha #1). |
| `pipelines/lint_gate.sh` | Tool-node wrapper for the structural gate. `reset` clears ALL counters (lint + both fact-check gates); `check` runs `narrative_lint.py` and emits routing JSON with bounded retries. |
| `pipelines/factcheck_gate.sh` | Deterministic router + bounded-retry counter for BOTH fact-check gates (`rfc` / `dfc`). Reads the checker's verdict file, applies the retry budget, emits `rfc_route`/`dfc_route`. |
| `pipelines/README.md` | Register + run instructions. |
| `tools/narrative_lint.py` | Structural reviewer (spine/frame-first/proof-early/beat-parity/etc). 17 passing tests. **Unchanged** by pipeline work. |

---

## ✅ VERIFIED vs ⚠️ UNVERIFIED — read this before trusting anything

| Component | Status | Evidence |
|-----------|--------|----------|
| `narrative_lint.py` structural gate | ✅ VERIFIED | 17 pytest cases; discriminates good/bad decks; used all session. |
| `factcheck_gate.sh` routing logic | ✅ VERIFIED (this session) | Direct test: `pass→pass`; three fails → `fail, fail, flagged` (bounded, no spin); missing verdict → `fail` (fail-safe). |
| Attractor runs on spark-1 at all | ✅ VERIFIED | Smoke test: `01-simple-linear.dot` completed, spawned a real sub-session, wrote a file. Old `ModuleNotFoundError` spawn bug did NOT recur. |
| Phase 1 linear run (research→spine→render) | ⚠️ REPORTED-PASS, NOT RE-CONFIRMED | Sub-agent said it produced a linter-passing deck — but see Critical Open Question. |
| Phase 2 lint gate + loop-back | ⚠️ REPORTED-PASS, NOT RE-CONFIRMED | Sub-agent claimed loop fired+recovered via a throwaway forced-failure. Not independently reproduced. |
| Phase 3 fact-check gates end-to-end | ❌ NEVER TESTED | Session terminated during this exact test. No run has ever exercised the fact-check nodes. |

---

## 🚨 Critical Open Question — resolve this FIRST

**Do LLM (box) nodes actually pass data to later nodes via context, or not?**
There is a **direct contradiction** in the build history:

- **Phase 1 reported:** `research_json` → `$research_json` → `spine_json` →
  `$spine_json` "all flowed through" via `report_outcome` `context_updates`.
- **Phase 3 discovered (and left in `factcheck_gate.sh` comments):** in this
  loop-pipeline backend, LLM nodes return **prose**; their
  `report_outcome`/`context_updates` are **NOT captured** (`context_updates=None`
  — "verified: research/spine/render all land as 'Plain text response'"). Only
  **tool nodes** (`parse_json`) reliably write context.

Both cannot be true. The likely explanation: each node produced coherent output
from its **own prompt + the graph goal**, so the deck looked right even if the
artifacts never actually flowed between nodes. If so, the whole "research →
verified facts → spine → deck" data hand-off is an illusion, and the pipeline is
really N independent nodes each re-deriving from the goal — which **defeats the
fact-check design** (the deck checker needs the *actual* verified research, not a
re-derivation).

**This is why Phase 3 introduced the file-based pattern:** the isolated LLM
checker WRITES its verdict + findings to fixed files under
`ai_working/pipeline-test/`, and the tool router (`factcheck_gate.sh`) READS
those files. That's the reliable hand-off mechanism. **The open work is to make
research → spine → render use the same file-based hand-off** (each stage writes
its artifact to a known file; the next stage reads it), rather than relying on
`$token` context expansion between LLM nodes that may not populate.

**First task on resume:** run one tiny 2-node test — LLM node A emits
`context_updates={foo: "bar"}`, node B's prompt contains `$foo` — and see whether
B actually receives `bar`. That single test tells you whether the elegant
context-passing works or whether everything must go through files. Everything
downstream depends on this answer.

---

## How to run it (exact, verified commands)

```bash
# One-time: register the Attractor bundle (local repo)
amplifier bundle add "file:///home/ramparte/dev/ANext/amplifier-resolve/amplifier-bundle-attractor/bundle.md"

# Register / refresh the make-a-deck overlay (re-run `remove` then `add` after editing the .dot or bundle.yaml)
amplifier bundle add "file:///home/ramparte/dev/ANext/amplifier-stories/pipelines/make-a-deck.bundle.yaml"

# Run (goal/topic comes from graph[goal=...] in the .dot — no --goal/--dot-file flags exist in this core)
cd /home/ramparte/dev/ANext/amplifier-stories
amplifier run -B make-a-deck -v "Run the pipeline"
```

- Output deck path is currently a **literal** in the render prompt:
  `ai_working/pipeline-test/deck.html` (gitignored scratch — NOT `docs/`).
- To change the topic, edit `graph[goal="..."]` in `make-a-deck.dot`.
- Requires `ANTHROPIC_API_KEY` in env.

**Safer run harness (recommended given the termination):** don't run the full
pipeline inside a long-lived agent turn. Run it via bash in the background with a
log file, so a session drop doesn't lose the run or its output:
```bash
cd /home/ramparte/dev/ANext/amplifier-stories
nohup amplifier run -B make-a-deck -v "Run the pipeline" > ai_working/pipeline-test/run.log 2>&1 &
# then tail ai_working/pipeline-test/run.log
```

---

## Attractor setup gotchas (learned this session — save yourself the pain)

1. **Recursion guard:** every child agent you route to MUST have an *inline*
   `session.orchestrator: {module: loop-agent, source: git+…#subdirectory=modules/loop-agent, config: {...}}`
   in the overlay's `agents:` map. Bundle-ref-only children resolve to
   `orchestrator.module=None` and trip the guard, killing the node. If you add an
   OpenAI/Gemini child for stylesheet routing, it needs the same inline block.
2. **No `--dot-file` / `--goal` CLI flags** in this core (2026.07.13 / core
   1.6.0). DOT goes in `session.orchestrator.config.dot_file`; goal in
   `graph[goal=...]`.
3. **`-B` needs a registered bundle NAME**, not a path. `bundle add` first;
   re-add (remove+add) after every edit to the `.dot` or bundle yaml.
4. **Keep app bundles out:** the run dir has `.amplifier/settings.yaml` with
   `bundle: {app: []}` so global app bundles / superpowers don't override the
   `loop-pipeline` orchestrator with `loop-streaming`.
5. **Tool nodes swallow stdout on FAIL:** a `parallelogram` node returning
   non-zero discards its stdout in the loop-pipeline handler — you lose the
   feedback. Pattern used here: the gate node **always exits 0** and carries the
   verdict in a parsed JSON key (`route` / `rfc_route` / `dfc_route`); edges route
   on `condition="context.<key>=..."`.
6. **Routing keys must be distinct per gate** so conditions don't collide: lint
   uses `route`, research gate uses `rfc_route`, deck gate uses `dfc_route`.
7. **Bounded retries:** counters live in the two `*_gate.sh` scripts (files under
   `ai_working/pipeline-test/`), reset once per run by the `reset` node. The
   engine `max_steps` guard is the backstop so nothing spins.
8. **Modules run from the published `@main` git checkout**, not the local
   attractor repo copy — local edits under `modules/` won't take effect unless
   you repoint `source:` to a local path.

---

## Recommended finish sequence

1. **Resolve the Critical Open Question** (the 2-node context test above). This
   decides the whole data-flow approach.
2. If context-passing between LLM nodes does NOT work: convert research → spine →
   render to the **file-based hand-off** (each writes its artifact to a fixed
   file; the next reads it). The fact-check nodes already use this pattern.
3. **Run the full pipeline once** with the background harness; confirm the happy
   path completes: `research → research_factcheck(pass) → spine → render →
   lint(pass) → deck_factcheck(pass) → done`, and the deck passes
   `narrative_lint.py`.
4. **Prove each gate is real** with planted falsehoods: inject a fake metric into
   the research artifact → confirm `research_factcheck` flags it and loops back;
   inject an unsupported claim into the deck → confirm `deck_factcheck` flags it
   and loops back. Confirm the checkers ran isolated (no knowledge of generation).
5. **Then** wire topic as a real parameter (not a hardcoded goal) and consider a
   batch mode for regenerating the existing corpus through the full gated pipeline.

---

## Unrelated repo notes (leave alone)

- `docs/amplifier-capability-survey-briefing.html` — untracked; user is actively
  using it. Do NOT overwrite/commit.
- `kevin/` — untracked; not part of this work. Leave alone. (`.gitignore` has an
  uncommitted `kevin/.corpus/` line — harmless hygiene; commit or drop as you see
  fit.)
- The 197-deck corpus regeneration + contract-v2 (frame-first) rewrites of the
  10 pilot decks are all committed and separate from this pipeline work. Nothing
  here has been pushed to `origin`.
