import importlib
import logging

from django.apps import apps
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin

from omap.core import urls as core_urls


def dynamic_url():
    _urlpatterns = [path("", include(core_urls)), path(r"admin/", admin.site.urls)] + (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        if settings.MEDIA_ROOT
        else []
    )

    """
    Here, apps are registered automatically with their urls if they have a property "url_prefix" set in their AppConfig
    AND if they have a valid urls.py file which sets a variable urlpatterns
    """
    for config in apps.get_app_configs():
        if hasattr(config, "url_prefix"):
            logging.debug(
                f"Found url_prefix in {config.name}, checking for .urls module"
            )
            urls_path = config.module.__name__ + ".urls"
            try:
                importlib.import_module(urls_path)
            except ModuleNotFoundError:
                logging.debug(f"No url module found under {urls_path}", exc_info=True)
                continue

            logging.debug(
                f"urls.py present under {urls_path}, setting for prefix {config.url_prefix}"
            )
            # Do the include
            _urlpatterns.append(path(config.url_prefix + "/", include(urls_path)))

    logging.debug(f"Patterns: {_urlpatterns}")

    return _urlpatterns


urlpatterns = dynamic_url()
