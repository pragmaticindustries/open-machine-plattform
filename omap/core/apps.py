from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "omap.core"

    url_prefix = "core"

    def ready(self):
        super().ready()
        from actstream import registry
        from django.contrib.auth.models import User

        registry.register(User)
        registry.register(self.get_model("Task"))
