from django.contrib.auth import get_user_model
from drf_signed_auth import settings, views
from drf_signed_auth.compat import mock
from model_mommy import mommy
from rest_framework.test import APIRequestFactory, APITestCase


class GetSignedUrlTest(APITestCase):
    def setUp(self):
        factory = APIRequestFactory()
        self.request = factory.post('/')
        self.request.user = mommy.make(get_user_model())

        self.sut = views.SignUrlView(request=self.request).get_signed_url

    @mock.patch('drf_signed_auth.signing.UserSigner.sign')
    def test_fixx(self, sign_mock):
        sign_mock.return_value = 'the-returned-signature'
        url = '/my-protected=path?param1=fizz&param2=buzz'
        result = self.sut(url)
        expected = 'http://testserver{url}&{param}={sig}'.format(
            url=url,
            param=settings.SIGNED_URL_QUERY_PARAM,
            sig=sign_mock.return_value
        )

        self.assertEqual(expected, result)
