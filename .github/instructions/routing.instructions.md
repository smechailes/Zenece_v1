---
applyTo: "routing/**/*.py"
description: "Use when editing Flask route registration or request handling in the routing package."
---

# Routing instructions for Zenece

- Keep route registration and handlers small, direct, and consistent with the existing Flask app.
- Preserve the public route contract: `/`, `/site/<variant>`, `/zenece2`, and `/api/site-config`.
- Keep the default and `zenece2` variants aligned with the selector and templates they render.
- Protect every mutation under `/admin/settings` with the shared `X-Admin-Token` check before validating or committing data.
- Preserve the existing JSON response and error shapes unless the task explicitly changes the API contract.
- Keep config validation and serialization aligned with `SiteConfig`, `public_config()`, and the supported value types in [app.py](../../app.py).
- Validate route changes by running `python app.py` and checking the affected endpoint with a browser or HTTP request.