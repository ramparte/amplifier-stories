# Story Narrative Spine — Implementation Plan

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Make "make an amplifier story" produce a compelling narrative deck (spine → 1:1 beats → well-formed slides) instead of a bag of random slides, and produce 3 regenerated sample decks the user can review.

**Architecture:** Two work items. (1) Add a "Narrative Layer" section near the top of the generator guidance file so every future deck is built spine-first. (2) Regenerate 3 existing decks into a NEW preview folder by re-deriving each deck's spine from facts already present in its verified HTML — no fresh repo research, no overwriting originals.

**Tech Stack:** Markdown (guidance), static HTML/CSS/JS decks (existing template), grep/browser for verification.

> **IMPORTANT — this is content-generation work, not testable software.** There is NO pytest / red-green-refactor cycle. Each task's verification is a concrete manual or scriptable CHECK (grep confirms text exists, deck opens, slide count == beat count, headlines are claims, etc.). Keep it fast and pragmatic — this is a prototype wanted tonight.

**Design doc:** `docs/plans/2026-07-13-story-narrative-spine-design.md`

---

## Work Item 1 — Add the narrative layer to the generator guidance

Base file: `context/storyteller-instructions.md` (412 lines; all slide-types + accuracy/visual checklists, ZERO narrative guidance today). The intro ends at line 3; `## Research Phase` begins at line 5. The new section goes BETWEEN them (after the intro, before `## Research Phase`).

### Task 1: Insert the "Narrative Layer (READ FIRST)" section

**Files:**
- Modify: `context/storyteller-instructions.md` (insert after line 3, before `## Research Phase`)

**Step 1: Insert the section**

Insert the following block immediately after the intro line (`Detailed guidance for creating presentation decks.`) and before `## Research Phase`:

```markdown
## Narrative Layer (READ FIRST)

A deck is a **narrative**, not a feature catalog. Before anything else, build the
spine; then map it 1:1 to slides; then make each slide well-formed. These three
contracts are mandatory. A deck that is pretty and accurate but not compelling
has failed.

### Contract 1 — The narrative spine (produce this BEFORE any slides)

Write the spine first, as an explicit artifact. It has three parts:

- **One-line ABT** — a single sentence in **And / But / Therefore** form:
  the stable situation (*And*), the complication (*But*), the resulting point
  (*Therefore*). This is the throughline of the whole deck.
- **Payoff, named up front** — state, in the spine, what the deck is driving
  toward. You must know the payoff before you write slide one.
- **Ordered list of beats** — proof-first. Each beat has a `role` from:
  `proof | tension | mechanism | turn | payoff | takeaway`, and an
  **`advances:` note** saying how it serves the ABT.

**Spine rules (hard):**

- **(a) Proof-first:** `beats[0].role == proof`. Open on the payoff/evidence,
  not a title card. The only exception is an explicit
  `proof_deferred_reason:` written into the spine.
- **(b) Every beat must advance the ABT:** each beat carries an `advances:` note.
  **No `advances`, no beat.** This is what kills random supporting material.
- **(c) Mechanism is capped, one claim each:** `mechanism` beats are limited in
  number and each makes exactly ONE claim. A 6-tile "here's everything it does"
  catalog beat is not representable — split it or cut it.

**Example spine (Foundry deck):**

```
ABT: AND a small tool builds a machine that writes software the model never
     could in one pass; BUT left running it can't tell what's worth building
     (it grinds tests instead of drawing a ruler); THEREFORE the machine is the
     leverage — judgment stays human.
Payoff: the "ruler incident" — the machine grinding tests while a human draws
        the ruler in seconds.
Beats:
  1. proof     — the machine shipped 89K lines in one run.   advances: establishes the AND (real leverage)
  2. tension   — but it couldn't tell what was worth doing.  advances: establishes the BUT
  3. mechanism — the dev-machine loop, one claim.            advances: shows HOW the leverage works
  4. turn      — the ruler incident.                         advances: the pivot from AND to THEREFORE
  5. payoff    — machine = leverage, judgment stays human.   advances: lands the THEREFORE
  6. takeaway  — the pattern, generalized.                   advances: what the audience keeps
