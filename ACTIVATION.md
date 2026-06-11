# Bundle Activation Guide

**As of v3.0.0, this bundle is named `stories`** (renamed from `amplifier-module-stories` — the `amplifier-module-*` prefix is reserved for Python kernel modules; bundles use short names per Amplifier convention).

## Update Your Settings

If you were previously using this bundle under its old name, edit `~/.amplifier/settings.yaml`:

```yaml
bundle:
  active: amplifier-module-stories  # OLD (pre-v3.0.0)
```

Change to:

```yaml
bundle:
  active: stories  # NEW (v3.0.0+)
```

## First-Time Activation

Add to `~/.amplifier/settings.yaml`:

```yaml
bundle:
  active: stories
```

Or load directly from the git repository:

```yaml
bundle:
  active: git+https://github.com/ramparte/amplifier-stories@master
```

## Restart Amplifier

```bash
# Exit current session
exit

# Start new session
amplifier
```

## Verify Activation

In the new session, run:

```
list available agents
```

You should see 12 agents:

| Agent | Purpose |
|-------|---------|
| `storyteller` | HTML/PDF presentation decks (canonical renderer) |
| `storyteller2` | YAML-first deck creation via deck engine |
| `story-researcher` | Research across session transcripts |
| `content-strategist` | Strategic content planning |
| `technical-writer` | Long-form technical documentation |
| `marketing-writer` | Marketing copy, case studies, landing pages |
| `executive-briefer` | Executive briefings and status reports |
| `release-manager` | Release notes and changelogs |
| `case-study-writer` | Structured case-study format |
| `data-analyst` | Data narratives from metrics/sessions |
| `content-adapter` | Converting content across formats |
| `community-manager` | Blog posts, weekly digests, social posts |

## Migration Notes for v3.0.0

If you have existing bundles, recipes, or sessions that reference `@amplifier-module-stories:`, update them to `@stories:`. The repository URL is unchanged — only the bundle's internal name and namespace have changed.

## Troubleshooting

**"Bundle not found" error:**
- Check `settings.yaml` has `active: stories` (not the old name)
- Verify the bundle is discoverable in your configured bundle paths
- Try the git URL method if local-path resolution is failing

**"Agents not loading" error:**
- Restart Amplifier after changing `settings.yaml`
- Run `list available agents` to confirm the 12 agents appear
- Check that `behaviors/stories.yaml` is intact (it's the single source of truth for agent declarations as of v3.0.0)

**"Skills not found" error:**
- Verify your skills directory configuration in `settings.yaml`
- Restart after adding skills configuration
