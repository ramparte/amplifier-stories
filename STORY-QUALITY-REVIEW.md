# Antagonistic Review: Amplifier Stories Quality Audit

**Date:** 2026-02-20
**Scope:** 82 published decks, 6 deep-dived, storyteller tool methodology
**Verdict:** Stories are visually polished but factually unreliable. The tool
prioritizes presentation over truth. Structural changes needed before republishing.

---

## Executive Summary

The amplifier-stories tool produces beautiful, well-structured HTML presentations
with strong visual design, responsive layouts, and consistent branding. The CSS
design system and presentation styles are genuinely excellent work.

The content, however, has serious problems:

1. **Fabricated or unverifiable metrics** appear in every deck reviewed
2. **No fact-checking gate** exists in the tool's methodology
3. **Impact claims lack baselines** - "100x faster" with no timing data
4. **Round-number syndrome** - suspiciously clean figures throughout (600, 700, 100x, 40%, 30%)
5. **Stories about inactive/disabled features** presented as current successes
6. **Single-author work presented as team efforts** without attribution
7. **The research agent is optional** - the storyteller can skip it entirely

If these decks were shown to an external audience, they would not survive
basic fact-checking. Several claims are provably wrong.

---

## Part 1: The Tool's Structural Weaknesses

### The Quality Checklist is 94% Visual

The storyteller's 18-item quality checklist contains exactly ONE accuracy item
("Velocity slide has accurate numbers"). The other 17 are CSS, layout, and
navigation checks. This ratio reveals the tool's priorities: **it optimizes
for looking good, not being true.**

### No Mandatory Research Gate

The story-researcher agent actually has a rigorous methodology - evidence-based
extraction, traceable metrics, explicit missing-data handling. But it's
**optional infrastructure**. The storyteller can (and does) skip it entirely
and generate decks from conversational context alone. There is no structural
enforcement that research happens before creation.

### No Source Citations in Output

No deck contains a "Sources" slide, footnotes, or "data as of" timestamps.
A reader cannot verify any claim in any deck. This is the single most
important missing feature.

### No Verification Step

The workflow is Research -> Design -> Create -> Save -> Deploy. There is no
**Verify** step between Create and Save. The human approval gate is for
visual review, not fact-checking (and humans reviewing pretty slides focus
on appearance).

---

## Part 2: Story-by-Story Fact-Check Results

### Story 1: Shadow Environments Deck

**Claim vs. Reality:**

