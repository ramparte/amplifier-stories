# Context Rot is a Systems Problem: How Amplifier's Architecture Keeps AI Sharp

---

You know the feeling. Ninety minutes into a coding session with your AI assistant, things start to slip. The model that was writing crisp, well-structured code at the start of the session is now hallucinating imports, forgetting your project conventions, and contradicting decisions it made twenty minutes ago. You are watching your AI assistant get dumber in real time.

This is context rot -- the progressive degradation of AI quality as a session's context window fills up. Every file the model reads, every error message it processes, every conversation turn it accumulates pushes older, more important information further from the model's attention. The instructions you gave at the start of the session are now buried under thousands of tokens of intermediate work product. The model is drowning in its own history.

The problem is well-known enough to have spawned an entire category of tooling. Projects like GSD (50k+ GitHub stars) market themselves primarily as solutions to this exact issue. And the solutions they offer are real -- better prompt hygiene, smarter context pruning, periodic session resets. These approaches work, to a point.

But they are solving the problem at the wrong layer.

## The Prompt-Engineering Band-Aid

Most approaches to context rot treat it as a prompting problem. The reasoning goes: if the context window is getting polluted, clean it up. Compress old messages. Summarize intermediate work. Restart sessions periodically. Write better system prompts that resist degradation.

These are reasonable tactics. They are also fundamentally limited, for the same reason that telling a developer "just write cleaner code" does not eliminate bugs. Discipline-based solutions require constant vigilance and degrade under pressure -- exactly when you need them most.

Consider what happens during a real development session. You ask the AI to implement an authentication module. It reads the existing codebase (8 files, ~15,000 tokens). It examines the test framework (3 files, ~4,000 tokens). It writes implementation code, encounters an error, reads the stack trace, tries a different approach, reads documentation, revises. Each of these steps is individually reasonable. Collectively, they have consumed 80% of the context window, and the model has not finished the task yet.

No amount of prompt engineering prevents this. The work itself generates context. The question is not how to prevent context accumulation -- it is where to put it.

## The Architectural Insight

Amplifier treats context rot as a systems architecture problem. Instead of trying to keep a single context window clean through discipline, it structures work so that context accumulation is physically isolated from the session that needs to stay sharp.

The core insight: **a context window should be used for working, not for remembering.** State belongs in files. Exploration belongs in disposable sub-sessions. The primary session should contain only what it needs to make its next decision.

This is not a single feature. It is a set of reinforcing architectural patterns that, taken together, make context rot structurally difficult rather than merely discouraged.

---

## Pattern 1: The Context Sink

The most direct attack on context rot is delegation with context isolation.

When an Amplifier session needs to explore a codebase, it does not read 20 files into its own context. It delegates to a sub-agent with `context_depth: "none"` -- a fresh session with an empty context window. The sub-agent does the heavy reading, processes the results, and returns a compact summary. The parent session sees only that summary.

```python
# Parent session: "I need to understand the auth module"
# Cost to parent context: ~200 tokens (the summary)
# Cost if done directly: ~20,000 tokens (reading all the files)

delegate(
    agent="foundation:explorer",
    instruction="Survey the auth module. What are the key interfaces, "
                "data flows, and integration points?",
    context_depth="none"  # Fresh session. No inherited context.
)
```

The sub-agent's context window fills up with file contents, type signatures, and implementation details. That is fine -- it was born to do this one task and will be discarded when it is done. The parent session receives a 200-token summary and moves on with 98% of its context budget intact.

This is the **context sink** pattern: sub-agents absorb the token cost of exploration in their own context window, not the parent's. The name is borrowed from heat sinks in hardware -- a component whose job is to absorb and dissipate what would otherwise damage the primary system.

The Amplifier architecture documentation captures the economics precisely:

```
WITHOUT context sink:
+-------------------------------------+
| Main Session                        |
| - Load full data (10,000 tokens)    |
| - Search and filter (2,000 tokens)  |
| - Format results (1,000 tokens)     |
| ------------------------------------+
| Total: 13,000 tokens consumed       |
+-------------------------------------+

WITH context sink:
+-------------------------------------+
| Main Session                        |
| - Delegate to sub-agent             |
| - Receive summary (200 tokens)      |
| ------------------------------------+
| Total: 200 tokens consumed          |
+-------------------------------------+
        |
        v
+-------------------------------------+
| Sub-Agent (disposable)              |
| - Load full data (10,000 tokens)    |
| - Search and filter (2,000 tokens)  |
| - Summarize for parent (1,000 tok)  |
| ------------------------------------+
| Total: 13,000 tokens (isolated)     |
| (doesn't affect parent)             |
+-------------------------------------+
```

Token savings in the parent: 98%. And those savings compound. Over a session that requires five such explorations, the parent has consumed ~1,000 tokens instead of ~65,000.

## Pattern 2: Fresh Sessions by Default

The context sink pattern works because of a deeper architectural commitment: **every delegated task gets a fresh context window.**

