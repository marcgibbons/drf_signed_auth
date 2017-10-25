from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register('countries', views.CountryViewSet)

urlpatterns = router.urls
