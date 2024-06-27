#!/bin/sh
set -eu
PYTHON="/app/.venv/bin/python"
$PYTHON manage.py migrate
$PYTHON manage.py collectstatic --no-input
$PYTHON manage.py runserver 0.0.0.0:8000
