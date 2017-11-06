web: gunicorn example.wsgi
release: python manage.py migrate --noinput && python manage.py loaddata countries user
