# Blog Post Generator - Test Example

Test the automated blog post generation from feature development data.

## Test Scenario

Generate a blog post about a specific Amplifier feature using git history and development data.

## Prerequisites

- Git repository with feature development history
- GitHub CLI authenticated for PR data
- Feature to write about (existing Amplifier feature)

## Test Data

**Feature to test:** "shadow environments" or "recipe workflows" or "session forking"

These features have:
- Clear git history
- Merged PRs with descriptions
- Measurable impact
- Code examples available

## Expected Inputs

```json
{
  "feature_name": "shadow environments",
  "target_audience": "community"
}
```

With PR number:
```json
{
  "feature_name": "recipe workflows",
  "pr_number": "123",
  "target_audience": "technical"
}
```

With technical appendix:
```json
{
  "feature_name": "session forking",
  "include_technical_appendix": true,
  "target_audience": "mixed"
}
```

## Expected Outputs

### 1. Blog Post
**Location:** `workspace/blog/posts/shadow-environments.md`

**Structure:**
```markdown
---
title: "Shadow Environments: Test Before You Push"
date: 2026-01-18
author: Amplifier Team
tags: [feature, testing, devex]
excerpt: "Test local changes in isolated containers before pushing to production"
---

# Engaging Headline

[Hook paragraph - grabs attention]

## The Problem

[Relatable pain point]

## The Solution

[How shadow environments work]

### Example Usage

\`\`\`bash
# Code example
amplifier shadow create --local ~/repos/my-lib:org/my-lib
\`\`\`

## The Impact

[Results and benefits with metrics]

## Try It Today

[Getting started guide]

## What's Next

[Future possibilities]
```

**Length:** 800-1200 words

### 2. Social Media Content
**Location:** `workspace/blog/social/shadow-environments-social.md`

**Includes:**
- Twitter/X thread (6-8 tweets)
- LinkedIn post (300-400 words)
- Discord/Teams announcement (150-200 words)

### 3. Technical Appendix (if requested)
**Location:** `workspace/docx/output/shadow-environments-technical.docx`

**Contents:**
- Architecture details
- Implementation notes
- Advanced usage patterns
- Integration guide

### 4. Auto-Opened
Blog post opens in default markdown editor.

## Validation Criteria

✅ **Feature research complete**
- Git history mined for feature commits
- PRs identified and descriptions extracted
- Code examples found
- Metrics calculated
- User feedback included (if available)

✅ **Blog post quality**
- Engaging headline
- Clear problem/solution structure
- Concrete code examples (tested)
- Quantified impact
- Clear call to action
- SEO-friendly structure
- 800-1200 words

✅ **Social media ready**
- Twitter thread punchy and engaging
- LinkedIn post professional
- Discord announcement friendly
- All ready to copy-paste

✅ **Technical accuracy**
- Code examples run without errors
- Links work
- API references current
- Metrics sourced

## Manual Test Steps

```bash
# 1. Run the recipe
amplifier tool invoke recipes operation=execute \
  recipe_path=stories:recipes/blog-post-generator.yaml \
  context='{"feature_name": "shadow environments", "target_audience": "community"}'

# 2. Check blog post (should auto-open)
cat workspace/blog/posts/shadow-environments.md

# 3. Review social media content
cat workspace/blog/social/shadow-environments-social.md

# 4. Verify code examples
# Extract code blocks and run them
grep -A5 '```bash' workspace/blog/posts/shadow-environments.md

# 5. Check SEO elements
# Title, description, tags, excerpt all present in frontmatter

# 6. Verify copied to docs/blog/posts/
ls -lh docs/blog/posts/
```

## Expected Runtime

- Feature research (git + PRs): 30-60 seconds
- Content planning: 15-30 seconds
- Blog post writing: 60-120 seconds
- Social media generation: 30-45 seconds
- Technical appendix (if requested): 60-90 seconds
- **Total:** 2.5-5 minutes (3-6 if including appendix)

## Success Indicators

- ✅ Blog post is engaging and accessible
- ✅ Code examples are complete and tested
- ✅ Metrics are specific and sourced
- ✅ Social media variants ready to post
- ✅ SEO elements properly formatted
- ✅ Technical accuracy validated
- ✅ Auto-opened for immediate review

## Test Variations

### Technical Audience
```bash
amplifier tool invoke recipes operation=execute \
  recipe_path=./recipes/blog-post-generator.yaml \
  context='{"feature_name": "recipe workflows", "target_audience": "technical"}'

# Expected: More code, deeper architecture, assumes expertise
```

### With Technical Appendix
```bash
amplifier tool invoke recipes operation=execute \
  recipe_path=./recipes/blog-post-generator.yaml \
  context='{"feature_name": "session forking", "include_technical_appendix": true}'

# Expected: Blog post + detailed Word doc with architecture
```

### Specific PR
```bash
amplifier tool invoke recipes operation=execute \
  recipe_path=./recipes/blog-post-generator.yaml \
  context='{"feature_name": "surface module", "pr_number": "456"}'

# Expected: Focuses on that specific PR's changes
```

## Failure Scenarios to Test

1. **Feature not found in git history**
   - Expected: Error with suggestions for similar features

2. **No significant commits/PRs**
   - Expected: Message that feature lacks enough material

3. **Missing output directories**
   - Expected: Directories created automatically

## Integration Test

After blog post created:

```bash
# Can we create a presentation from it?
amplifier run "create a PowerPoint presentation based on the shadow environments blog post"

# Can we adapt for different audience?
amplifier run "adapt the shadow environments blog post for an executive audience"

# Can we generate social media from it?
# (Already done by recipe, but can we regenerate with different tone?)
```

## Quality Verification

**Manual review checklist:**
- [ ] Headline is catchy and descriptive
- [ ] Opening hook grabs attention
- [ ] Problem is relatable
- [ ] Solution is clearly explained
- [ ] Code examples run without errors
- [ ] Metrics are impressive and accurate
- [ ] Call to action is clear
- [ ] Links all work
- [ ] Social media content matches blog tone
- [ ] SEO elements complete

## Distribution Test

After generation, verify content can be published:

```bash
# Copy to Jekyll/Hugo site
cp workspace/blog/posts/shadow-environments.md ~/blog/_posts/2026-01-18-shadow-environments.md

# Publish to GitHub Pages
cd ~/blog && git add _posts/ && git commit -m "post: shadow environments"

# Post social media
# Use the generated Twitter thread
```
