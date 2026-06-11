# Amplifier Stories Bundle

This is an **Amplifier bundle** for creating presentation decks showcasing Amplifier features and projects.

## Installation

```bash
# Add to your bundles
amplifier bundle add git+https://github.com/ramparte/amplifier-stories@master

# Or run directly
amplifier run --bundle git+https://github.com/ramparte/amplifier-stories@master
```

## Usage

Once the bundle is loaded, use the **storyteller** agent:

```
"Use storyteller to tell a story about [feature]"
"Create a deck about the new shadow environments feature"
"Make a presentation showing off recipe cancellation"
```

The storyteller agent will:
1. Research the feature (GitHub history, PRs, timeline)
2. Create a polished HTML deck in "Useful Apple Keynote" style
3. Save to `docs/` directory
4. Deploy to SharePoint when you approve

## Local Development

If you clone this repo directly for development:

```bash
# Set up SharePoint deployment
cp .env.local.example .env.local
# Edit .env.local with your SharePoint path

# Deploy decks
./deploy.sh                    # All decks
./deploy.sh my-deck.html       # Specific deck
```

## HTML to PowerPoint Conversion

To convert any HTML deck to PowerPoint, use `tools/html2pptx_v2.py`:

```bash
uv run --with python-pptx --with beautifulsoup4 --with lxml \
  python3 tools/html2pptx_v2.py docs/my-deck.html output.pptx
```

This is the **production converter**. It uses semantic layout (merged header
text frames, native PowerPoint tables, TEXT_TO_FIT_SHAPE auto-sizing) instead
of absolute positioning. Key features:

- Header elements (section-label, headline, subhead) merge into a single text frame
- Card grids render as native PowerPoint tables
- Code blocks cap to available slide space (never clip past bottom)
- Split containers route through the card grid handler
- All 90+ decks convert without crashes

The older `tools/html2pptx.py` (v1) is preserved for reference but should not
be used for new conversions. `tools/pptx_verify.py` can inspect output for
overflow and overlap issues.

## Bundle Structure

```
amplifier-stories/
├── bundle.md              # Bundle definition
├── agents/
│   └── storyteller.md     # Storyteller agent
├── context/
│   ├── presentation-styles.md
│   └── storyteller-instructions.md
├── tools/
│   ├── html2pptx_v2.py    # Production HTML-to-PPTX converter
│   ├── html2pptx.py       # Legacy v1 converter (reference only)
│   └── pptx_verify.py     # Overflow/overlap detection
├── docs/                  # Generated HTML decks
├── deploy.sh              # SharePoint deployment
└── .env.local             # Your SharePoint path (gitignored)
```

## Presentation Styles

The bundle supports two remembered styles:

- **Useful Apple Keynote** (default) - Higher density, good for engineers
- **Apple Keynote** - Pure visual impact, good for executives

See `context/presentation-styles.md` for details.
