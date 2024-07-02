#!/bin/sh
set -eu

# Do at runtime because you have db access then
python manage.py migrate && python manage.py runserver 0.0.0.0:8000