When an Amplifier orchestrator dispatches work to a sub-agent, the default is `context_depth: "none"`. The sub-agent starts clean. It does not inherit the orchestrator's conversation history, its accumulated file reads, or its prior reasoning. It receives only a task specification -- a self-contained description of what to do.

```yaml
# From a real recipe: every working session starts fresh
steps:
  - id: "working-session"
    type: "agent"
    agent: "foundation:zen-architect"
    context_depth: "none"    # Born clean. Dies clean.
    prompt: |
      Execute this task. Read STATE.yaml for current project state.
      Read CONTEXT-TRANSFER.md for recent decisions.
      Your spec is at: specs/features/F-042-auth-middleware.md
```

This is a design doctrine, not a default that developers override: **no session runs long enough to degrade.** Each unit of work -- implement a feature, review a change, run a diagnostic -- gets its own agent with its own context budget. When the work is done, that context is discarded.

The working session instructions make this explicit:

> *"You are a stateless agent. Everything you need to know is in the files. You were spawned to do a bounded unit of work. You start with zero context from previous sessions."*

This inverts the typical AI coding workflow. Instead of one long session that accumulates context until it degrades, you get a series of short, sharp sessions that each start at peak capability.

## Pattern 3: State Lives in Files, Not in the Window

Fresh sessions only work if state is persisted somewhere durable. Amplifier uses the filesystem.

Every project managed by Amplifier's development machine maintains two critical files:

**STATE.yaml** -- the single source of truth for project status:

```yaml
project: safeguard
phase: 10
phase_name: "Phase 10-13: Production Readiness"
epoch: 4240
next_action: "F-939 (shadow AI honeypot), then F-940, F-942"
blockers: []

features:
  F-939-shadow-ai-honeypot:
    status: "ready"
    spec: "specs/features/security/F-939-shadow-ai-honeypot.md"
    depends_on: ["F-937"]
```

**CONTEXT-TRANSFER.md** -- institutional memory across sessions:

```markdown
# Context Transfer: safeguard Development Machine
> Updated at the end of every working session.
> Read this at the start of every session. No exceptions.

## Architecture Overview
Three-layer system:
1. Gateway (Data Plane): Fast, deterministic API proxy...
2. Management Plane: Conversational admin interface...
3. DNS Backstop: Network-level blocking...

## Key Constraints
- Sub-50ms latency: No LLM in the gateway hot path.
- Async event writes: Logging must not block requests.

## Lessons Learned
**Pattern**: Missing null checks on optional policy fields
**Seen**: 4 times across sessions
**Prevention**: Always destructure with defaults for optional fields.
```

The context window is ephemeral. Files are permanent. Each new session reads these files to orient itself -- a fast, bounded operation that consumes maybe 2,000 tokens -- and then has a full, clean context window for actual work.

This is the separation of concerns: **the context window is for working, files are for remembering.** A human developer does not keep their entire project history in working memory. They check the ticket, read the relevant code, and focus. Amplifier's agents work the same way.

## Pattern 4: The Thin Orchestrator

The pattern that ties it all together is the orchestrator -- a coordinating agent that dispatches work but never does it directly.

In Amplifier's self-driving architecture, the orchestrator follows a strict doctrine: **it never reads code, writes code, runs tests, or debugs.** All of that is delegated to workers with clean context. The orchestrator's job is to read state, decide what to do next, dispatch a worker, evaluate the result, and update state.

```
Orchestrator (lean, ~30-40% context utilization)
  |
  +-- Worker (implement task A)     <- context_depth: none
  |     returns: summary + artifacts
  |
  +-- Reviewer (validate task A)    <- context_depth: none
  |     returns: pass/fail + evidence
  |
  +-- Worker (implement task B)     <- context_depth: none
  |     returns: summary + artifacts
  |
  +-- Reviewer (validate task B)    <- context_depth: none
        returns: pass/fail + evidence
```

The orchestrator stays lean because heavy work happens elsewhere. Workers absorb the token cost of reading code and writing implementations. Reviewers -- spawned with `context_depth: "none"` and given only the task spec and the worker's output -- provide genuine adversarial review because they have no shared context to bias them.

When context pressure does build on the orchestrator, it has one more escape valve: self-spawning. The orchestrator delegates to a copy of itself, passing the current state summary. The child continues the work. The parent receives a summary and either continues or writes a handoff file and terminates, letting the system restart fresh.

```python
# Orchestrator self-spawn under context pressure
delegate(
    agent="self",
    instruction="Continue orchestration. Current state: {state_summary}",
    context_depth="all",
    context_scope="full"
)
```

The design documentation calls out thin awareness pointers as the mechanism: the orchestrator's context contains ~25-line summaries that say "this capability exists, delegate to agent X." Heavy documentation lives in agent context sinks, never in the orchestrator.

## Pattern 5: Model Routing

Context rot is compounded when you use the wrong model for a task. A reasoning model processing boilerplate file operations wastes both tokens and attention. A fast model attempting complex architectural decisions produces low-quality output that requires correction -- which generates more context.

Amplifier's routing layer assigns tasks to the right model class:

