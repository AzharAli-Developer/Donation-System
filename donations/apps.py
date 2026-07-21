from django.apps import AppConfig


class DonationsConfig(AppConfig):
    """Application configuration for the donation workflow.

    The historical app label is preserved as ``app`` so existing migrations,
    database table names, and development SQLite data stay compatible after
    renaming the Python package from ``app`` to ``donations``.
    """

    default_auto_field = "django.db.models.BigAutoField"
    label = "app"
    name = "donations"
    verbose_name = "Donations"
