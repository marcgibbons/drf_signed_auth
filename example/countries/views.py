from drf_signed_auth.authentication import SignedURLAuthentication
from rest_framework import viewsets
from rest_framework.settings import api_settings

from . import models, serializers


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [
        SignedURLAuthentication
    ]
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
