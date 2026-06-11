# Responsive Design System for Amplifier Stories

## Philosophy

Every presentation must work seamlessly across:
- **Devices**: Phone (320px) → Tablet (768px) → Desktop (1440px+)
- **Browsers**: Chrome, Safari, Firefox, Edge (including mobile variants)
- **OS**: iOS, Android, macOS, Windows, Linux
- **Contexts**: Standalone viewing, embedded iframes, PWA

## Core Techniques

### 1. Fluid Typography with `clamp()`

Never use fixed `font-size` values. Always use `clamp()`:

```css
/* Pattern: clamp(mobile-min, fluid-scale, desktop-max) */
font-size: clamp(16px, 2.5vw, 24px);
```

| Element Type | Recommended Clamp |
|--------------|-------------------|
| Headlines (hero) | `clamp(36px, 10vw, 72px)` |
| Headlines (section) | `clamp(28px, 6vw, 48px)` |
| Subheads | `clamp(18px, 3vw, 28px)` |
| Body text | `clamp(14px, 2vw, 16px)` |
| Captions/labels | `clamp(12px, 1.8vw, 14px)` |
| Code blocks | `clamp(12px, 2vw, 16px)` |

### 2. Fluid Spacing with `clamp()`

```css
/* Padding */
padding: clamp(16px, 4vw, 40px);

/* Gaps */
gap: clamp(16px, 3vw, 32px);

/* Margins */
margin-bottom: clamp(16px, 3vw, 24px);
```

### 3. Responsive Grids with `auto-fit`

Never use fixed column counts:

```css
/* ❌ Bad - breaks on mobile */
grid-template-columns: repeat(3, 1fr);

/* ✅ Good - auto-stacks */
grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr));
```

### 4. Max-Width Constraints with `min()`

```css
/* Prevents overflow while allowing flexibility */
max-width: min(600px, 90vw);
width: min(200px, 80vw);
```

### 5. Dynamic Viewport Height

```css
/* Accounts for mobile browser chrome (URL bar) */
min-height: 100vh;
min-height: 100dvh;  /* Dynamic viewport - preferred */
```

### 6. Slide Overflow Pattern (IMPORTANT)

Slides should **NOT** use `justify-content: center` by default, as this causes content clipping when content exceeds viewport height. Instead:

```css
/* ❌ Bad - clips content at top AND bottom when overflow */
.slide {
    min-height: 100dvh;
    display: flex;
    flex-direction: column;
    justify-content: center;  /* Causes clipping! */
}

/* ✅ Good - content flows from top, scrolls when needed */
.slide {
    display: none;
    min-height: 100vh;
    min-height: 100dvh;
    padding: clamp(60px, 10vw, 120px) clamp(20px, 5vw, 80px) clamp(80px, 12vw, 100px);
    flex-direction: column;
    overflow-y: auto;    /* Enable scrolling for tall content */
    overflow-x: hidden;  /* Prevent horizontal scroll */
}

.slide.active {
    display: flex;
}

/* Centering is OPT-IN for title/short slides only */
.slide.center {
    text-align: center;
    align-items: center;
    justify-content: center;  /* Only when .center is applied */
}
```

**Key Design Decisions:**
1. **Top-aligned by default**: Content-heavy slides flow naturally from top
2. **Centering is opt-in**: Only `.slide.center` gets vertical centering (for title slides)
3. **Scroll when needed**: `overflow-y: auto` enables scrolling only when content exceeds viewport
4. **Generous top padding**: Replaces centering effect for visual balance
5. **Extra bottom padding**: Accounts for nav dots + "More Stories" link (~80-100px)

### 7. Touch-Friendly Targets

```css
/* Minimum 44px touch targets on touch devices */
@media (hover: none) {
    .nav-dot { 
        min-width: 16px; 
        min-height: 16px; 
    }
    
    button, a {
        min-height: 44px;
        min-width: 44px;
    }
}
```

### 8. Safe Area Insets (for notched devices)

```css
/* Viewport meta tag */
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">

/* CSS padding for notched devices */
padding-left: env(safe-area-inset-left);
padding-right: env(safe-area-inset-right);
padding-bottom: env(safe-area-inset-bottom);
```

### 9. Landscape Mobile Optimization (CRITICAL)

When users rotate phones to landscape, vertical space is severely limited (~320px height). Generous top padding can consume 50%+ of the screen. Add this media query:

