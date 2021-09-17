#!/bin/bash

# set -e

# ls -la /vol/
# ls -la /vol/web

# whoami

# python manage.py wait_for_db
# python manage.py collectstatic --noinput
# python manage.py migrate --noinput
# python manage.py db_types

# gunicorn config.wsgi:application --bind 0.0.0.0:8000
# # uwsgi --socket :9000 --workers 4 --master --enable-threads --module config.wsgi


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"