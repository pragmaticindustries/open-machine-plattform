from django.urls import include, re_path

from omap.modules.modules import ModuleConfig


class OmapCore(ModuleConfig):
    """
    Core Module of the OMAP
    """

    module_name = "omap_core"
    module_version = "0.1.0"
    pip_dependencies = ["django-tailwind==3.1.1", "django-activity-stream==1.4.0"]
    django_apps = [
        "django.contrib.sites",
        "omap.frontend",
        "omap.core",
        "omap.assets",
        "tailwind",
        "actstream",
    ]
    settings_entries = {"TAILWIND_APP_NAME": "omap/frontend", "SITE_ID": 1}
    urlpatterns = lambda: [  # noqa: E731
        re_path(r"^activity/", include("actstream.urls")),
    ]
