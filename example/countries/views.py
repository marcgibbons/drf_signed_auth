from rest_framework import viewsets

from . import models, serializers


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.CountrySerializer
    queryset = models.Country.objects.all()
