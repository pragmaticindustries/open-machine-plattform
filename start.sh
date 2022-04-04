#!/bin/bash
python manage.py migrate
gunicorn -k uvicorn.workers.UvicornWorker omap_site.asgi --bind :8000 --enable-stdio-inheritance
