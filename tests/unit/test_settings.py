"""
Tests application settings are connected to Django
settings and have sensible default values.
"""
import importlib

from django.test import TestCase, override_settings
from drf_signed_auth import settings
from rest_framework import permissions


class SettingsTest(TestCase):
    def setUp(self):
        self.sut = settings
        self.addCleanup(lambda: importlib.reload(settings))

    def test_default_ttl(self):
        self.assertEqual(30, settings.SIGNED_URL_TTL)

    def test_ttl_set_from_django_settings(self):
        expected = 9999
        with override_settings(SIGNED_URL_TTL=expected):
            importlib.reload(settings)
            self.assertEqual(expected, settings.SIGNED_URL_TTL)

    def test_default_signature_param(self):
        self.assertEqual('sig', settings.SIGNED_URL_QUERY_PARAM)

    def test_signature_param_from_django_settings(self):
        expected = 'serenity'
        with override_settings(SIGNED_URL_QUERY_PARAM=expected):
            importlib.reload(settings)
            self.assertEqual(expected, settings.SIGNED_URL_QUERY_PARAM)

    def test_default_permission_classes(self):
        expected = [permissions.IsAuthenticated]
        self.assertEqual(expected, settings.SIGNED_URL_PERMISSION_CLASSES)

    def test_permission_classes_from_django_settings(self):
        expected = ['some', 'other', 'classes']
        with override_settings(SIGNED_URL_PERMISSION_CLASSES=expected):
            importlib.reload(settings)
            self.assertEqual(expected, settings.SIGNED_URL_PERMISSION_CLASSES)
