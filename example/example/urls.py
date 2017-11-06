from django.conf.urls import include, url
from drf_signed_auth.views import SignUrlView

from . import views


urlpatterns = [
    url(r'', include('countries.urls')),
    url(r'^sign_url/', SignUrlView.as_view(), name='url-signer'),
    url(r'^$', views.index)
]
