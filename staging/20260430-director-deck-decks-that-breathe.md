---
title: "director-deck: Decks That Breathe"
date: 2026-04-30
author: kchau
tags: [amplifier, multi-agent, veo, pptx, recipe, video]
---

# director-deck: Decks That Breathe — A Multi-Agent Recipe for Cinematic PowerPoint

## One Prompt, One Polished Deck

You type a prompt. Twenty minutes later, you open `final_deck.pptx` — and it doesn't feel like a PowerPoint. The slides hold their beats. A contemplative title card lingers for five and a half seconds before dissolving into the next; a stat-heavy slide gets a quarter-second of extra breath so the number actually lands. Cuts ride the eye, not the clock.

These are decks that breathe.

`director-deck` is an Amplifier bundle that turns a single prompt into a finished, video-laden `.pptx` through a directed multi-agent pipeline. No drag-and-drop. No timing tweaks. The pacing is part of the content.

## Why AI-Generated Decks Still Feel Generated

We've all seen them. The auto-generated deck with the right words, the right charts, the right brand colors — and a uniformly hollow rhythm. Every transition the same. Every slide the same length. Cinematic intent flattened into a metronome.

The problem isn't the words. It's the time between them.

Slide pacing is content. A pitch needs urgency; a memorial needs stillness; a stat needs a beat to breathe. Most AI deck builders treat transitions as decoration. We treated them as direction.

## Five Agents, Three Gates, One Recipe

`director-deck` is a four-stage Amplifier recipe with five specialized agents and three human approval gates:

```
prompt
  → ghost-deck-writer       (draft the narrative)
  → slide-architect         (lay out wireframes)
  → [Gate 1: structure review]
  → visual-director         (specify imagery and motion)
  → slide-architect         (enriched layout pass)
  → [Gate 2: visual review]
  → transition-director     (score the pacing)
  → [Gate 3: pacing review]
  → deck-stitcher           (assemble final_deck.pptx)
```

Each agent does one job and hands off. The gates are where humans steer — confirm the voice, approve the visual direction, sign off on the pacing — before any expensive video generation runs. By the time Veo 3.1 starts rendering keyframes and transitions, every creative decision has been ratified.

Each run lives in its own isolated directory under `./runs/<date>-<slug>/` with a `DESIGN.md`, `slide_deck.json`, wireframe and enriched HTML+PPTX previews, an `assets/` folder, `keyframes/`, `transitions/`, and the final `final_deck.pptx`. You can replay, fork, or audit any run end to end.

## Content-Aware Pacing — The Philosophical Core

The breakthrough isn't the multi-agent topology. It's the `transition-director`.

Most pipelines pick a global transition speed: "fast" or "slow." `director-deck` reads each slide's emotional register and picks pacing per beat:

- **Contemplative or cultural decks** default to **4.5–6.0 seconds** with `ease_in_out` — long enough for the audience to settle into a feeling.
- **Business and pitch decks** default to **2.0–3.5 seconds** with sharper `ease_in` — fast enough to maintain forward pressure.
- **Heavy stat slides** get a **+1.5–2.0 second bonus** regardless of deck type — because a number you can't read is a number that didn't land.

The implementation lives in `video_processor.py`: four easing modes (`ease_in_out`, `ease_in`, `ease_out`, `linear`), content-aware duration rules, and **63 unit tests** covering every combination. ffmpeg does the actual frame interpolation; the director decides what to ask for.

The result is a deck where rhythm is intentional. You feel the difference before you can name it.

## Seamless PPTX Video — The Engineering Core

Here's the credibility-builder: getting video to actually play *correctly* inside a `.pptx` file required fixing four bugs in `python-pptx` itself.

PowerPoint's video XML is a minefield. Along the way we patched:

1. **`hlinkClick r:id` for click-to-play** — without this relationship, embedded videos were silent thumbnails.
2. **`delay=0` for autoplay** — the default omitted the timing node entirely; videos would load and just sit there.
3. **Unique per-slide poster frames** — `python-pptx` was reusing a single 1px placeholder across every slide, so every video shared the same thumbnail. Each slide now gets a real, unique poster frame.
4. **Auto-advance timing** — the transition node has to come *before* the timing node, and `fill="hold"` has to be set, or PowerPoint silently ignores auto-advance.

Each was a small XML fix. Together they're the difference between "video sort of works" and "open the file in Keynote, PowerPoint, or LibreOffice and the deck just plays."

If you've ever fought `python-pptx` to make a video deck behave, you know the value of this.

## Under the Hood — The Tooling Layer

`director-deck` runs on a thin stack:

- **Python** for orchestration and the `video_processor.py` module
- **Veo 3.1 (Google)** for keyframe and transition video generation
- **ffmpeg** for easing curves, duration trims, and concatenation
- **python-pptx** (with the four fixes above) for assembly
- **Playwright** to render HTML wireframes into preview PPTX before video runs
- **Amplifier** as the recipe runtime, agent dispatcher, and approval-gate engine

The interesting design choice: HTML wireframes and enriched previews are generated *before* Veo is called, so each gate is reviewing real layouts — not vibes. Generation cost stays bounded.

## What This Unlocks

The narrow win is gorgeous decks from a prompt. The broader pattern is the lesson:

**Directed multi-agent pipelines beat monolithic prompts when the work has multiple distinct creative phases.** Writing isn't layout. Layout isn't visual direction. Visual direction isn't pacing. Each phase deserves its own specialist, its own context window, and — crucially — its own human review gate before the next phase commits expensive resources downstream.

`ghost-deck-writer → slide-architect → visual-director → transition-director → deck-stitcher` is just one instance. The shape generalizes: **director agents** that make creative decisions, **specialist agents** that execute them, **gates** that humans use to steer, and **a stitcher** that assembles the final artifact.

Once you see the pattern, you start seeing it everywhere it should exist and doesn't.

## Try It

```bash
git clone <director-deck repo>
cd director-deck
amplifier run recipes/director-deck.yaml --prompt "Your deck idea"
```

Walk through the three gates. Approve, revise, or reroll. Watch your `runs/<date>-<slug>/` directory fill up with each stage's artifact. Open `final_deck.pptx`.

Notice how it breathes.

---

*director-deck v0.1.0 — built on Amplifier, Veo 3.1, ffmpeg, and python-pptx (four bug fixes included). PRs and pacing critiques welcome.*
