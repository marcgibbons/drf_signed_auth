from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import signing
from django.test import TestCase
from drf_signed_auth.authentication import SignedURLAuthentication
from drf_signed_auth import settings
from model_mommy import mommy
from rest_framework import exceptions
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory


class AuthenticateTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = mommy.make(get_user_model())

        self.sut = SignedURLAuthentication().authenticate

    def test_call_without_signature_param(self):
        """
        Given that the signature is not provided,
        None should be returned.
        """
        request = Request(self.factory.get('/fizz'))
        self.assertIsNone(self.sut(request))

    @patch('drf_signed_auth.signing.UserSigner.unsign')
    def test_signature_unsiged_using_user_signer(self, unsign_mock):
        """
        Given that a signature is provided, the UserSigner
        should decrypt this signature, and if a valid user,
        return.
        """
        signature = 'serenityNow!'
        params = {settings.SIGNED_URL_QUERY_PARAM: signature}
        request = Request(self.factory.get('/', data=params))
        unsign_mock.return_value = self.user
        result = self.sut(request)

        unsign_mock.assert_called_once_with(signature)
        expected = (self.user, None)

        self.assertEqual(expected, result)

    @patch('drf_signed_auth.signing.UserSigner.unsign')
    def test_inactive_user(self, unsign_mock):
        """
        Given that the unsigned user is inactive,
        an AuthenticationFailed exception should be raised.
        """
        self.user.is_active = False
        self.user.save()

        params = {settings.SIGNED_URL_QUERY_PARAM: 'henniganScotch'}
        request = Request(self.factory.get('/', data=params))
        unsign_mock.return_value = self.user

        with self.assertRaises(exceptions.AuthenticationFailed) as cm:
            self.sut(request)

        self.assertEqual('User inactive or deleted.', str(cm.exception))

    @patch('drf_signed_auth.signing.UserSigner.unsign')
    def test_expired_url(self, unsign_mock):
        """
        Given that the signature has expired, an AuthenticationFailed
        exception should be raised.
        """
        unsign_mock.side_effect = signing.SignatureExpired
        params = {settings.SIGNED_URL_QUERY_PARAM: 'puffyShirt'}
        request = Request(self.factory.get('/', data=params))

        with self.assertRaises(exceptions.AuthenticationFailed) as cm:
            self.sut(request)

        self.assertEqual('This URL has expired.', str(cm.exception))

    @patch('drf_signed_auth.signing.UserSigner.unsign')
    def test_bad_signature(self, unsign_mock):
        """
        Given that the signature was malformed, an AuthenticationFailed
        exception should be raised.
        """
        unsign_mock.side_effect = signing.BadSignature
        params = {settings.SIGNED_URL_QUERY_PARAM: 'spongeWorthySignature'}
        request = Request(self.factory.get('/', data=params))

        with self.assertRaises(exceptions.AuthenticationFailed) as cm:
            self.sut(request)

        self.assertEqual('Invalid signature.', str(cm.exception))
