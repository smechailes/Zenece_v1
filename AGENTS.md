# Project Guidelines

## Stack and architecture

- Keep this application lightweight: Flask, SQLAlchemy, Jinja templates, and vanilla HTML/CSS/JavaScript.
- [app.py](app.py) owns application setup, the `SiteConfig` model, startup seeding, config serialization, and the site-variant selector.
- Route handlers are registered through `register_routes`; keep public rendering, `/api/site-config`, `/admin`, and `/admin/settings` behavior aligned with the existing route structure in [routing/routes.py](routing/routes.py).
- The default landing page uses [templates/index.html](templates/index.html), [static/js/site.js](static/js/site.js), and [static/css/site.css](static/css/site.css). The alternate experience uses the corresponding `zenece2` template, script, and stylesheet.

## Project conventions

- Make small, focused changes and preserve the existing template names, CSS variables, and public APIs.
- Keep the two site variants synchronized with the selectors and paths exposed by the app: `/`, `/site/<variant>`, and `/zenece2`.
- Site settings are database-backed. Defaults are seeded only when missing, public values flow through `public_config()`, and supported types are `string`, `color`, `boolean`, `integer`, `decimal`, and `json`.
- Protect every admin settings mutation with `X-Admin-Token` matching `ADMIN_TOKEN`; keep validation explicit and JSON responses stable.
- Use `IntersectionObserver` for reveal, section tracking, and lazy-loading behavior. Do not add window scroll listeners for those workflows.
- Prefer fetch-based incremental loading and paginated queries for content that can grow; do not add a framework or dependency for simple UI behavior.

## Validation

- Set up the environment with `python -m venv .venv`, `source .venv/bin/activate`, and `pip install -r requirements.txt`.
- Run the app with `python app.py`, then check the affected route in a browser or with HTTP requests. There is currently no automated test suite.
- For admin changes, verify unauthorized writes are rejected and authorized requests include the `X-Admin-Token` header.

## Workflow

- Use [scripts/start-task.sh](scripts/start-task.sh) from an up-to-date `main` branch when creating a task branch.
- Follow the branch and Conventional Commit rules in [CONTRIBUTING.md](CONTRIBUTING.md); do not change the release flow unless requested.
