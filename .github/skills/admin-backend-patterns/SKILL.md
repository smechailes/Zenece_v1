---
name: admin-backend-patterns
description: "Use when working on Flask routes, database-backed config, admin API protections, or release/admin workflow logic in this repository. Focuses on minimal route handlers, X-Admin-Token checks, config serialization, and staying aligned with the current lightweight app structure."
---

# Admin and backend patterns for Zenece

## Scope

Use this skill when editing [app.py](../../../app.py), the admin flow in [templates/admin.html](../../../templates/admin.html), or related backend behavior around configuration updates and protected routes.

## Required conventions

- Keep the Flask app simple and lightweight; avoid unnecessary frameworks or abstraction layers.
- Preserve the existing SQLAlchemy setup and the default start-up seeding behavior in [app.py](../../../app.py).
- Protect admin-only routes and settings updates with the `X-Admin-Token` header and compare it against `ADMIN_TOKEN`.
- Keep validation logic explicit and small; reject malformed payloads with clear JSON errors.
- Support the existing configuration types: `string`, `color`, `boolean`, `integer`, `decimal`, and `json`.
- Keep database writes minimal and transactional for setting updates.

## Working rules

- Prefer direct, readable route handlers in [app.py](../../../app.py) rather than introducing extra service layers.
- When adding or changing config-backed features, update both the model serialization and the public API shape consistently.
- Keep response payloads JSON-friendly and avoid broad API redesigns unless the task explicitly requires it.
- Validate by running `python app.py` and checking the affected endpoint/router behavior directly in the browser or with HTTP requests.

## Anti-patterns to avoid

- Do not remove or bypass the admin-token check.
- Do not add new dependencies for simple backend tasks.
- Do not broaden the configuration model without updating serialization and validation together.
- Do not introduce complex async or background task infrastructure for this small app.

## Good examples in this repo

- The admin protection helper in [app.py](../../../app.py) checks the configured token and the request header before allowing updates.
- Site config public exposure is centralized through `public_config()` and is reused by the template context and `/api/site-config`.
- Default configuration values are created on startup only when they are missing, keeping the database bootstrapping predictable.
