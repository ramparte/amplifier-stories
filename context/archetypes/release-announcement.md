# Story Archetype: Release Announcement

Multi-channel announcement for software releases, optimized for different platforms.

## When to Use

- Version releases (major, minor, patch)
- Feature launches
- Important updates
- Milestone achievements

## Narrative Structure

### Part 1: The Hook (10%)

**Grab attention immediately**
- Lead with the most exciting change
- Use a compelling number or achievement
- Create curiosity

**Examples:**
```markdown
# Major release
"Amplifier 2.0: Autonomous Storytelling Is Here"

# Feature release  
"Ship 3x Faster with Shadow Environments"

# Milestone
"10,000 AI Agents Spawned: Amplifier Ecosystem Hits Milestone"
```

### Part 2: What's New (40%)

**Highlight key changes**
- Top 3-5 features or improvements
- Brief description of each
- Visual examples or code snippets
- Links to detailed docs

**Format:**
```markdown
## 🚀 What's New

**Shadow Environments** - Test local changes safely
Test uncommitted code in isolated containers before pushing. Zero production incidents.

**Recipe Workflows** - Multi-step automation  
Orchestrate complex agent workflows with approval gates and resumability.

**Session Forking** - Parallel agent execution
Spawn child sessions with configuration overlays for efficient parallelism.
```

### Part 3: How to Get It (20%)

**Make upgrading obvious**
- Installation command
- Upgrade instructions
- Breaking changes (if any)
- Migration guide link (if needed)

**Example:**
```markdown
## 📦 Installation

\`\`\`bash
# New installation
uv tool install git+https://github.com/microsoft/amplifier@v2.0.0

# Upgrade from 1.x
amplifier update
# See MIGRATION.md for breaking changes
\`\`\`
```

### Part 4: What's Next (20%)

**Build anticipation**
- Roadmap preview
- Upcoming features
- Community involvement opportunities
- Thank contributors

**Example:**
```markdown
## 🔮 What's Next

Coming in 2.1:
• Real-time collaboration between sessions
• Advanced recipe debugging tools
• Community bundle marketplace

Want to contribute? We're looking for:
• Bundle creators
• Module developers
• Documentation writers

## 🙏 Thank You

Special thanks to our contributors: @user1, @user2, @user3

And to everyone who filed issues, tested features, and shared feedback.
```

### Part 5: Links and Resources (10%)

**Provide all relevant links**
- Release notes
- Changelog
- Migration guide
- Documentation
- Community channels

## Channel-Specific Adaptations

### GitHub Release Notes
**Length:** 500-800 words  
**Format:** Markdown with sections and emoji  
**Tone:** Professional, detailed, includes technical info

```markdown
## 🚀 Amplifier 2.0.0

Autonomous storytelling engine with multi-format content generation.

### ✨ Highlights
- 10 specialist agents for content creation
- 4 automated workflow recipes
- Professional templates for all formats
- Black background Keynote aesthetic

### 📦 What's Included
[Detailed changelog-style list]

### ⚠️ Breaking Changes
[List with migration paths]

### 📝 Full Changelog
See [CHANGELOG.md](CHANGELOG.md) for complete details.
```

### Blog Post Announcement
**Length:** 800-1200 words  
**Format:** Markdown with frontmatter  
**Tone:** Engaging, community-friendly

```markdown
---
title: "Amplifier 2.0: Your AI Assistant Just Got Superpowers"
date: 2026-01-18
tags: [release, announcement]
---

# Headline with Hook

[Engaging opening paragraph]

## The Big Picture

[What this release means]

## Diving In

[Detailed feature explanations with examples]

## Try It Today

[Getting started guide]

## What's Next

[Roadmap preview]
```

### Social Media

