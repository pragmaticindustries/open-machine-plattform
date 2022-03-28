"""
ASGI config for omap project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from omap.modules import modules

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omap.modules.base_settings")
modules.configure_modules()

application = get_asgi_application()
