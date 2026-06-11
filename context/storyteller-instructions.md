# Storyteller Instructions

Detailed guidance for creating presentation decks.

## Research Phase

Before creating a deck, gather:

### ⚠️ CRITICAL: Source Verification (Avoid Anthropic Repos)

**The risk**: GitHub may surface `anthropics/amplifier*` repos when searching for Amplifier features. These are NOT the repos you're looking for.

**Default to the Microsoft Amplifier ecosystem** unless explicitly told otherwise:

- ✅ **Core Amplifier**: `microsoft/amplifier*` (e.g., `microsoft/amplifier-core`, `microsoft/amplifier-foundation`)
- ✅ **Team members**: `ramparte/*`, `momuno/*`, `payneio/*`, etc. (when researching team projects)
- ✅ **Personal forks**: When user specifies their own work
- ❌ **AVOID**: `anthropics/amplifier*` - different project, causes hallucinations

**Verification steps BEFORE researching:**
1. **Be explicit about org** in `gh` commands: `gh repo view microsoft/amplifier-core` (not just `amplifier-core`)
2. **Cross-reference core features** against `microsoft/amplifier` MODULES.md
3. **When in doubt**, ask the user which org/repo they mean

**Red flags that you grabbed the wrong repo:**
- References to Anthropic-internal tools or systems
- Features that conflict with what's in Microsoft Amplifier docs
- Repository URLs containing `/anthropics/` when user asked about "Amplifier"

**When user says "Amplifier feature"** → Default to `microsoft/amplifier*`  
**When user says "my project"** → Look at their repos (`ramparte/*` for this user)  
**When user names an org** → Use that org explicitly

### 1. **GitHub activity** - Use `gh` CLI to find:
   - Recent commits and PRs related to the feature
   - Timeline (when did development start/end?)
   - Number of repos touched
   - Key contributors
   
   **Example (note the explicit org scope):**
   ```bash
   gh repo view microsoft/amplifier-core
   gh pr list --repo microsoft/amplifier-core --search "feature-name"
   ```

### 2. **Feature details** - Understand:
   - What problem does it solve?
   - How does it work?
   - What's the user-facing impact?
   - Any metrics or numbers?

### 3. **Narrative angle** - Decide the story:
   - "Built with Amplifier" (showcase projects like Cortex)
   - "Amplifier Feature" (platform capabilities)
   - "Developer Experience" (tooling improvements)
   - "Enterprise Value" (compliance, cost, scale)

## Creating the Deck

### HTML Template

**IMPORTANT**: All presentations must be responsive and work across devices. See `context/responsive-design.md` for complete guidelines.

**CRITICAL - Slide Overflow Pattern**: Do NOT use `justify-content: center` on all slides. This causes content clipping on mobile. Instead:
- Slides flow from top by default (with generous top padding)
- Use `.center` class only for title slides that need vertical centering
- Always include `overflow-y: auto` on slides

Start with this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
    <title>Deck Title</title>
    <script>document.documentElement.classList.add('js')</script>
    <style>
        /* Core slide CSS - CRITICAL for preventing content clipping */
        .slide {
            display: flex;         /* Default: visible (no-JS scrollable fallback) */
            width: 100vw;
            min-height: 100vh;
            min-height: 100dvh;
            padding: clamp(60px, 10vw, 120px) clamp(20px, 5vw, 80px) clamp(80px, 12vw, 100px);
            flex-direction: column;
            overflow-y: auto;      /* Enable scrolling for tall content */
            overflow-x: hidden;    /* Prevent horizontal scroll */
            /* NO justify-content: center here! */
        }

        .slide.active {
            display: flex;
        }

        /* Progressive enhancement: no-JS fallback — all slides visible, scrollable */
        html:not(.js) .slide {
            display: flex !important;
            position: relative !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            visibility: visible !important;
            transform: none !important;
            width: 100%;
            min-height: 100vh;
            min-height: 100dvh;
        }

        /* Progressive enhancement: JS-only slide mode */
        html.js { overflow: hidden; }
        html.js body { overflow: hidden; overscroll-behavior: none; }
        html.js .slide { display: none; }
        html.js .slide.active { display: flex; }

        /* Centering is OPT-IN for title/short slides only */
        .center {
            text-align: center;
            align-items: center;
            justify-content: center;
        }

        /* Landscape mobile: reduce vertical padding */
        @media (max-height: 500px) and (orientation: landscape) {
            .slide {
                padding: 16px clamp(20px, 5vw, 80px) 60px;
            }
            .slide.center {
                justify-content: flex-start;
            }
        }

        /* Accessibility: respect reduced motion preference */
        @media (prefers-reduced-motion: reduce) {
            .slide, .slide * {
                animation: none !important;
                transition: none !important;
            }
        }

        /* More stories link - REQUIRED on all decks */
        .more-stories {
            position: fixed;
            bottom: 10px;
            left: 50%;
            transform: translateX(-50%);
            font-size: clamp(11px, 1.5vw, 12px);
            color: rgba(255,255,255,0.3);
            text-decoration: none;
            z-index: 100;
        }
        .more-stories:hover {
            color: rgba(255,255,255,0.5);
        }
    </style>