**Twitter/X Thread (8-12 tweets):**
```
1/ 🚀 Amplifier 2.0 is here!

Autonomous storytelling, 10 specialist agents, 4 automated workflows.

Everything you need to tell your development story - automatically.

2/ What's new? A LOT. 🧵

3/ 📊 Multi-Format Generation
Create presentations, docs, dashboards, and reports - all with consistent professional styling.

PowerPoint, Excel, Word, PDF, and HTML. One story, five formats.

4/ 🤖 10 Specialist Agents
- story-researcher: Automated data gathering
- content-strategist: Story planning
- technical-writer: Deep docs
- marketing-writer: Community content
[continue for all 10]

5/ ⚡ Automated Workflows
• Session → Case Study (in minutes)
• Git Tag → Complete Release Docs
• Weekly Ecosystem Digest (zero manual work)
• Blog Post Generator (from any feature)

6/ 📦 Getting Started

\`\`\`
uv tool install git+https://github.com/microsoft/amplifier@v2.0.0
\`\`\`

7/ 🔗 Resources
- Release Notes: [link]
- Migration Guide: [link]
- Examples: [link]

8/ 🙏 Thank You
To our amazing contributors and everyone who shared feedback.

This release is for you. Build something awesome! 💙
```

**LinkedIn Post:**
```
I'm thrilled to announce Amplifier 2.0 🎉

After months of development, we're releasing an autonomous storytelling engine that transforms how you document and share your AI development work.

What's included:
✅ 10 specialized agents for content creation
✅ 4 automated workflow recipes  
✅ Professional templates for all formats
✅ Multi-audience adaptation (technical, executive, community)

The vision: Your AI assistant doesn't just help you build software - it tells the story of how you built it. Automatically. Beautifully. For any audience.

Highlights:
• Session → Case Study recipe turns breakthrough sessions into shareable content
• Git Tag → Changelog automates all release documentation  
• Weekly Digest generates ecosystem updates with zero manual work
• Blog Post Generator creates community content from any feature

Ready to try it? [link to installation]

#AIEngineering #DeveloperTools #OpenSource #Productivity
```

**Discord/Teams Announcement:**
```markdown
@everyone 🚀 Amplifier 2.0 is live!

**TL;DR:** Autonomous storytelling engine with 10 specialist agents and 4 automated workflows.

**Quick highlights:**
- Multi-format content generation (PowerPoint, Excel, Word, PDF, HTML)
- Automated case studies from sessions
- Auto-generated release docs
- Weekly ecosystem digests
- Professional templates for everything

**Get it:**
\`uv tool install git+https://github.com/microsoft/amplifier@v2.0.0\`

**Learn more:**
- Release notes: [link]
- Migration guide: [link]
- Examples: [link]

Questions? Drop them in #support
Showcase your projects in #community-showcase!
```

## Release Communication Matrix

| Audience | Primary Channel | Format | Length | Tone |
|----------|----------------|--------|--------|------|
| Developers | GitHub Release | Markdown | 800 words | Technical, detailed |
| Community | Blog Post | Markdown | 1200 words | Engaging, accessible |
| Social | Twitter/X | Thread | 8-12 tweets | Punchy, exciting |
| Professional | LinkedIn | Post | 300 words | Professional, achievement-focused |
| Internal | Discord/Teams | Message | 200 words | Casual, celebratory |
| Media | Email | HTML | 600 words | Formal, newsworthy |

## Timing Strategy

### Pre-Release (T-7 days)
- Teaser posts
- "Coming soon" hints
- Build anticipation

### Release Day (T-0)
- GitHub release published
- Blog post live
- Social media threads
- Community announcements
- Email sent

### Post-Release (T+1 to T+7)
- Follow-up content (detailed tutorials)
- Community showcases
- Metrics tracking
- Response to questions

## Checklist

Before publishing release announcements:
- [ ] Version number is correct everywhere
- [ ] Installation/upgrade commands tested
- [ ] Links all work
- [ ] Breaking changes clearly highlighted
- [ ] Migration guide linked (if needed)
- [ ] Contributors credited
- [ ] Social media content ready for all platforms
- [ ] Timing coordinated across channels
- [ ] Announcement scheduled (if automated)

## Success Criteria

Release announcement succeeds when:
- Clear what's new and why it matters
- Upgrade path is obvious
- Breaking changes don't surprise anyone
- Community is excited and engaged
- Download/adoption numbers increase
- Feedback is positive and constructive

---

**Reference:** This archetype is used by release-manager agent for all version releases.
