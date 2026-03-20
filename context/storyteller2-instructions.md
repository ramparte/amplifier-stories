# Storyteller2 Instructions: YAML-First Deck Creation

## Core Principle

**YAML is the canonical representation.** You emit structured DeckInput YAML.
The deck engine renders both HTML and PPTX from the same source. You never
write raw HTML — the engine handles rendering, CSS, navigation, and layout.

## DeckInput YAML Schema

### Top-Level Structure

```yaml
deck:
  title: "Deck Title"
  template: "default"          # Use "default" for HTML rendering
  style:
    accent_color: "#0A84FF"    # Per-deck accent color
    density: standard          # executive | standard | dense

slides:
  - type: title
    title: "Opening Title"
    subtitle: "Subtitle line"
    notes: "Speaker notes (optional on all types)"
    purpose: "open"            # Narrative purpose (optional on all types)
    pacing: "statement"        # dense | standard | sparse | statement (optional)
  # ... more slides
```

### All 14 Slide Types

#### 1. title — Opening slide
```yaml
- type: title
  title: "Feature Name"
  subtitle: "One-line description — Date"
```

#### 2. section — Section divider
```yaml
- type: section
  title: "Section Name"
```

#### 3. content — Bullet points or statement
```yaml
- type: content
  title: "Key Points"
  bullets:
    - "First insight with detail"
    - "Second insight with detail"
    - "Third insight with detail"
```
When `bullets` is empty or omitted, renders as a statement slide (title only).

#### 4. image_content — Bullets with image
```yaml
- type: image_content
  title: "Architecture Overview"
  bullets:
    - "Main takeaway"
  image: "Description of the image for alt text / generation"
```

#### 5. two_column — Two columns
```yaml
- type: two_column
  title: "Compare Approaches"
  col1_head: "Option A"
  col1_body: "Details about Option A"
  col2_head: "Option B"
  col2_body: "Details about Option B"
```

#### 6. three_column — Three columns
```yaml
- type: three_column
  title: "Three Pillars"
  col1_head: "Speed"
  col1_body: "Fast deployments"
  col2_head: "Reliability"
  col2_body: "Zero-downtime releases"
  col3_head: "Security"
  col3_body: "Shift-left scanning"
```

#### 7. quote — Pull quote
```yaml
- type: quote
  text: "The best way to predict the future is to create it."
  attribution: "Peter Drucker"
```

#### 8. closing — Closing / CTA
```yaml
- type: closing
  title: "Thank You — Let's Build Together"
  subtitle: "Optional subtitle"
```

#### 9. cards — Feature/concept grid (2-6 cards)
```yaml
- type: cards
  title: "Platform Capabilities"
  section_label: "FEATURES"    # Optional uppercase label above title
  cards:
    - title: "Speed"
      body: "10x faster builds through parallel execution"
      accent: "green"          # Optional: green, orange, blue, etc.
    - title: "Quality"
      body: "Zero-defect pipeline with automated checks"
    - title: "Scale"
      body: "Serves millions of users globally"
```

#### 10. code — Code block with caption
```yaml
- type: code
  title: "Quick Start"
  language: python             # Optional language tag
  code: |
    from deck_engine.schema import load_deck_yaml
    deck = load_deck_yaml("my-deck.yaml")
    print(f"Loaded {len(deck.slides)} slides")
  caption: "Three lines to go from YAML to deck"  # Optional
```

#### 11. stats — Big metrics / KPIs (2-4 stats)
```yaml
- type: stats
  title: "Impact Metrics"
  stats:
    - value: "47x"
      label: "faster than manual"
    - value: "99.9%"
      label: "uptime"
    - value: "2.6K"
      label: "daily deployments"
```

#### 12. comparison — Before/after or A vs B
```yaml
- type: comparison
  title: "Before and After"
  left_label: "Without Deck Engine"
  left_items:
    - "Manual HTML editing"
    - "No quality gates"
    - "Fragile PPTX conversion"
  right_label: "With Deck Engine"
  right_items:
    - "Structured YAML input"
    - "Automated critic loop"
    - "Clean template-driven PPTX"
```

#### 13. flow — Process / pipeline steps (min 2 steps)
```yaml
- type: flow
  title: "The Pipeline"
  steps:
    - "Author YAML"
    - "Validate Schema"
    - "Critic Review"
    - "Render"
    - "Ship"
```

#### 14. highlight — Key insight callout
```yaml
- type: highlight
  title: "The Key Insight"
  highlight_text: "YAML is the canonical representation"
  body: "Both HTML and PPTX render from the same structured source"
  accent: "#30D158"            # Optional accent color override
```

## Validation Constraints

| Type | Constraint |
|------|-----------|
| `cards` | 2-6 cards required |
| `stats` | 2-4 stats required |
| `flow` | Minimum 2 steps |
| `slides` | At least 1 slide required |
| `pacing` | Must be one of: dense, standard, sparse, statement |

## Rendering Commands

### Validate YAML
```bash
cd ~/dev/ANext/decks && uv run python -c "
from deck_engine.schema import load_deck_yaml
deck = load_deck_yaml('PATH_TO_YAML')
print(f'Valid: {len(deck.slides)} slides')
for s in deck.slides: print(f'  {s.type}: {s.title}')
"
```

### Generate HTML
```bash
cd ~/dev/ANext/decks && uv run python -c "
from deck_engine.schema import load_deck_yaml, load_template
from deck_engine.html_gen import HtmlGenerator
from pathlib import Path
deck = load_deck_yaml('PATH_TO_YAML')
template = load_template(Path('templates/default.yaml'))
gen = HtmlGenerator()
out = gen.generate(deck, template, output_dir=Path('OUTPUT_DIR'))
print(f'HTML written to: {out}')
"
```

### Generate PPTX
```bash
cd ~/dev/ANext/decks && uv run python -c "
from deck_engine.schema import load_deck_yaml
from deck_engine.registry import load_registry
from deck_engine.assembler import assemble_deck
from pathlib import Path
deck = load_deck_yaml('PATH_TO_YAML')
registry = load_registry(Path('sdp-registry.yaml'))
assemble_deck(deck, Path('templates/sdp-summit-2026.pptx'), registry, Path('OUTPUT.pptx'))
print('PPTX written')
"
```

## Source Verification

Default to the **Microsoft Amplifier ecosystem** unless explicitly told otherwise:
- microsoft/amplifier* for core Amplifier repos
- ramparte/* for team member projects
- NEVER use anthropics/amplifier* repos

## What You Do NOT Do

- You do NOT write raw HTML. The engine renders it.
- You do NOT manage CSS, navigation JS, or slide transitions.
- You do NOT call html2pptx_v2.py. The engine's assembler handles PPTX natively.
- You do NOT skip the research step. story-researcher is mandatory.
- You do NOT invent metrics. If research doesn't support a claim, don't make it.
