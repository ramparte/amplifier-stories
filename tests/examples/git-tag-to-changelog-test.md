# Git Tag to Changelog - Test Example

Test the automated release documentation generation recipe.

## Test Scenario

Create complete release documentation from a git tag.

## Prerequisites

Repository must have:
- At least 2 tags (to calculate diff)
- Commits between tags
- Conventional commit messages (feat:, fix:, etc.)

## Test Data

**Tag to test:** Latest tag in amplifier-module-stories repository

```bash
# Check existing tags
git tag -l --sort=-creatordate | head -5

# For testing, can create a test tag
git tag -a v2.0.0-test -m "Test release"
```

## Expected Inputs

```json
{
  "tag_name": "v2.0.0",
  "repo_path": "."
}
```

## Expected Outputs

### 1. CHANGELOG.md Entry
**Location:** Updated CHANGELOG.md in repo root

**Format:**
```markdown
## [2.0.0] - 2026-01-18

### Added
- Multi-format storytelling support (PowerPoint, Excel, Word, PDF)
- 10 specialist agents for autonomous content creation
- 4 automated workflow recipes
- Professional templates for all formats

### Changed
- Bundle renamed to amplifier-module-stories
- Workspace structure consolidated

### Fixed
- Code block whitespace formatting in HTML presentations
- Auto-open functionality for all formats
```

### 2. GitHub Release Notes
**Location:** `workspace/releases/v2.0.0-release-notes.md`

**Includes:**
- 🚀 Highlights section
- 📦 What's New with details
- 🐛 Bug Fixes
- ⚡ Performance improvements
- 📝 Installation instructions
- 🙏 Contributors

### 3. Migration Guide (if breaking changes)
**Location:** `workspace/docx/output/migration-guide-v2.0.0.docx`

**Only created if:** Breaking changes detected in commits

### 4. Announcement Content
**Location:** `workspace/blog/releases/v2.0.0-announcement.md`

**Includes:**
- Blog post (Markdown)
- Social media snippets (Twitter, LinkedIn)

### 5. Git Branch with PR
**Branch:** `release-v2.0.0-docs`
**PR:** Opened automatically with all generated files

## Validation Criteria

✅ **Commit parsing**
- All commits since last tag extracted
- Semantic types correctly categorized
- Breaking changes identified
- PR/issue links extracted

✅ **CHANGELOG format**
- Follows Keep a Changelog specification
- Version and date correct
- Sections properly organized (Added/Changed/Fixed)
- Links work

✅ **Release notes**
- Engaging and complete
- Highlights most important changes
- Installation instructions clear
- Contributors credited

✅ **Automation**
- PR created successfully
- All files committed
- Ready for review

## Manual Test Steps

```bash
# 1. Ensure you have tags
git tag -l

# 2. Create test tag if needed
git tag v2.0.0-test

# 3. Run the recipe
amplifier tool invoke recipes operation=execute \
  recipe_path=stories:recipes/git-tag-to-changelog.yaml \
  context='{"tag_name": "v2.0.0-test"}'

# 4. Verify CHANGELOG.md was updated
git diff CHANGELOG.md

# 5. Check workspace files
ls -lh workspace/releases/
ls -lh workspace/blog/releases/

# 6. Verify PR was created
gh pr list | head -3

# 7. Review the PR
gh pr view <number>
```

## Expected Runtime

- Tag validation: 5 seconds
- Commit extraction: 10-20 seconds
- Analysis: 30-45 seconds
- Documentation generation: 60-90 seconds
- PR creation: 10-15 seconds
- **Total:** 2-3 minutes

## Success Indicators

- ✅ CHANGELOG.md has new entry
- ✅ Release notes are comprehensive
- ✅ Migration guide created (if breaking changes)
- ✅ PR opened and reviewable
- ✅ All commits categorized correctly
- ✅ Ready to publish

## Failure Scenarios to Test

1. **Tag doesn't exist**
   - Expected: Clear error, suggest `git tag -l`

2. **No previous tag (initial release)**
   - Expected: Uses all commits since first commit

3. **No commits since last tag**
   - Expected: Message that no changes to document

4. **PR creation fails** (permission issue)
   - Expected: Files still generated, manual PR instructions provided

## Integration Test

After release docs are generated:

```bash
# Can we adapt the release notes to different formats?
amplifier run "create a PowerPoint presentation from the v2.0.0 release notes"

# Can we extract key metrics for a dashboard?
amplifier run "create an Excel dashboard showing release statistics from v2.0.0 commits"
```

## Cleanup

```bash
# Remove test tag after testing
git tag -d v2.0.0-test

# Delete test branch if created
git branch -D release-v2.0.0-test-docs
```
