"""
Contains cryptographic signing of the user model
"""
from django.contrib.auth import get_user_model
from django.core import signing

from . import settings


class UserSigner:
    """
    Signs/unsigns user object with an expiry.
    """
    signer_class = signing.TimestampSigner

    def sign(self, user):
        """
        Creates signatures for user object.
        """
        signer = self.signer_class()
        data = {
            'user_id': user.pk,
            'username': user.get_username()  # Support custom user models
        }

        return signer.sign(signing.dumps(data))

    def unsign(self, signature, max_age=settings.SIGNED_URL_TTL):
        """
        Returns fresh user object for a valid signature.
        """
        User = get_user_model()
        signer = self.signer_class()
        data = signing.loads(signer.unsign(signature, max_age))

        if not isinstance(data, dict):
            raise signing.BadSignature()
        try:
            return User.objects.get(**{
                'pk': data.get('user_id'),
                User.USERNAME_FIELD: data.get('username')
            })
        except User.DoesNotExist:
            raise signing.BadSignature()
