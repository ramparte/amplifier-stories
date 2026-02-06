# Session to Case Study - Test Example

This example demonstrates how to test the session-to-case-study recipe.

## Test Scenario

Convert a real Amplifier session into a case study.

## Test Data

**Session file:** Use a real session from `~/.amplifier/sessions/`

Example session characteristics:
- Duration: > 15 minutes
- Tool calls: > 10
- Agent delegations: > 2
- Successful outcome: Yes
- Complex problem: Yes (multiple iterations)

## Expected Inputs

```json
{
  "session_file": "~/.amplifier/sessions/2026-01-17/events.jsonl",
  "output_name": "shadow-environments-implementation"
}
```

## Expected Outputs

### 1. Word Document
**Location:** `workspace/docx/output/case-study-shadow-environments-implementation.docx`

**Contents:**
- Title: "[User] Uses Amplifier to [Achievement]"
- The Challenge section with context
- The Approach section with agents used and key moments
- The Results section with metrics (time, iterations, outcome)
- Key Takeaways section with applicable patterns

### 2. Metrics Extracted
- Session duration in minutes
- Total tool calls
- Agents invoked (list)
- Iterations count
- Success indicator

### 3. Auto-Opened
Document opens in Word automatically for review.

## Validation Criteria

✅ **Recipe executes successfully**
- All 4 phases complete without errors
- story-researcher extracts accurate metrics
- content-strategist correctly evaluates worthiness
- case-study-writer generates compelling narrative

✅ **Output quality**
- Word document uses template correctly
- Metrics are quantified and sourced
- Narrative flows logically
- Technical details are accurate
- File auto-opens

✅ **Edge cases handled**
- If session not worthy → graceful message, no document created
- Missing session file → clear error message
- Malformed events.jsonl → error with recovery suggestion

## Manual Test Steps

```bash
# 1. Find a good session to test with
ls -lt ~/.amplifier/sessions/*/events.jsonl | head -5

# 2. Run the recipe
amplifier tool invoke recipes operation=execute \
  recipe_path=stories:recipes/session-to-case-study.yaml \
  context='{"session_file": "~/.amplifier/sessions/2026-01-17/events.jsonl"}'

# 3. Verify output
ls -lh workspace/docx/output/

# 4. Check document opened automatically
# Word should have launched with the case study

# 5. Review content
# - Are metrics accurate?
# - Does narrative make sense?
# - Are key moments captured?
# - Is it case-study worthy?
```

## Expected Runtime

- Session analysis: 30-60 seconds
- Strategy evaluation: 10-20 seconds
- Case study writing: 60-120 seconds
- Total: 2-3 minutes for typical session

## Success Indicators

- ✅ Document created and auto-opened
- ✅ Metrics match session reality
- ✅ Narrative is engaging and accurate
- ✅ Usable without manual editing
- ✅ Professional quality

## Failure Scenarios to Test

1. **Empty session file**
   - Expected: Error message, no crash
   
2. **Session not worthy** (< 10 tool calls)
   - Expected: Message explaining why, no document created

3. **Malformed JSON**
   - Expected: Parse error with helpful message

4. **Missing output directory**
   - Expected: Directory created automatically

## Integration Test

Can this case study be adapted to other formats?

```bash
# After case study is created, try content adaptation
amplifier run "adapt workspace/docx/output/case-study-X.docx to a blog post"

# Should use content-adapter agent to transform
```
