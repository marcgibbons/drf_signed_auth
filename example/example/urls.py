from django.conf.urls import include, url
from django.contrib import admin

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('countries.urls')),
    url(r'^$', views.index)
]
