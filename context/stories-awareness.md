# Stories Capability

You have access to the `stories` bundle for creating content from Amplifier sessions, projects, and work artifacts.

## When to Use

Delegate to the stories agents when the user wants to:
- Turn a session into a case study, blog post, or executive briefing
- Generate release notes, weekly digests, or changelogs
- Produce HTML presentation decks or PDF handouts
- Adapt existing content across formats or audiences

## Agent Dispatch

| Task | Agent |
|------|-------|
| HTML/PDF presentation decks (canonical renderer) | `stories:storyteller` |
| YAML-first deck creation via deck engine | `stories:storyteller2` |
| Research across session transcripts for narrative material | `stories:story-researcher` |
| Long-form technical documentation | `stories:technical-writer` |
| Marketing copy, case studies, landing-page content | `stories:marketing-writer` |
| Executive briefings and status reports | `stories:executive-briefer` |
| Release notes and changelogs | `stories:release-manager` |
| Structured case-study format | `stories:case-study-writer` |
| Data narratives from metrics/sessions | `stories:data-analyst` |
| Converting content across formats | `stories:content-adapter` |
| Blog posts, weekly digests, social posts | `stories:community-manager` |
| Strategic content planning | `stories:content-strategist` |

## Recipes

For multi-step workflows, prefer the recipes in this bundle (see `stories:recipes/`) over ad-hoc orchestration:
- `session-to-case-study` — turn a session into a case study with approval gates
- `blog-post-generator` — produce a blog post from a topic prompt
- `git-tag-to-changelog` — generate release notes from a git tag range
- `weekly-digest` — summarize a week of work

## Notes

Delegate to specialist agents rather than doing content work inline — they carry format-specific context, style guides, and quality heuristics.
