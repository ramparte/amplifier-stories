# Story2 Pipeline: Structured YAML + Deck Engine Quality Pipeline

## Status: Design Spec (not started)

## Problem

The current amplifier-stories pipeline generates HTML directly from LLM output.
When PPTX is requested, `html2pptx_v2.py` parses the bespoke HTML and maps it
to PowerPoint shapes heuristically. This has two problems:

1. **No quality pipeline** -- the storyteller self-reviews against a checklist,
   but there's no automated critique loop, no scoring, no re-generation.
2. **Fragile HTML-to-PPTX conversion** -- html2pptx must reverse-engineer the
   LLM's creative decisions from CSS classes and DOM structure.

Meanwhile, the deck engine at `~/dev/ANext/decks` has a proven quality
pipeline: YAML schema -> narrative critique -> mechanical checks -> heuristic
scoring -> visual critique loop -> aesthetic rubric. But its schema (8 slide
types) is too narrow for stories content.

## Proposed Architecture

```
Storyteller LLM
    |
    v
Extended DeckInput YAML (~15 slide types)
    |                           |
    v                           v (only when PPTX requested)
Stories HTML renderer           Deck engine pipeline
(keeps Apple Keynote            YAML -> critic loop -> PPTX assembler
 aesthetic, rich CSS,           -> pptx_verify -> ship
 dark theme)
    |                           |
    v                           v
HTML deck -> check -> ship      PPTX deck (quality-gated)
```

Key principle: YAML is the canonical representation. HTML and PPTX are two
renderers from the same source. The stories HTML renderer preserves the
existing visual richness. The deck engine provides the quality-gated PPTX path.

## What Must Change

### 1. Extend DeckInput Schema (in deck engine repo)

Add these slide types to `deck_engine/schema.py`:

```python
class CardItem(BaseModel):
    title: str
    body: str
    accent: str | None = None               # "green", "orange", "blue"

class CardsSlide(BaseModel):
    """Grid of feature/concept cards."""
    type: Literal["cards"]
    title: str
    section_label: str | None = None        # small uppercase label above title
    cards: list[CardItem]                    # 2-6 cards
    notes: str | None = None
    purpose: str | None = None
    pacing: Literal["dense", "standard", "sparse", "statement"] | None = None

class CodeSlide(BaseModel):
    """Slide with a code block and optional explanation."""
    type: Literal["code"]
    title: str
    language: str | None = None
    code: str                                # the code content
    caption: str | None = None               # explanation below
    notes: str | None = None
    purpose: str | None = None
    pacing: Literal["dense", "standard", "sparse", "statement"] | None = None

class StatItem(BaseModel):
    value: str                               # "47x", "2.6K", "98%"
    label: str                               # what the number means

class StatsSlide(BaseModel):
    """Big numbers / metrics display."""
    type: Literal["stats"]
    title: str
    stats: list[StatItem]                    # 2-4 stats
    notes: str | None = None
    purpose: str | None = None
    pacing: Literal["dense", "standard", "sparse", "statement"] | None = None

class ComparisonSlide(BaseModel):
    """Before/after or versus comparison."""
    type: Literal["comparison"]
    title: str
    left_label: str                          # "Before" / "Without"
    left_items: list[str]
    right_label: str                         # "After" / "With"
    right_items: list[str]
    notes: str | None = None
    purpose: str | None = None
    pacing: Literal["dense", "standard", "sparse", "statement"] | None = None

class FlowSlide(BaseModel):
    """Horizontal step flow (process/pipeline diagram)."""
    type: Literal["flow"]
    title: str
    steps: list[str]                         # rendered with arrows between
    notes: str | None = None
    purpose: str | None = None
    pacing: Literal["dense", "standard", "sparse", "statement"] | None = None

class HighlightSlide(BaseModel):
    """Callout/highlight box with supporting text."""
    type: Literal["highlight"]
    title: str
    highlight_text: str                      # the main callout
    body: str | None = None                  # supporting explanation
    accent: str | None = None                # color accent
    notes: str | None = None
    purpose: str | None = None
    pacing: Literal["dense", "standard", "sparse", "statement"] | None = None
```

This takes the schema from 8 to 15 slide types. Update the `SlideConfig`
discriminated union and `DeckInput` to include all new types.

### 2. Extend PPTX Assembler (in deck engine repo)

Add layout logic in `deck_engine/assembler.py` (or `pptx_export.py`) for each
new type. Reference html2pptx_v2.py for how stories currently renders cards,
stats, code blocks, and comparisons to PPTX -- but implement cleanly using the
structured YAML fields instead of HTML parsing.

