# Changelog

All notable changes to the amplifier-stories bundle will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] — 2026-04-22

### Changed (BREAKING)
- **Bundle namespace renamed from `amplifier-module-stories` to `stories`.** All `@amplifier-module-stories:` references must be updated to `@stories:` by consumers. The `amplifier-module-*` prefix is reserved for kernel modules; bundles use short names per Amplifier convention (see amplifier-bundle-recipes for the canonical example).
- **Restructured as thin bundle.** Agents, recipes, and context now declared in `behaviors/stories.yaml` rather than inline in `bundle.md`. The root bundle includes the behavior, which is the single source of truth. External bundles can compose just the behavior without the full root bundle.
- **Added explicit dependency on `amplifier-foundation`.** Previously the `includes:` block was empty; the bundle now correctly declares its foundation dependency.

### Added
- `behaviors/stories.yaml` — capability manifest composing 12 agents, 4 recipes, and the awareness context.
- `context/stories-awareness.md` — delegation pointer injected into parent sessions when the behavior is composed.

### Migration
External bundles or sessions that reference this bundle must update:
1. Git URL references and include paths (if any) — no change needed; repo URL is unchanged.
2. All `@amplifier-module-stories:` @mentions → `@stories:`.
3. If previously importing individual agents from `bundle.md`, they can now import `stories:behaviors/stories` to get the full capability.

## [1.0.0] - 2026-01-18

### Added
- Multi-format storytelling support (HTML, PowerPoint, Excel, Word, PDF)
- Integration with Anthropic skills library (pptx, xlsx, docx, pdf)
- Professional PowerPoint template based on Surface-Presentation.pptx
- Organized workspace structure for each output format
- Auto-open functionality for all generated files
- Comprehensive README with usage examples and dependencies
- Tools directory with session analysis utilities
- PowerPoint template specification with Microsoft corporate design
- File organization rules for each format
- Complete dependency documentation

### Changed
- Extended storyteller agent from HTML-only to 5 output formats
- Simplified PowerPoint workflow to use reusable template specification
- Updated .gitignore with comprehensive patterns for all workspaces
- Improved file organization with format-specific directories

### Fixed
- PowerPoint quality issues by requiring template adherence
- File organization - now uses proper workspace directories
- Missing gitignore patterns for Python cache and data files

## [0.1.0] - Initial Release

### Added
- Initial storyteller agent for HTML presentations
- "Useful Apple Keynote" style HTML decks
- SharePoint deployment script
- GitHub Pages hosting support
- Collection of existing presentation decks
