# Story Archetype: Technical Deep-Dive

Comprehensive technical exploration for developers who want deep understanding.

## When to Use

- Complex architectural decisions
- Performance optimization deep dives
- Security implementations
- Novel technical approaches
- API design and contracts

## Narrative Structure

### Part 1: Context and Requirements (15%)

**What we're building and why**
- Technical problem statement
- Requirements and constraints
- Success criteria
- Existing approaches and limitations

**Example:**
"Agent delegation in Amplifier requires spawning child sessions with configuration overlays. Requirements: preserve parent context, allow config inheritance, maintain session isolation, enable result passing. Existing subprocess approaches lose context; thread-based approaches break isolation."

### Part 2: Architecture Overview (20%)

**System design at high level**
- Key components and their roles
- Data flows
- Module contracts and boundaries
- Design decisions and trade-offs

**Diagrams:**
```
┌──────────────┐
│ Parent       │
│ Session      │
└───────┬──────┘
        │ spawn(config_overlay)
        ▼
┌──────────────┐
│ Child        │
│ Session      │
│ (merged cfg) │
└──────────────┘
```

### Part 3: Implementation Details (40%)

**How it actually works**
- Code walkthrough of critical paths
- Key algorithms or data structures
- Error handling and edge cases
- Integration points with other systems
- Performance considerations

**Code Examples (real, tested):**
```python
def spawn_session(self, config_overlay, instruction):
    # Merge configurations
    merged_config = self._merge_configs(
        self.base_config,
        config_overlay
    )
    
    # Create child session with parent link
    child = AmplifierSession(
        config=merged_config,
        parent_id=self.session_id
    )
    
    # Execute and return result
    return child.run(instruction)
```

### Part 4: Performance and Optimization (15%)

**Making it fast and efficient**
- Benchmarks and profiling results
- Optimization techniques applied
- Trade-offs made
- Resource usage characteristics

**Metrics:**
```
Session spawn time:     45ms (cold) → 12ms (warm)
Memory overhead:        +15MB per child
Context passing:        <1ms (serialization)
Max depth:              10 levels (tested)
```

### Part 5: Testing and Validation (10%)

**How we know it works**
- Test strategy (unit, integration, e2e)
- Edge cases covered
- Failure modes tested
- Performance regression tests

**Example:**
```python
def test_config_overlay_preserves_parent():
    parent = Session(provider="anthropic")
    child = parent.spawn(provider="openai")
    
    assert parent.provider == "anthropic"  # Unchanged
    assert child.provider == "openai"       # Overridden
```

## Format-Specific Adaptations

### For Word (3000-5000 words)
**Structure:**
- Executive Summary (200 words)
- Table of Contents (auto-generated)
- Context (500 words)
- Architecture (1000 words with diagrams)
- Implementation (1500 words with code)
- Performance (500 words with benchmarks)
- Testing (300 words)
- Appendix (references, glossary)

**Template:** `workspace/docx/templates/technical-doc-template.js`

### For PowerPoint (20-30 slides)
**Structure:**
- Title slide
- Context (2-3 slides)
- Architecture overview (3-4 slides with diagrams)
- Implementation walkthrough (8-12 slides with code)
- Performance results (2-3 slides with charts)
- Testing approach (2 slides)
- Q&A slide

**Templates:**
- `slide-title.html` - Opening
- `slide-content.html` - Explanations
- `slide-code.html` - Implementation details
- `slide-metrics.html` - Performance numbers
- `slide-comparison.html` - Before/after architecture

### For Blog Post (1500-2000 words)
**Structure:**
- Hook with interesting technical problem (200 words)
- Architecture overview with diagram (400 words)
- Key implementation highlights (700 words)
- Performance and results (300 words)
- Try it yourself (200 words)

**Tone:** Deep but accessible - explain complex ideas clearly

## Code Example Principles

### Complete and Runnable
```python
# Good - shows full context
from amplifier import Session

session = Session(provider="anthropic")
child = session.spawn(
    config_overlay={"model": "claude-opus-4"},
    instruction="Analyze this architecture"
)
result = child.run("Is this design sound?")
print(result)
```

### Show, Don't Just Describe
```markdown
# Weak
"The merge function combines parent and child configs."

# Strong
"Config merging uses dictionary overlay semantics:

\`\`\`python
def _merge_configs(parent, overlay):
    merged = parent.copy()
    merged.update(overlay)  # Child wins on conflicts
    return merged
\`\`\`

This means child can override any parent setting while preserving others."
```

### Include Error Cases
```python
# Show what happens when things go wrong
try:
    result = session.spawn(invalid_config)
except ConfigValidationError as e:
    print(f"Config invalid: {e}")
    # Agent gets clear error, not mysterious failure
```

## Technical Depth Guidelines

### Always Include
- File paths and line numbers for code references
- Exact type signatures for APIs
- Performance measurements (not estimates)
- Failure modes and error handling
- Links to source code

### Diagrams to Use
- Architecture diagrams (component relationships)
- Sequence diagrams (interaction flows)
- State diagrams (lifecycle stages)
- Data flow diagrams (where data goes)

### Benchmarks to Show
- Before/after performance (with workload description)
- Memory usage (peak and average)
- Resource overhead (CPU, I/O)
- Scaling characteristics (1, 10, 100, 1000)

## Checklist

Before publishing a Technical Deep-Dive:
- [ ] All code examples are tested and run
- [ ] File:line references are current
- [ ] Architecture diagrams are accurate
- [ ] Performance numbers are recent (<1 week)
- [ ] API signatures match actual implementation
- [ ] Error handling is documented
- [ ] Links to source code work
- [ ] Assumptions are explicit
- [ ] Trade-offs are explained

## Success Criteria

Technical deep-dive succeeds when:
- A developer can implement similar pattern from your docs
- All claims are backed by code/data evidence
- Reader understands both WHAT and WHY
- Common questions are preemptively answered
- Reader can debug issues using your guide

## Examples

**Good headlines for this archetype:**
- "Session Forking: Architecture and Implementation"
- "Under the Hood: How Recipe Resumability Works"
- "Provider Selection: Load Balancing and Failover Design"

**Good opening hooks:**
- "Ever wondered how Amplifier agents can spawn child sessions without losing context?"
- "The session forking implementation is deceptively simple - 200 lines that enable powerful patterns."
- "Let's dive into the architecture that makes recipe resumability possible."

---

**Reference:** Use this archetype when the audience wants to understand the implementation, not just use it.