### 3. Extend HTML Generator (in deck engine repo)

Add rendering logic in `deck_engine/html_gen.py` for each new type. This is
the stories-style HTML renderer. It should produce HTML that matches the
stories' Apple Keynote aesthetic:
- Dark background (#000 or near-black)
- White/light text
- Per-deck `--accent` CSS variable
- Component CSS classes matching stories conventions (`.card`, `.thirds`,
  `.code-block`, `.stat-grid`, `.flow-diagram`, etc.)

The simplest approach: copy the relevant CSS/HTML patterns from existing
stories decks and templatize them in html_gen.py.

### 4. Build story2 Agent (in amplifier-stories repo)

Create `agents/storyteller2.md` -- a parallel agent that:
1. Delegates to `stories:story-researcher` (same research step)
2. Instructs the LLM to emit `DeckInput` YAML (extended schema)
3. Calls the deck engine to render HTML
4. If PPTX requested: runs the deck engine's quality pipeline
5. Same antagonistic review checklist
6. Saves to `docs/` with a note it was generated by story2

### 5. Wire into Bundle

Add `storyteller2` to the agents list in `bundle.md`. Keep `storyteller` as
default -- story2 is opt-in for evaluation.

## Evaluation Plan

1. Pick 3-5 existing HTML decks that have good content
2. Extract their content into DeckInput YAML manually (one-time)
3. Run story2 to generate HTML + PPTX from the YAML
4. Compare side-by-side:
   - story2 HTML vs original HTML (visual quality)
   - story2 PPTX vs html2pptx_v2 PPTX (fidelity, text overflow, editability)
5. If story2 output is competitive, migrate; if not, identify gaps

## Implementation Order

### Phase 1: Schema + Renderers (in deck engine repo: ~/dev/ANext/decks)
1. Add new slide types to `schema.py`
2. Add HTML rendering for new types to `html_gen.py`
3. Add PPTX assembly for new types to `assembler.py` / `pptx_export.py`
4. Add tests for new types
5. Test with a sample YAML that uses all new types

### Phase 2: Story2 Agent (in amplifier-stories repo: ~/dev/ANext/amplifier-stories)
1. Create `agents/storyteller2.md`
2. Create `context/storyteller2-instructions.md` with YAML schema reference
3. Add to `bundle.md`
4. Test: ask story2 to generate a deck from a topic

### Phase 3: Evaluation
1. Convert 3-5 existing decks to YAML
2. Generate HTML + PPTX via story2
3. Side-by-side comparison
4. Decision: adopt, iterate, or roll back

## Files That Will Change

### Deck engine repo (`~/dev/ANext/decks`)
- `deck_engine/schema.py` -- add 7 new slide types + supporting models
- `deck_engine/html_gen.py` -- render new types with stories-style CSS
- `deck_engine/assembler.py` -- PPTX layout logic for new types
- `tests/` -- tests for new types

### Amplifier-stories repo (`~/dev/ANext/amplifier-stories`)
- `agents/storyteller2.md` -- new parallel agent
- `context/storyteller2-instructions.md` -- schema reference + instructions
- `bundle.md` -- add storyteller2 to agents list

## Dependencies

The deck engine is a standalone Python package at `~/dev/ANext/decks`. The
story2 agent would invoke it via:

```bash
cd ~/dev/ANext/decks && uv run python -m deck_engine.cli <input.yaml> --html --pptx
```

Or, if installed as a package:

```python
from deck_engine.schema import load_deck_yaml
from deck_engine.html_gen import HtmlGenerator
from deck_engine.pptx_export import PptxExporter
```

## Rollback

If evaluation fails:
- Delete `agents/storyteller2.md` and `context/storyteller2-instructions.md`
- Remove from `bundle.md`
- Schema extensions in deck engine are harmless (additive only)
- No changes to the existing storyteller pipeline

## Current Deck Engine Schema (for reference)

Existing 8 slide types:
- `title` -- opening title (title + subtitle)
- `section` -- section divider (title only)
- `content` -- bullets (title + list, or statement if empty list)
- `image_content` -- bullets + image description
- `two_column` -- two columns (head + body each)
- `three_column` -- three columns
- `quote` -- pull quote (text + attribution)
- `closing` -- closing/thank-you (title + subtitle)

All types share: `notes`, `purpose`, `pacing` fields.

Supporting models: `DeckConfig`, `StyleConfig`, `NarrativeBlueprint`, `Act`,
`DeckTemplate`, `ColorTokens`, `TypographyConfig`, `BuildResult`.
