# Amplifier Stories - Development Tools

Utility scripts for creating presentations, analyzing Amplifier usage, and generating data-driven insights.

## Available Tools

### html2pptx_v2.py (recommended)

Converts Amplifier Stories HTML decks to PowerPoint presentations. Uses native
PowerPoint tables and `MSO_AUTO_SIZE` for reliable text sizing — replaces v1's
hand-rolled font metrics.

**Usage:**
```bash
# Convert a single deck
uv run --with python-pptx,beautifulsoup4,lxml python tools/html2pptx_v2.py <input.html> [output.pptx]

# Examples
uv run --with python-pptx,beautifulsoup4,lxml python tools/html2pptx_v2.py docs/my-deck.html
uv run --with python-pptx,beautifulsoup4,lxml python tools/html2pptx_v2.py docs/my-deck.html output/presentation.pptx
```

**Key improvements over v1:**
- Cards rendered as native table cells (not absolute-positioned shapes)
- Header zone uses combined text frame (eliminates header-overlap bugs)
- `MSO_AUTO_SIZE` delegates height decisions to PowerPoint's engine
- Dynamic font sizing based on content length

**Supported Elements:**
- Slide structure (`.slide` divs and sections)
- Section labels (`.section-label`)
- Headlines and subheads (`.headline`, `.subhead`, `.medium-headline`)
- Cards with titles and text (`.card`, `.card-title`, `.card-text`)
- Card grids (`.thirds`, `.halves`, `.fourths`, `.grid-2` through `.grid-5`)
- Tenet boxes with accent colors (`.tenet`, `.tenet.green`, `.tenet.orange`)
- Feature lists with check/x marks (`.feature-list`)
- Data tables (`.data-table`) — rendered as native PowerPoint tables
- Highlight/callout boxes (`.highlight-box`)
- Big numbers and stats (`.stat-grid`, `.card-number`, `.big-stat`)
- Versus comparisons (`.versus`)
- Code blocks with syntax highlighting (`.code-block`)
- Flow diagrams (`.flow-diagram`, `.workflow`)
- Quotes (`.quote`)

**Output:**
- 16:9 widescreen format (10" x 5.625")
- Black backgrounds with Amplifier Stories color palette
- Editable text in PowerPoint
- CSS `--accent` variable extracted for per-deck theming

---

### pptx_verify.py

Checks every text shape in a .pptx for text overflow and shape overlap. Run
this after every html2pptx conversion.

**Usage:**
```bash
# Verify a single file
uv run --with python-pptx python tools/pptx_verify.py path/to/file.pptx

# Verify all .pptx files in a directory
uv run --with python-pptx python tools/pptx_verify.py path/to/directory/

# Verbose output (shape-level detail)
uv run --with python-pptx python tools/pptx_verify.py path/to/file.pptx --verbose
```

**What it checks:**
- `TextOverflow` — compares estimated text height vs shape height (MINOR/MODERATE/SEVERE)
- `ShapeOverlap` — detects bounding-box intersections between shapes on the same slide

**Output:** Per-slide issue list + summary: "N overflow issues, N overlaps across N slides. Clean slides: X/Y"

---

### deck-style-fix.py

Deterministic CSS accessibility fixer — zero LLM tokens, pure regex/DOM
transforms. Run this before converting to PPTX to ensure clean input.

**Usage:**
```bash
uv run --with beautifulsoup4,lxml python tools/deck-style-fix.py <input.html>
```

**Four phases:**
1. CSS variable value fixes (contrast, surface brightness, border visibility)
2. CSS rule font-size minimums (context-dependent)
3. Inline style fixes (font-size, color, opacity)
4. Inject missing surface hierarchy variables

Computes WCAG 2.1 contrast ratios. Tracks every change with structured logging.

---

### patch_progressive_enhancement.py

Patches HTML decks so they degrade gracefully without JavaScript (e.g., in
Teams/SharePoint which strip JS).

**Usage:**
```bash
uv run --with beautifulsoup4 python tools/patch_progressive_enhancement.py [docs_directory]
```

**Changes per file:**
- Adds `html.js` class toggle (`<script>` in `<head>`)
- Restores `.slide { display: flex }` for no-JS (all slides visible)
- Removes `overflow: hidden` and `overscroll-behavior: none` from body
- Adds `html.js`-scoped rules to restore JS-mode slide navigation

Returns per-file status: `patched` / `already_patched` / `not_a_deck` / `no_changes`.

---

### html2pptx.py (v1 — superseded)

Original HTML-to-PPTX converter. Uses hand-rolled font metrics for absolute
shape positioning. **Superseded by html2pptx_v2.py** — kept for reference only.

---

### analyze_sessions.py

Analyzes Amplifier session data from `events.jsonl` files to extract usage patterns, agent interactions, and performance metrics.

**Usage:**
```bash
python tools/analyze_sessions.py <path-to-events.jsonl>
```

**Output:** Session duration, turn count, agent invocations, tool usage, provider/model stats, error tracking, performance metrics.

### create_dashboard.py

Generates Excel dashboards from analyzed session data.

**Usage:**
```bash
# First analyze sessions to generate data
python tools/analyze_sessions.py sessions/*.jsonl > analysis.json

# Then create dashboard
python tools/create_dashboard.py analysis.json output-dashboard.xlsx
```

**Output:** Multi-sheet Excel workbook with charts, metrics tables, and professional styling.

## Data Flow

```
events.jsonl -> analyze_sessions.py -> analysis.json -> create_dashboard.py -> dashboard.xlsx
```

## PPTX Conversion Pipeline

The recommended pipeline for converting an HTML deck to PPTX:

```
deck.html -> deck-style-fix.py -> html2pptx_v2.py -> pptx_verify.py -> deck.pptx
             (fix accessibility)   (convert)          (verify quality)
```

## Dependencies

```bash
# For html2pptx_v2
uv run --with python-pptx,beautifulsoup4,lxml python tools/html2pptx_v2.py ...

# For pptx_verify
uv run --with python-pptx python tools/pptx_verify.py ...

# For deck-style-fix
uv run --with beautifulsoup4,lxml python tools/deck-style-fix.py ...

# For analyze/dashboard
pip install openpyxl pandas
```