```css
/* Landscape mobile: reduce vertical padding drastically */
@media (max-height: 500px) and (orientation: landscape) {
    .slide {
        padding: 16px clamp(20px, 5vw, 80px) 60px; /* Tight top, keep bottom for nav */
    }
    .slide.center {
        justify-content: flex-start; /* Don't center in cramped landscape */
    }
}
```

**Why this matters:** On an iPhone rotated sideways, 60px top padding + 80px bottom padding leaves only ~180px for content. This fix reclaims that space.

### 10. Reduced Motion (Accessibility)

Respect users who have enabled "Reduce Motion" in their OS settings (for vestibular disorders, motion sensitivity, etc.):

```css
/* Disable animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
    .slide,
    .slide * {
        animation: none !important;
        transition: none !important;
    }
    .slide.active {
        opacity: 1;
    }
}
```

**Why this matters:** ~10-30% of users experience motion sensitivity. This is a simple accessibility win with no downside.

## CSS Custom Properties for Consistency

Define a design system at the root:

```css
:root {
    /* Typography scale */
    --fs-hero: clamp(36px, 10vw, 72px);
    --fs-h1: clamp(28px, 6vw, 48px);
    --fs-h2: clamp(22px, 4vw, 32px);
    --fs-body: clamp(14px, 2vw, 16px);
    --fs-small: clamp(12px, 1.8vw, 14px);
    --fs-code: clamp(12px, 2vw, 16px);
    
    /* Spacing scale */
    --space-xs: clamp(8px, 1.5vw, 12px);
    --space-sm: clamp(12px, 2vw, 16px);
    --space-md: clamp(16px, 3vw, 24px);
    --space-lg: clamp(24px, 4vw, 40px);
    --space-xl: clamp(32px, 6vw, 60px);
    
    /* Border radius */
    --radius-sm: clamp(8px, 1vw, 12px);
    --radius-md: clamp(12px, 1.5vw, 16px);
    --radius-lg: clamp(16px, 2vw, 24px);
}
```

Usage:
```css
.headline { font-size: var(--fs-hero); }
.card { 
    padding: var(--space-md);
    border-radius: var(--radius-md);
}
```

## Checklist for New Presentations

- [ ] No fixed `font-size` values (use `clamp()`)
- [ ] No fixed grid columns (use `auto-fit`)
- [ ] No fixed widths without `min()` fallback
- [ ] `100dvh` used alongside `100vh`
- [ ] Touch targets ≥44px on touch devices
- [ ] `viewport-fit=cover` in meta tag
- [ ] **Slides use `overflow-y: auto` (no content clipping)**
- [ ] **`justify-content: center` only on `.slide.center` (opt-in)**
- [ ] **Landscape mobile media query included (`max-height: 500px`)**
- [ ] **`prefers-reduced-motion` media query included**
- [ ] Tested at 320px, 768px, 1440px viewports
- [ ] Tested with iOS Safari, Chrome, Firefox
- [ ] **Tested in landscape orientation on mobile**

## Testing Commands

```bash
# Open in browser with device emulation
open -a "Google Chrome" --args --auto-open-devtools-for-tabs

# Quick mobile viewport test (requires Chrome)
# DevTools → Toggle Device Toolbar (Cmd+Shift+M)
# Test at: iPhone SE (375px), iPad (768px), Desktop (1440px)
```

## Anti-Patterns to Avoid

| ❌ Don't | ✅ Do Instead |
|----------|---------------|
| `font-size: 24px` | `font-size: clamp(18px, 3vw, 24px)` |
| `width: 400px` | `width: min(400px, 90vw)` |
| `grid-template-columns: 1fr 1fr 1fr` | `grid-template-columns: repeat(auto-fit, minmax(min(280px, 100%), 1fr))` |
| `height: 100vh` alone | `min-height: 100vh; min-height: 100dvh;` |
| Inline `style="font-size: Npx"` | Use CSS classes with clamp values |
| `@media (max-width: 600px)` for everything | Use intrinsic sizing where possible |
| `.slide { justify-content: center }` on all slides | Only use `.slide.center` for title slides |
| `color: rgba(255,255,255,0.3)` for readable text | `color: var(--text-tertiary)` (0.5 minimum) |
| `opacity: 0.35` on content elements | Minimum `opacity: 0.5`, prefer full opacity with dim colors |
| Emoji at `font-size: 20px` or `24px` | `font-size: clamp(28px, 5vw, 48px)` for card icons |
| `background: rgba(255,255,255,0.04)` for cards | `background: var(--surface-1)` (0.06 minimum) |
