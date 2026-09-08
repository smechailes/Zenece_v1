# Deployment

## Render

1. Create a new Web Service connected to this repository.
2. Set the runtime to Python and use Python 3.12 or newer.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app`.
5. Configure these environment variables:
   - `ADMIN_TOKEN`: a long, randomly generated secret.
   - `FLASK_DEBUG`: `false`.
   - `DATABASE_URL`: a persistent database URL. The default SQLite database is suitable only for local development or a persistent disk.
6. Deploy and verify `/`, `/zenece2`, `/api/site-config`, and `/admin`.

Do not commit `.env`. Use [.env.example](.env.example) as the local configuration template. Production startup intentionally fails when `ADMIN_TOKEN` is missing while debug mode is disabled.
