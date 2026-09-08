---
applyTo: "templates/index.html, templates/zenece2.html, static/js/site.js, static/js/zenece2.js, static/css/site.css, static/css/zenece2.css"
description: "Use when editing landing-page templates, theme logic, reveal effects, or any vanilla JavaScript/CSS behavior in this Flask app."
---

# Frontend workflow instructions for Zenece

## Scope

Use this instruction when changing the landing page, theme switching, section navigation, animation behavior, or related styling in the public UI.

## Required conventions

- Prefer Flask + Jinja + vanilla JavaScript over framework-based UIs.
- Keep templates and styles lightweight and maintainable.
- Use `IntersectionObserver` for reveal animations, section tracking, and other scroll-driven UI behavior; avoid window scroll listeners.
- Preserve the existing theme system and CSS variable conventions instead of introducing new abstractions.
- Keep UI behavior aligned with the current markup and naming patterns in [templates/index.html](../../templates/index.html) and [templates/zenece2.html](../../templates/zenece2.html).

## Working rules

- Update [static/js/site.js](../../static/js/site.js) and [static/js/zenece2.js](../../static/js/zenece2.js) for behavior such as theme toggling, counts, reveal effects, and section navigation.
- Update [static/css/site.css](../../static/css/site.css) and [static/css/zenece2.css](../../static/css/zenece2.css) for styling only; keep selectors and theme tokens consistent with the current design system.
- For data-heavy or content-heavy sections, prefer fetch-based incremental loading or paginated patterns rather than loading everything upfront.
- Validate by running `python app.py` and checking the affected page in the browser.

## Anti-patterns to avoid

- Do not add custom window scroll listeners for scroll-driven behavior.
- Do not refactor the page into a framework or add dependencies without a clear need.
- Do not broaden the styling system or change the theme structure unrelated to the task.
- Do not introduce broad DOM abstractions for simple page interactions.

## References

- [templates/index.html](../../templates/index.html)
- [templates/zenece2.html](../../templates/zenece2.html)
- [static/js/site.js](../../static/js/site.js)
- [static/js/zenece2.js](../../static/js/zenece2.js)
- [static/css/site.css](../../static/css/site.css)
- [static/css/zenece2.css](../../static/css/zenece2.css)
- [AGENTS.md](../../AGENTS.md)
