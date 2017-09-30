import uuid

from django.contrib.auth import get_user_model
from drf_signed_auth.compat import mock
from drf_signed_auth.compat import reverse
from drf_signed_auth.views import SignUrlView
from model_mommy import mommy
from rest_framework.test import APITestCase


class SignUrlViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('sign-url')
        self.client.force_authenticate(mommy.make(get_user_model()))

    def test_when_no_data_is_present(self):
        """
        Given that the `url` is missing in the request POST data,
        a 400 error should be returned.
        """
        response = self.client.post(self.url)
        self.assertEqual(400, response.status_code)

        self.assertEqual(['`url` must be provided'], response.data)

    @mock.patch.object(SignUrlView, 'get_signed_url')
    def test_when_url_is_present(self, sign_mock):
        """
        Given that the `url` has been provided, the response
        should have a status code of 200 and a signed URL should
        be returned.
        """
        url = '/relative-path'
        sign_mock.return_value = str(uuid.uuid4())  # Something random
        response = self.client.post(self.url, data={'url': url})
        self.assertEqual(200, response.status_code)
        sign_mock.assert_called_once_with(url)

        self.assertEqual(sign_mock.return_value, response.data)


class AuthWorklfowTest(APITestCase):
    """
    Executes E2E workflow where:
        1) A URL is signed
        2) The returned URI is followed
        3) The protected resource is rendered
    """
    def setUp(self):
        self.sign_url = reverse('sign-url')  # Signature provider view
        self.me_url = reverse('me')  # Protected view

    def test_me_view_is_not_accessible_if_not_authenticated(self):
        """
        Given that an AnonymousUser requests the Me view,
        a 401 status code should be returned.
        """
        response = self.client.get(self.me_url)
        self.assertEqual(403, response.status_code)

    def test_me_view_is_accessible_given_a_sign_request(self):
        """
        Given that an AnonymousUser requests the Me view,
        and provides a valid signature, a 200 status code
        should be returned with an expected payload.
        """
        user = mommy.make(get_user_model())
        self.client.force_authenticate(user)

        # Get the signature
        response = self.client.post(self.sign_url, data={'url': self.me_url})
        signed_url = response.data

        # Log the user out; access signed URL without state
        self.client.logout()

        # Get protected content
        response = self.client.get(signed_url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            {
                'username': user.username,
                'full_name': user.get_full_name()
            },
            response.data
        )
