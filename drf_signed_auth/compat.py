# pylint: disable=W0611
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


try:
    from unittest import mock
except ImportError:
    import mock


try:
    from importlib import reload
except ImportError:
    reload = reload
