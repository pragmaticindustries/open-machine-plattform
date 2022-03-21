import os


def setup():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omap.modules.base_settings")
    os.environ.setdefault("OMAP_MODULES", "omap_core")

    from omap.modules import modules

    modules.configure_modules()
