web: cd example && gunicorn example.wsgi
release: cd example && python manage.py migrate --noinput && python manage.py loaddata countries user token
