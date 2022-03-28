#!/bin/bash
python manage.py migrate
gunicorn -k uvicorn.workers.UvicornWorker omap.modules.asgi --bind :8000 --enable-stdio-inheritance