</head>
<body>
    <!-- Slides -->
    <div class="slide active">...</div>
    <div class="slide">...</div>
    
    <!-- Navigation -->
    <div class="nav" id="nav"></div>
    <div class="slide-counter" id="counter"></div>
    
    <!-- More stories link - REQUIRED -->
    <a href="index.html" class="more-stories">More Amplifier Stories</a>
    
    <script>
        /* Navigation JS - arrow keys, click, dots */
    </script>
</body>
</html>
```

**Progressive Enhancement (REQUIRED):** All decks must include:
1. `<script>document.documentElement.classList.add('js')</script>` in `<head>` before `<style>`
2. `.slide { display: flex; }` as default (NOT `display: none`)
3. `html:not(.js) .slide` block forcing all slides visible for no-JS fallback
4. `html.js .slide { display: none; }` and `html.js .slide.active { display: flex; }` for JS mode
5. `html.js body { overflow: hidden; }` (NOT on body directly)

**Why:** Teams/SharePoint may block or strip JavaScript (SafeLinks, CSP, iframe sandbox).
Without progressive enhancement, users see only the first slide and cannot navigate.
With it, no-JS users get a scrollable single-page document; JS users get normal slides.

### Navigation JavaScript

Always include this exact pattern for animated slide transitions with keyboard/click/dot/**touch** navigation.

**CRITICAL — Do NOT improvise a different transition approach.** This pattern
handles the inline-style vs CSS-class specificity interaction correctly.
Variations (adding `.exiting`/`.prev` classes, skipping the reflow force,
or forgetting to clean up inline styles) cause broken back-and-forth
navigation.

```javascript
const slides = document.querySelectorAll('.slide');
const total = slides.length;
let current = 0;
let transitioning = false;

function goTo(n) {
    n = ((n % total) + total) % total;
    if (transitioning || n === current) return;
    transitioning = true;
    var direction = n > current ? 1 : -1;
    var prev = slides[current];
    var next = slides[n];

    // 1. Animate previous slide out
    prev.classList.remove('active');
    prev.style.transform = direction > 0 ? 'translateX(-40px)' : 'translateX(40px)';
    prev.style.opacity = '0';

    // 2. Position next slide at entry point (disable transition first)
    next.style.transition = 'none';
    next.style.transform = direction > 0 ? 'translateX(40px)' : 'translateX(-40px)';
    next.style.opacity = '0';

    // 3. Force reflow so browser registers the starting position
    void next.offsetWidth;

    // 4. Re-enable transitions and animate to final position
    next.style.transition = '';
    next.style.transform = 'translateX(0)';
    next.style.opacity = '1';
    next.classList.add('active');

    current = n;
    updateNav();

    // 5. Clean up ALL inline styles from BOTH slides after animation
    setTimeout(function() {
        prev.style.transform = '';
        prev.style.opacity = '';
        next.style.transform = '';
        next.style.opacity = '';
        transitioning = false;
    }, 500);
}

function updateNav() {
    const nav = document.getElementById('nav');
    const counter = document.getElementById('counter');
    nav.innerHTML = '';
    slides.forEach((_, i) => {
        const dot = document.createElement('div');
        dot.className = 'nav-dot' + (i === current ? ' active' : '');
        dot.onclick = () => goTo(i);
        nav.appendChild(dot);
    });
    counter.textContent = `${current + 1} / ${total}`;
}

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ') goTo(current + 1);
    if (e.key === 'ArrowLeft') goTo(current - 1);
});

// Click navigation (left half = back, right half = forward)
document.addEventListener('click', (e) => {
    if (e.target.closest('.nav')) return;
    if (e.clientX > window.innerWidth / 2) goTo(current + 1);
    else goTo(current - 1);
});

// Touch/swipe navigation (REQUIRED for mobile)
let touchStartX = 0;

const SWIPE_THRESHOLD = 50;

document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
}, { passive: true });

document.addEventListener('touchend', (e) => {
    const diff = touchStartX - e.changedTouches[0].screenX;
    if (Math.abs(diff) > SWIPE_THRESHOLD) {
        if (diff > 0) goTo(current + 1);
        else goTo(current - 1);
    }
}, { passive: true });

updateNav();
```

### Slide Types

**Title Slide:**
```html
<div class="slide active center">
    <div class="section-label">Category</div>
    <h1 class="headline">Feature Name</h1>
    <p class="subhead">One-line description</p>
    <div class="small-text">January 2026</div>
