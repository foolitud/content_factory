---
name: designing-ui-ux-pro
description: Provides advanced UI/UX design intelligence. Includes industry-specific reasoning, 50+ styles (Glassmorphism, Minimalist, etc.), 160+ color palettes, and accessibility-first guidelines. Use it to plan, build, or review professional interfaces.
---

# Designing UI/UX Pro

## When to use this skill

- Designing new web or mobile pages (Landing, Dashboard, SaaS, etc.).
- Creating or refactoring UI components for better usability and aesthetics.
- Choosing color schemes, typography, and spacing systems based on product type.
- Conducting UX/UI audits for accessibility (WCAG), performance, and visual consistency.
- Implementing advanced UI styles like Glassmorphism, Brutalism, or Bento Grid.

## Workflow: Design Intelligence Search

### 1. Generate Design System
Always start by generating a complete design system recommendation for your project. This provides the "Source of Truth" for styles, colors, and layout.

```bash
python3 scripts/search.py "<product_type> <industry> <keywords>" --design-system -p "<Project Name>"
```

### 2. Deep-Dive Searches
Use domain-specific searches to get detailed specifications for individual elements.

- **Styles**: `python3 scripts/search.py "<style_name>" --domain style`
- **Colors**: `python3 scripts/search.py "<industry>" --domain color`
- **UX Guidelines**: `python3 scripts/search.py "<topic>" --domain ux`
- **Components**: `python3 scripts/search.py "<component>" --domain landing`

### 3. Verification & Guardrails
Before delivery, run a validation pass using the internal checklists.

- [ ] Check contrast ratios (AA 4.5:1).
- [ ] Ensure touch targets are ≥44px.
- [ ] Verify responsive behavior and safe areas.
- [ ] No emojis as structural icons (use SVG).

## Core Guidelines

- **Accessibility First**: Contrast, keyboard navigation, and aria-labels are non-negotiable.
- **Micro-interactions**: Use 150-300ms transitions for all state changes.
- **Consistency**: Stick to the generated Design System across all views.
- **Performance**: Optimize images (WebP/AVIF) and reserve space for async content to prevent layout shifts.

## Output Directory

All websites, landing pages, and HTML files produced using this skill **must** be saved to:

```
websites/
```

This folder lives at the root of the project. Create subfolders inside `websites/` if needed (e.g., `websites/micro-aventures/`), but never place output files elsewhere.

## Resources

- [Scripts](scripts/)
- [Knowledge Base](resources/data/)

