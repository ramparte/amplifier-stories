# Story Regeneration Progress

## Tool Changes (COMPLETE)
- agents/storyteller.md - Added mandatory research gate, antagonistic review checklist, Sources slide requirement
- agents/story-researcher.md - Marked as REQUIRED in pipeline
- context/storyteller-instructions.md - Added Sources slide template, expanded quality checklist (accuracy section)

## Regenerated Decks (11/80)

| # | Deck | Status | Key Corrections |
|---|------|--------|----------------|
| 1 | shadow-environments-deck.html | DONE | ~2k→7,226 lines, 7→29 days, added Alpha badge |
| 2 | smoke-test-bundle-deck.html | DONE | "bundle"→agent file, 700→290 lines, deleted duplicate |
| 3 | recipe-efficiency-week.html | DONE | Doc-gen recipe never existed, reframed as infra maturation |
| 4 | amplifier-architecture-deck.html | DONE | ~7,800→8,134 lines, 5→6 protocols, "40 years"→~35 |
| 5 | team-tracking-story.html | DONE | Removed 6 fabricated claims, added "Disabled" badge |
| 6 | deliberate-development-deck.html | DONE | Added "Archived" badge, removed self-validating claims |
| 7 | attention-firewall-deck.html | DONE | "AI-powered"→rule-based, real DB metrics added |
| 8 | notifications-deck.html | DONE | Fabricated velocity stats removed, real code metrics |
| 9 | amplifier-modes-deck.html | DONE | Wrong mode name fixed, 3→4 policy tiers, 13 modes found |
| 10 | superpowers-deck.html | DONE | (rate-limited but file was modified) |
| 11 | what-is-amplifier.html | DONE | ~2,600→1,344 kernel lines, 5→6 module types |

## Remaining Decks (~69)

### Not yet processed:
- 20260130-amplifier-sdk.html
- 20260130-source-driven-content-generation.html
- agents-behavior-capabilities.html
- amplifier-app-benchmarks-story.html
- amplifier-bundle-containers.html
- amplifier-forge-deck.html
- amplifier-full-stack-deployed-app.html
- amplifier-in-action.html
- amplifier-swarm-deck.html
- amplifier-tui-showcase.html
- amplifier-ux-analyzer.html
- amplifier-voice-deck.html
- amplifier-vscode-extension.html
- azure-zap-story.html
- bbs-agent-collaboration.html
- best-practices-patterns.html
- browser-automation-deck.html
- browser-bundles-announcement.html
- bundle-orchestration-deck.html
- bundles-and-agents.html
- cli-quality-collaboration.html
- context-inheritance-deck.html
- cortex-amplifier-presentation.html
- cost-optimization-deck.html
- cross-session-intelligence-deck.html
- database-tool-deck.html
- design-intelligence-enhanced-deck.html
- design-intelligence-feedback.html
- diagrams-tool-deck.html
- distributed-ai-network-deck.html
- distributed-amplifier-network-gaming.html (DUPLICATE of above - delete one)
- ecosystem-audit-deck.html
- eval-recipes-v0.0.28-v0.0.31-release-deck.html
- exo-protocol-deck.html
- four-prompts-to-serverless-ai.html
- getting-started-guide.html
- github-actions-tool-deck.html
- kepler-refactor-deck.html
- language-dev-bundles-deck.html
- lazy-module-activation-deck.html
- longbuilder-deck.html
- m365-collaboration-journey.html
- m365-enterprise-sandbox-deck.html
- m365-hackathon-deck.html
- made-support-bundle-deck.html
- marathon-session-deck.html
- multi-provider-swarms-deck.html
- nexus-phase-0-story.html
- polyglot-amplifier-deck.html
- pr-review-recipes.html
- presentation-internet-archive.html
- presentation-ocr-rust-performance.html
- recipes-workflows.html
- recipe-runner-mode-story.html
- runtime-sdk-tui-journey.html
- rust-code-intel-deck.html
- rust-dev-bundle-deck.html
- self-improving-amplifier-deck.html
- session-forking-deck.html
- stories-bundle-overview.html
- story-50-percent-rule.html
- story-making-llms-reliable.html
- story-observers-bundle.html
- story-proving-parallel-execution.html
- story-three-branches-one-recipe.html
- submit-pr-story-deck.html
- tui-tester-innovation-story.html
- vibecoding-deck.html
- vision-roadmap.html
- withamplifier-site-deck.html

## Regeneration Instructions for Each Deck

Each deck follows the same pipeline:
1. Read updated storyteller instructions (agents/storyteller.md, context/storyteller-instructions.md, context/presentation-styles.md)
2. Read existing deck to extract topic, accent color, narrative
3. Research topic with actual git commands (commits, line counts, contributors, dates)
4. Regenerate with: Sources slide, feature status badge, contributor attribution, verified metrics
5. Antagonistic review: verify every number, no round-number inflation, no self-validating claims
6. Write to docs/

## Known Duplicates to Delete
- smoke-test-bundle-presentation.html (DELETED - was identical to smoke-test-bundle-deck.html)
- distributed-amplifier-network-gaming.html (same title+size as distributed-ai-network-deck.html - DELETE ONE)

## Rate Limit Notes
- Hit rate limits at ~11 parallel deck regenerations
- Each deck regeneration consumes significant tokens (reading existing HTML + research + generating new HTML)
- Sustainable pace: 2-3 parallel delegations with pauses between batches