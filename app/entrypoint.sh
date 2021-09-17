#!/bin/sh

set -e

whoami

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py db_types
python manage.py createsuperuser --noinput
