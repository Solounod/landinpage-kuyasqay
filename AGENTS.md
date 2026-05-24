# AGENTS.md

## Project
Django 6.0 landing page for a Chilean pastry shop (Kuyasqay). Single Django app under `apps/core/`.

## Commands

```bash
# Dev server (SQLite, DEBUG=True, ALLOWED_HOSTS=['*'])
poetry run python manage.py runserver

# Tests (Django's unittest runner; no tests written yet)
poetry run python manage.py test

# Migrations
poetry run python manage.py makemigrations apps.core
poetry run python manage.py migrate

# Django shell
poetry run python manage.py shell
```

No pytest, no lint/typecheck config, no CI, no pre-commit hooks.

## Settings

`manage.py` overrides `DJANGO_SETTINGS_MODULE` to `config.settings.local` (Django's default behavior would look for `config.settings` — the override here is intentional and required).

- **`local.py`** (default in dev): SQLite, DEBUG=True, `ALLOWED_HOSTS=['*']`, media stored in `media/`.
- **`prod.py`**: PostgreSQL via `DATABASE_URL` env var, Supabase S3 (`django-storages`) for media, Whitenoise for static files (compressed manifest).

## Architecture

Single app: `apps/core/`. Registered in `INSTALLED_APPS` as `"apps.core"` — use this dotted path in management commands and imports (e.g., `from apps.core.models import Product`).

### Models
- `HeroImage` — hero carousel images (auto-converted to WebP on save, max_width=1600)
- `Category` — product categories, slugged
- `Product` — FK to Category, has background_color choices, min_order
- `ProductImage` — FK to Product, max 8 images per product (enforced in `clean()`), auto-WebP (max_width=1200)
- `ProductVariant` — pricing packs per product
- `Review` — customer testimonials, optional image, auto-WebP

### Image optimization
All image fields (HeroImage, ProductImage, Review) run through `apps/core/utils.py:optimize_image()` on save. Uploaded images are converted to WebP (quality=85), EXIF-rotated, and resized. Images are renamed to `.webp` extension. This is triggered by checking `image.name.lower().endswith('.webp')` — if an upload already has a `.webp` extension, it skips re-encoding.

## Dependencies / gotchas

- **`django-storages` is missing from `pyproject.toml`** but imported in `prod.py`. Running prod settings will fail with `ImportError`. Add it before production deployment.
- **`django-jazzmin`** — the pip package is `django-jazzmin` but the Django app label in `INSTALLED_APPS` is `jazzmin` (single 'z').
- **Whitenoise middleware** is commented out in `base.py` but its storage backend is used in `prod.py`. If you uncomment the middleware, it will activate WhiteNoise for all settings modules (including local dev).
- **Tailwind CSS** loaded from CDN (`<script src="https://cdn.tailwindcss.com">`), not built locally. No `package.json` or Node tooling.

## Django Admin (Jazzmin)

Customized via `JAZZMIN_SETTINGS` in `base.py`:
- Model icons use `"core.*"` prefix (not `"apps.core.*"`) because Django's internal app label is `core`.
- `auth.Group` is hidden.
- Model ordering: Product → Category → HeroImage → Review.
- UI Builder enabled.

## Production env vars

```
SECRET_KEY
ALLOWED_HOSTS
DATABASE_URL
SUPABASE_ACCESS_KEY_ID
SUPABASE_SECRET_ACCESS_KEY
SUPABASE_BUCKET_NAME
SUPABASE_S3_ENDPOINT
```

## Locale

`LANGUAGE_CODE = 'es-cl'`, `TIME_ZONE = 'America/Santiago'`. All model verbose names, admin text, and templates are in Spanish.
