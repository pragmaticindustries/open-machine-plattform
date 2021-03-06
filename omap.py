#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from omap.modules import modules


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omap_site.settings")
    # Here we set the OMAP_MODULES env varible, if not set
    os.environ.setdefault("OMAP_MODULES", "")

    # Here we inject our custom settings
    modules.configure_modules()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
