from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'ingredients',
    IngredientsViewSet,
    basename='ingredients'
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
