from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, ShowSubscriptionsViewSet,
                    SubscriptionView)

router_v1 = DefaultRouter()
router_v1.register(
    r'users/subscriptions', ShowSubscriptionsViewSet,
    basename='subscribtions')
router_v1.register(
    'users',
    CustomUserViewSet,
    basename='users'
)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('users/<int:user_id>/subscribe/', SubscriptionView.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