</div>
```

**Problem Slide:**
```html
<div class="slide">
    <div class="section-label">The Problem</div>
    <h2 class="headline">Pain point headline</h2>
    <div class="thirds">
        <div class="card">...</div>
        <div class="card">...</div>
        <div class="card">...</div>
    </div>
</div>
```

**Code Example Slide:**
```html
<div class="slide">
    <div class="section-label">Usage</div>
    <h2 class="medium-headline">How to use it</h2>
    <div class="code-block">
<span class="code-comment"># Comment</span>
command --flag value
    </div>
</div>
```

**Velocity Slide:**
```html
<div class="slide center">
    <h2 class="medium-headline">Development velocity</h2>
    <div class="velocity-grid">
        <div class="velocity-stat">
            <div class="velocity-number">3</div>
            <div class="velocity-label">Repositories</div>
        </div>
        <!-- More stats -->
    </div>
</div>
```

**Sources & Methodology Slide (REQUIRED):**
```html
<div class="slide">
    <div class="section-label">Sources</div>
    <h2 class="medium-headline">Research Methodology</h2>
    <div class="small-text" style="opacity: 0.7; line-height: 1.6;">
        <p><strong>Data as of:</strong> February 20, 2026</p>
        <p><strong>Feature status:</strong> Active</p>
        <p><strong>Research performed:</strong></p>
        <ul>
            <li>Git log analysis: <code>git log --oneline repo-name</code> (N commits found)</li>
            <li>PR history: <code>gh pr list --repo org/repo</code> (N PRs found)</li>
            <li>Line counts: <code>find . -name "*.py" | xargs wc -l</code></li>
            <li>Contributors: extracted from git log --format="%an"</li>
        </ul>
        <p><strong>Gaps:</strong> [List any data that was unavailable or estimated]</p>
        <p><strong>Primary contributors:</strong> [Name(s) with commit %]</p>
    </div>
</div>
```

This slide is mandatory on every deck. It serves as the audit trail. If a reader
questions any metric in the deck, this slide tells them how it was derived.

## Quality Checklist

Before presenting to user, verify ALL items in both sections:

### Accuracy (verify FIRST — a beautiful deck with wrong numbers is worse than ugly truth)

- [ ] **Research was performed** — story-researcher agent was invoked and returned structured data
- [ ] **Every metric traces to research output** — no number appears without evidence
- [ ] **No round-number inflation** — real numbers used, qualifiers preserved (~, approximately)
- [ ] **Timeline dates verified against git commits** — not narrative estimates
- [ ] **Impact claims have baselines** — "X% faster than Y, measured by Z"
- [ ] **Feature status badge present** — Active / Experimental / Archived / Disabled
- [ ] **Repository org is correct** — microsoft/ vs ramparte/ vs personal repos stated accurately
- [ ] **Contributors attributed** — primary author(s) named with approximate commit share
- [ ] **No self-validating claims** — removed "our tool says we're excellent" type statements
- [ ] **Sources & Methodology slide present** — with data-as-of date, commands run, gaps noted
- [ ] **Velocity slide numbers match research output** — cross-checked, not approximated

### Visual & Technical

- [ ] **Progressive enhancement present** — `<script>...classList.add('js')</script>` before `<style>`, `html.js`/`html:not(.js)` scoped rules, `.slide { display: flex }` default
- [ ] **No-JS fallback works** — without JS, all slides visible and scrollable as a single page
- [ ] Navigation works (arrows, click, dots, **swipe on mobile**)
- [ ] Slide counter updates correctly
- [ ] No horizontal scrolling on any slide
- [ ] **No content clipping on mobile (test at 320px viewport)**
- [ ] **Slides use `overflow-y: auto` (not clipping tall content)**
- [ ] **`justify-content: center` only on `.slide.center` classes**
- [ ] Code blocks don't overflow (use `pre-wrap`)
- [ ] Consistent color scheme throughout
- [ ] All links are correct
- [ ] "More Amplifier Stories" link present (links to index.html)
- [ ] **Responsive: Text readable on mobile without zooming**
- [ ] **Responsive: Grids collapse to single column on narrow screens**
- [ ] **Responsive: Touch targets ≥44px for tappable elements**
- [ ] **Maximum 20 inline style attributes in the entire deck** (use CSS classes with clamp values)
- [ ] **No inline font-size values** — all sizing must use clamp() via CSS classes
- [ ] **All text meets WCAG AA contrast** (4.5:1 for normal text, 3:1 for large text on its background)
- [ ] **Card backgrounds visually distinct from body** (cards must be visible, not invisible-on-black)
- [ ] **Icons >= 28px minimum** in card layouts (use .icon-card or .icon-feature classes)
- [ ] **No text opacity below 0.5** for any content that must be read

## Deployment Workflow

1. Create deck, save to `docs/`
2. Present to user for review
3. Iterate based on feedback
4. When approved: `./deploy.sh filename.html`
5. Commit changes to git
