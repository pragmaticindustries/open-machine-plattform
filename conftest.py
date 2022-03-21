import os


def pytest_configure():
    """
    We have to use this custom loading for the django "context"
    as we have no settings.py
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omap.modules.base_settings")
    os.environ.setdefault("OMAP_MODULES", "omap_core")
    from omap.modules import modules

    modules.configure_modules()
