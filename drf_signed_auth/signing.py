"""
Contains cryptographic signing of the user model
"""
from django.contrib.auth import get_user_model
from django.core import signing

from . import settings


User = get_user_model()


class UserSigner(signing.TimestampSigner):
    """
    Signs/unsigns user object with an expiry.
    """
    def sign(self, user):
        """
        Creates signatures for user object.
        """
        data = {
            'user_id': user.pk,
            'username': user.get_username()  # Support custom user models
        }

        return super().sign(signing.dumps(data))

    def unsign(self, value, max_age=settings.SIGNED_URL_TTL):
        """
        Returns fresh user object for a valid signature.
        """
        value = super().unsign(value, max_age)
        data = signing.loads(value)
        if not isinstance(data, dict):
            raise signing.BadSignature()

        try:
            user = User.objects.get(pk=data.get('user_id'))
            if user.get_username() != data.get('username'):
                raise User.DoesNotExist()
        except User.DoesNotExist:
            raise signing.BadSignature()

        return user
