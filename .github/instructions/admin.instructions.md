---
applyTo: "app.py, templates/admin.html, static/js/admin.js"
description: "Use when editing admin routes, settings payload validation, or protected admin interface behavior in this Flask app."
---

# Admin workflow instructions for Zenece

## Scope

Use this instruction when changing the admin dashboard, protected settings updates, or any backend code in [app.py](../../app.py) related to site configuration.

## Required conventions

- Keep the admin flow lightweight and consistent with the current Flask app structure in [app.py](../../app.py).
- Protect every write operation with the `X-Admin-Token` header and compare it against `ADMIN_TOKEN` before accepting any mutation.
- Preserve the existing config types: `string`, `color`, `boolean`, `integer`, `decimal`, and `json`.
- Keep validation explicit and JSON-friendly; reject malformed payloads with clear error responses.
- Keep database writes minimal and transactional when updating settings.

## Working rules

- Prefer direct route handlers in [app.py](../../app.py) over new abstraction layers or service modules.
- When updating config-backed behavior, keep serialization in `public_config()` and the `/api/site-config` response aligned with the same underlying model.
- Ensure the admin UI in [templates/admin.html](../../templates/admin.html) and [static/js/admin.js](../../static/js/admin.js) matches the JSON contract expected by the backend.
- Validate by running `python app.py` and checking the affected admin route in the browser.

## Anti-patterns to avoid

- Do not bypass the token check or accept unauthenticated writes.
- Do not broaden the config model without updating both validation and public serialization together.
- Do not add dependencies or frontend frameworks for a simple admin interface.
- Do not create custom scroll listeners or unrelated UI changes while editing admin behavior.

## References

- [app.py](../../app.py)
- [templates/admin.html](../../templates/admin.html)
- [static/js/admin.js](../../static/js/admin.js)
- [AGENTS.md](../../AGENTS.md)
