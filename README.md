# Amplifier Module: Stories

**Autonomous storytelling engine for the Amplifier ecosystem.**

Transform development activity into professional content - automatically, across formats and audiences.

## What This Module Does

**v2.0 Transformation:** From manual presentation tool to autonomous content engine.

### Three Core Capabilities

1. **Automated Story Generation** - Content emerges from live data (git, sessions, bundles)
2. **Multi-Audience Adaptation** - One story → technical, executive, and community voices
3. **Ecosystem Intelligence** - Deep integration with Amplifier's data sources

### Content Formats (5)
- **HTML** - "Useful Apple Keynote" style presentations (14 existing decks)
- **PowerPoint** - Professional .pptx with black backgrounds and blue gradients
- **Excel** - Data dashboards, metrics tracking, ROI analysis
- **Word** - Technical docs, proposals, case studies
- **PDF** - Executive one-pagers and summaries

### Specialist Agents (10)
- **story-researcher** - Automated data gathering from ecosystem
- **content-strategist** - Story selection and planning
- **technical-writer** - Deep technical documentation
- **marketing-writer** - Community and public communication
- **executive-briefer** - High-level summaries and ROI content
- **release-manager** - Automated release documentation
- **case-study-writer** - Narrative case studies from sessions
- **data-analyst** - Data transformation and visualization
- **content-adapter** - Format and audience transformation
- **community-manager** - Community engagement and recognition

### Automated Workflows (4 Recipes)
- **Session→Case Study** - Turn breakthrough sessions into shareable content
- **Git Tag→Changelog** - Generate complete release documentation automatically
- **Weekly Digest** - Regular ecosystem updates with zero manual work
- **Blog Post Generator** - Feature stories for community from git data

## Quick Start

### 1. Install Anthropic Skills (Required)

The agents use Anthropic's skills library for PowerPoint, Excel, Word, and PDF creation:

```bash
# Clone skills repository
git clone https://github.com/anthropics/skills ~/dev/anthropic-skills

# Add to Amplifier settings (if not already configured)
cat >> ~/.amplifier/settings.yaml << 'EOF'
skills:
  dirs:
    - ~/dev/anthropic-skills/skills
    - ~/.amplifier/skills
EOF
```

### 2. Activate the Bundle

Update your `~/.amplifier/settings.yaml` to use this bundle:

```yaml
bundle:
  active: amplifier-module-stories
```

**Note:** Despite "module" in the name, this is an Amplifier **bundle** (not a module). Bundles provide agents, recipes, and behaviors. The name reflects its role as a storytelling capability for the module ecosystem.

### 3. Restart Amplifier

After configuring skills and activating the bundle:
```bash
# Exit current session
exit

# Start new session
amplifier
```

### 4. Verify Bundle Is Active

In your new session:
```
"list available agents"
```

You should see: storyteller, story-researcher, content-strategist, technical-writer, marketing-writer, executive-briefer, release-manager, case-study-writer, data-analyst, content-adapter, community-manager (11 total)

---

## Quick Test

Once the bundle is active, test in a new Amplifier session with these prompts:

### Test 1: Verify Agent Availability
```
"list available agents"
```
**Expected:** See all 11 agents (storyteller + 10 specialists)

### Test 2: Manual Content Creation
```
"Use storyteller to create a PowerPoint slide using the title template about testing amplifier-module-stories"
```
**Expected:** Single PowerPoint slide created and auto-opened

### Test 3: Story Research
```
"Use story-researcher to gather data about the amplifier-module-stories repository"
```
**Expected:** Structured JSON with repository metrics, commits, timeline

### Test 4: Automated Recipe - Weekly Digest
```
"Run the weekly-digest recipe for the amplifier ecosystem"
```
**Expected:** Blog post + email + social media content generated (3-4 minutes)

### Test 5: Automated Recipe - Blog Post
```
"Run blog-post-generator with feature_name='shadow environments' target_audience='community'"
```
**Expected:** Blog post + social media snippets created and auto-opened (2.5-5 minutes)

> **Note:** When running recipes via CLI, use the `@` prefix for bundle paths:
> ```bash
> amplifier tool invoke recipes operation=execute recipe_path="@stories:recipes/blog-post-generator.yaml"
> ```

### Test 6: Multi-Format Storytelling
```
"Create a PowerPoint, Excel dashboard, and PDF one-pager about amplifier-module-stories capabilities"
```
**Expected:** Three files created in parallel, all auto-opened

### Test 7: Content Adaptation
```
"Use content-adapter to convert one of the HTML presentations in docs/ to a Word document"
```
**Expected:** Word document created with expanded content from HTML slides

### Test 8: Agent Coordination
```
"Use story-researcher to gather shadow environments data, then content-strategist to plan a multi-format campaign, then show me the plan"
```
**Expected:** Complete content plan with audience mapping and format selection

**For comprehensive testing:** See `tests/examples/*.md` for detailed test procedures for all 4 recipes.