| Claim in Deck | Ground Truth | Verdict |
|---------------|-------------|---------|
| "~2k Lines of Python" | 2,570 lines total (bundle content) | CLOSE - within range of "~2k" |
| "7 Days" to build | Foundation commits span Jan 7 - Feb 4 (28 days) | MISLEADING - compressed timeline |
| "Security hardened containers" | Docker/Podman with embedded Gitea | UNVERIFIABLE - no specifics given |
| Uses embedded Gitea for URL rewriting | Confirmed in actual code | ACCURATE |
| Repo: microsoft/amplifier-bundle-shadow | Exists (SAML-blocked, can't audit) | PLAUSIBLE |

**Grade: C+** - Technical architecture is accurately described, but the "7 days"
velocity claim is misleading and "security hardened" is marketing fluff.

---

### Story 2: Team Tracking Story

**Claim vs. Reality:**

| Claim in Deck | Ground Truth | Verdict |
|---------------|-------------|---------|
| "354 sessions processed successfully" | System is currently DISABLED (`enabled: false`) | MISLEADING |
| "600 unique capabilities mapped" | Suspiciously round; unverifiable since system is off | UNVERIFIABLE |
| "100x performance improvement" | No baseline timing data exists anywhere | FABRICATED metric |
| "3 people tracked across sessions" | Only 3 people in the system | ACCURATE but underwhelming |
| "144 projects identified" | 144 = 12^2, suspiciously round | SUSPICIOUS |
| "0 recipe crashes in production" | After how long? Duration unstated | MISLEADING |
| Commit 435d0d4 referenced | Used as credibility anchor, not for reference | ACCURATE but theatrical |

**Additional finding:** There are actually 5 separate "team tracking" implementations
by 4 different people across different repos. The story presents one of them as
"the" team tracking system while it's currently disabled.

**Grade: D** - The story describes a debugging journey that probably happened, but
the impact metrics are unverifiable-to-fabricated, and the system is currently off.

---

### Story 3: Deliberate Development Deck

**Claim vs. Reality:**

| Claim in Deck | Ground Truth | Verdict |
|---------------|-------------|---------|
| Four agents (planner, implementer, reviewer, debugger) | Confirmed in bundle | ACCURATE |
| "0 Gotchas Found" by validation | Self-assessment by the tool's own validator | MEANINGLESS |
| "Excellent agent descriptions" | Graded by the AI itself | SELF-PRAISE |
| Repo: ramparte/amplifier-bundle-deliberate-development | Confirmed | ACCURATE (but personal repo, not Microsoft) |
| Three-tier discovery architecture | Confirmed in code structure | ACCURATE |
| Two recipes: deliberate-design, feature-development | Actually 9 recipes exist | UNDERSTATED |

**Additional finding:** The entire bundle is in the `Inactive/` directory. It has
only 4 commits, all by a single author, over 11 days. Despite this, it's presented
as a mature methodology. The agents ARE still available in sessions (loaded from
the git URL), but the local copy is archived.

**Grade: C** - Technical claims are mostly accurate, but the self-validating
quality claims ("excellent! zero gotchas!") are embarrassing, and presenting
an inactive/archived project as a current capability is misleading.

---

### Story 4: Smoke Test Bundle Deck

**Claim vs. Reality:**

| Claim in Deck | Ground Truth | Verdict |
|---------------|-------------|---------|
| "700 Lines of YAML" | The feature is a SINGLE 290-line markdown file | WRONG - not even a bundle |
| "12 Test Phases" | Mock output lists only 11 test names but claims "12 passed" | INTERNAL INCONSISTENCY |
| "Bundle" (in the title) | It's an agent file, not a bundle | MISCHARACTERIZED |
| CLI tests ~30 sec, LLM tests ~3-5 min | Environment-dependent, unverified | UNVERIFIABLE |
| Repo: samueljklee/amplifier-bundle-smoke-test | Personal repo, not microsoft/ | ACCURATE but inconsistent org |

**Additional finding:** There are TWO separate presentation decks about this single
290-line file (`smoke-test-bundle-deck.html` and `smoke-test-bundle-presentation.html`
at identical byte sizes). Two decks for one file.

**Grade: D-** - Calling a 290-line agent file a "bundle" with "700 lines of YAML"
is factually wrong. The mock output has an internal count mismatch. Two decks
about one small file is padding.

---

### Story 5: Amplifier Architecture Deck

**Claim vs. Reality:**

| Claim in Deck | Ground Truth | Verdict |
|---------------|-------------|---------|
| "~7,800 lines" for amplifier-core | amplifier_core/ source = 8,134 lines | CLOSE (within ~4%) |
| "Linux solved this 40 years ago" | Linux is from 1991 (~35 years in 2026) | FACTUALLY WRONG |
| Five module types | 6 primary Protocols + 2 system Protocols = 8 total | APPROXIMATELY TRUE |
| Kernel deps: pydantic, tomli, pyyaml, typing-extensions | Verifiable in pyproject.toml | ACCURATE |
| "No LLM SDKs" in kernel | Confirmed | ACCURATE |
| Six repositories listed | Confirmed on GitHub | ACCURATE |
| claude-sonnet-4-20250514 model reference | Real Anthropic model ID | ACCURATE |

**Note:** The ecosystem overview context document claims "~2,600 lines" for the
kernel. The architecture deck claims "~7,800 lines." The actual number is 8,134
for full source (or 4,752 for kernel-proper without validation/). The ~2,600
figure is provably wrong by 3x. The ~7,800 figure is close to reality.

**Grade: B** - The most technically grounded deck. Most claims are verifiable
and approximately correct. The "40 years" error is sloppy but minor. The line
count discrepancy with other Amplifier docs (2,600 vs 7,800) suggests nobody
is checking consistency across materials.

---

### Story 6: Recipe Efficiency Week

**Claim vs. Reality:**

| Claim in Deck | Ground Truth | Verdict |
|---------------|-------------|---------|
| "8 Versions in 2 Days" | Title says "Week of January 27" - which is it? | SELF-CONTRADICTING |
| "40% Faster Execution" | No baseline measurements exist | UNVERIFIABLE |
| "30% Cost Reduction" | Cost of what? No specifics | UNVERIFIABLE |
| "12 stages -> 6 stages" | Exactly halved (12/2=6) | SUSPICIOUSLY CLEAN |
| "Brian's feedback" about 25-min demos | Brian who? No last name given | UNVERIFIABLE narrative device |
| "Efficiency Week" as an event | No burst of recipe commits visible in any repo's git history | NARRATIVE CONSTRUCT |
| v7.0 -> v8.0 progression | No version tags found in git to confirm | UNVERIFIABLE |

**Additional finding:** The "Efficiency Week" appears to be a retroactive
narrative applied to normal development work. The recipe bundle's commit
history shows continuous development from Dec 29 - Jan 28, not a concentrated
sprint. The story was committed on Jan 30 by Mollie Munoz.

**Grade: D** - The framing ("Brian said it was too slow, so we fixed it in a
week!") is a compelling story, but neither the triggering event nor the impact
metrics are verifiable. Every number on the impact slide is suspiciously round.

---

## Part 3: Cross-Cutting Patterns

### Pattern 1: Round Number Syndrome

| Deck | Suspicious Numbers |
|------|--------------------|
| Team Tracking | 600 capabilities, 100x improvement, 144 projects |
| Smoke Test | 700 lines of YAML |
| Recipe Efficiency | 40% faster, 30% cheaper, 12->6 stages |
| Shadow | 7 days, ~2k lines |

Real engineering metrics almost never land on round numbers. This pattern
suggests estimates presented as measurements, or outright fabrication for
narrative convenience.

### Pattern 2: Impact Claims Without Baselines

Every deck claims dramatic improvement. None provide:
- Before/after timing data
- Benchmark methodology
- Reproducible measurements
- Environment specifications

The pattern is: [impressive-sounding multiplier] + [no methodology] = unverifiable.

### Pattern 3: Stories About Dead Features

| Feature | Status | Deck Impression |
|---------|--------|-----------------|
| Team Tracking (marklicata) | Disabled (`enabled: false`) | Active, processing hundreds of sessions |
| Deliberate Development | In `Inactive/` directory | Current methodology |
| Smoke Test "Bundle" | Single 290-line file | Full bundle with 700 lines and 12 test phases |

Stories do not disclose the current status of the features they celebrate.

### Pattern 4: Attribution and Org Confusion

Three different GitHub orgs appear across decks without distinction:
- `microsoft/amplifier-*` (official)
- `ramparte/amplifier-*` (Sam's personal)
- `samueljklee/amplifier-*` (Samuel's personal)

The decks present everything as part of a unified "Amplifier ecosystem"
without distinguishing official from personal repos.

### Pattern 5: Single-Author Features Presented Without Attribution

| Feature | Dominant Author | Their Commit % |
|---------|----------------|----------------|
| amplifier-core | Brian Krabach | ~97% |
| Shadow Environments | Brian Krabach | 100% |
| Smoke Test | Brian Krabach | 100% |
| Recipe Bundle | Brian Krabach | 92% |
| Deliberate Development | Sam Schillace | 100% |
| Team Tracking hook | Salil Das | ~80% |

Decks don't attribute work to individuals. Features created entirely by
one person are presented as ecosystem achievements.

### Pattern 6: Deck Bloat

| Feature Complexity | Deck Slides | Proportion |
|-------------------|-------------|------------|
| 290-line file (smoke test) | 13 slides (x2 decks!) | Massively over-presented |
| 6,163-line bundle (deliberate dev) | 15 slides | 2+ filler slides |
| Recipe efficiency (normal iteration) | 7 slides | Appropriately sized |
| Core architecture (8,134 lines) | 15 slides | Justified by scope |

There is no correlation between feature significance and deck size.
The smoke test has two entire decks for a single file.

---

## Part 4: Scoring Summary

| Deck | Accuracy | Completeness | Storytelling | Overall |
|------|----------|-------------|-------------|---------|
| Architecture | B | B+ | B+ | **B** |
| Shadow Environments | C+ | B | B | **B-** |
| Deliberate Development | C | C | B- | **C** |
| Team Tracking | D | C- | B | **C-** |
| Recipe Efficiency | D | D+ | B+ | **D+** |
| Smoke Test Bundle | D- | D | C+ | **D** |

**Average across sample: C-**

The storytelling craft (narrative arc, visual design, pacing) is consistently
strong (B to B+). The accuracy drags every deck down. The tool is good at
telling stories. It's bad at telling true stories.

---

## Part 5: Recommendations

### Changes to the Storyteller Tool

**Priority 1: Mandatory Research Gate**
- The storyteller MUST invoke story-researcher before generating any deck
- Research output must be logged and referenced
- No deck creation without completed research artifact

**Priority 2: Source Citations**
- Every deck must include a "Sources & Methodology" slide (can be hidden/last)
- Every metric must cite its source (git command, API response, manual count)
- Include "Data as of: [date]" on any slide with metrics

**Priority 3: Accuracy Checklist Parity**
- Add at minimum these items to the quality checklist:
  - [ ] All numbers verified against actual git/tool output
  - [ ] Timeline dates confirmed against commit timestamps
  - [ ] No metrics without source evidence
  - [ ] Feature status (active/inactive/experimental) disclosed
  - [ ] Impact claims include baseline and methodology
  - [ ] Repository ownership (org) correctly attributed

**Priority 4: Second-Agent Verification**
- After deck creation, a fact-checker agent should compare claims to research
- Flag any claim not supported by research output
- Flag any suspiciously round numbers for manual review

**Priority 5: Feature Status Disclosure**
- Every deck should state: "Status: Active / Experimental / Archived"
- If a feature is disabled or in Inactive/, the deck must say so

### Republishing Strategy

**Do NOT bulk-republish all 82 decks without review.** That would compound the
problem by re-stamping inaccurate content.

Recommended approach:

1. **Triage the 82 decks into tiers:**
   - Tier 1 (keep as-is): Decks about concepts/philosophy (no factual claims)
   - Tier 2 (update metrics): Decks with specific numbers that can be refreshed
   - Tier 3 (rewrite): Decks with fundamental accuracy problems
   - Tier 4 (retire): Decks about dead/disabled features, duplicates

2. **Immediate actions:**
   - Remove the duplicate smoke-test deck (keep one, delete the other)
   - Add feature status badges to all decks
   - Add "Data as of" dates to all velocity/impact slides

3. **Before any new decks ship:**
   - Implement the mandatory research gate
   - Add the accuracy checklist items
   - Require source citations

4. **Consider a quality floor:**
   - Any deck scoring below C on accuracy should be pulled or rewritten
   - Based on this sample, that's ~50% of decks (extrapolating from 4/6)

---

## Appendix: Methodology

This review examined:
- All 82 published decks (inventory and categorization)
- The storyteller agent definition, instructions, and style guides
- The story-researcher agent methodology
- 6 representative decks selected for diversity of topic, size, and category
- Actual git history, line counts, commit logs, and file structures
  for the features described in each reviewed deck
- Cross-referencing of claims against ground truth from local repos
  and GitHub API queries

Ground truth was gathered from:
- `amplifier-core` local repo (134 commits, 52 Python files)
- `amplifier-foundation` local repo (shadow, smoke-test commits)
- `amplifier-bundle-recipes` local repo (77 commits)
- `amplifier-bundle-deliberate-development` in Inactive/ (4 commits)
- `amplifier-bundle-made-support` local repo (50 commits)
- `amplifier-teamdata` local repo (8 commits)
- `~/.amplifier/` configuration files (team-tracking.yaml, settings.yaml)
- GitHub API queries (where SAML didn't block access)