---
name: frontend-patterns
description: "Use when working on the landing page UI, theme switching, reveal effects, section nav, or any vanilla JavaScript behavior in this Flask app. Focuses on Intersection Observer patterns, lightweight DOM updates, and preserving the existing theme system."
---

# Frontend patterns for Zenece

## Scope

Use this skill when editing the landing page frontend in [templates/index.html](../../../templates/index.html), [static/js/site.js](../../../static/js/site.js), or [static/css/site.css](../../../static/css/site.css).

## Required conventions

- Prefer vanilla JavaScript and DOM APIs over frameworks or larger UI libraries.
- Use Intersection Observer for reveal animations, active section tracking, and any scroll-driven behavior.
- Do not add window scroll listeners for this page; the project explicitly avoids them.
- Keep CSS variables and theme toggles aligned with the current design system instead of introducing new abstraction layers.
- Preserve the existing markup and naming patterns unless the task explicitly requires a redesign.
- For content-heavy or data-heavy UI, prefer lightweight fetch-based or paginated loading patterns rather than loading everything upfront.

## Working rules

- Update [static/js/site.js](../../../static/js/site.js) for interactive behavior such as theme switching, counts, tabs, or section navigation.
- Update [static/css/site.css](../../../static/css/site.css) for styling only; keep selectors and theme tokens consistent with the current layout.
- Keep changes small and focused; do not refactor unrelated frontend code.
- Validate by running `python app.py` and checking the affected route in the browser, since there is no automated frontend test suite.

## Anti-patterns to avoid

- Avoid custom scroll handlers for lazy reveal or nav tracking.
- Avoid framework migrations or adding dependencies without a clear need.
- Avoid broad refactors that change the site structure or theme system unrelated to the task.

## Good examples in this repo

- Theme buttons in [static/js/site.js](../../../static/js/site.js) update `data-theme` and persist to `localStorage`.
- Section tracking uses `IntersectionObserver` instead of scroll listeners.
- Reveal effects and animated counts also use observer-driven behavior.