```

### Contract 2 — The deck contract (beat → slide)

- Slides render **1:1 from beats**. One beat = one slide.
- **If it's not a beat, it's not a slide.** No slide exists without a beat.
- **Payoff lands before the midpoint** of the deck — never buried near the end
  (the Foundry deck's payoff was at slide 13/16; that is the failure mode).
- The mandatory **Sources & Methodology** slide is the one allowed exception to
  1:1 (it is an audit-trail slide, not a beat) and sits at the end.

### Contract 3 — The slide contract (each slide must be well-formed)

Every content slide must:

- **(a) Name the beat it serves.** State which beat/role this slide is (an HTML
  comment `<!-- beat N: role -->` at the top of the slide is enough).
- **(b) Lead with a CLAIM as its headline** — an assertion that advances the
  beat (e.g. *"The machine wrote 89K lines it couldn't judge"*), **never a bare
  topic label** like *"Metrics"*, *"Architecture"*, *"Overview"*, *"Features"*.
- **(c) Earn every fact/number/visual on it** — each supporting element must
  make THAT ONE claim land harder. If it doesn't, cut it.
- **(d) Hand off** — end pointed at the next beat, so the deck reads as a
  throughline, not islands.
- **(e) No default tile-grid** — a pile of co-equal tiles is banned as a layout
  default. Mechanism gets one claim per slide, shown not catalogued. If you find
  yourself making 4+ co-equal tiles, you are cataloguing, not narrating.
```

**Step 2: Add a "Narrative" subsection to the Quality Checklist**

In `context/storyteller-instructions.md`, in the `## Quality Checklist` section (currently `### Accuracy` then `### Visual & Technical`), add a NEW subsection **before** `### Accuracy`:

```markdown
### Narrative (verify FIRST — a pretty, accurate, non-compelling deck has failed)

- [ ] **Spine written before slides** — ABT (And/But/Therefore) + named payoff + ordered beats exist as an artifact (see "Narrative Layer")
- [ ] **Proof-first** — first content slide is the `proof` beat (or an explicit `proof_deferred_reason` is stated)
- [ ] **Every beat advances the ABT** — each beat has an `advances:` note; no orphan beats
- [ ] **Slides are 1:1 with beats** — slide count == beat count (excluding the Sources slide)
- [ ] **Payoff lands before the midpoint** — not buried at the end
- [ ] **Every slide headline is a CLAIM, not a topic label** — no "Metrics"/"Architecture"/"Overview" title slides
- [ ] **No co-equal tile-grid catalog slides** — mechanism is one claim per slide, not a 4+ tile pile
```

**Step 3: Verify (concrete checks — no tests)**

Run each and confirm:

```bash
cd /home/ramparte/dev/ANext/amplifier-stories

# 3a. The new top-level section and all three contract headings exist
grep -n "## Narrative Layer (READ FIRST)" context/storyteller-instructions.md
grep -n "Contract 1 — The narrative spine" context/storyteller-instructions.md
grep -n "Contract 2 — The deck contract" context/storyteller-instructions.md
grep -n "Contract 3 — The slide contract" context/storyteller-instructions.md

# 3b. The Narrative Layer section appears BEFORE "## Research Phase"
awk '/## Narrative Layer/{n=NR} /## Research Phase/{r=NR} END{ if (n>0 && n<r) print "PASS: Narrative Layer at line "n" precedes Research Phase at line "r; else print "FAIL" }' context/storyteller-instructions.md

# 3c. The checklist subsection exists
grep -n "### Narrative (verify FIRST" context/storyteller-instructions.md
```

Expected: every grep returns a line; the awk prints `PASS:`.

