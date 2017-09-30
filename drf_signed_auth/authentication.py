"""
Provides Django REST Framework authentication backend
to authenticate signed URL requests.
"""
from django.core import signing
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication, exceptions

from . import settings
from .signing import UserSigner


class SignedURLAuthentication(authentication.BaseAuthentication):
    """
    Authentication backend for signed URLs.
    """
    def authenticate(self, request):
        """
        Returns authenticated user if URL signature is valid.
        """
        signer = UserSigner()
        sig = request.query_params.get(settings.SIGNED_URL_QUERY_PARAM)
        if not sig:
            return

        try:
            user = signer.unsign(sig)
        except signing.SignatureExpired:
            raise exceptions.AuthenticationFailed(_('This URL has expired.'))
        except signing.BadSignature:
            raise exceptions.AuthenticationFailed(_('Invalid signature.'))
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.')
            )

        return (user, None)
