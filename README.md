# Donation and Volunteer Management System

A Django web application for coordinating item donations between donors, administrators, and approved volunteers.

The system supports three role-specific workflows:

- Donors create donation requests and track their donation history.
- Administrators review donation requests, approve or reject volunteers, assign approved volunteers, and monitor delivery status.
- Volunteers collect assigned donations and update collection/delivery progress.

## Architecture Overview

This is a server-rendered Django application. Django handles routing, authentication, forms, business rules, database access, templates, static assets, and admin tooling.

```text
Browser
  -> Django URL router
  -> Role-protected view
  -> Form validation
  -> Selector/service layer
  -> Django ORM models
  -> Template response
```

The code is organized so each layer has a clear responsibility:

- `config/` contains project-level Django configuration.
- `donations/models.py` defines database entities and workflow status enums.
- `donations/forms.py` owns user input validation and form widgets.
- `donations/selectors.py` owns read/query logic.
- `donations/services.py` owns workflow state changes.
- `donations/decorators.py` owns role-based access control.
- `donations/views.py` coordinates requests, forms, permissions, and responses.
- `donations/templates/` contains server-rendered pages.
- `donations/static/` contains CSS, JavaScript, and bundled static assets.

The historical Django app label is still `app` for migration/database compatibility, but the Python package is now named `donations`.

## Project Structure

```text
.
├── config/
│   ├── settings.py          # Environment-driven Django settings
│   ├── urls.py              # Project URL entry point
│   ├── asgi.py              # ASGI application
│   └── wsgi.py              # WSGI application
├── donations/
│   ├── admin.py             # Django admin registration
│   ├── apps.py              # App config, keeps historical label "app"
│   ├── decorators.py        # admin/donor/volunteer access decorators
│   ├── forms.py             # Authentication, registration, profile, donation forms
│   ├── models.py            # Donor, Volunteer, DonationArea, Donation, Gallery
│   ├── selectors.py         # Reusable optimized ORM read queries
│   ├── services.py          # Donation workflow state transitions
│   ├── tests.py             # Security and workflow regression tests
│   ├── urls.py              # App routes
│   ├── views.py             # Request handlers
│   ├── migrations/          # Database migrations
│   ├── static/              # CSS, JS, images
│   └── templates/           # Django templates
├── media/                   # Local uploaded files, ignored by git
├── manage.py                # Django CLI entry point
├── pyproject.toml           # Runtime/dev dependencies and tool config
├── uv.lock                  # Locked dependency graph
├── .env.example             # Environment variable template
└── README.md
```

## Core Data Model

`Donor`
: One-to-one profile for a Django `User` who submits donations.

`Volunteer`
: One-to-one profile for a Django `User` who collects donations. Volunteers must be approved by an admin before they can access volunteer workflows.

`DonationArea`
: Delivery/distribution area managed by administrators.

`Donation`
: Main workflow record. It belongs to a donor and can later be assigned to a volunteer and donation area.

`Gallery`
: Public gallery entry for delivered donations.

## Donation Workflow

1. A donor signs up and logs in.
2. The donor submits a donation request from `donate-now/`.
3. The request starts with status `Pending`.
4. An admin reviews the request.
5. Admin sets the status to `Accept` or `Reject`.
6. Accepted donations can be assigned to an approved volunteer and donation area.
7. Assigned donations move to `Volunteer Allocated`.
8. The volunteer marks the donation as `Donation Received` or `Donation Not Received`.
9. Received donations can be marked `Donation Delivered Successfully`.
10. Delivered donations can be displayed in the public gallery.

## Access Control

Role checks are enforced in `donations/decorators.py`:

- `admin_required`: only staff/superusers can access admin pages.
- `donor_required`: only users with a `Donor` profile can access donor pages.
- `volunteer_required`: only approved volunteers can access volunteer pages.

Object-level checks are enforced in views by filtering through selectors:

- Donors can only view their own donations.
- Volunteers can only view donations assigned to them.
- Admins can view and manage all records.

## Configuration

