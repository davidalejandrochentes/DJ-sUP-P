#!/bin/sh

echo 'Running collecstatic...'
python manage.py collectstatic --no-input --settings=sUP.settings.production

echo 'Applying migrations...'
python manage.py wait_for_db --settings=sUP.settings.production
python manage.py migrate --settings=sUP.settings.production

echo 'Running server...'
gunicorn --env DJANGO_SETTINGS_MODULE=sUP.settings.production sUP.wsgi:application --bind 0.0.0.0:8000