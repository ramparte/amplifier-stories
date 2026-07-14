# Story Narrative Spine Design

## Goal

Make amplifier-stories decks read as compelling **narratives** with a clear
throughline, instead of a "bag of random slides" — polished-but-disjointed
feature catalogs.

The trigger: even the better decks (e.g. `docs/the-foundry-and-the-machine.html`)
are superficially good but not compelling. The problem is structural, not
cosmetic. Root cause: `context/storyteller-instructions.md` (~412 lines) is
**all** slide-types plus visual/accuracy checklists with **zero** narrative
guidance. The generator therefore optimizes for *pretty* and *true* — but nobody
ever told it to be *compelling*.

## Chosen Approach (and rejected alternatives)

**Chosen:** A spine-first narrative contract added to the existing storyteller
generation guidance, enforced by the generator's instructions, with a
human-in-the-loop review only.

**Rejected — Approach A: full Attractor DOT-graph pipeline.** An orchestrated
pipeline with an independent automated critic node and bounded retry loops.
Rejected as massively over-engineered for the need.

**Deferred — Approach B: separate narrative-architect agent.** A dedicated agent
that designs the spine before handing off to the generator. Deferred as YAGNI.

The automated critic, the Attractor pipeline, and a batch "rewrite every story"
capability are all explicitly **deferred** to a possible future iteration. This
design is a deliberately simplified prototype.

## Design — three contracts

The narrative discipline is expressed as three nested contracts: the deck's
spine, the mapping from spine to slides, and the well-formedness of each slide.

### 1. The narrative spine (deck-level, produced BEFORE any slides)

Before writing a single slide, the generator must produce a spine:

- A one-line **ABT** (And / But / Therefore) — the throughline.
- The **payoff named up front**.
- An **ordered list of beats**, proof-first: open with the proof/payoff, not a
  title card. Beat roles: `proof | tension | mechanism | turn | payoff | takeaway`.

**Example ABT (Foundry deck):**

> **AND** a small tool builds a machine that writes software the model never
> could in one pass; **BUT** left running it can't tell what's worth building
> (it grinds tests instead of drawing a ruler); **THEREFORE** the machine is the
> leverage, judgment stays human.

Payoff = the "ruler" beat.

**Structural rules:**

- **(a)** `beats[0].role == proof` unless an explicit `proof_deferred_reason` is
  given.
- **(b)** Every beat must carry an **"advances"** note stating how it serves the
  ABT. No advances, no beat. This kills random supporting text.
- **(c)** `mechanism` beats are **capped** and get **one claim each**. A 6-tile
  mechanism catalog slide becomes structurally unrepresentable.

### 2. The deck contract (beat -> slide mapping)

Slides render **1:1 from beats**. If it's not a beat, it's not a slide. The spine
therefore determines which slides exist and their order (proof-first). The payoff
**lands before the midpoint** — not buried at slide 13/16 like the Foundry deck.

### 3. The slide contract (each slide must be well-formed)

Every slide must:

- **(a) Name the beat it serves.**
- **(b) Lead with a CLAIM as its headline**, not a topic label — e.g. "The
  machine wrote 89K lines it couldn't judge", never "Metrics" / "Architecture".
- **(c) Earn its supporting content** — every fact, number, and visual must
  support that one claim, or it's cut.
- **(d) Hand off** — end pointed at the next beat, so the deck reads as a
  throughline.
- **(e) No default tile-grid** — a pile of co-equal tiles is banned as a layout
  default. Mechanism gets one claim per slide, shown not catalogued.

## Review model

Human-in-the-loop **only**. The user reviews generated decks later and gives
feedback; the generator regenerates.

Explicitly **not** in this prototype:

- No automated critic.
- No per-deck approval gate.
- No Attractor orchestration.

## Where it lives

The narrative guidance is added as a new **"Narrative Layer"** section near the
**top** of `context/storyteller-instructions.md` — so it's discoverable and
precedes the slide-type/checklist material rather than being buried under it. The
existing accuracy and visual checklists remain in place.

## Open questions (defer, don't block)

- The exact `mechanism`-beat cap number.
- Whether to later add the automated critic and/or the batch "rewrite every
  story" capability.
- How old decks with unverifiable or round-number metrics get re-verified when
  regenerated — the existing accuracy gate handles this.
