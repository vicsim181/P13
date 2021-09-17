#!/bin/sh

set -e

whoami

python manage.py wait_for_db
python manage.py createsuperuser --noinput
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py db_types