**Step 4: Commit**

```bash
git add context/storyteller-instructions.md
git commit -m "feat: add narrative spine layer to storyteller guidance"
```

---

## Work Item 2 — Regenerate 3 sample decks into a preview folder

Regenerate three existing decks into a NEW folder so old vs new can be compared side by side. **Do NOT overwrite the originals in `docs/`.** **Do NOT do fresh repo research** — re-use the verified metrics/content already present in each existing deck's HTML; only restructure it into a spine + well-formed slides.

Target decks:
1. `docs/the-foundry-and-the-machine.html` — grounding example; its payoff ("ruler incident") is currently buried at ~slide 13/16 and MUST move before the midpoint.
2. `docs/superpowers-deck.html`
3. `docs/context-rot-systems-architecture.html`

If a chosen deck turns out unsuitable during execution (e.g. it has no coherent narrative to recover), substitute another feature-catalog deck from `docs/` and note the substitution in the commit message.

Each regenerated deck MUST:
- Begin with the written **spine as an HTML comment** at the very top of the `<body>` (or just after `<!DOCTYPE>`), for reviewability — include the ABT, named payoff, and the ordered beats with roles and `advances:` notes.
- Be **proof-first** (first content slide = proof beat).
- Have slides **1:1 with beats**; payoff **before the midpoint**.
- Have **every slide headline be a claim**, not a topic label.
- Have **no co-equal tile-grid catalog slides** (no 4+ co-equal tiles).
- Keep the **existing HTML template/CSS, nav JS, progressive-enhancement patterns**, and the **mandatory Sources & Methodology slide** (copy the Sources slide's content over from the original so metrics stay verified).

### Task 2: Set up the preview folder

**Files:**
- Create: `docs/narrative-preview/` (new directory)

**Step 1: Create the folder**

```bash
cd /home/ramparte/dev/ANext/amplifier-stories
mkdir -p docs/narrative-preview
```

**Step 2: Verify**

```bash
test -d docs/narrative-preview && echo "PASS: folder exists"
```

Expected: `PASS: folder exists`.

### Task 3: Regenerate the Foundry deck

**Files:**
- Read: `docs/the-foundry-and-the-machine.html` (source facts + template + Sources slide)
- Create: `docs/narrative-preview/the-foundry-and-the-machine.html`

**Step 1: Extract the reusable facts and Sources slide**

Read `docs/the-foundry-and-the-machine.html`. Pull out (do not re-research): every verified metric/number, the Sources & Methodology slide content, and the CSS/nav/progressive-enhancement scaffolding. These are reused verbatim.

**Step 2: Write the spine**

Write the spine for this deck (ABT + named payoff + ordered proof-first beats with roles and `advances:` notes). Use the Foundry example in Contract 1 as the guide — the payoff is the "ruler incident" and it must be placed before the midpoint.

**Step 3: Build the deck from the spine**

Create `docs/narrative-preview/the-foundry-and-the-machine.html`:
- Put the spine as an HTML comment at the top.
- Emit one slide per beat, in order, proof-first, each with a `<!-- beat N: role -->` comment and a CLAIM headline.
- Reuse the original CSS, nav JS, progressive-enhancement blocks, and the Sources slide.
- No co-equal tile-grid slides.

**Step 4: Verify (concrete checks — no tests)**

```bash
cd /home/ramparte/dev/ANext/amplifier-stories
F=docs/narrative-preview/the-foundry-and-the-machine.html

# 4a. Spine comment present
grep -qi "ABT:" $F && echo "PASS: spine comment present" || echo "FAIL: no spine"

# 4b. Slide count == beat count. Count beat comments and slide divs.
echo "beats:  $(grep -c '<!-- beat' $F)"
echo "slides: $(grep -oc 'class="slide' $F)"
# Manually confirm slides == beats + 1 Sources slide (Sources is the allowed non-beat slide).

# 4c. Progressive enhancement + Sources slide + more-stories link preserved
grep -q "classList.add('js')" $F && echo "PASS: progressive enhancement"
grep -qi "Sources" $F && echo "PASS: sources slide present"
grep -q "More Amplifier Stories" $F && echo "PASS: more-stories link"
```

Then **open the file in a browser** and manually confirm:
- First content slide is the **proof** beat (not a title card).
- The **payoff (ruler incident) lands before the midpoint**.
- **Every slide headline is a claim**, not a topic label.
- **No slide has 4+ co-equal tiles.**
- Navigation (arrows/click/dots) works.

**Step 5: Commit**

```bash
git add docs/narrative-preview/the-foundry-and-the-machine.html
git commit -m "feat: regenerate Foundry deck spine-first (narrative preview)"
```

### Task 4: Regenerate the Superpowers deck

**Files:**
- Read: `docs/superpowers-deck.html`
- Create: `docs/narrative-preview/superpowers-deck.html`

**Step 1–3:** Same procedure as Task 3, applied to `docs/superpowers-deck.html`:
1. Extract verified facts + Sources slide + scaffolding from the original (no fresh research).
2. Write the spine (ABT + named payoff + ordered proof-first beats with `advances:` notes) for the Superpowers story.
3. Build `docs/narrative-preview/superpowers-deck.html` — spine comment at top, one slide per beat proof-first with `<!-- beat N: role -->` comments and claim headlines, original CSS/nav/PE reused, Sources slide kept, no tile-grid catalog slides.

**Step 4: Verify** — run the same check block as Task 3 Step 4 with `F=docs/narrative-preview/superpowers-deck.html`, then open in a browser and confirm proof-first, payoff-before-midpoint, claim headlines, no 4+ co-equal tiles, nav works.

**Step 5: Commit**

```bash
git add docs/narrative-preview/superpowers-deck.html
git commit -m "feat: regenerate Superpowers deck spine-first (narrative preview)"
```

### Task 5: Regenerate the Context-Rot deck

**Files:**
- Read: `docs/context-rot-systems-architecture.html`
- Create: `docs/narrative-preview/context-rot-systems-architecture.html`

**Step 1–3:** Same procedure, applied to `docs/context-rot-systems-architecture.html`:
1. Extract verified facts + Sources slide + scaffolding (no fresh research).
2. Write the spine for the Context-Rot story.
3. Build `docs/narrative-preview/context-rot-systems-architecture.html` — spine comment at top, one slide per beat proof-first with beat comments and claim headlines, original CSS/nav/PE reused, Sources slide kept, no tile-grid catalog slides.

> Note: if this deck proves unsuitable (no recoverable narrative), substitute another feature-catalog deck from `docs/` and record the substitution in the commit message.

**Step 4: Verify** — run the same check block as Task 3 Step 4 with `F=docs/narrative-preview/context-rot-systems-architecture.html`, then open in a browser and confirm proof-first, payoff-before-midpoint, claim headlines, no 4+ co-equal tiles, nav works.

**Step 5: Commit**

```bash
git add docs/narrative-preview/context-rot-systems-architecture.html
git commit -m "feat: regenerate Context-Rot deck spine-first (narrative preview)"
```

---

## Done criteria

- `context/storyteller-instructions.md` has a `## Narrative Layer (READ FIRST)` section (with all three contracts) placed before `## Research Phase`, plus a `### Narrative` checklist subsection.
- `docs/narrative-preview/` contains 3 regenerated decks, each with a spine comment, proof-first ordering, 1:1 beat↔slide mapping, claim headlines, payoff before the midpoint, no tile-grid catalog slides, and the preserved template/Sources slide.
- Originals in `docs/` are untouched (side-by-side comparison intact).
- One local commit per item. **No `deploy.sh`, no push, no PR** — the user reviews the preview folder first.

**Report to the user:** the 3 preview file paths under `docs/narrative-preview/` for review.
