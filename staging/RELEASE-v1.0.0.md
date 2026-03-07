# Release v1.0.0 - Amplifier Bundle: Stories

**Release Date:** January 27, 2026  
**Release Type:** Initial Release (MAJOR)  
**Bundle:** `amplifier-bundle-stories`

---

## Highlights

**Autonomous Storytelling Engine for Any Project**

The Stories bundle transforms your development activity into professional presentations, documents, and content across multiple formats and audiences. From git commits to executive summaries, from session logs to compelling case studies - all automated.

### Key Capabilities

- **11 Specialist Agents** - Purpose-built agents for every content need
- **5 Output Formats** - HTML, PowerPoint, Excel, Word, PDF
- **4 Automated Workflows** - Recipes that run end-to-end without intervention
- **6 Story Archetypes** - Proven narrative patterns for technical storytelling

---

## What's New

### Specialist Agents (11)

| Agent | Purpose |
|-------|---------|
| `stories:storyteller` | Primary agent - creates Apple Keynote-style presentations |
| `stories:story-researcher` | Gathers data from git, sessions, APIs |
| `stories:content-strategist` | Plans what stories to tell and when |
| `stories:technical-writer` | Deep technical documentation |
| `stories:marketing-writer` | Community and public communication |
| `stories:executive-briefer` | High-level summaries for decision-makers |
| `stories:release-manager` | Automated release documentation from git tags |
| `stories:case-study-writer` | Narrative case studies from session data |
| `stories:data-analyst` | Data transformation and visualization |
| `stories:content-adapter` | Format and audience transformation |
| `stories:community-manager` | Community engagement content |

### Output Formats (5)

| Format | Best For | Templates Included |
|--------|----------|-------------------|
| **HTML** | Quick internal shares, GitHub Pages | 8 slide templates |
| **PowerPoint** | Executive presentations, corporate settings | Via html2pptx converter |
| **Excel** | Data analysis, metrics dashboards | 3 templates (dashboard, metrics, comparison) |
| **Word** | Technical documentation, proposals | 3 templates (case study, proposal, technical doc) |
| **PDF** | Final deliverables, archival | 1 template (one-pager) |

### Automated Workflows (4 Recipes)

| Recipe | Description |
|--------|-------------|
| `session-to-case-study` | Convert Amplifier sessions into professional Word case studies |
| `git-tag-to-changelog` | Generate complete release documentation from git tags |
| `weekly-digest` | Regular project updates with zero manual work |
| `blog-post-generator` | Feature stories from git activity |

### Story Archetypes (6)

Proven narrative patterns for technical storytelling:

- **Problem-Solution-Impact** - Classic business case structure
- **Feature Journey** - How a feature evolved from idea to reality
- **Technical Deep Dive** - Architecture and implementation details
- **Velocity Metrics** - Data-driven progress and productivity stories
- **Release Announcement** - What's new and why it matters
- **Community Showcase** - Highlighting contributors and adoption

### Developer Tools (3)

| Tool | Purpose |
|------|---------|
| `html2pptx.py` | Convert HTML decks to native PowerPoint |
| `analyze_sessions.py` | Extract usage patterns from Amplifier sessions |
| `create_dashboard.py` | Generate Excel dashboards from session data |

---

## Installation

```bash
# Add the bundle
amplifier bundle add git+https://github.com/microsoft/amplifier-bundle-stories@main

# Activate it
amplifier bundle use stories
```

### Dependencies

This bundle includes `amplifier-foundation` for core tools.

For document creation with Word/Excel templates:
```bash
# Anthropic Skills (for docx package)
git clone https://github.com/anthropics/skills ~/dev/anthropic-skills
```

---

## Quick Start

### Manual Content Creation

```
"Create a PowerPoint about shadow environments"
"Make an Excel dashboard showing adoption metrics"
"Write a case study about the authentication refactor"
```

### Automated Workflows

```
"Run the weekly digest recipe"
"Generate a case study from this session"
"Create release notes for the v2.0 tag"
```

---

## Bundle Structure

```
amplifier-bundle-stories/
├── bundle.md                 # Entry point
├── behaviors/
│   └── stories.yaml          # Agent + recipe configuration
├── agents/                   # 11 specialist agents
├── context/                  # Instructions & styles
│   ├── storyteller-instructions.md
│   ├── presentation-styles.md
│   ├── responsive-design.md
│   ├── powerpoint-template.md
│   └── archetypes/           # 6 story patterns
├── recipes/                  # 4 automated workflows
├── tools/                    # Python utilities
│   ├── html2pptx.py
│   ├── analyze_sessions.py
│   └── create_dashboard.py
└── workspace/                # Format templates
    ├── pptx/templates/       # 8 HTML slide templates
    ├── xlsx/templates/       # 3 Excel templates
    ├── docx/templates/       # 3 Word templates
    └── pdf/templates/        # 1 PDF template
```

---

## Release Statistics

| Metric | Value |
|--------|-------|
| Total Files | 58 |
| Lines of Code | ~12,000 |
| Agents | 11 |
| Recipes | 4 |
| Templates | 15+ |
| Story Archetypes | 6 |
| Commits | 4 |

---

## Migration Notes

**Renamed from `storyteller` to `stories`**

This bundle was renamed from `amplifier-bundle-storyteller` to `amplifier-bundle-stories` to avoid the `storyteller:storyteller` namespace collision. 

All agents are now namespaced as `stories:*`:
- `stories:storyteller` (primary agent)
- `stories:case-study-writer`
- `stories:release-manager`
- etc.

---

## Contributors

- **Brian Krabach** - Bundle author and maintainer
- **Amplifier** - AI pair programming assistant

---

## License

MIT License - see [LICENSE](../LICENSE)

---

## What's Next

Future releases may include:
- Additional story archetypes
- More output format templates
- Enhanced recipe automation
- Integration with more data sources
- Community-contributed agents

---

## Links

- [Repository](https://github.com/microsoft/amplifier-bundle-stories)
- [Amplifier Core](https://github.com/microsoft/amplifier)
- [Bug Reports](https://github.com/microsoft/amplifier-bundle-stories/issues)

---

*Generated with [Amplifier](https://github.com/microsoft/amplifier)*
