---
bundle:
  name: amplifier-module-stories
  version: 2.0.0
  description: Autonomous storytelling engine for the Amplifier ecosystem - automated content generation across formats and audiences

includes:

agents:
  # Legacy agent (maintained for backward compatibility)
  storyteller:
    path: amplifier-module-stories:agents/storyteller.md

  # Story2: YAML-first deck creation via deck engine
  storyteller2:
    path: amplifier-module-stories:agents/storyteller2.md

  # Specialist agents for autonomous storytelling
  story-researcher:
    path: amplifier-module-stories:agents/story-researcher.md
  content-strategist:
    path: amplifier-module-stories:agents/content-strategist.md
  technical-writer:
    path: amplifier-module-stories:agents/technical-writer.md
  marketing-writer:
    path: amplifier-module-stories:agents/marketing-writer.md
  executive-briefer:
    path: amplifier-module-stories:agents/executive-briefer.md
  release-manager:
    path: amplifier-module-stories:agents/release-manager.md
  case-study-writer:
    path: amplifier-module-stories:agents/case-study-writer.md
  data-analyst:
    path: amplifier-module-stories:agents/data-analyst.md
  content-adapter:
    path: amplifier-module-stories:agents/content-adapter.md
  community-manager:
    path: amplifier-module-stories:agents/community-manager.md

recipes:
  session-to-case-study:
    path: amplifier-module-stories:recipes/session-to-case-study.yaml
  git-tag-to-changelog:
    path: amplifier-module-stories:recipes/git-tag-to-changelog.yaml
  weekly-digest:
    path: amplifier-module-stories:recipes/weekly-digest.yaml
  blog-post-generator:
    path: amplifier-module-stories:recipes/blog-post-generator.yaml
---

# Amplifier Module: Stories

**Autonomous storytelling engine for the Amplifier ecosystem.**

From manual "create a deck about X" to automated story generation from live data - across formats, audiences, and use cases.

## The Transformation

**Before:** Manual presentation creation  
**After:** Autonomous content engine that captures, adapts, and distributes stories automatically

### Three Core Capabilities

1. **Automated Story Generation** - Stories emerge from data (git, sessions, bundles)
2. **Multi-Audience Adaptation** - One story → technical, executive, community voices
3. **Ecosystem Intelligence** - Deep integration with Amplifier's data sources

## What This Module Does

### Content Formats (5)
- **HTML** - "Useful Apple Keynote" style presentations
- **PowerPoint** - Professional .pptx with black backgrounds and blue gradients
- **Excel** - Data dashboards, metrics tracking, comparisons
- **Word** - Technical docs, proposals, case studies
- **PDF** - Executive one-pagers and summaries

### Specialist Agents (10)
- **story-researcher** - Automated data gathering from ecosystem
- **content-strategist** - Determines what stories to tell
- **technical-writer** - Deep technical documentation
- **marketing-writer** - External communication
- **executive-briefer** - High-level summaries for decision-makers
- **release-manager** - Automated release documentation
- **case-study-writer** - Turns sessions into narratives
- **data-analyst** - Transforms raw data into insights
- **content-adapter** - Converts between formats and audiences
- **community-manager** - Community engagement content

### Automated Workflows (4 Recipes)
- **Session→Case Study** - Turn breakthrough sessions into shareable content
- **Git Tag→Changelog** - Generate release notes automatically
- **Weekly Digest** - Regular ecosystem updates with zero manual work
- **Blog Post Generator** - Feature stories for community

## Quick Start

### Basic Usage (Manual)
```
"Create a PowerPoint about shadow environments"
"Make an Excel dashboard showing adoption metrics"
"Write a case study about the Surface feature development"
```

### Automated Usage (Recipes)
```
"Run the weekly digest recipe"
"Generate a case study from this session"
"Create release notes for the v2.0 tag"
```

## Local Configuration

For SharePoint deployment, copy `.env.local.example` to `.env.local` and set your path:

```bash
cp .env.local.example .env.local
# Edit .env.local with your SharePoint folder path
```

Then deploy with:
```bash
./deploy.sh                    # All decks
./deploy.sh my-deck.html       # Specific deck
```

---

@amplifier-module-stories:context/storyteller-instructions.md

---

@foundation:context/shared/common-system-base.md
