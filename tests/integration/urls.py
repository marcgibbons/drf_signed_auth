from django.conf.urls import url
from drf_signed_auth.views import SignUrlView

from .views import MeView


urlpatterns = [
    url(r'sign-url/$', SignUrlView.as_view(), name='sign-url'),
    url(r'me/$', MeView.as_view(), name='me'),
]
