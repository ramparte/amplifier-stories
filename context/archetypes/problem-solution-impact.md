# Story Archetype: Problem/Solution/Impact

Classic narrative structure for feature launches and improvements.

## When to Use

- Feature launches
- Performance improvements
- Bug fixes with interesting solutions
- Process improvements

## Narrative Structure

### Act 1: The Problem (30%)

**What pain exists?**
- Describe the user's pain point
- Quantify the cost (time, money, frustration)
- Show why existing solutions don't work
- Make it relatable

**Example:**
"Developers were spending 3 hours debugging provider integration issues that broke production. The problem? No way to test local changes before pushing. Existing approaches (manual mocking, staging environments) were either incomplete or too slow."

### Act 2: The Solution (40%)

**How we solved it**
- Introduce the capability
- Explain the approach (high-level first, then details)
- Show how it works with examples
- Highlight what makes it effective

**Example:**
"Shadow Environments let you test local code changes in isolated containers before pushing. Create a shadow with your uncommitted changes, run your full test suite, see exactly what breaks - all without touching production or staging."

**Code Example:**
```bash
# Create shadow with local changes
amplifier shadow create --local ~/repos/my-lib:org/my-lib

# Run tests
amplifier shadow exec <id> "pytest tests/"

# Verify before pushing
amplifier shadow exec <id> "amplifier run 'test the integration'"
```

### Act 3: The Impact (30%)

**Results and benefits**
- Quantify improvements
- Show before/after comparison
- Include user testimonials if available
- Paint the future enabled

**Example:**
"Results: 80% reduction in debugging time, zero production incidents in 3 months, teams shipping 3 days faster. 'I can finally sleep at night knowing my changes won't break prod,' one developer said."

## Slide/Section Mapping

### For PowerPoint (10-15 slides)
1. **Title** (1 slide) - Feature name + one-line value prop
2. **Problem** (2-3 slides) - Pain point, cost, why it matters
3. **Solution** (5-7 slides) - How it works, examples, key features
4. **Impact** (2-3 slides) - Metrics, comparison, testimonials
5. **CTA** (1 slide) - Getting started, links

### For Word (1500-2500 words)
- **Introduction** (150 words) - Hook + context
- **The Problem** (400 words) - Detailed pain point analysis
- **The Solution** (900 words) - How it works, examples, architecture
- **The Impact** (350 words) - Results, metrics, future possibilities
- **Conclusion** (200 words) - Summary, call to action

### For Blog Post (800-1200 words)
- **Hook** (100 words) - Relatable opening, grab attention
- **Problem** (250 words) - Pain point with examples
- **Solution** (500 words) - How it works, code example
- **Impact** (200 words) - Results and benefits
- **Try It** (150 words) - Getting started guide

### For Executive PDF (1 page)
- **Headline** - Business value statement
- **Problem** (3 bullets) - Cost, risk, opportunity lost
- **Solution** (3 bullets) - What it does, how it helps
- **Impact** (3 metrics) - Time saved, cost reduced, risk eliminated

## Key Principles

### Lead with Empathy
Start with the pain, not the solution. Readers need to recognize their problem before caring about your solution.

### Make It Concrete
- Real examples > abstract descriptions
- Specific numbers > vague claims
- User quotes > feature lists
- Before/after > "this is better"

### Show, Don't Tell
```markdown
# Weak
"Shadow environments make testing easier."

# Strong
"Before: 3 hours debugging a broken production deploy.
After: 5 minutes testing in shadow, catching the issue before it shipped."
```

### End with Action
Every story needs a clear next step:
- "Try it today with..."
- "Get started in 2 minutes..."
- "Read the full guide at..."
- "Join the discussion at..."

## Checklist

Before publishing a Problem/Solution/Impact story:
- [ ] Problem is relatable and quantified
- [ ] Solution is clearly explained with examples
- [ ] Impact has specific metrics (before/after)
- [ ] Code examples are tested and working
- [ ] User quotes included (if available)
- [ ] Call to action is clear
- [ ] Story flows naturally from pain → relief
- [ ] Appropriate length for format

## Examples

**Good headlines for this archetype:**
- "Shadow Environments: Test Before You Push"
- "Recipe Cancellation: Take Back Control"
- "Session Forking: Parallelize Your Work"

**Good metrics for impact:**
- "1,500 → 0 lines of boilerplate"
- "3 weeks → 2 days development time"
- "80% reduction in debugging time"
- "Zero production incidents since deployment"

---

**Reference:** This archetype is used in most Amplifier Stories HTML presentations (see docs/).
