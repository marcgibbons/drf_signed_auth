from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core import signing
from django.test import TestCase, override_settings
from drf_signed_auth import settings
from drf_signed_auth.signing import UserSigner
from model_mommy import mommy


class SignTest(TestCase):
    """
    Covers the UserSigner.sign method.
    """
    def setUp(self):
        self.sut = UserSigner().sign

    @patch('django.core.signing.dumps')
    def test_dumps_user_pk_and_user_name(self, mock):
        """
        Asserts that the signature is created using the user's
        primary key and username.
        """
        user = MagicMock()
        self.sut(user)

        mock.assert_called_once_with({
            'user_id': user.pk,
            'username': user.get_username()
        })

    @patch('django.core.signing.dumps')
    @patch('django.core.signing.TimestampSigner.sign')
    def test_signs_result_of_dump(self, sign_mock, dumps_mock):
        """
        Asserts that the django TimestampSigner sign method
        is called using the dumped user data and returned.
        """
        user = MagicMock()
        result = self.sut(user)
        sign_mock.assert_called_once_with(dumps_mock.return_value)

        self.assertEqual(sign_mock.return_value, result)


class UnsignTest(TestCase):
    def setUp(self):
        self.sut = UserSigner().unsign

    def test_unsign_none(self):
        """
        Given a None signature, a BadSignature exception should be
        raised.
        """
        with self.assertRaises(signing.BadSignature):
            self.sut(None)

    def test_unsign_an_invalid_structure(self):
        """
        Given an invalid data type (not a dict), a BadSignature
        exception should be raised.
        """
        signer = signing.TimestampSigner()
        signature = signer.sign(signing.dumps('this is not a dict'))

        with self.assertRaises(signing.BadSignature):
            self.sut(signature)

    def test_unsigns_an_empty_dict(self):
        """
        Given that a dict is returned, but does not have
        appropriate keys, a BadSignature exception should
        raised.
        """
        signer = signing.TimestampSigner()
        signature = signer.sign(signing.dumps({'fizz': 'buzz'}))

        with self.assertRaises(signing.BadSignature):
            self.sut(signature)

    def test_user_does_not_exist(self):
        """
        Given that primary key and username do not match
        an existing user, a BadSignature exception should be
        raised.
        """
        signer = signing.TimestampSigner()
        signature = signer.sign(
            signing.dumps({
                'user_id': 1234,
                'username': 'crazyjoedavaola'
            })
        )

        with self.assertRaises(signing.BadSignature):
            self.sut(signature)

    def test_valid_user_signature(self):
        """
        Given a valid user signature, the user object should
        be returned.
        """
        user = mommy.make(get_user_model())
        signature = UserSigner().sign(user)
        result = self.sut(signature)

        self.assertEqual(user, result)

    @patch('django.core.signing.loads')
    @patch('django.core.signing.TimestampSigner.unsign')
    def test_django_signers_called(self, unsign_mock, loads_mock):
        """
        Asserts that the method calls Django's signers using
        the SIGNED_URL_TTL for the expiry.
        """
        user = mommy.make(get_user_model())
        signature = UserSigner().sign(user)
        loads_mock.return_value = {
            'user_id': user.pk,
            'username': user.get_username()
        }
        self.sut(signature)

        unsign_mock.assert_called_once_with(signature, settings.SIGNED_URL_TTL)

    def test_signing_with_custom_user_model(self):
        """
        Given a custom user model, the signature should sign
        and unsign the user object correctly
        """
        user = mommy.make('unit.CustomUser')

        with override_settings(AUTH_USER_MODEL='unit.CustomUser'):
            signature = UserSigner().sign(user)
            result = self.sut(signature)

        self.assertEqual(user, result)
