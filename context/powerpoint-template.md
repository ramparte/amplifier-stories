# Professional PowerPoint Template Specification

This template defines the visual style for all PowerPoint presentations created by the storyteller agent.

**Reference:** Based on Surface-Presentation.pptx professional corporate style.

---

## Color Palette

### Primary Colors
```
Background:     #FFFFFF (White)
Text Primary:   #1F1F1F (Near Black)
Text Secondary: #595959 (Medium Gray)
Accent Blue:    #0078D4 (Microsoft Blue)
Accent Orange:  #D83B01 (Microsoft Orange)
```

### Supporting Colors
```
Light Gray:     #F3F2F1 (Backgrounds, dividers)
Medium Gray:    #EDEBE9 (Subtle backgrounds)
Dark Gray:      #323130 (Headings)
Success Green:  #107C10
Warning Red:    #D13438
```

### Usage Guidelines
- **Backgrounds:** White (#FFFFFF) for main slides, Light Gray (#F3F2F1) for alternating sections
- **Headings:** Dark Gray (#323130), bold
- **Body text:** Text Primary (#1F1F1F), regular weight
- **Accents:** Blue for interactive elements, Orange for highlights/emphasis
- **Code blocks:** Light Gray background (#F3F2F1), Dark Gray text

---

## Typography

### Font Families
```css
Primary:   'Segoe UI', Arial, sans-serif
Secondary: 'Calibri', Arial, sans-serif
Code:      'Consolas', 'Courier New', monospace
```

**Note:** Use web-safe fonts for html2pptx compatibility:
- Primary: Arial (as Segoe UI fallback)
- Secondary: Arial
- Code: Courier New (as Consolas fallback)

### Type Scale

**Title Slides:**
```
Slide Title:     44pt, Bold, Dark Gray (#323130)
Subtitle:        24pt, Regular, Text Secondary (#595959)
Meta info:       18pt, Regular, Medium Gray
```

**Content Slides:**
```
Slide Heading:   32pt, Bold, Dark Gray (#323130)
Section Label:   14pt, Bold, ALL CAPS, Accent Blue (#0078D4)
Body Text:       18pt, Regular, Text Primary (#1F1F1F)
Bullets Level 1: 18pt, Regular, Text Primary
Bullets Level 2: 16pt, Regular, Text Secondary (#595959)
Code Text:       16pt, Regular, Consolas/Courier New
Captions:        14pt, Regular, Text Secondary
```

### Line Heights
```
Headings:    1.2 (tight)
Body text:   1.5 (comfortable)
Bullets:     1.6 (generous)
Code blocks: 1.4 (readable)
```

---

## Layout Patterns

### Dimensions
```
Aspect Ratio: 16:9
Width:        720pt (10 inches)
Height:       405pt (5.625 inches)
```

### Margins & Spacing
```
Top margin:        60pt
Bottom margin:     60pt
Left margin:       80pt
Right margin:      80pt

Section spacing:   40pt (between major sections)
Paragraph spacing: 20pt (between paragraphs)
Bullet spacing:    12pt (between bullet items)
```

### Grid System
```
Use 12-column grid for layout alignment
Column width: ~50pt
Gutter: ~10pt
```

---

## Slide Templates

### 1. Title Slide
```
Layout:
┌─────────────────────────────────────────────────┐
│                                                 │
│          [SECTION LABEL - 14pt, ALL CAPS]      │
│                                                 │
│        [MAIN TITLE - 44pt, Bold, Center]       │
│                                                 │
│      [Subtitle - 24pt, Regular, Center]        │
│                                                 │
│        [Date/Meta - 18pt, Bottom Right]        │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Style:**
- Centered alignment
- Large title (44pt)
- Generous whitespace
- Optional accent color underline for title

### 2. Section Divider
```
Layout:
┌─────────────────────────────────────────────────┐
│                                                 │
│                                                 │
│      [SECTION TITLE - 44pt, Bold, Center]      │
│                                                 │
│    [Section Number/Icon - Accent Color]        │
│                                                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Style:**
- Centered alignment
- Bold section title
- Large section number or icon in accent color
- Minimal text

### 3. Content Slide (Standard)
```
Layout:
┌─────────────────────────────────────────────────┐
│ [Section Label - 14pt, ALL CAPS, Top Left]     │
│                                                 │
│ [Slide Heading - 32pt, Bold]                   │
│                                                 │
│ • [Bullet point - 18pt]                        │
│ • [Bullet point - 18pt]                        │
│ • [Bullet point - 18pt]                        │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Style:**
- Left-aligned heading
- Section label above heading (optional)
- Generous bullet spacing
- Maximum 5-6 bullets per slide

### 4. Two-Column Comparison
```
Layout:
┌─────────────────────────────────────────────────┐
│ [Heading - 32pt, Bold]                         │
│                                                 │
│ ┌──────────────┐  ┌──────────────┐            │
│ │   Before     │  │    After      │            │
│ │              │  │               │            │
│ │ • Point      │  │ • Point       │            │
│ │ • Point      │  │ • Point       │            │
│ │ • Point      │  │ • Point       │            │
│ └──────────────┘  └──────────────┘            │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Style:**
- Equal width columns (45% each, 10% gutter)
- Light gray background boxes for each column
- Column headers in accent color or bold
- Aligned content

### 5. Code Example Slide
```
Layout:
┌─────────────────────────────────────────────────┐
│ [Section Label - 14pt]                         │
│ [Heading - 32pt, Bold]                         │
│                                                 │
│ ┌─────────────────────────────────────────────┐│
│ │ # Code example - 16pt, Courier New         ││
│ │ def function():                             ││
│ │     return "example"                        ││
│ └─────────────────────────────────────────────┘│
│                                                 │
│ [Explanation text - 18pt]                      │
└─────────────────────────────────────────────────┘
```

**Style:**
- Light gray background (#F3F2F1) for code block
- Courier New font
- 16pt font size for readability
- 12pt padding inside code block
- Brief explanation below

### 6. Data/Metrics Slide
```
Layout:
┌─────────────────────────────────────────────────┐
│ [Heading - 32pt, Bold, Center]                 │
│                                                 │
│     ┌─────┐    ┌─────┐    ┌─────┐             │
│     │ 87% │    │ 45  │    │ 2.3x│             │
│     │     │    │     │    │     │             │
│     │Label│    │Label│    │Label│             │
│     └─────┘    └─────┘    └─────┘             │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Style:**
- Large numbers (72pt+), bold, accent color
- Small labels below (18pt)
- Equal spacing between metrics
- Centered alignment

---

## Visual Elements

### Shapes & Borders
```
Border radius:    4pt (subtle rounding)
Border width:     2pt (borders when used)
Border color:     #EDEBE9 (Medium Gray)
Shadow:           None or subtle (2pt blur, 10% opacity)
```

### Dividers
```
Horizontal line:  2pt height, #EDEBE9 color, 80% slide width
Vertical line:    2pt width, #EDEBE9 color, centered in gutter
```

### Icons & Bullets
```
Bullets:          Standard round bullets (•)
Custom bullets:   Simple geometric shapes (▪ ▸ →)
Icons:            Simple, flat, 2-color max (primary + accent)
Icon size:        24-48pt depending on context
```

### Boxes & Containers
```
Background:       #F3F2F1 (Light Gray)
Padding:          20pt all sides
Border:           Optional 2pt in #EDEBE9
Border radius:    4pt
```

---

## Content Guidelines

### Text Density
- **Maximum 6 bullets per slide**
- **Maximum 10-12 words per bullet**
- **Prefer 3-4 bullets** for better impact
- Use sub-bullets sparingly (max 2 levels)

### Visual Hierarchy
1. **Most important:** Large, bold, dark color
2. **Supporting:** Medium size, regular weight
3. **Details:** Smaller, lighter color

### Spacing Philosophy
- **Generous whitespace** - slides should breathe
- **Consistent rhythm** - equal spacing between elements
- **Visual balance** - distribute content evenly

### Slide Flow
1. Title slide
2. Problem/Context (1-2 slides)
3. Solution overview (1 slide)
4. Deep dive details (3-5 slides)
5. Impact/Results (1-2 slides)
6. Call to action (1 slide)

**Total:** Aim for 10-15 slides for a 10-minute presentation

---

## Common Patterns

### Before/After Comparison
```css
.before-after {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40pt;
}

.before { 
  background: #FFF4CE; /* Light yellow */
  border-left: 4pt solid #D83B01; /* Orange */
}

.after { 
  background: #DFF6DD; /* Light green */
  border-left: 4pt solid #107C10; /* Green */
}
```

### Feature Highlight
```css
.feature-highlight {
  background: #F3F2F1; /* Light gray */
  border-left: 4pt solid #0078D4; /* Blue accent */
  padding: 20pt;
}
```

### Code Block
```css
.code-block {
  background: #F3F2F1;
  font-family: 'Courier New', monospace;
  font-size: 16pt;
  line-height: 1.4;
  padding: 20pt;
  border-radius: 4pt;
}
```

### Metric Display
```css
.metric {
  text-align: center;
}

.metric-number {
  font-size: 72pt;
  font-weight: bold;
  color: #0078D4; /* Accent blue */
  line-height: 1;
}

.metric-label {
  font-size: 18pt;
  color: #595959; /* Text secondary */
  margin-top: 12pt;
}
```

---

## HTML Implementation Example

```html
<!DOCTYPE html>
<html>
<head>
<style>
body {
  width: 720pt;
  height: 405pt;
  margin: 0;
  padding: 60pt 80pt;
  font-family: Arial, sans-serif;
  background: #FFFFFF;
  color: #1F1F1F;
}

.section-label {
  font-size: 14pt;
  font-weight: bold;
  text-transform: uppercase;
  color: #0078D4;
  letter-spacing: 1pt;
  margin-bottom: 20pt;
}

h1 {
  font-size: 44pt;
  font-weight: bold;
  color: #323130;
  line-height: 1.2;
  margin: 0 0 20pt 0;
}

h2 {
  font-size: 32pt;
  font-weight: bold;
  color: #323130;
  line-height: 1.2;
  margin: 0 0 30pt 0;
}

p {
  font-size: 18pt;
  line-height: 1.5;
  margin: 0 0 20pt 0;
}

ul {
  font-size: 18pt;
  line-height: 1.6;
  margin: 0;
  padding-left: 30pt;
}

li {
  margin-bottom: 12pt;
}

.code-block {
  background: #F3F2F1;
  font-family: 'Courier New', monospace;
  font-size: 16pt;
  line-height: 1.4;
  padding: 20pt;
  border-radius: 4pt;
  white-space: pre;
}
</style>
</head>
<body>
  <!-- Slide content here -->
</body>
</html>
```

---

## Quality Checklist

Before finalizing any PowerPoint:

- [ ] Colors match the palette (no random colors)
- [ ] Fonts are consistent (Arial for body, Courier New for code)
- [ ] Margins are 60pt/80pt top-bottom/left-right
- [ ] Maximum 6 bullets per slide
- [ ] Generous whitespace on every slide
- [ ] Visual hierarchy is clear (size + weight + color)
- [ ] Code blocks have light gray background
- [ ] Text is left-aligned (except title slides)
- [ ] No text smaller than 14pt
- [ ] Consistent spacing between elements
