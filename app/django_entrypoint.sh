#!/bin/sh

echo "Making migrations and migrating the database. "
python manage.py migrate

echo "Run data transfer. "
python sqlite_to_postgres/load_data.py

echo "Create superuser. "
python manage.py createsuperuser --noinput

echo "Collect static files. "
python manage.py collectstatic --noinput

echo "Run uwsgi. "
uwsgi --strict --ini uwsgi.ini

exec "$@"
