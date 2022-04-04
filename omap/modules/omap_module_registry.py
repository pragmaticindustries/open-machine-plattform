from omap.modules.modules import ModuleConfig


class OmapCore(ModuleConfig):
    """
    Example Module for OMAP
    """

    module_name = "omap_core"
    module_version = "0.1.0"
    django_apps = []

    # pip_dependencies = ["django-tailwind==3.1.1"]
    # django_apps = ["omap.frontend", "omap.core", "omap.assets", "tailwind"]
    # settings_entries = {"TAILWIND_APP_NAME": "omap/frontend"}
