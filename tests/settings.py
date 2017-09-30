SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'tests',
    'tests.unit'
]

ROOT_URLCONF = 'tests.integration.urls'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3'}}
