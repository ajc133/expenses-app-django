#!/bin/sh
set -eu

# Do at runtime because you have db access then
python manage.py migrate && \
	gunicorn -w 3 --bind 0.0.0.0:8000 splootwyze.wsgi