## Usage Examples

### HTML Presentations (Default)
```
"Tell a story about shadow environments"
"Create a deck about the new recipe feature"
```

### PowerPoint
```
"Create a PowerPoint about shadow environments"
"Make a .pptx presentation for the session forking feature"
```

### Excel Dashboards
```
"Make an Excel dashboard showing Amplifier adoption metrics"
"Create an xlsx workbook analyzing recipe execution performance"
```

### Word Documents
```
"Write a Word document detailing the recipe system architecture"
"Create a docx technical guide for the shadow environment feature"
```

### PDF Reports
```
"Create a PDF report summarizing Q1 Amplifier achievements"
"Make a PDF one-pager about the cost optimization feature"
```

## Dependencies

### Core (Always Required)
- **Amplifier CLI** - `uv tool install git+https://github.com/microsoft/amplifier`
- **Anthropic Skills** - Cloned to `~/dev/anthropic-skills`

### Format-Specific Dependencies

#### PowerPoint (.pptx)
```bash
# Node.js packages (global)
npm install -g pptxgenjs playwright sharp react-icons react react-dom

# Python packages
pip install markitdown defusedxml Pillow
```

#### Excel (.xlsx)
```bash
# Python packages
pip install openpyxl pandas defusedxml

# LibreOffice (for formula recalculation)
# macOS:
brew install libreoffice
# Linux:
sudo apt-get install libreoffice
```

#### Word (.docx)
```bash
# Node.js packages (for new documents)
npm install -g docx

# Python packages (for editing)
pip install defusedxml

# Optional: pandoc for text extraction
# macOS:
brew install pandoc
# Linux:
sudo apt-get install pandoc

# Optional: LibreOffice for PDF conversion
brew install libreoffice  # or apt-get install libreoffice
```

#### PDF
```bash
# Python packages
pip install pypdf pdfplumber reportlab pytesseract pdf2image

# Command-line tools
# macOS:
brew install poppler qpdf
# Linux:
sudo apt-get install poppler-utils qpdf

# Optional: OCR support
# macOS:
brew install tesseract
# Linux:
sudo apt-get install tesseract-ocr
```

## Templates

Professional templates for each format, all styled with the "Useful Apple Keynote" aesthetic (black backgrounds, blue accents, clean typography).

### PowerPoint (7 slide templates)
`workspace/pptx/templates/`:
- **slide-title.html** - Centered opening slides
- **slide-content.html** - Standard content with bullets
- **slide-code.html** - Code examples with green syntax highlighting
- **slide-comparison.html** - Before/After two-column layouts
- **slide-metrics.html** - Big gradient numbers (3-column grid)
- **slide-cards.html** - Feature cards in grid layout
- **slide-section.html** - Section dividers with large numbers

### Excel (3 Python templates)
`workspace/xlsx/templates/`:
- **dashboard-template.py** - Complete dashboard with metrics and charts
- **metrics-template.py** - Metrics tracking with trend analysis
- **comparison-template.py** - Before/after comparison tables

### Word (3 JavaScript templates)
`workspace/docx/templates/`:
- **technical-doc-template.js** - Technical docs with table of contents
- **proposal-template.js** - Feature proposals with executive summary
- **case-study-template.js** - Narrative case studies

### PDF (1 Python template)
`workspace/pdf/templates/`:
- **one-pager-template.py** - Executive one-page summaries

**Each format includes a `templates/README.md` with usage examples and style specifications.**

## File Organization

```
amplifier-stories/
├── docs/                     # Final deliverables (all formats)
│   ├── *.html                # HTML presentations
│   ├── *.pptx                # PowerPoint files (approved)
│   ├── *.xlsx                # Excel workbooks (approved)
│   ├── *.docx                # Word documents (approved)
│   └── *.pdf                 # PDF files (approved)
├── workspace/                # Working directory for all formats
│   ├── pptx/
│   │   ├── templates/        # 7 HTML slide templates (kept in git)
│   │   ├── html-slides/      # Working HTML (gitignored)
│   │   ├── assets/           # Generated images (gitignored)
│   │   ├── output/           # Final .pptx (kept in git)
│   │   └── thumbnails/       # Validation previews (gitignored)
│   ├── xlsx/
│   │   ├── templates/        # 3 Python templates (kept in git)
│   │   └── output/           # Final .xlsx (kept in git)
│   ├── docx/
│   │   ├── templates/        # 3 JavaScript templates (kept in git)
│   │   └── output/           # Final .docx (kept in git)
│   └── pdf/
│       ├── templates/        # 1 Python template (kept in git)
│       └── output/           # Final .pdf (kept in git)
├── context/                  # Style guides and instructions
├── agents/                   # Agent definitions
├── tools/                    # Development utilities
├── deploy.sh                 # Deployment script
└── .env.local                # Local config (gitignored)
```

## Deployment

