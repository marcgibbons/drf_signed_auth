from furl import furl
from rest_framework import exceptions, response, views

from . import settings
from .signing import UserSigner


class SignUrlView(views.APIView):
    """
    Adds authentication signature to provided URL

    url -- URL to be wrapped
    """
    param = settings.SIGNED_URL_QUERY_PARAM
    permission_classes = settings.SIGNED_URL_PERMISSION_CLASSES

    def post(self, request):
        url = request.data.get('url')
        if not url:
            raise exceptions.ValidationError('`url` must be provided')

        return response.Response(self.get_signed_url(url))

    def get_signed_url(self, url):
        """
        Returns provided URL with an authentication
        signature.
        """
        signer = UserSigner()
        url = self.request.build_absolute_uri(url)
        signature = signer.sign(user=self.request.user)

        return furl(url).add({self.param: signature}).url