Copy `.env.example` to `.env` for local development if you use an environment loader, or export the values directly in your shell.

Important variables:

```text
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=
DJANGO_TIME_ZONE=UTC
DJANGO_DB_ENGINE=django.db.backends.sqlite3
DJANGO_DB_NAME=db.sqlite3
DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DJANGO_DEFAULT_FROM_EMAIL=noreply@example.com
```

For production:

- Set `DJANGO_DEBUG=False`.
- Use a strong `DJANGO_SECRET_KEY`.
- Set `DJANGO_ALLOWED_HOSTS` to your real domains.
- Configure HTTPS/security cookie settings.
- Use a production database instead of SQLite.
- Configure a real email backend.
- Serve static/media files through your web server or object storage.

## Installation

This project uses `uv` for reproducible dependency management.

```bash
uv sync --extra dev
```

Expected output includes installed packages such as:

```text
Installed ...
 + django==4.2.x
 + pillow==...
 + pytest-django==...
 + ruff==...
```

If you prefer standard `pip`, create a virtual environment and install from `pyproject.toml`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e ".[dev]"
```

## Database Setup

Run migrations:

```bash
uv run python manage.py migrate
```

Create an admin user:

```bash
uv run python manage.py createsuperuser
```

## Running The Application

Start the development server:

```bash
uv run python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Common route groups:

- Public: `/`, `/gallery/`
- Admin login: `/login-admin/`
- Donor login: `/login-donor/`
- Volunteer login: `/login-volunteer/`
- Django admin: `/admin/`

## Running Checks And Tests

Django system checks:

```bash
uv run python manage.py check
```

Expected output:

```text
System check identified no issues (0 silenced).
```

Run tests:

```bash
uv run python manage.py test
```

Expected output:

```text
Found 4 test(s).
....
OK
```

Run linting:

```bash
uv run ruff check .
```

Expected output:

```text
All checks passed!
```

Format code:

```bash
uv run ruff format .
```

## Development Notes

Use selectors for query reuse:

```python
donations_for_donor(request.user.donor)
donations_by_status(DonationStatus.PENDING)
```

Use services for workflow changes:

```python
review_donation(donation=donation, status=DonationStatus.ACCEPTED)
allocate_donation(donation=donation, area=area, volunteer=volunteer)
```

This keeps views focused on HTTP concerns and makes business logic easier to test.

## Troubleshooting

`ModuleNotFoundError: No module named 'django'`
: Run `uv sync --extra dev`, then use `uv run python ...` commands.

`no such table`
: Run `uv run python manage.py migrate`.

Volunteer cannot log in
: The volunteer account must be approved by an administrator first.

Static files not loading in production
: Run `uv run python manage.py collectstatic` and configure your web server to serve `STATIC_ROOT`.

Uploaded images not showing
: In development, `DEBUG=True` serves `MEDIA_URL`. In production, configure media hosting separately.

`DisallowedHost`
: Add the host to `DJANGO_ALLOWED_HOSTS`.

## Recent Quality Improvements

- Renamed the Django project package from `Donor` to `config`.
- Renamed the app package from `app` to `donations` while preserving the database app label.
- Renamed `form.py` to `forms.py`.
- Renamed dashboard assets to `dashboard.css` and `dashboard.js`.
- Added role-based decorators for admin, donor, and volunteer views.
- Added object-level filtering for donor and volunteer detail pages.
- Removed browser-controlled donor assignment from donation creation.
- Changed deletion to require POST + CSRF.
- Added selectors and services to reduce duplicated query/business logic.
- Added status enums and query indexes.
- Made dashboard CSS responsive and removed global scroll blocking.
- Added tests for critical security behavior.
- Added reproducible dependencies and dev tooling.

## Future Improvements

- Move repeated table/detail templates into reusable includes.
- Add pagination beyond DataTables for large production datasets.
- Add email notifications for volunteer approval and donation status changes.
- Add image validation and upload size limits.
- Add audit history for status transitions.
- Add deployment-specific settings for PostgreSQL, static storage, and structured logging.
