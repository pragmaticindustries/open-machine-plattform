from django.apps import AppConfig


class OmapAssetsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "omap.assets"

    url_prefix = "assets"
