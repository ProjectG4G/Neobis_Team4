from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import (
    CountryViewSet,
    RegionViewSet,
    CityViewSet,
    DistrictViewSet,
    VillageViewSet,
    GeoDataAPIView,
)

router = SimpleRouter()
router.register('countries', CountryViewSet, basename='country')
router.register('regions', RegionViewSet, basename='region')
router.register('cities', CityViewSet, basename='city')
router.register('districts', DistrictViewSet, basename='district')
router.register('villages', VillageViewSet, basename='village')

urlpatterns = [path('json/', GeoDataAPIView.as_view(), name='geodata_json'), ]
urlpatterns += router.urls
