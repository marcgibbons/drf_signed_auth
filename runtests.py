#!/usr/bin/env python
import os
import sys

import coverage
import django
from django.conf import settings
from django.test.utils import get_runner


if __name__ == '__main__':
    cov = coverage.Coverage(auto_data=True, include='drf_signed_auth/*.py')
    cov.start()
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    cov.stop()
    sys.exit(bool(failures))
