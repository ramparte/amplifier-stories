TITLE: [FIX] Compaction O(n²) stall fixed (minutes-long turns now sub-second)

---

Long-running sessions no longer freeze for minutes on every LLM turn — a compaction stall that had grown past 6 minutes per turn now finishes in under a second (~500x faster)

What changed:
• Rewrote two compounding O(n²) hot loops in SimpleContextManager that re-scanned the entire message history for every removal/truncation candidate during compaction
• _truncate_tool_wave now tracks a lazy token baseline with O(1) per-message deltas; _remove_messages_with_protection precomputes per-message token lengths and a tool_call_id→indices map once per pass — pure loop-shape restructure, no caching layer, no architecture change
• Added a red/green regression test proving scaling dropped from 16.2x (quadratic) to 4.2x (linear) growth for a 4x message-count increase, plus a defensive budget guard so a negative compaction reserve falls back to the full budget instead of silently disabling compaction
• No behavioral changes — event shapes and compaction levels are unaffected

Try it: Pull the update and RESTART the process (a git pull alone won't hot-reload the already-imported module) — the next compaction on a large session drops from ~368s to 0.6–0.95s, verified live in the session that surfaced the bug

More info:
• PR: github.com/microsoft/amplifier-module-context-simple/pull/15
• Commit: aa8464c
• Repo: github.com/microsoft/amplifier-module-context-simple
