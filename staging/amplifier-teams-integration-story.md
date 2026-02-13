---
title: "Building on Amplifier: When Architecture Should Follow Intent"
date: 2026-02-13
author: Amplifier Team
tags: [case-study, teams, integration, architecture]
---

# Building on Amplifier: When Architecture Should Follow Intent

"I want a Teams integration for Amplifier."

Simple request, right? But what does that *actually* mean? A chat extension? A standalone bot? An app that lives in Copilot? This is the story of how we built the Teams integration—and why the journey from idea to working solution taught us more than the destination.

## Act 1: The Declarative Agent Path

When you hear "Teams integration" in 2026, the shiny new option is Microsoft 365 Copilot's declarative agent extensions. It's the fastest path: pure JSON configuration, no custom code, works across Teams, Outlook, and the entire M365 ecosystem. 

We dove in, creating JSON manifests for the Teams app package. It felt clean. Declarative. Modern.

Then came the validation marathon.

### The Marathon Nobody Wants to Run

Building software means encountering errors. But schema validation errors? Those teach you things you didn't know you needed to know.

**Lesson 1: Schema versions evolve fast.** We started with v1.17. The platform wanted v1.24. Every version brings subtle changes in what's required, what's deprecated, what's newly possible.

**Lesson 2: File naming is semantic, not cosmetic.** It's `declarativeAgent.json`, not `declarative-copilot.json`. The manifest loader doesn't fuzzy-match. Character-for-character precision matters.

**Lesson 3: Icon formats have opinions.** PNG, not SVG. Specific dimensions. Transparent backgrounds. These constraints aren't arbitrary—they ensure consistency across the platform.

**Lesson 4: IDs mean different things in different contexts.** The `id` field in your manifest references your app. The `id` field in your declarative agent JSON is an internal identifier. Mix them up, and validation fails with cryptic messages.

**Lesson 5: Build hygiene prevents contamination.** Clean your output directories between builds. Old files can sneak into new packages, creating phantom validation errors that disappear when you start fresh.

We fixed each issue. We validated successfully. We uploaded to Teams.

And then came the clarifying question.

## Act 2: The Question That Changes Everything

"How is this different from a standalone app in Teams?"

It's the kind of question that makes you pause. The declarative agent approach gives you an extension *within* Microsoft 365 Copilot. Users invoke Amplifier through Copilot's interface. It's powerful—but it's not a dedicated Amplifier chat experience.

The realization hit: **We'd been building what was technically impressive, not what was actually wanted.**

The user wanted a standalone Amplifier interface in Teams. A bot you could chat with directly. A dedicated experience that felt like Amplifier, not like a Copilot plugin.

Time to pivot.

## The Pivot: Why a Teams Bot?

We could have stuck with the declarative agent. We'd already solved the validation puzzles. But architecture should follow intent, not sunk cost.

Here's why the Teams Bot architecture was the right choice:

**Native conversational UX**: People understand bots. You open a chat, you type, you get responses. No explaining "invoke Amplifier through Copilot."

**Direct integration**: The bot talks directly to `amplifier-app-api`. No intermediary layers. Clean, straightforward communication.

**Context flexibility**: Works in personal chats, group conversations, and channels. The same interface adapts to different collaboration contexts.

**Full experience control**: We own the interaction model. Formatting, response timing, error handling—all tuned for Amplifier's needs.

**No license barriers**: Users don't need Copilot licenses. If they have Teams, they can use Amplifier.

## Implementation: How It Actually Works

The architecture is surprisingly elegant:

```
User types in Teams
  ↓
Azure Bot Service validates and forwards
  ↓
Container App receives webhook
  ↓
Session Manager maps Teams conversation → Amplifier session
  ↓
API client calls amplifier-app-api
  ↓
Response formatted and sent back
```

The components:

- **FastAPI webhook service**: Receives messages from Azure Bot Service
- **Session Manager**: Maps Teams conversations to Amplifier sessions (so your chat history makes sense)
- **Amplifier API client**: Handles all backend communication
- **Bot Framework adapter**: Formats messages for Teams's rich formatting
- **Azure Container Apps**: Provides scalable hosting

No machine learning models to train. No complex NLP pipelines. Just a well-designed webhook service that bridges two APIs.

## What We Learned

**1. Clarify intent before choosing architecture**

"Teams integration" could mean five different things. The declarative agent was technically valid—just not what was needed. Ask clarifying questions early.

**2. Declarative agents ≠ Bots**

They're different patterns for different use cases. Declarative agents extend Copilot. Bots create standalone experiences. Neither is universally better.

**3. Validation errors teach platform semantics**

Every schema error forced us to understand *why* Teams needed things structured that way. The errors weren't obstacles—they were education.

**4. Fast iteration enables pivots**

Because we built quickly, we could test the declarative agent approach, get feedback, and pivot without losing weeks of work. Speed created flexibility.

## The Impact

Today, there's a working Teams Bot for Amplifier running in Azure Container Apps. It provides exactly what was requested: a dedicated Amplifier chat experience inside Teams.

But the bigger impact is the pattern. The integration approach we built—FastAPI webhook + session management + API client—is reusable. Want a Slack integration? Discord? The same architecture applies.

## Try It Yourself

The Teams integration demonstrates how Amplifier's architecture enables ecosystem extensions. The same patterns we used—session management, API integration, webhook handling—are available to anyone building on Amplifier.

Want to build your own integration? Start by asking: What do users actually want to do? Then choose the architecture that serves that intent.

The code and deployment configurations for the Teams bot are part of the Amplifier ecosystem. Whether you're building integrations, extending functionality, or solving novel problems with Amplifier, remember: architecture should follow intent.

**What integration would you build?** Share your ideas in the [Amplifier community discussions](https://github.com/amplifier/discussions).

---

*The Amplifier Teams integration is deployed and available. For more on building with Amplifier's API, see the [integration guide](https://amplifier.dev/docs/integrations).*
