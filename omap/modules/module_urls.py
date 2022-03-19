import importlib
import logging

from django.apps import apps
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from omap.modules import modules
from omap.modules.modules import ModuleConfig


def dynamic_url():
    _urlpatterns = [url(r"admin/", admin.site.urls)] + (
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

    # Now add urls from Modules
    for mod in modules.modules():
        mod: ModuleConfig
        if mod.urlpatterns:
            if callable(mod.urlpatterns):
                patterns = mod.urlpatterns()
            else:
                patterns = mod.urlpatterns
            _urlpatterns.extend(patterns)

    logging.debug(f"Patterns: {_urlpatterns}")

    return _urlpatterns


urlpatterns = dynamic_url()
