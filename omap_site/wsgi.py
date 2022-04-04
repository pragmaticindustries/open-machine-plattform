"""
WSGI config for portal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from omap.modules import modules

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omap_site.settings")
modules.configure_modules()

application = get_wsgi_application()
