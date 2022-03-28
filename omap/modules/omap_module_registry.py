from omap.modules.modules import ModuleConfig


class OmapCore(ModuleConfig):
    """
    Core Module of the OMAP
    """

    module_name = "omap_core"
    module_version = "0.1.0"
    pip_dependencies = [
        "django-tailwind==3.1.1",
        "django-tag-parser~=3.2",
        # Thumbnails
        "sorl-thumbnail==12.7.0",
        "Pillow==8.1.0",
    ]
    django_apps = [
        "omap.frontend",
        "omap.core",
        "omap.assets",
        "tailwind",
        "sorl.thumbnail",
    ]
    settings_entries = {"TAILWIND_APP_NAME": "omap/frontend"}