| Role | Model Tier | Example Tasks |
|------|-----------|---------------|
| `fast` | Lightweight | File parsing, classification, bulk operations |
| `coding` | Code-specialized | Implementation, debugging, refactoring |
| `reasoning` | Deep reasoning | Architecture decisions, complex analysis |
| `critique` | Analytical | Code review, finding flaws in existing work |
| `writing` | Long-form | Documentation, case studies, content |
| `research` | Investigation | Multi-source synthesis, deep exploration |
| `security-audit` | Specialized | Vulnerability assessment, attack surface analysis |

This is a 13-role routing matrix. No single model tries to do everything. A classification task that a fast model handles in 500 tokens does not need to consume context in a reasoning model's window. An architectural decision gets the full attention of a model optimized for that work, unburdened by irrelevant prior context.

## Pattern 6: Recipes -- Workflows That Outlive Sessions

For multi-step development workflows, Amplifier provides recipes: declarative YAML specifications where each step is a fresh agent invocation with automatic state persistence between steps.

```yaml
# Each iteration of the development machine loop
name: "safeguard-session-iteration"
steps:
  - id: "orient"
    type: "bash"
    command: "python3 read_state.py"   # Read STATE.yaml

  - id: "working-session"
    type: "agent"
    context_depth: "none"              # Fresh agent
    prompt: "Read state, implement next feature, persist results."

  - id: "structural-gate"
    type: "bash"
    command: "pytest && pyright"        # Must pass to continue

  - id: "post-session"
    type: "bash"
    command: "python3 archive_and_check.py"  # Update state files
```

Each step runs in isolation. The orient step reads state from disk. The working session gets a fresh context window to do actual development. The structural gate verifies the output with deterministic tools. The post-session step archives results.

Recipes are resumable -- if the system crashes or is interrupted, it picks up from the last completed checkpoint. The state is in the recipe's checkpoint files and the project's STATE.yaml, not in any context window. You can stop a 50-step workflow at step 23, come back three days later, and resume at step 24 with zero context loss.

---

## The Compound Effect

None of these patterns is individually revolutionary. Context isolation is a known technique. File-based state is as old as computing. Delegation is a standard architectural pattern.

What matters is the compound effect. When every layer of the system is designed to prevent context accumulation in long-lived sessions, you get qualitative behavior change:

- The orchestrator that ran for 4,240 epochs on a real project (safeguard) maintained consistent quality because it never accumulated the context of any individual task.
- Adversarial reviewers that evaluated code "cold" -- with no shared context from the implementation session -- consistently found issues that in-context review missed.
- Working sessions that started fresh from STATE.yaml and CONTEXT-TRANSFER.md made decisions as good in session 200 as in session 1.

The safeguard project shipped hundreds of features across thousands of autonomous sessions. Each session read a 50-line state file and a few hundred lines of context transfer notes. Each session had nearly its entire context window available for the actual work.

## Prompt-Level vs. Architecture-Level Solutions

| Dimension | Prompt-Level | Architecture-Level (Amplifier) |
|-----------|-------------|-------------------------------|
| **Mechanism** | Compress/prune context within one session | Distribute work across isolated sessions |
| **State management** | In the context window | In files on disk (STATE.yaml, CONTEXT-TRANSFER.md) |
| **Exploration cost** | Borne by the primary session | Absorbed by disposable sub-agents |
| **Session lifetime** | Long, with periodic cleanup | Short by design; fresh starts are the norm |
| **Failure mode** | Gradual degradation as window fills | Hard boundaries; each session either works or does not |
| **Scalability** | Bounded by one model's context window | Bounded by disk space and orchestration depth |
| **Discipline required** | High (user must manage context) | Low (architecture enforces isolation) |
| **Review quality** | Reviewer shares implementer's context biases | Reviewer starts cold with no shared context |
| **Resumability** | Restart means starting over | Checkpoint files preserve progress across any interruption |

## The Deeper Point

Context rot is real, and it matters. As AI-assisted development moves toward longer-running, more autonomous workflows, the degradation of AI quality over time becomes a structural bottleneck, not a minor annoyance.

The industry's instinct has been to solve this at the model layer (bigger context windows) or the prompt layer (better context management). These help. But they do not address the fundamental issue: a single, long-running context window is the wrong abstraction for sustained work.

The right abstraction borrows from decades of systems engineering: isolated processes with explicit state passing. Short-lived workers with well-defined inputs and outputs. Orchestrators that coordinate without accumulating. State that lives in durable storage, not in volatile memory.

Amplifier did not invent these ideas. It applied them to a new domain. And the result is an AI development system that stays sharp not because someone remembered to clean up the context, but because the architecture makes it structurally difficult for context to rot in the first place.

Context management is a systems problem. It deserves a systems solution.

---

*Amplifier is an open-source AI agent framework from Microsoft. The patterns described in this article are implemented across the [amplifier-foundation](https://github.com/microsoft/amplifier-foundation), [amplifier-bundle-dev-machine](https://github.com/microsoft/amplifier-bundle-dev-machine), and [amplifier-bundle-self-driving](https://github.com/microsoft/amplifier-bundle-self-driving) repositories.*