### SharePoint Deployment (Optional)

Configure SharePoint path for automatic deployment:

```bash
# Copy example config
cp .env.local.example .env.local

# Edit .env.local and set your SharePoint folder path
# SHAREPOINT_DECKS_PATH=/Users/yourname/OneDrive - Company/Shared/Decks
```

Deploy files:
```bash
# Deploy all HTML files to SharePoint
./deploy.sh

# Deploy specific file
./deploy.sh my-presentation.html

# Export to local Downloads instead
./deploy.sh --local
```

## Development

### Creating New Content

Ask the storyteller agent naturally:
```
"Create a [format] about [topic]"
"Make a [format] showing [data/story]"
```

The agent will:
1. Research the topic (GitHub activity, commits, PRs)
2. Design the narrative arc
3. Create content in the requested format
4. Organize files in appropriate workspace
5. Present for approval before deployment

### Workflow by Format

**HTML:**
- Creates self-contained file with inline CSS/JS
- Saves directly to `docs/`
- Updates `docs/index.html`

**PowerPoint:**
- Reads html2pptx guide
- Creates HTML slides in `pptx-workspace/html-slides/`
- Generates assets in `pptx-workspace/assets/`
- Converts to .pptx in `pptx-workspace/output/`
- Validates with thumbnails

**Excel:**
- Creates workbook with openpyxl/pandas
- Uses formulas (not hardcoded values)
- Recalculates to verify zero errors
- Saves to `workspace/xlsx/output/`

**Word:**
- Uses docx-js for new documents
- Uses OOXML library for editing
- Supports tracked changes and comments
- Saves to `workspace/docx/output/`

**PDF:**
- Creates with reportlab or converts from other formats
- Extracts data with pdfplumber
- Merges/splits with pypdf
- Saves to `workspace/pdf/output/`

## Style Guidelines

### HTML Presentations
- Black backgrounds, clean typography
- One concept per slide
- Big impact numbers
- Code examples with syntax highlighting
- "Useful Apple Keynote" aesthetic

### PowerPoint
- Professional corporate style
- Can match existing templates (e.g., Surface-Presentation.pptx)
- Web-safe fonts only
- Accurate positioning via html2pptx

### Excel
- Financial modeling standards
- Color coding: Blue=inputs, Black=formulas, Green=cross-sheet, Red=external
- Zero formula errors (mandatory)
- Formatted zeros as "-"

### Word
- Clear hierarchy with headings
- Table of contents for long documents
- Tracked changes for reviews
- Professional formatting

### PDF
- Print-ready quality
- Consistent fonts and spacing
- Proper page breaks

## Recipe Path Syntax

When invoking recipes programmatically (via CLI or tool calls), use the `@` prefix for bundle paths:

```bash
# Correct - with @ prefix
amplifier tool invoke recipes operation=execute \
  recipe_path="@stories:recipes/blog-post-generator.yaml"

# Wrong - won't work (missing @ prefix)
amplifier tool invoke recipes operation=execute \
  recipe_path="stories:recipes/blog-post-generator.yaml"
```

**Available recipes:**
| Recipe | Path |
|--------|------|
| Session to Case Study | `@stories:recipes/session-to-case-study.yaml` |
| Git Tag to Changelog | `@stories:recipes/git-tag-to-changelog.yaml` |
| Weekly Digest | `@stories:recipes/weekly-digest.yaml` |
| Blog Post Generator | `@stories:recipes/blog-post-generator.yaml` |

**In conversational mode**, you can use natural language and the `@` prefix is handled automatically:
```
"Run the weekly-digest recipe"
"Execute blog-post-generator for shadow environments"
```

## Troubleshooting

### Recipe Path Not Found
If you get "Recipe file not found" errors:
1. Ensure you're using the `@` prefix: `@stories:recipes/...`
2. Use absolute paths if bundle resolution fails: `$(pwd)/recipes/recipe-name.yaml`
3. Verify the bundle is active: `amplifier bundle list`

### Skills Not Loading
```bash
# Verify skills directory exists
ls ~/dev/anthropic-skills/skills

# Check settings.yaml configuration
grep -A3 "skills:" ~/.amplifier/settings.yaml

# Restart Amplifier session
exit
# Start new session
```

### Missing Dependencies

**Check Python packages:**
```bash
pip list | grep -E "openpyxl|pypdf|pdfplumber|reportlab|markitdown"
```

**Check Node.js packages:**
```bash
npm list -g | grep -E "pptxgenjs|playwright|sharp|docx"
```

**Install missing packages** using commands from Dependencies section above.

### Formula Errors in Excel
```bash
# Recalculate formulas
python ~/dev/anthropic-skills/skills/xlsx/recalc.py your-file.xlsx

# Check for errors
# Script will return JSON with error details
```

## Contributing

See `AGENTS.md` for agent configuration and `bundle.md` for bundle details.

## License

MIT - See repository for details.
